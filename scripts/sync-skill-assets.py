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
    import subprocess as _sp
    projection = _sp.run(
        ["python3", str(ROOT / "scripts" / "build_skill_projection.py"), "--check"],
        capture_output=False,
    )
    if projection.returncode != 0:
        raise SystemExit("skill projection differs; run scripts/build_skill_projection.py")
    return
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DESTINATION)
    print(f"synced {DESTINATION.relative_to(ROOT)}")
    import subprocess as _sp
    _sp.run(["python3", str(ROOT / "scripts" / "build_skill_projection.py")], check=True)


if __name__ == "__main__":
    main()
