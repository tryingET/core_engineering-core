#!/usr/bin/env python3
"""Deterministic, read-only owner-evidence reconciliation dogfood."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.catalog import load_catalog
from engineering_core.engineering_plan import compile_plan
from engineering_core.evidence_reconcile import reconcile_evidence

GIT_ENV = {**os.environ, "GIT_AUTHOR_DATE": "2026-07-11T00:00:00Z", "GIT_COMMITTER_DATE": "2026-07-11T00:00:00Z"}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, env=GIT_ENV, text=True).strip()


def main() -> None:
    catalog = load_catalog(ROOT, prefer_repo=True)
    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary) / "repo"
        (repo / "policy").mkdir(parents=True)
        (repo / "governance").mkdir()
        (repo / "pyproject.toml").write_text("[project]\nname='dogfood'\nversion='1.0.0'\n")
        (repo / "policy/engineering-lane.json").write_text(json.dumps({"engineering_core": {"lane": "py", "disciplines": ["validation"]}}))
        git(repo, "init", "-q", "-b", "main")
        git(repo, "config", "user.email", "dogfood@example.com")
        git(repo, "config", "user.name", "Dogfood")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "initial")
        revision = git(repo, "rev-parse", "HEAD")
        plan = compile_plan(repo, catalog)
        artifact = repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan, sort_keys=True, separators=(",", ":")))
        receipt = {
            "schema": "engineering-evidence-receipt-v1",
            "receipt_id": "dogfood-receipt",
            "authority": "owner-evidence-only; not CI, release, AK, or compliance authority",
            "provenance": {"owner": "dogfood/repo", "owner_type": "repository", "produced_at": "2026-07-11T00:00:00Z", "source": "deterministic dogfood"},
            "bindings": dict(plan["digests"]),
            "target": {"repository": "dogfood/repo", "revision": revision, "recommendation_id": "planning-static-use"},
            "observations": [{"kind": "artifact", "outcome": "observed", "evidence_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "reference": "governance/plan.json"}],
            "state": "schema-valid",
            "reason": "Schema-valid planning artifact only.",
        }
        receipt_path = repo / "governance/receipt.json"
        receipt_path.write_text(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
        git(repo, "add", "governance")
        git(repo, "commit", "-q", "-m", "evidence")
        matched = reconcile_evidence([("dogfood/repo", repo)], [receipt_path], repo_root=ROOT, prefer_repo=True)
        policy = json.loads((repo / "policy/engineering-lane.json").read_text())
        policy["engineering_core"]["disciplines"].append("testing")
        (repo / "policy/engineering-lane.json").write_text(json.dumps(policy))
        git(repo, "add", "policy")
        git(repo, "commit", "-q", "-m", "drift")
        stale = reconcile_evidence([("dogfood/repo", repo)], [receipt_path], repo_root=ROOT, prefer_repo=True)
        bad = json.loads(receipt_path.read_text())
        bad["target"]["revision"] = "0" * 40
        bad_path = repo / "governance/bad.json"
        bad_path.write_text(json.dumps(bad))
        mismatched = reconcile_evidence([("dogfood/repo", repo)], [bad_path], repo_root=ROOT, prefer_repo=True)
        link = repo / "governance/link.json"
        link.symlink_to(receipt_path)
        unsafe = reconcile_evidence([("dogfood/repo", repo)], [link], repo_root=ROOT, prefer_repo=True)
        assert matched["summary"]["result_counts"]["matched"] == 1
        assert matched["records"][0]["owner_evidence_state"] == "schema-valid"
        assert stale["summary"]["result_counts"]["stale"] == 1
        assert mismatched["summary"]["result_counts"]["mismatched"] == 1
        assert unsafe["failures"]
        output = {
            "schema": "engineering-evidence-reconcile-dogfood-v1",
            "status": "passed",
            "matched": 1,
            "stale": 1,
            "mismatched": 1,
            "unsafe_inputs_rejected": 1,
            "owner_state_preserved": "schema-valid",
            "consumer_commands_executed": False,
            "external_models_invoked": False,
            "mutations_performed": [],
        }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
