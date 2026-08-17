#!/usr/bin/env python3
# summary: Checks semantic version surfaces, existing tag ancestry, catalog history, and release documentation.
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engineering_core.release_lineage import ReleaseLineageError, inspect_release_lineage


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate engineering-core release lineage")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--mode", choices=("ci", "release"), default="ci")
    parser.add_argument("--tag")
    parser.add_argument("--main-ref")
    args = parser.parse_args()
    try:
        report = inspect_release_lineage(
            Path(args.repo_root),
            mode=args.mode,
            tag_name=args.tag,
            main_ref=args.main_ref,
        )
    except ReleaseLineageError as exc:
        raise SystemExit(f"release lineage invalid: {exc}") from exc
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
