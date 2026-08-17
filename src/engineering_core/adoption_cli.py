from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from engineering_core.adoption import AdoptionPlan, apply_plan, plan_init, plan_migration, render_plan
from engineering_core.catalog_model import load_catalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engineering-core")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Plan or apply repository adoption files")
    init_cmd.add_argument("--repo", default=".")
    init_cmd.add_argument("--profile")
    init_cmd.add_argument("--lane", action="append", default=[])
    init_cmd.add_argument("--discipline", action="append", default=[])
    init_cmd.add_argument("--ref", default="workspace-local-unpinned")
    init_cmd.add_argument("--force", action="store_true")
    init_cmd.add_argument("--apply", action="store_true", help="Write changes; default is dry-run")
    init_cmd.add_argument("--format", choices=("human", "json"), default="human")
    init_cmd.add_argument("--repo-root", default=".")
    init_cmd.add_argument("--prefer-repo", action="store_true")

    migrate = sub.add_parser("migrate", help="Plan or apply migration from legacy tech-stack surfaces")
    migrate.add_argument("--repo", default=".")
    migrate.add_argument("--ref", default="workspace-local-unpinned")
    migrate.add_argument("--force", action="store_true")
    migrate.add_argument("--remove-legacy", action="store_true")
    migrate.add_argument("--apply", action="store_true", help="Write changes; default is dry-run")
    migrate.add_argument("--format", choices=("human", "json"), default="human")
    migrate.add_argument("--repo-root", default=".")
    migrate.add_argument("--prefer-repo", action="store_true")
    return parser


def _print(plan: AdoptionPlan, output_format: str, *, applied: bool) -> None:
    if output_format == "json":
        payload: dict[str, Any] = plan.as_dict()
        payload["applied"] = applied
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(render_plan(plan))
    print(f"applied: {str(applied).lower()}")


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)

    try:
        if args.command == "init":
            plan = plan_init(
                Path(args.repo),
                catalog,
                profile=args.profile,
                lanes=args.lane,
                disciplines=args.discipline,
                ref=args.ref,
                force=args.force,
            )
        else:
            plan = plan_migration(
                Path(args.repo),
                catalog,
                ref=args.ref,
                force=args.force,
                remove_legacy=args.remove_legacy,
            )
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    applied = False
    if args.apply:
        if plan.conflicts:
            _print(plan, args.format, applied=False)
            raise SystemExit(2)
        apply_plan(plan)
        applied = True

    _print(plan, args.format, applied=applied)
    if plan.conflicts:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
