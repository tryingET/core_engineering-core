#!/usr/bin/env python3
"""G1 dependable-adoption proof harness (engineering-core v1.0 convergence).

Internal qualification tooling. Validates candidate-independent journey manifests
and machine-decidable result envelopes for RFC Gate G1. Never executes
participant commands, never resolves remotes, never mutates repositories.

Modes:
  template   Emit the frozen candidate-independent journey template (deterministic).
  validate   Validate one journey-manifest instance against the frozen template.
  envelope   Validate one completed journey record as a result envelope.

Exit codes: 0 pass; 2 validation failure; 3 usage/drift error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

SCHEMA = "engineering-core.v1.g1/1"
ENVELOPE_SCHEMA = "engineering-core.v1.g1.journey-envelope/1"
UNASSIGNED = "unassigned"

JOURNEY_CATEGORIES = [
    "resolve_install_remote",
    "retrieve_explain_guidance",
    "plan_transition_mode",
    "apply_owner_plan",
    "diagnose_v1_adoption",
    "prove_active_resolution",
    "failure_boundaries",
    "rollback_recovery",
    "removal_with_owner_edits",
    "final_posture_disposal",
]

CATEGORY_ASSERTIONS = {
    "resolve_install_remote": [
        "resolved_from_immutable_remote",
        "zero_local_checkout_fallback",
        "zero_git_file_resolution",
    ],
    "retrieve_explain_guidance": [
        "guidance_rendered",
        "dependencies_and_omissions_listed",
        "local_deviations_listed",
        "stability_class_listed",
        "pre_v1_break_disclosed",
    ],
    "plan_transition_mode": [
        "mode_selected_from_clean_adopt_transition_migration",
        "plan_diff_reviewed",
        "local_truth_preserved_in_plan",
        "backup_recovery_removal_effects_declared",
    ],
    "apply_owner_plan": [
        "plan_digest_cryptographically_bound",
        "starting_state_preconditions_checked",
        "drift_rejected",
        "atomic_completion_or_documented_recovery",
        "no_accepted_partial_state",
    ],
    "diagnose_v1_adoption": [
        "no_undeclared_command_executed",
        "no_undeclared_url_or_model_contacted",
        "no_patch_applied",
    ],
    "prove_active_resolution": [
        "exactly_one_active_v1_resolution_per_scope",
        "zero_active_pre_v1_or_mixed_runtime",
        "owner_truth_preserved",
    ],
    "failure_boundaries": [
        "malformed_pin_fails_before_dns_network",
        "malformed_pin_fails_before_helpers_import_build_mutation",
        "unavailable_pin_contacts_only_credentialless_fixture_remote",
        "no_interactive_or_helper_auth",
        "malformed_policy_fails_before_consumer_command",
        "interruption_atomicity_proven_per_boundary",
        "recovery_leaves_no_fabricated_or_partial_state",
    ],
    "rollback_recovery": [
        "public_rollback_procedure_executed",
        "exact_starting_posture_restored",
        "git_filesystem_independent_oracle_equal",
    ],
    "removal_with_owner_edits": [
        "owner_edits_present_on_mixed_ownership_cases",
        "plan_bound_removal_or_structured_refusal",
        "validation_passes_without_engineering_core",
        "zero_classified_pins_selections_surfaces_remaining",
        "unrelated_content_preserved",
        "no_noop_success",
    ],
    "final_posture_disposal": [
        "predeclared_final_posture_restored",
        "residual_state_inventoried",
        "replica_disposed_or_quarantined",
    ],
}

FORBIDDEN_FALLBACK_KEYS = ("local_checkout_fallback", "git_file_resolution")
MIN_POSITIVE_BASELINES = 4
MIN_POSITIVE_OWNER_GROUPS = 3

BASELINE_REQUIRED_FIELDS = [
    "baseline_id",
    "owner_group",
    "repository_identity",
    "pinned_revision",
    "role",
    "starting_posture",
    "owner_task_ref",
    "validation_commands",
    "evidence_custody",
    "isolation_boundary",
    "rollback_boundary",
    "final_proof_workspace_posture",
]

MANIFEST_REQUIRED_FIELDS = [
    "schema",
    "stage",
    "template_digest",
    "candidate_commit",
    "candidate_digest",
    "baselines",
    "negative_control",
    "journeys",
]


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest_of(obj) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


class ValidationError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def build_template() -> dict:
    return {
        "schema": SCHEMA,
        "stage": "g1-journey-template",
        "binding": "candidate_independent_g0a2",
        "candidate_commit": UNASSIGNED,
        "candidate_digest": UNASSIGNED,
        "journey_categories": [
            {
                "category": cat,
                "required_assertions": CATEGORY_ASSERTIONS[cat],
                "runbook_digest": UNASSIGNED,
            }
            for cat in JOURNEY_CATEGORIES
        ],
        "baseline_required_fields": list(BASELINE_REQUIRED_FIELDS),
        "population_rules": {
            "min_positive_baselines": MIN_POSITIVE_BASELINES,
            "min_positive_owner_groups": MIN_POSITIVE_OWNER_GROUPS,
            "negative_control_count": 1,
            "duplicate_physical_identity_forbidden": True,
            "engineering_core_not_positive_adopter": True,
        },
        "negative_control_rules": {
            "read_only": True,
            "executes_no_command": True,
            "frozen_missing_absent_schema_result": True,
            "identical_pre_post_revision_receipts": True,
            "counts_only_in_completeness": True,
        },
        "pass_threshold": {
            "positive_journeys": "10xN_of_10xN",
            "negative_control_results": "100_percent_frozen_missing",
            "failure_boundary_probes": "100_percent_at_frozen_boundary",
            "narrative_cannot_override": True,
        },
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def _require(cond: bool, code: str, detail: str) -> None:
    if not cond:
        raise ValidationError(code, detail)


def _check_unassigned(value, field: str) -> None:
    _require(
        value == UNASSIGNED,
        "candidate_field_assigned",
        f"{field} must remain '{UNASSIGNED}' until G0-B",
    )


def validate_manifest(manifest: dict) -> dict:
    _require(isinstance(manifest, dict), "not_an_object", "manifest must be a JSON object")
    for field in MANIFEST_REQUIRED_FIELDS:
        _require(field in manifest, "missing_field", f"missing required field: {field}")
    _require(manifest["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(
        manifest.get("stage") == "g1-journey-manifest", "stage_mismatch",
        "expected stage g1-journey-manifest",
    )
    _require(
        manifest.get("template_digest") == template_digest(),
        "template_digest_mismatch", "journey template digest does not match frozen template",
    )
    _check_unassigned(manifest.get("candidate_commit"), "candidate_commit")
    _check_unassigned(manifest.get("candidate_digest"), "candidate_digest")

    baselines = manifest["baselines"]
    _require(isinstance(baselines, list) and len(baselines) >= MIN_POSITIVE_BASELINES,
             "population_too_small", f"need >= {MIN_POSITIVE_BASELINES} positive baselines")
    seen_ids, seen_repos, groups = set(), set(), set()
    for b in baselines:
        for field in BASELINE_REQUIRED_FIELDS:
            _require(isinstance(b, dict) and b.get(field) not in (None, "", []),
                     "missing_field", f"baseline missing required field: {field}")
        _require(b["baseline_id"] not in seen_ids, "duplicate_identity",
                 f"duplicate baseline_id: {b['baseline_id']}")
        _require(b["repository_identity"] not in seen_repos, "duplicate_identity",
                 f"duplicate physical repository identity: {b['repository_identity']}")
        _require(
            "engineering-core" not in str(b.get("owner_group", "")).lower(),
            "producer_as_adopter", "engineering-core cannot be a positive adopter",
        )
        seen_ids.add(b["baseline_id"])
        seen_repos.add(b["repository_identity"])
        groups.add(b["owner_group"])
    _require(len(groups) >= MIN_POSITIVE_OWNER_GROUPS, "population_groups_too_small",
             f"need >= {MIN_POSITIVE_OWNER_GROUPS} independent owner groups")

    nc = manifest["negative_control"]
    _require(isinstance(nc, dict), "missing_field", "negative_control entry required")
    for field in ("repository_identity", "pinned_revision", "expected_result_schema"):
        _require(nc.get(field) not in (None, ""), "missing_field",
                 f"negative_control missing: {field}")
    for flag in ("declared_mutation", "declared_execution"):
        _require(nc.get(flag) is False, "negative_control_mutated",
                 f"negative_control.{flag} must be false")

    def scan_fallbacks(node, path="manifest"):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in FORBIDDEN_FALLBACK_KEYS and v:
                    raise ValidationError("forbidden_fallback_declared",
                                          f"{path}.{k} must be false/absent")
                scan_fallbacks(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                scan_fallbacks(v, f"{path}[{i}]")

    scan_fallbacks(manifest)

    journeys = manifest["journeys"]
    _require(isinstance(journeys, list), "missing_field", "journeys list required")
    seen = set()
    for j in journeys:
        cat = j.get("category")
        _require(cat in JOURNEY_CATEGORIES, "unknown_category", f"unknown category: {cat}")
        _require(cat not in seen, "duplicate_category", f"duplicate category: {cat}")
        seen.add(cat)
        _require(j.get("baseline_id") in seen_ids, "unknown_baseline",
                 f"journey references unknown baseline: {j.get('baseline_id')}")
        _require(j.get("runbook_digest") == UNASSIGNED, "candidate_field_assigned",
                 "journey.runbook_digest must remain unassigned until G0-B")
        _require(j.get("expected_candidate_bytes") == UNASSIGNED, "candidate_field_assigned",
                 "expected_candidate_bytes must remain unassigned until G0-B")
        for name in CATEGORY_ASSERTIONS[cat]:
            _require(name in j.get("assertions", {}), "missing_assertion",
                     f"journey {cat} missing frozen assertion: {name}")
    _require(len(seen) == len(JOURNEY_CATEGORIES), "missing_category",
             "every one of the ten journey categories must be present")

    return {
        "schema": SCHEMA,
        "stage": "g1-manifest-validation",
        "status": "pass",
        "validated_baselines": len(baselines),
        "validated_owner_groups": len(groups),
        "validated_journeys": len(seen),
        "template_digest": template_digest(),
        "manifest_digest": digest_of(manifest),
    }


ENVELOPE_REQUIRED = [
    "schema", "stage", "category", "baseline_id", "owner_group", "status",
    "assertions", "effects", "digests", "owner_task_ref", "review",
]
ENVELOPE_STATUSES = {"pass", "fail", "blocked", "incomplete"}


def validate_envelope(env: dict) -> dict:
    for field in ENVELOPE_REQUIRED:
        _require(isinstance(env, dict) and field in env, "missing_field",
                 f"envelope missing required field: {field}")
    _require(env["schema"] == ENVELOPE_SCHEMA, "schema_mismatch",
             f"expected {ENVELOPE_SCHEMA}")
    _require(env["category"] in JOURNEY_CATEGORIES, "unknown_category",
             f"unknown category: {env['category']}")
    _require(env["status"] in ENVELOPE_STATUSES, "invalid_status",
             f"status must be one of {sorted(ENVELOPE_STATUSES)}")
    _require(isinstance(env["assertions"], list) and env["assertions"],
             "missing_assertion", "assertion list required")
    for a in env["assertions"]:
        for field in ("name", "expected", "observed", "required"):
            _require(field in a, "missing_field", f"assertion missing: {field}")
        _require(a["name"] in CATEGORY_ASSERTIONS[env["category"]], "unknown_assertion",
                 f"assertion not frozen for {env['category']}: {a['name']}")
    review = env["review"]
    _require(isinstance(review, dict) and review.get("reviewer"), "missing_field",
             "review.reviewer required")
    _require(review.get("independent_of_producer") is True, "review_not_independent",
             "producer cannot be sole reviewer")
    effects = env["effects"]
    _require(isinstance(effects, dict), "missing_field", "effects record required")
    if env["status"] == "pass":
        for a in env["assertions"]:
            if a["required"]:
                _require(a["observed"] == a["expected"], "required_assertion_failed",
                         f"required assertion not met: {a['name']}")
        _require(effects.get("undeclared_residual") == [], "undeclared_residual",
                 "pass requires zero undeclared residual effects")
    else:
        reasons = env.get("missingness_reasons") or env.get("failure_reasons")
        _require(reasons not in (None, "", []), "missing_reason",
                 f"{env['status']} requires explicit reasons")
    return {
        "schema": ENVELOPE_SCHEMA,
        "stage": "g1-envelope-validation",
        "status": "pass",
        "envelope_status": env["status"],
        "category": env["category"],
        "baseline_id": env["baseline_id"],
        "envelope_digest": digest_of(env),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["template", "validate", "envelope"])
    parser.add_argument("path", nargs="?", help="input JSON file ('-' for stdin)")
    args = parser.parse_args(argv)

    try:
        if args.mode == "template":
            out = build_template()
            out["template_digest"] = template_digest()
        else:
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
            out = validate_manifest(payload) if args.mode == "validate" else validate_envelope(payload)
        print(canonical(out))
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
