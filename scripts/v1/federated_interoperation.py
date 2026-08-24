#!/usr/bin/env python3
"""G2 federated-interoperation conformance harness (engineering-core v1.0).

Internal qualification tooling. Freezes and validates the candidate-independent
fixture-template corpus, entrypoint x threat matrix, version-negotiation
transcripts, adapter-chain records, and resource-bound manifests for RFC Gate
G2. Executes no participant command, model, URL, or helper; mutates nothing.

Modes:
  template               Emit the frozen candidate-independent corpus template.
  validate-fixture       Validate one fixture instance against the template.
  validate-negotiation   Validate one offer/selection transcript.
  validate-adapter       Validate one ingress conversion record.
  check-bounds           Validate one resource-bound manifest.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

SCHEMA = "engineering-core.v1.g2/1"
UNASSIGNED = "unassigned"

VALID_FIXTURE_CLASSES = [
    "pre_v1_clean_transition",
    "pre_v1_explicit_migration",
    "pre_v1_unsupported",
    "canonical_candidate_v1",
    "additive_v1x",
    "unsupported_future_major",
    "unknown_critical_extension",
]

POPULATION_CLASSES = [
    "complete", "partial", "unavailable", "denied",
    "redacted", "stale", "unsupported",
]

STRUCTURE_CLASSES = [
    "duplicate_json", "reordering", "unknown_fields", "unknown_schema", "catalog_skew",
]

HOSTILE_CLASSES = [
    "malformed_json", "invalid_utf8", "depth_limit", "size_limit", "growth_limit",
    "exact_limit", "path_absolute", "path_empty", "path_dot", "path_traversal",
    "path_control_chars", "path_option_injection", "revision_ambiguous",
    "symlink_target", "hardlink_target", "special_file", "unreadable_file",
    "unwritable_file", "parent_replacement", "toctou_race", "hostile_git_helper",
    "terminal_injection", "markdown_injection", "html_injection", "link_injection",
    "url_payload", "tool_instruction", "hostile_patch", "hostile_model_response",
]

ALL_FIXTURE_CLASSES = VALID_FIXTURE_CLASSES + POPULATION_CLASSES + STRUCTURE_CLASSES + HOSTILE_CLASSES

FAILING_FAMILIES = set(HOSTILE_CLASSES) | {
    "unknown_fields", "unknown_schema",
}
STRUCTURED_OUTCOMES = {"pass", "fail_at_boundary", "incomplete", "unsupported"}

ENTRYPOINTS = [
    "cli_command", "parser", "renderer", "git_subprocess", "output_path",
    "owner_transfer", "model_response_sink",
]

THREAT_FAMILIES = ["compatibility", "population_missingness", "malformed_input",
                   "path_attack", "race_replacement", "injection", "hostile_source"]

NEGOTIATION_VERSIONS = ["1", "1.1", "1.2", "2"]


EXPECTED_BY_CLASS = {
    "pre_v1_clean_transition": "pass",
    "pre_v1_explicit_migration": "incomplete",
    "pre_v1_unsupported": "unsupported",
    "canonical_candidate_v1": "pass",
    "additive_v1x": "pass",
    "unsupported_future_major": "unsupported",
    "unknown_critical_extension": "fail_at_boundary",
}


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
    matrix_rows = {}
    for ep in ENTRYPOINTS:
        matrix_rows[ep] = {family: UNASSIGNED for family in THREAT_FAMILIES}
    return {
        "schema": SCHEMA,
        "stage": "g2-corpus-template",
        "binding": "candidate_independent_g0a2",
        "candidate_commit": UNASSIGNED,
        "candidate_digest": UNASSIGNED,
        "normalization": {
            "canonicalization": "rfc8785_jcs",
            "ordering_permitted": ["top_level_list_order"],
            "algorithm_digest": UNASSIGNED,
        },
        "fixture_classes": {
            "valid": VALID_FIXTURE_CLASSES,
            "population": POPULATION_CLASSES,
            "structure": STRUCTURE_CLASSES,
            "hostile": HOSTILE_CLASSES,
            "failing_families": sorted(FAILING_FAMILIES),
        },
        "entrypoint_threat_matrix": matrix_rows,
        "negotiation": {
            "offer_required_fields": ["peer_identities", "offer_id", "freshness_scope",
                                      "replay_scope", "channel_binding", "payload_digest",
                                      "offered_versions"],
            "floor_required": True,
            "selection_rule": "highest_common_version_at_or_above_floor",
            "fallback_on_parse_error": False,
            "fallback_on_attacker_claim": False,
            "unknown_critical_extension": "fail_closed",
            "unknown_non_critical": "declared_preserve_or_ignore",
        },
        "adapter_chain": {
            "conversion_sites": "bounded_ingress_once",
            "required_bindings": ["input_digest", "output_digest",
                                  "adapter_executable_digest", "trust_decision",
                                  "identity_version", "defaults", "transformations",
                                  "losses", "prior_chain_digest"],
            "double_conversion": "fail",
            "chain_truncation": "fail",
        },
        "denominators": "every count and percentage binds its exact frozen denominator",
        "no_central_control_plane": True,
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def validate_fixture(fixture: dict) -> dict:
    _require(isinstance(fixture, dict), "not_an_object", "fixture must be an object")
    for field in ("schema", "stage", "fixture_class", "expected_outcome",
                  "boundary", "diagnostics"):
        _require(field in fixture, "missing_field", f"fixture missing: {field}")
    _require(fixture["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(fixture["stage"] == "g2-fixture-instance", "stage_mismatch",
             "expected stage g2-fixture-instance")
    cls = fixture["fixture_class"]
    _require(cls in ALL_FIXTURE_CLASSES, "unknown_class", f"unknown fixture class: {cls}")
    _require(fixture.get("candidate_binding") == UNASSIGNED, "candidate_field_assigned",
             "candidate_binding must remain unassigned until G0-B")
    expected = fixture["expected_outcome"]
    _require(expected in STRUCTURED_OUTCOMES, "invalid_outcome",
             f"expected_outcome must be one of {sorted(STRUCTURED_OUTCOMES)}")
    if cls in EXPECTED_BY_CLASS:
        _require(expected == EXPECTED_BY_CLASS[cls], "outcome_class_mismatch",
                 f"class {cls} must expect {EXPECTED_BY_CLASS[cls]}")
        if expected == "fail_at_boundary":
            _require(isinstance(fixture["boundary"], str) and fixture["boundary"],
                     "missing_boundary",
                     "failing fixture requires a named frozen boundary")
    if cls in FAILING_FAMILIES:
        _require(expected == "fail_at_boundary", "outcome_class_mismatch",
                 f"failing class {cls} must expect fail_at_boundary")
        _require(isinstance(fixture["boundary"], str) and fixture["boundary"],
                 "missing_boundary", "failing fixture requires a named frozen boundary")
    if cls in POPULATION_CLASSES:
        _require(expected == "incomplete", "outcome_class_mismatch",
                 f"population class {cls} must expect incomplete, never a coerced state")
    _require(isinstance(fixture["diagnostics"], dict)
             and fixture["diagnostics"].get("sanitized") is True,
             "unsanitized_diagnostics", "diagnostics must be structured and sanitized")
    _require(not fixture["diagnostics"].get("contains_private_metadata"),
             "private_metadata_leak", "diagnostics must not contain private metadata")
    return {
        "schema": SCHEMA,
        "stage": "g2-fixture-validation",
        "status": "pass",
        "fixture_class": cls,
        "expected_outcome": expected,
        "boundary": fixture.get("boundary"),
        "fixture_digest": digest_of(fixture),
    }


def validate_negotiation(t: dict) -> dict:
    for field in ("schema", "stage", "offer", "allowlist", "floor", "result"):
        _require(isinstance(t, dict) and field in t, "missing_field",
                 f"transcript missing: {field}")
    _require(t["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(t["stage"] == "g2-negotiation-transcript", "stage_mismatch",
             "expected stage g2-negotiation-transcript")
    offer = t["offer"]
    for field in build_template()["negotiation"]["offer_required_fields"]:
        _require(offer.get(field) not in (None, "", []), "missing_field",
                 f"offer missing: {field}")
    _require(t.get("floor") in NEGOTIATION_VERSIONS, "invalid_floor",
             f"floor must be one of {NEGOTIATION_VERSIONS}")
    _require(isinstance(t.get("allowlist"), list) and t["allowlist"],
             "missing_field", "trusted allowlist required")
    result = t["result"]
    for field in ("selected_version", "replay_detected", "offer_stripped",
                  "parse_error", "payload_digest_bound", "full_offer_bound"):
        _require(field in result, "missing_field", f"result missing: {field}")
    _require(result["replay_detected"] is not True, "replayed_offer",
             "replayed offers must be rejected, not selected")
    _require(result["offer_stripped"] is not True, "stripped_offer",
             "stripped offers must be rejected")
    if result["parse_error"]:
        _require(result["selected_version"] is None, "fallback_on_parse_error",
                 "parse error must never select a version")
    offered = [v for v in offer["offered_versions"] if v in t["allowlist"]]
    offered_at_floor = [v for v in offered
                        if NEGOTIATION_VERSIONS.index(v) >= NEGOTIATION_VERSIONS.index(t["floor"])]
    expected_pick = (max(offered_at_floor, key=lambda v: NEGOTIATION_VERSIONS.index(v))
                     if offered_at_floor else None)
    _require(result["selected_version"] == expected_pick, "selection_rule_violated",
             f"expected {expected_pick}, got {result['selected_version']}")
    _require(result["payload_digest_bound"] is True and result["full_offer_bound"] is True,
             "unbound_selection", "selection must bind payload digest and full offer")
    return {
        "schema": SCHEMA, "stage": "g2-negotiation-validation", "status": "pass",
        "selected_version": result["selected_version"], "transcript_digest": digest_of(t),
    }


def validate_adapter(rec: dict) -> dict:
    for field in ("schema", "stage", "input_digest", "output_digest",
                  "adapter_executable_digest", "trust_decision", "identity_version",
                  "defaults", "transformations", "losses", "prior_chain_digest",
                  "conversion_site"):
        _require(isinstance(rec, dict) and rec.get(field) not in (None, ""),
                 "missing_field", f"adapter record missing: {field}")
    _require(rec["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(rec["stage"] == "g2-adapter-conversion", "stage_mismatch",
             "expected stage g2-adapter-conversion")
    _require(rec["conversion_site"] == "bounded_ingress", "double_conversion",
             "conversion is legal only once at bounded ingress")
    _require(rec.get("already_canonical_input") is not True, "double_conversion",
             "re-converting an already canonical record is forbidden")
    _require(rec.get("chain_truncated") is not True, "chain_truncation",
             "prior chain must be carried, not truncated")
    loss = rec["losses"]
    _require(loss in ("none", "declared_non_critical"), "invalid_loss",
             "critical-field loss must yield unsupported, not a conversion record")
    _require(rec["trust_decision"] in ("trusted", "untrusted_rejected"),
             "invalid_trust", "trust decision must be explicit")
    return {"schema": SCHEMA, "stage": "g2-adapter-validation", "status": "pass",
            "adapter_digest": digest_of(rec)}


def check_bounds(b: dict) -> dict:
    for field in ("schema", "stage", "budgets", "public_acceptance_floor",
                  "derivation", "margin", "output_visibility_frozen"):
        _require(isinstance(b, dict) and field in b, "missing_field",
                 f"bounds manifest missing: {field}")
    _require(b["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(b["stage"] == "g2-resource-bounds", "stage_mismatch",
             "expected stage g2-resource-bounds")
    budgets = b["budgets"]
    for field in ("population", "filesystem", "output_bytes", "memory", "cpu_seconds",
                  "subprocess_count", "wall_clock_seconds"):
        _require(isinstance(budgets.get(field), (int, float)) and budgets[field] > 0,
                 "missing_field", f"budget missing or non-positive: {field}")
    floor = b["public_acceptance_floor"]
    for field in ("max_nesting", "max_members", "max_string_bytes",
                  "max_payload_bytes", "max_path_length"):
        _require(isinstance(floor.get(field), int) and floor[field] > 0,
                 "missing_field", f"public floor missing: {field}")
    for scope, fkey in (("population", "max_members"),
                       ("output_bytes", "max_payload_bytes")):
        _require(budgets[scope] >= floor[fkey], "budget_undercuts_public_floor",
                 f"budget {scope} undercuts public floor {fkey}")
    d = b["derivation"]
    for field in ("measured_baseline", "benchmark", "toolchain", "rationale"):
        _require(d.get(field) not in (None, ""), "missing_field",
                 f"derivation missing: {field}")
    _require(isinstance(b.get("margin"), (int, float)) and b["margin"] > 0,
             "missing_margin", "positive safety margin required")
    if b["output_visibility_frozen"] is True:
        _require(b.get("bounds_revision") in (None, "", UNASSIGNED),
                 "bounds_raised_after_visibility",
                 "bounds cannot be raised after output visibility")
    return {"schema": SCHEMA, "stage": "g2-bounds-validation", "status": "pass",
            "budgets": sorted(budgets), "bounds_digest": digest_of(b)}


MODES = {
    "template": lambda a: {**build_template(), "template_digest": template_digest()},
    "validate-fixture": validate_fixture,
    "validate-negotiation": validate_negotiation,
    "validate-adapter": validate_adapter,
    "check-bounds": check_bounds,
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=sorted(MODES))
    parser.add_argument("path", nargs="?", help="input JSON file ('-' for stdin)")
    args = parser.parse_args(argv)
    try:
        if args.mode == "template":
            print(canonical(MODES["template"](None)))
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
        print(canonical(MODES[args.mode](payload)))
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
