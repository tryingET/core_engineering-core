#!/usr/bin/env python3
"""Deterministic owner-use packet/bundle/verification dogfood with adversarial probes."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.catalog import load_catalog
from engineering_core.closed_loop import canonical_digest
from engineering_core.work_bundle import WorkBundleError, finalize_work
from engineering_core.work_packet import WorkPacketError, prepare_work
from engineering_core.work_verify import verify_work

ROOT = Path("/tmp/engineering-core-owner-use-dogfood")
REPO_ID = "dogfood/owner-use"


def git(*args: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": "2026-07-12T00:00:00Z", "GIT_COMMITTER_DATE": "2026-07-12T00:00:00Z"}
    subprocess.run(["git", "-C", str(ROOT), *args], check=True, env=env, stdout=subprocess.DEVNULL)


def main() -> None:
    shutil.rmtree(ROOT, ignore_errors=True); ROOT.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(ROOT)], check=True)
    git("config", "user.email", "dogfood@example.invalid"); git("config", "user.name", "Dogfood")
    (ROOT / "pyproject.toml").write_text('[project]\nname="owner-use-dogfood"\nversion="0.1.0"\n')
    (ROOT / "focus.py").write_text('SENTINEL_CONSUMER_COMMAND = "must-never-run"\n')
    git("add", "."); git("commit", "-qm", "deterministic fixture")
    context = {
        "schema": "engineering-work-context-v1", "authority": "owner-supplied task context; repository and task authorities remain external",
        "repository_id": REPO_ID, "work": {"id": "dogfood-1", "title": "Owner-use evidence bridge", "objective": "Produce a bounded plan and externally reviewed evidence bundle."}, "mode": "advisor-ready",
        "scope": {"focus_paths": ["focus.py"], "constraints": ["Never execute the sentinel command."], "validation": ["Deterministic schema validation only."]},
        "provenance": {"owner": REPO_ID, "owner_type": "repository", "produced_at": "2026-07-12T00:00:00Z", "source": "deterministic dogfood"},
    }
    catalog = load_catalog(); packet = prepare_work(ROOT, REPO_ID, context, catalog); request = packet["advice_request"]
    catalog_id = packet["plan"]["selections"][0]["id"]
    advice = {
        "schema": "engineering-advice-response-v1", "request_sha256": request["request_sha256"],
        "provenance": {"provider": "external-fixture", "model": "none", "model_version": "0", "adapter": "dogfood", "adapter_version": "1", "prompt_id": request["prompt"]["id"], "prompt_version": request["prompt"]["version"]},
        "status": "advice", "summary": "Review-only deterministic fixture advice.",
        "recommendations": [{"id": "r1", "catalog_ids": [catalog_id], "recommendation": "Keep the owner validation boundary explicit.", "confidence": 0.5, "unknowns": ["No consumer command was executed."], "counterevidence": [], "falsification": ["A consumer command execution would invalidate the claim."], "citations": [], "competes_with": []}],
        "critiques": [], "patch_proposals": [],
    }
    b = packet["bindings"]
    disposition = {
        "schema": "engineering-recommendation-disposition-v1", "disposition_id": "d1", "authority": "owner disposition; advisory inputs do not self-authorize",
        "provenance": {"owner": REPO_ID, "owner_type": "repository", "produced_at": "2026-07-12T00:01:00Z", "source": "dogfood owner review"},
        "bindings": {"request_sha256": b["request_sha256"], "advice_sha256": canonical_digest(advice), "plan_sha256": b["plan_sha256"], "catalog_sha256": b["catalog_sha256"], "repository_facts_sha256": b["repository_facts_sha256"]},
        "target": {"repository": REPO_ID, "revision": packet["repository"]["revision"]}, "recommendation_id": "r1", "decision": "deferred", "reason_code": "needs-evidence", "rationale": "No runtime evidence was produced by preparation.",
    }
    receipt = {
        "schema": "engineering-evidence-receipt-v1", "receipt_id": "receipt-1", "authority": "owner-evidence-only; not CI, release, AK, or compliance authority",
        "provenance": {"owner": REPO_ID, "owner_type": "repository", "produced_at": "2026-07-12T00:02:00Z", "source": "dogfood owner artifact"},
        "bindings": {key: b[key] for key in ("plan_sha256", "catalog_sha256", "repository_facts_sha256")},
        "target": {"repository": REPO_ID, "revision": packet["repository"]["revision"], "recommendation_id": "r1"},
        "observations": [{"kind": "artifact", "outcome": "observed", "evidence_sha256": "a" * 64, "reference": "owner/result.json"}], "state": "schema-valid", "reason": "Schema-valid owner claim only.",
    }
    canon = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    bundle = finalize_work(packet, advice, [disposition], [receipt], {"packet": canon(packet), "advice": canon(advice), "dispositions": [canon(disposition)], "receipts": [canon(receipt)]})
    matched = verify_work(ROOT, REPO_ID, bundle, catalog)
    (ROOT / "focus.py").write_text('SENTINEL_CONSUMER_COMMAND = "still-must-never-run"\n')
    stale = verify_work(ROOT, REPO_ID, bundle, catalog)
    rejected = []
    bad = json.loads(json.dumps(disposition)); bad["provenance"]["owner"] = "other/repo"
    try: finalize_work(packet, advice, [bad], [], {"packet": canon(packet), "advice": canon(advice), "dispositions": [canon(bad)], "receipts": []})
    except WorkBundleError: rejected.append("cross-repository-disposition")
    try: prepare_work(ROOT, REPO_ID, {**context, "scope": {**context["scope"], "focus_paths": ["../escape"]}}, catalog)
    except WorkPacketError: rejected.append("path-traversal")
    output = {
        "schema": "engineering-owner-use-dogfood-v1", "packet_sha256": packet["packet_sha256"], "bundle_sha256": bundle["bundle_sha256"],
        "matched_result": matched["result"], "stale_result": stale["result"], "owner_decision": bundle["records"][0]["disposition"]["decision"],
        "owner_state": bundle["records"][0]["owner_receipts"][0]["state"], "rejected": sorted(rejected),
        "consumer_commands_executed": False, "external_models_invoked": False, "patches_applied": False, "authority_promotions": [],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    shutil.rmtree(ROOT, ignore_errors=True)


if __name__ == "__main__": main()
