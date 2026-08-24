"""Tests for G2 candidate-bound materialization (task 4980)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g2_materialize.py"
RECORD = ROOT / "docs" / "project" / "v1-g2-materialization.json"

spec = importlib.util.spec_from_file_location("g2_materialize", SCRIPT)
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


class G2MaterializeTests(unittest.TestCase):
    def test_checked_in_record_validates(self):
        r = gm.validate_record(load_record())
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["fixture_count"], 48)
        self.assertEqual(r["matrix_cells"], 49)
        self.assertFalse(r["g2_pass_claimed"])

    def test_cli_validate(self):
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "validate", str(RECORD)],
            capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_fixtures_stay_unassigned(self):
        rec = load_record()
        self.assertTrue(all(f["candidate_binding"] == "unassigned" for f in rec["fixtures"]))
        self.assertTrue(all(v["candidate_commit"] == gm.CANDIDATE_COMMIT
                            for v in rec["validations"]))

    def test_pass_claim_rejected(self):
        rec = load_record()
        rec["g2_pass_claimed"] = True
        with self.assertRaises(gm.ValidationError) as ctx:
            gm.validate_record(rec)
        self.assertEqual(ctx.exception.code, "pass_claimed")

    def test_wrong_candidate_rejected(self):
        rec = load_record()
        rec["candidate_commit"] = "0" * 40
        with self.assertRaises(gm.ValidationError) as ctx:
            gm.validate_record(rec)
        self.assertEqual(ctx.exception.code, "wrong_candidate")

    def test_unbound_materialization_row_rejected(self):
        rec = load_record()
        rec["validations"][0]["candidate_commit"] = "unassigned"
        with self.assertRaises(gm.ValidationError) as ctx:
            gm.validate_record(rec)
        self.assertEqual(ctx.exception.code, "candidate_unbound")

    def test_wheel_smoke_recorded(self):
        rec = load_record()
        self.assertEqual(rec["wheel_smoke"]["status"], "pass")
        self.assertEqual(len(rec["wheel_smoke"]["commands"]), 4)
        self.assertTrue(all(c["pass"] for c in rec["wheel_smoke"]["commands"]))


if __name__ == "__main__":
    unittest.main()
