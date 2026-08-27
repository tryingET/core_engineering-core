"""Tests for the pi skill projection (task 5099)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_skill_projection.py"
SKILLS_DIR = ROOT / "skills"

spec = importlib.util.spec_from_file_location("build_skill_projection", SCRIPT)
bsp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bsp)


class ProjectionTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        a = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(a.returncode, 0, a.stderr)
        snapshots = {p: p.read_bytes() for p in SKILLS_DIR.rglob("SKILL.md")}
        b = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(b.returncode, 0, b.stderr)
        after = {p: p.read_bytes() for p in SKILLS_DIR.rglob("SKILL.md")}
        self.assertEqual(
            {p.name for p in snapshots}, {p.name for p in after}
        )
        for path, payload in snapshots.items():
            self.assertEqual(payload, path.read_bytes(), f"nondeterministic: {path}")

    def test_every_catalog_lane_and_discipline_has_a_skill(self):
        catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        lane_ids = {entry["id"] for entry in catalog["lanes"] if entry.get("kind") == "lane"}
        discipline_ids = {entry["id"] for entry in catalog["disciplines"]}
        for lane in lane_ids:
            self.assertTrue(
                (SKILLS_DIR / f"ec-lane-{lane}" / "SKILL.md").is_file(),
                f"missing lane skill for {lane}",
            )
        for discipline in discipline_ids:
            self.assertTrue(
                (SKILLS_DIR / f"ec-discipline-{discipline}" / "SKILL.md").is_file(),
                f"missing discipline skill for {discipline}",
            )

    def test_frontmatter_is_valid_and_carries_triggers(self):
        for path in sorted(SKILLS_DIR.glob("ec-*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"missing frontmatter: {path}")
            header = text.split("---\n")[1]
            self.assertIn("name: ec-", header)
            self.assertIn("description: ", header)
            self.assertIn("Load when:", header, f"description lacks triggers: {path}")
            description_line = next(
                (line for line in header.splitlines() if line.startswith("description: ")), ""
            )
            self.assertTrue(description_line, f"missing description line: {path}")
            self.assertIn("[ec-", description_line)

    def test_body_budget_enforced(self):
        for path in sorted(SKILLS_DIR.glob("ec-*/SKILL.md")):
            size = path.stat().st_size
            self.assertLessEqual(
                size,
                bsp.MAX_BODY_BYTES + 2_000,
                f"skill exceeds budget: {path} ({size} bytes)",
            )

    def test_profiles_reference_existing_skills_only(self):
        profiles = json.loads((SKILLS_DIR / "profiles.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(profiles), 20)
        for profile, members in profiles.items():
            self.assertIsInstance(members, list)
            self.assertTrue(members, f"empty profile: {profile}")
            for member in members:
                self.assertTrue(
                    (SKILLS_DIR / member / "SKILL.md").is_file(),
                    f"profile {profile} references missing skill {member}",
                )

    def test_lane_profile_includes_default_disciplines(self):
        profiles = json.loads((SKILLS_DIR / "profiles.json").read_text(encoding="utf-8"))
        self.assertIn("ec-py", profiles)
        for discipline in bsp.DEFAULT_DISCIPLINES:
            self.assertIn(
                f"ec-discipline-{discipline}", profiles["ec-py"],
                f"ec-py profile missing default discipline {discipline}",
            )
        self.assertIn("ec-lane-py", profiles["ec-py"])
        self.assertIn("ec-defaults", profiles)


if __name__ == "__main__":
    unittest.main()
