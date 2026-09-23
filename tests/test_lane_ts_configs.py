# ---
# summary: "Offline scenarios proving the ts lane's documented configs are jointly satisfiable, exactly pinned, and locked for the conformance harness."
# read_when:
#   - "Changing the bunfig.toml, biome.json, tsconfig.json, or package.json blocks in the ts lane."
#   - "Changing scripts/lane-conformance.py or its committed fixture lock."
# ---

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = REPO_ROOT / "scripts" / "lane-conformance.py"


def load_harness():
    spec = importlib.util.spec_from_file_location("lane_conformance", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TsLaneConfigFeature(unittest.TestCase):
    """Feature: a repo that copies the ts lane configs verbatim can pass every lane gate."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.harness = load_harness()
        cls.lane = cls.harness.LANES["ts"]
        # Given the authoritative ts lane doc
        cls.files = cls.harness.extract_lane_files(cls.lane.doc.read_text(encoding="utf-8"))
        cls.tsconfig = json.loads(cls.harness.strip_line_comments(cls.files["tsconfig.json"]))
        cls.biome = json.loads(cls.files["biome.json"])
        cls.lane_package = json.loads(cls.files["package.json"])

    def test_scenario_biome_yields_to_index_signature_access(self) -> None:
        # When tsconfig requires obj["key"] for index signatures (TS4111)
        self.assertTrue(self.tsconfig["compilerOptions"]["noPropertyAccessFromIndexSignature"])
        # Then Biome must not demand obj.key for the same line
        self.assertEqual(self.biome["linter"]["rules"]["complexity"].get("useLiteralKeys"), "off")

    def test_scenario_biome_config_matches_its_exact_2x_pin(self) -> None:
        # When the lane documents a Biome config
        schema_version = self.biome["$schema"].split("/schemas/")[1].split("/")[0]
        # Then it uses the 2.x shape
        self.assertRegex(schema_version, r"^2\.\d+\.\d+$")
        self.assertNotIn("organizeImports", self.biome)
        self.assertNotIn("ignore", self.biome.get("files", {}))
        # And its schema equals the exact pinned Biome version
        self.assertEqual(self.lane_package["devDependencies"]["@biomejs/biome"], schema_version)

    def test_scenario_tsconfig_is_accepted_by_native_typescript(self) -> None:
        # When TypeScript 7's native tsc reads the lane tsconfig
        # Then no removed option (baseUrl, TS5102) is present
        self.assertNotIn("baseUrl", self.tsconfig["compilerOptions"])

    def test_scenario_bun_config_uses_the_file_bun_reads(self) -> None:
        # When a repo copies the lane's Bun install policy
        text = self.lane.doc.read_text(encoding="utf-8")
        # Then the block is named bunfig.toml, because Bun silently ignores bun.toml
        self.assertTrue("bunfig.toml" in self.files, "lane has no **bunfig.toml:** block")
        self.assertNotRegex(text, r"\*\*bun\.toml:\*\*")
        self.assertNotIn("`bun.toml`", text)

    def test_scenario_every_gate_tool_is_an_exact_dev_dependency(self) -> None:
        dev = self.lane_package["devDependencies"]
        scripts = self.lane_package["scripts"]
        for script in self.harness.GATE_SCRIPTS:
            # When a lane gate script invokes a tool binary
            for binary, package in self.harness.BINARY_PACKAGES.items():
                if re.search(rf"(^|[\s&]){re.escape(binary)}\s", scripts[script] + " "):
                    # Then the package providing it is a devDependency
                    self.assertIn(package, dev, f"{script} runs {binary} without {package}")
        # And every toolchain package is pinned to an exact version
        for package in self.harness.TOOLCHAIN_PACKAGES:
            self.assertRegex(dev.get(package, "missing"), r"^\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?$", package)

    def test_scenario_typecheck_uses_stable_native_typescript(self) -> None:
        # Given TypeScript 7 ships the native (Go) compiler as `tsc` and the
        # @typescript/native-preview (`tsgo`) channel stopped publishing
        dev = self.lane_package["devDependencies"]
        scripts = self.lane_package["scripts"]
        # Then the lane typechecks with typescript@7's tsc
        self.assertRegex(dev.get("typescript", "missing"), r"^7\.\d+\.\d+$")
        self.assertEqual(scripts["typecheck"], "tsc --noEmit")
        self.assertIn("tsc --noEmit", scripts["check"])
        # And carries no preview-era tooling or dual-compiler fallback
        self.assertNotIn("@typescript/native-preview", dev)
        self.assertNotIn("typecheck:fallback", scripts)
        # (the doc may still explain that tsgo was the preview name; it must not run it)
        self.assertNotIn("tsgo --noEmit", self.lane.doc.read_text(encoding="utf-8"))

    def test_scenario_pi_ts_lane_names_the_same_typechecker(self) -> None:
        # Given the pi-ts lane shares the TypeScript typecheck policy
        text = (self.lane.doc.parent / "engineering-pi-ts.md").read_text(encoding="utf-8")
        # Then it names typescript@7's tsc and never runs the retired tsgo preview
        self.assertNotIn("tsgo --noEmit", text)
        self.assertIn("`tsc --noEmit` from an exactly pinned `typescript@7`", text)

    def test_scenario_typescript_lanes_have_no_typescript6_fallback(self) -> None:
        for name in ("engineering-ts.md", "engineering-pi-ts.md"):
            text = (self.lane.doc.parent / name).read_text(encoding="utf-8")
            # When a dev tool only supports the classic (TypeScript 6) compiler API
            # Then the lane replaces the tool instead of routing it to TypeScript 6
            self.assertIn("TypeScript 7 only, no fallback", text, name)
            self.assertNotIn("tsc6", text, name)
            self.assertNotRegex(text, r"use it through `@typescript/typescript6`", name)
            # And runtime use of the compiler API never takes the `typescript` name
            self.assertIn("never under the name `typescript`", text, name)

    def test_scenario_committed_lock_matches_lane_pins(self) -> None:
        # Given the committed conformance lock
        lock_text = (self.lane.fixture / "bun.lock").read_text(encoding="utf-8")
        dev = self.lane_package["devDependencies"]
        for package in self.harness.TOOLCHAIN_PACKAGES:
            # Then it resolves each toolchain package to the lane pin
            self.assertIn(f'"{package}": ["{package}@{dev[package]}"', lock_text, package)


class LaneConformanceReleaseWiringFeature(unittest.TestCase):
    """Feature: every release proof executes lane conformance and can actually run it."""

    def test_scenario_release_verify_runs_the_harness(self) -> None:
        # Given the release proof command list
        text = (REPO_ROOT / "scripts" / "release-local.py").read_text(encoding="utf-8")
        # Then it runs the ts lane conformance harness
        self.assertIn('"scripts/lane-conformance.py", "ts"', text)

    def test_scenario_every_workflow_running_verify_installs_bun(self) -> None:
        for workflow in sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml")):
            text = workflow.read_text(encoding="utf-8")
            # When a workflow job runs the release proof
            for job in re.split(r"\n  (?=[\w-]+:\n)", text):
                if "release-local.py verify" in job:
                    # Then that job installs Bun first
                    self.assertIn("oven-sh/setup-bun@", job, f"{workflow.name} runs verify without bun")
                    self.assertLess(job.index("oven-sh/setup-bun@"), job.index("release-local.py verify"))


if __name__ == "__main__":
    unittest.main()
