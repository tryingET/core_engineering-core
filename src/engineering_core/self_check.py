from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from engineering_core import __version__
from engineering_core.catalog_model import (
    canonical_catalog_path,
    catalog_projection_matches,
    collection_file_map,
    collection_ids,
    load_catalog,
    validate_catalog,
)

PROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"\s*$', re.MULTILINE)
LOCK_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"\s*$', re.MULTILINE)


def _project_version(repo_root: Path) -> str | None:
    match = PROJECT_VERSION_RE.search((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    return match.group(1) if match else None


def _lock_package_version(repo_root: Path) -> str | None:
    text = (repo_root / "uv.lock").read_text(encoding="utf-8")
    package_marker = '[[package]]\nname = "engineering-core"\n'
    _, separator, tail = text.partition(package_marker)
    if not separator:
        return None
    match = LOCK_VERSION_RE.search(tail)
    return match.group(1) if match else None


def _check_cli_projection(catalog: dict[str, object]) -> list[str]:
    from engineering_core import cli

    expected = {
        "lanes": set(collection_ids(catalog, "lanes")),
        "disciplines": set(collection_ids(catalog, "disciplines")),
        "templates": set(collection_ids(catalog, "templates")),
        "lane-files": collection_file_map(catalog, "lanes"),
        "discipline-files": collection_file_map(catalog, "disciplines"),
        "template-files": collection_file_map(catalog, "templates"),
    }
    actual = {
        "lanes": set(cli.LANES),
        "disciplines": set(cli.DISCIPLINES),
        "templates": set(cli.TEMPLATES),
        "lane-files": dict(cli.LANE_FILES),
        "discipline-files": dict(cli.DISCIPLINE_FILES),
        "template-files": dict(cli.TEMPLATE_FILES),
    }
    return [
        f"self-check.cli-catalog-drift:{name}"
        for name in expected
        if expected[name] != actual[name]
    ]


def run_self_check(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    canonical = canonical_catalog_path(repo_root)
    if not canonical.exists():
        return [f"self-check.missing-canonical-catalog:{canonical}"]

    catalog = load_catalog(repo_root, prefer_repo=True)
    errors = validate_catalog(catalog, repo_root=repo_root, check_paths=True)
    errors.extend(_check_cli_projection(catalog))

    if not catalog_projection_matches(repo_root):
        errors.append("self-check.catalog-projection-drift")

    canonical_catalog = json.loads(canonical.read_text(encoding="utf-8"))
    versions = {
        "package": __version__,
        "pyproject": _project_version(repo_root),
        "uv-lock": _lock_package_version(repo_root),
        "catalog": catalog.get("version"),
        "canonical-catalog": canonical_catalog.get("version"),
    }
    for surface, version in versions.items():
        if version != __version__:
            errors.append(f"self-check.version-mismatch:{surface}:{version}:{__version__}")

    for path in sorted((repo_root / "src" / "engineering_core").rglob("*.py")):
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            errors.append(f"self-check.syntax-error:{path.relative_to(repo_root)}:{exc.lineno}")

    return sorted(set(errors))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an engineering-core checkout.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    errors = run_self_check(Path(args.repo_root))
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("engineering-core self-check passed")


if __name__ == "__main__":
    main()
