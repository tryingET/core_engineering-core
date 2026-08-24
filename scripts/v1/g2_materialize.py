#!/usr/bin/env python3
"""G2 candidate-bound materializer (engineering-core v1.0).

Binds the frozen G2 template to the G0-B candidate SHA and validates
every fixture instance. Does not modify federated_interoperation.py.
Does not claim Gate G2 PASS.

Modes:
  emit       Write the materialization record (JSON) to stdout.
  validate   Validate a materialization record.
  wheel-smoke  Run no-effect CLI entrypoints from an installed candidate.

Exit codes: 0 pass; 2 validation failure; 3 usage/io error.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

SCHEMA = "engineering-core.v1.g2-materialization/1"
CANDIDATE_COMMIT = "b313becf7f1bf5261843d7b29c939b0bc5072ef1"
CANDIDATE_BRANCH = "proof/v1-candidate-2"


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


def load_fi():
    path = Path(__file__).resolve().parent / "federated_interoperation.py"
    spec = importlib.util.spec_from_file_location("federated_interoperation", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def expected_for(fi, cls: str) -> tuple[str, str | None]:
    if cls in fi.EXPECTED_BY_CLASS:
        outcome = fi.EXPECTED_BY_CLASS[cls]
        boundary = "ingress_parse" if outcome == "fail_at_boundary" else None
        return outcome, boundary
    if cls in fi.POPULATION_CLASSES:
        return "incomplete", None
    if cls in fi.FAILING_FAMILIES:
        return "fail_at_boundary", "ingress_parse"
    if cls in ("duplicate_json", "reordering", "catalog_skew"):
        return "pass", None
    return "fail_at_boundary", "ingress_parse"


def make_fixture(fi, cls: str) -> dict:
    outcome, boundary = expected_for(fi, cls)
    return {
        "schema": fi.SCHEMA,
        "stage": "g2-fixture-instance",
        "fixture_class": cls,
        "expected_outcome": outcome,
        "boundary": boundary,
        "diagnostics": {"sanitized": True, "contains_private_metadata": False},
        "candidate_binding": fi.UNASSIGNED,
    }


def emit_record(fi) -> dict:
    fixtures = [make_fixture(fi, cls) for cls in fi.ALL_FIXTURE_CLASSES]
    validations = []
    for fix in fixtures:
        out = fi.validate_fixture(fix)
        validations.append({
            "fixture_class": fix["fixture_class"],
            "status": out["status"],
            "expected_outcome": out["expected_outcome"],
            "fixture_digest": out["fixture_digest"],
            "candidate_commit": CANDIDATE_COMMIT,
        })
    matrix = []
    executed_families = {"compatibility"}  # wheel smoke covers public CLI only
    for ep in fi.ENTRYPOINTS:
        for family in fi.THREAT_FAMILIES:
            executed = ep == "cli_command" and family in executed_families
            matrix.append({
                "entrypoint": ep,
                "threat_family": family,
                "state": "executed_no_effect" if executed else "materialized_not_executed",
            })
    return {
        "schema": SCHEMA,
        "stage": "g2-materialization",
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_branch": CANDIDATE_BRANCH,
        "g2_pass_claimed": False,
        "template_schema": fi.SCHEMA,
        "fixture_count": len(fixtures),
        "fixtures": fixtures,
        "validations": validations,
        "matrix": matrix,
        "executed_cells": sum(1 for c in matrix if c["state"] == "executed_no_effect"),
        "materialized_only_cells": sum(1 for c in matrix if c["state"] != "executed_no_effect"),
    }


def validate_record(record: dict) -> dict:
    fi = load_fi()
    for field in ("schema", "stage", "candidate_commit", "fixtures", "validations",
                  "matrix", "g2_pass_claimed"):
        _require(isinstance(record, dict) and field in record, "missing_field",
                 f"record missing: {field}")
    _require(record["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(record["stage"] == "g2-materialization", "stage_mismatch",
             "expected stage g2-materialization")
    _require(record["candidate_commit"] == CANDIDATE_COMMIT, "wrong_candidate",
             "candidate SHA must be the frozen G0-B commit")
    _require(record["g2_pass_claimed"] is False, "pass_claimed",
             "this slice must not claim G2 PASS")
    classes = [f["fixture_class"] for f in record["fixtures"]]
    _require(classes == list(fi.ALL_FIXTURE_CLASSES), "class_set_mismatch",
             "fixtures must be exactly the frozen class list in order")
    for fix in record["fixtures"]:
        _require(fix.get("candidate_binding") == fi.UNASSIGNED,
                 "fixture_mutated",
                 f"{fix.get('fixture_class')} must keep candidate_binding unassigned in the G0-A2 fixture")
        out = fi.validate_fixture(fix)
        _require(out["status"] == "pass", "fixture_invalid",
                 f"{fix['fixture_class']} failed frozen validate-fixture")
    _require(len(record["validations"]) == len(fi.ALL_FIXTURE_CLASSES),
             "validation_count", "validation rows must match fixture count")
    for row in record["validations"]:
        _require(row.get("candidate_commit") == CANDIDATE_COMMIT, "candidate_unbound",
                 f"{row.get('fixture_class')} materialization is not bound to the candidate")
    _require(len(record["matrix"]) == len(fi.ENTRYPOINTS) * len(fi.THREAT_FAMILIES),
             "matrix_incomplete", "entrypoint x threat matrix is incomplete")
    return {
        "schema": SCHEMA,
        "stage": "g2-materialization-validation",
        "status": "pass",
        "fixture_count": len(record["fixtures"]),
        "matrix_cells": len(record["matrix"]),
        "g2_pass_claimed": False,
        "record_digest": digest_of(record),
    }


def wheel_smoke(python: str) -> dict:
    exe = str(Path(python).parent / "engineering-core")
    commands = [
        ["--help"],
        ["list"],
        ["list-disciplines"],
        ["catalog"],
    ]
    results = []
    for argv in commands:
        proc = subprocess.run([exe, *argv], capture_output=True, text=True)
        results.append({
            "argv": argv,
            "exit": proc.returncode,
            "stdout_bytes": len(proc.stdout.encode()),
            "pass": proc.returncode == 0,
        })
    failed = [r for r in results if not r["pass"]]
    return {
        "candidate_commit": CANDIDATE_COMMIT,
        "entrypoint": "cli_command",
        "commands": results,
        "status": "pass" if not failed else "fail",
        "failed": failed,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["emit", "validate", "wheel-smoke"])
    parser.add_argument("path", nargs="?", help="materialization JSON or python exe")
    args = parser.parse_args(argv)
    try:
        if args.mode == "emit":
            print(canonical(emit_record(load_fi())))
            return 0
        if args.mode == "wheel-smoke":
            if not args.path:
                print(json.dumps({"status": "fail", "code": "missing_input"}), file=sys.stderr)
                return 3
            out = wheel_smoke(args.path)
            print(canonical(out))
            return 0 if out["status"] == "pass" else 2
        if not args.path:
            print(json.dumps({"status": "fail", "code": "missing_input"}), file=sys.stderr)
            return 3
        raw = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
        print(canonical(validate_record(json.loads(raw))))
        return 0
    except ValidationError as exc:
        print(json.dumps({"status": "fail", "code": exc.code, "detail": exc.detail}),
              file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(json.dumps({"status": "fail", "code": "invalid_json", "detail": str(exc)}),
              file=sys.stderr)
        return 2
    except OSError as exc:
        print(json.dumps({"status": "fail", "code": "io_error", "detail": str(exc)}),
              file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
