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

from engineering_core import __version__
from engineering_core.cli import DISCIPLINES, LANES, TEMPLATES, main


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> str:
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["engineering-core", *args]), redirect_stdout(stdout):
            main()
        return stdout.getvalue()

    def test_list(self) -> None:
        output = self.run_cli("list")
        self.assertEqual(output.splitlines(), list(LANES))
        self.assertIn("ts", output)

    def test_list_disciplines(self) -> None:
        output = self.run_cli("list-disciplines")
        self.assertEqual(output.splitlines(), list(DISCIPLINES))
        self.assertIn("validation", output)
        for discipline in (
            "service-api",
            "ai-ml",
            "performance",
            "release-package",
            "data-governance",
            "domain-modeling",
            "design-patterns",
        ):
            self.assertIn(discipline, output.splitlines())

    def test_show_ts(self) -> None:
        output = self.run_cli("show", "ts", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("TypeScript engineering lane", output)

    def test_show_ts_frontend(self) -> None:
        output = self.run_cli("show", "ts-frontend", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Frontend Application Addendum", output)

    def test_show_rust_build_graph(self) -> None:
        output = self.run_cli("show", "rust-build-graph", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Rust Lane — Build Graph Acceleration Addendum", output)
        self.assertIn("Cargo remains", output)

    def test_show_discipline_validation(self) -> None:
        output = self.run_cli("show-discipline", "validation", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Discipline — Validation", output)

    def test_show_discipline_readme_prints_overview(self) -> None:
        output = self.run_cli("show-discipline", "README", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Engineering Core Disciplines", output)

    def test_show_discipline_build_graph(self) -> None:
        output = self.run_cli("show-discipline", "build-graph-acceleration", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Discipline — Build Graph Acceleration", output)
        self.assertIn("Buck2", output)
        self.assertIn("Bazel", output)

    def test_show_new_disciplines(self) -> None:
        expected = {
            "service-api": "Discipline — Service/API",
            "ai-ml": "Discipline — AI/ML",
            "performance": "Discipline — Performance",
            "release-package": "Discipline — Release and Package",
            "data-governance": "Discipline — Data Governance",
            "domain-modeling": "Discipline — Domain Modeling",
            "design-patterns": "Discipline — Design Patterns",
        }
        for discipline, heading in expected.items():
            with self.subTest(discipline=discipline):
                output = self.run_cli("show-discipline", discipline, "--repo-root", str(REPO_ROOT), "--prefer-repo")
                self.assertIn(heading, output)

    def test_design_patterns_lists_sixty_three_numbered_patterns(self) -> None:
        output = self.run_cli("show-discipline", "design-patterns", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        numbered_patterns = [line for line in output.splitlines() if line and line[0].isdigit() and ". **" in line]
        self.assertEqual(len(numbered_patterns), 63)
        self.assertIn("24. **Actor**", output)
        self.assertIn("63. **Policy Object**", output)

    def test_data_domain_docs_link_to_ak_architecture_with_wikilinks(self) -> None:
        convergence_link = (
            "[[~/ai-society/softwareco/owned/agent-kernel/docs/project/"
            "ai-society-convergence-architecture.md|AI Society Convergence Architecture]]"
        )
        vocabulary_link = (
            "[[~/ai-society/softwareco/owned/agent-kernel/docs/project/"
            "2026-04-25-layer-12-operator-vocabulary-boundary.md|Layer-12 Operator Vocabulary Boundary]]"
        )
        for discipline in ("data-governance", "domain-modeling"):
            with self.subTest(discipline=discipline):
                output = self.run_cli("show-discipline", discipline, "--repo-root", str(REPO_ROOT), "--prefer-repo")
                self.assertIn(convergence_link, output)
                self.assertIn(vocabulary_link, output)

    def test_catalog_disciplines_match_cli_and_files(self) -> None:
        catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        catalog_ids = [entry["id"] for entry in catalog["disciplines"]]
        self.assertEqual(catalog_ids, list(DISCIPLINES))
        for discipline in DISCIPLINES:
            self.assertTrue((REPO_ROOT / "src" / "engineering_core" / "disciplines" / f"{discipline}.md").exists())

    def test_packaged_catalog_disciplines_match_repo_catalog(self) -> None:
        repo_catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        package_catalog = json.loads((REPO_ROOT / "src" / "engineering_core" / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(repo_catalog["disciplines"], package_catalog["disciplines"])
        self.assertEqual(repo_catalog["profiles"], package_catalog["profiles"])

    def test_overview(self) -> None:
        output = self.run_cli("overview", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Engineering Core Disciplines", output)

    def test_catalog(self) -> None:
        output = self.run_cli("catalog", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn('"name": "engineering-core"', output)
        self.assertIn('"profiles"', output)

    def test_list_profiles(self) -> None:
        output = self.run_cli("list-profiles", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("browser-app", output.splitlines())

    def test_list_templates(self) -> None:
        output = self.run_cli("list-templates")
        self.assertEqual(output.splitlines(), list(TEMPLATES))
        self.assertIn("engineering-local", output)

    def test_show_template(self) -> None:
        output = self.run_cli("show-template", "validation-tier-map", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("Validation Tier Map", output)

    def test_template_path(self) -> None:
        output = self.run_cli("template-path", "engineering-local", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertEqual(output.strip(), str(REPO_ROOT / "templates" / "engineering.local.template.md"))

    def test_recommend(self) -> None:
        output = self.run_cli("recommend", "browser-app", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("# engineering-core recommendation: browser-app", output)
        self.assertIn("ts-frontend", output)
        self.assertIn("accessibility", output)

    def test_recommend_repo_prefers_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            policy_dir = repo / "policy"
            policy_dir.mkdir()
            (policy_dir / "engineering-lane.json").write_text(
                json.dumps(
                    {
                        "engineering_core": {
                            "lanes": [{"lane": "ts"}, {"lane": "ts-frontend"}],
                            "disciplines": ["validation", "accessibility"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            output = self.run_cli("recommend", "--repo", str(repo), "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertIn("# engineering-core recommendation: repo:", output)
        self.assertIn("ts-frontend", output)
        self.assertIn("accessibility", output)

    def test_scan_adoption_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = Path(tmp)
            repo = scope / "service"
            repo.mkdir()
            (repo / ".git").mkdir()
            output = self.run_cli(
                "scan-adoption",
                "--scope",
                str(scope),
                "--format",
                "json",
                "--repo-root",
                str(REPO_ROOT),
                "--prefer-repo",
            )
        scan = json.loads(output)
        self.assertEqual(scan["summary"]["total"], 1)
        self.assertEqual(scan["records"][0]["status"], "missing")

    def test_show_all_for_prints_lane_and_disciplines(self) -> None:
        output = self.run_cli(
            "show-all-for",
            "ts",
            "--with",
            "validation",
            "testing",
            "--repo-root",
            str(REPO_ROOT),
            "--prefer-repo",
        )
        self.assertIn("TypeScript engineering lane", output)
        self.assertIn("Discipline — Validation", output)
        self.assertIn("Discipline — Testing", output)

    def test_path(self) -> None:
        output = self.run_cli("path", "ts", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertEqual(output.strip(), str(REPO_ROOT / "lanes" / "engineering-ts.md"))

    def test_discipline_path(self) -> None:
        output = self.run_cli("discipline-path", "validation", "--repo-root", str(REPO_ROOT), "--prefer-repo")
        self.assertEqual(output.strip(), str(REPO_ROOT / "disciplines" / "validation.md"))

    def test_catalog_has_machine_readable_metadata(self) -> None:
        catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        for collection in ("lanes", "disciplines", "templates"):
            for entry in catalog[collection]:
                with self.subTest(collection=collection, entry=entry["id"]):
                    self.assertIn("kind", entry)
                    self.assertIn("category", entry)
                    self.assertIn("file", entry)
                    self.assertIn("description", entry)

    def test_version_matches_catalogs(self) -> None:
        root_catalog = json.loads((REPO_ROOT / "catalog.json").read_text(encoding="utf-8"))
        package_catalog = json.loads((REPO_ROOT / "src" / "engineering_core" / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(root_catalog["version"], __version__)
        self.assertEqual(package_catalog["version"], __version__)

    def test_no_legacy_cli_or_import_aliases(self) -> None:
        pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('engineering-core = "engineering_core.cli:main"', pyproject)
        self.assertNotIn('tech-stack-core', pyproject)
        self.assertFalse((REPO_ROOT / "src" / "tech_stack_core").exists())

    def test_version_matches_current_release(self) -> None:
        self.assertEqual(__version__, "0.3.3")


if __name__ == "__main__":
    unittest.main()
