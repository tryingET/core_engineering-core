from __future__ import annotations

import argparse
from importlib import resources
from pathlib import Path


LANES = ("py", "ts", "ts-frontend", "pi-ts", "go", "cpp", "rust", "elixir")
LANE_FILES = {
    "py": "engineering-py.md",
    "ts": "engineering-ts.md",
    "ts-frontend": "engineering-ts.frontend.md",
    "pi-ts": "engineering-pi-ts.md",
    "go": "engineering-go.md",
    "cpp": "engineering-cpp.md",
    "rust": "engineering-rust.md",
    "elixir": "engineering-elixir.md",
}

DISCIPLINES = (
    "design-system",
    "accessibility",
    "validation",
    "testing",
    "local-first-data",
    "observability",
    "security-privacy",
    "documentation",
    "dependency-governance",
)
DISCIPLINE_FILES = {name: f"{name}.md" for name in DISCIPLINES}


def _repo_lane_path(repo_root: Path, lane: str) -> Path:
    return repo_root / "lanes" / LANE_FILES[lane]


def _package_lane_path(lane: str) -> Path:
    return resources.files("engineering_core").joinpath("lanes", LANE_FILES[lane])  # type: ignore[no-any-return]


def _repo_discipline_path(repo_root: Path, discipline: str) -> Path:
    return repo_root / "disciplines" / DISCIPLINE_FILES[discipline]


def _package_discipline_path(discipline: str) -> Path:
    return resources.files("engineering_core").joinpath("disciplines", DISCIPLINE_FILES[discipline])  # type: ignore[no-any-return]


def _print_doc(path: Path) -> None:
    print(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="engineering-core", description="View engineering-core lane and discipline docs.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available lanes")
    sub.add_parser("list-disciplines", help="List available cross-language disciplines")

    show = sub.add_parser("show", help="Print a lane doc to stdout")
    show.add_argument("lane", choices=LANES)
    show.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    show.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    path_cmd = sub.add_parser("path", help="Print filesystem path to lane doc")
    path_cmd.add_argument("lane", choices=LANES)
    path_cmd.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    path_cmd.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    show_discipline = sub.add_parser("show-discipline", help="Print a cross-language discipline doc to stdout")
    show_discipline.add_argument("discipline", choices=DISCIPLINES)
    show_discipline.add_argument("--repo-root", default=".", help="Repo root that contains ./disciplines (default: .)")
    show_discipline.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./disciplines over packaged files")

    discipline_path = sub.add_parser("discipline-path", help="Print filesystem path to a discipline doc")
    discipline_path.add_argument("discipline", choices=DISCIPLINES)
    discipline_path.add_argument("--repo-root", default=".", help="Repo root that contains ./disciplines (default: .)")
    discipline_path.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./disciplines over packaged files")

    args = parser.parse_args()

    if args.cmd == "list":
        for lane in LANES:
            print(lane)
        return

    if args.cmd == "list-disciplines":
        for discipline in DISCIPLINES:
            print(discipline)
        return

    if args.cmd == "show":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_lane_path(repo_root, args.lane)
        if args.prefer_repo and repo_path.exists():
            _print_doc(repo_path)
            return
        _print_doc(Path(_package_lane_path(args.lane)))
        return

    if args.cmd == "path":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_lane_path(repo_root, args.lane)
        if args.prefer_repo and repo_path.exists():
            print(str(repo_path))
            return
        print(str(_package_lane_path(args.lane)))
        return

    if args.cmd == "show-discipline":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_discipline_path(repo_root, args.discipline)
        if args.prefer_repo and repo_path.exists():
            _print_doc(repo_path)
            return
        _print_doc(Path(_package_discipline_path(args.discipline)))
        return

    if args.cmd == "discipline-path":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_discipline_path(repo_root, args.discipline)
        if args.prefer_repo and repo_path.exists():
            print(str(repo_path))
            return
        print(str(_package_discipline_path(args.discipline)))
        return
