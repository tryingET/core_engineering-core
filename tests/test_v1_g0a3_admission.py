"""Tests for the G0-A3 candidate-admission harness (task 4955)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g0a3_admission.py"
RECORD = ROOT / "docs" / "project" / "v1-g0a3-admission.json"

spec = importlib.util.spec_from_file_location("g0a3_admission", SCRIPT)
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

    def test_template_leaves_candidate_unassigned(self):
        t = ga.build_template()
        self.assertEqual(t["candidate_commit"], ga.UNASSIGNED)
        self.assertEqual(t["package_version"], ga.UNASSIGNED)


class AdmissionTest(unittest.TestCase):
    def test_checked_in_record_passes(self):
        r = ga.validate_admission(load_record(), ROOT)
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["candidate_task_id"], 4876)
        self.assertEqual(r["accepted_g4_content_count"], 0)
        self.assertGreaterEqual(r["revised_lineage_count"], 3)

    def test_cli_validate(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", str(RECORD),
             "--repo-root", str(ROOT)],
            capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_early_version_claim_rejected(self):
        rec = load_record()
        rec["package_version"] = "1.0.0"
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertIn(ctx.exception.code, ("candidate_field_assigned", "forbidden_claim"))

    def test_main_target_rejected(self):
        rec = load_record()
        rec["target_channel"] = "main"
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "target_is_main")

    def test_wrong_candidate_task_rejected(self):
        rec = load_record()
        rec["candidate_task_id"] = 1
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "wrong_candidate_task")

    def test_empty_lineage_rejected(self):
        rec = load_record()
        rec["revised_lineage"] = []
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "lineage_too_small")

    def test_digest_mismatch_rejected(self):
        rec = load_record()
        rec["bindings"]["g0a2_admission"]["sha256"] = "f" * 64
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "digest_mismatch")

    def test_allowlist_drift_rejected(self):
        rec = load_record()
        rec["path_allowlist"] = rec["path_allowlist"] + ["secrets/**"]
        with self.assertRaises(ga.ValidationError) as ctx:
            ga.validate_admission(rec, ROOT)
        self.assertEqual(ctx.exception.code, "allowlist_mismatch")


if __name__ == "__main__":
    unittest.main()
