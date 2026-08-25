"""Tests for the public rollback/remove adoption CLIs (task 5050)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engineering_core.adoption import (
    ADOPTION_JOURNAL,
)
from engineering_core.adoption_cli import main as adoption_main


def run_cli(*argv: str) -> tuple[int, dict]:
    import contextlib, io
    buffer = io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(buffer):
            adoption_main(list(argv))
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    try:
        payload = json.loads(buffer.getvalue())
    except json.JSONDecodeError:
        payload = {"raw": buffer.getvalue()}
    return code, payload


class RollbackRemoveTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp(prefix="ec-rollback-test."))
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        (self.repo / "README.md").write_text("owner content\n", encoding="utf-8")
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _init_apply(self):
        code, payload = run_cli(
            "init", "--repo", str(self.repo), "--lane", "py", "--apply",
            "--format", "json",
        )
        return code, payload

    def test_apply_writes_journal_with_exact_transaction(self):
        code, payload = self._init_apply()
        self.assertEqual(code, 0, payload)
        journal_path = self.repo / ADOPTION_JOURNAL
        self.assertTrue(journal_path.is_file())
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        self.assertEqual(journal["schema"], "engineering-core.adoption-journal/1")
        paths = {entry["path"] for entry in journal["changes"]}
        self.assertEqual(paths, {"policy/engineering-lane.json", "docs/engineering.local.md"})
        for entry in journal["changes"]:
            if entry["action"] == "create":
                self.assertIsNone(entry["before_sha256"])
            import hashlib
            actual = hashlib.sha256((self.repo / entry["path"]).read_bytes()).hexdigest()
            self.assertEqual(actual, entry["after_sha256"])

    def test_rollback_restores_absence_and_removes_journal(self):
        self._init_apply()
        code, receipt = run_cli("rollback", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 0, receipt)
        self.assertEqual(receipt["status"], "rolled_back")
        self.assertFalse((self.repo / "policy/engineering-lane.json").exists())
        self.assertFalse((self.repo / "docs/engineering.local.md").exists())
        self.assertFalse((self.repo / ADOPTION_JOURNAL).exists())
        # unrelated owner content untouched
        self.assertEqual((self.repo / "README.md").read_text(encoding="utf-8"), "owner content\n")

    def test_rollback_restores_exact_prior_bytes(self):
        policy = self.repo / "policy/engineering-lane.json"
        policy.parent.mkdir(parents=True, exist_ok=True)
        prior = '{"engineering_core": {"lanes": ["js"]}}\n'
        policy.write_text(prior, encoding="utf-8")
        code, _ = run_cli(
            "init", "--repo", str(self.repo), "--lane", "py", "--apply", "--format", "json",
        )
        self.assertEqual(code, 0)
        self.assertNotEqual(policy.read_text(encoding="utf-8"), prior)
        code, receipt = run_cli("rollback", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 0, receipt)
        self.assertEqual(policy.read_text(encoding="utf-8"), prior)

    def test_rollback_refuses_on_owner_edit_drift(self):
        self._init_apply()
        doc = self.repo / "docs/engineering.local.md"
        doc.write_text(doc.read_text(encoding="utf-8") + "\nowner appended line\n", encoding="utf-8")
        code, receipt = run_cli("rollback", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 2)
        self.assertEqual(receipt["status"], "refused")
        self.assertTrue(any("drift" in reason for reason in receipt["reasons"]))
        # owner edit preserved byte-for-byte
        self.assertIn("owner appended line", doc.read_text(encoding="utf-8"))

    def test_rollback_refuses_without_journal(self):
        code, receipt = run_cli("rollback", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 2)
        self.assertEqual(receipt["status"], "refused")

    def test_remove_deletes_clean_adoption_surfaces(self):
        self._init_apply()
        code, receipt = run_cli("remove", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 0, receipt)
        self.assertEqual(receipt["status"], "removed")
        self.assertFalse((self.repo / "policy/engineering-lane.json").exists())
        self.assertFalse((self.repo / ADOPTION_JOURNAL).exists())
        self.assertTrue((self.repo / "README.md").exists())

    def test_remove_refuses_on_owner_edits_preserving_them(self):
        self._init_apply()
        policy = self.repo / "policy/engineering-lane.json"
        edited = json.loads(policy.read_text(encoding="utf-8"))
        edited["engineering_core"]["owner_deviation"] = true_sentinel()
        policy.write_text(json.dumps(edited, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        code, receipt = run_cli("remove", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 2)
        self.assertEqual(receipt["status"], "refused")
        self.assertTrue(policy.exists())
        self.assertIn("owner_deviation", policy.read_text(encoding="utf-8"))

    def test_remove_refuses_noop_without_adoption(self):
        code, receipt = run_cli("remove", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 2)
        self.assertEqual(receipt["status"], "refused")

    def test_rollback_after_remove_refuses_honestly(self):
        self._init_apply()
        run_cli("remove", "--repo", str(self.repo), "--format", "json")
        code, receipt = run_cli("rollback", "--repo", str(self.repo), "--format", "json")
        self.assertEqual(code, 2)
        self.assertEqual(receipt["status"], "refused")



class EntryRoutingTests(unittest.TestCase):
    def test_console_entry_routes_rollback_and_remove(self):
        # AK 5050 follow-up: the public console entry must dispatch the new
        # commands to the adoption CLI (the freeze defect this test pins).
        source = (Path(__file__).resolve().parents[1]
                  / "src/engineering_core/cli.py").read_text(encoding="utf-8")
        self.assertIn('("init", "migrate", "rollback", "remove")', source)

def true_sentinel() -> bool:
    return True
