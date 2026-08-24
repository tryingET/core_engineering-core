"""Tests for the G0-A2 admission harness (task 4951)."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g0a2_admission.py"
RECORD = ROOT / "docs" / "project" / "v1-g0a2-admission.json"

spec = importlib.util.spec_from_file_location("g0a2_admission", SCRIPT)
ga = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ga)


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


class TemplateTest(unittest.TestCase):
    def test_template_deterministic(self):
        a = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        b = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_template_candidate_independent(self):
        t = ga.build_template()
        self.assertEqual(t["candidate_commit"], ga.UNASSIGNED)
        self.assertEqual(t["package_version"], ga.UNASSIGNED)


class AdmissionTest(unittest.TestCase):
    def test_checked_in_record_passes(self):
        r = ga.validate_admission(load_record(), ROOT)
        self.assertEqual(r["status"], "pass")
        self.assertEqual(len(r["checked_freezes"]), len(ga.REQUIRED_FREEZES))

    def test_cli_validate_repo_record(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", str(RECORD),
             "--repo-root", str(ROOT)],
            capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["status"], "pass")

    def test_early_candidate_assignment_rejected(self):
        rec = load_record()
        rec["candidate_commit"] = "abc123"
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "candidate_field_assigned")

    def test_version_claim_rejected(self):
        rec = load_record()
        rec["package_version"] = "1.0.0"
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertIn(ctx.exception.code, ("candidate_field_assigned", "forbidden_claim"))

    def test_digest_mismatch_rejected(self):
        rec = load_record()
        rec["freezes"]["g1_harness"]["sha256"] = "f" * 64
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "digest_mismatch")

    def test_missing_freeze_rejected(self):
        rec = load_record()
        del rec["freezes"]["impact_matrix"]
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "missing_freeze")

    def test_wrong_population_decision_rejected(self):
        rec = load_record()
        rec["decisions"]["population"] = 0
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "missing_decision")

    def test_template_digest_drift_rejected(self):
        rec = load_record()
        rec["template_digest"] = "0" * 64
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "template_digest_mismatch")


if __name__ == "__main__":
    unittest.main()
