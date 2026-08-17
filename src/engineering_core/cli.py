from __future__ import annotations

import argparse
import json
from importlib import resources
from pathlib import Path
from typing import Any

from engineering_core.adoption_render import render_markdown
from engineering_core.adoption_scan import build_scan
from engineering_core.catalog_model import (
    DISCIPLINES,
    DISCIPLINE_FILES,
    LANES,
    LANE_FILES,
    TEMPLATES,
    TEMPLATE_FILES,
    load_catalog,
    sync_catalog_projection,
)
from engineering_core.doctor import doctor_repo, exit_code as doctor_exit_code, render_human as render_doctor_human
from engineering_core.self_check import run_self_check


def _repo_lane_path(repo_root: Path, lane: str) -> Path:
    return repo_root / "lanes" / LANE_FILES[lane]


def _package_lane_path(lane: str) -> Path:
    return Path(resources.files("engineering_core").joinpath("lanes", LANE_FILES[lane]))


def _repo_discipline_path(repo_root: Path, discipline: str) -> Path:
    return repo_root / "disciplines" / DISCIPLINE_FILES[discipline]


def _package_discipline_path(discipline: str) -> Path:
    return Path(resources.files("engineering_core").joinpath("disciplines", DISCIPLINE_FILES[discipline]))


def _repo_template_path(repo_root: Path, template: str) -> Path:
    return repo_root / "templates" / TEMPLATE_FILES[template]


def _package_template_path(template: str) -> Path:
    return Path(resources.files("engineering_core").joinpath("templates", TEMPLATE_FILES[template]))


def _repo_catalog_path(repo_root: Path) -> Path:
    return repo_root / "catalog.json"


def _package_catalog_path() -> Path:
    return Path(resources.files("engineering_core").joinpath("catalog.json"))


def _repo_discipline_overview_path(repo_root: Path) -> Path:
    return repo_root / "disciplines" / "README.md"


def _package_discipline_overview_path() -> Path:
    return Path(resources.files("engineering_core").joinpath("disciplines", "README.md"))


def _print_doc(path: Path) -> None:
    print(path.read_text(encoding="utf-8"))


def _load_catalog(repo_root: Path, prefer_repo: bool) -> dict[str, Any]:
    return load_catalog(repo_root, prefer_repo=prefer_repo)


def _print_catalog(catalog: dict[str, Any], *, pretty: bool) -> None:
    if pretty:
        print(json.dumps(catalog, indent=2, sort_keys=True))
    else:
        print(json.dumps(catalog, sort_keys=True))


def _print_recommendation_items(title: str, lanes: list[str], disciplines: list[str]) -> None:
    print(f"# engineering-core recommendation: {title}")
    print("\nLanes/addenda:")
    for lane in lanes:
        print(f"- {lane}")
    if not lanes:
        print("- <select language lane(s) from repo implementation language>")
    print("\nDisciplines:")
    for discipline in disciplines:
        print(f"- {discipline}")


def _print_recommendation(catalog: dict[str, Any], profile_id: str) -> None:
    for profile in catalog.get("profiles", []):
        if profile.get("id") == profile_id:
            _print_recommendation_items(profile_id, profile.get("lanes", []), profile.get("disciplines", []))
            return
    valid = ", ".join(profile.get("id", "") for profile in catalog.get("profiles", []))
    raise SystemExit(f"unknown profile: {profile_id}. valid profiles: {valid}")


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _repo_policy_recommendation(repo_root: Path) -> tuple[list[str], list[str]] | None:
    policy_path = repo_root / "policy" / "engineering-lane.json"
    if not policy_path.exists():
        return None
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    engineering_core = policy.get("engineering_core", {})
    lanes: list[str] = []
    if isinstance(engineering_core.get("lane"), str):
        lanes.append(engineering_core["lane"])
    if isinstance(policy.get("lane"), str) and policy["lane"] not in lanes:
        lanes.append(policy["lane"])
    for entry in engineering_core.get("lanes", []):
        if isinstance(entry, dict) and isinstance(entry.get("lane"), str):
            lanes.append(entry["lane"])
        elif isinstance(entry, str):
            lanes.append(entry)
    disciplines = [item for item in engineering_core.get("disciplines", []) if isinstance(item, str)]
    return _dedupe(lanes), _dedupe(disciplines)


def _infer_repo_recommendation(repo_root: Path) -> tuple[list[str], list[str]]:
    policy = _repo_policy_recommendation(repo_root)
    if policy is not None:
        return policy

    lanes: list[str] = []
    if (repo_root / "Cargo.toml").exists():
        lanes.append("rust")
    if (repo_root / "package.json").exists() or (repo_root / "tsconfig.json").exists():
        lanes.append("ts")
    if (repo_root / "pyproject.toml").exists():
        lanes.append("py")
    if (repo_root / "go.mod").exists():
        lanes.append("go")
    if (repo_root / "mix.exs").exists():
        lanes.append("elixir")

    package_json = repo_root / "package.json"
    if package_json.exists():
        try:
            package = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            package = {}
        deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
        if any(name in deps for name in ("react", "vue", "svelte", "@vitejs/plugin-react", "vite")):
            lanes.append("ts-frontend")

    disciplines = ["validation", "testing", "security-privacy", "documentation", "dependency-governance"]
    if "ts-frontend" in lanes:
        disciplines.extend(["design-system", "accessibility"])
    if any((repo_root / name).exists() for name in ("schema", "schemas", "contracts")):
        disciplines.append("specification-and-dsls")
    return _dedupe(lanes), _dedupe(disciplines)


def _add_repo_catalog_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", default=".", help="Repository root (default: .)")
    parser.add_argument("--prefer-repo", action="store_true", help="Prefer repository files over packaged files")


def _write_scan(scan: dict[str, Any], *, json_out: str | None, markdown_out: str | None) -> None:
    if json_out:
        json_path = Path(json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(scan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote: {json_path}")
    if markdown_out:
        markdown_path = Path(markdown_out)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown(scan), encoding="utf-8")
        print(f"wrote: {markdown_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="engineering-core", description="View and validate engineering-core guidance.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available lanes")
    sub.add_parser("list-disciplines", help="List available cross-language disciplines")
    sub.add_parser("list-templates", help="List available adoption/review templates")

    list_profiles = sub.add_parser("list-profiles", help="List catalog recommendation profiles")
    _add_repo_catalog_options(list_profiles)

    catalog_cmd = sub.add_parser("catalog", help="Print the machine-readable engineering-core catalog")
    _add_repo_catalog_options(catalog_cmd)
    catalog_cmd.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    recommend = sub.add_parser("recommend", help="Print lane/discipline recommendation for a catalog profile or repo")
    recommend.add_argument("profile", nargs="?", help="Catalog profile id, for example browser-app or service-api")
    recommend.add_argument("--repo", help="Infer recommendation from a repository path")
    _add_repo_catalog_options(recommend)

    scan_adoption = sub.add_parser("scan-adoption", help="Scan one or more scopes for engineering-core adoption coverage")
    scan_adoption.add_argument("--scope", action="append", default=[], help="Scope root to scan; repeat for multiple scopes")
    scan_adoption.add_argument("--include-packages", action="store_true", help="Also scan nested package/app/member adoption surfaces")
    scan_adoption.add_argument("--include-scope-root", action="store_true", help="Include the scope root itself when it is a git repo")
    scan_adoption.add_argument("--repo-discovery", choices=("immediate", "recursive"), default="immediate")
    scan_adoption.add_argument("--format", choices=("markdown", "json"), default="markdown")
    scan_adoption.add_argument("--write", action="store_true", help="Write outputs instead of printing")
    scan_adoption.add_argument("--json-out")
    scan_adoption.add_argument("--markdown-out")
    _add_repo_catalog_options(scan_adoption)

    overview = sub.add_parser("overview", help="Print the disciplines overview doc")
    _add_repo_catalog_options(overview)

    show_template = sub.add_parser("show-template", help="Print an adoption/review template")
    show_template.add_argument("template", choices=TEMPLATES)
    _add_repo_catalog_options(show_template)

    template_path = sub.add_parser("template-path", help="Print path to an adoption/review template")
    template_path.add_argument("template", choices=TEMPLATES)
    _add_repo_catalog_options(template_path)

    show = sub.add_parser("show", help="Print a lane doc")
    show.add_argument("lane", choices=LANES)
    _add_repo_catalog_options(show)

    path_cmd = sub.add_parser("path", help="Print path to a lane doc")
    path_cmd.add_argument("lane", choices=LANES)
    _add_repo_catalog_options(path_cmd)

    show_discipline = sub.add_parser("show-discipline", help="Print a cross-language discipline doc")
    show_discipline.add_argument("discipline", choices=(*DISCIPLINES, "README", "readme"))
    _add_repo_catalog_options(show_discipline)

    show_all_for = sub.add_parser("show-all-for", help="Print one lane/addendum followed by selected disciplines")
    show_all_for.add_argument("lane", choices=LANES)
    show_all_for.add_argument("--with", dest="disciplines", nargs="+", choices=DISCIPLINES, default=[])
    _add_repo_catalog_options(show_all_for)

    discipline_path = sub.add_parser("discipline-path", help="Print path to a discipline doc")
    discipline_path.add_argument("discipline", choices=DISCIPLINES)
    _add_repo_catalog_options(discipline_path)

    sync = sub.add_parser("sync", help="Check or update generated catalog projections")
    sync.add_argument("--repo-root", default=".")
    mode = sync.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Fail when generated projections drift")
    mode.add_argument("--apply", action="store_true", help="Update generated projections")

    check_self = sub.add_parser("check-self", help="Validate this engineering-core checkout")
    check_self.add_argument("--repo-root", default=".")

    doctor = sub.add_parser("doctor", help="Diagnose one repository adoption surface")
    doctor.add_argument("--repo", default=".", help="Repository to diagnose (default: .)")
    doctor.add_argument("--format", choices=("human", "json"), default="human")
    doctor.add_argument("--repo-root", default=".", help="engineering-core checkout containing catalog.json")
    doctor.add_argument("--prefer-repo", action="store_true", help="Prefer checkout catalog.json")

    return parser


def _preferred_path(repo_path: Path, package_path: Path, prefer_repo: bool) -> Path:
    return repo_path if prefer_repo and repo_path.exists() else package_path


def main() -> None:
    args = build_parser().parse_args()

    if args.cmd == "list":
        print("\n".join(LANES))
        return
    if args.cmd == "list-disciplines":
        print("\n".join(DISCIPLINES))
        return
    if args.cmd == "list-templates":
        print("\n".join(TEMPLATES))
        return

    if args.cmd == "sync":
        repo_root = Path(args.repo_root).resolve()
        drifted = sync_catalog_projection(repo_root, apply=args.apply)
        if drifted and not args.apply:
            raise SystemExit("catalog projection differs from src/engineering_core/catalog.json; run engineering-core sync --apply")
        print("catalog projection updated" if drifted else "catalog projection is current")
        return

    if args.cmd == "check-self":
        errors = run_self_check(Path(args.repo_root))
        if errors:
            for error in errors:
                print(error)
            raise SystemExit(1)
        print("engineering-core self-check passed")
        return

    if args.cmd == "doctor":
        catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)
        report = doctor_repo(Path(args.repo), catalog)
        if args.format == "json":
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print(render_doctor_human(report))
        code = doctor_exit_code(report)
        if code:
            raise SystemExit(code)
        return

    if args.cmd == "list-profiles":
        catalog = _load_catalog(Path(args.repo_root).resolve(), args.prefer_repo)
        for profile in catalog.get("profiles", []):
            print(profile.get("id"))
        return

    if args.cmd == "catalog":
        _print_catalog(_load_catalog(Path(args.repo_root).resolve(), args.prefer_repo), pretty=args.pretty)
        return

    if args.cmd == "recommend":
        catalog = _load_catalog(Path(args.repo_root).resolve(), args.prefer_repo)
        if args.repo:
            repo_root = Path(args.repo).resolve()
            lanes, disciplines = _infer_repo_recommendation(repo_root)
            _print_recommendation_items(f"repo:{repo_root}", lanes, disciplines)
            return
        if not args.profile:
            raise SystemExit("recommend requires a profile id or --repo <path>")
        _print_recommendation(catalog, args.profile)
        return

    if args.cmd == "scan-adoption":
        if args.write and not args.json_out and not args.markdown_out:
            raise SystemExit("scan-adoption --write requires --json-out and/or --markdown-out")
        scopes = [Path(scope).resolve() for scope in (args.scope or ["."])]
        catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)
        scan = build_scan(
            scopes,
            include_packages=args.include_packages,
            include_scope_root=args.include_scope_root,
            repo_discovery=args.repo_discovery,
            catalog=catalog,
        )
        if args.write:
            _write_scan(scan, json_out=args.json_out, markdown_out=args.markdown_out)
        elif args.format == "json":
            print(json.dumps(scan, indent=2, sort_keys=True))
        else:
            print(render_markdown(scan))
        return

    repo_root = Path(args.repo_root).resolve()
    if args.cmd == "overview":
        _print_doc(_preferred_path(_repo_discipline_overview_path(repo_root), _package_discipline_overview_path(), args.prefer_repo))
        return
    if args.cmd == "show-template":
        _print_doc(_preferred_path(_repo_template_path(repo_root, args.template), _package_template_path(args.template), args.prefer_repo))
        return
    if args.cmd == "template-path":
        print(_preferred_path(_repo_template_path(repo_root, args.template), _package_template_path(args.template), args.prefer_repo))
        return
    if args.cmd == "show":
        _print_doc(_preferred_path(_repo_lane_path(repo_root, args.lane), _package_lane_path(args.lane), args.prefer_repo))
        return
    if args.cmd == "path":
        print(_preferred_path(_repo_lane_path(repo_root, args.lane), _package_lane_path(args.lane), args.prefer_repo))
        return
    if args.cmd == "show-discipline":
        if args.discipline.lower() == "readme":
            _print_doc(_preferred_path(_repo_discipline_overview_path(repo_root), _package_discipline_overview_path(), args.prefer_repo))
        else:
            _print_doc(_preferred_path(_repo_discipline_path(repo_root, args.discipline), _package_discipline_path(args.discipline), args.prefer_repo))
        return
    if args.cmd == "show-all-for":
        _print_doc(_preferred_path(_repo_lane_path(repo_root, args.lane), _package_lane_path(args.lane), args.prefer_repo))
        for discipline in args.disciplines:
            print("\n---\n")
            _print_doc(_preferred_path(_repo_discipline_path(repo_root, discipline), _package_discipline_path(discipline), args.prefer_repo))
        return
    if args.cmd == "discipline-path":
        print(_preferred_path(_repo_discipline_path(repo_root, args.discipline), _package_discipline_path(args.discipline), args.prefer_repo))
        return


if __name__ == "__main__":
    main()
