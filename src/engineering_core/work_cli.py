# summary: "Registers prepare-work, finalize-work, and verify-work CLI commands with bounded no-follow inputs and deterministic stdout-only JSON output."
# read_when:
#   - "When changing owner-use workflow command arguments, safe input loading, output behavior, or verification exit semantics."

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from engineering_core.catalog import load_catalog
from engineering_core.closed_loop import ClosedLoopError, load_record_with_bytes
from engineering_core.safe_io import SafeInputError
from engineering_core.work_bundle import WorkBundleError, finalize_work
from engineering_core.work_packet import WorkPacketError, prepare_work
from engineering_core.work_render import build_summary, render_markdown
from engineering_core.work_verify import verify_work

COMMANDS = ("prepare-work", "finalize-work", "verify-work", "summarize-work")
MAX_WORKFLOW_INPUT_BYTES = 8_388_608
MAX_REPEATED_RECORDS = 100


def _catalog_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", default=".", help="Repo root containing catalog.json (default: .)")
    parser.add_argument("--prefer-repo", action="store_true", help="Prefer repo catalog.json over packaged catalog")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON")


def add_parsers(subparsers: argparse._SubParsersAction) -> None:
    prepare = subparsers.add_parser("prepare-work", help="Build a deterministic owner-use work packet without executing commands or invoking models")
    prepare.add_argument("--repo", required=True, help="Explicit repository Git root")
    prepare.add_argument("--repo-id", required=True, help="Stable owner-supplied repository identity")
    prepare.add_argument("--context", required=True, help="Bounded engineering-work-context-v1 JSON")
    _catalog_args(prepare)

    finalize = subparsers.add_parser("finalize-work", help="Bind external advice, owner dispositions, and receipts into a non-authoritative evidence bundle")
    finalize.add_argument("--packet", required=True, help="engineering-work-packet-v1 JSON")
    finalize.add_argument("--advice", help="Externally supplied engineering-advice-response-v1 JSON")
    finalize.add_argument("--disposition", action="append", default=[], help="Owner disposition JSON; repeat as needed")
    finalize.add_argument("--receipt", action="append", default=[], help="Owner receipt JSON; repeat as needed")
    finalize.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON")

    summary = subparsers.add_parser("summarize-work", help="Render a concise owner handoff from an evidence bundle and optional verification")
    summary.add_argument("--bundle", required=True, help="engineering-evidence-bundle-v1 JSON")
    summary.add_argument("--verification", help="Optional engineering-work-verification-v1 JSON")
    summary.add_argument("--format", choices=("json", "markdown"), default="markdown")

    verify = subparsers.add_parser("verify-work", help="Verify an evidence bundle against one explicit current repository without mutation")
    verify.add_argument("--repo", required=True, help="Explicit repository Git root")
    verify.add_argument("--repo-id", required=True, help="Stable owner-supplied repository identity")
    verify.add_argument("--bundle", required=True, help="engineering-evidence-bundle-v1 JSON")
    _catalog_args(verify)


def _load(path: str) -> tuple[dict, str]:
    value, raw = load_record_with_bytes(Path(path), max_bytes=MAX_WORKFLOW_INPUT_BYTES)
    if not isinstance(value, dict):
        raise WorkBundleError("owner-use input must be a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def _print(value: dict, pretty: bool) -> None:
    print(json.dumps(value, indent=2 if pretty else None, sort_keys=True, separators=None if pretty else (",", ":")))


def run(args: argparse.Namespace) -> bool:
    if args.cmd not in COMMANDS:
        return False
    try:
        if args.cmd == "prepare-work":
            context, _ = _load(args.context)
            output = prepare_work(Path(args.repo), args.repo_id, context, load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo))
        elif args.cmd == "finalize-work":
            packet, packet_raw = _load(args.packet)
            advice, advice_raw = _load(args.advice) if args.advice else (None, None)
            if len(args.disposition) > MAX_REPEATED_RECORDS or len(args.receipt) > MAX_REPEATED_RECORDS:
                raise WorkBundleError(f"owner-use inputs accept at most {MAX_REPEATED_RECORDS} dispositions or receipts")
            disposition_pairs = [_load(path) for path in args.disposition]
            receipt_pairs = [_load(path) for path in args.receipt]
            output = finalize_work(
                packet, advice,
                [value for value, _ in disposition_pairs],
                [value for value, _ in receipt_pairs],
                {"packet": packet_raw, "advice": advice_raw, "dispositions": [digest for _, digest in disposition_pairs], "receipts": [digest for _, digest in receipt_pairs]},
            )
        elif args.cmd == "verify-work":
            bundle, _ = _load(args.bundle)
            output = verify_work(Path(args.repo), args.repo_id, bundle, load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo))
        else:
            bundle, _ = _load(args.bundle)
            verification = _load(args.verification)[0] if args.verification else None
            output = build_summary(bundle, verification)
    except (ClosedLoopError, SafeInputError, WorkPacketError, WorkBundleError, OSError, ValueError) as exc:
        raise SystemExit(f"owner-use input rejected: {exc}") from exc
    if args.cmd == "summarize-work" and args.format == "markdown":
        print(render_markdown(output))
    else:
        _print(output, getattr(args, "pretty", False))
    if args.cmd == "verify-work" and output["result"] != "matched":
        raise SystemExit(1)
    return True
