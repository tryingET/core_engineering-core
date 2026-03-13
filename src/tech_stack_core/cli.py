from __future__ import annotations

import argparse
from importlib import resources
from pathlib import Path


LANES = ("py", "ts", "pi-ts", "go", "rust", "elixir")
LANE_FILES = {
    "py": "tech-stack-py.md",
    "ts": "tech-stack-ts.md",
    "pi-ts": "tech-stack-pi-ts.md",
    "go": "tech-stack-go.md",
    "rust": "tech-stack-rust.md",
    "elixir": "tech-stack-elixir.md",
}


def _repo_lane_path(repo_root: Path, lane: str) -> Path:
    return repo_root / "lanes" / LANE_FILES[lane]


def _package_lane_path(lane: str) -> Path:
    return resources.files("tech_stack_core").joinpath("lanes", LANE_FILES[lane])  # type: ignore[no-any-return]


def main() -> None:
    parser = argparse.ArgumentParser(prog="tech-stack-core", description="View tech-stack-core lane docs.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available lanes")

    show = sub.add_parser("show", help="Print a lane doc to stdout")
    show.add_argument("lane", choices=LANES)
    show.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    show.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    path_cmd = sub.add_parser("path", help="Print filesystem path to lane doc")
    path_cmd.add_argument("lane", choices=LANES)
    path_cmd.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    path_cmd.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    args = parser.parse_args()

    if args.cmd == "list":
        for lane in LANES:
            print(lane)
        return

    if args.cmd == "show":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_lane_path(repo_root, args.lane)
        if args.prefer_repo and repo_path.exists():
            print(repo_path.read_text(encoding="utf-8"))
            return
        p = _package_lane_path(args.lane)
        print(p.read_text(encoding="utf-8"))
        return

    if args.cmd == "path":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_lane_path(repo_root, args.lane)
        if args.prefer_repo and repo_path.exists():
            print(str(repo_path))
            return
        print(str(_package_lane_path(args.lane)))
        return
