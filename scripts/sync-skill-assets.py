from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "engineering_core" / "skill" / "SKILL.md"
DESTINATION = ROOT / "skills" / "engineering-core" / "SKILL.md"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        if not DESTINATION.exists() or SOURCE.read_bytes() != DESTINATION.read_bytes():
            raise SystemExit(
                "engineering-core skill projection differs; run scripts/sync-skill-assets.py"
            )
        print("engineering-core skill projection is current")
        return
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    print(f"synced {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
