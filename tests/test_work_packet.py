import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from engineering_core.catalog import load_catalog
from engineering_core.closed_loop import canonical_digest
from engineering_core.work_bundle import finalize_work
from engineering_core.work_packet import WorkPacketError, _plan_digest, _request_digest, _validate_snapshot, prepare_work, validate_packet
from engineering_core.safe_io import read_bounded_json
from engineering_core.work_verify import verify_work


class WorkPacketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        (self.repo / "pyproject.toml").write_text('[project]\nname="fixture"\nversion="0.1.0"\n')
        (self.repo / "focus.txt").write_text("bounded work\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "fixture"], check=True)
        self.catalog = load_catalog()

    def tearDown(self):
        self.temp.cleanup()

    def context(self, mode="advisor-ready"):
        return {
            "schema": "engineering-work-context-v1",
            "authority": "owner-supplied task context; repository and task authorities remain external",
            "repository_id": "owned/fixture",
            "work": {"id": "task-1", "title": "Bounded fixture", "objective": "Exercise the owner-use packet."},
            "mode": mode,
            "scope": {"focus_paths": ["focus.txt"], "constraints": ["Do not execute commands."], "validation": ["Owner selects validation."]},
            "provenance": {"owner": "owned/fixture", "owner_type": "repository", "produced_at": "2026-07-12T00:00:00Z", "source": "test fixture"},
        }

    def test_prepare_is_deterministic_and_bound(self):
        first = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        second = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        self.assertEqual(first, second)
        self.assertEqual("advisor-ready", first["context"]["mode"])
        self.assertIsNotNone(first["advice_request"])
        self.assertIn("focus.txt", [item["path"] for item in first["advice_request"]["evidence"]])
        self.assertEqual(first, validate_packet(first))
        self.assertFalse(first["effects"]["consumer_commands_executed"])

    def test_plan_only_has_no_request(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context("plan-only"), self.catalog)
        self.assertIsNone(packet["advice_request"])
        self.assertIsNone(packet["bindings"]["request_sha256"])

    def test_different_owner_task_context_changes_request_binding(self):
        first = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        context = self.context(); context["work"] = {**context["work"], "id": "task-2", "objective": "A different bounded owner task."}
        second = prepare_work(self.repo, "owned/fixture", context, self.catalog)
        self.assertNotEqual(first["context_sha256"], second["context_sha256"])
        self.assertNotEqual(first["bindings"]["request_sha256"], second["bindings"]["request_sha256"])
        self.assertEqual("engineering-work-advice-request-v1", first["advice_request"]["schema"])
        self.assertEqual(first["context_sha256"], first["advice_request"]["work"]["context_sha256"])

    def test_context_identity_and_paths_fail_closed(self):
        context = self.context(); context["repository_id"] = "other"
        with self.assertRaisesRegex(WorkPacketError, "repository_id"):
            prepare_work(self.repo, "owned/fixture", context, self.catalog)
        for unsafe in ("../escape", ":(glob)**", "-option"):
            context = self.context(); context["scope"]["focus_paths"] = [unsafe]
            with self.assertRaisesRegex(WorkPacketError, "safe repository-relative"):
                prepare_work(self.repo, "owned/fixture", context, self.catalog)

    def test_symlink_focus_is_rejected(self):
        (self.repo / "focus.txt").unlink(); (self.repo / "focus.txt").symlink_to("pyproject.toml")
        with self.assertRaisesRegex(WorkPacketError, "focus path rejected"):
            prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)

    def test_dangling_symlink_focus_is_rejected(self):
        (self.repo / "focus.txt").unlink(); (self.repo / "focus.txt").symlink_to("missing-target")
        with self.assertRaisesRegex(WorkPacketError, "focus path rejected"):
            prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)

    def test_prepare_does_not_write_git_index_metadata(self):
        (self.repo / "focus.txt").write_text("dirty owner work\n")
        index = self.repo / ".git/index"; before = index.stat().st_mtime_ns
        prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        self.assertEqual(before, index.stat().st_mtime_ns)

    def test_absent_focus_below_symlinked_parent_is_rejected(self):
        outside = Path(self.temp.name) / "outside"; outside.mkdir()
        (self.repo / "linked").symlink_to(outside, target_is_directory=True)
        context = self.context(); context["scope"]["focus_paths"] = ["linked/absent.txt"]
        with self.assertRaisesRegex(WorkPacketError, "focus path rejected"):
            prepare_work(self.repo, "owned/fixture", context, self.catalog)

    def test_repository_fsmonitor_command_is_disabled(self):
        sentinel = Path(self.temp.name) / "fsmonitor-ran"
        hook = Path(self.temp.name) / "fsmonitor.sh"
        hook.write_text(f"#!/bin/sh\ntouch {sentinel}\necho\n")
        hook.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "config", "core.fsmonitor", str(hook)], check=True)
        prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        self.assertFalse(sentinel.exists())

    def test_maximal_evidence_packet_round_trips_with_workflow_budget(self):
        paths = []
        for index in range(5):
            relative = f"large-{index}.txt"; (self.repo / relative).write_text("x" * 60_000); paths.append(relative)
        context = self.context(); context["scope"]["focus_paths"] = paths
        packet = prepare_work(self.repo, "owned/fixture", context, self.catalog)
        packet_path = Path(self.temp.name) / "packet.json"; packet_path.write_text(json.dumps(packet, sort_keys=True))
        loaded, _ = read_bounded_json(packet_path, max_bytes=8_388_608)
        self.assertEqual(packet["packet_sha256"], loaded["packet_sha256"])
        bundle = finalize_work(packet, None, [], [], {"packet": "a"*64, "advice": None, "dispositions": [], "receipts": []})
        bundle_path = Path(self.temp.name) / "bundle.json"; bundle_path.write_text(json.dumps(bundle, sort_keys=True))
        self.assertEqual(bundle["bundle_sha256"], read_bounded_json(bundle_path, max_bytes=8_388_608)[0]["bundle_sha256"])

    def test_verify_reports_scope_drift_as_stale(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context("plan-only"), self.catalog)
        digest = "a" * 64
        bundle = finalize_work(packet, None, [], [], {"packet": digest, "advice": None, "dispositions": [], "receipts": []})
        self.assertEqual("matched", verify_work(self.repo, "owned/fixture", bundle, self.catalog)["result"])
        (self.repo / "focus.txt").write_text("changed owner work\n")
        result = verify_work(self.repo, "owned/fixture", bundle, self.catalog)
        self.assertEqual("stale", result["result"])
        self.assertFalse(result["scope_match"])

    def test_packet_tampering_is_rejected(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        packet = json.loads(json.dumps(packet)); packet["context"]["work"]["title"] = "tampered"
        with self.assertRaisesRegex(WorkPacketError, "self-digest"):
            validate_packet(packet)

    def test_deep_nested_validators_reject_redigested_tampering(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        request = json.loads(json.dumps(packet["advice_request"])); request["authority"] = "changed"; request["request_sha256"] = canonical_digest({k:v for k,v in request.items() if k != "request_sha256"})
        with self.assertRaisesRegex(WorkPacketError, "authority"):
            _request_digest(request, packet["plan"], packet["context"], packet["scope_snapshot"], packet["repository"]["revision"])
        request = json.loads(json.dumps(packet["advice_request"])); request["work"]["repository_revision"] = "0"*40; binding={k:request["work"][k] for k in ("context_sha256","scope_sha256","repository_revision")}; binding["plan_sha256"]=packet["plan"]["digests"]["plan_sha256"]; request["work"]["work_binding_sha256"]=canonical_digest(binding); request["request_sha256"] = canonical_digest({k:v for k,v in request.items() if k != "request_sha256"})
        with self.assertRaisesRegex(WorkPacketError, "context or scope binding"):
            _request_digest(request, packet["plan"], packet["context"], packet["scope_snapshot"], packet["repository"]["revision"])
        snapshot=json.loads(json.dumps(packet["scope_snapshot"])); snapshot["files"][0]["bytes"]=1_048_577; snapshot["scope_sha256"]=canonical_digest({k:v for k,v in snapshot.items() if k != "scope_sha256"})
        with self.assertRaisesRegex(WorkPacketError, "bounded bytes"):
            _validate_snapshot(snapshot, packet["context"]["scope"]["focus_paths"])
        plan=json.loads(json.dumps(packet["plan"])); plan["selections"].append(plan["selections"][0]); unsigned=dict(plan); unsigned["digests"]=dict(plan["digests"]); unsigned["digests"].pop("plan_sha256"); plan["digests"]["plan_sha256"]=canonical_digest(unsigned)
        with self.assertRaisesRegex(WorkPacketError, "duplicated"):
            _plan_digest(plan)

    def test_redigested_nonfinite_and_oversized_packets_are_rejected(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        nonfinite = json.loads(json.dumps(packet)); nonfinite["plan"]["diagnostics"] = [{"code": "bad", "message": float("nan"), "path": "x", "severity": "error"}]
        plan_unsigned = dict(nonfinite["plan"]); plan_unsigned["digests"] = dict(plan_unsigned["digests"]); plan_unsigned["digests"].pop("plan_sha256"); nonfinite["plan"]["digests"]["plan_sha256"] = canonical_digest(plan_unsigned)
        unsigned = dict(nonfinite); unsigned.pop("packet_sha256"); nonfinite["packet_sha256"] = canonical_digest(unsigned)
        with self.assertRaisesRegex(WorkPacketError, "non-finite"):
            validate_packet(nonfinite)
        oversized = json.loads(json.dumps(packet)); oversized["plan"]["diagnostics"] = [{"code": "large", "message": "x" * 4_300_000, "path": "x", "severity": "error"}]
        plan_unsigned = dict(oversized["plan"]); plan_unsigned["digests"] = dict(plan_unsigned["digests"]); plan_unsigned["digests"].pop("plan_sha256"); oversized["plan"]["digests"]["plan_sha256"] = canonical_digest(plan_unsigned)
        unsigned = dict(oversized); unsigned.pop("packet_sha256"); oversized["packet_sha256"] = canonical_digest(unsigned)
        with self.assertRaisesRegex(WorkPacketError, "byte budget"):
            validate_packet(oversized)

    def test_redigested_malformed_nested_plan_is_rejected(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        packet["plan"]["selections"] = "not-an-array"
        plan_unsigned = dict(packet["plan"]); plan_unsigned["digests"] = dict(plan_unsigned["digests"]); plan_unsigned["digests"].pop("plan_sha256"); packet["plan"]["digests"]["plan_sha256"] = canonical_digest(plan_unsigned)
        unsigned = dict(packet); unsigned.pop("packet_sha256"); packet["packet_sha256"] = canonical_digest(unsigned)
        with self.assertRaisesRegex(WorkPacketError, "bounded array"):
            validate_packet(packet)

    def test_redigested_malformed_snapshot_is_rejected(self):
        packet = prepare_work(self.repo, "owned/fixture", self.context(), self.catalog)
        packet["scope_snapshot"] = {"scope_sha256": packet["scope_snapshot"]["scope_sha256"]}
        unsigned = dict(packet); unsigned.pop("packet_sha256"); packet["packet_sha256"] = canonical_digest(unsigned)
        with self.assertRaisesRegex(WorkPacketError, "scope_snapshot"):
            validate_packet(packet)


if __name__ == "__main__":
    unittest.main()
