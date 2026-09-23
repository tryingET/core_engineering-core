# ---
# summary: "Executable scenarios that install the ts lane's pinned tools and run its own gate scripts on a fixture; opt-in because they need Bun and a registry or warm cache."
# read_when:
#   - "Changing scripts/lane-conformance.py, its fixture, or the ts lane config blocks."
#   - "Wondering why these scenarios skip: set ENGINEERING_CORE_LANE_CONFORMANCE=1; release verify runs the harness directly."
# ---

from __future__ import annotations

import os
import shutil
import unittest

from test_lane_ts_configs import load_harness

ENABLED = os.environ.get("ENGINEERING_CORE_LANE_CONFORMANCE") == "1"


@unittest.skipUnless(ENABLED, "set ENGINEERING_CORE_LANE_CONFORMANCE=1 (needs bun); release verify runs it")
class TsLaneConformanceFeature(unittest.TestCase):
    """Feature: the ts lane's gates accept lane-conformant code and reject what they claim to reject."""

    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("bun") is None:
            raise AssertionError("ENGINEERING_CORE_LANE_CONFORMANCE=1 but bun is not on PATH")
        harness = load_harness()
        # Given the lane configs installed with their pinned tools
        cls.report = harness.run_lane(harness.LANES["ts"])

    def test_scenario_conformant_code_passes_every_gate(self) -> None:
        # When the lane gate scripts run on code that uses process.env["X"] and @/ aliases
        # Then every gate exits 0
        self.assertTrue(self.report.passes, self.report.render())
        self.assertTrue(all(result.ok for result in self.report.passes), self.report.render())

    def test_scenario_every_gate_rejects_its_probe(self) -> None:
        # When each gate runs on a probe that violates a rule it claims to enforce
        # Then that gate fails with the expected diagnostic, proving the config was loaded
        self.assertTrue(self.report.probes, self.report.render())
        self.assertTrue(all(result.ok for result in self.report.probes), self.report.render())


if __name__ == "__main__":
    unittest.main()
