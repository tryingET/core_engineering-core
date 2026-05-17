#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "engineering-core"
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "src" / "engineering_core" / "__init__.py"
CATALOG = ROOT / "catalog.json"
CHANGELOG = ROOT / "CHANGELOG.md"


def run(args: list[str], *, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    import os

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check, env=merged_env)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def version_from_pyproject() -> str:
    match = re.search(r'^version\s*=\s*"([^"]+)"', read_text(PYPROJECT), re.MULTILINE)
    if not match:
        raise SystemExit("pyproject.toml is missing project version")
    return match.group(1)


def assert_semver(version: str) -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise SystemExit(f"invalid semver-like version: {version}")


def assert_versions_match(version: str) -> None:
    init_text = read_text(INIT)
    catalog = json.loads(read_text(CATALOG))
    if f'__version__ = "{version}"' not in init_text:
        raise SystemExit(f"src/engineering_core/__init__.py does not match {version}")
    if catalog.get("version") != version:
        raise SystemExit(f"catalog.json version {catalog.get('version')!r} does not match {version}")


def tag_exists(tag: str) -> bool:
    result = run(["git", "tag", "--list", tag], check=False)
    return result.stdout.strip() == tag


def release_notes_path(version: str) -> Path:
    release_dir = ROOT / "docs" / "releases"
    existing = sorted(release_dir.glob(f"*-v{version}-local-release.md")) if release_dir.exists() else []
    if existing:
        return existing[0]
    from datetime import date

    return release_dir / f"{date.today().isoformat()}-v{version}-local-release.md"


def migration_path(version: str) -> Path:
    return ROOT / "docs" / "releases" / "migrations" / f"v{version}.md"


def assert_release_docs(version: str) -> None:
    notes = release_notes_path(version)
    if not notes.exists():
        raise SystemExit(f"missing release notes: {notes.relative_to(ROOT)}")
    notes_text = read_text(notes)
    required_sections = ["## Title", "## Release body", "### Breaking Changes", "### Verification before tag"]
    missing = [section for section in required_sections if section not in notes_text]
    if missing:
        raise SystemExit(f"release notes missing sections: {', '.join(missing)}")
    if "### Agent migration notes" in notes_text and "migrations/v" in notes_text and not migration_path(version).exists():
        raise SystemExit(f"release notes link a migration map but {migration_path(version).relative_to(ROOT)} is missing")
    if not CHANGELOG.exists() or f"## [{version}]" not in read_text(CHANGELOG):
        raise SystemExit(f"CHANGELOG.md is missing section for {version}")


def verify(version: str) -> None:
    assert_semver(version)
    assert_versions_match(version)
    assert_release_docs(version)
    commands = [
        [sys.executable, "-m", "py_compile", "src/engineering_core/cli.py"],
        [sys.executable, "scripts/check-justfile-addenda.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ["uv", "run", "engineering-core", "list"],
        ["uv", "run", "engineering-core", "list-disciplines"],
        ["uv", "run", "engineering-core", "show", "ts", "--prefer-repo"],
        ["uv", "run", "engineering-core", "show-discipline", "validation", "--prefer-repo"],
        ["uv", "build"],
    ]
    for command in commands:
        print(f"+ {' '.join(command)}")
        env = {"PYTHONPATH": "src"} if command[:3] == [sys.executable, "-m", "unittest"] else None
        result = run(command, check=False, env=env)
        if result.returncode != 0:
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
            raise SystemExit(result.returncode)
    print(json.dumps({"action": "verify", "version": version, "tag": f"v{version}", "status": "ok"}, indent=2))


def plan(args: argparse.Namespace) -> None:
    version = args.version or version_from_pyproject()
    assert_semver(version)
    status = run(["git", "status", "--short"], check=False).stdout.strip().splitlines()
    payload = {
        "releaseAuthority": "local-git-tag",
        "publishing": "local uv build artifact; no registry publish",
        "packageName": PACKAGE_NAME,
        "version": version,
        "tag": f"v{version}",
        "tagExists": tag_exists(f"v{version}"),
        "dirtyWorktree": bool(status),
        "nextActions": [
            f"python scripts/release-local.py verify --version {version}",
            "git add CHANGELOG.md uv.lock docs/releases scripts/release-local.py README.md",
            f"git commit -m 'chore(release): v{version}'",
            f"git tag -a v{version} -m '{PACKAGE_NAME} v{version}'",
        ],
    }
    print(json.dumps(payload, indent=2))


def tag(args: argparse.Namespace) -> None:
    version = args.version or version_from_pyproject()
    verify(version)
    tag_name = f"v{version}"
    if tag_exists(tag_name):
        raise SystemExit(f"tag already exists: {tag_name}")
    if run(["git", "status", "--short"], check=False).stdout.strip():
        raise SystemExit("worktree must be clean before tagging")
    if args.apply:
        run(["git", "tag", "-a", tag_name, "-m", f"{PACKAGE_NAME} {tag_name}"])
    print(json.dumps({"action": "tag", "applied": args.apply, "tag": tag_name}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Local release workflow for engineering-core")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "verify", "tag"):
        command = sub.add_parser(name)
        command.add_argument("--version")
    sub.choices["tag"].add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.command == "plan":
        plan(args)
    elif args.command == "verify":
        verify(args.version or version_from_pyproject())
    elif args.command == "tag":
        tag(args)


if __name__ == "__main__":
    main()
