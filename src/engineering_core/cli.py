# summary: Implements the engineering-core command-line interface for catalog retrieval, recommendations, plans, advice, adoption scans, and delegated capability or closed-loop commands.
# read_when:
#   - "Adding commands, changing argument contracts, output routing, or repository-versus-packaged resource selection."
from __future__ import annotations

import argparse
import json
import os
import tempfile
from importlib import resources
from pathlib import Path
from typing import Any

from engineering_core.adoption_render import render_markdown
from engineering_core.adoption_scan import build_scan
from engineering_core.advisor import AdviceError, build_request, load_json, validate_response
from engineering_core.catalog import load_catalog
from engineering_core.capability_cli import add_parsers as add_capability_parsers, run as run_capability
from engineering_core.closed_loop_cli import add_parsers as add_closed_loop_parsers, run as run_closed_loop
from engineering_core.engineering_plan import compile_plan, explain_plan
from engineering_core.evidence_reconcile_cli import add_parser as add_evidence_reconcile_parser, run as run_evidence_reconcile
from engineering_core.policy import load_policy


_PACKAGED_CATALOG = load_catalog()
LANES = _PACKAGED_CATALOG.ids("lanes")
LANE_FILES = _PACKAGED_CATALOG.files("lanes")
DISCIPLINES = _PACKAGED_CATALOG.ids("disciplines")
DISCIPLINE_FILES = _PACKAGED_CATALOG.files("disciplines")
TEMPLATES = _PACKAGED_CATALOG.ids("templates")
TEMPLATE_FILES = _PACKAGED_CATALOG.files("templates")


def _repo_lane_path(repo_root: Path, lane: str) -> Path:
    return repo_root / "lanes" / LANE_FILES[lane]


def _package_lane_path(lane: str) -> Path:
    return resources.files("engineering_core").joinpath("lanes", LANE_FILES[lane])  # type: ignore[no-any-return]


def _repo_discipline_path(repo_root: Path, discipline: str) -> Path:
    return repo_root / "disciplines" / DISCIPLINE_FILES[discipline]


def _package_discipline_path(discipline: str) -> Path:
    return resources.files("engineering_core").joinpath("disciplines", DISCIPLINE_FILES[discipline])  # type: ignore[no-any-return]


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
    return load_catalog(repo_root, prefer_repo=prefer_repo).raw


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
    policy, errors = load_policy(policy_path)
    if errors or policy is None:
        raise SystemExit(f"invalid engineering policy {policy_path}: {'; '.join(errors)}")
    return list(policy.lanes), list(policy.disciplines)


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


def main() -> None:
    parser = argparse.ArgumentParser(prog="engineering-core", description="View engineering-core lane and discipline docs.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available lanes")
    sub.add_parser("list-disciplines", help="List available cross-language disciplines")
    sub.add_parser("list-templates", help="List available adoption/review templates")

    list_profiles = sub.add_parser("list-profiles", help="List catalog recommendation profiles")
    list_profiles.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    list_profiles.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")

    catalog_cmd = sub.add_parser("catalog", help="Print the machine-readable engineering-core catalog")
    catalog_cmd.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    catalog_cmd.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    catalog_cmd.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    recommend = sub.add_parser("recommend", help="Print lane/discipline recommendation for a catalog profile or repo")
    recommend.add_argument("profile", nargs="?", help="Catalog profile id, for example browser-app or service-api")
    recommend.add_argument("--repo", help="Infer recommendation from a repository path, preferring policy/engineering-lane.json when present")
    recommend.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    recommend.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")

    plan_cmd = sub.add_parser("plan", help="Compile an advisory engineering-plan-v1 JSON projection")
    plan_cmd.add_argument("--repo", required=True, help="Repository to inspect declaratively; commands are never executed")
    plan_cmd.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    plan_cmd.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    plan_cmd.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON")

    explain = sub.add_parser("explain", help="Explain a compiled plan or one selected catalog id")
    explain.add_argument("subject", nargs="?", help="Optional lane, addendum, or discipline id")
    explain.add_argument("--repo", required=True, help="Repository to inspect declaratively; commands are never executed")
    explain.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    explain.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    explain.add_argument("--pretty", action="store_true", help="Pretty-print deterministic JSON")

    advise = sub.add_parser("advise", help="Export a bounded provider-neutral advice request or validate a response; never applies patches")
    advise.add_argument("--repo", required=True, help="Repository to inspect declaratively; commands are never executed")
    advise.add_argument("--response", help="JSON response to validate against the freshly compiled request")
    advise.add_argument("--request-out", help="Write the request JSON for an external model adapter")
    advise.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    advise.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    advise.add_argument("--max-files", type=int, default=12)
    advise.add_argument("--max-file-bytes", type=int, default=65536)
    advise.add_argument("--max-total-bytes", type=int, default=262144)
    advise.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    add_closed_loop_parsers(sub)
    add_capability_parsers(sub)
    add_evidence_reconcile_parser(sub)

    scan_adoption = sub.add_parser("scan-adoption", help="Scan one or more scopes for engineering-core adoption coverage")
    scan_adoption.add_argument("--scope", action="append", default=[], help="Scope root to scan; repeat for multiple scopes (default: .)")
    scan_adoption.add_argument("--include-packages", action="store_true", help="Also scan nested package/app/member adoption surfaces")
    scan_adoption.add_argument("--include-scope-root", action="store_true", help="Include the scope root itself when it is a git repo")
    scan_adoption.add_argument("--repo-discovery", choices=("immediate", "recursive"), default="immediate", help="Repo discovery mode within each scope")
    scan_adoption.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Stdout format when --write is not used")
    scan_adoption.add_argument("--write", action="store_true", help="Write JSON and/or markdown outputs instead of printing to stdout")
    scan_adoption.add_argument("--json-out", help="JSON output path for --write")
    scan_adoption.add_argument("--markdown-out", help="Markdown output path for --write")
    scan_adoption.add_argument("--repo-root", default=".", help="Repo root that contains ./catalog.json (default: .)")
    scan_adoption.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./catalog.json over packaged catalog")
    scan_adoption.add_argument("--max-repositories", type=int, default=1000, help="Maximum repositories to inspect (default: 1000)")
    scan_adoption.add_argument("--max-depth", type=int, default=12, help="Maximum recursive discovery depth (default: 12)")
    scan_adoption.add_argument("--max-files", type=int, default=100000, help="Maximum discovery files to visit (default: 100000)")
    scan_adoption.add_argument("--max-read-bytes", type=int, default=10485760, help="Maximum policy/doc bytes to read (default: 10485760)")

    overview = sub.add_parser("overview", help="Print the disciplines overview doc")
    overview.add_argument("--repo-root", default=".", help="Repo root that contains ./disciplines (default: .)")
    overview.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./disciplines over packaged files")

    show_template = sub.add_parser("show-template", help="Print an adoption/review template to stdout")
    show_template.add_argument("template", choices=TEMPLATES)
    show_template.add_argument("--repo-root", default=".", help="Repo root that contains ./templates (default: .)")
    show_template.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./templates over packaged files")

    template_path = sub.add_parser("template-path", help="Print filesystem path to an adoption/review template")
    template_path.add_argument("template", choices=TEMPLATES)
    template_path.add_argument("--repo-root", default=".", help="Repo root that contains ./templates (default: .)")
    template_path.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./templates over packaged files")

    show = sub.add_parser("show", help="Print a lane doc to stdout")
    show.add_argument("lane", choices=LANES)
    show.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    show.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    path_cmd = sub.add_parser("path", help="Print filesystem path to lane doc")
    path_cmd.add_argument("lane", choices=LANES)
    path_cmd.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes (default: .)")
    path_cmd.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./lanes over packaged files")

    show_discipline = sub.add_parser("show-discipline", help="Print a cross-language discipline doc to stdout; use README for the overview")
    show_discipline.add_argument("discipline", choices=(*DISCIPLINES, "README", "readme"))
    show_discipline.add_argument("--repo-root", default=".", help="Repo root that contains ./disciplines (default: .)")
    show_discipline.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./disciplines over packaged files")

    show_all_for = sub.add_parser("show-all-for", help="Print one lane/addendum followed by selected discipline docs")
    show_all_for.add_argument("lane", choices=LANES)
    show_all_for.add_argument("--with", dest="disciplines", nargs="+", choices=DISCIPLINES, default=[], help="Discipline id(s) to print after the lane")
    show_all_for.add_argument("--repo-root", default=".", help="Repo root that contains ./lanes and ./disciplines (default: .)")
    show_all_for.add_argument("--prefer-repo", action="store_true", help="Prefer repo files over packaged files")

    discipline_path = sub.add_parser("discipline-path", help="Print filesystem path to a discipline doc")
    discipline_path.add_argument("discipline", choices=DISCIPLINES)
    discipline_path.add_argument("--repo-root", default=".", help="Repo root that contains ./disciplines (default: .)")
    discipline_path.add_argument("--prefer-repo", action="store_true", help="Prefer repo ./disciplines over packaged files")

    args = parser.parse_args()

    if run_capability(args, parser):
        return

    if args.cmd == "list":
        for lane in LANES:
            print(lane)
        return

    if args.cmd == "list-disciplines":
        for discipline in DISCIPLINES:
            print(discipline)
        return

    if args.cmd == "list-templates":
        for template in TEMPLATES:
            print(template)
        return

    if args.cmd == "list-profiles":
        catalog = _load_catalog(Path(args.repo_root).resolve(), args.prefer_repo)
        for profile in catalog.get("profiles", []):
            print(profile.get("id"))
        return

    if args.cmd == "catalog":
        catalog = _load_catalog(Path(args.repo_root).resolve(), args.prefer_repo)
        _print_catalog(catalog, pretty=args.pretty)
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

    if args.cmd in ("plan", "explain"):
        catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)
        plan = compile_plan(Path(args.repo), catalog)
        output = plan if args.cmd == "plan" else explain_plan(plan, args.subject)
        print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True, separators=None if args.pretty else (",", ":")))
        return

    if args.cmd == "advise":
        catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo)
        plan = compile_plan(Path(args.repo), catalog)
        ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
        try:
            request = build_request(Path(args.repo), plan, ids, max_files=args.max_files, max_file_bytes=args.max_file_bytes, max_total_bytes=args.max_total_bytes)
            if args.request_out:
                destination = Path(args.request_out)
                payload = (json.dumps(request, indent=2, sort_keys=True) + "\n").encode("utf-8")
                temporary_name: str | None = None
                try:
                    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
                    os.chmod(temporary_name, 0o600)
                    with os.fdopen(fd, "wb") as stream:
                        stream.write(payload)
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.link(temporary_name, destination)
                except FileExistsError as exc:
                    raise AdviceError(f"request output already exists: {destination}") from exc
                except OSError as exc:
                    raise AdviceError(f"cannot write request output: {exc}") from exc
                finally:
                    if temporary_name:
                        try:
                            os.unlink(temporary_name)
                        except FileNotFoundError:
                            pass
            output = request if not args.response else {"schema": "engineering-advice-validation-v1", "valid": True, "authority": request["authority"], "response": validate_response(request, load_json(Path(args.response))), "patches_applied": False}
        except AdviceError as exc:
            raise SystemExit(f"advice rejected: {exc}") from exc
        print(json.dumps(output, indent=2 if args.pretty else None, sort_keys=True, separators=None if args.pretty else (",", ":")))
        return

    if run_closed_loop(args):
        return
    if run_evidence_reconcile(args):
        return

    if args.cmd == "scan-adoption":
        if args.write and not args.json_out and not args.markdown_out:
            raise SystemExit("scan-adoption --write requires --json-out and/or --markdown-out")
        scopes = [Path(scope).resolve() for scope in (args.scope or ["."])]
        catalog = load_catalog(Path(args.repo_root).resolve(), prefer_repo=args.prefer_repo).raw
        scan = build_scan(
            scopes,
            include_packages=args.include_packages,
            include_scope_root=args.include_scope_root,
            repo_discovery=args.repo_discovery,
            catalog=catalog,
            max_repositories=args.max_repositories,
            max_depth=args.max_depth,
            max_files=args.max_files,
            max_read_bytes=args.max_read_bytes,
        )
        if args.write:
            if args.json_out:
                json_path = Path(args.json_out)
                json_path.parent.mkdir(parents=True, exist_ok=True)
                json_path.write_text(json.dumps(scan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                print(f"wrote: {json_path}")
            if args.markdown_out:
                markdown_path = Path(args.markdown_out)
                markdown_path.parent.mkdir(parents=True, exist_ok=True)
                markdown_path.write_text(render_markdown(scan), encoding="utf-8")
                print(f"wrote: {markdown_path}")
            return
        if args.format == "json":
            print(json.dumps(scan, indent=2, sort_keys=True))
        else:
            print(render_markdown(scan))
        return

    if args.cmd == "overview":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_discipline_overview_path(repo_root)
        if args.prefer_repo and repo_path.exists():
            _print_doc(repo_path)
            return
        _print_doc(_package_discipline_overview_path())
        return

    if args.cmd == "show-template":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_template_path(repo_root, args.template)
        if args.prefer_repo and repo_path.exists():
            _print_doc(repo_path)
            return
        _print_doc(_package_template_path(args.template))
        return

    if args.cmd == "template-path":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_template_path(repo_root, args.template)
        if args.prefer_repo and repo_path.exists():
            print(str(repo_path))
            return
        print(str(_package_template_path(args.template)))
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
        if args.discipline.lower() == "readme":
            repo_path = _repo_discipline_overview_path(repo_root)
            if args.prefer_repo and repo_path.exists():
                _print_doc(repo_path)
                return
            _print_doc(_package_discipline_overview_path())
            return
        repo_path = _repo_discipline_path(repo_root, args.discipline)
        if args.prefer_repo and repo_path.exists():
            _print_doc(repo_path)
            return
        _print_doc(Path(_package_discipline_path(args.discipline)))
        return

    if args.cmd == "show-all-for":
        repo_root = Path(args.repo_root).resolve()
        lane_path = _repo_lane_path(repo_root, args.lane)
        if args.prefer_repo and lane_path.exists():
            _print_doc(lane_path)
        else:
            _print_doc(Path(_package_lane_path(args.lane)))
        for discipline in args.disciplines:
            print("\n---\n")
            discipline_path = _repo_discipline_path(repo_root, discipline)
            if args.prefer_repo and discipline_path.exists():
                _print_doc(discipline_path)
            else:
                _print_doc(Path(_package_discipline_path(discipline)))
        return

    if args.cmd == "discipline-path":
        repo_root = Path(args.repo_root).resolve()
        repo_path = _repo_discipline_path(repo_root, args.discipline)
        if args.prefer_repo and repo_path.exists():
            print(str(repo_path))
            return
        print(str(_package_discipline_path(args.discipline)))
        return
