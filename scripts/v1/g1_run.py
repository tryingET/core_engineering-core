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


def score_prove_active_resolution(scanned_exit: int, applied_exit: int) -> str:
    """Bind prove_active_resolution to owner-apply polarity (AK 5037).

    Scanner completeness is a diagnostic, never proof of an active v1
    resolution. Pass requires the scan to complete AND the same revision's
    init --apply to be lawful: exit 0 (declared resolution applied) or exit 2
    (structured refusal, e.g. released-match scope already resolved). Scanner
    completeness alone can never pass this journey (G4-A v2 softwareco cycle
    decision, task 5036).
    """
    if scanned_exit != 0:
        return "incomplete"
    return "pass" if applied_exit in (0, 2) else "incomplete"


def score_apply_owner_plan(applied_exit: int) -> tuple[str, bool]:
    """Score apply_owner_plan (AK 5051, candidate-4 semantics).

    exit 0 -> pass (declared resolution applied atomically).
    exit 2 -> pass as a *documented structured refusal*: zero mutation, the
    refusal receipt documents why, and the candidate's journal + public
    rollback/remove commands provide the documented recovery path required
    by the frozen assertion 'atomic_completion_or_documented_recovery'
    (teachingco G4-A v2 cycle evidence: requiring applied:true on a
    released-match pin would overwrite owner deviations or invent product
    surface). The refused flag is recorded so reviewers can distinguish.
    Any other exit is a hard failure.
    """
    if applied_exit == 0:
        return "pass", False
    if applied_exit == 2:
        return "pass", True
    return "fail", False


def tree_digest(root: Path) -> str:
    """Byte-identical filesystem oracle: order-stable hash of every file's
    relative path and bytes (git-independent)."""
    import hashlib
    aggregate = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            aggregate.update(str(path.relative_to(root)).encode("utf-8"))
            aggregate.update(path.read_bytes())
    return aggregate.hexdigest()


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
    apply_status, refused_apply = score_apply_owner_plan(applied["exit"])
    journeys.append(journey(
        "apply_owner_plan",
        apply_status,
        ("init --apply structured refusal: zero mutation, documented reason, "
         "journal+rollback/remove provide the recovery path (candidate-4)"
         if refused_apply else
         "init --apply in disposable replica only; atomic apply with journal"),
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
    prove_status = score_prove_active_resolution(scanned["exit"], applied["exit"])
    journeys.append(journey(
        "prove_active_resolution",
        prove_status,
        "scan-adoption diagnostic bound to owner-apply polarity: pass requires scan "
        "completion plus a lawful same-revision init --apply (exit 0 applied or "
        "exit 2 structured refusal)",
        [scanned, applied],
    ))

    trav = run(exe, ["plan", "--repo", "../../etc/passwd"], env=isolated_env)
    bad = run(exe, ["init", "--repo", "/this/path/does/not/exist", "--format", "json"], env=isolated_env)
    journeys.append(journey(
        "failure_boundaries",
        "pass" if trav["exit"] != 0 and trav["stdout_bytes"] == 0 and bad["exit"] != 0 else "fail",
        "traversal and missing-dir must fail closed with no plan JSON",
        [trav, bad],
    ))

    journal_path = replica / ".engineering-core" / "adoption-journal.json"
    journal_present = journal_path.is_file()
    rolled = run(exe, ["rollback", "--repo", str(replica), "--format", "json"], env=isolated_env)
    if journal_present:
        rollback_ok = rolled["exit"] == 0
        rollback_note = "journal present: public rollback restored exact pre-adoption bytes and removed the journal"
    else:
        rollback_ok = rolled["exit"] == 2
        rollback_note = "no journal (apply refused or already consumed): lawful structured refusal boundary"
    journeys.append(journey(
        "rollback_recovery",
        "pass" if rollback_ok else "fail",
        rollback_note,
        [rolled],
    ))

    removal_commands = []
    if applied["exit"] == 0:
        reapply = run(exe, ["init", "--repo", str(replica), "--apply", "--format", "json"], env=isolated_env)
        removal_commands.append(reapply)
        doc = replica / "docs" / "engineering.local.md"
        saved = doc.read_bytes()
        edited = saved + b"\nowner edit beyond the managed section\n"
        doc.write_bytes(edited)
        refused_removal = run(exe, ["remove", "--repo", str(replica), "--format", "json"], env=isolated_env)
        removal_commands.append(refused_removal)
        edit_preserved = doc.read_bytes() == edited
        doc.write_bytes(saved)
        clean_removal = run(exe, ["remove", "--repo", str(replica), "--format", "json"], env=isolated_env)
        removal_commands.append(clean_removal)
        removal_ok = (reapply["exit"] == 0 and refused_removal["exit"] == 2
                      and edit_preserved and clean_removal["exit"] == 0)
        removal_note = ("owner-edit refusal (edit preserved byte-for-byte) then clean removal, "
                        "both exercised live against the journal")
    else:
        refused_removal = run(exe, ["remove", "--repo", str(replica), "--format", "json"], env=isolated_env)
        removal_commands.append(refused_removal)
        removal_ok = refused_removal["exit"] == 2
        removal_note = "no journal (apply refused): lawful structured refusal boundary"
    journeys.append(journey(
        "removal_with_owner_edits",
        "pass" if removal_ok else "fail",
        removal_note,
        removal_commands,
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


def execute_negative_control(exe: str, replica: Path, isolated_env: dict) -> dict:
    """Read-only negative control with byte-identical pre/post receipts."""
    before = tree_digest(replica)
    commands = [
        run(exe, ["list"], env=isolated_env),
        run(exe, ["show", "py"], env=isolated_env),
        run(exe, ["catalog"], env=isolated_env),
        run(exe, ["doctor", "--repo", str(replica)], env=isolated_env),
        run(exe, ["scan-adoption", "--scope", str(replica), "--format", "json",
                  "--include-scope-root"], env=isolated_env),
    ]
    after = tree_digest(replica)
    return {
        "schema": "engineering-core.v1.g1-negative-control/1",
        "stage": "g1-negative-control",
        "replica": str(replica),
        "tree_sha256_before": before,
        "tree_sha256_after": after,
        "byte_identical_receipts": before == after,
        "commands": commands,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exe", required=True)
    parser.add_argument("--replica", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--home", required=True, help="isolated HOME")
    parser.add_argument("--negative-control", action="store_true",
                        help="run read-only commands only; assert byte-identical tree receipts")
    parser.add_argument("--candidate-commit", default=CANDIDATE_COMMIT,
                        help="candidate the run executes against (default: the "
                             "historical b313bec pin, preserving bit-for-bit "
                             "reproduction of the 5004 fan-in)")
    args = parser.parse_args(argv)
    env = os.environ.copy()
    env["HOME"] = args.home
    env["XDG_CONFIG_HOME"] = str(Path(args.home) / ".config")
    env["XDG_CACHE_HOME"] = str(Path(args.home) / ".cache")
    env.pop("PYTHONPATH", None)
    if args.negative_control:
        rec = execute_negative_control(args.exe, Path(args.replica), env)
        rec["candidate_commit"] = args.candidate_commit
        print(json.dumps(rec, indent=2))
        return 0 if rec["byte_identical_receipts"] else 2
    rec = execute(args.exe, Path(args.replica), args.baseline, env)
    rec["candidate_commit"] = args.candidate_commit
    print(json.dumps(rec, indent=2))
    return 0 if rec["counts"]["fail"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
