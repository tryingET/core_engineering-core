import copy
import subprocess
import tempfile
import unittest
from pathlib import Path

from engineering_core.catalog import load_catalog
from engineering_core.closed_loop import canonical_digest
from engineering_core.work_bundle import WorkBundleError, finalize_work, validate_bundle
from engineering_core.work_packet import prepare_work
from engineering_core.work_render import build_summary, render_markdown
from engineering_core.work_verify import validate_verification, verify_work


class WorkBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.repo = Path(self.temp.name) / "repo"; self.repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        (self.repo / "pyproject.toml").write_text('[project]\nname="fixture"\nversion="0.1.0"\n')
        (self.repo / "focus.txt").write_text("bounded work\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True); subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "fixture"], check=True)
        context = {
            "schema": "engineering-work-context-v1", "authority": "owner-supplied task context; repository and task authorities remain external",
            "repository_id": "owned/fixture", "work": {"id": "task-1", "title": "Fixture", "objective": "Review bounded work."}, "mode": "advisor-ready",
            "scope": {"focus_paths": ["focus.txt"], "constraints": ["No patch application."], "validation": ["Owner review."]},
            "provenance": {"owner": "owned/fixture", "owner_type": "repository", "produced_at": "2026-07-12T00:00:00Z", "source": "test"},
        }
        self.packet = prepare_work(self.repo, "owned/fixture", context, load_catalog())
        request = self.packet["advice_request"]
        catalog_id = self.packet["plan"]["selections"][0]["id"]
        self.advice = {
            "schema": "engineering-advice-response-v1", "request_sha256": request["request_sha256"],
            "provenance": {"provider": "external-test", "model": "fixture", "model_version": "1", "adapter": "manual", "adapter_version": "1", "prompt_id": request["prompt"]["id"], "prompt_version": request["prompt"]["version"]},
            "status": "advice", "summary": "One bounded recommendation.",
            "recommendations": [{"id": "r1", "catalog_ids": [catalog_id], "recommendation": "Keep validation bounded to the owner scope.", "confidence": 0.7, "unknowns": ["Runtime outcome is not observed."], "counterevidence": [], "falsification": ["Owner validation rejects the approach."], "citations": [], "competes_with": []}],
            "critiques": [], "patch_proposals": [],
        }
        b = self.packet["bindings"]; advice_sha = canonical_digest(self.advice)
        self.disposition = {
            "schema": "engineering-recommendation-disposition-v1", "disposition_id": "d1", "authority": "owner disposition; advisory inputs do not self-authorize",
            "provenance": {"owner": "owned/fixture", "owner_type": "repository", "produced_at": "2026-07-12T00:01:00Z", "source": "owner review"},
            "bindings": {"request_sha256": b["request_sha256"], "advice_sha256": advice_sha, "plan_sha256": b["plan_sha256"], "catalog_sha256": b["catalog_sha256"], "repository_facts_sha256": b["repository_facts_sha256"]},
            "target": {"repository": "owned/fixture", "revision": self.packet["repository"]["revision"]}, "recommendation_id": "r1", "decision": "deferred", "reason_code": "needs-evidence", "rationale": "No execution evidence exists yet.",
        }
        self.receipt = {
            "schema": "engineering-evidence-receipt-v1", "receipt_id": "receipt-1", "authority": "owner-evidence-only; not CI, release, AK, or compliance authority",
            "provenance": {"owner": "owned/fixture", "owner_type": "repository", "produced_at": "2026-07-12T00:02:00Z", "source": "owner artifact"},
            "bindings": {"plan_sha256": b["plan_sha256"], "catalog_sha256": b["catalog_sha256"], "repository_facts_sha256": b["repository_facts_sha256"]},
            "target": {"repository": "owned/fixture", "revision": self.packet["repository"]["revision"], "recommendation_id": "r1"},
            "observations": [{"kind": "artifact", "outcome": "observed", "evidence_sha256": "b" * 64, "reference": "owner/result.json"}], "state": "schema-valid", "reason": "Owner supplied schema-valid evidence only.",
        }
        self.content = {"packet": "1" * 64, "advice": "2" * 64, "dispositions": ["3" * 64], "receipts": ["4" * 64]}

    def tearDown(self): self.temp.cleanup()

    def test_finalize_preserves_separate_owner_claims(self):
        bundle = finalize_work(self.packet, self.advice, [self.disposition], [self.receipt], self.content)
        self.assertEqual(bundle, validate_bundle(bundle))
        self.assertEqual("deferred", bundle["records"][0]["disposition"]["decision"])
        self.assertEqual("schema-valid", bundle["records"][0]["owner_receipts"][0]["state"])
        self.assertNotIn("verified", bundle["summary"])
        self.assertEqual([], bundle["effects"]["authority_promotions"])

    def test_advice_without_disposition_exposes_pending_owner_review(self):
        bundle = finalize_work(self.packet, self.advice, [], [], {"packet": "1"*64, "advice": "2"*64, "dispositions": [], "receipts": []})
        self.assertEqual(1, len(bundle["records"]))
        self.assertEqual("r1", bundle["records"][0]["subject"]["recommendation_id"])
        self.assertEqual("awaiting-owner-review", bundle["records"][0]["posture"])
        self.assertIsNone(bundle["records"][0]["disposition"])

    def test_owner_summary_makes_pending_recommendation_actionable(self):
        bundle = finalize_work(self.packet, self.advice, [], [], {"packet": "1"*64, "advice": "2"*64, "dispositions": [], "receipts": []})
        summary = build_summary(bundle)
        self.assertEqual("pending-owner-review", summary["recommendations"][0]["decision"])
        self.assertIn("Owner reviews", summary["next_action"])
        markdown = render_markdown(summary)
        self.assertIn("Keep validation bounded", markdown)
        self.assertIn("focus.txt", markdown)

    def test_verification_validation_rejects_incoherent_nonhex_and_oversized_inputs(self):
        bundle = finalize_work(self.packet, self.advice, [], [], {"packet": "1"*64, "advice": "2"*64, "dispositions": [], "receipts": []})
        verification = verify_work(self.repo, "owned/fixture", bundle, load_catalog())
        bad = copy.deepcopy(verification); bad["revision_relation"] = "mismatched"
        with self.assertRaisesRegex(WorkBundleError, "incoherent"): validate_verification(bad)
        bad = copy.deepcopy(verification); bad["bundle_sha256"] = "z"*64
        with self.assertRaisesRegex(WorkBundleError, "digest"): validate_verification(bad)
        bad = copy.deepcopy(verification); bad["findings"] = [{"code":"x","severity":"warning","message":"x"*1_100_000}]; bad["result"]="stale"; bad["scope_match"]=False
        with self.assertRaisesRegex(WorkBundleError, "byte budget"): validate_verification(bad)

    def test_malformed_verification_summary_input_is_rejected(self):
        bundle = finalize_work(self.packet, self.advice, [], [], {"packet": "1"*64, "advice": "2"*64, "dispositions": [], "receipts": []})
        malformed = {"schema": "engineering-work-verification-v1", "result": "matched", "bundle_sha256": bundle["bundle_sha256"]}
        with self.assertRaisesRegex(WorkBundleError, "verification schema"):
            build_summary(bundle, malformed)

    def test_exact_advice_digest_is_required(self):
        disposition = copy.deepcopy(self.disposition); disposition["bindings"]["advice_sha256"] = "0" * 64
        with self.assertRaisesRegex(WorkBundleError, "advice binding mismatch"):
            finalize_work(self.packet, self.advice, [disposition], [], {**self.content, "receipts": []})

    def test_owner_and_cross_repo_mixups_are_rejected(self):
        disposition = copy.deepcopy(self.disposition); disposition["provenance"]["owner"] = "owned/other"
        with self.assertRaisesRegex(WorkBundleError, "owner or target"):
            finalize_work(self.packet, self.advice, [disposition], [], {**self.content, "receipts": []})
        receipt = copy.deepcopy(self.receipt); receipt["target"]["repository"] = "owned/other"
        with self.assertRaisesRegex(WorkBundleError, "receipt owner or target"):
            finalize_work(self.packet, self.advice, [self.disposition], [receipt], self.content)

    def test_receipt_cannot_bypass_exact_advice_and_disposition_chain(self):
        with self.assertRaisesRegex(WorkBundleError, "requires supplied advice"):
            finalize_work(self.packet, None, [], [self.receipt], {"packet": "1"*64, "advice": None, "dispositions": [], "receipts": ["4"*64]})

    def test_duplicate_disposition_and_receipt_ids_reject_all(self):
        second = copy.deepcopy(self.disposition); second["disposition_id"] = "d2"
        with self.assertRaisesRegex(WorkBundleError, "ambiguous"):
            finalize_work(self.packet, self.advice, [self.disposition, second], [], {"packet": "1"*64, "advice": "2"*64, "dispositions": ["3"*64, "5"*64], "receipts": []})
        with self.assertRaisesRegex(WorkBundleError, "duplicate receipt"):
            finalize_work(self.packet, self.advice, [self.disposition], [self.receipt, self.receipt], {"packet": "1"*64, "advice": "2"*64, "dispositions": ["3"*64], "receipts": ["4"*64, "4"*64]})

    def test_tampered_bundle_is_rejected(self):
        bundle = finalize_work(self.packet, self.advice, [self.disposition], [self.receipt], self.content)
        bundle["summary"]["receipts"] = 99
        with self.assertRaisesRegex(WorkBundleError, "self-digest"):
            validate_bundle(bundle)


if __name__ == "__main__": unittest.main()
