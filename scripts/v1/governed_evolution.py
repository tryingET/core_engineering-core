#!/usr/bin/env python3
"""G4 review-governed evolution harness (engineering-core v1.0).

Internal qualification tooling. Freezes the live-cycle contract, the
deterministic lifecycle-conformance transition table, and the mandatory
rollback drill for RFC Gate G4; validates cycle and transition records
fail-closed. Creates no pilot content and mutates no participant.

Modes:
  template              Emit the frozen cycle contract and transition table.
  validate-cycle        Validate one live G4-A cycle record.
  validate-transition   Validate one lifecycle-conformance fixture.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

SCHEMA = "engineering-core.v1.g4/1"
UNASSIGNED = "unassigned"

MINIMUM_DECISION_RECORD = [
    "problem", "audience_and_scope", "invariant_or_decision_rule", "load_triggers",
    "evidence_references", "strongest_alternative", "counterevidence_and_exceptions",
    "falsification_conditions", "adoption_and_compatibility", "review_trigger",
    "retirement_signal", "semantic_references",
]

STATES = ["proposal", "pilot_selection", "participant_disposition",
          "content_owner_decision", "final_state"]

LEGAL_TRANSITIONS = {
    ("proposal", "pilot_selection"),
    ("pilot_selection", "participant_disposition"),
    ("participant_disposition", "content_owner_decision"),
    ("content_owner_decision", "final_state"),
    ("pilot_selection", "rollback_restored"),
    ("content_owner_decision", "rollback_restored"),
}

LAWFUL_FINAL_DISPOSITIONS = [
    "promoted", "revised", "rejected", "deprecated", "retired", "other_disposition",
]

SUITE_CASES = [
    "proposal", "pilot_selection", "promotion", "revision_split", "rejection",
    "deprecation", "retirement", "expiry", "rollback", "invalid_transition",
    "stale_evidence", "unauthorized_promotion",
]

TERMINAL_LINEAGE_REQUIRED = [
    "rejected", "revised", "deprecated", "retired", "expired", "reverted",
]

CYCLE_REQUIRED_FIELDS = [
    "schema", "stage", "cycle_id", "candidate", "origin_group", "pilot_groups",
    "participant_disposition", "content_owner_decision", "final_state",
    "minimum_decision_record", "pilot_bounds", "rollback_drill",
]


class ValidationError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest_of(obj) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _require(cond, code, detail):
    if not cond:
        raise ValidationError(code, detail)


def build_template() -> dict:
    return {
        "schema": SCHEMA,
        "stage": "g4-lifecycle-template",
        "binding": "candidate_independent_g0a2",
        "live_cycle": [
            "proposal_record", "opt_in_bounded_pilot", "evidence_and_counterevidence",
            "participant_local_disposition", "engineering_core_content_owner_decision",
            "rollback_expiry_final_state_with_preserved_lineage",
        ],
        "population": {
            "distinct_positive_owner_groups": 3,
            "two_baselines_one_company_count_as_one": True,
            "each_originates_one_substantial_candidate": True,
        },
        "minimum_decision_record": MINIMUM_DECISION_RECORD,
        "promotion_rules": {
            "min_distinct_positive_owner_groups": 2,
            "requires_non_originator": True,
            "emergency_exception_cannot_satisfy": True,
            "participant_evidence_alone_changes_nothing": True,
            "no_automatic_promotion": True,
        },
        "no_distribution_of_live_outcomes_required": True,
        "lawful_final_dispositions": LAWFUL_FINAL_DISPOSITIONS,
        "expiry_without_decision_completes_nothing": True,
        "states": STATES + ["rollback_restored"],
        "legal_transitions": [list(t) for t in sorted(LEGAL_TRANSITIONS)],
        "suite_cases": SUITE_CASES,
        "rollback_drill": {
            "mandatory": True,
            "restores_exact_prior_stable_selection": True,
            "preserves_proposal_evidence_decision_failure_history": True,
        },
        "g4b": {
            "mutating": False,
            "inclusion_map_from_accepted_digest_to_candidate_path_digest": True,
            "negative_outcomes_to_immutable_lineage": True,
        },
        "candidate_identity": UNASSIGNED,
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def validate_cycle(c: dict) -> dict:
    _require(isinstance(c, dict), "not_an_object", "cycle must be an object")
    for field in CYCLE_REQUIRED_FIELDS:
        _require(field in c, "missing_field", f"cycle missing: {field}")
    _require(c["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(c["stage"] == "g4-live-cycle", "stage_mismatch",
             "expected stage g4-live-cycle")
    _require(c.get("template_digest") == template_digest(), "template_digest_mismatch",
             "cycle template digest does not match frozen template")
    _require(c.get("candidate_identity") == UNASSIGNED, "candidate_field_assigned",
             "candidate identity binds at G4-A owner acceptance, not in the template")

    mdr = c["minimum_decision_record"]
    for field in MINIMUM_DECISION_RECORD:
        _require(isinstance(mdr, dict) and mdr.get(field) not in (None, ""),
                 "missing_decision_record_field", f"minimum decision record missing: {field}")

    bounds = c["pilot_bounds"]
    _require(isinstance(bounds, dict), "missing_field", "pilot_bounds required")
    _require(bounds.get("opt_in") is True, "pilot_not_opt_in", "pilots must be opt-in")
    _require(bounds.get("bounded") is True, "pilot_unbounded", "pilots must be bounded")
    _require(bounds.get("expiry_or_review_event") not in (None, ""),
             "pilot_never_expires", "every pilot expires or reaches a named review event")
    _require(bounds.get("can_become_default_silently") is False,
             "silent_default", "a pilot cannot silently become default")

    disp = c["participant_disposition"]
    _require(isinstance(disp, dict) and disp.get("disposition") not in (None, ""),
             "missing_field", "participant disposition required")
    _require(disp.get("evidence_supported") is True, "disposition_without_evidence",
             "disposition must be evidence-supported")
    dec = c["content_owner_decision"]
    _require(isinstance(dec, dict) and dec.get("decision") in LAWFUL_FINAL_DISPOSITIONS,
             "unlawful_decision",
             f"decision must be one of {LAWFUL_FINAL_DISPOSITIONS}")
    _require(dec.get("decided_by") == "engineering_core_content_owner",
             "participant_transitioned_shared_content",
             "only the engineering-core content owner may transition shared content")
    _require(dec.get("coerced") is False, "coerced_disposition",
             "dispositions cannot be coerced by the gate")

    final = c["final_state"]
    _require(final.get("disposition") == dec.get("decision"), "final_state_mismatch",
             "final state must match the content-owner decision")
    if final.get("disposition") == "expired":
        _require(dec.get("decision") is not None, "expiry_without_decision",
                 "expiry without the required decision completes nothing")

    if dec.get("decision") == "promoted":
        groups = c.get("promotion_groups") or []
        _require(len(set(groups)) >= 2, "promotion_groups_insufficient",
                 "promotion requires at least two distinct positive owner groups")
        _require(c.get("non_originator_present") is True, "promotion_originator_only",
                 "promotion requires a group other than the originator")
        _require(c.get("emergency_exception_used") is not True,
                 "emergency_promotion", "emergency exception cannot satisfy promotion proof")

    rd = c["rollback_drill"]
    _require(isinstance(rd, dict), "missing_field", "rollback drill is mandatory")
    _require(rd.get("restored_exact_prior_stable_selection") is True,
             "rollback_imprecise", "drill must restore the exact prior stable selection")
    _require(rd.get("history_preserved") is True, "rollback_erased_history",
             "rollback must preserve proposal, evidence, decision, and failure history")

    lin = final.get("preserved_lineage") or []
    if final.get("disposition") in TERMINAL_LINEAGE_REQUIRED:
        _require(len(lin) >= 1, "erased_negative_history",
                 "terminal negative outcomes require preserved immutable lineage")
    for ref in lin:
        _require(isinstance(ref, dict) and ref.get("immutable") is True,
                 "mutable_lineage", "lineage references must be immutable")

    for status_field in ("distribution_status", "adoption_status"):
        _require(status_field in c, "missing_field",
                 f"{status_field} must be recorded separately")

    return {
        "schema": SCHEMA, "stage": "g4-cycle-validation", "status": "pass",
        "cycle_id": c["cycle_id"], "final_disposition": final.get("disposition"),
        "cycle_digest": digest_of(c),
    }


def validate_transition(t: dict) -> dict:
    for field in ("schema", "stage", "suite_case", "from_state", "to_state",
                  "authorized_by", "evidence_freshness", "lineage"):
        _require(isinstance(t, dict) and field in t, "missing_field",
                 f"transition missing: {field}")
    _require(t["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(t["stage"] == "g4-transition-fixture", "stage_mismatch",
             "expected stage g4-transition-fixture")
    _require(t["suite_case"] in SUITE_CASES, "unknown_case",
             f"suite case must be one of {SUITE_CASES}")
    pair = (t["from_state"], t["to_state"])
    legal = pair in LEGAL_TRANSITIONS
    if t["suite_case"] in ("invalid_transition", "unauthorized_promotion"):
        _require(legal is False, "invalid_transition_expected",
                 f"{t['suite_case']} fixture must use an illegal transition")
        _require(t.get("expected_result") == "rejected",
                 "invalid_transition_must_fail", "illegal transitions must be rejected")
        return {"schema": SCHEMA, "stage": "g4-transition-validation",
                "status": "pass", "suite_case": t["suite_case"],
                "result": "rejected", "transition_digest": digest_of(t)}
    _require(legal, "illegal_transition",
             f"transition {pair} is not in the frozen legal table")
    _require(t.get("expected_result") == "accepted", "valid_transition_must_pass",
             "legal transitions must be accepted")
    _require(t["authorized_by"] == "engineering_core_content_owner",
             "unauthorized_promotion",
             "shared-content transitions require the content owner")
    if t["suite_case"] == "stale_evidence":
        _require(t["evidence_freshness"] == "stale" and t.get("re_review") is True,
                 "stale_evidence_re_review", "stale evidence requires re-review")
    if t["suite_case"] == "expiry":
        _require(t.get("decision_present") is not False, "expiry_without_decision",
                 "expiry fixtures must include the required decision")
    if t["to_state"] == "rollback_restored":
        _require(t["lineage"].get("history_preserved") is True,
                 "rollback_erased_history", "rollback must preserve history")
    return {"schema": SCHEMA, "stage": "g4-transition-validation", "status": "pass",
            "suite_case": t["suite_case"], "result": "accepted",
            "transition_digest": digest_of(t)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["template", "validate-cycle", "validate-transition"])
    parser.add_argument("path", nargs="?", help="input JSON file ('-' for stdin)")
    args = parser.parse_args(argv)
    handlers = {
        "template": lambda p: {**build_template(), "template_digest": template_digest()},
        "validate-cycle": validate_cycle,
        "validate-transition": validate_transition,
    }
    try:
        if args.mode == "template":
            print(canonical(handlers["template"](None)))
            return 0
        if not args.path:
            print(json.dumps({"status": "fail", "code": "missing_input"}), file=sys.stderr)
            return 3
        raw = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(json.dumps({"status": "fail", "code": "invalid_json",
                              "detail": str(exc)}), file=sys.stderr)
            return 2
        print(canonical(handlers[args.mode](payload)))
        return 0
    except ValidationError as exc:
        print(json.dumps({"status": "fail", "code": exc.code, "detail": exc.detail}),
              file=sys.stderr)
        return 2
    except OSError as exc:
        print(json.dumps({"status": "fail", "code": "io_error", "detail": str(exc)}),
              file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
