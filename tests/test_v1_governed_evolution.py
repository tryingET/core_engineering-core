"""Tests for the G4 review-governed evolution harness (task 4874)."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "governed_evolution.py"

spec = importlib.util.spec_from_file_location("governed_evolution", SCRIPT)
ge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ge)


def make_cycle(**over):
    c = {
        "schema": ge.SCHEMA,
        "stage": "g4-live-cycle",
        "template_digest": ge.template_digest(),
        "cycle_id": "cycle-1",
        "candidate": "cand-1",
        "candidate_identity": ge.UNASSIGNED,
        "origin_group": "holdingco",
        "pilot_groups": ["teachingco", "softwareco"],
        "participant_disposition": {"disposition": "supports", "evidence_supported": True},
        "content_owner_decision": {
            "decision": "revised", "decided_by": "engineering_core_content_owner",
            "coerced": False,
        },
        "final_state": {
            "disposition": "revised",
            "preserved_lineage": [{"ref": "r1", "immutable": True}],
        },
        "minimum_decision_record": {f: "recorded" for f in ge.MINIMUM_DECISION_RECORD},
        "pilot_bounds": {
            "opt_in": True, "bounded": True,
            "expiry_or_review_event": "2026-09-30",
            "can_become_default_silently": False,
        },
        "rollback_drill": {
            "restored_exact_prior_stable_selection": True, "history_preserved": True,
        },
        "distribution_status": "not_distributed",
        "adoption_status": "not_adopted",
    }
    c.update(over)
    return c


def make_transition(case="proposal", frm="proposal", to="pilot_selection", **over):
    t = {
        "schema": ge.SCHEMA,
        "stage": "g4-transition-fixture",
        "suite_case": case,
        "from_state": frm,
        "to_state": to,
        "authorized_by": "engineering_core_content_owner",
        "evidence_freshness": "fresh",
        "expected_result": "accepted",
        "lineage": {"history_preserved": True},
    }
    t.update(over)
    return t


class TemplateTest(unittest.TestCase):
    def test_template_deterministic(self):
        outs = [subprocess.run([sys.executable, str(SCRIPT), "template"],
                               capture_output=True, text=True).stdout for _ in range(2)]
        self.assertEqual(outs[0], outs[1])

    def test_template_freezes_rules(self):
        t = ge.build_template()
        self.assertEqual(len(t["suite_cases"]), 12)
        self.assertTrue(t["no_distribution_of_live_outcomes_required"])
        self.assertTrue(t["rollback_drill"]["mandatory"])
        self.assertFalse(t["g4b"]["mutating"])


class CycleTest(unittest.TestCase):
    def test_valid_cycle_passes(self):
        r = ge.validate_cycle(make_cycle())
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["final_disposition"], "revised")

    def test_missing_decision_record_field_rejected(self):
        c = make_cycle()
        del c["minimum_decision_record"]["falsification_conditions"]
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "missing_decision_record_field")

    def test_non_opt_in_pilot_rejected(self):
        c = make_cycle()
        c["pilot_bounds"]["opt_in"] = False
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "pilot_not_opt_in")

    def test_never_expiring_pilot_rejected(self):
        c = make_cycle()
        c["pilot_bounds"]["expiry_or_review_event"] = None
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "pilot_never_expires")

    def test_silent_default_rejected(self):
        c = make_cycle()
        c["pilot_bounds"]["can_become_default_silently"] = True
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "silent_default")

    def test_participant_transition_rejected(self):
        c = make_cycle()
        c["content_owner_decision"]["decided_by"] = "participant_owner"
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "participant_transitioned_shared_content")

    def test_coerced_disposition_rejected(self):
        c = make_cycle()
        c["content_owner_decision"]["coerced"] = True
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "coerced_disposition")

    def test_unlawful_decision_rejected(self):
        c = make_cycle()
        c["content_owner_decision"]["decision"] = "mandated"
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "unlawful_decision")

    def test_promotion_needs_two_distinct_groups(self):
        base = {
            "content_owner_decision": {"decision": "promoted",
                                       "decided_by": "engineering_core_content_owner",
                                       "coerced": False},
            "final_state": {"disposition": "promoted", "preserved_lineage": []},
            "non_originator_present": True,
        }
        c = make_cycle(**base, promotion_groups=["holdingco"])
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "promotion_groups_insufficient")
        c = make_cycle(**base, promotion_groups=["holdingco", "teachingco"])
        self.assertEqual(ge.validate_cycle(c)["final_disposition"], "promoted")

    def test_promotion_needs_non_originator(self):
        c = make_cycle(
            content_owner_decision={"decision": "promoted",
                                    "decided_by": "engineering_core_content_owner",
                                    "coerced": False},
            final_state={"disposition": "promoted", "preserved_lineage": []},
            promotion_groups=["holdingco", "teachingco"], non_originator_present=False)
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "promotion_originator_only")

    def test_emergency_promotion_rejected(self):
        c = make_cycle(
            content_owner_decision={"decision": "promoted",
                                    "decided_by": "engineering_core_content_owner",
                                    "coerced": False},
            final_state={"disposition": "promoted", "preserved_lineage": []},
            promotion_groups=["holdingco", "teachingco"], non_originator_present=True,
            emergency_exception_used=True)
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "emergency_promotion")

    def test_erased_negative_history_rejected(self):
        c = make_cycle()
        c["final_state"]["preserved_lineage"] = []
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "erased_negative_history")

    def test_mutable_lineage_rejected(self):
        c = make_cycle()
        c["final_state"]["preserved_lineage"] = [{"ref": "r1", "immutable": False}]
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "mutable_lineage")

    def test_missing_rollback_drill_rejected(self):
        c = make_cycle()
        c["rollback_drill"] = {}
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertIn(ctx.exception.code,
                      ("rollback_imprecise", "rollback_erased_history"))

    def test_rollback_erasing_history_rejected(self):
        c = make_cycle()
        c["rollback_drill"]["history_preserved"] = False
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "rollback_erased_history")

    def test_missing_separate_status_fields_rejected(self):
        c = make_cycle()
        del c["distribution_status"]
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_cycle(c)
        self.assertEqual(ctx.exception.code, "missing_field")


class TransitionTest(unittest.TestCase):
    def test_legal_transition_accepted(self):
        r = ge.validate_transition(make_transition())
        self.assertEqual(r["result"], "accepted")

    def test_illegal_transition_rejected(self):
        t = make_transition(frm="proposal", to="final_state")
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_transition(t)
        self.assertEqual(ctx.exception.code, "illegal_transition")

    def test_unauthorized_promotion_fixture(self):
        t = make_transition(case="unauthorized_promotion", frm="proposal",
                            to="final_state", expected_result="rejected")
        r = ge.validate_transition(t)
        self.assertEqual(r["result"], "rejected")

    def test_unauthorized_promoter_rejected(self):
        t = make_transition(frm="content_owner_decision", to="final_state")
        t["authorized_by"] = "participant_owner"
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_transition(t)
        self.assertEqual(ctx.exception.code, "unauthorized_promotion")

    def test_stale_evidence_requires_rereview(self):
        t = make_transition(frm="participant_disposition", to="content_owner_decision",
                            case="stale_evidence", evidence_freshness="stale",
                            re_review=False)
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_transition(t)
        self.assertEqual(ctx.exception.code, "stale_evidence_re_review")

    def test_rollback_transition_preserves_history(self):
        t = make_transition(case="rollback", frm="pilot_selection",
                            to="rollback_restored")
        t["lineage"] = {"history_preserved": False}
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_transition(t)
        self.assertEqual(ctx.exception.code, "rollback_erased_history")

    def test_unknown_case_rejected(self):
        t = make_transition(case="vibes")
        with self.assertRaises(ge.ValidationError) as ctx:
            ge.validate_transition(t)
        self.assertEqual(ctx.exception.code, "unknown_case")


class CliTest(unittest.TestCase):
    def test_cli_cycle_roundtrip(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "validate-cycle", "-"],
                           input=json.dumps(make_cycle()),
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_cli_invalid_json_fails_closed(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "validate-transition", "-"],
                           input="nope{", capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("invalid_json", r.stderr)


if __name__ == "__main__":
    unittest.main()
