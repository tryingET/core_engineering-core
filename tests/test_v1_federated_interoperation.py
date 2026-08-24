"""Tests for the G2 federated-interoperation conformance harness (task 4872)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "federated_interoperation.py"

spec = importlib.util.spec_from_file_location("federated_interoperation", SCRIPT)
fi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fi)


def run_cli(mode, stdin=None):
    argv = [sys.executable, str(SCRIPT), mode]
    if stdin is not None:
        argv.append("-")
    return subprocess.run(argv, input=stdin, capture_output=True, text=True)


def make_fixture(cls="canonical_candidate_v1", outcome="pass", **over):
    f = {
        "schema": fi.SCHEMA,
        "stage": "g2-fixture-instance",
        "fixture_class": cls,
        "expected_outcome": outcome,
        "boundary": "ingress_parse" if outcome == "fail_at_boundary" else None,
        "diagnostics": {"sanitized": True, "contains_private_metadata": False},
        "candidate_binding": fi.UNASSIGNED,
    }
    f.update(over)
    return f


def make_negotiation(selected="1.2", replay=False, stripped=False, parse_error=False):
    return {
        "schema": fi.SCHEMA,
        "stage": "g2-negotiation-transcript",
        "offer": {
            "peer_identities": ["peer-a"],
            "offer_id": "offer-1",
            "freshness_scope": "2026-08-24T00:00:00Z/PT1H",
            "replay_scope": "offer-1:once",
            "channel_binding": "artifact-digest",
            "payload_digest": "a" * 64,
            "offered_versions": ["1", "1.1", "1.2"],
        },
        "allowlist": ["1", "1.1", "1.2"],
        "floor": "1",
        "result": {
            "selected_version": selected,
            "replay_detected": replay,
            "offer_stripped": stripped,
            "parse_error": parse_error,
            "payload_digest_bound": True,
            "full_offer_bound": True,
        },
    }


def make_adapter(**over):
    rec = {
        "schema": fi.SCHEMA,
        "stage": "g2-adapter-conversion",
        "conversion_site": "bounded_ingress",
        "input_digest": "b" * 64,
        "output_digest": "c" * 64,
        "adapter_executable_digest": "d" * 64,
        "trust_decision": "trusted",
        "identity_version": "1",
        "defaults": {},
        "transformations": ["normalize_keys"],
        "losses": "none",
        "prior_chain_digest": "0" * 64,
        "already_canonical_input": False,
        "chain_truncated": False,
    }
    rec.update(over)
    return rec


def make_bounds(**over):
    b = {
        "schema": fi.SCHEMA,
        "stage": "g2-resource-bounds",
        "budgets": {
            "population": 2000, "filesystem": 4096, "output_bytes": 10_000_000,
            "memory": 1_000_000_000, "cpu_seconds": 600, "subprocess_count": 50,
            "wall_clock_seconds": 3600,
        },
        "public_acceptance_floor": {
            "max_nesting": 32, "max_members": 1000, "max_string_bytes": 100_000,
            "max_payload_bytes": 1_000_000, "max_path_length": 260,
        },
        "derivation": {"measured_baseline": "workstation", "benchmark": "frozen-bench-1",
                       "toolchain": "py3.12", "rationale": "measured + margin"},
        "margin": 0.25,
        "output_visibility_frozen": False,
        "bounds_revision": fi.UNASSIGNED,
    }
    b.update(over)
    return b


class TemplateTest(unittest.TestCase):
    def test_template_deterministic(self):
        a = run_cli("template")
        b = run_cli("template")
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)

    def test_template_candidate_independent(self):
        t = fi.build_template()
        self.assertEqual(t["candidate_commit"], fi.UNASSIGNED)
        self.assertEqual(t["normalization"]["algorithm_digest"], fi.UNASSIGNED)

    def test_matrix_covers_every_entrypoint_threat_cell(self):
        t = fi.build_template()
        for ep, row in t["entrypoint_threat_matrix"].items():
            for family, cell in row.items():
                self.assertIn(cell, (fi.UNASSIGNED, "not_applicable_reviewed"),
                              f"{ep}x{family} cell unpopulated")


class FixtureTest(unittest.TestCase):
    def test_every_compatibility_class_binds_expected_outcome(self):
        for cls, outcome in fi.EXPECTED_BY_CLASS.items():
            r = fi.validate_fixture(
                make_fixture(cls, outcome,
                             boundary="ingress_parse"
                             if outcome == "fail_at_boundary" else None))
            self.assertEqual(r["expected_outcome"], outcome)

    def test_unsupported_class_never_guesses(self):
        r = fi.validate_fixture(make_fixture("pre_v1_unsupported", "unsupported"))
        self.assertEqual(r["expected_outcome"], "unsupported")
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture("pre_v1_unsupported", "pass"))
        self.assertEqual(ctx.exception.code, "outcome_class_mismatch")

    def test_hostile_class_requires_boundary(self):
        r = fi.validate_fixture(make_fixture("path_traversal", "fail_at_boundary"))
        self.assertEqual(r["status"], "pass")
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture("path_traversal", "pass"))
        self.assertEqual(ctx.exception.code, "outcome_class_mismatch")

    def test_population_class_stays_incomplete(self):
        r = fi.validate_fixture(make_fixture("stale", "incomplete"))
        self.assertEqual(r["status"], "pass")
        with self.assertRaises(fi.ValidationError):
            fi.validate_fixture(make_fixture("stale", "pass"))

    def test_unknown_class_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture("benevolent_blob", "pass"))
        self.assertEqual(ctx.exception.code, "unknown_class")

    def test_early_candidate_binding_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture(candidate_binding="deadbeef"))
        self.assertEqual(ctx.exception.code, "candidate_field_assigned")

    def test_unsanitized_diagnostics_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture(diagnostics={"sanitized": False}))
        self.assertEqual(ctx.exception.code, "unsanitized_diagnostics")

    def test_private_metadata_leak_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_fixture(make_fixture(diagnostics={"sanitized": True, "contains_private_metadata": True}))
        self.assertEqual(ctx.exception.code, "private_metadata_leak")

    def test_invalid_json_fails_closed_via_cli(self):
        r = run_cli("validate-fixture", stdin="]]not json[[")
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid_json", r.stderr)


class NegotiationTest(unittest.TestCase):
    def test_highest_common_at_floor_selected(self):
        r = fi.validate_negotiation(make_negotiation())
        self.assertEqual(r["selected_version"], "1.2")

    def test_no_common_version_yields_none(self):
        t = make_negotiation(selected=None)
        t["allowlist"] = ["9"]
        r = fi.validate_negotiation(t)
        self.assertIsNone(r["selected_version"])

    def test_replayed_offer_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_negotiation(make_negotiation(replay=True))
        self.assertEqual(ctx.exception.code, "replayed_offer")

    def test_stripped_offer_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_negotiation(make_negotiation(stripped=True))
        self.assertEqual(ctx.exception.code, "stripped_offer")

    def test_parse_error_never_selects(self):
        t = make_negotiation(parse_error=True)
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_negotiation(t)
        self.assertEqual(ctx.exception.code, "fallback_on_parse_error")

    def test_selection_below_floor_rejected(self):
        t = make_negotiation(selected="1.1")
        t["floor"] = "1.2"
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_negotiation(t)
        self.assertEqual(ctx.exception.code, "selection_rule_violated")

    def test_unbound_selection_rejected(self):
        t = make_negotiation()
        t["result"]["payload_digest_bound"] = False
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_negotiation(t)
        self.assertEqual(ctx.exception.code, "unbound_selection")


class AdapterTest(unittest.TestCase):
    def test_valid_ingress_conversion_passes(self):
        self.assertEqual(fi.validate_adapter(make_adapter())["status"], "pass")

    def test_second_conversion_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_adapter(make_adapter(conversion_site="egress"))
        self.assertEqual(ctx.exception.code, "double_conversion")

    def test_reconverting_canonical_input_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_adapter(make_adapter(already_canonical_input=True))
        self.assertEqual(ctx.exception.code, "double_conversion")

    def test_chain_truncation_rejected(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_adapter(make_adapter(chain_truncated=True))
        self.assertEqual(ctx.exception.code, "chain_truncation")

    def test_critical_loss_cannot_be_a_conversion(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.validate_adapter(make_adapter(losses="critical_field"))
        self.assertEqual(ctx.exception.code, "invalid_loss")


class BoundsTest(unittest.TestCase):
    def test_valid_bounds_pass(self):
        self.assertEqual(fi.check_bounds(make_bounds())["status"], "pass")

    def test_missing_margin_fails(self):
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.check_bounds(make_bounds(margin=0))
        self.assertEqual(ctx.exception.code, "missing_margin")

    def test_budget_undercutting_public_floor_fails(self):
        b = make_bounds()
        b["budgets"]["population"] = 10
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.check_bounds(b)
        self.assertEqual(ctx.exception.code, "budget_undercuts_public_floor")

    def test_raise_after_visibility_fails(self):
        b = make_bounds(output_visibility_frozen=True, bounds_revision="rev-2")
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.check_bounds(b)
        self.assertEqual(ctx.exception.code, "bounds_raised_after_visibility")

    def test_missing_derivation_fails(self):
        b = make_bounds()
        b["derivation"]["benchmark"] = ""
        with self.assertRaises(fi.ValidationError) as ctx:
            fi.check_bounds(b)
        self.assertEqual(ctx.exception.code, "missing_field")


if __name__ == "__main__":
    unittest.main()
