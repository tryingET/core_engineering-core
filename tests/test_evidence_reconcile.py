# ---
# summary: "Exercises owner-evidence reconciliation across revisions, plans, advice, receipts, repository identity, artifact integrity, and bounded safe I/O."
# read_when:
#   - "Changing evidence reconciliation results, revision checks, receipt validation, repository mapping, artifact verification, or safe readers."
# ---

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.advisor import build_request
from engineering_core.catalog import load_catalog, load_catalog_history
from engineering_core.closed_loop import canonical_digest
from engineering_core.engineering_plan import compile_plan
from engineering_core.evidence_reconcile import reconcile_evidence
from engineering_core.safe_io import SafeInputError, read_bounded_bytes


class EvidenceReconcileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name) / "repo"
        (self.repo / "policy").mkdir(parents=True)
        (self.repo / "governance").mkdir()
        (self.repo / "pyproject.toml").write_text("[project]\nname='fixture'\nversion='1.0.0'\n")
        (self.repo / "policy/engineering-lane.json").write_text(json.dumps({"engineering_core": {"ref": "v0.8.0", "lane": "py", "disciplines": ["validation"]}}))
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=self.repo, check=True)
        self.target_revision = self.head()
        self.catalog = load_catalog(ROOT, prefer_repo=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def head(self) -> str:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip()

    def plan(self) -> dict:
        plan = compile_plan(self.repo, self.catalog)
        self.assertEqual(plan["status"], "complete")
        return plan

    def receipt(self, artifact: Path, plan: dict, *, recommendation_id: str = "planning-static-use", target: str | None = None) -> Path:
        value = {
            "schema": "engineering-evidence-receipt-v1",
            "receipt_id": "receipt-1",
            "authority": "owner-evidence-only; not CI, release, AK, or compliance authority",
            "provenance": {"owner": "fixture/repo", "owner_type": "repository", "produced_at": "2026-07-11T00:00:00Z", "source": "test"},
            "bindings": dict(plan["digests"]),
            "target": {"repository": "fixture/repo", "revision": target or self.target_revision, "recommendation_id": recommendation_id},
            "observations": [{"kind": "artifact", "outcome": "observed", "evidence_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "reference": artifact.relative_to(self.repo).as_posix()}],
            "state": "schema-valid",
            "reason": "Schema-valid owner artifact only.",
        }
        path = self.repo / "governance/receipt.json"
        path.write_text(json.dumps(value))
        return path

    def commit_artifacts(self) -> None:
        subprocess.run(["git", "add", "governance"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "artifacts"], cwd=self.repo, check=True)

    def reconcile(self, *receipts: Path) -> dict:
        return reconcile_evidence([("fixture/repo", self.repo)], list(receipts), repo_root=ROOT, prefer_repo=True)

    def test_v07_catalog_receipt_reconciles_without_projecting_v08_protocols(self):
        historical = load_catalog_history("0.7.0", ROOT, prefer_repo=True)
        self.assertIsNone(historical.protocols.work_packet)
        policy = json.loads((self.repo / "policy/engineering-lane.json").read_text()); policy["engineering_core"]["ref"] = "v0.7.0"
        (self.repo / "policy/engineering-lane.json").write_text(json.dumps(policy))
        subprocess.run(["git", "add", "policy"], cwd=self.repo, check=True); subprocess.run(["git", "commit", "-qm", "v07 policy"], cwd=self.repo, check=True)
        self.target_revision = self.head(); plan = compile_plan(self.repo, historical)
        artifact = self.repo / "governance/plan.json"; artifact.write_text(json.dumps(plan)); receipt = self.receipt(artifact, plan); self.commit_artifacts()
        output = self.reconcile(receipt)
        self.assertEqual("0.7.0", output["catalog"]["version"])
        self.assertEqual(1, output["summary"]["result_counts"]["matched"])

    def test_planning_artifact_matches_advanced_compatible_revision(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        self.commit_artifacts()
        output = self.reconcile(receipt)
        self.assertEqual(output["summary"]["result_counts"]["matched"], 1)
        self.assertEqual(output["records"][0]["capability"], "planning")
        self.assertEqual(output["records"][0]["owner_evidence_state"], "schema-valid")
        self.assertEqual(output["records"][0]["revision"]["relation"], "advanced-compatible")

    def test_advice_artifact_validates_against_fresh_request(self):
        plan = self.plan()
        request = build_request(self.repo, plan, set(self.catalog.ids("lanes")) | set(self.catalog.ids("disciplines")))
        evidence = request["evidence"][0]
        advice = {
            "schema": "engineering-advice-response-v1", "request_sha256": request["request_sha256"],
            "provenance": {"provider": "test", "model": "fixture", "model_version": "1", "adapter": "file", "adapter_version": "1", "prompt_id": request["prompt"]["id"], "prompt_version": request["prompt"]["version"]},
            "status": "advice", "summary": "Bounded fixture advice.",
            "recommendations": [{"id": "r1", "catalog_ids": ["py"], "recommendation": "Keep metadata explicit.", "confidence": 0.7, "unknowns": [], "counterevidence": [], "falsification": ["Python is not shipped."], "citations": [{"evidence_id": evidence["id"], "path": evidence["path"], "start": 0, "end": 1}], "competes_with": []}],
            "critiques": [], "patch_proposals": [],
        }
        artifact = self.repo / "governance/advice.json"
        artifact.write_text(json.dumps(advice))
        receipt = self.receipt(artifact, plan, recommendation_id="r1")
        self.commit_artifacts()
        output = self.reconcile(receipt)
        self.assertEqual(output["records"][0]["result"], "matched")
        self.assertEqual(output["records"][0]["capability"], "advisor")
        policy = json.loads((self.repo / "policy/engineering-lane.json").read_text())
        policy["engineering_core"]["disciplines"].append("testing")
        (self.repo / "policy/engineering-lane.json").write_text(json.dumps(policy))
        advice["critiques"] = [{"recommendation_id": "r1", "critique": "bad", "severity": "critical", "falsification": "none"}]
        artifact.write_text(json.dumps(advice))
        receipt_value = json.loads(receipt.read_text())
        receipt_value["observations"][0]["evidence_sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        receipt.write_text(json.dumps(receipt_value))
        subprocess.run(["git", "add", "policy", "governance"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "invalid stale advice"], cwd=self.repo, check=True)
        output = self.reconcile(receipt)
        self.assertEqual(output["records"][0]["result"], "mismatched")
        self.assertIn("advice-validation-failed", {item["code"] for item in output["records"][0]["findings"]})

    def test_policy_drift_is_stale_not_verified(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        self.commit_artifacts()
        policy = json.loads((self.repo / "policy/engineering-lane.json").read_text())
        policy["engineering_core"]["disciplines"].append("testing")
        (self.repo / "policy/engineering-lane.json").write_text(json.dumps(policy))
        subprocess.run(["git", "add", "policy"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "drift"], cwd=self.repo, check=True)
        output = self.reconcile(receipt)
        self.assertEqual(output["records"][0]["result"], "stale")
        self.assertEqual(output["records"][0]["owner_evidence_state"], "schema-valid")

    def test_nonexistent_and_mutable_revisions_are_mismatched(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        for target in ("0" * 40, "HEAD", "main", self.target_revision[:12]):
            with self.subTest(target=target):
                receipt = self.receipt(artifact, plan, target=target)
                output = self.reconcile(receipt)
                self.assertEqual(output["records"][0]["result"], "mismatched")

    def test_artifact_hash_and_plan_self_digest_mismatch(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        value = json.loads(artifact.read_text())
        value["status"] = "incomplete"
        artifact.write_text(json.dumps(value))
        output = self.reconcile(receipt)
        codes = {item["code"] for item in output["records"][0]["findings"]}
        self.assertIn("artifact-sha256-mismatch", codes)
        self.assertIn("plan-self-digest-mismatch", codes)

    def test_identity_and_owner_mismatch_fail_closed(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        value = json.loads(receipt.read_text())
        value["provenance"]["owner"] = "other/repo"
        receipt.write_text(json.dumps(value))
        output = self.reconcile(receipt)
        self.assertEqual(output["records"][0]["result"], "mismatched")

    def test_duplicate_receipt_key_reports_failure(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        output = self.reconcile(receipt, receipt)
        self.assertTrue(output["failures"])
        self.assertEqual(output["records"], [])

    def test_receipt_symlink_and_parent_symlink_are_rejected(self):
        plan = self.plan()
        artifact = self.repo / "governance/plan.json"
        artifact.write_text(json.dumps(plan))
        receipt = self.receipt(artifact, plan)
        link = self.repo / "governance/link.json"
        link.symlink_to(receipt)
        self.assertTrue(self.reconcile(link)["failures"])
        parent = Path(self.temporary.name) / "linked-parent"
        parent.symlink_to(self.repo / "governance", target_is_directory=True)
        self.assertTrue(self.reconcile(parent / "receipt.json")["failures"])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable")
    def test_fifo_rejected_without_blocking(self):
        fifo = self.repo / "governance/receipt.fifo"
        os.mkfifo(fifo)
        output = self.reconcile(fifo)
        self.assertTrue(output["failures"])

    def test_oversize_and_secret_receipts_are_rejected(self):
        large = self.repo / "governance/large.json"
        large.write_bytes(b"x" * (262_144 + 1))
        self.assertTrue(self.reconcile(large)["failures"])
        secret = self.repo / "governance/secret.json"
        secret.write_text('{"password":"hunter2"}')
        failure = self.reconcile(secret)["failures"][0]
        self.assertNotIn("hunter2", failure["message"])

    def test_safe_reader_rejects_special_and_changed_bounds(self):
        with self.assertRaises(SafeInputError):
            read_bounded_bytes(self.repo, max_bytes=100)
        path = self.repo / "bounded"
        path.write_bytes(b"1234")
        self.assertEqual(read_bounded_bytes(path, max_bytes=4), b"1234")
        with self.assertRaises(SafeInputError):
            read_bounded_bytes(path, max_bytes=3)

    def test_duplicate_json_members_and_unsafe_catalog_are_structured_failures(self):
        duplicate = self.repo / "governance/duplicate.json"
        duplicate.write_text('{"schema":"x","schema":"y"}')
        self.assertTrue(self.reconcile(duplicate)["failures"])
        catalog_root = Path(self.temporary.name) / "catalog-root"
        catalog_root.mkdir()
        (catalog_root / "catalog.json").symlink_to(ROOT / "catalog.json")
        output = reconcile_evidence([("fixture/repo", self.repo)], [duplicate], repo_root=catalog_root, prefer_repo=True)
        self.assertEqual(output["failures"][0]["code"], "catalog-invalid")

    def test_no_receipts_and_duplicate_repository_mapping_fail(self):
        output = reconcile_evidence([("fixture/repo", self.repo)], [], repo_root=ROOT, prefer_repo=True)
        self.assertTrue(output["failures"])
        output = reconcile_evidence([("fixture/repo", self.repo), ("fixture/repo", self.repo)], [self.repo / "missing"], repo_root=ROOT, prefer_repo=True)
        self.assertTrue(any(item["code"] in {"repository-id-duplicate", "repository-path-duplicate"} for item in output["failures"]))
        alias = self.repo / ".." / self.repo.name
        output = reconcile_evidence([("fixture/repo", self.repo), ("fixture/alias", alias)], [self.repo / "missing"], repo_root=ROOT, prefer_repo=True)
        self.assertTrue(any(item["code"] == "repository-path-duplicate" for item in output["failures"]))
        symlink_alias = Path(self.temporary.name) / "repo-link"
        symlink_alias.symlink_to(self.repo, target_is_directory=True)
        output = reconcile_evidence([("fixture/repo", self.repo), ("fixture/symlink", symlink_alias)], [self.repo / "missing"], repo_root=ROOT, prefer_repo=True)
        self.assertTrue(any(item["code"] == "repository-path-duplicate" for item in output["failures"]))
        output = reconcile_evidence([("fixture/subroot", self.repo / "governance")], [self.repo / "missing"], repo_root=ROOT, prefer_repo=True)
        self.assertTrue(any(item["code"] == "repository-subroot-rejected" for item in output["failures"]))


if __name__ == "__main__":
    unittest.main()
