from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.adoption import (
    MANAGED_MARKER,
    apply_plan,
    plan_init,
    plan_migration,
)
from engineering_core.catalog_model import load_catalog
from engineering_core.cli import main


class AdoptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog(REPO_ROOT, prefer_repo=True)

    def test_init_is_dry_run_until_applied_and_then_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            plan = plan_init(repo, self.catalog)
            self.assertTrue(plan.safe_to_apply)
            self.assertTrue(plan.changed)
            self.assertFalse((repo / "policy" / "engineering-lane.json").exists())
            apply_plan(plan)
            second = plan_init(repo, self.catalog)
            self.assertFalse(second.changed)
            self.assertIn(MANAGED_MARKER, (repo / "docs" / "engineering.local.md").read_text(encoding="utf-8"))

    def test_init_closes_addendum_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            plan = plan_init(
                repo,
                self.catalog,
                lanes=["ts-frontend"],
                disciplines=["validation"],
            )
        self.assertIn("ts", plan.lanes)
        self.assertIn("ts-frontend", plan.lanes)

    def test_unmanaged_doc_is_a_conflict_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs").mkdir()
            (repo / "docs" / "engineering.local.md").write_text("# Hand-written policy\n", encoding="utf-8")
            plan = plan_init(repo, self.catalog, lanes=["py"], disciplines=["validation"])
        self.assertFalse(plan.safe_to_apply)
        self.assertTrue(any("unmanaged" in conflict for conflict in plan.conflicts))

    def test_migration_can_remove_legacy_after_planning_new_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs").mkdir()
            (repo / "policy").mkdir()
            (repo / "docs" / "tech-stack.local.md").write_text("legacy doc\n", encoding="utf-8")
            (repo / "policy" / "stack-lane.json").write_text(
                json.dumps(
                    {
                        "lane": "py",
                        "engineering_core": {"disciplines": ["validation", "testing"]},
                    }
                ),
                encoding="utf-8",
            )
            plan = plan_migration(repo, self.catalog, remove_legacy=True)
            self.assertTrue(plan.safe_to_apply)
            apply_plan(plan)
            self.assertTrue((repo / "policy" / "engineering-lane.json").exists())
            self.assertFalse((repo / "policy" / "stack-lane.json").exists())
            self.assertFalse((repo / "docs" / "tech-stack.local.md").exists())

    def test_cli_init_json_is_dry_run_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            stdout = io.StringIO()
            with patch.object(
                sys,
                "argv",
                [
                    "engineering-core",
                    "init",
                    "--repo",
                    str(repo),
                    "--lane",
                    "py",
                    "--discipline",
                    "validation",
                    "--format",
                    "json",
                    "--repo-root",
                    str(REPO_ROOT),
                    "--prefer-repo",
                ],
            ), redirect_stdout(stdout):
                main()
            result = json.loads(stdout.getvalue())
            self.assertFalse(result["applied"])
            self.assertFalse((repo / "policy" / "engineering-lane.json").exists())


if __name__ == "__main__":
    unittest.main()
