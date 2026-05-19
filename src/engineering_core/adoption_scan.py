from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import Any


ENGINEERING_DOC = Path("docs/engineering.local.md")
ENGINEERING_POLICY = Path("policy/engineering-lane.json")
LEGACY_DOC = Path("docs/tech-stack.local.md")
LEGACY_POLICY = Path("policy/stack-lane.json")

DEFAULT_SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".autoresearch",
    ".autoresearch-worktrees",
    ".migration-backup",
    ".mypy_cache",
    ".ontology",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp",
    ".venv",
    ".worktrees",
    "__pycache__",
    "archive",
    "backups",
    "bak",
    "build",
    "dist",
    "node_modules",
    "out",
    "target",
    "vendor",
    "venv",
}

CONTROL_DIR_NAMES = {
    "contracts",
    "diary",
    "docs",
    "governance",
    "ontology",
    "policy",
    "scripts",
    "tools",
}

STRUCTURAL_REVIEW_STATUSES = {
    "partial",
    "missing",
    "doc-only",
    "policy-only",
    "legacy-only",
    "legacy-mixed",
    "invalid-policy",
}


@dataclass
class AdoptionRecord:
    scope: str
    name: str
    path: str
    kind: str
    status: str
    has_engineering_doc: bool
    has_engineering_policy: bool
    has_legacy_doc: bool
    has_legacy_policy: bool
    has_catalog_command: bool
    has_list_disciplines_command: bool
    has_list_templates_command: bool
    lanes: list[str]
    lane_status: str | None
    implementation_stack: list[str]
    disciplines: list[str]
    ref: str | None
    has_justfile: bool
    structural_notes: list[str]
    semantic_status: str
    semantic_flags: list[str]
    notes: list[str]


def load_catalog(repo_root: Path | None = None, *, prefer_repo: bool = False) -> dict[str, Any]:
    if repo_root is not None and prefer_repo:
        repo_catalog = repo_root / "catalog.json"
        if repo_catalog.exists():
            return json.loads(repo_catalog.read_text(encoding="utf-8"))
    catalog_path = resources.files("engineering_core").joinpath("catalog.json")
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def catalog_ids(catalog: dict[str, Any], key: str) -> set[str]:
    return {entry["id"] for entry in catalog.get(key, []) if isinstance(entry, dict) and isinstance(entry.get("id"), str)}


def rel_to(path: Path, scope: Path) -> str:
    try:
        return str(path.resolve().relative_to(scope.resolve())) or "."
    except ValueError:
        return str(path.resolve())


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"invalid json: {exc}"
    if not isinstance(value, dict):
        return None, f"invalid json type: expected object, got {type(value).__name__}"
    return value, None


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_policy(policy: dict[str, Any] | None) -> tuple[list[str], str | None, list[str], list[str], str | None, dict[str, bool]]:
    if not policy:
        return [], None, [], [], None, {
            "catalog_command": False,
            "list_disciplines_command": False,
            "list_templates_command": False,
        }
    ec = policy.get("engineering_core", {}) if isinstance(policy.get("engineering_core", {}), dict) else {}
    lanes: list[str] = []
    if isinstance(policy.get("lane"), str):
        lanes.append(policy["lane"])
    if isinstance(ec.get("lane"), str):
        lanes.append(ec["lane"])
    for entry in ec.get("lanes", []):
        if isinstance(entry, str):
            lanes.append(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("lane"), str):
            lanes.append(entry["lane"])
    lane_status = ec.get("lane_status") if isinstance(ec.get("lane_status"), str) else None
    raw_stack = ec.get("implementation_stack", [])
    implementation_stack = [item for item in raw_stack if isinstance(item, str)] if isinstance(raw_stack, list) else []
    disciplines = [d for d in ec.get("disciplines", []) if isinstance(d, str)]
    ref = ec.get("ref") if isinstance(ec.get("ref"), str) else None
    commands = {
        "catalog_command": isinstance(ec.get("catalog_command"), str) and bool(ec.get("catalog_command")),
        "list_disciplines_command": isinstance(ec.get("list_disciplines_command"), str) and bool(ec.get("list_disciplines_command")),
        "list_templates_command": isinstance(ec.get("list_templates_command"), str) and bool(ec.get("list_templates_command")),
    }
    return dedupe(lanes), lane_status, dedupe(implementation_stack), dedupe(disciplines), ref, commands


def classify(
    *,
    has_doc: bool,
    has_policy: bool,
    has_legacy_doc: bool,
    has_legacy_policy: bool,
    has_all_commands: bool,
    lanes: list[str],
    lane_status: str | None,
    disciplines: list[str],
    json_error: str | None,
    unknown_lanes: list[str],
    unknown_disciplines: list[str],
) -> tuple[str, list[str]]:
    notes: list[str] = []
    if json_error:
        notes.append(json_error)
        return "invalid-policy", notes
    if has_legacy_doc or has_legacy_policy:
        notes.append("legacy tech-stack surface still present")
    if unknown_lanes:
        notes.append("unknown lane(s): " + ", ".join(unknown_lanes))
    if unknown_disciplines:
        notes.append("unknown discipline(s): " + ", ".join(unknown_disciplines))

    has_current = has_doc or has_policy
    has_legacy = has_legacy_doc or has_legacy_policy
    if not has_current and has_legacy:
        return "legacy-only", notes
    if has_current and has_legacy:
        return "legacy-mixed", notes
    if not has_current:
        return "missing", notes
    if has_doc and not has_policy:
        notes.append("docs/engineering.local.md exists without policy/engineering-lane.json")
        return "doc-only", notes
    if has_policy and not has_doc:
        notes.append("policy/engineering-lane.json exists without docs/engineering.local.md")
        return "policy-only", notes

    if has_all_commands and (lanes or lane_status) and disciplines and not unknown_lanes and not unknown_disciplines:
        return "adopted", notes
    if not has_all_commands:
        notes.append("missing one or more catalog/list command fields")
    if not lanes and not lane_status:
        notes.append("no lane declared")
    if not disciplines:
        notes.append("no disciplines declared")
    return "partial", notes


def semantic_audit(path: Path, *, scope: Path, kind: str, lanes: list[str], disciplines: list[str], has_doc: bool) -> tuple[str, list[str]]:
    flags: list[str] = []
    rel_path = rel_to(path, scope).lower()
    lane_set = set(lanes)
    discipline_set = set(disciplines)
    doc_text = ""
    doc_path = path / ENGINEERING_DOC
    if doc_path.exists():
        doc_text = doc_path.read_text(encoding="utf-8", errors="replace").lower()

    def missing(discipline: str, reason: str) -> None:
        explicitly_not_selected = discipline in doc_text and ("not selected" in doc_text or "not selected by default" in doc_text)
        if discipline not in discipline_set and not explicitly_not_selected:
            flags.append(f"missing_expected_discipline:{discipline}:{reason}")

    if not has_doc:
        flags.append("missing_engineering_doc_for_semantic_review")
    elif "validation" not in doc_text and "canonical local commands" not in doc_text and "validate" not in doc_text:
        flags.append("doc_lacks_validation_expectations")

    if "ts-frontend" in lane_set or any(token in rel_path for token in ("ui", "web", "frontend", "visual", "viz")):
        missing("accessibility", "ui_or_frontend_surface")
        missing("design-system", "ui_or_frontend_surface")

    if any(token in rel_path for token in ("dependency", "quality", "security", "redteam")):
        missing("dependency-governance", "dependency_or_quality_surface")
        missing("security-privacy", "dependency_or_quality_surface")

    if any(token in rel_path for token in ("runtime", "trace", "observability", "server", "api", "service", "orchestrator")):
        missing("observability", "runtime_or_service_surface")

    if any(token in rel_path for token in ("local", "data", "db", "database", "persistence", "store")):
        missing("local-first-data", "local_data_or_persistence_surface")

    if any(token in rel_path for token in ("contract", "schema", "dsl", "ontology", "policy", "quality")):
        missing("specification-and-dsls", "schema_contract_policy_surface")

    if "rust-build-graph" in lane_set:
        if "rust" not in lane_set:
            flags.append("rust_build_graph_without_rust_lane")
        if "build-graph-acceleration" not in discipline_set:
            flags.append("rust_build_graph_without_build_graph_discipline")
        if doc_text and not all(term in doc_text for term in ("conditional", "cargo")):
            flags.append("rust_build_graph_doc_lacks_conditional_cargo_language")

    if "build-graph-acceleration" in discipline_set:
        if not any(term in doc_text for term in ("conditional", "measured", "bottleneck", "evidence-gated")):
            flags.append("build_graph_discipline_not_clearly_evidence_gated_in_doc")

    if kind == "package" and not discipline_set:
        flags.append("package_policy_has_no_selected_disciplines")

    if not flags:
        return "ok", []
    if any(flag.startswith("missing_expected_discipline") for flag in flags):
        return "likely-incomplete", flags
    return "needs-review", flags


def record_for(path: Path, *, scope: Path, kind: str, valid_lanes: set[str], valid_disciplines: set[str], name: str | None = None) -> AdoptionRecord:
    policy_path = path / ENGINEERING_POLICY
    policy, json_error = load_json(policy_path)
    lanes, lane_status, implementation_stack, disciplines, ref_value, commands = extract_policy(policy)
    has_doc = (path / ENGINEERING_DOC).exists()
    has_policy = policy_path.exists()
    has_legacy_doc = (path / LEGACY_DOC).exists()
    has_legacy_policy = (path / LEGACY_POLICY).exists()
    unknown_lanes = [lane for lane in lanes if lane not in valid_lanes]
    unknown_disciplines = [discipline for discipline in disciplines if discipline not in valid_disciplines]
    has_all_commands = all(commands.values())
    status, structural_notes = classify(
        has_doc=has_doc,
        has_policy=has_policy,
        has_legacy_doc=has_legacy_doc,
        has_legacy_policy=has_legacy_policy,
        has_all_commands=has_all_commands,
        lanes=lanes,
        lane_status=lane_status,
        disciplines=disciplines,
        json_error=json_error,
        unknown_lanes=unknown_lanes,
        unknown_disciplines=unknown_disciplines,
    )
    semantic_status, semantic_flags = semantic_audit(path, scope=scope, kind=kind, lanes=lanes, disciplines=disciplines, has_doc=has_doc)
    notes = structural_notes + semantic_flags
    path_rel = rel_to(path, scope)
    return AdoptionRecord(
        scope=str(scope.resolve()),
        name=name or path.name,
        path=path_rel,
        kind=kind,
        status=status,
        has_engineering_doc=has_doc,
        has_engineering_policy=has_policy,
        has_legacy_doc=has_legacy_doc,
        has_legacy_policy=has_legacy_policy,
        has_catalog_command=commands["catalog_command"],
        has_list_disciplines_command=commands["list_disciplines_command"],
        has_list_templates_command=commands["list_templates_command"],
        lanes=lanes,
        lane_status=lane_status,
        implementation_stack=implementation_stack,
        disciplines=disciplines,
        ref=ref_value,
        has_justfile=(path / "Justfile").exists() or (path / "justfile").exists(),
        structural_notes=structural_notes,
        semantic_status=semantic_status,
        semantic_flags=semantic_flags,
        notes=notes,
    )


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_SKIP_DIR_NAMES or path.name.startswith(".tmp") or path.name.endswith(".backup")


def has_git_marker(path: Path) -> bool:
    return (path / ".git").exists()


def immediate_repo_roots(scope: Path, *, include_scope_root: bool) -> list[Path]:
    repos: list[Path] = []
    if include_scope_root and has_git_marker(scope):
        repos.append(scope)
    if not scope.exists():
        return repos
    for child in sorted(scope.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or should_skip_dir(child) or child.name in CONTROL_DIR_NAMES:
            continue
        if has_git_marker(child):
            repos.append(child)
    return repos


def recursive_repo_roots(scope: Path, *, include_scope_root: bool) -> list[Path]:
    repos: list[Path] = []
    if not scope.exists():
        return repos
    for root, dirs, files in os.walk(scope):
        root_path = Path(root)
        has_marker = ".git" in dirs or ".git" in files
        dirs[:] = [d for d in dirs if not should_skip_dir(root_path / d)]
        if root_path == scope and not include_scope_root:
            pass
        elif has_marker:
            repos.append(root_path)
    return sorted(set(repos), key=lambda p: rel_to(p, scope))


def repo_roots(scope: Path, *, discovery: str, include_scope_root: bool) -> list[Path]:
    if not scope.exists():
        raise FileNotFoundError(f"scan scope does not exist: {scope}")
    if discovery == "recursive":
        repos = recursive_repo_roots(scope, include_scope_root=include_scope_root)
    elif discovery == "immediate":
        repos = immediate_repo_roots(scope, include_scope_root=include_scope_root)
    else:
        raise ValueError(f"unknown repo discovery mode: {discovery}")
    if not repos and not include_scope_root and has_git_marker(scope):
        return [scope]
    return repos


def is_under(path: Path, ancestor: Path) -> bool:
    try:
        path.resolve().relative_to(ancestor.resolve())
        return True
    except ValueError:
        return False


def surface_roots(repo: Path, *, repo_set: set[Path]) -> list[Path]:
    roots: set[Path] = set()
    repo_resolved = repo.resolve()
    for relative_file in (ENGINEERING_DOC, ENGINEERING_POLICY, LEGACY_DOC, LEGACY_POLICY):
        for surface in repo.rglob(str(relative_file)):
            rel_surface = surface.relative_to(repo)
            if any(should_skip_dir(Path(part)) for part in rel_surface.parts):
                continue
            root = surface.parent.parent
            root_resolved = root.resolve()
            if root_resolved == repo_resolved:
                continue
            nested_repo_owner = False
            for other_repo in repo_set:
                # Only skip surfaces owned by a git repo nested inside this repo.
                # Ancestor scope roots should not steal package/member surfaces.
                if other_repo != repo_resolved and is_under(other_repo, repo_resolved) and is_under(root_resolved, other_repo):
                    nested_repo_owner = True
                    break
            if not nested_repo_owner:
                roots.add(root)
    pruned_roots: list[Path] = []
    for root in sorted(roots, key=lambda p: (len(p.parts), rel_to(p, repo))):
        if any(is_under(root, ancestor) for ancestor in pruned_roots):
            continue
        pruned_roots.append(root)
    return sorted(pruned_roots, key=lambda p: rel_to(p, repo))


def count(records: list[AdoptionRecord], attr: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(getattr(record, attr))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def build_scan(
    scopes: list[Path],
    *,
    include_packages: bool = False,
    include_scope_root: bool = False,
    repo_discovery: str = "immediate",
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    loaded_catalog = catalog if catalog is not None else load_catalog()
    valid_lanes = catalog_ids(loaded_catalog, "lanes")
    valid_disciplines = catalog_ids(loaded_catalog, "disciplines")
    records: list[AdoptionRecord] = []
    scope_summaries: list[dict[str, Any]] = []

    for raw_scope in scopes:
        scope = raw_scope.resolve()
        repos = repo_roots(scope, discovery=repo_discovery, include_scope_root=include_scope_root)
        repo_set = {repo.resolve() for repo in repos}
        repo_records = [record_for(repo, scope=scope, kind="repo", valid_lanes=valid_lanes, valid_disciplines=valid_disciplines) for repo in repos]
        package_records: list[AdoptionRecord] = []
        if include_packages:
            for repo in repos:
                for package in surface_roots(repo, repo_set=repo_set):
                    package_records.append(
                        record_for(
                            package,
                            scope=scope,
                            kind="package",
                            valid_lanes=valid_lanes,
                            valid_disciplines=valid_disciplines,
                            name=f"{repo.name}:{package.relative_to(repo)}",
                        )
                    )
        scope_records = repo_records + package_records
        scope_summaries.append(
            {
                "scope": str(scope),
                "repos": len(repo_records),
                "packages": len(package_records),
                "total": len(scope_records),
                "status_counts": count(scope_records, "status"),
                "semantic_status_counts": count(scope_records, "semantic_status"),
            }
        )
        records.extend(scope_records)

    structural_counts = count(records, "status")
    semantic_counts = count(records, "semantic_status")
    review_records = [record for record in records if record.status in STRUCTURAL_REVIEW_STATUSES or record.semantic_status != "ok"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scopes": [str(scope.resolve()) for scope in scopes],
        "include_packages": include_packages,
        "include_scope_root": include_scope_root,
        "repo_discovery": repo_discovery,
        "summary": {
            "total": len(records),
            "repos": len([record for record in records if record.kind == "repo"]),
            "packages": len([record for record in records if record.kind == "package"]),
            "status_counts": structural_counts,
            "semantic_status_counts": semantic_counts,
        },
        "total": len(records),
        "status_counts": structural_counts,
        "semantic_status_counts": semantic_counts,
        "scope_summaries": scope_summaries,
        "review_candidates": [asdict(record) for record in review_records],
        "records": [asdict(record) for record in records],
    }
