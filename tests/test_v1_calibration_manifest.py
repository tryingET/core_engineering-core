"""Tests for the G3 evidence-calibration manifest validator (task 4873)."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "calibration_manifest.py"

spec = importlib.util.spec_from_file_location("calibration_manifest", SCRIPT)
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

FAMILIES = [
    {"family_id": "fam-a", "identity": "model-x-2026-08"},
    {"family_id": "fam-b", "identity": "model-y-2026-08"},
]
OWNER_WEIGHTS = [
    {"owner_group": "holdingco", "top_level_weight": 1.0, "baseline_model_weights": [
        {"baseline": "fcos", "family": "fam-a", "weight": 0.5},
        {"baseline": "fcos", "family": "fam-b", "weight": 0.5},
    ]},
    {"owner_group": "teachingco", "top_level_weight": 1.0, "baseline_model_weights": [
        {"baseline": "mathe", "family": "fam-a", "weight": 0.5},
        {"baseline": "wib", "family": "fam-b", "weight": 0.5},
    ]},
    {"owner_group": "softwareco", "top_level_weight": 1.0, "baseline_model_weights": [
        {"baseline": "pi-extensions", "family": "fam-a", "weight": 0.25},
        {"baseline": "pi-extensions", "family": "fam-b", "weight": 0.75},
    ]},
]
SAFETY = [
    {"owner_group": o["owner_group"], "base_model_family": f["family_id"]}
    for o in OWNER_WEIGHTS for f in FAMILIES
]


def authored_manifest():
    t = cm.build_template()
    return {
        "schema": cm.SCHEMA,
        "stage": "g3-protocol-manifest",
        "protocol_stage": "authored",
        "template_digest": cm.template_digest(),
        "sections": copy.deepcopy(t["sections"]),
    }


def accepted_manifest():
    m = authored_manifest()
    m["protocol_stage"] = "accepted"
    s = m["sections"]
    for section, field in cm.MEASURED_FIELDS:
        s[section][field] = "frozen-value"
    s["model_identity"]["families"] = copy.deepcopy(FAMILIES)
    s["weighting"]["owner_weights"] = copy.deepcopy(OWNER_WEIGHTS)
    s["harm_safety"]["safety_set"] = copy.deepcopy(SAFETY)
    s["calibration"]["reference_forecast"] = "disjoint_development"
    return m


class TemplateTest(unittest.TestCase):
    def test_template_deterministic(self):
        a = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        b = subprocess.run([sys.executable, str(SCRIPT), "template"],
                           capture_output=True, text=True)
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_all_measured_values_unassigned_at_authored(self):
        t = cm.build_template()
        for section, field in cm.MEASURED_FIELDS:
            self.assertEqual(t["sections"][section][field], cm.UNASSIGNED)


class AuthoredStageTest(unittest.TestCase):
    def test_authored_manifest_passes(self):
        r = cm.validate_manifest(authored_manifest())
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["protocol_stage"], "authored")

    def test_early_measured_value_rejected(self):
        m = authored_manifest()
        m["sections"]["power"]["total_per_cell_sample"] = 48
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "measured_value_assigned_early")

    def test_missing_section_rejected(self):
        m = authored_manifest()
        del m["sections"]["privacy_manifest"]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "missing_section")

    def test_authority_claim_rejected(self):
        m = authored_manifest()
        m["sections"]["result_bindings"]["release_authority"] = True
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "authority_claim")

    def test_raw_snapshot_transmission_rejected(self):
        m = authored_manifest()
        m["sections"]["privacy_manifest"]["raw_cross_owner_snapshot_transmitted"] = True
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "raw_snapshot_transmission")

    def test_privacy_transfer_missing_field_rejected(self):
        m = authored_manifest()
        t = {f: "x" for f in cm.PRIVACY_REQUIRED_FIELDS}
        t["training_use_prohibited"] = True
        del t["retention_deletion"]
        m["sections"]["privacy_manifest"]["transfers"] = [t]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "privacy_field_missing")

    def test_training_use_allowed_rejected(self):
        m = authored_manifest()
        t = {f: "x" for f in cm.PRIVACY_REQUIRED_FIELDS}
        t["training_use_prohibited"] = False
        m["sections"]["privacy_manifest"]["transfers"] = [t]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "training_use_not_prohibited")

    def test_optional_stopping_rejected(self):
        m = authored_manifest()
        m["sections"]["population_design"]["stopping_rule"] = "optional_after_peak"
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "optional_stopping")

    def test_non_disjoint_split_rejected(self):
        m = authored_manifest()
        m["sections"]["population_design"]["development_confirmatory_split"] = "shared"
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "split_not_disjoint")


class AcceptedStageTest(unittest.TestCase):
    def test_accepted_manifest_passes(self):
        r = cm.validate_manifest(accepted_manifest())
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["protocol_stage"], "accepted")

    def test_unfrozen_measured_value_rejected(self):
        m = accepted_manifest()
        m["sections"]["power"]["power_analysis"] = cm.UNASSIGNED
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "missing_frozen_value")

    def test_single_model_family_rejected(self):
        m = accepted_manifest()
        m["sections"]["model_identity"]["families"] = FAMILIES[:1]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "model_diversity_insufficient")

    def test_variant_counted_as_family_rejected(self):
        m = accepted_manifest()
        m["sections"]["model_identity"]["families"] = [
            FAMILIES[0],
            {"family_id": "fam-a-var", "identity": "model-x-2026-08@t0.2",
             "is_variant_of_another_family": True},
        ]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "variant_counted_as_diversity")

    def test_unequal_owner_weights_rejected(self):
        m = accepted_manifest()
        m["sections"]["weighting"]["owner_weights"][1]["top_level_weight"] = 2.0
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "unequal_owner_weights")

    def test_within_owner_weights_not_summing_rejected(self):
        m = accepted_manifest()
        m["sections"]["weighting"]["owner_weights"][0]["baseline_model_weights"][0]["weight"] = 0.9
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "weights_do_not_sum_to_one")

    def test_uncovered_safety_cell_rejected(self):
        m = accepted_manifest()
        m["sections"]["harm_safety"]["safety_set"] = SAFETY[:-1]
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "safety_cell_uncovered")

    def test_unjustified_constant_reference_rejected(self):
        m = accepted_manifest()
        m["sections"]["calibration"]["reference_forecast"] = "constant_0.5"
        m["sections"]["calibration"]["reference_forecast_justification"] = "none"
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "unjustified_constant_reference")

    def test_template_digest_drift_rejected(self):
        m = accepted_manifest()
        m["template_digest"] = "f" * 64
        with self.assertRaises(cm.ValidationError) as ctx:
            cm.validate_manifest(m)
        self.assertEqual(ctx.exception.code, "template_digest_mismatch")


class CliTest(unittest.TestCase):
    def test_cli_validate_accepted_roundtrip(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "validate", "-"],
                           input=json.dumps(accepted_manifest()),
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], "pass")

    def test_cli_invalid_json_fails_closed(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "validate", "-"],
                           input="{bad", capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid_json", r.stderr)


if __name__ == "__main__":
    unittest.main()
