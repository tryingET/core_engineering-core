"""Tests for G2 additional wheel execution (task 4982)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g2_execute.py"
RECORD = ROOT / "docs" / "project" / "v1-g2-execution.json"

spec = importlib.util.spec_from_file_location("g2_execute", SCRIPT)
ge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ge)


class G2ExecuteTests(unittest.TestCase):
    def test_checked_in_record_validates(self):
        rec = json.loads(RECORD.read_text())
        r = ge.validate_record(rec)
        self.assertEqual(r["status"], "pass")
        self.assertEqual(rec["status"], "pass")
        self.assertEqual(rec.get("failed") or [], [])
        self.assertIn({"entrypoint": "cli_command", "threat_family": "path_attack"}, rec["executed_cells"])
        self.assertFalse(rec["g2_pass_claimed"])

    def test_cli_validate(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "validate", str(RECORD)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_pass_claim_rejected(self):
        rec = json.loads(RECORD.read_text())
        rec["g2_pass_claimed"] = True
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_record(rec)
        self.assertEqual(ctx.exception.code, "pass_claimed")

    def test_wrong_candidate_rejected(self):
        rec = json.loads(RECORD.read_text())
        rec["candidate_commit"] = "0" * 40
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_record(rec)
        self.assertEqual(ctx.exception.code, "wrong_candidate")


if __name__ == "__main__":
    unittest.main()
