#!/usr/bin/env python3
# ---
# summary: "Executes a lane's documented config blocks with their pinned tools: conformant fixture code must pass every gate script and each probe must fail its gate."
# read_when:
#   - "Changing config blocks (bunfig.toml, biome.json, tsconfig.json, package.json) in a lane doc covered here."
#   - "Bumping a lane tool pin: run with --update-lock, then without, and commit the fixture lock."
#   - "Adding executable conformance for another lane."
# ---
"""Lane config conformance harness.

The lane doc is the source of truth; this harness extracts its fenced config
blocks verbatim, installs the exact pinned tools from a committed lock
(--frozen-lockfile --ignore-scripts), and runs the lane's own package.json gate
scripts. Pass cases prove conformant code is accepted; probes prove each gate
actually enforces what the lane claims (a config that silently fails to load
would otherwise pass). See docs/project/2026-09-23-lane-config-conformance-greats.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_SCRIPTS = ("typecheck", "check")
BINARY_PACKAGES = {"biome": "@biomejs/biome", "tsc": "typescript"}
TOOLCHAIN_PACKAGES = ("@biomejs/biome", "typescript", "@types/bun")
CONFIG_BLOCKS = ("bunfig.toml", "biome.json", "tsconfig.json")
EXPECT = re.compile(r"^(?://|#|;+|%) expect: (\S+) (.+?)\s*$", re.MULTILINE)
# Any rule diagnostic, including info severity: an exit-0 gate that still advises
# rewriting conformant code (e.g. useLiteralKeys vs TS4111) is not clean.
LINT_DIAGNOSTIC = re.compile(r"\blint/\w+/\w+")


class LaneContractError(Exception):
    """The lane doc lacks or malforms a block the harness executes."""


@dataclass
class Result:
    scenario: str
    ok: bool
    detail: str = ""


@dataclass
class Report:
    lane_id: str
    passes: list[Result] = field(default_factory=list)
    probes: list[Result] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return bool(self.passes) and bool(self.probes) and all(r.ok for r in self.passes + self.probes)

    def render(self) -> str:
        lines = [f"Feature: {self.lane_id} lane configs pass their own gates"]
        for result in self.passes + self.probes:
            lines.append(f"  Scenario: {result.scenario} ... {'PASS' if result.ok else 'FAIL'}")
            if not result.ok and result.detail:
                lines.extend(f"    | {line}" for line in result.detail.strip().splitlines()[-25:])
        return "\n".join(lines)


def extract_lane_files(doc_text: str) -> dict[str, str]:
    files: dict[str, str] = {}
    for name in CONFIG_BLOCKS:
        match = re.search(rf"\*\*{re.escape(name)}:\*\*\n```\w*\n(.*?)```", doc_text, re.S)
        if match:
            files[name] = match.group(1)
    match = re.search(r"### \*\*Package\.json Scripts\*\*\n\n```json\n(.*?)```", doc_text, re.S)
    if match:
        files["package.json"] = match.group(1)
    return files


def labeled_blocks(doc_text: str) -> dict[str, str]:
    """Every `**<label>:**` immediately followed by a fenced block, keyed by label."""
    return {
        match.group(1): match.group(2)
        for match in re.finditer(r"^\*\*([^*\n]+?):\*\*\n```[\w-]*\n(.*?)```", doc_text, re.S | re.M)
    }


def quality_gates(doc_text: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Parse the lane's `**Quality gates:**` block: `# <name>` lines, each followed by one command."""
    block = labeled_blocks(doc_text).get("Quality gates")
    if block is None:
        raise LaneContractError("lane doc lacks a **Quality gates:** block")
    gates: list[tuple[str, tuple[str, ...]]] = []
    name: str | None = None
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            name = line.lstrip("#").strip()
            continue
        if name is None:
            raise LaneContractError(f"quality gate command without a `# name` line: {line}")
        # Run exactly as a reader pasting the ```bash block would.
        gates.append((name, ("bash", "-o", "pipefail", "-c", line)))
        name = None
    if not gates:
        raise LaneContractError("**Quality gates:** block declares no gates")
    return tuple(gates)


def write_labeled_files(doc_text: str, work: Path, names: tuple[str, ...]) -> None:
    blocks = labeled_blocks(doc_text)
    missing = [name for name in names if name not in blocks]
    if missing:
        raise LaneContractError(f"lane doc lacks config blocks: {', '.join(missing)}")
    for name in names:
        (work / name).write_text(blocks[name], encoding="utf-8")


def strip_line_comments(jsonc: str) -> str:
    return "\n".join(line for line in jsonc.splitlines() if not line.strip().startswith("//"))


def conformance_package(lane_package_text: str) -> dict:
    lane_package = json.loads(lane_package_text)
    dev = lane_package.get("devDependencies", {})
    missing = [package for package in TOOLCHAIN_PACKAGES if package not in dev]
    if missing:
        raise LaneContractError(f"lane package.json lacks toolchain devDependencies: {', '.join(missing)}")
    return {
        "name": "lane-conformance",
        "private": True,
        "type": "module",
        "scripts": {script: lane_package["scripts"][script] for script in GATE_SCRIPTS},
        "devDependencies": {package: dev[package] for package in TOOLCHAIN_PACKAGES},
    }


def run(args: list[str] | tuple[str, ...], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, text=True, capture_output=True, check=False, env=env)


LEAKY_ENV = frozenset({"VIRTUAL_ENV", "CONDA_PREFIX", "PYTHONPATH", "PYTHONHOME", "UV_PROJECT_ENVIRONMENT"})


def tool_cache_root() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "engineering-core" / "lane-tools"


def install_tools(lane: Lane, work: Path, doc_text: str) -> tuple[dict[str, str], subprocess.CompletedProcess[str] | None]:
    """Run the doc's `**Tool install:**` block once per content hash into a cache; put its bin first on PATH."""
    # Gates must not inherit the caller's interpreter selection (e.g. engineering-core's own
    # venv when run via `uv run`): that would test the harness environment, not the lane.
    env = {key: value for key, value in os.environ.items() if key not in LEAKY_ENV}
    block = labeled_blocks(doc_text).get("Tool install")
    if block is None:
        return env, None
    cache = tool_cache_root() / f"{lane.lane_id}-{hashlib.sha256(block.encode()).hexdigest()[:16]}"
    env.update({
        "GOBIN": str(cache / "bin"),
        "CARGO_INSTALL_ROOT": str(cache),
        "UV_TOOL_DIR": str(cache / "uv-tools"),
        "UV_TOOL_BIN_DIR": str(cache / "bin"),
        "PATH": f"{cache / 'bin'}{os.pathsep}{env.get('PATH', '')}",
    })
    if (cache / ".installed").exists():
        return env, None
    (cache / "bin").mkdir(parents=True, exist_ok=True)
    # Installed from the work dir so pinned toolchain files (rust-toolchain.toml) apply.
    proc = run(["bash", "-o", "pipefail", "-c", block], work, env)
    if proc.returncode == 0:
        (cache / ".installed").write_text(block, encoding="utf-8")
    return env, proc


@dataclass(frozen=True)
class Lane:
    """One lane's executable contract: how to build a project from its doc, and its gates."""

    lane_id: str
    doc: Path
    fixture: Path
    tools: tuple[str, ...]
    prepare: Callable[[Lane, Path, str], None]
    # Static gates, or a function deriving them from the (possibly mutated) doc text.
    gates: tuple[tuple[str, tuple[str, ...]], ...] | Callable[[str], tuple[tuple[str, tuple[str, ...]], ...]]
    probe_suffix: str
    probe_dir: str
    install: Callable[[Lane, Path], subprocess.CompletedProcess[str]] | None = None
    refresh_lock: Callable[[Lane], None] | None = None
    clean: re.Pattern[str] | None = None

    def gates_for(self, doc_text: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
        return self.gates(doc_text) if callable(self.gates) else self.gates


def write_project(lane: Lane, work: Path, doc_text: str, *, with_bunfig: bool) -> None:
    files = extract_lane_files(doc_text)
    missing = [name for name in (*CONFIG_BLOCKS, "package.json") if name not in files]
    if missing:
        raise LaneContractError(f"{lane.doc.name} lacks config blocks: {', '.join(missing)}")
    for name in ("biome.json", "tsconfig.json"):
        (work / name).write_text(files[name], encoding="utf-8")
    if with_bunfig:
        (work / "bunfig.toml").write_text(files["bunfig.toml"], encoding="utf-8")
    package = conformance_package(files["package.json"])
    (work / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")


def prepare_ts(lane: Lane, work: Path, doc_text: str) -> None:
    write_project(lane, work, doc_text, with_bunfig=True)
    shutil.copy(lane.fixture / "bun.lock", work / "bun.lock")


def install_ts(lane: Lane, work: Path) -> subprocess.CompletedProcess[str]:
    return run(["bun", "install", "--frozen-lockfile", "--ignore-scripts"], work)


PROBE_EXPECT_FILE = "expect"


def use_sources(lane: Lane, work: Path, probe: Path | None) -> None:
    """Reset the fixture sources, then apply a probe: a file lands in probe_dir, a directory overlays the root."""
    for entry in (lane.fixture / "pass").iterdir():
        target = work / entry.name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    # shutil.copy (not copy2) gives every file a fresh mtime, so incremental build tools
    # (cargo fingerprints, mix) never trust a cached result from a previous probe.
    shutil.copytree(lane.fixture / "pass", work, dirs_exist_ok=True, copy_function=shutil.copy)
    if probe is None:
        return
    if probe.is_dir():
        shutil.copytree(
            probe, work, dirs_exist_ok=True, copy_function=shutil.copy,
            ignore=shutil.ignore_patterns(PROBE_EXPECT_FILE),
        )
    else:
        (work / lane.probe_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(probe, work / lane.probe_dir / probe.name)


def probe_expectations(probe: Path) -> list[tuple[str, str]]:
    source = probe / PROBE_EXPECT_FILE if probe.is_dir() else probe
    return EXPECT.findall(source.read_text(encoding="utf-8")) if source.exists() else []


def run_lane(lane: Lane, *, doc_text: str | None = None, keep: bool = False) -> Report:
    doc_text = doc_text if doc_text is not None else lane.doc.read_text(encoding="utf-8")
    report = Report(lane.lane_id)
    work = Path(tempfile.mkdtemp(prefix=f"lane-conformance-{lane.lane_id}-"))
    try:
        lane.prepare(lane, work, doc_text)
        env, tool_install = install_tools(lane, work, doc_text)
        if tool_install is not None and tool_install.returncode != 0:
            report.passes.append(Result(
                "pinned tools install from the lane's **Tool install:** block",
                False, tool_install.stdout + tool_install.stderr,
            ))
            return report
        if lane.install is not None:
            install = lane.install(lane, work)
            if install.returncode != 0:
                report.passes.append(Result(
                    "pinned tools install from the committed lock (rerun with --update-lock after a pin change)",
                    False, install.stdout + install.stderr,
                ))
                return report
        gates = lane.gates_for(doc_text)
        use_sources(lane, work, None)
        for name, argv in gates:
            proc = run(argv, work, env)
            output = proc.stdout + proc.stderr
            clean = lane.clean is None or not lane.clean.search(output)
            report.passes.append(Result(
                f"conformant code passes `{name}` without diagnostics", proc.returncode == 0 and clean, output,
            ))
        probes = [p for p in sorted((lane.fixture / "probes").iterdir()) if p.is_dir() or p.suffix == lane.probe_suffix]
        for probe in probes:
            expectations = probe_expectations(probe)
            if not expectations:
                report.probes.append(Result(f"probe {probe.name} declares expectations", False))
                continue
            # Re-prepare first: a directory probe may overwrite a doc-derived file (go.mod, deny.toml).
            lane.prepare(lane, work, doc_text)
            use_sources(lane, work, probe)
            for name, needle in expectations:
                argv = dict(gates).get(name)
                if argv is None:
                    report.probes.append(Result(f"probe {probe.name} names a known gate ({name})", False))
                    continue
                proc = run(argv, work, env)
                output = proc.stdout + proc.stderr
                report.probes.append(Result(
                    f"`{name}` rejects {probe.name} with {needle}",
                    proc.returncode != 0 and needle in output, output,
                ))
        return report
    finally:
        if keep:
            print(f"kept work dir: {work}", file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)


def refresh_ts_lock(lane: Lane) -> None:
    with tempfile.TemporaryDirectory(prefix=f"lane-conformance-{lane.lane_id}-lock-") as tmp:
        work = Path(tmp)
        # bunfig.toml sets frozenLockfile; write it only for verification runs.
        write_project(lane, work, lane.doc.read_text(encoding="utf-8"), with_bunfig=False)
        proc = run(["bun", "install", "--ignore-scripts"], work)
        if proc.returncode != 0:
            raise SystemExit(proc.stdout + proc.stderr)
        shutil.copy(work / "bun.lock", lane.fixture / "bun.lock")
    print(f"updated {(lane.fixture / 'bun.lock').relative_to(ROOT)}")


def prepare_from_blocks(*names: str) -> Callable[[Lane, Path, str], None]:
    def prepare(lane: Lane, work: Path, doc_text: str) -> None:
        write_labeled_files(doc_text, work, names)

    return prepare


def prepare_py(lane: Lane, work: Path, doc_text: str) -> None:
    write_labeled_files(doc_text, work, ("pyproject.toml", ".python-version"))
    shutil.copy(lane.fixture / "uv.lock", work / "uv.lock")


def refresh_py_lock(lane: Lane) -> None:
    with tempfile.TemporaryDirectory(prefix="lane-conformance-py-lock-") as tmp:
        work = Path(tmp)
        write_labeled_files(lane.doc.read_text(encoding="utf-8"), work, ("pyproject.toml", ".python-version"))
        proc = run(["uv", "lock"], work)
        if proc.returncode != 0:
            raise SystemExit(proc.stdout + proc.stderr)
        shutil.copy(work / "uv.lock", lane.fixture / "uv.lock")
    print(f"updated {(lane.fixture / 'uv.lock').relative_to(ROOT)}")


LANES_DIR = ROOT / "src" / "engineering_core" / "lanes"
FIXTURES = ROOT / "tests" / "fixtures" / "lane-conformance"
# Toolchain notes and ignored-config warnings on an otherwise passing run are defects.
WARNING_LINE = re.compile(r"^warning:", re.MULTILINE)

LANES: dict[str, Lane] = {
    "ts": Lane(
        lane_id="ts",
        doc=ROOT / "src" / "engineering_core" / "lanes" / "engineering-ts.md",
        fixture=ROOT / "tests" / "fixtures" / "lane-conformance" / "ts",
        tools=("bun",),
        prepare=prepare_ts,
        install=install_ts,
        refresh_lock=refresh_ts_lock,
        gates=tuple((script, ("bun", "run", script)) for script in GATE_SCRIPTS),
        probe_suffix=".ts",
        probe_dir="src",
        clean=LINT_DIAGNOSTIC,
    ),
    "go": Lane(
        lane_id="go",
        doc=LANES_DIR / "engineering-go.md",
        fixture=FIXTURES / "go",
        tools=("go",),
        prepare=prepare_from_blocks("go.mod", ".golangci.yml"),
        gates=quality_gates,
        probe_suffix=".go",
        probe_dir="calc",
    ),
    "py": Lane(
        lane_id="py",
        doc=LANES_DIR / "engineering-py.md",
        fixture=FIXTURES / "py",
        tools=("uv",),
        prepare=prepare_py,
        refresh_lock=refresh_py_lock,
        gates=quality_gates,
        probe_suffix=".py",
        probe_dir="src/example_service",
        clean=WARNING_LINE,
    ),
    "rust": Lane(
        lane_id="rust",
        doc=LANES_DIR / "engineering-rust.md",
        fixture=FIXTURES / "rust",
        tools=("cargo", "rustup"),
        prepare=prepare_from_blocks("rust-toolchain.toml", "deny.toml"),
        gates=quality_gates,
        probe_suffix=".rs",
        probe_dir="tests",
        clean=WARNING_LINE,
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("lanes", nargs="*", choices=sorted(LANES), metavar="lane", help=f"one or more of: {', '.join(sorted(LANES))}")
    parser.add_argument("--all", action="store_true", help="run every registered lane (release proof)")
    parser.add_argument("--lane-doc", type=Path, help="run against another copy of the lane doc (e.g. a prior revision)")
    parser.add_argument("--update-lock", action="store_true", help="re-resolve the fixture lock from the lane pins")
    parser.add_argument("--keep", action="store_true", help="keep the temporary project for inspection")
    args = parser.parse_args()
    if args.all == bool(args.lanes):
        parser.error("name one or more lanes, or pass --all")
    if args.all:
        args.lanes = sorted(LANES)
    if args.lane_doc and len(args.lanes) != 1:
        raise SystemExit("--lane-doc applies to exactly one lane")
    lanes = [LANES[lane_id] for lane_id in args.lanes]
    missing = sorted({tool for lane in lanes for tool in lane.tools if shutil.which(tool) is None})
    if missing:
        raise SystemExit(f"lane conformance needs on PATH: {', '.join(missing)}")
    if args.update_lock:
        for lane in lanes:
            if lane.refresh_lock is None:
                raise SystemExit(f"{lane.lane_id} lane has no lock to refresh")
            lane.refresh_lock(lane)
        return
    doc_text = args.lane_doc.read_text(encoding="utf-8") if args.lane_doc else None
    ok = True
    for lane in lanes:
        try:
            report = run_lane(lane, doc_text=doc_text, keep=args.keep)
        except LaneContractError as error:
            print(f"Feature: {lane.lane_id} lane configs pass their own gates\n  contract error: {error}")
            ok = False
            continue
        print(report.render())
        ok = ok and report.ok
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
