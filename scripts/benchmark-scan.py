from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

from engineering_core.adoption_scan import build_scan
from engineering_core.catalog_model import load_catalog


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure synthetic engineering-core scan throughput."
    )
    parser.add_argument("--repos", type=int, default=250)
    args = parser.parse_args()
    if args.repos < 1:
        parser.error("--repos must be positive")

    catalog = load_catalog()
    with tempfile.TemporaryDirectory() as tmp:
        scope = Path(tmp)
        for index in range(args.repos):
            repo = scope / f"repo-{index:04d}"
            repo.mkdir()
            (repo / ".git").mkdir()
        started = time.perf_counter()
        scan = build_scan(
            [scope],
            include_packages=False,
            include_scope_root=False,
            repo_discovery="immediate",
            catalog=catalog,
        )
        elapsed = time.perf_counter() - started
    rate = scan["summary"]["total"] / elapsed if elapsed else float("inf")
    print(
        f"records={scan['summary']['total']} elapsed_seconds={elapsed:.6f} "
        f"records_per_second={rate:.2f}"
    )


if __name__ == "__main__":
    main()
