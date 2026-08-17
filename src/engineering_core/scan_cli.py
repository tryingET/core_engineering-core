from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from engineering_core.adoption_render import render_markdown as render_scan_markdown
from engineering_core.adoption_scan import build_scan
from engineering_core.catalog_model import load_catalog
from engineering_core.scan_diagnostics import (
    build_diagnostics,
    evaluate,
    failing_diagnostics,
    load_baseline,
    make_baseline,
    normalize_selectors,
    render_markdown as render_diagnostics_markdown,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engineering-core")
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan-adoption", help="Scan scopes for engineering-core adoption coverage")
    scan.add_argument("--scope", action="append", default=[])
    scan.add_argument("--include-packages", action="store_true")
    scan.add_argument("--include-scope-root", action="store_true")
    scan.add_argument("--repo-discovery", choices=("immediate", "recursive"), default="immediate")
    scan.add_argument("--format", choices=("markdown", "json"), default="markdown")
    scan.add_argument("--write", action="store_true")
    scan.add_argument("--json-out")
    scan.add_argument("--markdown-out")
    scan.add_argument("--diagnostics-out")
    scan.add_argument("--baseline", help="Compare against a versioned diagnostic baseline")
    scan.add_argument("--write-baseline", help="Write the current diagnostic baseline")
    scan.add_argument(
        "--fail-on",
        action="append",
        default=[],
        help="Severity, exact rule ID, or prefix ending in *; repeat or comma-separate",
    )
    scan.add_argument("--repo-root", default=".")
    scan.add_argument("--prefer-repo", action="store_true")
    return parser


def _write_text(path_value: str, content: str) -> None:
    path = Path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote: {path}", file=sys.stderr)


def _write_json(path_value: str, value: dict[str, Any]) -> None:
    _write_text(path_value, json.dumps(value, indent=2, sort_keys=True) + "\n")


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.write and not args.json_out and not args.markdown_out:
        parser.error("scan-adoption --write requires --json-out and/or --markdown-out")

    catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)
    scopes = [Path(value).resolve() for value in (args.scope or ["."])]
    try:
        scan = build_scan(
            scopes,
            include_packages=args.include_packages,
            include_scope_root=args.include_scope_root,
            repo_discovery=args.repo_discovery,
            catalog=catalog,
        )
        baseline = load_baseline(Path(args.baseline)) if args.baseline else None
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    diagnostics = build_diagnostics(scan, catalog)
    evaluation = evaluate(diagnostics, baseline=baseline)
    scan["diagnostics"] = diagnostics
    scan["diagnostic_summary"] = evaluation["summary"]
    scan["baseline_supplied"] = evaluation["baseline_supplied"]

    if args.write_baseline:
        _write_json(
            args.write_baseline,
            make_baseline(diagnostics, generated_at=scan.get("generated_at")),
        )
    if args.diagnostics_out:
        _write_json(args.diagnostics_out, evaluation)

    json_output = json.dumps(scan, indent=2, sort_keys=True) + "\n"
    markdown_output = render_scan_markdown(scan) + "\n" + render_diagnostics_markdown(evaluation)
    if args.write:
        if args.json_out:
            _write_text(args.json_out, json_output)
        if args.markdown_out:
            _write_text(args.markdown_out, markdown_output)
    elif args.format == "json":
        print(json_output, end="")
    else:
        print(markdown_output, end="")

    selectors = normalize_selectors(args.fail_on)
    failures = failing_diagnostics(evaluation, selectors)
    if failures:
        rules = ", ".join(sorted({item["rule_id"] for item in failures}))
        print(
            f"engineering-core scan-adoption failed on {len(failures)} matching diagnostic(s): {rules}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
