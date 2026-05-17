from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from engineering_core import __version__
from engineering_core.cli import DISCIPLINES, LANES, main


REPO_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> str:
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["engineering-core", *args]), redirect_stdout(stdout):
            main()
        return stdout.getvalue()

    def test_list(self) -> None:
        output = self.run_cli("list")
        self.assertEqual(output.splitlines(), list(LANES))
        self.assertIn("ts", output)

    def test_list_disciplines(self) -> None:
        output = self.run_cli("list-disciplines")
        self.assertEqual(output.splitlines(), list(DISCIPLINES))
        self.assertIn("validation", output)

    def test_show_ts(self) -> None:
        output = self.run_cli("show", "ts", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("TypeScript engineering lane", output)

    def test_show_ts_frontend(self) -> None:
        output = self.run_cli("show", "ts-frontend", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Frontend Application Addendum", output)

    def test_show_discipline_validation(self) -> None:
        output = self.run_cli("show-discipline", "validation", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Discipline — Validation", output)

    def test_path(self) -> None:
        output = self.run_cli("path", "py", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertEqual(output.strip(), str(REPO_ROOT / "lanes" / "engineering-py.md"))

    def test_discipline_path(self) -> None:
        output = self.run_cli("discipline-path", "validation", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertEqual(output.strip(), str(REPO_ROOT / "disciplines" / "validation.md"))

    def test_no_legacy_cli_alias(self) -> None:
        pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('engineering-core = "engineering_core.cli:main"', pyproject)
        legacy_cli = "tech" + "-" + "stack" + "-" + "core"
        legacy_package = "tech" + "_" + "stack" + "_" + "core"
        self.assertNotIn(legacy_cli, pyproject)
        self.assertNotIn(legacy_package, pyproject)

    def test_version_bumped_for_breaking_rename(self) -> None:
        self.assertEqual(__version__, "0.2.0")


if __name__ == "__main__":
    unittest.main()
