"""Tests for the pi skill projection (task 5099)."""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_skill_projection.py"
SKILLS_DIR = ROOT / "skills"
# Agent Skills spec (enforced by Pi's validateName): lowercase a-z, 0-9, single hyphens.
SPEC_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

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
            # The emitter promises a JSON string, a YAML-compatible scalar.
            # Substring checks alone accepted invalid `[ec-lane] ...` YAML.
            description = json.loads(description_line.removeprefix("description: "))
            self.assertIsInstance(description, str)
            self.assertIn("[ec-", description)
            self.assertIn("Load when:", description)

    def test_description_scalar_round_trips_yaml_sensitive_text(self):
        descriptions = [
            '[ec-discipline] Release: packages # not a comment',
            'Quotes "double", \'single\', and C:\\packages\\release',
            'First line\nname: injected\n---\nsecond line',
            'Tabs\tand carriage returns\r remain description content',
            'Unicode: Grüße → release \u2028 next \u2029 paragraph',
            'true',
            '*alias',
            '{mapping: value}',
        ]
        for description in descriptions:
            with self.subTest(description=description):
                header = bsp.skill_front_matter("ec-discipline-release-package", description)
                lines = header.splitlines()
                self.assertEqual(len(lines), 4, "description escaped its scalar")
                self.assertEqual(lines[0], "---")
                self.assertEqual(lines[1], "name: ec-discipline-release-package")
                self.assertEqual(lines[3], "---")
                self.assertEqual(
                    json.loads(lines[2].removeprefix("description: ")), description
                )

    def test_body_budget_enforced(self):
        for path in sorted(SKILLS_DIR.glob("ec-*/SKILL.md")):
            size = path.stat().st_size
            self.assertLessEqual(
                size,
                bsp.MAX_BODY_BYTES + 2_000,
                f"skill exceeds budget: {path} ({size} bytes)",
            )

    def profile_interface(self):
        return json.loads((SKILLS_DIR / "profiles.json").read_text(encoding="utf-8"))

    def test_profile_interface_schema_and_members(self):
        document = self.profile_interface()
        self.assertEqual(document["schema"], bsp.PROFILE_SCHEMA)
        # The one-release dotted-profile aliases from 0.11.0 (AK5774) are gone (AK6002).
        self.assertEqual(document["deprecated_aliases"], {})
        self.assertEqual(bsp.validate_profile_interface(document), [])
        profiles = document["profiles"]
        self.assertGreaterEqual(len(profiles), 20)
        for profile, members in profiles.items():
            self.assertIsInstance(members, list)
            self.assertTrue(members, f"empty profile: {profile}")
            for member in members:
                self.assertTrue(
                    (SKILLS_DIR / member / "SKILL.md").is_file(),
                    f"profile {profile} references missing skill {member}",
                )

    def test_projected_skill_names_follow_the_agent_skills_spec(self):
        # Pi warns on (and stricter harnesses may skip) names with dots (AK5774)
        for skill in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            name = skill.parent.name
            with self.subTest(skill=name):
                self.assertRegex(name, SPEC_NAME)
                self.assertLessEqual(len(name), 64)
                front = skill.read_text(encoding="utf-8").split("---")[1]
                self.assertIn(f"\nname: {name}\n", front)

    def test_canonical_profile_names_follow_the_agent_skills_spec(self):
        document = self.profile_interface()
        for profile in document["profiles"]:
            self.assertRegex(profile, SPEC_NAME)
        for alias in document["deprecated_aliases"]:
            self.assertNotRegex(alias, SPEC_NAME, f"{alias} is spec-valid; no alias needed")

    def test_generator_prunes_and_check_reports_orphaned_projections(self):
        rendered, _ = bsp.render_projection()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "ec-lane-ts.justfile").mkdir()
            (out / "ec-lane-ts.justfile" / "SKILL.md").write_text("stale", encoding="utf-8")
            (out / "unrelated").mkdir()
            orphans = bsp.orphaned_projection_dirs(rendered, out)
            self.assertEqual([p.name for p in orphans], ["ec-lane-ts.justfile"])

    def test_published_v1_profile_keys_are_preserved(self):
        baseline = set(json.loads(
            (ROOT / "tests" / "fixtures" / "skill-profile-v1-keys.json").read_text()
        ))
        document = self.profile_interface()
        current = set(document["profiles"])
        # A published key keeps resolving: canonical, or a deprecated alias of one (AK5774)
        for key in baseline:
            resolved = key if key in current else document["deprecated_aliases"].get(key)
            self.assertIn(resolved, current, f"published profile {key!r} no longer resolves")
        self.assertIn("ec-defaults", current)
        self.assertIn("ec-full", current)

    def test_lane_profile_includes_default_disciplines(self):
        profiles = self.profile_interface()["profiles"]
        self.assertIn("ec-py", profiles)
        for discipline in bsp.DEFAULT_DISCIPLINES:
            self.assertIn(
                f"ec-discipline-{discipline}", profiles["ec-py"],
                f"ec-py profile missing default discipline {discipline}",
            )
        self.assertIn("ec-lane-py", profiles["ec-py"])
        self.assertIn("ec-defaults", profiles)

    def test_deprecated_alias_fixture_is_accepted_with_repo_profile_diagnostic(self):
        document = copy.deepcopy(self.profile_interface())
        document["deprecated_aliases"] = {"ec-python": "ec-py"}
        fleet = ROOT / "tests" / "fixtures" / "skill-profile-fleet-alias"
        problems, warnings = bsp.validate_fleet_references(fleet, document)
        self.assertEqual(problems, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("repo=", warnings[0])
        self.assertIn("profile='ec-python'", warnings[0])
        self.assertIn("use 'ec-py'", warnings[0])

    def test_missing_profile_fails_closed_with_repo_profile_diagnostic(self):
        fleet = ROOT / "tests" / "fixtures" / "skill-profile-fleet-missing"
        problems, warnings = bsp.validate_fleet_references(fleet, self.profile_interface())
        self.assertEqual(warnings, [])
        self.assertEqual(len(problems), 1)
        self.assertIn("repo=", problems[0])
        self.assertIn("profile='ec-does-not-exist'", problems[0])
        self.assertIn("unknown profile", problems[0])

    def test_check_accepts_fleet_root_override(self):
        fleet = ROOT / "tests" / "fixtures" / "skill-profile-fleet-valid"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check", "--fleet-root", str(fleet)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"fleet={fleet}", result.stdout)



if __name__ == "__main__":
    unittest.main()
