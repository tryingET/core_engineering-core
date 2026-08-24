"""Smoke tests for the G1 replica runner (task 5004)."""

from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g1_run.py"
FANIN = ROOT / "docs" / "project" / "v1-g1-run.json"


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


if __name__ == "__main__":
    unittest.main()
