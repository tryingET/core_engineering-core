# summary: Validates package-version consistency and Git release ancestry without mutating the repository.
# read_when:
#   - "Changing release versions, tags, main-line ancestry, changelog requirements, or release automation."
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$")
PROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"\s*$', re.MULTILINE)
PACKAGE_VERSION_RE = re.compile(r'^__version__\s*=\s*"([^"]+)"\s*$', re.MULTILINE)
LOCK_PACKAGE_RE = re.compile(
    r'^\[\[package\]\]\nname\s*=\s*"engineering-core"\nversion\s*=\s*"([^"]+)"',
    re.MULTILINE,
)


class ReleaseLineageError(ValueError):
    pass


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int
    prerelease: str | None = None

    @property
    def stable(self) -> bool:
        return self.prerelease is None

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return base if self.prerelease is None else f"{base}-{self.prerelease}"


def parse_version(value: str) -> Version:
    match = SEMVER_RE.fullmatch(value)
    if not match:
        raise ReleaseLineageError(f"invalid semantic version: {value!r}")
    return Version(int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4))


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ReleaseLineageError(f"cannot read {path}: {exc}") from exc


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        env={"GIT_OPTIONAL_LOCKS": "0", "GIT_LITERAL_PATHSPECS": "1"},
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise ReleaseLineageError(f"git {' '.join(args)} failed: {detail}")
    return result


def version_surfaces(root: Path) -> dict[str, str | None]:
    project_match = PROJECT_VERSION_RE.search(_read(root / "pyproject.toml"))
    package_match = PACKAGE_VERSION_RE.search(_read(root / "src/engineering_core/__init__.py"))
    lock_match = LOCK_PACKAGE_RE.search(_read(root / "uv.lock"))
    try:
        root_catalog = json.loads(_read(root / "catalog.json"))
        package_catalog = json.loads(_read(root / "src/engineering_core/catalog.json"))
    except json.JSONDecodeError as exc:
        raise ReleaseLineageError(f"catalog JSON is invalid: {exc}") from exc
    return {
        "pyproject": project_match.group(1) if project_match else None,
        "package": package_match.group(1) if package_match else None,
        "uv-lock": lock_match.group(1) if lock_match else None,
        "catalog": root_catalog.get("version") if isinstance(root_catalog, dict) else None,
        "packaged-catalog": package_catalog.get("version") if isinstance(package_catalog, dict) else None,
        "catalog-projection": "match" if root_catalog == package_catalog else "mismatch",
    }


def stable_tags(root: Path) -> list[tuple[Version, str]]:
    result: list[tuple[Version, str]] = []
    for tag in _git(root, "tag", "--list", "v*", check=False).stdout.splitlines():
        if not tag.startswith("v"):
            continue
        try:
            version = parse_version(tag[1:])
        except ReleaseLineageError:
            continue
        if version.stable:
            result.append((version, tag))
    return sorted(result)


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    return _git(root, "merge-base", "--is-ancestor", ancestor, descendant, check=False).returncode == 0


def _release_notes(root: Path, version: str) -> list[Path]:
    return sorted((root / "docs/releases").glob(f"*-v{version}-local-release.md"))


def _assert_release_documents(root: Path, version: str) -> None:
    changelog = _read(root / "CHANGELOG.md")
    if f"## [{version}]" not in changelog:
        raise ReleaseLineageError(f"CHANGELOG.md has no [{version}] section")
    notes = _release_notes(root, version)
    if not notes:
        raise ReleaseLineageError(f"release notes for {version} are missing")
    required = ("## Title", "## Release body", "### Breaking Changes", "### Verification before tag")
    text = _read(notes[0])
    missing = [section for section in required if section not in text]
    if missing:
        raise ReleaseLineageError(f"release notes for {version} lack: {', '.join(missing)}")


def _assert_catalog_history(root: Path, version: Version, tag: str) -> None:
    path = root / f"catalog-history/{version}.json"
    packaged = root / f"src/engineering_core/catalog-history/{version}.json"
    if not path.exists() or not packaged.exists():
        raise ReleaseLineageError(f"catalog history snapshot for {version} is missing")
    tagged = _git(root, "show", f"{tag}:catalog.json").stdout
    if _read(path) != _read(packaged) or _read(path) != tagged:
        raise ReleaseLineageError(f"catalog history snapshot for {version} does not match {tag}")


def inspect_release_lineage(
    root: Path,
    *,
    mode: str = "ci",
    tag_name: str | None = None,
    main_ref: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    if mode not in {"ci", "release"}:
        raise ReleaseLineageError(f"unknown release-lineage mode: {mode}")

    surfaces = version_surfaces(root)
    project_value = surfaces["pyproject"]
    if not isinstance(project_value, str):
        raise ReleaseLineageError("pyproject.toml has no project version")
    current = parse_version(project_value)
    mismatches = {
        name: value
        for name, value in surfaces.items()
        if name != "catalog-projection" and value != project_value
    }
    if surfaces["catalog-projection"] != "match":
        mismatches["catalog-projection"] = surfaces["catalog-projection"]
    if mismatches:
        raise ReleaseLineageError(f"version surfaces disagree with {project_value}: {mismatches}")

    head = _git(root, "rev-parse", "HEAD").stdout.strip()
    tags = stable_tags(root)
    exact_tag = f"v{current}"
    prior = [(version, tag) for version, tag in tags if version < current]
    equal = [(version, tag) for version, tag in tags if version == current]
    newer = [(version, tag) for version, tag in tags if version > current]
    if newer:
        raise ReleaseLineageError(
            f"project version {current} is older than existing stable tag {newer[-1][1]}"
        )

    latest_prior = prior[-1] if prior else None
    if latest_prior is not None:
        prior_version, prior_tag = latest_prior
        if not _is_ancestor(root, prior_tag, "HEAD"):
            raise ReleaseLineageError(f"latest prior stable tag {prior_tag} is not an ancestor of HEAD")
        _assert_catalog_history(root, prior_version, prior_tag)

    if mode == "release":
        effective_tag = tag_name or exact_tag
        if effective_tag != exact_tag:
            raise ReleaseLineageError(
                f"release tag {effective_tag!r} does not match package version {current}"
            )
        if not equal:
            raise ReleaseLineageError(f"release tag {exact_tag} does not exist")
        tagged_commit = _git(root, "rev-list", "-n", "1", exact_tag).stdout.strip()
        if tagged_commit != head:
            raise ReleaseLineageError(f"{exact_tag} points to {tagged_commit}, not HEAD {head}")
        if main_ref is not None:
            _git(root, "rev-parse", "--verify", main_ref)
            if not _is_ancestor(root, exact_tag, main_ref):
                raise ReleaseLineageError(f"{exact_tag} is not contained in {main_ref}")
    else:
        if equal:
            tagged_commit = _git(root, "rev-list", "-n", "1", exact_tag).stdout.strip()
            if not _is_ancestor(root, tagged_commit, "HEAD"):
                raise ReleaseLineageError(f"existing {exact_tag} is not an ancestor of HEAD")
        else:
            _assert_release_documents(root, str(current))

    return {
        "schema": "engineering-release-lineage-v1",
        "status": "ok",
        "mode": mode,
        "head": head,
        "version": str(current),
        "expected_tag": exact_tag,
        "tag_exists": bool(equal),
        "latest_prior_tag": latest_prior[1] if latest_prior else None,
        "main_ref": main_ref,
        "surfaces": surfaces,
    }
