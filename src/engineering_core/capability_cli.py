# summary: "Defines and dispatches the doctor and explicit-population capability-scan CLI commands."
# read_when:
#   - "Changing doctor or scan-capabilities arguments, exit behavior, JSON emission, or command routing."

from __future__ import annotations

import argparse
import json
from pathlib import Path

from engineering_core.capability_scan import PopulationError, build_capability_scan, resolve_population
from engineering_core.doctor import build_doctor


def add_parsers(sub: argparse._SubParsersAction) -> None:
    doctor = sub.add_parser("doctor", help="Run deterministic non-executing repository readiness checks")
    doctor.add_argument("--repo", required=True)
    doctor.add_argument("--repo-root", default=".")
    doctor.add_argument("--prefer-repo", action="store_true")
    doctor.add_argument("--pretty", action="store_true")
    scan = sub.add_parser("scan-capabilities", help="Observe capabilities across an explicit repository population")
    scan.add_argument("--repo", action="append", default=[])
    scan.add_argument("--repo-file", action="append", default=[])
    scan.add_argument("--repo-root", default=".")
    scan.add_argument("--prefer-repo", action="store_true")
    scan.add_argument("--max-repositories", type=int, default=1000)
    scan.add_argument("--pretty", action="store_true")


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> bool:
    if args.cmd not in ("doctor", "scan-capabilities"):
        return False
    if args.cmd == "doctor":
        report = build_doctor(Path(args.repo), repo_root=Path(args.repo_root), prefer_repo=args.prefer_repo)
        _emit(report, args.pretty)
        if report["status"] == "blocked":
            raise SystemExit(1)
        return True
    if not args.repo and not args.repo_file:
        parser.error("scan-capabilities requires --repo and/or --repo-file")
    try:
        population = resolve_population([Path(item) for item in args.repo], [Path(item) for item in args.repo_file], max_repositories=args.max_repositories)
        report = build_capability_scan(population, repo_root=Path(args.repo_root), prefer_repo=args.prefer_repo)
    except PopulationError as exc:
        report = build_capability_scan([])
        report["completeness"] = "partial"
        report["failures"] = [{"path": "", "code": "population-invalid", "message": str(exc)}]
        _emit(report, args.pretty)
        raise SystemExit(1) from exc
    _emit(report, args.pretty)
    if not report["records"]:
        raise SystemExit(1)
    return True


def _emit(value: object, pretty: bool) -> None:
    print(json.dumps(value, indent=2 if pretty else None, sort_keys=True, separators=None if pretty else (",", ":")))
