# summary: "Extracts bounded no-follow repository evidence and deterministic manifest, policy, and local-document facts for planning."
# read_when:
#   - "Changing repository-facts schema, safe path traversal, evidence budgets, manifest inference inputs, diagnostics, or fact digests."

from __future__ import annotations

import errno
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

FACT_SCHEMA = "repository-facts-v1"
_MANIFESTS = ("pyproject.toml", "package.json", "tsconfig.json", "Cargo.toml", "go.mod", "mix.exs")
MAX_FILE_BYTES = 1_048_576
MAX_TOTAL_BYTES = 4_194_304


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _evidence(path: str, data: bytes, kind: str) -> dict[str, Any]:
    return {"kind": kind, "path": path, "sha256": _sha256(data), "size": len(data)}


def _read_regular_file(root: Path, relative: str, remaining: int) -> tuple[bytes | None, str | None]:
    """Open each path component without following links, then perform a bounded read."""
    cloexec = getattr(os, "O_CLOEXEC", 0)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory = getattr(os, "O_DIRECTORY", 0)
    opened: list[int] = []
    try:
        parent = os.open(root, os.O_RDONLY | directory | cloexec)
        opened.append(parent)
        parts = relative.split("/")
        for component in parts[:-1]:
            try:
                info = os.stat(component, dir_fd=parent, follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    return None, "file-symlink-rejected"
                if not stat.S_ISDIR(info.st_mode):
                    return None, "file-not-regular"
                child = os.open(component, os.O_RDONLY | directory | cloexec | nofollow, dir_fd=parent)
            except FileNotFoundError:
                return None, None
            except OSError as exc:
                return None, "file-symlink-rejected" if exc.errno == errno.ELOOP else "file-unreadable"
            opened.append(child)
            parent = child
        try:
            initial = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return None, None
        if stat.S_ISLNK(initial.st_mode):
            return None, "file-symlink-rejected"
        if not stat.S_ISREG(initial.st_mode):
            return None, "file-not-regular"
        try:
            fd = os.open(parts[-1], os.O_RDONLY | cloexec | nofollow | getattr(os, "O_NONBLOCK", 0), dir_fd=parent)
        except FileNotFoundError:
            return None, None
        except OSError as exc:
            return None, "file-symlink-rejected" if exc.errno == errno.ELOOP else "file-unreadable"
        opened.append(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            return None, "file-not-regular"
        limit = min(MAX_FILE_BYTES, max(remaining, 0))
        if info.st_size > limit:
            return None, "file-budget-exceeded"
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(fd, min(65_536, limit + 1 - size))
            if not chunk:
                return b"".join(chunks), None
            chunks.append(chunk)
            size += len(chunk)
            if size > limit:
                return None, "file-budget-exceeded"
    except OSError:
        return None, "file-unreadable"
    finally:
        for fd in reversed(opened):
            os.close(fd)


def extract_repository_facts(repo: Path) -> dict[str, Any]:
    """Read a fixed, byte-bounded set of declarative regular files; execute nothing."""
    root = repo.resolve()
    evidence: list[dict[str, Any]] = []
    diagnostics: list[dict[str, str]] = []
    consumed = 0

    def read(relative: str, kind: str) -> bytes | None:
        nonlocal consumed
        data, error = _read_regular_file(root, relative, MAX_TOTAL_BYTES - consumed)
        if error:
            diagnostics.append({
                "code": error,
                "message": f"{relative} was omitted from repository facts ({error}).",
                "path": relative,
                "severity": "warning",
            })
            return None
        if data is not None:
            consumed += len(data)
            evidence.append(_evidence(relative, data, kind))
        return data

    manifests: list[str] = []
    inferred: list[str] = []
    mapping = {"pyproject.toml": "py", "package.json": "ts", "tsconfig.json": "ts", "Cargo.toml": "rust", "go.mod": "go", "mix.exs": "elixir"}
    package: Any = None
    for name in _MANIFESTS:
        data = read(name, "manifest")
        if data is None:
            continue
        manifests.append(name)
        inferred.append(mapping[name])
        if name == "package.json":
            try:
                package = json.loads(data)
                if not isinstance(package, dict):
                    raise ValueError("root must be an object")
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                diagnostics.append({"code": "manifest-malformed", "message": f"package.json: {exc}", "path": name, "severity": "warning"})
    if isinstance(package, dict):
        dependencies: dict[str, Any] = {}
        for key in ("dependencies", "devDependencies"):
            value = package.get(key, {})
            if isinstance(value, dict):
                dependencies.update(value)
        if any(item in dependencies for item in ("react", "vue", "svelte", "vite", "@vitejs/plugin-react")):
            inferred.append("ts-frontend")

    policy_name = "policy/engineering-lane.json"
    policy_data = read(policy_name, "policy")
    policy_text: str | None = None
    if policy_data is not None:
        try:
            policy_text = policy_data.decode("utf-8")
        except UnicodeDecodeError:
            diagnostics.append({"code": "policy-unreadable", "message": "policy/engineering-lane.json is not UTF-8.", "path": policy_name, "severity": "error"})
    guidance_candidates = ("docs/engineering.local.md", ".codex/engineering.local.md", ".claude/docs/engineering.local.md")
    local_docs = [name for name in guidance_candidates if read(name, "local-guidance") is not None]
    policy_observed = policy_data is not None or any(item["path"] == policy_name for item in diagnostics)
    result: dict[str, Any] = {
        "schema": FACT_SCHEMA,
        "repo": ".",
        "manifests": sorted(manifests),
        "inferred_lanes": sorted(set(inferred)),
        "policy": {"path": policy_name, "present": policy_observed, "text": policy_text},
        "local_guidance": sorted(local_docs),
        "evidence": sorted(evidence, key=lambda item: (item["path"], item["kind"])),
        "diagnostics": sorted(diagnostics, key=lambda item: (item["code"], item["path"], item["message"])),
        "read_limits": {"max_file_bytes": MAX_FILE_BYTES, "max_total_bytes": MAX_TOTAL_BYTES, "bytes_read": consumed},
    }
    digest_input = {key: value for key, value in result.items() if key != "policy"}
    digest_input["policy"] = {"path": result["policy"]["path"], "present": result["policy"]["present"]}
    result["digest"] = _sha256(json.dumps(digest_input, sort_keys=True, separators=(",", ":")).encode())
    return result
