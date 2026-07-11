#!/usr/bin/env python3
# summary: "Runs the deterministic end-to-end fixture for receipts, dispositions, calibration, pattern synthesis, and unapplied doctrine proposals."
# read_when:
#   - "Changing closed-loop evidence schemas, advisory bindings, calibration, pattern synthesis, or doctrine proposal behavior."

"""Reproducible, read-only Wave 4 closed-loop dogfood."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.advisor import AdviceError, build_request, validate_response
from engineering_core.catalog import load_catalog
from engineering_core.closed_loop import (
    DISPOSITION_SCHEMA, RECEIPT_SCHEMA, ClosedLoopError, calibration,
    canonical_digest, doctrine_proposal, load_record, summarize_receipts,
    synthesize_patterns, validate_disposition, validate_receipt,
)
from engineering_core.engineering_plan import compile_plan

OWNER = {"owner": "dogfood-owner", "owner_type": "repository", "produced_at": "2026-07-11T00:00:00Z", "source": "bounded dogfood fixture"}
DECISIONS = (("accepted", "adopted"), ("deferred", "needs-evidence"), ("rejected", "conflicting-evidence"), ("abstained", "insufficient-evidence"))
STATES = ("evidence-verified", "schema-valid", "stale", "mismatched")


def expect_rejected(label, function, failures):
    try:
        function()
    except (AdviceError, ClosedLoopError):
        failures.append(label)
    else:
        raise AssertionError(f"negative probe did not fail closed: {label}")


def main() -> None:
    catalog = load_catalog(ROOT, prefer_repo=True)
    ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
    rejected = []
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        repos = []
        sentinel = base / "consumer-command-executed"
        for index in (1, 2):
            repo = base / f"repo-{index}"
            (repo / "policy").mkdir(parents=True)
            (repo / "pyproject.toml").write_text(f"[project]\nname='dogfood-{index}'\n", encoding="utf-8")
            (repo / "policy" / "engineering-lane.json").write_text(json.dumps({
                "engineering_core": {"lanes": ["py"], "disciplines": ["validation"]},
                "commands": {"test": f"touch {sentinel}"},
            }), encoding="utf-8")
            repos.append(repo)
        plans = [compile_plan(repo, catalog) for repo in repos]
        requests = [build_request(repo, plan, ids) for repo, plan in zip(repos, plans)]
        recommendations = [{
            "id": f"r{i}", "catalog_ids": ["validation"], "recommendation": f"Owner review recommendation {i}.",
            "confidence": 0.9 - i / 10, "unknowns": [], "counterevidence": [],
            "falsification": ["Owner evidence contradicts the recommendation."], "citations": [], "competes_with": [],
        } for i in range(1, 5)]
        advice = {
            "schema": "engineering-advice-response-v1", "request_sha256": requests[0]["request_sha256"],
            "provenance": {"provider": "fixture", "model": "deterministic", "model_version": "1", "adapter": "none", "adapter_version": "1", "prompt_id": "engineering-core-bounded-advisor", "prompt_version": "1"},
            "status": "advice", "summary": "Bounded deterministic dogfood advice.",
            "recommendations": recommendations, "critiques": [],
            "patch_proposals": [{"path": "docs/engineering.local.md", "unified_diff": "--- a/docs/engineering.local.md\n+++ b/docs/engineering.local.md\n@@ -0,0 +1 @@\n+proposal only\n", "rationale": "Owner review only.", "recommendation_id": "r1"}],
        }
        validate_response(requests[0], advice)
        advice_digest = canonical_digest(advice)
        plan = plans[0]
        dispositions = []
        receipts = []
        for index, ((decision, reason), state) in enumerate(zip(DECISIONS, STATES), 1):
            disposition = {
                "schema": DISPOSITION_SCHEMA, "disposition_id": f"d{index}",
                "authority": "owner disposition; advisory inputs do not self-authorize", "provenance": OWNER,
                "bindings": {"request_sha256": requests[0]["request_sha256"], "advice_sha256": advice_digest, **plan["digests"]},
                "target": {"repository": "dogfood/repo", "revision": "fixture-revision"},
                "recommendation_id": f"r{index}", "decision": decision, "reason_code": reason,
                "rationale": f"Owner recorded {decision} for dogfood.",
            }
            validate_disposition(disposition, advice)
            dispositions.append(disposition)
            observations = [{"kind": "artifact", "outcome": "passed" if index == 1 else "failed", "evidence_sha256": "a" * 64, "reference": f"owner evidence {index}"}]
            receipt = {
                "schema": RECEIPT_SCHEMA, "receipt_id": f"e{index}",
                "authority": "owner-evidence-only; not CI, release, AK, or compliance authority", "provenance": OWNER,
                "bindings": dict(plan["digests"]),
                "target": {"repository": "dogfood/repo", "revision": "fixture-revision", "recommendation_id": f"r{index}"},
                "observations": observations, "state": state, "reason": f"Owner-recorded {state} outcome.",
            }
            validate_receipt(receipt)
            receipts.append(receipt)
        calibration_result = calibration(advice, dispositions, receipts)
        # The second plan participates in recurring-selection synthesis; records remain explicitly bound to plan one.
        patterns = synthesize_patterns(plans, [advice], dispositions, receipts)
        proposal = doctrine_proposal(patterns)

        bad_id = copy.deepcopy(dispositions[0]); bad_id["recommendation_id"] = "unknown-id"
        expect_rejected("unknown-id", lambda: validate_disposition(bad_id, advice), rejected)
        bad_binding = copy.deepcopy(dispositions[0]); bad_binding["bindings"]["plan_sha256"] = "f" * 64
        expect_rejected("mismatched-provenance", lambda: synthesize_patterns(plans, [advice], [bad_binding], []), rejected)
        bad_path = copy.deepcopy(advice); bad_path["patch_proposals"][0]["path"] = "../hallucinated"
        expect_rejected("hallucinated-path", lambda: validate_response(requests[0], bad_path), rejected)
        malformed = base / "malformed.json"; malformed.write_text("{bad", encoding="utf-8")
        expect_rejected("malformed", lambda: load_record(malformed), rejected)
        secret = base / "secret.json"; secret.write_text('{"password":"hunter2"}', encoding="utf-8")
        expect_rejected("secret-bearing", lambda: load_record(secret), rejected)

        assert not sentinel.exists(), "consumer command executed"
        assert proposal["status"] == "unapplied" and proposal["mutations_performed"] == []
        assert advice["patch_proposals"] and not (repos[0] / "docs" / "engineering.local.md").exists()
        output = {
            "schema": "engineering-closed-loop-dogfood-v1", "status": "passed",
            "flow": ["plan", "advisor-validation", "dispositions", "receipts", "calibration", "multi-input-patterns", "doctrine-proposal"],
            "plans": len(plans), "dispositions": sorted(x[0] for x in DECISIONS),
            "receipt_summary": summarize_receipts(receipts)["counts"],
            "calibration": calibration_result["metrics"], "patterns": len(patterns["patterns"]),
            "proposal_status": proposal["status"], "patches_applied": False,
            "consumer_commands_executed": False, "fail_closed_probes": sorted(rejected),
            "authority": "owner fixtures only; no CI, release, AK, compliance, consumer, or doctrine authority promoted",
        }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
