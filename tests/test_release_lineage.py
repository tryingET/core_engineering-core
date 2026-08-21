from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from engineering_core.release_lineage import ReleaseLineageError, inspect_release_lineage


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def write_version(root: Path, version: str) -> None:
    (root / "src/engineering_core").mkdir(parents=True, exist_ok=True)
    (root / "docs/releases").mkdir(parents=True, exist_ok=True)
    (root / "catalog-history").mkdir(parents=True, exist_ok=True)
    (root / "src/engineering_core/catalog-history").mkdir(parents=True, exist_ok=True)
    (root / "pyproject.toml").write_text(f'[project]\nname="engineering-core"\nversion = "{version}"\n')
    (root / "src/engineering_core/__init__.py").write_text(f'__version__ = "{version}"\n')
    catalog = {"name": "engineering-core", "version": version}
    text = json.dumps(catalog, indent=2) + "\n"
    (root / "catalog.json").write_text(text)
    (root / "src/engineering_core/catalog.json").write_text(text)
    (root / "uv.lock").write_text(f'[[package]]\nname = "engineering-core"\nversion = "{version}"\n')
    (root / "CHANGELOG.md").write_text(f'# Changelog\n\n## [{version}]\n')
    (root / f"docs/releases/2026-08-17-v{version}-local-release.md").write_text(
        "## Title\n\n## Release body\n\n### Breaking Changes\n\n### Verification before tag\n"
    )


class ReleaseLineageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")
        self.default_branch = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        git(self.root, "config", "user.email", "tests@example.invalid")
        git(self.root, "config", "user.name", "Tests")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def commit(self, message: str) -> None:
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", message)

    def test_rejects_version_older_than_existing_tag(self) -> None:
        write_version(self.root, "0.8.0")
        self.commit("0.8.0")
        git(self.root, "tag", "v0.8.0")
        write_version(self.root, "0.3.8")
        self.commit("regression")
        with self.assertRaisesRegex(ReleaseLineageError, "older than"):
            inspect_release_lineage(self.root)

    def test_accepts_next_version_with_tag_ancestry_and_snapshot(self) -> None:
        write_version(self.root, "0.8.0")
        self.commit("0.8.0")
        git(self.root, "tag", "v0.8.0")
        tagged = (self.root / "catalog.json").read_text()
        (self.root / "catalog-history/0.8.0.json").write_text(tagged)
        (self.root / "src/engineering_core/catalog-history/0.8.0.json").write_text(tagged)
        write_version(self.root, "0.9.0")
        # write_version recreates directories but preserves the snapshots.
        self.commit("0.9.0 candidate")
        report = inspect_release_lineage(self.root)
        self.assertEqual(report["latest_prior_tag"], "v0.8.0")
        self.assertFalse(report["tag_exists"])

    def test_rejects_diverged_latest_tag(self) -> None:
        write_version(self.root, "0.8.0")
        self.commit("base")
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        git(self.root, "checkout", "-qb", "release")
        (self.root / "release.txt").write_text("release\n")
        self.commit("release line")
        git(self.root, "tag", "v0.8.0")
        git(self.root, "checkout", "-q", self.default_branch)
        write_version(self.root, "0.9.0")
        self.commit("different line")
        with self.assertRaisesRegex(ReleaseLineageError, "not an ancestor"):
            inspect_release_lineage(self.root)
        self.assertTrue(base)


if __name__ == "__main__":
    unittest.main()
