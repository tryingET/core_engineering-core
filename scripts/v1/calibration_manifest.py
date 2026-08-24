#!/usr/bin/env python3
"""G3 evidence-calibration manifest validator (engineering-core v1.0).

Internal qualification tooling. Emits the frozen prospective empirical
protocol manifest template and fail-closed validates instances for RFC
Gate G3. Performs no campaign execution, no analysis, no cross-owner data
transfer; DSPx/Oracle owns the empirical campaign.

Modes:
  template   Emit the frozen protocol manifest template (all measured values unassigned).
  validate   Validate one protocol manifest instance.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

SCHEMA = "engineering-core.v1.g3/1"
UNASSIGNED = "unassigned"
MIN_BASE_MODEL_FAMILIES = 2

VARIANT_KEYS_OF_ONE_BASE = {"prompt_variant", "seed_variant", "temperature_variant",
                            "endpoint_variant", "adapter_variant", "quantization_variant"}

REQUIRED_SECTIONS = [
    "population_design", "power", "weighting", "model_identity",
    "calibration", "harm_safety", "outcome_definition", "privacy_manifest",
    "result_bindings", "separation_of_record_classes",
]

MEASURED_FIELDS = [
    ("power", "smallest_effect_of_practical_interest"),
    ("power", "interval_error_criterion"),
    ("power", "design_alternative_justification"),
    ("power", "power_analysis"),
    ("power", "attrition_inflation"),
    ("power", "sensitivity_analyses"),
    ("power", "total_per_cell_sample"),
    ("calibration", "reference_forecast_justification"),
    ("harm_safety", "cell_harm_boundaries"),
    ("harm_safety", "marginal_harm_boundaries"),
    ("harm_safety", "safety_set"),
]

PRIVACY_REQUIRED_FIELDS = [
    "classification", "owner_approved_bytes_digest", "owner_approved_length",
    "recipients", "endpoint_region", "purpose", "access_encryption",
    "logs_cache_session", "retention_deletion", "route", "adapter_model_identity",
    "training_use_prohibited", "custody", "readers", "quarantine_state",
    "owner_attestation",
]

FORBIDDEN_AUTHORITY_CLAIMS = ["release_authority", "rollout_authority",
                              "doctrine_authority", "governance_decision"]


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
        "stage": "g3-protocol-template",
        "protocol_stage": "authored",
        "binding": "candidate_independent_g0a2",
        "empirical_owner": {"required": True, "identity": UNASSIGNED},
        "sections": {
            "population_design": {
                "target_population": UNASSIGNED,
                "independent_clusters": UNASSIGNED,
                "development_confirmatory_split": "disjoint_required",
                "arm_neutral_rubric": UNASSIGNED,
                "objective_oracle": UNASSIGNED,
                "exclusions": UNASSIGNED,
                "sole_treatment_contrast": UNASSIGNED,
                "prompts_context": UNASSIGNED,
                "model_set": UNASSIGNED,
                "allocations": UNASSIGNED,
                "executors": UNASSIGNED,
                "masking_contamination_controls": UNASSIGNED,
                "stopping_rule": "no_optional_stopping",
                "scoring_code_environment": UNASSIGNED,
                "multiplicity_error_control": UNASSIGNED,
            },
            "power": {field: UNASSIGNED for field in [
                "smallest_effect_of_practical_interest", "interval_error_criterion",
                "design_alternative_justification", "power_analysis",
                "attrition_inflation", "sensitivity_analyses", "total_per_cell_sample",
            ]},
            "weighting": {
                "top_level": "equal_weight_per_owner_group",
                "within_owner_rule": "baseline_x_model_weights_sum_to_one",
                "owner_weights": UNASSIGNED,
            },
            "model_identity": {
                "min_base_model_families": MIN_BASE_MODEL_FAMILIES,
                "same_frozen_set_in_every_positive_owner_group": True,
                "variant_of_one_base_is_not_diversity": sorted(VARIANT_KEYS_OF_ONE_BASE),
                "families": UNASSIGNED,
            },
            "calibration": {
                "metrics": UNASSIGNED,
                "estimator": UNASSIGNED,
                "interval_procedure": UNASSIGNED,
                "threshold": UNASSIGNED,
                "missing_forecast_treatment": UNASSIGNED,
                "reference_forecast": "disjoint_development",
                "reference_forecast_justification": UNASSIGNED,
                "forecast_emitted_by_advice_surface_before_execution": True,
                "forecaster_claim_only_if_separate_forecaster": True,
                "forecasts_hidden_from_outcome_reviewers": True,
            },
            "harm_safety": {
                "cell_harm_boundaries": UNASSIGNED,
                "marginal_harm_boundaries": UNASSIGNED,
                "sensitivity_analysis": "required_with_boundaries",
                "aggregate_effect_cannot_waive_harm_stop": True,
                "safety_set": UNASSIGNED,
                "safety_set_rule": "at_least_one_case_per_owner_group_x_base_model_cell",
                "safety_set_excluded_from_estimates": True,
                "insufficient_evidence_emits_abstain_or_unknown": True,
            },
            "outcome_definition": {
                "y_equals_one_only_on_owner_constraints_validation_objective_verification": True,
                "evidence_use_citation_preference_never_sets_y": True,
                "intention_to_treat": True,
                "arm_attributable_failure_is_y_zero": True,
                "administrative_missingness": "pessimistically_bounded",
                "no_pseudoreplication": True,
            },
            "privacy_manifest": {
                "raw_cross_owner_snapshot_transmitted": False,
                "transfers": [],
                "required_transfer_fields": PRIVACY_REQUIRED_FIELDS,
            },
            "result_bindings": {
                "protocol_decision_ref": UNASSIGNED,
                "power_sensitivity_evidence": UNASSIGNED,
                "bounded_results": UNASSIGNED,
                "replay_configuration_receipt": UNASSIGNED,
                "limitations": UNASSIGNED,
                "masking_breaches": UNASSIGNED,
                "exclusions": UNASSIGNED,
                "missingness": UNASSIGNED,
                "counterevidence": UNASSIGNED,
            },
            "separation_of_record_classes": {
                "owner_dispositions": "distinct_class",
                "empirical_outcomes": "distinct_class",
                "evidence_receipts": "distinct_class",
                "governance_decisions": "distinct_class",
                "empirical_output_grants_no_authority": True,
            },
        },
        "forbidden_fields": FORBIDDEN_AUTHORITY_CLAIMS,
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def _check_unassigned(section: str, field: str, value, stage: str) -> None:
    if stage == "authored":
        _require(value == UNASSIGNED, "measured_value_assigned_early",
                 f"{section}.{field} must remain '{UNASSIGNED}' until protocol acceptance")
    else:
        _require(value != UNASSIGNED, "missing_frozen_value",
                 f"{section}.{field} must be frozen before output at accepted stage")


def validate_manifest(m: dict) -> dict:
    _require(isinstance(m, dict), "not_an_object", "manifest must be an object")
    _require(m.get("schema") == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    stage = m.get("protocol_stage")
    _require(stage in ("authored", "accepted"), "invalid_stage",
             "protocol_stage must be authored or accepted")
    _require(m.get("template_digest") == template_digest(), "template_digest_mismatch",
             "manifest template digest does not match frozen template")
    def _walk_keys(node):
        if isinstance(node, dict):
            for k, v in node.items():
                _require(k not in FORBIDDEN_AUTHORITY_CLAIMS, "authority_claim",
                         f"empirical manifest cannot contain field {k}")
                _walk_keys(v)
        elif isinstance(node, list):
            for v in node:
                _walk_keys(v)

    _walk_keys(m)
    sections = m.get("sections", {})
    for name in REQUIRED_SECTIONS:
        _require(name in sections, "missing_section", f"missing section: {name}")
    for section, field in MEASURED_FIELDS:
        _require(section in sections and field in sections[section], "missing_field",
                 f"missing field: {section}.{field}")
        _check_unassigned(section, field, sections[section][field], stage)

    # Model identity
    mi = sections["model_identity"]
    families = mi.get("families")
    if stage == "accepted":
        _require(isinstance(families, list) and len(families) >= MIN_BASE_MODEL_FAMILIES,
                 "model_diversity_insufficient",
                 f"need >= {MIN_BASE_MODEL_FAMILIES} distinct base-model families")
        for fam in families:
            _require(isinstance(fam, dict) and fam.get("family_id") and fam.get("identity"),
                     "invalid_family", "each family needs family_id and identity")
            _require(not fam.get("is_variant_of_another_family"), "variant_counted_as_diversity",
                     "variants of one base model do not count as families")

    # Weighting
    w = sections["weighting"]
    owner_weights = w.get("owner_weights")
    if stage == "accepted":
        _require(isinstance(owner_weights, list) and len(owner_weights) >= 3,
                 "missing_owner_groups", "at least three owner groups required")
        top = [o.get("top_level_weight") for o in owner_weights]
        _require(all(t == top[0] for t in top), "unequal_owner_weights",
                 "top-level primary-estimand weight must be equal per owner group")
        for o in owner_weights:
            inner = o.get("baseline_model_weights")
            _require(isinstance(inner, list) and inner, "missing_field",
                     f"owner {o.get('owner_group')} missing baseline_model_weights")
            total = sum(x.get("weight", 0) for x in inner)
            _require(abs(total - 1.0) < 1e-9, "weights_do_not_sum_to_one",
                     f"owner {o.get('owner_group')} within-owner weights sum to {total}")

    # Safety set coverage
    hs = sections["harm_safety"]
    if stage == "accepted":
        safety = hs.get("safety_set")
        _require(isinstance(safety, list) and safety, "missing_safety_set",
                 "safety set required at accepted stage")
        covered = {(c.get("owner_group"), c.get("base_model_family")) for c in safety}
        for o in owner_weights:
            for fam in families:
                key = (o.get("owner_group"), fam.get("family_id"))
                _require(key in covered, "safety_cell_uncovered",
                         f"safety set must cover {key}")

    # Calibration provenance
    cal = sections["calibration"]
    _require(cal.get("forecast_emitted_by_advice_surface_before_execution") is True
             or cal.get("forecaster_claim_only_if_separate_forecaster") is True,
             "forecast_provenance_unbound",
             "probability source must be the advice surface or explicitly a forecaster claim")
    ref = cal.get("reference_forecast")
    if stage == "accepted" and isinstance(ref, str) and "constant" in ref:
        justification = cal.get("reference_forecast_justification")
        _require(justification not in (UNASSIGNED, "", "none", "not_justified"),
                 "unjustified_constant_reference",
                 "a constant reference requires prospective justification against prevalence")

    # Stopping and masking
    pd = sections["population_design"]
    _require(pd.get("stopping_rule") == "no_optional_stopping", "optional_stopping",
             "stopping rule must remain the frozen no_optional_stopping")
    _require(pd.get("development_confirmatory_split") == "disjoint_required",
             "split_not_disjoint", "development/confirmatory split must be disjoint")

    # Privacy manifest
    pm = sections["privacy_manifest"]
    _require(pm.get("raw_cross_owner_snapshot_transmitted") is False,
             "raw_snapshot_transmission",
             "no raw cross-owner snapshot may be transmitted")
    for i, t in enumerate(pm.get("transfers", [])):
        for field in PRIVACY_REQUIRED_FIELDS:
            _require(isinstance(t, dict) and t.get(field) not in (None, ""),
                     "privacy_field_missing", f"transfers[{i}] missing {field}")
        _require(t.get("training_use_prohibited") is True, "training_use_not_prohibited",
                 f"transfers[{i}] must prohibit training use")

    # Separation of record classes
    sep = sections["separation_of_record_classes"]
    for cls in ("owner_dispositions", "empirical_outcomes", "evidence_receipts",
                "governance_decisions"):
        _require(sep.get(cls) == "distinct_class", "record_classes_blurred",
                 f"{cls} must remain a distinct record class")

    return {
        "schema": SCHEMA,
        "stage": "g3-protocol-validation",
        "status": "pass",
        "protocol_stage": stage,
        "template_digest": template_digest(),
        "manifest_digest": digest_of(m),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["template", "validate"])
    parser.add_argument("path", nargs="?", help="input JSON file ('-' for stdin)")
    args = parser.parse_args(argv)
    try:
        if args.mode == "template":
            print(canonical({**build_template(), "template_digest": template_digest()}))
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
        print(canonical(validate_manifest(payload)))
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
