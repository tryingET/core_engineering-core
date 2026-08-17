from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.catalog_model import load_catalog
from engineering_core.cli import main
from engineering_core.doctor import doctor_repo, exit_code, render_human


def write_policy(repo: Path, *, lanes: list[str], disciplines: list[str]) -> None:
    (repo / "docs").mkdir(parents=True, exist_ok=True)
    (repo / "policy").mkdir(parents=True, exist_ok=True)
    selections = "\n".join(f"- {item}" for item in [*lanes, *disciplines])
    (repo / "docs" / "engineering.local.md").write_text(
        f"# engineering.local\n\n## Selected guidance\n{selections}\n\nCanonical local commands: validate before handoff.\n",
        encoding="utf-8",
    )
    (repo / "policy" / "engineering-lane.json").write_text(
        json.dumps(
            {
                "engineering_core": {
                    "lanes": lanes,
                    "disciplines": disciplines,
                    "ref": "workspace-local-unpinned",
                    "catalog_command": "engineering-core catalog --pretty",
                    "list_disciplines_command": "engineering-core list-disciplines",
                    "list_templates_command": "engineering-core list-templates",
                }
            }
        ),
        encoding="utf-8",
    )


class DoctorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog(REPO_ROOT, prefer_repo=True)

    def test_valid_adoption_has_no_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_policy(repo, lanes=["ts"], disciplines=["validation", "testing"])
            report = doctor_repo(repo, self.catalog)
        self.assertEqual(exit_code(report), 0)
        self.assertEqual(report["summary"]["fail"], 0)
        self.assertIn("[PASS] policy.parse", render_human(report))

    def test_invalid_policy_is_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "policy").mkdir()
            (repo / "policy" / "engineering-lane.json").write_text("{", encoding="utf-8")
            report = doctor_repo(repo, self.catalog)
        self.assertEqual(exit_code(report), 1)
        rule_ids = {item["rule_id"] for item in report["diagnostics"]}
        self.assertIn("policy.invalid-json", rule_ids)

    def test_addendum_requirements_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_policy(repo, lanes=["ts-frontend"], disciplines=["validation"])
            report = doctor_repo(repo, self.catalog)
        failures = [item for item in report["diagnostics"] if item["status"] == "fail"]
        self.assertTrue(any(item["rule_id"] == "catalog.unsatisfied-requirement" for item in failures))

    def test_cli_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_policy(repo, lanes=["py"], disciplines=["validation", "testing"])
            stdout = io.StringIO()
            with patch.object(
                sys,
                "argv",
                [
                    "engineering-core",
                    "doctor",
                    "--repo",
                    str(repo),
                    "--format",
                    "json",
                    "--repo-root",
                    str(REPO_ROOT),
                    "--prefer-repo",
                ],
            ), redirect_stdout(stdout):
                main()
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["schema_version"], "1")
        self.assertEqual(report["summary"]["fail"], 0)


if __name__ == "__main__":
    unittest.main()
