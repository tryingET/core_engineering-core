from __future__ import annotations

import argparse
from pathlib import Path

from engineering_core.catalog_model import sync_catalog_projection


def main() -> None:
    parser = argparse.ArgumentParser(description="Check or refresh the root catalog projection.")
    parser.add_argument("--repo-root", default=".")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Fail when the projection differs")
    mode.add_argument("--apply", action="store_true", help="Refresh the projection")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    drifted = sync_catalog_projection(repo_root, apply=args.apply)
    if drifted and not args.apply:
        raise SystemExit("catalog projection differs from src/engineering_core/catalog.json; rerun with --apply")
    print("catalog projection updated" if drifted else "catalog projection is current")


if __name__ == "__main__":
    main()
