# ---
# summary: "Tests deterministic capability-scan population resolution, repository-list parsing, deduplication, bounds, and unsafe-input rejection."
# read_when:
#   - "Changing capability-scan population inputs, repository-list syntax, path safety, completeness, or repository limits."
# ---

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engineering_core.capability_scan import PopulationError, build_capability_scan, resolve_population


class CapabilityScanTests(unittest.TestCase):
    def test_deduplication_digest_and_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); good = root / "repo"; good.mkdir(); missing = root / "missing"
            population = resolve_population([good, good, missing], [])
            first = build_capability_scan(population)
            second = build_capability_scan(list(reversed(population)))
        self.assertEqual(first, second)
        self.assertEqual(first["population"]["count"], 2)
        self.assertEqual(first["completeness"], "partial")
        self.assertEqual(len(first["records"]), 1)

    def test_repo_file_relative_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "a").mkdir(); file = root / "repos.txt"
            file.write_text("# owner population\n\na\n")
            self.assertEqual(resolve_population([], [file]), [(root / "a").resolve()])

    def test_repo_file_symlink_and_control_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); target = root / "target"; target.write_text("x")
            link = root / "link"; link.symlink_to(target)
            with self.assertRaises(PopulationError): resolve_population([], [link])
            bad = root / "bad"; bad.write_bytes(b"a\x00b")
            with self.assertRaises(PopulationError): resolve_population([], [bad])

    def test_direct_and_repo_file_paths_reject_controls_and_overbound_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tabbed = root / "tabbed"; tabbed.write_text("a\tb\n")
            with self.assertRaises(PopulationError): resolve_population([], [tabbed])
            with self.assertRaises(PopulationError): resolve_population([Path("a\tb")], [])
            with self.assertRaises(PopulationError): build_capability_scan([Path("x" * 5000)])

    def test_population_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / str(i) for i in range(2)]
            with self.assertRaises(PopulationError): resolve_population(paths, [], max_repositories=1)


if __name__ == "__main__": unittest.main()
