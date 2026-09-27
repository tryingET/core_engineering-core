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
    AdoptionPlan,
    FileChange,
    apply_plan,
    plan_init,
    plan_migration,
)
from engineering_core.repository_facts import RepositoryPathError
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

    def write_pinned_policy(self, repo: Path) -> None:
        # Given a repo pinned to v0.7.0 through a workstation-local git+file source
        old = "git+file:///home/someone/engineering-core@99290024b78eb6f1665adda6d75d06045b6a9cc2"
        policy = {
            "engineering_core": {
                "tool": "engineering-core",
                "repository": "workspace:/home/someone/engineering-core",
                "ref": "v0.7.0",
                "lane": "py",
                "disciplines": ["validation"],
                "catalog_command": f"uv tool -n run --from '{old}' engineering-core catalog --pretty",
                "list_disciplines_command": f"uv tool -n run --from '{old}' engineering-core list-disciplines",
                "list_templates_command": f"uv tool -n run --from '{old}' engineering-core list-templates",
                "command": f"uv tool -n run --from '{old}' engineering-core show py",
                "release_pin": {
                    "kind": "git-commit",
                    "ref": "v0.7.0",
                    "resolved_commit": "99290024b78eb6f1665adda6d75d06045b6a9cc2",
                    "source": old,
                },
            }
        }
        (repo / "policy").mkdir()
        (repo / "policy" / "engineering-lane.json").write_text(json.dumps(policy), encoding="utf-8")

    def planned_policy(self, plan: AdoptionPlan) -> dict:
        change = next(c for c in plan.changes if c.path.endswith("engineering-lane.json"))
        return json.loads(change.after)["engineering_core"]

    def test_explicit_ref_with_commit_moves_the_whole_pin(self) -> None:
        commit = "3fc8387274dddccbae3d7fab80954ad483c9b681"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.write_pinned_policy(repo)
            # When migrate is asked for v0.12.0 at its release commit (AK6055)
            plan = plan_migration(repo, self.catalog, ref="v0.12.0", ref_commit=commit, force=True)
        ec = self.planned_policy(plan)
        source = f"git+https://github.com/tryingET/core_engineering-core.git@{commit}"
        # Then ref, release_pin, repository and every pinned command move together
        self.assertEqual(ec["ref"], "v0.12.0")
        self.assertEqual(
            ec["release_pin"],
            {"kind": "git-commit", "ref": "v0.12.0", "resolved_commit": commit, "source": source},
        )
        self.assertEqual(ec["repository"], "https://github.com/tryingET/core_engineering-core")
        for key in ("catalog_command", "list_disciplines_command", "list_templates_command", "command"):
            self.assertIn(f"--from '{source}'", ec[key], key)
            self.assertNotIn("git+file", ec[key], key)
        self.assertEqual(plan.conflicts, [])

    def test_explicit_ref_without_commit_refuses_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.write_pinned_policy(repo)
            plan = plan_migration(repo, self.catalog, ref="v0.12.0", force=True)
        # Then the plan is blocked with the command that yields the commit, and the pin stays put
        self.assertTrue(any("--ref-commit" in c and "git ls-remote" in c for c in plan.conflicts), plan.conflicts)
        change = next((c for c in plan.changes if c.path.endswith("engineering-lane.json")), None)
        if change is not None:
            self.assertEqual(json.loads(change.after)["engineering_core"]["ref"], "v0.7.0")

    def test_no_ref_preserves_the_existing_pin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.write_pinned_policy(repo)
            plan = plan_migration(repo, self.catalog, force=True)
        ec = self.planned_policy(plan)
        self.assertEqual(ec["ref"], "v0.7.0")
        self.assertEqual(ec["release_pin"]["ref"], "v0.7.0")
        self.assertEqual(plan.conflicts, [])

    def test_malformed_ref_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.write_pinned_policy(repo)
            with self.assertRaisesRegex(ValueError, "40-character"):
                plan_migration(repo, self.catalog, ref="v0.12.0", ref_commit="3fc8387", force=True)

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

    def test_init_rejects_missing_directory_before_any_plan(self) -> None:
        missing = Path("/this/path/does/not/exist-engineering-core-test")
        with self.assertRaises(RepositoryPathError):
            plan_init(missing, self.catalog)

    def test_init_rejects_parent_traversal_before_any_plan(self) -> None:
        with self.assertRaises(RepositoryPathError):
            plan_init(Path("../../etc/passwd"), self.catalog)

    def test_apply_refuses_escaped_change_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            plan = AdoptionPlan(
                repo=str(repo),
                mode="init",
                lanes=["py"],
                disciplines=["validation"],
                changes=[FileChange("../outside.md", "create", None, "leaked\n")],
                conflicts=[],
            )
            with self.assertRaises(ValueError):
                apply_plan(plan)
            self.assertFalse((Path(tmp).parent / "outside.md").exists())

    def test_cli_init_rejects_traversal_with_no_stdout(self) -> None:
        stdout = io.StringIO()
        with patch.object(
            sys, "argv",
            ["engineering-core", "init", "--repo", "../../etc/passwd", "--format", "json"],
        ), redirect_stdout(stdout), self.assertRaises(SystemExit) as ctx:
            main()
        self.assertNotEqual(ctx.exception.code, 0)
        self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
