# summary: "Classifies repository adoption from catalog-aware policy, local docs, legacy surfaces, semantic hints, and optional loop-validation declarations."
# read_when:
#   - "Changing adoption status taxonomy, policy/doc interpretation, semantic review signals, loop-validation checks, or scan completeness accounting."

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engineering_core.adoption_discovery import (
    BudgetedReader,
    ReadBudgetExceeded,
    rel_to,
    repo_roots,
    surface_roots,
)
from engineering_core.catalog import load_catalog as load_typed_catalog
from engineering_core.policy import parse_policy_text


ENGINEERING_DOC = Path("docs/engineering.local.md")
ENGINEERING_POLICY = Path("policy/engineering-lane.json")
LEGACY_DOC = Path("docs/tech-stack.local.md")
LEGACY_POLICY = Path("policy/stack-lane.json")

STRUCTURAL_REVIEW_STATUSES = {
    "partial",
    "missing",
    "doc-only",
    "policy-only",
    "legacy-only",
    "legacy-mixed",
    "invalid-policy",
}

LOOP_VALIDATION_VERSION = "repo-loop-validation-v1"
LOOP_VALIDATION_COMMANDS = (
    "loop-doctor",
    "loop-verify-fast",
    "loop-impact-plan",
    "loop-impact-run",
    "loop-impact-wide",
    "loop-landing-check",
)
LOOP_VALIDATION_REVIEW_STATUSES = {"invalid", "partial", "unknown-version"}


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
    has_loop_validation_contract: bool
    loop_validation_version: str | None
    loop_validation_status: str
    loop_validation_commands: list[str]
    loop_validation_missing_commands: list[str]
    loop_validation_notes: list[str]
    notes: list[str]


def load_catalog(repo_root: Path | None = None, *, prefer_repo: bool = False) -> dict[str, Any]:
    """Compatibility wrapper returning validated raw catalog metadata."""
    return load_typed_catalog(repo_root, prefer_repo=prefer_repo).raw


def catalog_ids(catalog: dict[str, Any], key: str) -> set[str]:
    return {entry["id"] for entry in catalog.get(key, []) if isinstance(entry, dict) and isinstance(entry.get("id"), str)}


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_policy(policy: dict[str, Any] | None) -> tuple[dict[str, Any], list[str], str | None, list[str], list[str], str | None, dict[str, bool]]:
    if not policy:
        return {}, [], None, [], [], None, {
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
    return ec, dedupe(lanes), lane_status, dedupe(implementation_stack), dedupe(disciplines), ref, commands


def extract_loop_validation(ec: dict[str, Any]) -> tuple[bool, str | None, str, list[str], list[str], list[str]]:
    loop_validation = ec.get("loop_validation")
    if loop_validation is None:
        return False, None, "absent", [], [], []
    if not isinstance(loop_validation, dict):
        return True, None, "invalid", [], list(LOOP_VALIDATION_COMMANDS), ["loop_validation must be an object"]

    version = loop_validation.get("version")
    if not isinstance(version, str) or not version:
        return True, None, "invalid", [], list(LOOP_VALIDATION_COMMANDS), ["loop_validation.version must be a non-empty string"]

    raw_commands = loop_validation.get("commands")
    if not isinstance(raw_commands, dict):
        return True, version, "invalid", [], list(LOOP_VALIDATION_COMMANDS), ["loop_validation.commands must be an object"]

    mapped_commands: list[str] = []
    missing_commands: list[str] = []
    notes: list[str] = []
    for command in LOOP_VALIDATION_COMMANDS:
        value = raw_commands.get(command)
        if isinstance(value, str) and value.strip():
            mapped_commands.append(command)
        else:
            missing_commands.append(command)

    unknown_commands = sorted(str(command) for command in raw_commands if command not in LOOP_VALIDATION_COMMANDS)
    if unknown_commands:
        notes.append("unknown loop validation command(s): " + ", ".join(unknown_commands))
    if version != LOOP_VALIDATION_VERSION:
        notes.append(f"unknown loop validation version: {version}")
        return True, version, "unknown-version", mapped_commands, missing_commands, notes
    if missing_commands:
        notes.append("missing loop validation command(s): " + ", ".join(missing_commands))
        return True, version, "partial", mapped_commands, missing_commands, notes
    return True, version, "complete", mapped_commands, [], notes


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


def semantic_audit(path: Path, *, scope: Path, kind: str, lanes: list[str], disciplines: list[str], has_doc: bool, reader: BudgetedReader) -> tuple[str, list[str]]:
    flags: list[str] = []
    rel_path = rel_to(path, scope).lower()
    lane_set = set(lanes)
    discipline_set = set(disciplines)
    doc_text = ""
    doc_path = path / ENGINEERING_DOC
    if doc_path.exists():
        doc_text = reader.read_text(doc_path).lower()

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


def record_for(path: Path, *, scope: Path, kind: str, valid_lanes: set[str], valid_disciplines: set[str], reader: BudgetedReader, name: str | None = None) -> AdoptionRecord:
    policy_path = path / ENGINEERING_POLICY
    parsed_policy, policy_errors = parse_policy_text(reader.read_text(policy_path)) if policy_path.exists() else (None, [])
    json_error = "; ".join(policy_errors) or None
    if parsed_policy is None:
        ec, lanes, lane_status, implementation_stack, disciplines, ref_value, commands = extract_policy(None)
    else:
        ec = parsed_policy.engineering_core
        lanes = list(parsed_policy.lanes)
        lane_status = parsed_policy.lane_status
        implementation_stack = list(parsed_policy.implementation_stack)
        disciplines = list(parsed_policy.disciplines)
        ref_value = parsed_policy.ref
        commands = parsed_policy.commands
    (
        has_loop_validation_contract,
        loop_validation_version,
        loop_validation_status,
        loop_validation_commands,
        loop_validation_missing_commands,
        loop_validation_notes,
    ) = extract_loop_validation(ec)
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
    semantic_status, semantic_flags = semantic_audit(path, scope=scope, kind=kind, lanes=lanes, disciplines=disciplines, has_doc=has_doc, reader=reader)
    notes = structural_notes + semantic_flags + loop_validation_notes
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
        has_loop_validation_contract=has_loop_validation_contract,
        loop_validation_version=loop_validation_version,
        loop_validation_status=loop_validation_status,
        loop_validation_commands=loop_validation_commands,
        loop_validation_missing_commands=loop_validation_missing_commands,
        loop_validation_notes=loop_validation_notes,
        notes=notes,
    )


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
    max_repositories: int = 1000,
    max_depth: int = 12,
    max_files: int = 100000,
    max_read_bytes: int = 10485760,
) -> dict[str, Any]:
    limits = {
        "max_repositories": max_repositories,
        "max_depth": max_depth,
        "max_files": max_files,
        "max_read_bytes": max_read_bytes,
    }
    invalid_limits = [name for name, value in limits.items() if value < 0]
    if invalid_limits:
        raise ValueError(f"scan limits must be non-negative: {', '.join(invalid_limits)}")
    loaded_catalog = catalog if catalog is not None else load_catalog()
    valid_lanes = catalog_ids(loaded_catalog, "lanes")
    valid_disciplines = catalog_ids(loaded_catalog, "disciplines")
    records: list[AdoptionRecord] = []
    scope_summaries: list[dict[str, Any]] = []
    omissions: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []
    files_visited = 0
    reader = BudgetedReader(max_read_bytes)
    repositories_inspected = 0

    for raw_scope in scopes:
        scope = raw_scope.resolve()
        try:
            repos, scope_omissions, visited = repo_roots(scope, discovery=repo_discovery, include_scope_root=include_scope_root, max_depth=max_depth, max_files=max_files - files_visited)
        except (OSError, ValueError) as exc:
            failures.append({"path": str(scope), "reason": str(exc)})
            continue
        files_visited += visited
        omissions.extend({"path": str(scope / item["path"]), "reason": item["reason"]} for item in scope_omissions)
        if len(repos) > max_repositories - repositories_inspected:
            allowed = max(0, max_repositories - repositories_inspected)
            omissions.append({"path": str(scope), "reason": "repository budget reached"})
            repos = repos[:allowed]
        repo_set = {repo.resolve() for repo in repos}
        repo_records: list[AdoptionRecord] = []
        for repo in repos:
            repositories_inspected += 1
            try:
                repo_records.append(record_for(repo, scope=scope, kind="repo", valid_lanes=valid_lanes, valid_disciplines=valid_disciplines, reader=reader))
            except ReadBudgetExceeded as exc:
                omissions.append({"path": str(repo), "reason": str(exc)})
            except OSError as exc:
                failures.append({"path": str(repo), "reason": str(exc)})
        package_records: list[AdoptionRecord] = []
        if include_packages:
            for repo in repos:
                try:
                    packages, package_omissions, package_files = surface_roots(
                        repo,
                        repo_set=repo_set,
                        surface_paths=(ENGINEERING_DOC, ENGINEERING_POLICY, LEGACY_DOC, LEGACY_POLICY),
                        max_files=max(0, max_files - files_visited),
                        max_depth=max_depth,
                    )
                    files_visited += package_files
                    omissions.extend(package_omissions)
                except OSError as exc:
                    failures.append({"path": str(repo), "reason": str(exc)})
                    continue
                for package in packages:
                    try:
                        package_records.append(
                            record_for(
                                package,
                                scope=scope,
                                kind="package",
                                valid_lanes=valid_lanes,
                                valid_disciplines=valid_disciplines,
                                reader=reader,
                                name=f"{repo.name}:{package.relative_to(repo)}",
                            )
                        )
                    except ReadBudgetExceeded as exc:
                        omissions.append({"path": str(package), "reason": str(exc)})
                    except OSError as exc:
                        failures.append({"path": str(package), "reason": str(exc)})
        scope_records = repo_records + package_records
        scope_summaries.append(
            {
                "scope": str(scope),
                "repos": len(repo_records),
                "packages": len(package_records),
                "total": len(scope_records),
                "status_counts": count(scope_records, "status"),
                "semantic_status_counts": count(scope_records, "semantic_status"),
                "loop_validation_status_counts": count(scope_records, "loop_validation_status"),
            }
        )
        records.extend(scope_records)

    structural_counts = count(records, "status")
    semantic_counts = count(records, "semantic_status")
    loop_validation_counts = count(records, "loop_validation_status")
    review_records = [
        record
        for record in records
        if record.status in STRUCTURAL_REVIEW_STATUSES
        or record.semantic_status != "ok"
        or record.loop_validation_status in LOOP_VALIDATION_REVIEW_STATUSES
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scopes": [str(scope.resolve()) for scope in scopes],
        "include_packages": include_packages,
        "include_scope_root": include_scope_root,
        "repo_discovery": repo_discovery,
        "completeness": "complete" if not omissions and not failures else "partial",
        "limits": limits,
        "usage": {"repositories": repositories_inspected, "files": files_visited, "read_bytes": reader.used},
        "omissions": omissions,
        "failures": failures,
        "summary": {
            "total": len(records),
            "repos": len([record for record in records if record.kind == "repo"]),
            "packages": len([record for record in records if record.kind == "package"]),
            "status_counts": structural_counts,
            "semantic_status_counts": semantic_counts,
            "loop_validation_status_counts": loop_validation_counts,
        },
        "total": len(records),
        "status_counts": structural_counts,
        "semantic_status_counts": semantic_counts,
        "loop_validation_status_counts": loop_validation_counts,
        "scope_summaries": scope_summaries,
        "review_candidates": [asdict(record) for record in review_records],
        "records": [asdict(record) for record in records],
    }
