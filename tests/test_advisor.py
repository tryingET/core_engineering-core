# summary: "Tests bounded advisory request construction and fail-closed response, citation, redaction, and review-only patch validation."
# read_when:
#   - "Changing advisory evidence budgets, response schemas, abstention, citations, secret handling, or patch proposal constraints."

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.advisor import AdviceError, build_request, validate_response
from engineering_core.catalog import load_catalog
from engineering_core.engineering_plan import compile_plan


class AdvisorTests(unittest.TestCase):
    def request(self, repo: Path | None = None):
        repo = repo or ROOT
        catalog = load_catalog(ROOT, prefer_repo=True)
        plan = compile_plan(repo, catalog)
        ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
        return build_request(repo, plan, ids)

    def response(self, request):
        evidence = request["evidence"][0]
        return {
            "schema": "engineering-advice-response-v1", "request_sha256": request["request_sha256"],
            "provenance": {"provider": "fixture", "model": "deterministic", "model_version": "1", "adapter": "file", "adapter_version": "1", "prompt_id": request["prompt"]["id"], "prompt_version": request["prompt"]["version"]},
            "status": "advice", "summary": "Review this bounded proposal.",
            "recommendations": [{"id": "r1", "catalog_ids": ["py"], "recommendation": "Keep package metadata explicit.", "confidence": 0.8, "unknowns": ["Runtime deployment is unknown."], "counterevidence": ["A manifest alone does not prove runtime use."], "falsification": ["Show that Python is not shipped."], "citations": [{"evidence_id": evidence["id"], "path": evidence["path"], "start": 0, "end": 1}], "competes_with": []}],
            "critiques": [{"recommendation_id": "r1", "critique": "Manifest inference can be stale.", "severity": "medium", "falsification": "Confirm active build output."}],
            "patch_proposals": [{"path": "docs/engineering.local.md", "unified_diff": "--- a/docs/engineering.local.md\n+++ b/docs/engineering.local.md\n@@ -0,0 +1 @@\n+proposal\n", "rationale": "Owner-reviewable documentation proposal.", "recommendation_id": "r1"}],
        }

    def test_valid_competing_advice_and_patch_is_not_applied(self):
        request = self.request(); response = self.response(request)
        second = copy.deepcopy(response["recommendations"][0]); second["id"] = "r2"; second["competes_with"] = ["r1"]
        response["recommendations"][0]["competes_with"] = ["r2"]; response["recommendations"].append(second)
        before = (ROOT / "docs" / "engineering.local.md").exists()
        self.assertEqual(validate_response(request, response), response)
        self.assertEqual((ROOT / "docs" / "engineering.local.md").exists(), before)

    def test_abstain_is_first_class(self):
        request = self.request(); response = self.response(request)
        response.update(status="abstain", recommendations=[], critiques=[], patch_proposals=[], summary="Insufficient bounded evidence.")
        validate_response(request, response)

    def test_hallucinations_malformed_and_adversarial_paths_fail_closed(self):
        request = self.request()
        mutations = []
        unknown = self.response(request); unknown["recommendations"][0]["catalog_ids"] = ["invented"]; mutations.append(unknown)
        path = self.response(request); path["recommendations"][0]["citations"][0]["path"] = "invented.txt"; mutations.append(path)
        span = self.response(request); span["recommendations"][0]["citations"][0]["end"] = 10**9; mutations.append(span)
        patch = self.response(request); patch["patch_proposals"][0]["path"] = "../escape"; mutations.append(patch)
        malformed = self.response(request); malformed["surprise"] = True; mutations.append(malformed)
        mismatch = self.response(request); mismatch["patch_proposals"][0]["unified_diff"] = "--- a/etc/passwd\n+++ b/etc/passwd\n@@ -1 +1 @@\n-x\n+y\n"; mutations.append(mismatch)
        extra = self.response(request); extra["patch_proposals"][0]["unified_diff"] += "--- a/other\n+++ b/other\n"; mutations.append(extra)
        windows = self.response(request); windows["patch_proposals"][0]["path"] = "C:\\Windows\\win.ini"; mutations.append(windows)
        boolean_span = self.response(request); boolean_span["recommendations"][0]["citations"][0]["start"] = False; mutations.append(boolean_span)
        for response in mutations:
            with self.assertRaises(AdviceError): validate_response(request, response)

    def test_budget_and_secret_redaction(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary); (repo / "pyproject.toml").write_text(
                '[project]\nname="x"\npassword = "hunter2"\n'
                'metadata = {"api_key":"json-secret", "token": "json-token"}\n'
                'email="me@example.com"\n'
            )
            request = self.request(repo)
            serialized = json.dumps(request)
            for secret in ("hunter2", "json-secret", "json-token", "me@example.com"):
                self.assertNotIn(secret, serialized)
            self.assertGreaterEqual(request["safeguards"]["redactions"], 4)
            catalog = load_catalog(ROOT, prefer_repo=True)
            plan = compile_plan(repo, catalog)
            source_size = (repo / "pyproject.toml").stat().st_size
            expanded = build_request(repo, plan, set(catalog.ids("lanes")), max_file_bytes=source_size)
            self.assertEqual(expanded["evidence"], [], "redacted disclosure must obey the per-file budget")
            with self.assertRaises(AdviceError):
                build_request(repo, plan, set(catalog.ids("lanes")), max_total_bytes=262145)

    def test_response_item_budget_rejected(self):
        request = self.request(); response = self.response(request)
        response["recommendations"] = response["recommendations"] * 21
        with self.assertRaises(AdviceError): validate_response(request, response)


if __name__ == "__main__": unittest.main()
