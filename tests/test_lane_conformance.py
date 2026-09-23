# ---
# summary: "Executable scenarios that install each registered lane's pinned tools and run its own gates on a fixture; opt-in because they need the lane toolchains."
# read_when:
#   - "Changing scripts/lane-conformance.py, its fixtures, or any lane's config blocks or Quality gates."
#   - "Wondering why these scenarios skip: set ENGINEERING_CORE_LANE_CONFORMANCE=1; release verify runs the harness directly."
# ---

from __future__ import annotations

import os
import shutil
import unittest

from test_lane_ts_configs import load_harness

ENABLED = os.environ.get("ENGINEERING_CORE_LANE_CONFORMANCE") == "1"


@unittest.skipUnless(ENABLED, "set ENGINEERING_CORE_LANE_CONFORMANCE=1 (needs lane toolchains); release verify runs it")
class LaneConformanceFeature(unittest.TestCase):
    """Feature: every lane's gates accept lane-conformant code and reject what they claim to reject."""

    def test_scenario_each_lane_passes_conformant_code_and_rejects_its_probes(self) -> None:
        harness = load_harness()
        for lane_id, lane in sorted(harness.LANES.items()):
            with self.subTest(lane=lane_id):
                missing = [tool for tool in lane.tools if shutil.which(tool) is None]
                self.assertFalse(missing, f"ENGINEERING_CORE_LANE_CONFORMANCE=1 but {lane_id} needs {missing}")
                # Given the lane configs installed with their pinned tools
                report = harness.run_lane(lane)
                # Then every gate passes conformant code without diagnostics
                self.assertTrue(report.passes, report.render())
                self.assertTrue(all(result.ok for result in report.passes), report.render())
                # And every probe fails its gate with the expected diagnostic, proving the config was loaded
                self.assertTrue(report.probes, report.render())
                self.assertTrue(all(result.ok for result in report.probes), report.render())


if __name__ == "__main__":
    unittest.main()
