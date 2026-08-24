#!/usr/bin/env python3
"""G4-B non-mutating verification (engineering-core v1.0).

Replays the frozen G4 transition suite and checks the candidate inclusion
map plus revise lineage. Does not import-write the G4-A harness and does
not mutate the candidate.

Modes:
  template   Emit the verification schema.
  validate   Validate one G4-B verification record.

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

SCHEMA = "engineering-core.v1.g4b/1"
CANDIDATE_COMMIT = "b313becf7f1bf5261843d7b29c939b0bc5072ef1"
CANDIDATE_BRANCH = "proof/v1-candidate-2"
SUITE_CASES = [
    "proposal", "pilot_selection", "promotion", "revision_split", "rejection",
    "deprecation", "retirement", "expiry", "rollback", "invalid_transition",
    "stale_evidence", "unauthorized_promotion",
]
LINEAGE = [
    {
        "cycle_id": "cycle-holdingco-pin-drift",
        "disposition": "revised",
        "cycle_digest": "6e188a012d0a661fa4536506e259974fc25bcc6e52b5e8fc670d1810d1967ff7",
        "path": "/home/tryinget/ai-society/holdingco/fcos-control-board/docs/v1-proof/g4a-cycle.json",
    },
    {
        "cycle_id": "cycle-teachingco-minimal-validation",
        "disposition": "revised",
        "cycle_digest": "0ece9f07cb4eecf43760c981231ee0acc5785b3326ae2bba817707e85794f151",
        "path": "/home/tryinget/ai-society/teachingco/mathe/docs/v1-proof/g4a-cycle.json",
    },
    {
        "cycle_id": "cycle-softwareco-package-scopes",
        "disposition": "revised",
        "cycle_digest": "f3feef7f66d09877708f4a783d06a1977b6814173bf690ea3998239cb7293473",
        "path": "/home/tryinget/ai-society/softwareco/owned/pi-extensions/docs/v1-proof/g4a-cycle.json",
    },
]
ILLEGAL_CASES = {"invalid_transition", "unauthorized_promotion"}
CASE_TRANSITIONS = {
    "proposal": ("proposal", "pilot_selection"),
    "pilot_selection": ("pilot_selection", "participant_disposition"),
    "promotion": ("content_owner_decision", "final_state"),
    "revision_split": ("content_owner_decision", "final_state"),
    "rejection": ("content_owner_decision", "final_state"),
    "deprecation": ("content_owner_decision", "final_state"),
    "retirement": ("content_owner_decision", "final_state"),
    "expiry": ("content_owner_decision", "final_state"),
    "rollback": ("pilot_selection", "rollback_restored"),
    "invalid_transition": ("proposal", "final_state"),
    "stale_evidence": ("participant_disposition", "content_owner_decision"),
    "unauthorized_promotion": ("proposal", "final_state"),
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


def load_ge():
    path = Path(__file__).resolve().parent / "governed_evolution.py"
    spec = importlib.util.spec_from_file_location("governed_evolution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_read(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def build_template() -> dict:
    return {
        "schema": SCHEMA,
        "stage": "g4b-verification-template",
        "mutating": False,
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_branch": CANDIDATE_BRANCH,
        "suite_cases": list(SUITE_CASES),
        "accepted_g4_content_must_be_empty_until_promotion": True,
    }


def template_digest() -> str:
    body = dict(build_template())
    body.pop("schema", None)
    return digest_of(body)


def fixture_for(case: str, ge) -> dict:
    frm, to = CASE_TRANSITIONS[case]
    illegal = case in ILLEGAL_CASES
    rec = {
        "schema": ge.SCHEMA,
        "stage": "g4-transition-fixture",
        "suite_case": case,
        "from_state": frm,
        "to_state": to,
        "authorized_by": "engineering_core_content_owner",
        "evidence_freshness": "stale" if case == "stale_evidence" else "fresh",
        "expected_result": "rejected" if illegal else "accepted",
        "lineage": {"history_preserved": True},
        "decision_present": True,
    }
    if case == "stale_evidence":
        rec["re_review"] = True
    return rec


def replay_suite(ge) -> list:
    results = []
    for case in SUITE_CASES:
        out = ge.validate_transition(fixture_for(case, ge))
        _require(out["status"] == "pass", "suite_case_failed",
                 f"suite case {case} did not pass")
        expected = "rejected" if case in ILLEGAL_CASES else "accepted"
        _require(out["result"] == expected, "suite_result_mismatch",
                 f"suite case {case} expected {expected} got {out['result']}")
        results.append({"suite_case": case, "result": out["result"],
                        "digest": out["transition_digest"]})
    return results


def validate_record(record: dict, repo_root: Path) -> dict:
    ge = load_ge()
    for field in ("schema", "stage", "template_digest", "candidate_commit",
                  "candidate_branch", "accepted_g4_content", "revised_lineage",
                  "suite_replay", "tag_absent", "main_untouched"):
        _require(isinstance(record, dict) and field in record, "missing_field",
                 f"verification missing: {field}")
    _require(record["schema"] == SCHEMA, "schema_mismatch", f"expected {SCHEMA}")
    _require(record["stage"] == "g4b-verification", "stage_mismatch",
             "expected stage g4b-verification")
    _require(record["template_digest"] == template_digest(), "template_digest_mismatch",
             "template digest drift")
    _require(record["candidate_commit"] == CANDIDATE_COMMIT, "wrong_candidate",
             "candidate commit does not match frozen G0-B SHA")
    _require(record["candidate_branch"] == CANDIDATE_BRANCH, "wrong_branch",
             "candidate branch must be proof/v1-candidate-2")
    _require(record["accepted_g4_content"] == [], "accepted_content_not_empty",
             "G4-B inclusion map must be empty until a promotion lands")
    _require(record["tag_absent"] is True, "tag_present", "v1.0.0 must remain untagged")
    _require(record["main_untouched"] is True, "main_mutated",
             "G4-B must not treat main as the candidate")

    tip = git_read(repo_root, "rev-parse", CANDIDATE_BRANCH)
    _require(tip.returncode == 0 and tip.stdout.strip() == CANDIDATE_COMMIT,
             "candidate_missing", "candidate branch tip is not the frozen SHA")
    main = git_read(repo_root, "rev-parse", "main")
    _require(main.returncode == 0 and main.stdout.strip() != CANDIDATE_COMMIT,
             "candidate_is_main", "candidate SHA must not be main")
    tag = git_read(repo_root, "tag", "-l", "v1.0.0")
    _require(tag.stdout.strip() == "", "tag_present", "v1.0.0 tag exists")

    lineage = record["revised_lineage"]
    _require(isinstance(lineage, list) and len(lineage) == 3, "lineage_count",
             "expected exactly three revised lineages")
    expected = {item["cycle_id"]: item for item in LINEAGE}
    for item in lineage:
        exp = expected.get(item.get("cycle_id"))
        _require(exp is not None, "unknown_cycle", f"unknown cycle {item.get('cycle_id')}")
        _require(item.get("disposition") == "revised" and item.get("immutable") is True,
                 "invalid_lineage", f"{item.get('cycle_id')} is not immutable revised")
        _require(item.get("cycle_digest") == exp["cycle_digest"], "digest_mismatch",
                 f"{item['cycle_id']} digest drifted")
        path = Path(exp["path"])
        _require(path.is_file(), "missing_file", f"cycle file missing: {path}")
        live = ge.validate_cycle(json.loads(path.read_text(encoding="utf-8")))
        _require(live["cycle_digest"] == exp["cycle_digest"], "digest_mismatch",
                 f"live cycle digest drifted for {item['cycle_id']}")

    replayed = replay_suite(ge)
    recorded = record["suite_replay"]
    _require(isinstance(recorded, list) and len(recorded) == 12, "suite_incomplete",
             "suite replay must contain all 12 cases")
    rec_map = {r["suite_case"]: r for r in recorded}
    for live in replayed:
        rec = rec_map.get(live["suite_case"])
        _require(rec is not None, "suite_incomplete", f"missing case {live['suite_case']}")
        _require(rec.get("result") == live["result"], "suite_result_mismatch",
                 f"{live['suite_case']} result drifted")
        _require(rec.get("digest") == live["digest"], "suite_digest_mismatch",
                 f"{live['suite_case']} digest drifted or omitted")

    return {
        "schema": SCHEMA,
        "stage": "g4b-verification-validation",
        "status": "pass",
        "candidate_commit": CANDIDATE_COMMIT,
        "accepted_g4_content_count": 0,
        "revised_lineage_count": 3,
        "suite_cases": 12,
        "verification_digest": digest_of(record),
        "template_digest": template_digest(),
    }


def emit_record(repo_root: Path) -> dict:
    ge = load_ge()
    return {
        "schema": SCHEMA,
        "stage": "g4b-verification",
        "template_digest": template_digest(),
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_branch": CANDIDATE_BRANCH,
        "mutating": False,
        "accepted_g4_content": [],
        "revised_lineage": [
            {"cycle_id": i["cycle_id"], "disposition": "revised",
             "immutable": True, "cycle_digest": i["cycle_digest"]}
            for i in LINEAGE
        ],
        "suite_replay": replay_suite(ge),
        "tag_absent": True,
        "main_untouched": True,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["template", "emit", "validate"])
    parser.add_argument("path", nargs="?", help="verification JSON ('-' for stdin)")
    parser.add_argument("--repo-root", default=".", help="engineering-core repo root")
    args = parser.parse_args(argv)
    root = Path(args.repo_root).resolve()
    try:
        if args.mode == "template":
            print(canonical({**build_template(), "template_digest": template_digest()}))
            return 0
        if args.mode == "emit":
            print(canonical(emit_record(root)))
            return 0
        if not args.path:
            print(json.dumps({"status": "fail", "code": "missing_input"}), file=sys.stderr)
            return 3
        raw = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
        payload = json.loads(raw)
        print(canonical(validate_record(payload, root)))
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
