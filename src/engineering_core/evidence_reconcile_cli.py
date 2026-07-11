# summary: "Defines and dispatches the explicit repository-to-receipt evidence reconciliation CLI command."
# read_when:
#   - "Changing reconcile-evidence arguments, repository identity mapping, output emission, or failure exit criteria."

from __future__ import annotations

import argparse
import json
from pathlib import Path

from engineering_core.evidence_reconcile import reconcile_evidence

COMMAND = "reconcile-evidence"


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(COMMAND, help="Reconcile explicit owner receipt artifacts without promoting authority")
    parser.add_argument("--repo", action="append", nargs=2, metavar=("REPOSITORY_ID", "PATH"), required=True, help="Explicit stable repository id and local path; repeat for multiple repositories")
    parser.add_argument("--receipt", action="append", required=True, help="Explicit owner receipt JSON path; repeat for multiple receipts")
    parser.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    parser.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON")


def run(args: argparse.Namespace) -> bool:
    if args.cmd != COMMAND:
        return False
    output = reconcile_evidence(
        [(repository_id, Path(path)) for repository_id, path in args.repo],
        [Path(path) for path in args.receipt],
        repo_root=Path(args.repo_root).resolve(),
        prefer_repo=args.prefer_repo,
    )
    print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True, separators=None if args.pretty else (",", ":")))
    if output["failures"] or not output["records"] or any(item["result"] != "matched" for item in output["records"]):
        raise SystemExit(1)
    return True
