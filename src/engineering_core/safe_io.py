# summary: "Provides bounded no-follow regular-file reads and duplicate-key-rejecting UTF-8 JSON decoding for untrusted inputs."
# read_when:
#   - "When changing input path bounds, symlink defenses, file identity checks, byte limits, or strict JSON parsing."

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

MAX_PATH_BYTES = 4096


class SafeInputError(ValueError):
    pass


def _bounded_path(path: Path) -> Path:
    text = str(path)
    if not text or len(text.encode("utf-8")) > MAX_PATH_BYTES or any(ord(char) < 32 for char in text):
        raise SafeInputError("input path is empty, over-bound, or contains control characters")
    return path.absolute()


def _open_nofollow(path: Path) -> int:
    path = _bounded_path(path)
    if not path.name:
        raise SafeInputError("input path must identify a file")
    directory_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    file_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        directory_fd = os.open(path.anchor, directory_flags)
    except OSError as exc:
        raise SafeInputError(f"unable to open input root: {path}") from exc
    try:
        for part in path.parts[1:-1]:
            try:
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            except OSError as exc:
                raise SafeInputError(f"symlinked or unavailable parent rejected: {path}") from exc
            os.close(directory_fd)
            directory_fd = next_fd
        try:
            return os.open(path.name, file_flags, dir_fd=directory_fd)
        except OSError as exc:
            raise SafeInputError(f"unable to open no-follow input: {path}") from exc
    finally:
        os.close(directory_fd)


def validate_nofollow_parent(path: Path) -> None:
    path = _bounded_path(path)
    directory_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        directory_fd = os.open(path.anchor, directory_flags)
    except OSError as exc:
        raise SafeInputError(f"unable to open input root: {path}") from exc
    try:
        for part in path.parts[1:-1]:
            try:
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            except OSError as exc:
                raise SafeInputError(f"symlinked or unavailable parent rejected: {path}") from exc
            os.close(directory_fd)
            directory_fd = next_fd
    finally:
        os.close(directory_fd)


def read_bounded_bytes(path: Path, *, max_bytes: int) -> bytes:
    path = _bounded_path(path)
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes < 1:
        raise SafeInputError("max_bytes must be a positive integer")
    fd = _open_nofollow(path)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise SafeInputError(f"input is not a regular file: {path}")
        if before.st_size > max_bytes:
            raise SafeInputError(f"input exceeds {max_bytes} bytes")
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        if identity_before != identity_after:
            raise SafeInputError(f"input changed while reading: {path}")
        if len(raw) > max_bytes:
            raise SafeInputError(f"input exceeds {max_bytes} bytes")
        return raw
    finally:
        os.close(fd)


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object member rejected")
        result[key] = value
    return result


def _reject_nonfinite_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number rejected: {value}")


def read_bounded_json(path: Path, *, max_bytes: int) -> tuple[Any, bytes]:
    raw = read_bounded_bytes(path, max_bytes=max_bytes)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_object_without_duplicates, parse_constant=_reject_nonfinite_constant)
        return value, raw
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError, MemoryError) as exc:
        raise SafeInputError("input is not valid bounded UTF-8 JSON") from exc
