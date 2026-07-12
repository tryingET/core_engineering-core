# ---
# summary: "Covers capability-contract parsing and the declaration, observation, and evidence statuses exposed for supported capabilities."
# read_when:
#   - "Changing capability contract versions, schema bindings, invalid declarations, or capability result transitions."
# ---

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.capabilities import capability_results, parse_capability_contract

P = SimpleNamespace(engineering_plan="engineering-plan-v1", advice_request="engineering-advice-request-v1", advice_response="engineering-advice-response-v1", evidence_receipt="engineering-evidence-receipt-v1", recommendation_disposition="engineering-recommendation-disposition-v1")


class CapabilityTests(unittest.TestCase):
    def test_absent_is_compatible(self):
        contract = parse_capability_contract({}, P)
        self.assertEqual(contract.status, "absent")
        self.assertEqual(capability_results(contract, P)["planning"]["observation_status"], "not-declared")

    def test_exact_contract_and_transitions(self):
        raw = {"capability_contract": {"version": "engineering-core-capabilities-v1", "capabilities": {
            "planning": {"status": "declared", "schema": "engineering-plan-v1"},
            "advisor": {"status": "declared", "request_schema": "engineering-advice-request-v1", "response_schema": "engineering-advice-response-v1"},
            "closed_loop": {"status": "declared", "receipt_schema": "engineering-evidence-receipt-v1", "disposition_schema": "engineering-recommendation-disposition-v1"}}}}
        contract = parse_capability_contract(raw, P)
        result = capability_results(contract, P, {"planning": True, "advisor": True})
        self.assertEqual(contract.status, "valid")
        self.assertEqual(result["planning"]["observation_status"], "observable")
        self.assertEqual(result["advisor"]["observation_status"], "observable")
        self.assertEqual(result["closed_loop"]["observation_status"], "not-observed")
        self.assertTrue(all(item["evidence_status"] == "not-supplied" for item in result.values()))

    def test_mixed_invalid_contract_blocks_all_capabilities(self):
        raw = {"capability_contract": {"version": "engineering-core-capabilities-v1", "capabilities": {
            "planning": {"status": "declared", "schema": "engineering-plan-v1"}, "unknown": {}}}}
        result = capability_results(parse_capability_contract(raw, P), P, {"planning": True})
        self.assertTrue(all(item["declaration_status"] == "invalid" for item in result.values()))
        self.assertTrue(all(item["observation_status"] == "blocked" for item in result.values()))

    def test_unsupported_and_unknown_are_blocked(self):
        unsupported = parse_capability_contract({"capability_contract": {"version": "future", "capabilities": {}}}, P)
        invalid = parse_capability_contract({"capability_contract": {"version": "engineering-core-capabilities-v1", "capabilities": {"shell": {}}}}, P)
        self.assertEqual(unsupported.status, "unsupported")
        self.assertEqual(invalid.status, "invalid")
        self.assertEqual(capability_results(invalid, P)["advisor"]["observation_status"], "blocked")


if __name__ == "__main__": unittest.main()
