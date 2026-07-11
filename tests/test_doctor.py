import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.doctor import build_doctor


class DoctorTests(unittest.TestCase):
    def repo(self, root: Path, contract=None, ref="v0.7.0") -> Path:
        (root / "policy").mkdir()
        ec = {"ref": ref, "lane": "py", "disciplines": []}
        if contract is not None: ec["capability_contract"] = contract
        (root / "policy/engineering-lane.json").write_text(json.dumps({"engineering_core": ec}))
        return root

    def test_absent_contract_degraded_and_non_executing(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = build_doctor(self.repo(Path(tmp)))
        self.assertEqual(report["status"], "degraded")
        self.assertFalse(report["consumer_commands_executed"])
        self.assertFalse(report["external_models_invoked"])
        self.assertEqual(report["mutations_performed"], [])

    def test_planning_advisor_healthy(self):
        contract = {"version": "engineering-core-capabilities-v1", "capabilities": {
            "planning": {"status": "declared", "schema": "engineering-plan-v1"},
            "advisor": {"status": "declared", "request_schema": "engineering-advice-request-v1", "response_schema": "engineering-advice-response-v1"}}}
        with tempfile.TemporaryDirectory() as tmp:
            report = build_doctor(self.repo(Path(tmp), contract))
        self.assertEqual(report["status"], "healthy")
        self.assertEqual(report["capabilities"]["planning"]["observation_status"], "observable")

    def test_oversized_target_path_returns_structured_blocked_report(self):
        report = build_doctor(Path("x" * 5000))
        self.assertEqual(report["schema"], "engineering-doctor-v1")
        self.assertEqual(report["status"], "blocked")
        self.assertLessEqual(len(report["repository"].encode()), 4096)
        self.assertEqual(set(report["capabilities"]), {"planning", "advisor", "closed_loop"})

    def test_symlinked_policy_is_rejected_without_reading_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "policy").mkdir()
            outside = root / "outside.json"; outside.write_text(json.dumps({"engineering_core": {"ref": "v0.6.0"}}))
            (root / "policy/engineering-lane.json").symlink_to(outside)
            report = build_doctor(root)
        self.assertEqual(report["status"], "blocked")
        policy_check = next(item for item in report["checks"] if item["id"] == "policy")
        self.assertEqual(policy_check["status"], "fail")

    def test_invalid_contract_blocks(self):
        contract = {"version": "engineering-core-capabilities-v1", "capabilities": {"planning": {"status": "declared", "schema": "wrong"}}}
        with tempfile.TemporaryDirectory() as tmp:
            report = build_doctor(self.repo(Path(tmp), contract))
        self.assertEqual(report["status"], "blocked")


if __name__ == "__main__": unittest.main()
