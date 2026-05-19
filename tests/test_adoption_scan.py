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


def write_adoption(path: Path, *, lane: str = "ts", disciplines: list[str] | None = None) -> None:
    (path / "docs").mkdir(parents=True, exist_ok=True)
    (path / "policy").mkdir(parents=True, exist_ok=True)
    selected_disciplines = disciplines or ["validation", "testing", "security-privacy", "documentation", "dependency-governance", "observability"]
    (path / "docs" / "engineering.local.md").write_text(
        "# engineering.local\n\nCanonical local commands: run validation before handoff.\n",
        encoding="utf-8",
    )
    (path / "policy" / "engineering-lane.json").write_text(
        json.dumps(
            {
                "lane": lane,
                "engineering_core": {
                    "tool": "engineering-core",
                    "lane": lane,
                    "ref": "workspace-local-unpinned",
                    "catalog_command": "engineering-core catalog --pretty",
                    "list_disciplines_command": "engineering-core list-disciplines",
                    "list_templates_command": "engineering-core list-templates",
                    "disciplines": selected_disciplines,
                },
            }
        ),
        encoding="utf-8",
    )


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

    def test_missing_scope_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            with self.assertRaises(FileNotFoundError):
                build_scan([missing], catalog=load_catalog(REPO_ROOT, prefer_repo=True))

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
