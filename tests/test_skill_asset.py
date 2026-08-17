from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillAssetTests(unittest.TestCase):
    def test_skill_projection_matches_packaged_source(self) -> None:
        source = ROOT / "src" / "engineering_core" / "skill" / "SKILL.md"
        projection = ROOT / "skills" / "engineering-core" / "SKILL.md"
        self.assertEqual(source.read_bytes(), projection.read_bytes())


if __name__ == "__main__":
    unittest.main()
