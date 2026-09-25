# ---
# summary: "Offline scenarios for non-ts lanes: each lane declares executable Quality gates and pinned config blocks, and its prose never contradicts them."
# read_when:
#   - "Changing the Quality gates, config blocks, or command guidance of the rust, py, go, cpp, elixir, or common-lisp lanes or their Justfile addenda."
#   - "Registering another lane in scripts/lane-conformance.py."
# ---

from __future__ import annotations

import re
import unittest

from test_lane_ts_configs import load_harness

HARNESS = load_harness()
LANES_DIR = HARNESS.ROOT / "src" / "engineering_core" / "lanes"


def lane_text(name: str) -> str:
    return (LANES_DIR / name).read_text(encoding="utf-8")


def backtick_commands(text: str, program: str) -> list[str]:
    """Inline `...` spans and fenced lines that invoke `program`."""
    spans = re.findall(r"`([^`\n]+)`", text)
    fenced = [line for block in re.findall(r"```[\w-]*\n(.*?)```", text, re.S) for line in block.splitlines()]
    return [c.strip() for c in spans + fenced if re.search(rf"(^|[\s;&|(]){re.escape(program)}\s", c.strip() + " ")]


class RustLaneFeature(unittest.TestCase):
    """Feature: a repo following the rust lane runs gates that cover the whole workspace on a pinned toolchain."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-rust.md")
        cls.addenda = lane_text("engineering-rust.justfile.md") + lane_text("engineering-rust.build-graph.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_declares_executable_gates(self) -> None:
        # Then the lane names every gate a conformant repo must pass
        for gate in ("toolchain", "fmt", "lint", "test", "supply-chain", "build"):
            self.command(gate)

    def test_scenario_gates_cover_workspace_members_and_the_lockfile(self) -> None:
        # When a workspace has a root package, cargo without --workspace skips members
        for program in ("clippy", "test", "build", "nextest"):
            for command in backtick_commands(self.doc + self.addenda, "cargo"):
                # (a bare `cargo test` names the tool; only invocations with arguments are commands)
                if command == f"cargo {program}" or "-p <crate>" in command:
                    continue
                if re.search(rf"\bcargo (\+\S+ )?{program}\b", command):
                    # Then every such command covers the workspace
                    self.assertIn("--workspace", command, command)
        for gate in ("lint", "test", "build"):
            self.assertIn("--locked", self.command(gate), gate)

    def test_scenario_format_gate_checks_instead_of_rewriting(self) -> None:
        self.assertIn("cargo fmt --all --check", self.command("fmt"))
        self.assertIn("cargo fmt --all --check", self.addenda)

    def test_scenario_toolchain_is_pinned(self) -> None:
        # Given rustup silently applies a nightly default when nothing is pinned
        block = self.blocks.get("rust-toolchain.toml", "")
        # Then the lane pins an exact stable channel with rustfmt and clippy
        channel = re.search(r'channel = "(\d+\.\d+\.\d+)"', block)
        self.assertIsNotNone(channel, "rust-toolchain.toml must pin an exact channel")
        self.assertIn('"rustfmt"', block)
        self.assertIn('"clippy"', block)
        self.assertIn(channel.group(1), self.command("toolchain"))

    def test_scenario_supply_chain_gate_has_its_config(self) -> None:
        self.assertIn("cargo deny check", self.command("supply-chain"))
        self.assertIn("deny.toml", self.blocks)
        self.assertRegex(self.command("toolchain"), r"cargo-deny \d+\.\d+\.\d+")

    def test_scenario_nextest_is_paired_with_doctests(self) -> None:
        # nextest does not run doctests
        self.assertIn("cargo test --workspace --doc --locked", self.doc)

    def test_scenario_build_graph_timings_start_cold(self) -> None:
        block = re.search(r"## Measure first.*?```bash\n(.*?)```", self.addenda, re.S).group(1)
        lines = [line for line in block.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            if line.startswith("time "):
                self.assertEqual(lines[index - 1], "cargo clean", line)


class GoLaneFeature(unittest.TestCase):
    """Feature: a repo following the go lane runs gates that fail on violations instead of rewriting or trusting caches."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-go.md")
        cls.justfile = lane_text("engineering-go.justfile.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_declares_executable_gates(self) -> None:
        for gate in ("toolchain", "fmt", "vet", "test", "build", "mod", "lint"):
            self.command(gate)

    def test_scenario_format_gate_fails_instead_of_rewriting(self) -> None:
        # When code is unformatted, `go fmt ./...` rewrites it and exits 0
        # Then the gate lists unformatted files and fails if any
        self.assertIn("gofmt -l", self.command("fmt"))
        self.assertNotIn("go fmt", self.command("fmt"))

    def test_scenario_module_gate_detects_drift_not_just_cache_tampering(self) -> None:
        # `go mod verify` passes with a missing or stale go.sum; tidy -diff catches drift
        self.assertIn("go mod tidy -diff", self.command("mod"))
        self.assertIn("go mod verify", self.command("mod"))
        self.assertIn("go mod tidy -diff", self.doc.split("**Quality gates:**")[0])

    def test_scenario_toolchain_and_linter_are_pinned(self) -> None:
        toolchain = re.search(r"^toolchain go(\d+\.\d+\.\d+)$", self.blocks.get("go.mod", ""), re.M)
        self.assertIsNotNone(toolchain, "go.mod block must pin `toolchain goX.Y.Z`")
        self.assertIn(toolchain.group(1).replace(".", r"\."), self.command("toolchain"))
        pin = re.search(r"golangci-lint@v(\d+\.\d+\.\d+)", self.blocks.get("Tool install", ""))
        self.assertIsNotNone(pin, "Tool install must pin golangci-lint")
        self.assertIn(f"version {pin.group(1)}", self.command("toolchain"))
        self.assertIn("version:", self.blocks.get(".golangci.yml", ""))

    def test_scenario_prose_matches_verified_command_behavior(self) -> None:
        self.assertRegex(self.doc, r"-fuzz=[^ `]+ -fuzztime=")
        self.assertIn("CGO_ENABLED=1", self.doc)
        # `go run ./cmd/...` fails once there is more than one command
        self.assertNotIn("go run ./cmd/...", self.justfile)
        # `gofmt -w .` also rewrites testdata/, so it must not be the recommended fixer
        self.assertNotIn("prefer: `gofmt -w .`", self.justfile)
        self.assertIn("prefer: `go fmt ./...`", self.justfile)


class PyLaneFeature(unittest.TestCase):
    """Feature: a repo following the py lane gets config uv actually reads and gates that run its pinned tools."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-py.md")
        cls.justfile = lane_text("engineering-py.justfile.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))
        cls.pyproject = HARNESS.tomllib.loads(cls.blocks.get("pyproject.toml", ""))

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_never_prescribes_config_uv_rejects(self) -> None:
        # Given uv has no task runner: [tool.uv.scripts] fails to parse and drops
        # every other project-level [tool.uv] setting
        # (prose may warn about it; no TOML block may prescribe it)
        for block in re.findall(r"```toml\n(.*?)```", self.doc + self.justfile, re.S):
            self.assertNotIn("[tool.uv.scripts]", block)
        self.assertNotIn("scripts", self.pyproject.get("tool", {}).get("uv", {}))
        # And the tasks it defined never existed: they may appear only in the warning paragraph
        warning = re.search(r"uv has no task runner\. Don't add.*?\n\n", self.doc, re.S)
        self.assertIsNotNone(warning, "the lane must warn that uv has no task runner")
        outside = self.doc.replace(warning.group(0), "") + self.justfile
        for task in ("uv run dev", "uv run test", "uv run lint", "uv run format"):
            self.assertNotIn(f"`{task}`", outside, task)

    def test_scenario_lane_declares_executable_gates(self) -> None:
        for gate in ("toolchain", "lint", "fmt", "typecheck", "test"):
            self.assertIn("--locked", self.command(gate), gate)
        self.assertIn("ruff format --check", self.command("fmt"))
        self.assertIn("ty check", self.command("typecheck"))

    def test_scenario_uv_config_problems_fail_instead_of_warning(self) -> None:
        # uv only warns about config it can't parse (and then ignores all project [tool.uv]
        # settings); it has no strict mode, so a gate must turn that warning into a failure
        config = self.command("config")
        self.assertIn("uv lock --check", config)
        self.assertIn("^warning:", config)
        # And the package-age quarantine travels with the project, not only ~/.config/uv
        self.assertEqual(self.pyproject["tool"]["uv"]["exclude-newer"], "7 days")

    def test_scenario_quality_tools_are_pinned_and_configured(self) -> None:
        dev = self.pyproject["dependency-groups"]["dev"]
        for tool in ("ruff", "ty", "pytest"):
            self.assertTrue(any(re.fullmatch(rf"{tool}==\d+\.\d+\.\d+", spec) for spec in dev), tool)
        tool = self.pyproject["tool"]
        self.assertIn("select", tool["ruff"]["lint"])
        # ty has no strict mode; the lane's strictness is explicit
        self.assertEqual(tool["ty"]["rules"]["all"], "error")
        self.assertTrue(tool["ty"]["terminal"]["error-on-warning"])
        self.assertIn(".python-version", self.blocks)

    def test_scenario_commands_match_verified_uv_behavior(self) -> None:
        self.assertIn("uv remove --dev pytest", self.doc)
        self.assertIn("granian[reload]", self.doc)
        self.assertIn("--interface asgi", self.doc)
        self.assertNotIn("(module paths don't work)", self.doc)
        self.assertIn("uv run python --version", self.justfile)
        self.assertIn("uv run ty check", self.justfile)


class CppLaneFeature(unittest.TestCase):
    """Feature: a repo following the cpp lane gets pinned tools, wired sanitizers, and a Justfile that can pass."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-cpp.md")
        cls.addendum = lane_text("engineering-cpp.justfile.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))
        cls.presets = HARNESS.json.loads(cls.blocks.get("CMakePresets.json", "{}"))
        cls.justfile = HARNESS.labeled_blocks(cls.addendum).get("Justfile", "")

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_declares_executable_gates(self) -> None:
        for gate in ("toolchain", "build-test", "sanitizers", "fmt", "tidy"):
            self.command(gate)

    def test_scenario_tools_are_pinned_and_verified(self) -> None:
        install = self.blocks.get("Tool install", "")
        for tool in ("cmake", "ninja", "clang-format", "clang-tidy"):
            pin = re.search(rf"\b{tool}==(\d+\.\d+\.\d+)", install)
            self.assertIsNotNone(pin, f"Tool install must pin {tool}")
            self.assertIn(pin.group(1), self.command("toolchain").replace("\\", ""), tool)

    def test_scenario_presets_make_warnings_tests_and_sanitizers_bite(self) -> None:
        configure = {p["name"]: p for p in self.presets["configurePresets"]}
        self.assertEqual(configure["ci"]["cacheVariables"]["CMAKE_COMPILE_WARNING_AS_ERROR"], "ON")
        self.assertIn("-fsanitize=address,undefined", configure["asan"]["cacheVariables"]["CMAKE_CXX_FLAGS"])
        for test in self.presets["testPresets"]:
            # ctest exits 0 when it finds no tests unless told otherwise
            self.assertEqual(test["execution"]["noTestsAction"], "error", test["name"])
        self.assertIn("WarningsAsErrors", self.blocks.get(".clang-tidy", ""))

    def test_scenario_format_check_never_reads_stdin(self) -> None:
        # With no matching files, `clang-format --dry-run` reads stdin (hang or silent pass)
        self.assertRegex(self.command("fmt"), r'\[ -z "\$files" \] \|\|')

    def test_scenario_reference_justfile_is_runnable(self) -> None:
        self.assertTrue(self.justfile, "addendum needs a **Justfile:** block")
        # just passes `$$` through to bash, where it expands to the shell PID
        self.assertNotIn("$$", self.justfile)
        # a lint recipe that echoes instead of failing is a silent pass
        self.assertNotIn("relying on compiler warnings", self.justfile)
        self.assertIn("--preset", self.justfile)


class ElixirLaneFeature(unittest.TestCase):
    """Feature: a repo following the elixir lane can run its own `mix ci` and ship with an image that exists."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-elixir.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))
        cls.mix = cls.blocks.get("mix.exs", "")

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_declares_executable_gates(self) -> None:
        for gate in ("toolchain", "deps", "fmt", "compile", "lint", "typecheck", "test", "ci"):
            self.command(gate)
        self.assertIn("--check-locked", self.command("deps"))
        self.assertIn("--warnings-as-errors", self.command("compile"))

    def test_scenario_ci_alias_runs_tests_in_the_test_env(self) -> None:
        # Without preferred_envs, `mix ci` aborts: "mix test" is running in the "dev" environment
        self.assertIn("defmodule", self.mix)
        self.assertRegex(self.mix, r"preferred_envs: \[ci: :test\]")

    def test_scenario_toolchain_pins_agree(self) -> None:
        versions = dict(line.split() for line in self.blocks.get(".tool-versions", "").splitlines() if line.strip())
        elixir = versions["elixir"].split("-otp-")[0]
        otp_major = versions["erlang"].split(".")[0]
        self.assertIn(f"Elixir {elixir} (compiled with Erlang/OTP {otp_major})", self.command("toolchain"))
        dockerfile = self.blocks.get("Dockerfile", "")
        self.assertIn(f"hexpm/elixir:{elixir}-erlang-{versions['erlang']}-", dockerfile)

    def test_scenario_docker_stages_share_one_debian_snapshot(self) -> None:
        dockerfile = self.blocks.get("Dockerfile", "")
        build = re.search(r"^FROM hexpm/elixir:\S+-debian-(\w+)-(\d{8}) AS build$", dockerfile, re.M)
        self.assertIsNotNone(build, "builder must pin a dated Debian image")
        self.assertIn(f"FROM debian:{build.group(1)}-{build.group(2)}-slim AS runner", dockerfile)
        self.assertIn("ENV MIX_ENV=prod", dockerfile)

    def test_scenario_snippets_use_current_apis(self) -> None:
        self.assertNotIn("Repo.transaction()", self.doc)
        self.assertIn("mix phx.gen.release --docker", self.doc)


class CommonLispLaneFeature(unittest.TestCase):
    """Feature: a repo following the common-lisp lane has gates that can actually fail."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = lane_text("engineering-common-lisp.md")
        cls.blocks = HARNESS.labeled_blocks(cls.doc)
        cls.gates = dict(HARNESS.quality_gates(cls.doc))

    def command(self, gate: str) -> str:
        self.assertIn(gate, self.gates, f"missing gate {gate}")
        return self.gates[gate][-1]

    def test_scenario_lane_declares_executable_gates(self) -> None:
        for gate in ("toolchain", "check", "test"):
            self.command(gate)

    def test_scenario_test_op_signals_failure(self) -> None:
        # asdf:test-system exits 0 on failing tests unless perform test-op signals an error
        asd = self.blocks.get("my-system.asd", "")
        self.assertRegex(asd, r"\(error \"my-system tests failed\"\)")

    def test_scenario_load_check_fails_on_deferred_warnings(self) -> None:
        # SBCL defers undefined-variable/function warnings past ASDF's failure hook
        check = self.blocks.get("scripts/check.lisp", "")
        self.assertIn("handler-bind", check)
        self.assertIn(":ignore-inherited-configuration", check)
        self.assertIn(":force", check)

    def test_scenario_gates_never_reuse_cached_fasls(self) -> None:
        for gate in ("check", "test"):
            self.assertIn('XDG_CACHE_HOME="$(mktemp -d)"', self.command(gate), gate)


if __name__ == "__main__":
    unittest.main()
