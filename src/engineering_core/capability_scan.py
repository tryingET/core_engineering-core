# summary: Resolves bounded explicit repository populations and aggregates per-repository doctor observations into capability scan reports.
# read_when:
#   - "Changing population input safety, repository limits, scan completeness, or summary counters."
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any, Iterable

from engineering_core.doctor import build_doctor

MAX_REPO_FILE_BYTES = 1_048_576
HARD_MAX_REPOSITORIES = 10_000
MAX_FAILURES = 1_000


class PopulationError(ValueError):
    pass


def _bounded(text: str) -> str:
    raw = text.encode("utf-8")
    if len(raw) > 4096:
        raise PopulationError("text exceeds 4096-byte bound")
    return text


def _resolved_path(value: Path, *, base: Path, where: str) -> Path:
    text = str(value)
    if len(text.encode("utf-8")) > 4096 or any(ord(char) < 32 for char in text):
        raise PopulationError(f"{where} path exceeds bounds or contains control characters")
    try:
        resolved = ((base / value) if not value.is_absolute() else value).resolve()
    except (OSError, ValueError) as exc:
        raise PopulationError(f"unable to resolve {where} path") from exc
    _bounded(str(resolved))
    return resolved


def _repo_file_path(value: Path, *, base: Path) -> Path:
    text = str(value)
    if len(text.encode("utf-8")) > 4096 or any(ord(char) < 32 for char in text):
        raise PopulationError("repo-file path exceeds bounds or contains control characters")
    path = Path(os.path.abspath(base / value if not value.is_absolute() else value))
    _bounded(str(path))
    return path


def _read_repo_file(path: Path) -> list[Path]:
    path = _repo_file_path(path, base=Path.cwd())
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or info.st_size > MAX_REPO_FILE_BYTES:
            raise PopulationError(f"repo file is not a no-follow bounded regular file: {path}")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode) or opened.st_size > MAX_REPO_FILE_BYTES:
                raise PopulationError(f"repo file changed or is not a bounded regular file: {path}")
            raw = os.read(fd, MAX_REPO_FILE_BYTES + 1)
            if os.read(fd, 1):
                raise PopulationError(f"repo file exceeds byte budget: {path}")
        finally:
            os.close(fd)
    except OSError as exc:
        raise PopulationError(f"unable to read repo file {path}: {exc}") from exc
    if len(raw) > MAX_REPO_FILE_BYTES:
        raise PopulationError(f"repo file exceeds byte budget: {path}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PopulationError(f"repo file is not UTF-8: {path}") from exc
    if any(ord(char) < 32 and char not in "\n\r" for char in text):
        raise PopulationError(f"repo file contains control characters: {path}")
    result = []
    for line in text.splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            result.append(_resolved_path(Path(value), base=path.parent, where="repository"))
    return result


def resolve_population(repos: Iterable[Path], repo_files: Iterable[Path], *, cwd: Path | None = None, max_repositories: int = 1000) -> list[Path]:
    if not 1 <= max_repositories <= HARD_MAX_REPOSITORIES:
        raise PopulationError("max repositories must be between 1 and 10000")
    base = (cwd or Path.cwd()).resolve()
    paths = [_resolved_path(item, base=base, where="repository") for item in repos]
    for item in repo_files:
        paths.extend(_read_repo_file(_repo_file_path(item, base=base)))
    unique = sorted(set(paths), key=str)
    if len(unique) > max_repositories:
        raise PopulationError("repository population exceeds configured limit")
    return unique


def _empty_summary() -> dict[str, Any]:
    declaration = {key: 0 for key in ("absent", "valid", "invalid", "unsupported")}
    observation = {key: 0 for key in ("not-declared", "observable", "blocked", "not-observed")}
    evidence = {"not-supplied": 0}
    return {"doctor_status_counts": {key: 0 for key in ("healthy", "degraded", "blocked")}, "capabilities": {name: {"declaration_status_counts": dict(declaration), "observation_status_counts": dict(observation), "evidence_status_counts": dict(evidence)} for name in ("planning", "advisor", "closed_loop")}}


def build_capability_scan(repositories: list[Path], *, repo_root: Path | None = None, prefer_repo: bool = False) -> dict[str, Any]:
    if len(repositories) > HARD_MAX_REPOSITORIES:
        raise PopulationError("repository population exceeds hard limit")
    canonical = sorted({_resolved_path(item, base=Path.cwd(), where="repository") for item in repositories}, key=str)
    names = [str(item) for item in canonical]
    digest = hashlib.sha256(json.dumps(names, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    records, failures = [], []
    for path in canonical:
        if not path.is_dir():
            failures.append({"path": _bounded(str(path)), "code": "repository-unavailable", "message": "repository is not a readable directory"})
            continue
        try:
            records.append(build_doctor(path, repo_root=repo_root, prefer_repo=prefer_repo))
        except (OSError, ValueError) as exc:
            failures.append({"path": _bounded(str(path)), "code": "inspection-failed", "message": _bounded(str(exc))})
        if len(failures) > MAX_FAILURES:
            raise PopulationError("scan failure budget exceeded")
    summary = _empty_summary()
    for record in records:
        summary["doctor_status_counts"][record["status"]] += 1
        for name, result in record["capabilities"].items():
            summary["capabilities"][name]["declaration_status_counts"][result["declaration_status"]] += 1
            summary["capabilities"][name]["observation_status_counts"][result["observation_status"]] += 1
            summary["capabilities"][name]["evidence_status_counts"][result["evidence_status"]] += 1
    return {"schema": "engineering-capability-scan-v1", "authority": "explicit-population static observations; not rollout closure", "population": {"count": len(canonical), "sha256": digest, "repositories": names}, "completeness": "partial" if failures else "complete", "summary": summary, "records": sorted(records, key=lambda item: item["repository"]), "failures": sorted(failures, key=lambda item: (item["path"], item["code"]))}
