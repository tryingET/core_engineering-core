from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from engineering_core.catalog_model import (
    catalog_projection_matches,
    collection_ids,
    load_catalog,
    sync_catalog_projection,
    validate_catalog,
)


class CatalogModelTests(unittest.TestCase):
    def test_catalog_collections_match_cli_projection(self) -> None:
        from engineering_core.cli import DISCIPLINES, LANES, TEMPLATES

        catalog = load_catalog(REPO_ROOT, prefer_repo=True)
        self.assertEqual(set(LANES), set(collection_ids(catalog, "lanes")))
        self.assertEqual(set(DISCIPLINES), set(collection_ids(catalog, "disciplines")))
        self.assertEqual(set(TEMPLATES), set(collection_ids(catalog, "templates")))

    def test_repository_catalog_matches_canonical_projection(self) -> None:
        self.assertTrue(catalog_projection_matches(REPO_ROOT))

    def test_catalog_is_structurally_valid(self) -> None:
        catalog = load_catalog(REPO_ROOT, prefer_repo=True)
        self.assertEqual(validate_catalog(catalog, repo_root=REPO_ROOT, check_paths=True), [])

    def test_unknown_profile_reference_is_reported(self) -> None:
        catalog = json.loads(json.dumps(load_catalog(REPO_ROOT, prefer_repo=True)))
        catalog["profiles"][0]["lanes"].append("missing-lane")
        errors = validate_catalog(catalog)
        self.assertIn("catalog.unknown-profile-lane:browser-app:missing-lane", errors)

    def test_sync_projection_is_checkable_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = root / "src" / "engineering_core" / "catalog.json"
            canonical.parent.mkdir(parents=True)
            shutil.copyfile(REPO_ROOT / "src" / "engineering_core" / "catalog.json", canonical)
            (root / "catalog.json").write_text("{}\n", encoding="utf-8")
            self.assertTrue(sync_catalog_projection(root, apply=False))
            self.assertTrue(sync_catalog_projection(root, apply=True))
            self.assertFalse(sync_catalog_projection(root, apply=False))


if __name__ == "__main__":
    unittest.main()
