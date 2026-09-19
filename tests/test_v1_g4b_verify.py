"""Hermetic G4-B conformance tests; not live historical qualification proof."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from g4b_fixture import synthetic_workspace

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "v1" / "g4b_verify.py"
RECORD = ROOT / "docs" / "project" / "v1-g4b-verification.json"

spec = importlib.util.spec_from_file_location("g4b_verify", SCRIPT)
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


class G4BFrozenContractTests(unittest.TestCase):
    """Freeze historical bindings without querying ambient refs or sibling repos."""

    def test_emit_equals_checked_in_historical_record(self):
        self.assertEqual(gv.emit_record(ROOT), load_record())
        self.assertEqual(len(load_record()["suite_replay"]), 12)
        self.assertEqual(load_record()["accepted_g4_content"], [])

    def test_lineage_binds_decided_v2_cycles(self):
        rec = load_record()
        self.assertEqual(
            [(e["cycle_id"], e["disposition"]) for e in rec["revised_lineage"]],
            [
                ("cycle-holdingco-coordination-nonclaimable-v2", "revised"),
                ("cycle-teachingco-g1-already-adopted-refusal", "other_disposition"),
                ("cycle-softwareco-g1-scanner-completeness-is-not-active-resolution",
                 "revised"),
            ],
        )
        for item in gv.LINEAGE:
            self.assertFalse(Path(item["path"]).is_absolute())

    def test_template_deterministic_subprocess(self):
        outputs = []
        for _ in range(2):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "template"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(result.stdout)
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(json.loads(outputs[0])["candidate_commit"], gv.CANDIDATE_COMMIT)

    def test_emit_subprocess_preserves_historical_bindings(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "emit"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), load_record())

    def test_unmodified_cli_refuses_missing_historical_candidate(self):
        # A real subprocess imports unpatched production constants. Do not pass
        # the synthetic record: that would fail before checking the Git ref.
        with synthetic_workspace(gv) as fixture:
            fixture.git("branch", "-D", gv.CANDIDATE_BRANCH)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "validate", str(RECORD),
                 "--repo-root", str(fixture.root)],
                capture_output=True, text=True, cwd=fixture.workspace)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["code"], "candidate_missing")

    def test_fixture_restores_bindings_and_environment(self):
        candidate, lineage = gv.CANDIDATE_COMMIT, gv.LINEAGE
        environment = dict(os.environ)
        with synthetic_workspace(gv) as fixture:
            self.assertNotEqual(gv.CANDIDATE_COMMIT, candidate)
            self.assertTrue(fixture.root.is_dir())
        self.assertEqual(gv.CANDIDATE_COMMIT, candidate)
        self.assertIs(gv.LINEAGE, lineage)
        self.assertEqual(dict(os.environ), environment)
        self.assertFalse(fixture.workspace.exists())


class G4BSyntheticTests(unittest.TestCase):
    def setUp(self):
        context = synthetic_workspace(gv)
        self.fixture = context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        self.root = self.fixture.root
        self.record = self.fixture.record

    def assert_rejected(self, code):
        with self.assertRaises(gv.ValidationError) as ctx:
            gv.validate_record(self.record, self.root)
        self.assertEqual(ctx.exception.code, code)

    def cli_main(self):
        # Exercises actual argument parsing, file loading and serialization with
        # test-bound identities; it is not a live historical CLI acceptance.
        path = self.root / "synthetic-verification.json"
        path.write_text(json.dumps(self.record), encoding="utf-8")
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = gv.main(["validate", str(path), "--repo-root", str(self.root)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_validate_passes(self):
        result = gv.validate_record(self.record, self.root)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["suite_cases"], 12)
        self.assertEqual(result["accepted_g4_content_count"], 0)
        self.assertEqual(result["verification_digest"], gv.digest_of(self.record))

    def test_cli_main_success_with_synthetic_bindings(self):
        code, stdout, stderr = self.cli_main()
        self.assertEqual(code, 0, stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout)["candidate_commit"], self.fixture.candidate)
        self.assertEqual(json.loads(stdout)["status"], "pass")

    def test_cli_main_missing_cycle_is_structured_failure(self):
        (self.root / self.fixture.lineage[0]["path"]).unlink()
        code, stdout, stderr = self.cli_main()
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(json.loads(stderr)["code"], "missing_file")

    def test_accepted_content_rejected(self):
        self.record["accepted_g4_content"] = [{"path": "catalog.json"}]
        self.assert_rejected("accepted_content_not_empty")

    def test_wrong_candidate_rejected(self):
        self.record["candidate_commit"] = "0" * 40
        self.assert_rejected("wrong_candidate")

    def test_wrong_branch_rejected(self):
        self.record["candidate_branch"] = "other-branch"
        self.assert_rejected("wrong_branch")

    def test_missing_candidate_ref_rejected(self):
        self.fixture.git("branch", "-D", gv.CANDIDATE_BRANCH)
        self.assert_rejected("candidate_missing")

    def test_drifted_candidate_tip_rejected(self):
        self.fixture.git("branch", "-f", gv.CANDIDATE_BRANCH, "main")
        self.assert_rejected("candidate_missing")

    def test_candidate_is_main_rejected(self):
        self.fixture.git("update-ref", "refs/heads/main", self.fixture.candidate)
        self.assert_rejected("candidate_is_main")

    def test_actual_release_tag_rejected(self):
        self.fixture.git("tag", "v1.0.0")
        self.assert_rejected("tag_present")

    def test_missing_cycle_file_rejected(self):
        for item in self.fixture.lineage:
            with self.subTest(cycle=item["cycle_id"]):
                path = self.root / item["path"]
                original = path.read_bytes()
                path.unlink()
                try:
                    self.assert_rejected("missing_file")
                finally:
                    path.write_bytes(original)

    def test_valid_on_disk_cycle_digest_drift_rejected(self):
        for item in self.fixture.lineage:
            with self.subTest(cycle=item["cycle_id"]):
                path = self.root / item["path"]
                original = path.read_bytes()
                cycle = json.loads(original)
                cycle["minimum_decision_record"]["problem"] = "changed synthetic problem"
                # Still a valid cycle; only its binding to the expected bytes drifts.
                gv.load_ge().validate_cycle(cycle)
                path.write_text(json.dumps(cycle), encoding="utf-8")
                try:
                    self.assert_rejected("digest_mismatch")
                finally:
                    path.write_bytes(original)

    def test_lineage_digest_drift_rejected(self):
        self.record["revised_lineage"][0]["cycle_digest"] = "f" * 64
        self.assert_rejected("digest_mismatch")

    def test_lineage_promoted_rejected(self):
        self.record["revised_lineage"][0]["disposition"] = "promoted"
        self.assert_rejected("invalid_lineage")

    def test_lineage_disposition_drift_rejected(self):
        self.record["revised_lineage"][1]["disposition"] = "revised"
        self.assert_rejected("disposition_mismatch")

    def test_suite_digest_drift_rejected(self):
        self.record["suite_replay"][0]["digest"] = "0" * 64
        self.assert_rejected("suite_digest_mismatch")

    def test_incomplete_suite_rejected(self):
        self.record["suite_replay"] = self.record["suite_replay"][:10]
        self.assert_rejected("suite_incomplete")

    def test_validate_resolves_synthetic_repo_root_from_any_cwd(self):
        previous = Path.cwd()
        try:
            os.chdir(self.fixture.workspace)
            code, stdout, stderr = self.cli_main()
        finally:
            os.chdir(previous)
        self.assertEqual(code, 0, stderr)
        self.assertEqual(json.loads(stdout)["status"], "pass")

    def test_validation_does_not_change_refs_or_cycles(self):
        refs = self.fixture.git("show-ref")
        files = [(self.root / item["path"]).resolve() for item in self.fixture.lineage]
        before = {path: path.read_bytes() for path in files}
        gv.validate_record(self.record, self.root)
        self.assertEqual(self.fixture.git("show-ref"), refs)
        self.assertEqual({path: path.read_bytes() for path in files}, before)


if __name__ == "__main__":
    unittest.main()
