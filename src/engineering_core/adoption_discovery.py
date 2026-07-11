# ---
# summary: "Discovers repository and package adoption surfaces while enforcing skip rules, nested-repository ownership, traversal budgets, and budgeted text reads."
# read_when:
#   - "Changing adoption scan traversal modes, excluded directories, package-surface ownership, or depth, file, and byte budget behavior."
# ---
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_SKIP_DIR_NAMES = {
    ".git", ".hg", ".svn", ".autoresearch", ".autoresearch-worktrees",
    ".migration-backup", ".mypy_cache", ".ontology", ".pytest_cache",
    ".ruff_cache", ".tmp", ".venv", ".worktrees", "__pycache__",
    "archive", "backups", "bak", "build", "dist", "node_modules", "out",
    "target", "vendor", "venv",
}
CONTROL_DIR_NAMES = {"contracts", "diary", "docs", "governance", "ontology", "policy", "scripts", "tools"}


class ReadBudgetExceeded(Exception):
    """Raised before a file read would exceed the configured byte budget."""


@dataclass
class BudgetedReader:
    limit: int
    used: int = 0

    def read_text(self, path: Path) -> str:
        size = path.stat().st_size
        if size > self.limit - self.used:
            raise ReadBudgetExceeded(f"read-byte budget reached before reading {path}")
        with path.open("rb") as handle:
            data = handle.read(size)
        self.used += len(data)
        return data.decode("utf-8", errors="replace")


def rel_to(path: Path, scope: Path) -> str:
    try:
        return str(path.resolve().relative_to(scope.resolve())) or "."
    except ValueError:
        return str(path.resolve())


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_SKIP_DIR_NAMES or path.name.startswith(".tmp") or path.name.endswith(".backup")


def has_git_marker(path: Path) -> bool:
    return (path / ".git").exists()


def immediate_repo_roots(scope: Path, *, include_scope_root: bool) -> list[Path]:
    repos: list[Path] = []
    if include_scope_root and has_git_marker(scope):
        repos.append(scope)
    if not scope.exists():
        return repos
    for child in sorted(scope.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or should_skip_dir(child) or child.name in CONTROL_DIR_NAMES:
            continue
        if has_git_marker(child):
            repos.append(child)
    return repos


def recursive_repo_roots(
    scope: Path, *, include_scope_root: bool, max_depth: int | None = None, max_files: int | None = None
) -> tuple[list[Path], list[dict[str, str]], int]:
    repos: list[Path] = []
    omissions: list[dict[str, str]] = []
    visited = 0
    if not scope.exists():
        return repos, omissions, visited
    for root, dirs, files in os.walk(scope, onerror=lambda exc: omissions.append({"path": str(exc.filename), "reason": str(exc)})):
        root_path = Path(root)
        depth = len(root_path.relative_to(scope).parts)
        has_marker = ".git" in dirs or ".git" in files
        dirs[:] = [d for d in dirs if not should_skip_dir(root_path / d)]
        if max_depth is not None and depth >= max_depth:
            if dirs:
                omissions.append({"path": rel_to(root_path, scope), "reason": "depth budget reached"})
            dirs[:] = []
        if max_files is not None and max_files == visited and (files or dirs):
            omissions.append({"path": rel_to(root_path, scope), "reason": "file budget reached"})
            dirs[:] = []
            break
        if max_files is not None and len(files) > max_files - visited:
            visited = max_files
            omissions.append({"path": rel_to(root_path, scope), "reason": "file budget reached"})
            dirs[:] = []
            break
        visited += len(files)
        if (root_path != scope or include_scope_root) and has_marker:
            repos.append(root_path)
    return sorted(set(repos), key=lambda p: rel_to(p, scope)), omissions, visited


def repo_roots(
    scope: Path, *, discovery: str, include_scope_root: bool,
    max_depth: int | None = None, max_files: int | None = None,
) -> tuple[list[Path], list[dict[str, str]], int]:
    if not scope.exists():
        raise FileNotFoundError(f"scan scope does not exist: {scope}")
    if discovery == "recursive":
        repos, omissions, visited = recursive_repo_roots(
            scope, include_scope_root=include_scope_root, max_depth=max_depth, max_files=max_files
        )
    elif discovery == "immediate":
        repos = immediate_repo_roots(scope, include_scope_root=include_scope_root)
        omissions, visited = [], len(repos)
    else:
        raise ValueError(f"unknown repo discovery mode: {discovery}")
    if not repos and not include_scope_root and has_git_marker(scope):
        return [scope], omissions, visited
    return repos, omissions, visited


def is_under(path: Path, ancestor: Path) -> bool:
    try:
        path.resolve().relative_to(ancestor.resolve())
        return True
    except ValueError:
        return False


def _ends_with_path(path: Path, suffix: Path) -> bool:
    return len(path.parts) >= len(suffix.parts) and path.parts[-len(suffix.parts):] == suffix.parts


def surface_roots(
    repo: Path, *, repo_set: set[Path], surface_paths: tuple[Path, ...],
    max_files: int, max_depth: int,
) -> tuple[list[Path], list[dict[str, str]], int]:
    """Discover package surfaces without exceeding the shared file budget."""
    roots: set[Path] = set()
    omissions: list[dict[str, str]] = []
    visited = 0
    repo_resolved = repo.resolve()
    for root, dirs, files in os.walk(
        repo, onerror=lambda exc: omissions.append({"path": str(exc.filename), "reason": str(exc)})
    ):
        root_path = Path(root)
        dirs[:] = [name for name in dirs if not should_skip_dir(root_path / name)]
        depth = len(root_path.relative_to(repo).parts)
        if depth >= max_depth:
            if dirs:
                omissions.append({"path": str(root_path), "reason": "depth budget reached during package discovery"})
            dirs[:] = []
        remaining = max_files - visited
        if remaining == 0 and (files or dirs):
            omissions.append({"path": str(root_path), "reason": "file budget reached during package discovery"})
            dirs[:] = []
            break
        if len(files) > remaining:
            visited += max(0, remaining)
            omissions.append({"path": str(root_path), "reason": "file budget reached during package discovery"})
            dirs[:] = []
            break
        visited += len(files)
        for filename in files:
            surface = root_path / filename
            try:
                relative_file = surface.relative_to(repo)
            except ValueError:
                continue
            matched = next((candidate for candidate in surface_paths if _ends_with_path(relative_file, candidate)), None)
            if matched is None:
                continue
            root_candidate = surface.parents[len(matched.parts) - 1]
            root_resolved = root_candidate.resolve()
            if root_resolved == repo_resolved:
                continue
            nested_repo_owner = any(
                other_repo != repo_resolved
                and is_under(other_repo, repo_resolved)
                and is_under(root_resolved, other_repo)
                for other_repo in repo_set
            )
            if not nested_repo_owner:
                roots.add(root_candidate)
    pruned_roots: list[Path] = []
    for root in sorted(roots, key=lambda p: (len(p.parts), rel_to(p, repo))):
        if any(is_under(root, ancestor) for ancestor in pruned_roots):
            continue
        pruned_roots.append(root)
    return sorted(pruned_roots, key=lambda p: rel_to(p, repo)), omissions, visited
