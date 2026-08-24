"""Tests for the G1 dependable-adoption proof harness (task 4871)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "dependable_adoption.py"

spec = importlib.util.spec_from_file_location("dependable_adoption", SCRIPT)
da = importlib.util.module_from_spec(spec)
spec.loader.exec_module(da)


def run_cli(*args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=stdin, capture_output=True, text=True,
    )


def make_baseline(bid="b1", group="holdingco", repo="holdingco/fcos-control-board"):
    return {
        "baseline_id": bid,
        "owner_group": group,
        "repository_identity": repo,
        "pinned_revision": "0" * 40,
        "role": "existing_adopter_transition",
        "starting_posture": "v0.9 adopter",
        "owner_task_ref": "ak://task/pending-owner-acceptance",
        "validation_commands": ["just validate"],
        "evidence_custody": "owner-local",
        "isolation_boundary": "disposable replica",
        "rollback_boundary": "replica restore",
        "final_proof_workspace_posture": "disposed",
    }


def make_manifest():
    return {
        "schema": da.SCHEMA,
        "stage": "g1-journey-manifest",
        "template_digest": da.template_digest(),
        "candidate_commit": da.UNASSIGNED,
        "candidate_digest": da.UNASSIGNED,
        "baselines": [
            make_baseline("b1", "holdingco", "holdingco/fcos-control-board"),
            make_baseline("b2", "teachingco", "teachingco/mathe"),
            make_baseline("b3", "teachingco", "teachingco/wib"),
            make_baseline("b4", "softwareco", "softwareco/owned/pi-extensions"),
        ],
        "negative_control": {
            "repository_identity": "healthco/agents",
            "pinned_revision": "1" * 40,
            "expected_result_schema": "missing_absent",
            "declared_mutation": False,
            "declared_execution": False,
        },
        "journeys": [
            {
                "category": cat,
                "baseline_id": "b1",
                "runbook_digest": da.UNASSIGNED,
                "expected_candidate_bytes": da.UNASSIGNED,
                "assertions": {name: {"expected": "bool"} for name in names},
            }
            for cat, names in da.CATEGORY_ASSERTIONS.items()
        ],
    }


def make_envelope(status="pass", category="rollback_recovery"):
    assertions = [
        {"name": n, "expected": True, "observed": True if status == "pass" else False,
         "required": True}
        for n in da.CATEGORY_ASSERTIONS[category]
    ]
    return {
        "schema": da.ENVELOPE_SCHEMA,
        "stage": "g1-journey-envelope",
        "category": category,
        "baseline_id": "b1",
        "owner_group": "holdingco",
        "status": status,
        "assertions": assertions,
        "effects": {"declared_before": [], "declared_after": [],
                    "undeclared_residual": []},
        "digests": {"journey_manifest": "x" * 64, "candidate": da.UNASSIGNED},
        "owner_task_ref": "ak://task/1",
        "review": {"reviewer": "independent-owner-reviewer", "independent_of_producer": True},
        **({"failure_reasons": ["boundary fired"]} if status != "pass" else {}),
    }


class TemplateTest(unittest.TestCase):
    def test_template_covers_ten_categories(self):
        t = da.build_template()
        self.assertEqual(len(t["journey_categories"]), 10)
        self.assertEqual([c["category"] for c in t["journey_categories"]],
                         da.JOURNEY_CATEGORIES)

    def test_template_is_candidate_independent(self):
        t = da.build_template()
        for c in t["journey_categories"]:
            self.assertEqual(c["runbook_digest"], da.UNASSIGNED)
        self.assertEqual(t["candidate_commit"], da.UNASSIGNED)

    def test_template_deterministic(self):
        a = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        b = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_cli_template_contains_digest(self):
        r = run_cli("template")
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)
        self.assertEqual(out["template_digest"], da.template_digest())


class ManifestValidationTest(unittest.TestCase):
    def test_valid_manifest_passes(self):
        result = da.validate_manifest(make_manifest())
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["validated_baselines"], 4)

    def test_missing_category_fails_closed(self):
        m = make_manifest()
        m["journeys"] = m["journeys"][:-1]
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "missing_category")

    def test_unknown_category_fails_closed(self):
        m = make_manifest()
        m["journeys"][0]["category"] = "teleport_the_repo"
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "unknown_category")

    def test_template_digest_drift_fails_closed(self):
        m = make_manifest()
        m["template_digest"] = "f" * 64
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "template_digest_mismatch")

    def test_early_candidate_assignment_fails_closed(self):
        m = make_manifest()
        m["candidate_commit"] = "abc123"
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "candidate_field_assigned")

    def test_local_fallback_declaration_fails_closed(self):
        m = make_manifest()
        m["baselines"][0]["local_checkout_fallback"] = True
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "forbidden_fallback_declared")

    def test_git_file_fallback_nested_fails_closed(self):
        m = make_manifest()
        m["journeys"][0]["resolution"] = {"git_file_resolution": True}
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "forbidden_fallback_declared")

    def test_negative_control_mutation_fails_closed(self):
        m = make_manifest()
        m["negative_control"]["declared_mutation"] = True
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "negative_control_mutated")

    def test_producer_cannot_be_adopter(self):
        m = make_manifest()
        m["baselines"][0]["owner_group"] = "Engineering-Core"
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "producer_as_adopter")

    def test_duplicate_physical_identity_fails_closed(self):
        m = make_manifest()
        m["baselines"][1]["repository_identity"] = m["baselines"][0]["repository_identity"]
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "duplicate_identity")

    def test_too_few_baselines_fails_closed(self):
        m = make_manifest()
        m["baselines"] = m["baselines"][:3]
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "population_too_small")

    def test_missing_frozen_assertion_fails_closed(self):
        m = make_manifest()
        m["journeys"][0]["assertions"].pop(
            da.CATEGORY_ASSERTIONS[m["journeys"][0]["category"]][0])
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "missing_assertion")

    def test_cli_validate_exit_codes(self):
        good = json.dumps(make_manifest())
        r = run_cli("validate", "-", stdin=good)
        self.assertEqual(r.returncode, 0, r.stderr)
        bad = json.dumps({**make_manifest(), "schema": "wrong"})
        r = run_cli("validate", "-", stdin=bad)
        self.assertEqual(r.returncode, 2)
        self.assertIn("schema_mismatch", r.stderr)

    def test_cli_invalid_json_fails_closed(self):
        r = run_cli("validate", "-", stdin="{not json")
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid_json", r.stderr)


class EnvelopeTest(unittest.TestCase):
    def test_pass_envelope_validates(self):
        result = da.validate_envelope(make_envelope())
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["envelope_status"], "pass")

    def test_required_assertion_failure_blocks_pass(self):
        env = make_envelope()
        env["assertions"][0]["observed"] = False
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "required_assertion_failed")

    def test_undeclared_residual_blocks_pass(self):
        env = make_envelope()
        env["effects"]["undeclared_residual"] = ["stray process"]
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "undeclared_residual")

    def test_producer_review_rejected(self):
        env = make_envelope()
        env["review"]["independent_of_producer"] = False
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "review_not_independent")

    def test_invalid_status_rejected(self):
        env = make_envelope(status="mostly-fine")
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "invalid_status")

    def test_narrative_cannot_replace_reasons(self):
        env = make_envelope(status="incomplete")
        env.pop("failure_reasons")
        env["narrative"] = "operator says it went fine"
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "missing_reason")

    def test_unknown_assertion_rejected(self):
        env = make_envelope()
        env["assertions"].append(
            {"name": "vibes_ok", "expected": True, "observed": True, "required": False})
        with self.assertRaises(da.ValidationError) as ctx:
            da.validate_envelope(env)
        self.assertEqual(ctx.exception.code, "unknown_assertion")

    def test_cli_envelope_roundtrip(self):
        r = run_cli("envelope", "-", stdin=json.dumps(make_envelope()))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["envelope_status"], "pass")


if __name__ == "__main__":
    unittest.main()
