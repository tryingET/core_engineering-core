#!/usr/bin/env python3
"""G0-A3 candidate-admission harness (engineering-core v1.0).

Read-only verifier for the immutable candidate-admission record. Binds
G0-A2 freezes, G4-A lineage, the exact candidate task, and the path
allowlist. Does not create a candidate, set 1.0.0, or run journeys.

Modes:
  template   Emit the frozen admission schema.
  validate   Validate one admission record against the repo tree.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "engineering-core.v1.g0a3/1"
UNASSIGNED = "unassigned"
CANDIDATE_TASK_ID = 4876
REQUIRED_ALLOWLIST = [
    "CHANGELOG.md",
    "README.md",
    "catalog-history/**",
    "catalog.json",
    "docs/releases/**",
    "docs/support-policy.md",
    "pyproject.toml",
    "src/engineering_core/__init__.py",
    "src/engineering_core/catalog-history/**",
    "src/engineering_core/catalog.json",
    "uv.lock",
]
REQUIRED_BINDINGS = [
    "g0a2_admission",
    "population_manifest",
    "g4a_content_owner_decisions",
    "impact_matrix",
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
        "stage": "g0a3-admission-template",
        "binding": "source_to_candidate_admission",
        "candidate_commit": UNASSIGNED,
        "candidate_digest": UNASSIGNED,
        "package_version": UNASSIGNED,
        "candidate_task_id": CANDIDATE_TASK_ID,
        "required_allowlist": list(REQUIRED_ALLOWLIST),
        "required_bindings": list(REQUIRED_BINDINGS),
        "accepted_g4_content_may_be_empty": True,
        "target_channel_must_not_be_main": True,
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def validate_admission(record: dict, repo_root: Path) -> dict:
    _require(isinstance(record, dict), "not_an_object", "admission must be an object")
    for field in ("schema", "stage", "template_digest", "base_commit",
                  "candidate_commit", "candidate_digest", "package_version",
                  "candidate_task_id", "target_channel", "path_allowlist",
                  "bindings", "accepted_g4_content", "revised_lineage",
                  "decisions"):
        _require(field in record, "missing_field", f"admission missing: {field}")
    _require(record["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(record["stage"] == "g0a3-admission", "stage_mismatch",
             "expected stage g0a3-admission")
    _require(record["template_digest"] == template_digest(), "template_digest_mismatch",
             "admission template digest does not match frozen template")
    for field in ("candidate_commit", "candidate_digest", "package_version"):
        _require(record[field] == UNASSIGNED, "candidate_field_assigned",
                 f"{field} must remain '{UNASSIGNED}' until the candidate task")
    _require(record["candidate_task_id"] == CANDIDATE_TASK_ID, "wrong_candidate_task",
             f"candidate task must be {CANDIDATE_TASK_ID}")
    _require(isinstance(record["base_commit"], str)
             and len(record["base_commit"]) == 40
             and all(c in "0123456789abcdef" for c in record["base_commit"]),
             "invalid_base_commit", "base_commit must be a full lowercase Git object id")
    _require(record["target_channel"] not in ("main", "master"), "target_is_main",
             "target channel must be an isolated non-main proof channel")

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

    allow = record["path_allowlist"]
    _require(allow == REQUIRED_ALLOWLIST, "allowlist_mismatch",
             "path allowlist must equal the frozen 4876 scope")

    bindings = record["bindings"]
    _require(isinstance(bindings, dict), "missing_field", "bindings object required")
    missing = [k for k in REQUIRED_BINDINGS if k not in bindings]
    _require(not missing, "missing_binding", f"missing bindings: {missing}")
    for key in REQUIRED_BINDINGS:
        entry = bindings[key]
        _require(isinstance(entry, dict) and entry.get("path") and entry.get("sha256"),
                 "missing_field", f"binding {key} needs path and sha256")
        path = repo_root / entry["path"]
        _require(path.is_file(), "missing_file", f"binding {key} missing: {entry['path']}")
        actual = file_sha256(path)
        _require(actual == entry["sha256"], "digest_mismatch",
                 f"binding {key} sha256 mismatch")

    accepted = record["accepted_g4_content"]
    _require(isinstance(accepted, list), "missing_field", "accepted_g4_content must be a list")
    lineage = record["revised_lineage"]
    _require(isinstance(lineage, list) and len(lineage) >= 3, "lineage_too_small",
             "need at least three revised/negative lineage entries")
    for item in lineage:
        _require(isinstance(item, dict) and item.get("cycle_id") and item.get("disposition") == "revised"
                 and item.get("immutable") is True,
                 "invalid_lineage",
                 "each lineage entry needs cycle_id, disposition=revised, immutable=true")

    decisions = record["decisions"]
    _require(decisions.get("governing") == 128, "missing_decision", "governing must be 128")
    _require(decisions.get("g0a2") == 134, "missing_decision", "g0a2 must be 134")
    _require(decisions.get("population") == 131, "missing_decision", "population must be 131")

    return {
        "schema": SCHEMA,
        "stage": "g0a3-admission-validation",
        "status": "pass",
        "candidate_task_id": CANDIDATE_TASK_ID,
        "accepted_g4_content_count": len(accepted),
        "revised_lineage_count": len(lineage),
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
