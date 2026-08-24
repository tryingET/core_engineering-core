#!/usr/bin/env python3
"""G0-A2 admission harness (engineering-core v1.0).

Validates the candidate-independent G0-A2 admission record: bound freeze
digests, unassigned candidate identity, impact matrix, transition templates,
and no 1.0.0/release claim. Executes no journeys and mutates nothing.

Modes:
  template   Emit the frozen admission schema (no file digests).
  validate   Validate one admission record against the repo tree.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "engineering-core.v1.g0a2/1"
UNASSIGNED = "unassigned"

REQUIRED_FREEZES = [
    "g1_protocol_plan",
    "g1_harness",
    "g2_protocol_plan",
    "g2_harness",
    "g3_handoff_plan",
    "g3_harness",
    "g4_protocol_plan",
    "g4_harness",
    "population_manifest",
    "compatibility_schema",
    "rendered_product_schema",
    "impact_matrix",
    "transition_templates",
]

CHANGE_CLASSES = [
    "protocol_template",
    "population",
    "compatibility_class",
    "rendered_product",
    "candidate_bytes",
    "empirical_protocol",
    "g4_content",
]

FORBIDDEN_KEYS = ("release_authority", "rollout_authority", "doctrine_authority")
FORBIDDEN_VALUES = ("1.0.0", "v1.0.0")


class ValidationError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest_of(obj) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(cond, code, detail):
    if not cond:
        raise ValidationError(code, detail)


def build_template() -> dict:
    return {
        "schema": SCHEMA,
        "stage": "g0a2-admission-template",
        "binding": "candidate_independent_g0a2",
        "candidate_commit": UNASSIGNED,
        "candidate_digest": UNASSIGNED,
        "package_version": UNASSIGNED,
        "required_freezes": list(REQUIRED_FREEZES),
        "change_classes": list(CHANGE_CLASSES),
        "admits": [
            "convergence_implementation_tasks",
            "owner_accepted_g4a_pilots",
        ],
        "does_not_admit": [
            "candidate_1_0_0",
            "g1_g4_outcome_capture",
            "publication",
            "participant_mutation_beyond_exact_owner_tasks",
        ],
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def validate_admission(record: dict, repo_root: Path) -> dict:
    _require(isinstance(record, dict), "not_an_object", "admission must be an object")
    for field in ("schema", "stage", "template_digest", "candidate_commit",
                  "candidate_digest", "package_version", "freezes", "impact_matrix_ref",
                  "transition_templates_ref", "decisions"):
        _require(field in record, "missing_field", f"admission missing: {field}")
    _require(record["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(record["stage"] == "g0a2-admission", "stage_mismatch",
             "expected stage g0a2-admission")
    _require(record["template_digest"] == template_digest(), "template_digest_mismatch",
             "admission template digest does not match frozen template")
    for field in ("candidate_commit", "candidate_digest", "package_version"):
        _require(record[field] == UNASSIGNED, "candidate_field_assigned",
                 f"{field} must remain '{UNASSIGNED}' until G0-B")
    def _walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                _require(k not in FORBIDDEN_KEYS, "forbidden_claim",
                         f"admission cannot contain field {k}")
                _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)
        elif isinstance(node, str):
            _require(node not in FORBIDDEN_VALUES, "forbidden_claim",
                     f"admission cannot claim {node}")

    _walk(record)

    freezes = record["freezes"]
    _require(isinstance(freezes, dict), "missing_field", "freezes object required")
    missing = [k for k in REQUIRED_FREEZES if k not in freezes]
    _require(not missing, "missing_freeze", f"missing freeze bindings: {missing}")
    checked = []
    for key in REQUIRED_FREEZES:
        entry = freezes[key]
        _require(isinstance(entry, dict) and entry.get("path") and entry.get("sha256"),
                 "missing_field", f"freeze {key} needs path and sha256")
        path = repo_root / entry["path"]
        _require(path.is_file(), "missing_file", f"freeze {key} file missing: {entry['path']}")
        actual = file_sha256(path)
        _require(actual == entry["sha256"], "digest_mismatch",
                 f"freeze {key} sha256 mismatch: recorded {entry['sha256']} actual {actual}")
        checked.append(key)

    for ref_field in ("impact_matrix_ref", "transition_templates_ref",
                      "compatibility_schema_ref", "rendered_product_schema_ref"):
        ref = record.get(ref_field)
        _require(isinstance(ref, str) and (repo_root / ref).is_file(),
                 "missing_file", f"{ref_field} missing: {ref}")

    decisions = record["decisions"]
    _require(decisions.get("governing") == 128, "missing_decision",
             "governing decision must be 128")
    _require(decisions.get("population") == 131, "missing_decision",
             "population decision must be 131")
    _require(decisions.get("g3_protocol") == 132, "missing_decision",
             "g3 protocol decision must be 132")

    return {
        "schema": SCHEMA,
        "stage": "g0a2-admission-validation",
        "status": "pass",
        "checked_freezes": checked,
        "admission_digest": digest_of(record),
        "template_digest": template_digest(),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["template", "validate"])
    parser.add_argument("path", nargs="?", help="admission JSON ('-' for stdin)")
    parser.add_argument("--repo-root", default=".", help="repository root for digest checks")
    args = parser.parse_args(argv)
    try:
        if args.mode == "template":
            print(canonical({**build_template(), "template_digest": template_digest()}))
            return 0
        if not args.path:
            print(json.dumps({"status": "fail", "code": "missing_input"}), file=sys.stderr)
            return 3
        raw = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(json.dumps({"status": "fail", "code": "invalid_json",
                              "detail": str(exc)}), file=sys.stderr)
            return 2
        print(canonical(validate_admission(payload, Path(args.repo_root).resolve())))
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
