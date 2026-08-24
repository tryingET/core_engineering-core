"""Tests for G4-B non-mutating verification (task 4974)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g4b_verify.py"
RECORD = ROOT / "docs" / "project" / "v1-g4b-verification.json"

spec = importlib.util.spec_from_file_location("g4b_verify", SCRIPT)
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


class G4BTests(unittest.TestCase):
    def test_emit_and_checked_in_record_match_cases(self):
        rec = load_record()
        self.assertEqual(len(rec["suite_replay"]), 12)
        self.assertEqual(rec["accepted_g4_content"], [])
        self.assertEqual(rec["candidate_commit"], gv.CANDIDATE_COMMIT)

    def test_validate_passes(self):
        r = gv.validate_record(load_record(), ROOT)
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["suite_cases"], 12)
        self.assertEqual(r["accepted_g4_content_count"], 0)

    def test_cli_validate(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", str(RECORD),
             "--repo-root", str(ROOT)],
            capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_accepted_content_rejected(self):
        rec = load_record()
        rec["accepted_g4_content"] = [{"path": "catalog.json"}]
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(rec, ROOT)
        self.assertEqual(ctx.exception.code, "accepted_content_not_empty")

    def test_wrong_candidate_rejected(self):
        rec = load_record()
        rec["candidate_commit"] = "0" * 40
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(rec, ROOT)
        self.assertEqual(ctx.exception.code, "wrong_candidate")

    def test_lineage_digest_drift_rejected(self):
        rec = load_record()
        rec["revised_lineage"][0]["cycle_digest"] = "f" * 64
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(rec, ROOT)
        self.assertEqual(ctx.exception.code, "digest_mismatch")

    def test_suite_digest_drift_rejected(self):
        rec = load_record()
        rec["suite_replay"][0]["digest"] = "0" * 64
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(rec, ROOT)
        self.assertEqual(ctx.exception.code, "suite_digest_mismatch")

    def test_incomplete_suite_rejected(self):
        rec = load_record()
        rec["suite_replay"] = rec["suite_replay"][:10]
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(rec, ROOT)
        self.assertEqual(ctx.exception.code, "suite_incomplete")

    def test_template_deterministic(self):
        a = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        b = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)


if __name__ == "__main__":
    unittest.main()
