# ---
# summary: "Exercises adoption discovery, structural and semantic status, repository budgets, package surfaces, and loop-validation contracts."
# read_when:
#   - "Changing adoption-scan discovery, status taxonomy, budget accounting, package handling, or loop-validation reporting."
# ---

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.adoption_scan import build_scan, load_catalog


def mark_git(path: Path) -> None:
    (path / ".git").mkdir(parents=True)


def write_adoption(
    path: Path,
    *,
    lane: str = "ts",
    disciplines: list[str] | None = None,
    loop_validation: object | None = None,
) -> None:
    (path / "docs").mkdir(parents=True, exist_ok=True)
    (path / "policy").mkdir(parents=True, exist_ok=True)
    selected_disciplines = disciplines or ["validation", "testing", "security-privacy", "documentation", "dependency-governance", "observability"]
    engineering_core = {
        "tool": "engineering-core",
        "lane": lane,
        "ref": "workspace-local-unpinned",
        "catalog_command": "engineering-core catalog --pretty",
        "list_disciplines_command": "engineering-core list-disciplines",
        "list_templates_command": "engineering-core list-templates",
        "disciplines": selected_disciplines,
    }
    if loop_validation is not None:
        engineering_core["loop_validation"] = loop_validation
    (path / "docs" / "engineering.local.md").write_text(
        "# engineering.local\n\nCanonical local commands: run validation before handoff.\n",
        encoding="utf-8",
    )
    (path / "policy" / "engineering-lane.json").write_text(
        json.dumps(
            {
                "lane": lane,
                "engineering_core": engineering_core,
            }
        ),
        encoding="utf-8",
    )


def complete_loop_validation(**overrides: str) -> dict[str, object]:
    commands = {
        "loop-doctor": "just loop-doctor",
        "loop-verify-fast": "just loop-verify-fast",
        "loop-impact-plan": "just loop-impact-plan",
        "loop-impact-run": "just loop-impact-run",
        "loop-impact-wide": "just loop-impact-wide",
        "loop-landing-check": "just loop-landing-check",
    }
    commands.update(overrides)
    return {
        "version": "repo-loop-validation-v1",
        "contract_doc": "docs/engineering.local.md#repo-loop-validation",
        "commands": commands,
    }


class AdoptionScanTests(unittest.TestCase):
    def test_scan_missing_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["summary"]["total"], 1)
        self.assertEqual(scan["records"][0]["status"], "missing")

    def test_scan_adopted_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo)
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["summary"]["status_counts"], {"adopted": 1})
        self.assertEqual(scan["summary"]["semantic_status_counts"], {"ok": 1})
        self.assertEqual(scan["summary"]["loop_validation_status_counts"], {"absent": 1})
        self.assertEqual(scan["records"][0]["loop_validation_status"], "absent")

    def test_loop_validation_complete_contract_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, loop_validation=complete_loop_validation())
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        record = scan["records"][0]
        self.assertEqual(record["status"], "adopted")
        self.assertEqual(record["loop_validation_status"], "complete")
        self.assertEqual(scan["summary"]["loop_validation_status_counts"], {"complete": 1})
        self.assertEqual(record["loop_validation_missing_commands"], [])

    def test_loop_validation_explicit_na_counts_as_mapped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, loop_validation=complete_loop_validation(**{"loop-impact-wide": "n/a: wide validation belongs to CI"}))
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["records"][0]["loop_validation_status"], "complete")

    def test_loop_validation_partial_contract_is_review_candidate(self) -> None:
        loop_validation = complete_loop_validation()
        commands = loop_validation["commands"]
        assert isinstance(commands, dict)
        commands.pop("loop-impact-wide")
        commands.pop("loop-landing-check")
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, loop_validation=loop_validation)
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        record = scan["records"][0]
        self.assertEqual(record["loop_validation_status"], "partial")
        self.assertEqual(record["loop_validation_missing_commands"], ["loop-impact-wide", "loop-landing-check"])
        self.assertEqual(scan["review_candidates"][0]["path"], "service")

    def test_loop_validation_unknown_version_is_review_candidate(self) -> None:
        loop_validation = complete_loop_validation()
        loop_validation["version"] = "repo-loop-validation-v0"
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, loop_validation=loop_validation)
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["records"][0]["loop_validation_status"], "unknown-version")
        self.assertIn("unknown loop validation version", scan["records"][0]["notes"][0])
        self.assertEqual(scan["review_candidates"][0]["path"], "service")

    def test_loop_validation_malformed_shape_is_invalid_loop_validation_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, loop_validation=["not", "an", "object"])
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        record = scan["records"][0]
        self.assertEqual(record["status"], "adopted")
        self.assertEqual(record["loop_validation_status"], "invalid")
        self.assertIn("loop_validation must be an object", record["notes"])

    def test_scan_invalid_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            (repo / "docs").mkdir()
            (repo / "policy").mkdir()
            (repo / "docs" / "engineering.local.md").write_text("# engineering.local\n", encoding="utf-8")
            (repo / "policy" / "engineering-lane.json").write_text("", encoding="utf-8")
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["records"][0]["status"], "invalid-policy")
        self.assertIn("invalid json", scan["records"][0]["notes"][0])

    def test_scan_non_object_policy_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            (repo / "docs").mkdir()
            (repo / "policy").mkdir()
            (repo / "docs" / "engineering.local.md").write_text("# engineering.local\n", encoding="utf-8")
            (repo / "policy" / "engineering-lane.json").write_text("[]", encoding="utf-8")
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["records"][0]["status"], "invalid-policy")
        self.assertIn("invalid json type", scan["records"][0]["notes"][0])

    def test_scan_single_repo_scope_auto_includes_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            mark_git(repo)
            scan = build_scan([repo], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["summary"]["total"], 1)
        self.assertEqual(scan["records"][0]["path"], ".")

    def test_missing_scope_is_isolated_and_reported_partial(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            scan = build_scan([missing], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["completeness"], "partial")
        self.assertEqual(scan["summary"]["total"], 0)
        self.assertIn("does not exist", scan["failures"][0]["reason"])

    def test_repository_budget_reports_omission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            for name in ("a", "b"):
                repo = scope / name
                repo.mkdir()
                mark_git(repo)
            scan = build_scan([scope], max_repositories=1, catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["completeness"], "partial")
        self.assertEqual(scan["summary"]["repos"], 1)
        self.assertEqual(scan["omissions"][0]["reason"], "repository budget reached")

    def test_package_discovery_consumes_shared_file_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            package = repo / "packages" / "api"
            package.mkdir(parents=True)
            mark_git(repo)
            write_adoption(package)
            scan = build_scan(
                [scope], include_packages=True, max_files=1,
                catalog=load_catalog(REPO_ROOT, prefer_repo=True),
            )
        self.assertEqual(scan["completeness"], "partial")
        self.assertLessEqual(scan["usage"]["files"], 1)
        self.assertTrue(any("package discovery" in item["reason"] for item in scan["omissions"]))

    def test_read_budget_counts_policy_and_semantic_document_reads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo)
            policy_size = (repo / "policy" / "engineering-lane.json").stat().st_size
            scan = build_scan(
                [scope], max_read_bytes=policy_size,
                catalog=load_catalog(REPO_ROOT, prefer_repo=True),
            )
        self.assertEqual(scan["completeness"], "partial")
        self.assertEqual(scan["usage"]["read_bytes"], policy_size)
        self.assertEqual(scan["usage"]["repositories"], 1)
        self.assertEqual(scan["summary"]["repos"], 0)
        self.assertIn("read-byte budget reached", scan["omissions"][0]["reason"])

    def test_scan_legacy_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            (repo / "docs").mkdir()
            (repo / "policy").mkdir()
            (repo / "docs" / "tech-stack.local.md").write_text("legacy", encoding="utf-8")
            (repo / "policy" / "stack-lane.json").write_text("{}", encoding="utf-8")
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["records"][0]["status"], "legacy-only")

    def test_include_packages_finds_doc_only_member_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "monorepo"
            package = repo / "packages" / "ui"
            package.mkdir(parents=True)
            mark_git(repo)
            write_adoption(repo)
            (package / "docs").mkdir(parents=True)
            (package / "docs" / "engineering.local.md").write_text(
                "# engineering.local\n\nCanonical local commands: validate package.\n",
                encoding="utf-8",
            )
            scan_without = build_scan([scope], include_packages=False, catalog=load_catalog(REPO_ROOT, prefer_repo=True))
            scan_with = build_scan([scope], include_packages=True, catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan_without["summary"]["total"], 1)
        self.assertEqual(scan_with["summary"]["total"], 2)
        package_record = [record for record in scan_with["records"] if record["kind"] == "package"][0]
        self.assertEqual(package_record["status"], "doc-only")

    def test_include_packages_requires_exact_surface_path_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "monorepo"
            false_surface = repo / "packages" / "ui" / "foopolicy"
            false_surface.mkdir(parents=True)
            mark_git(repo)
            write_adoption(repo)
            (false_surface / "engineering-lane.json").write_text("{}", encoding="utf-8")
            scan = build_scan([scope], include_packages=True, catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        self.assertEqual(scan["summary"]["packages"], 0)

    def test_include_packages_suppresses_nested_surfaces_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "monorepo"
            package = repo / "packages" / "ui"
            nested = package / "src" / "component"
            nested.mkdir(parents=True)
            mark_git(repo)
            write_adoption(repo)
            for root in (package, nested):
                (root / "docs").mkdir(parents=True)
                (root / "docs" / "engineering.local.md").write_text("# engineering.local\n", encoding="utf-8")
            scan = build_scan([scope], include_packages=True, catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        packages = [record for record in scan["records"] if record["kind"] == "package"]
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0]["path"], "monorepo/packages/ui")

    def test_unknown_lane_and_discipline_are_structural_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            mark_git(repo)
            write_adoption(repo, lane="unknown-lane", disciplines=["validation", "unknown-discipline"])
            scan = build_scan([scope], catalog=load_catalog(REPO_ROOT, prefer_repo=True))
        record = scan["records"][0]
        self.assertEqual(record["status"], "partial")
        self.assertIn("unknown lane(s): unknown-lane", record["structural_notes"])
        self.assertIn("unknown discipline(s): unknown-discipline", record["structural_notes"])


if __name__ == "__main__":
    unittest.main()
