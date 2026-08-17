from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.catalog_model import load_catalog
from engineering_core.scan_diagnostics import (
    build_diagnostics,
    evaluate,
    failing_diagnostics,
    load_baseline,
    make_baseline,
)


def record(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "scope": "/workspace/core",
        "path": "service",
        "kind": "repo",
        "status": "partial",
        "lanes": ["ts-frontend"],
        "disciplines": ["validation"],
        "structural_notes": ["missing one or more catalog/list command fields"],
        "semantic_flags": ["missing_expected_discipline:accessibility:ui_or_frontend_surface"],
    }
    value.update(overrides)
    return value


class ScanDiagnosticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog(REPO_ROOT, prefer_repo=True)

    def test_fingerprints_are_stable_and_requirements_are_objective(self) -> None:
        scan = {"records": [record()]}
        first = build_diagnostics(scan, self.catalog)
        second = build_diagnostics(scan, self.catalog)
        self.assertEqual(first, second)
        rules = {item["rule_id"] for item in first}
        self.assertIn("catalog.unsatisfied-requirement", rules)
        self.assertIn("semantic.expected-discipline.accessibility", rules)
        semantic = [item for item in first if item["rule_id"].startswith("semantic.")]
        self.assertTrue(all(item["suppressible"] for item in semantic))

    def test_baseline_only_exposes_new_diagnostics_to_ratchet(self) -> None:
        current = build_diagnostics({"records": [record()]}, self.catalog)
        baseline = make_baseline(current, generated_at="2026-08-17T00:00:00Z")
        evaluation = evaluate(current, baseline=baseline)
        self.assertEqual(evaluation["summary"]["new"], 0)
        self.assertEqual(failing_diagnostics(evaluation, ["error", "warning"]), [])

        expanded = build_diagnostics(
            {
                "records": [
                    record(),
                    record(
                        path="worker",
                        status="missing",
                        lanes=[],
                        disciplines=[],
                        structural_notes=[],
                        semantic_flags=[],
                    ),
                ]
            },
            self.catalog,
        )
        evaluation = evaluate(expanded, baseline=baseline)
        failures = failing_diagnostics(evaluation, ["warning"])
        self.assertTrue(any(item["rule_id"] == "adoption.missing" for item in failures))

    def test_baseline_round_trip(self) -> None:
        diagnostics = build_diagnostics({"records": [record()]}, self.catalog)
        baseline = make_baseline(diagnostics)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            path.write_text(json.dumps(baseline), encoding="utf-8")
            loaded = load_baseline(path)
        self.assertEqual(loaded["issues"], baseline["issues"])


if __name__ == "__main__":
    unittest.main()
