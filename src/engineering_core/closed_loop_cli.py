# summary: "Defines and dispatches receipt, disposition, calibration, pattern, and doctrine-proposal CLI workflows over explicit record files."
# read_when:
#   - "Changing closed-loop CLI arguments, record loading, validation dispatch, output schemas, or command exit behavior."

from __future__ import annotations

import argparse
import json
from pathlib import Path

from engineering_core.closed_loop import ClosedLoopError, calibration, doctrine_proposal, load_record, summarize_receipts, synthesize_patterns, validate_disposition, validate_receipt


def add_parsers(sub: argparse._SubParsersAction) -> None:
    receipt = sub.add_parser("receipt", help="Validate or summarize owner-produced evidence receipts")
    receipt.add_argument("action", choices=("validate", "summarize")); receipt.add_argument("--receipt", action="append", required=True); receipt.add_argument("--pretty", action="store_true")
    disposition = sub.add_parser("disposition", help="Validate an owner recommendation disposition")
    disposition.add_argument("action", choices=("validate",)); disposition.add_argument("--disposition", required=True); disposition.add_argument("--advice"); disposition.add_argument("--pretty", action="store_true")
    cal = sub.add_parser("calibration", help="Separate model confidence, owner acceptance, and evidence outcomes")
    cal.add_argument("--advice", required=True); cal.add_argument("--disposition", action="append", required=True); cal.add_argument("--receipt", action="append", default=[]); cal.add_argument("--pretty", action="store_true")
    patterns = sub.add_parser("patterns", help="Synthesize deterministic patterns from explicitly supplied records")
    for flag in ("plan", "advice", "disposition", "receipt"): patterns.add_argument(f"--{flag}", action="append", default=[])
    patterns.add_argument("--pretty", action="store_true")
    doctrine = sub.add_parser("doctrine-propose", help="Produce an unapplied doctrine/catalog review proposal")
    doctrine.add_argument("--patterns", required=True); doctrine.add_argument("--pretty", action="store_true")


def run(args: argparse.Namespace) -> bool:
    if args.cmd not in ("receipt", "disposition", "calibration", "patterns", "doctrine-propose"): return False
    try:
        if args.cmd == "receipt":
            records = [load_record(Path(path)) for path in args.receipt]
            if args.action == "validate" and len(records) != 1: raise ClosedLoopError("receipt validate accepts exactly one receipt")
            output = {"schema": "engineering-receipt-validation-v1", "valid": True, "receipt": validate_receipt(records[0])} if args.action == "validate" else summarize_receipts(records)
        elif args.cmd == "disposition":
            output = {"schema": "engineering-disposition-validation-v1", "valid": True, "disposition": validate_disposition(load_record(Path(args.disposition)), load_record(Path(args.advice)) if args.advice else None)}
        elif args.cmd == "calibration":
            output = calibration(load_record(Path(args.advice)), [load_record(Path(x)) for x in args.disposition], [load_record(Path(x)) for x in args.receipt])
        elif args.cmd == "patterns":
            output = synthesize_patterns([load_record(Path(x)) for x in args.plan], [load_record(Path(x)) for x in args.advice], [load_record(Path(x)) for x in args.disposition], [load_record(Path(x)) for x in args.receipt])
        else: output = doctrine_proposal(load_record(Path(args.patterns)))
    except ClosedLoopError as exc: raise SystemExit(f"closed-loop input rejected: {exc}") from exc
    print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True, separators=None if args.pretty else (",", ":")))
    return True
