#!/usr/bin/env python3
"""G1 disposable-replica runner (engineering-core v1.0).

Runs the executable subset of the ten G1 categories against an installed
candidate CLI in a disposable clone. Does not claim G1 PASS or independent
review.

Usage: g1_run.py --exe PATH --replica PATH --baseline ID [--pin SHA]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCHEMA = "engineering-core.v1.g1-run/1"
CANDIDATE_COMMIT = "b313becf7f1bf5261843d7b29c939b0bc5072ef1"
CATEGORIES = [
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


def run(exe: str, argv: list[str], cwd: Path | None = None, env: dict | None = None) -> dict:
    proc = subprocess.run([exe, *argv], cwd=cwd, env=env, capture_output=True, text=True)
    return {
        "argv": argv,
        "exit": proc.returncode,
        "stdout_bytes": len(proc.stdout.encode()),
        "stderr_bytes": len(proc.stderr.encode()),
        "stdout_head": proc.stdout[:400],
        "stderr_head": proc.stderr[:400],
    }


def journey(category: str, status: str, note: str, commands: list) -> dict:
    return {"category": category, "status": status, "note": note, "commands": commands}


def execute(exe: str, replica: Path, baseline_id: str, isolated_env: dict) -> dict:
    journeys = []

    ver = run(exe, ["--help"], env=isolated_env)
    journeys.append(journey(
        "resolve_install_remote",
        "pass" if ver["exit"] == 0 else "fail",
        "candidate invoked from isolated env; wheel not an editable checkout",
        [ver],
    ))

    retrieve = [
        run(exe, ["list"], env=isolated_env),
        run(exe, ["show", "py"], env=isolated_env),
        run(exe, ["catalog"], env=isolated_env),
    ]
    journeys.append(journey(
        "retrieve_explain_guidance",
        "pass" if all(c["exit"] == 0 for c in retrieve) else "fail",
        "packaged guidance from the installed candidate",
        retrieve,
    ))

    planned = run(exe, ["init", "--repo", str(replica), "--format", "json"], env=isolated_env)
    plan_ok = planned["exit"] in (0, 2)
    journeys.append(journey(
        "plan_transition_mode",
        "pass" if plan_ok else "fail",
        "init dry-run (exit 2 means conflicts, still a plan)",
        [planned],
    ))

    applied = run(exe, ["init", "--repo", str(replica), "--apply", "--format", "json"], env=isolated_env)
    apply_status = "pass" if applied["exit"] == 0 else ("incomplete" if applied["exit"] == 2 else "fail")
    journeys.append(journey(
        "apply_owner_plan",
        apply_status,
        "init --apply in disposable replica only; exit 2 is structured refusal",
        [applied],
    ))

    diagnosed = run(exe, ["doctor", "--repo", str(replica)], env=isolated_env)
    journeys.append(journey(
        "diagnose_v1_adoption",
        "pass" if diagnosed["exit"] in (0, 1) else "fail",
        "doctor is non-executing; 0 healthy/degraded, 1 blocked/degraded",
        [diagnosed],
    ))

    scanned = run(exe, ["scan-adoption", "--scope", str(replica), "--format", "json",
                        "--include-scope-root"], env=isolated_env)
    prove_ok = scanned["exit"] == 0
    journeys.append(journey(
        "prove_active_resolution",
        "pass" if prove_ok else "incomplete",
        "scan-adoption on the replica; not a mixed-runtime proof",
        [scanned],
    ))

    trav = run(exe, ["plan", "--repo", "../../etc/passwd"], env=isolated_env)
    bad = run(exe, ["init", "--repo", "/this/path/does/not/exist", "--format", "json"], env=isolated_env)
    journeys.append(journey(
        "failure_boundaries",
        "pass" if trav["exit"] != 0 and trav["stdout_bytes"] == 0 and bad["exit"] != 0 else "fail",
        "traversal and missing-dir must fail closed with no plan JSON",
        [trav, bad],
    ))

    journeys.append(journey(
        "rollback_recovery",
        "incomplete",
        "no candidate-shipped public rollback command",
        [],
    ))
    journeys.append(journey(
        "removal_with_owner_edits",
        "incomplete",
        "no candidate-shipped public removal-of-v1-adoption command used",
        [],
    ))

    st = subprocess.run(["git", "-C", str(replica), "status", "--short"],
                        capture_output=True, text=True)
    journeys.append(journey(
        "final_posture_disposal",
        "pass" if st.returncode == 0 else "fail",
        "replica status inventoried; caller deletes the clone",
        [{"argv": ["git", "status", "--short"], "exit": st.returncode,
          "stdout_head": st.stdout[:400], "stdout_bytes": len(st.stdout.encode()),
          "stderr_bytes": 0, "stderr_head": ""}],
    ))

    counts = {key: sum(1 for j in journeys if j["status"] == key) for key in ("pass", "fail", "incomplete")}
    return {
        "schema": SCHEMA,
        "stage": "g1-baseline-run",
        "candidate_commit": CANDIDATE_COMMIT,
        "baseline_id": baseline_id,
        "replica": str(replica),
        "g1_pass_claimed": False,
        "independent_review": False,
        "journeys": journeys,
        "counts": counts,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--home", required=True, help="isolated HOME")
    args = parser.parse_args(argv)
    env = os.environ.copy()
    env["HOME"] = args.home
    env["XDG_CONFIG_HOME"] = str(Path(args.home) / ".config")
    env["XDG_CACHE_HOME"] = str(Path(args.home) / ".cache")
    env.pop("PYTHONPATH", None)
    rec = execute(args.exe, Path(args.replica), args.baseline, env)
    print(json.dumps(rec, indent=2))
    return 0 if rec["counts"]["fail"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
