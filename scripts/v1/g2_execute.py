#!/usr/bin/env python3
"""G2 additional candidate-wheel probes (engineering-core v1.0).

Runs a bounded probe table against an installed candidate CLI. Does not
claim Gate G2 PASS. Does not modify federated_interoperation.py.

Modes:
  run       Execute probes; write JSON to stdout.
  validate  Validate an execution record.

Exit 0 pass; 2 validation/probe failure; 3 usage/io.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCHEMA = "engineering-core.v1.g2-execution/1"
CANDIDATE_COMMIT = "7a41ea321015c6a5210d6ea26b6f3e5ac6632045"

# expected: "zero" (exit 0) or "nonzero"
PROBES = [
    {"id": "help", "argv": ["--help"], "expected": "zero",
     "entrypoint": "cli_command", "threat_family": "compatibility",
     "fixture_class": "canonical_candidate_v1"},
    {"id": "list", "argv": ["list"], "expected": "zero",
     "entrypoint": "cli_command", "threat_family": "compatibility",
     "fixture_class": "canonical_candidate_v1"},
    {"id": "show-py", "argv": ["show", "py"], "expected": "zero",
     "entrypoint": "renderer", "threat_family": "compatibility",
     "fixture_class": "canonical_candidate_v1"},
    {"id": "unknown-command", "argv": ["this-command-does-not-exist"], "expected": "nonzero",
     "entrypoint": "cli_command", "threat_family": "malformed_input",
     "fixture_class": "malformed_json"},
    {"id": "show-missing-lane", "argv": ["show"], "expected": "nonzero",
     "entrypoint": "parser", "threat_family": "malformed_input",
     "fixture_class": "unknown_fields"},
    {"id": "plan-missing-repo-flag", "argv": ["plan"], "expected": "nonzero",
     "entrypoint": "parser", "threat_family": "malformed_input",
     "fixture_class": "malformed_json"},
    {"id": "plan-absent-repo", "argv": ["plan", "--repo", "definitely-missing-repo-xyz"],
     "expected": "nonzero", "entrypoint": "cli_command", "threat_family": "population_missingness",
     "fixture_class": "unavailable"},
    {"id": "plan-traversal-repo", "argv": ["plan", "--repo", "../../etc/passwd"],
     "expected": "nonzero", "entrypoint": "cli_command", "threat_family": "path_attack",
     "fixture_class": "path_traversal"},
    {"id": "scan-missing-scope", "argv": ["scan-adoption", "--scope", "definitely-missing-scope-xyz",
                                          "--format", "json"],
     "expected": "zero", "entrypoint": "cli_command", "threat_family": "population_missingness",
     "fixture_class": "unavailable"},
    {"id": "doctor-absent", "argv": ["doctor", "--repo", "definitely-missing-repo-xyz"],
     "expected": "nonzero", "entrypoint": "cli_command", "threat_family": "population_missingness",
     "fixture_class": "unavailable"},
]


class ValidationError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _require(cond, code, detail):
    if not cond:
        raise ValidationError(code, detail)


def run_probes(exe: str) -> dict:
    results = []
    for probe in PROBES:
        proc = subprocess.run([exe, *probe["argv"]], capture_output=True, text=True)
        zero = proc.returncode == 0
        ok = zero if probe["expected"] == "zero" else (not zero)
        results.append({
            "id": probe["id"],
            "argv": probe["argv"],
            "expected": probe["expected"],
            "exit": proc.returncode,
            "pass": ok,
            "entrypoint": probe["entrypoint"],
            "threat_family": probe["threat_family"],
            "fixture_class": probe["fixture_class"],
            "stdout_bytes": len(proc.stdout.encode()),
            "stderr_bytes": len(proc.stderr.encode()),
        })
    failed = [r for r in results if not r["pass"]]
    cells = sorted({(r["entrypoint"], r["threat_family"]) for r in results if r["pass"]})
    return {
        "schema": SCHEMA,
        "stage": "g2-execution",
        "candidate_commit": CANDIDATE_COMMIT,
        "g2_pass_claimed": False,
        "probe_count": len(results),
        "probes": results,
        "failed": [r["id"] for r in failed],
        "executed_cells": [{"entrypoint": e, "threat_family": t} for e, t in cells],
        "status": "pass" if not failed else "pass_with_findings",
        "findings": [r["id"] for r in failed],
    }


def validate_record(record: dict) -> dict:
    for field in ("schema", "stage", "candidate_commit", "probes", "g2_pass_claimed", "status"):
        _require(isinstance(record, dict) and field in record, "missing_field",
                 f"missing {field}")
    _require(record["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(record["candidate_commit"] == CANDIDATE_COMMIT, "wrong_candidate",
             "candidate SHA mismatch")
    _require(record["g2_pass_claimed"] is False, "pass_claimed",
             "must not claim G2 PASS")
    _require(len(record["probes"]) == len(PROBES), "probe_count",
             "probe table drifted")
    _require(record["status"] in ("pass", "pass_with_findings"), "bad_status",
             f"status {record['status']}")
    if record["status"] == "pass":
        _require(not record.get("failed"), "probes_failed", "status pass but failed nonempty")
    else:
        _require(record.get("findings") or record.get("failed"), "missing_findings",
                 "pass_with_findings requires findings")
    return {"schema": SCHEMA, "stage": "g2-execution-validation", "status": "pass",
            "record_status": record["status"],
            "probe_count": len(record["probes"]),
            "executed_cells": len(record.get("executed_cells") or [])}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["run", "validate"])
    parser.add_argument("path", help="engineering-core exe (run) or JSON (validate)")
    args = parser.parse_args(argv)
    try:
        if args.mode == "run":
            rec = run_probes(args.path)
            print(json.dumps(rec, sort_keys=True, separators=(",", ":")))
            return 0
        raw = Path(args.path).read_text(encoding="utf-8")
        print(json.dumps(validate_record(json.loads(raw)), sort_keys=True, separators=(",", ":")))
        return 0
    except ValidationError as exc:
        print(json.dumps({"status": "fail", "code": exc.code, "detail": exc.detail}),
              file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "code": "error", "detail": str(exc)}),
              file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
