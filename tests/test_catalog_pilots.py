from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.adoption import plan_init
from engineering_core.catalog_model import (
    collection_ids,
    load_catalog,
    validate_catalog,
)
from engineering_core.cli import main


class CatalogPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = load_catalog(REPO_ROOT, prefer_repo=True)

    def run_cli(self, *args: str) -> str:
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["engineering-core", *args]), redirect_stdout(stdout):
            main()
        return stdout.getvalue()

    def test_pilot_overlay_is_projected_and_valid(self) -> None:
        source = REPO_ROOT / "src" / "engineering_core" / "catalog.pilots.json"
        projection = REPO_ROOT / "catalog.pilots.json"
        self.assertEqual(source.read_bytes(), projection.read_bytes())
        self.assertEqual(
            validate_catalog(self.catalog, repo_root=REPO_ROOT, check_paths=True),
            [],
        )

    def test_pilot_ids_are_visible_through_catalog_driven_cli(self) -> None:
        lanes = collection_ids(self.catalog, "lanes")
        templates = collection_ids(self.catalog, "templates")
        self.assertIn("ts-ultracite-pilot", lanes)
        self.assertIn("ts-evidence-safety", lanes)
        self.assertIn("typescript-quality-pilot", templates)
        self.assertIn("ts-ultracite-pilot", self.run_cli("list"))
        self.assertIn("typescript-quality-pilot", self.run_cli("list-templates"))

    def test_profiles_close_lane_and_discipline_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = plan_init(
                Path(tmp),
                self.catalog,
                profile="typescript-high-assurance",
            )
        self.assertIn("ts", plan.lanes)
        self.assertIn("ts-evidence-safety", plan.lanes)
        self.assertIn("specification-and-dsls", plan.disciplines)
        self.assertIn("security-privacy", plan.disciplines)

    def test_pilot_docs_and_template_are_retrievable(self) -> None:
        self.assertIn(
            "Ultracite pilot addendum",
            self.run_cli("show", "ts-ultracite-pilot", "--repo-root", str(REPO_ROOT), "--prefer-repo"),
        )
        self.assertIn(
            "evidence-safety addendum",
            self.run_cli("show", "ts-evidence-safety", "--repo-root", str(REPO_ROOT), "--prefer-repo"),
        )
        self.assertIn(
            "TypeScript Quality Pilot",
            self.run_cli("show-template", "typescript-quality-pilot", "--repo-root", str(REPO_ROOT), "--prefer-repo"),
        )


if __name__ == "__main__":
    unittest.main()
