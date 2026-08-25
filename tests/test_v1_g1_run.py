"""Tests for the G1 replica runner (tasks 5004, 5037)."""

from __future__ import annotations

import ast
import json
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g1_run.py"
FANIN = ROOT / "docs" / "project" / "v1-g1-run.json"


def load_runner():
    spec = spec_from_file_location("g1_run_under_test", SCRIPT)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class G1RunTests(unittest.TestCase):
    def test_script_parses(self):
        ast.parse(SCRIPT.read_text(encoding="utf-8"))

    def test_fanin_does_not_claim_pass(self):
        rec = json.loads(FANIN.read_text(encoding="utf-8"))
        self.assertFalse(rec["g1_pass_claimed"])
        self.assertFalse(rec["independent_review"])
        self.assertEqual(len(rec["baselines"]), 4)
        self.assertFalse(rec["negative_control"]["mutated"])
        self.assertEqual(rec["candidate_commit"], "b313becf7f1bf5261843d7b29c939b0bc5072ef1")


class ProveActiveResolutionPolarityTests(unittest.TestCase):
    """AK 5037: scanner completeness alone can never pass prove_active_resolution."""

    def setUp(self):
        self.runner = load_runner()

    def test_scanner_green_plus_hard_apply_failure_is_not_pass(self):
        # The exact softwareco gap: scan-adoption completeness=complete while
        # init --apply crashed (exit 1). Must not score pass.
        self.assertEqual(
            self.runner.score_prove_active_resolution(0, 1), "incomplete"
        )

    def test_pass_when_scan_completes_and_apply_applied(self):
        self.assertEqual(self.runner.score_prove_active_resolution(0, 0), "pass")

    def test_pass_when_scan_completes_and_apply_is_structured_refusal(self):
        self.assertEqual(self.runner.score_prove_active_resolution(0, 2), "pass")

    def test_scanner_failure_is_incomplete_regardless_of_apply(self):
        for applied_exit in (0, 1, 2):
            self.assertEqual(
                self.runner.score_prove_active_resolution(1, applied_exit),
                "incomplete",
            )

    def test_journey_note_and_basis_recorded(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("owner-apply polarity", source)
        self.assertIn("[scanned, applied]", source)

    def test_candidate_commit_parameterized_with_historical_default(self):
        # Task 5046: the runner takes an explicit --candidate-commit; the
        # default must stay the historical b313bec pin so the 5004 fan-in
        # remains bit-for-bit reproducible (ambiguity register Q4).
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"--candidate-commit", default=CANDIDATE_COMMIT', source)
        self.assertIn('rec["candidate_commit"] = args.candidate_commit', source)
        self.assertIn('"candidate_commit": CANDIDATE_COMMIT', source)


class ApplyScoringTests(unittest.TestCase):
    """AK 5051: apply exit-2 is a documented structured refusal, not incompleteness."""

    def setUp(self):
        self.runner = load_runner()

    def test_applied_scores_pass(self):
        self.assertEqual(self.runner.score_apply_owner_plan(0), ("pass", False))

    def test_structured_refusal_scores_pass_flagged(self):
        status, refused = self.runner.score_apply_owner_plan(2)
        self.assertEqual(status, "pass")
        self.assertTrue(refused)

    def test_hard_failure_still_fails(self):
        self.assertEqual(self.runner.score_apply_owner_plan(1), ("fail", False))
        self.assertEqual(self.runner.score_apply_owner_plan(3), ("fail", False))


class TreeDigestTests(unittest.TestCase):
    def setUp(self):
        self.runner = load_runner()

    def test_deterministic_and_content_sensitive(self):
        import tempfile, shutil
        root = Path(tempfile.mkdtemp(prefix="ec-tree-digest."))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "a.txt").write_text("one", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "b.txt").write_text("two", encoding="utf-8")
        first = self.runner.tree_digest(root)
        self.assertEqual(first, self.runner.tree_digest(root))
        (root / "a.txt").write_text("changed", encoding="utf-8")
        self.assertNotEqual(first, self.runner.tree_digest(root))


if __name__ == "__main__":
    unittest.main()
