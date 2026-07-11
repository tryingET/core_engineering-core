from __future__ import annotations
import copy, json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from engineering_core.closed_loop import *
from engineering_core.catalog import load_catalog
from engineering_core.engineering_plan import compile_plan

SHA = "a" * 64
class ClosedLoopTests(unittest.TestCase):
    def receipt(self, state="declared"):
        observations = []
        if state == "execution-observed": observations = [{"kind":"execution","outcome":"observed","evidence_sha256":SHA,"reference":"owner log 1"}]
        if state == "evidence-verified": observations = [{"kind":"artifact","outcome":"passed","evidence_sha256":SHA,"reference":"owner artifact 1"}]
        return {"schema":RECEIPT_SCHEMA,"receipt_id":"e1","authority":"owner-evidence-only; not CI, release, AK, or compliance authority","provenance":{"owner":"repo-owner","owner_type":"repository","produced_at":"2026-07-11T00:00:00Z","source":"fixture"},"bindings":{"plan_sha256":SHA,"catalog_sha256":SHA,"repository_facts_sha256":SHA},"target":{"repository":"example/repo","revision":"abc","recommendation_id":"r1"},"observations":observations,"state":state,"reason":"owner declaration"}
    def advice(self):
        return {
            "schema":"engineering-advice-response-v1", "request_sha256":"b"*64,
            "provenance":{"provider":"fixture","model":"deterministic","model_version":"1","adapter":"file","adapter_version":"1","prompt_id":"bounded-advisor","prompt_version":"1"},
            "status":"advice", "summary":"Bounded fixture advice.",
            "recommendations":[{"id":"r1","catalog_ids":["py"],"recommendation":"Keep metadata explicit.","confidence":.8,"unknowns":[],"counterevidence":[],"falsification":[],"citations":[],"competes_with":[]}],
            "critiques":[], "patch_proposals":[],
        }
    def disposition(self, advice):
        return {"schema":DISPOSITION_SCHEMA,"disposition_id":"d1","authority":"owner disposition; advisory inputs do not self-authorize","provenance":{"owner":"repo-owner","owner_type":"repository","produced_at":"2026-07-11T00:00:00Z","source":"review"},"bindings":{"request_sha256":"b"*64,"advice_sha256":canonical_digest(advice),"plan_sha256":SHA,"catalog_sha256":SHA,"repository_facts_sha256":SHA},"target":{"repository":"example/repo","revision":"abc"},"recommendation_id":"r1","decision":"accepted","reason_code":"adopted","rationale":"Owner accepted after review."}
    def test_receipt_states_and_summary_are_deterministic(self):
        receipts = [self.receipt(s) for s in STATES]
        for i, receipt in enumerate(receipts): receipt["receipt_id"] = f"e{i}"
        self.assertEqual(summarize_receipts(reversed(receipts)), summarize_receipts(receipts))
        self.assertEqual(sum(summarize_receipts(receipts)["counts"].values()), len(STATES))
    def test_disposition_calibration_separates_outcomes(self):
        advice=self.advice(); disposition=self.disposition(advice); receipt=self.receipt("evidence-verified")
        validate_disposition(disposition, advice)
        row=calibration(advice,[disposition],[receipt])["outcomes"][0]
        self.assertEqual(row["model_confidence"],.8); self.assertTrue(row["accepted"]); self.assertTrue(row["evidence_verified"])
    def test_calibration_does_not_cross_contaminate_reused_id(self):
        advice=self.advice(); disposition=self.disposition(advice)
        mutations = (
            lambda receipt: receipt["bindings"].__setitem__("catalog_sha256", "c"*64),
            lambda receipt: receipt["bindings"].__setitem__("repository_facts_sha256", "c"*64),
            lambda receipt: receipt["target"].__setitem__("repository", "other/repo"),
            lambda receipt: receipt["target"].__setitem__("revision", "other-revision"),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                receipt=self.receipt("evidence-verified"); mutate(receipt)
                row=calibration(advice,[disposition],[receipt])["outcomes"][0]
                self.assertFalse(row["evidence_verified"]); self.assertEqual(row["receipt_ids"],[])
    def test_patterns_reject_mismatched_plan_provenance(self):
        plan=compile_plan(ROOT,load_catalog(ROOT,prefer_repo=True)); receipt=self.receipt()
        receipt["bindings"]["plan_sha256"]=plan["digests"]["plan_sha256"]
        receipt["bindings"]["catalog_sha256"]="c"*64
        receipt["bindings"]["repository_facts_sha256"]=plan["digests"]["repository_facts_sha256"]
        with self.assertRaises(ClosedLoopError): synthesize_patterns([plan],[],[],[receipt])
    def test_duplicate_records_fail_closed(self):
        advice=self.advice(); disposition=self.disposition(advice)
        with self.assertRaises(ClosedLoopError): calibration(advice,[disposition,copy.deepcopy(disposition)],[])
    def test_patterns_malformed_records_fail_with_closed_loop_error(self):
        plan=compile_plan(ROOT,load_catalog(ROOT,prefer_repo=True)); advice=self.advice()
        malformed_values = (
            ([plan], [advice], [{}], []),
            ([plan], [advice], [], [{}]),
            ([plan], [{"schema":"engineering-advice-response-v1","recommendations":None}], [], []),
            ([plan], [{"schema":"engineering-advice-response-v1"}], [], []),
            ([None], [], [], []),
            ([{**plan, "digests": None}], [], [], []),
            ([{**plan, "selections": [{}]}], [], [], []),
        )
        for args in malformed_values:
            with self.subTest(args=args):
                with self.assertRaises(ClosedLoopError):
                    synthesize_patterns(*args)

    def test_fail_closed_and_proposals_unapplied(self):
        advice=self.advice(); bad=self.disposition(advice); bad["recommendation_id"]="hallucinated"
        with self.assertRaises(ClosedLoopError): validate_disposition(bad, advice)
        secret=self.receipt(); secret["reason"]="password=hunter2"
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.json"; p.write_text(json.dumps(secret))
            with self.assertRaises(ClosedLoopError): load_record(p)
            p.write_text('{"password":"hunter2"}')
            with self.assertRaises(ClosedLoopError): load_record(p)
        plan=compile_plan(ROOT,load_catalog(ROOT,prefer_repo=True))
        with self.assertRaises(ClosedLoopError): synthesize_patterns([plan,copy.deepcopy(plan)],[],[],[])
        patterns=synthesize_patterns([plan],[],[],[])
        proposal=doctrine_proposal(patterns)
        self.assertEqual(proposal["status"],"unapplied"); self.assertEqual(proposal["mutations_performed"],[])
if __name__ == "__main__": unittest.main()
