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
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_SCRIPTS = ("typecheck", "check")
BINARY_PACKAGES = {"biome": "@biomejs/biome", "tsc": "typescript"}
TOOLCHAIN_PACKAGES = ("@biomejs/biome", "typescript", "@types/bun")
CONFIG_BLOCKS = ("bunfig.toml", "biome.json", "tsconfig.json")
EXPECT = re.compile(r"^// expect: (\S+) (\S+)$", re.MULTILINE)
# Any rule diagnostic, including info severity: an exit-0 gate that still advises
# rewriting conformant code (e.g. useLiteralKeys vs TS4111) is not clean.
LINT_DIAGNOSTIC = re.compile(r"\blint/\w+/\w+")


@dataclass(frozen=True)
class Lane:
    lane_id: str
    doc: Path
    fixture: Path


LANES = {
    "ts": Lane(
        "ts",
        ROOT / "src" / "engineering_core" / "lanes" / "engineering-ts.md",
        ROOT / "tests" / "fixtures" / "lane-conformance" / "ts",
    ),
}


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


def strip_line_comments(jsonc: str) -> str:
    return "\n".join(line for line in jsonc.splitlines() if not line.strip().startswith("//"))


def conformance_package(lane_package_text: str) -> dict:
    lane_package = json.loads(lane_package_text)
    dev = lane_package.get("devDependencies", {})
    missing = [package for package in TOOLCHAIN_PACKAGES if package not in dev]
    if missing:
        raise SystemExit(f"lane package.json lacks toolchain devDependencies: {', '.join(missing)}")
    return {
        "name": "lane-conformance",
        "private": True,
        "type": "module",
        "scripts": {script: lane_package["scripts"][script] for script in GATE_SCRIPTS},
        "devDependencies": {package: dev[package] for package in TOOLCHAIN_PACKAGES},
    }


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def write_project(lane: Lane, work: Path, doc_text: str, *, with_bunfig: bool) -> None:
    files = extract_lane_files(doc_text)
    missing = [name for name in (*CONFIG_BLOCKS, "package.json") if name not in files]
    if missing:
        raise SystemExit(f"{lane.doc.name} lacks config blocks: {', '.join(missing)}")
    for name in ("biome.json", "tsconfig.json"):
        (work / name).write_text(files[name], encoding="utf-8")
    if with_bunfig:
        (work / "bunfig.toml").write_text(files["bunfig.toml"], encoding="utf-8")
    package = conformance_package(files["package.json"])
    (work / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")


def use_sources(lane: Lane, work: Path, probe: Path | None) -> None:
    for name in ("src", "test"):
        shutil.rmtree(work / name, ignore_errors=True)
    shutil.copytree(lane.fixture / "pass", work, dirs_exist_ok=True)
    if probe is not None:
        shutil.copy(probe, work / "src" / probe.name)


def run_lane(lane: Lane, *, doc_text: str | None = None, keep: bool = False) -> Report:
    doc_text = doc_text if doc_text is not None else lane.doc.read_text(encoding="utf-8")
    report = Report(lane.lane_id)
    work = Path(tempfile.mkdtemp(prefix=f"lane-conformance-{lane.lane_id}-"))
    try:
        write_project(lane, work, doc_text, with_bunfig=True)
        shutil.copy(lane.fixture / "bun.lock", work / "bun.lock")
        install = run(["bun", "install", "--frozen-lockfile", "--ignore-scripts"], work)
        if install.returncode != 0:
            report.passes.append(Result(
                "pinned tools install from the committed lock (rerun with --update-lock after a pin change)",
                False, install.stdout + install.stderr,
            ))
            return report
        use_sources(lane, work, None)
        for script in GATE_SCRIPTS:
            proc = run(["bun", "run", script], work)
            output = proc.stdout + proc.stderr
            report.passes.append(Result(
                f"conformant code passes `{script}` without diagnostics",
                proc.returncode == 0 and not LINT_DIAGNOSTIC.search(output), output,
            ))
        for probe in sorted((lane.fixture / "probes").glob("*.ts")):
            expectations = EXPECT.findall(probe.read_text(encoding="utf-8"))
            if not expectations:
                report.probes.append(Result(f"probe {probe.name} declares expectations", False))
                continue
            use_sources(lane, work, probe)
            for script, needle in expectations:
                proc = run(["bun", "run", script], work)
                output = proc.stdout + proc.stderr
                report.probes.append(Result(
                    f"`{script}` rejects {probe.name} with {needle}",
                    proc.returncode != 0 and needle in output, output,
                ))
        return report
    finally:
        if keep:
            print(f"kept work dir: {work}", file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)


def update_lock(lane: Lane) -> None:
    with tempfile.TemporaryDirectory(prefix=f"lane-conformance-{lane.lane_id}-lock-") as tmp:
        work = Path(tmp)
        # bunfig.toml sets frozenLockfile; write it only for verification runs.
        write_project(lane, work, lane.doc.read_text(encoding="utf-8"), with_bunfig=False)
        proc = run(["bun", "install", "--ignore-scripts"], work)
        if proc.returncode != 0:
            raise SystemExit(proc.stdout + proc.stderr)
        shutil.copy(work / "bun.lock", lane.fixture / "bun.lock")
    print(f"updated {(lane.fixture / 'bun.lock').relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("lane", choices=sorted(LANES))
    parser.add_argument("--lane-doc", type=Path, help="run against another copy of the lane doc (e.g. a prior revision)")
    parser.add_argument("--update-lock", action="store_true", help="re-resolve the fixture lock from the lane pins")
    parser.add_argument("--keep", action="store_true", help="keep the temporary project for inspection")
    args = parser.parse_args()
    if shutil.which("bun") is None:
        raise SystemExit("lane conformance needs bun on PATH")
    lane = LANES[args.lane]
    if args.update_lock:
        update_lock(lane)
        return
    doc_text = args.lane_doc.read_text(encoding="utf-8") if args.lane_doc else None
    report = run_lane(lane, doc_text=doc_text, keep=args.keep)
    print(report.render())
    raise SystemExit(0 if report.ok else 1)


if __name__ == "__main__":
    main()
