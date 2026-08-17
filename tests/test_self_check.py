from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.catalog_sync import main as sync_main
from engineering_core.self_check import main as self_check_main, run_self_check


class SelfCheckTests(unittest.TestCase):
    def test_self_check_passes_for_repository(self) -> None:
        self.assertEqual(run_self_check(REPO_ROOT), [])

    def test_self_check_module_cli(self) -> None:
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["self-check", "--repo-root", str(REPO_ROOT)]), redirect_stdout(stdout):
            self_check_main()
        self.assertIn("engineering-core self-check passed", stdout.getvalue())

    def test_catalog_sync_check(self) -> None:
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["catalog-sync", "--check", "--repo-root", str(REPO_ROOT)]), redirect_stdout(stdout):
            sync_main()
        self.assertIn("catalog projection is current", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
