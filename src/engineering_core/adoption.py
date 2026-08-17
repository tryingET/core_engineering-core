from __future__ import annotations

import difflib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from engineering_core.adoption_scan import (
    ENGINEERING_DOC,
    ENGINEERING_POLICY,
    LEGACY_DOC,
    LEGACY_POLICY,
    dedupe,
    extract_policy,
    load_json,
)
from engineering_core.catalog_model import collection_entries, collection_ids

MANAGED_MARKER = "<!-- engineering-core-managed:v1 -->"
ADOPTION_SCHEMA_VERSION = "1"


@dataclass(frozen=True)
class FileChange:
    path: str
    action: str
    before: str | None
    after: str | None


@dataclass(frozen=True)
class AdoptionPlan:
    repo: str
    mode: str
    lanes: list[str]
    disciplines: list[str]
    changes: list[FileChange]
    conflicts: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.changes)

    @property
    def safe_to_apply(self) -> bool:
        return not self.conflicts

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["changed"] = self.changed
        value["safe_to_apply"] = self.safe_to_apply
        value["diff"] = render_diff(self)
        return value


def _profile(catalog: dict[str, Any], profile_id: str) -> tuple[list[str], list[str]]:
    for profile in catalog.get("profiles", []):
        if isinstance(profile, dict) and profile.get("id") == profile_id:
            return list(profile.get("lanes", [])), list(profile.get("disciplines", []))
    valid = ", ".join(
        str(profile.get("id"))
        for profile in catalog.get("profiles", [])
        if isinstance(profile, dict)
    )
    raise ValueError(f"unknown profile {profile_id!r}; valid profiles: {valid}")


def infer_repo_selection(repo_root: Path) -> tuple[list[str], list[str]]:
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
        dependencies = {
            **package.get("dependencies", {}),
            **package.get("devDependencies", {}),
        }
        if any(name in dependencies for name in ("react", "vue", "svelte", "vite", "@vitejs/plugin-react")):
            lanes.append("ts-frontend")

    disciplines = [
        "validation",
        "testing",
        "security-privacy",
        "documentation",
        "dependency-governance",
    ]
    if "ts-frontend" in lanes:
        disciplines.extend(["design-system", "accessibility"])
    if any((repo_root / name).exists() for name in ("schema", "schemas", "contracts")):
        disciplines.append("specification-and-dsls")
    return dedupe(lanes), dedupe(disciplines)


def _requirements(catalog: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for entry in collection_entries(catalog, "lanes"):
        entry_id = entry.get("id")
        raw = entry.get("requires", [])
        if isinstance(entry_id, str) and isinstance(raw, list):
            result[entry_id] = [item for item in raw if isinstance(item, str)]
    return result


def close_requirements(
    lanes: list[str], disciplines: list[str], catalog: dict[str, Any]
) -> tuple[list[str], list[str]]:
    lane_ids = set(collection_ids(catalog, "lanes"))
    discipline_ids = set(collection_ids(catalog, "disciplines"))
    selected_lanes = dedupe(lanes)
    selected_disciplines = dedupe(disciplines)
    selected = set(selected_lanes) | set(selected_disciplines)

    changed = True
    requirements = _requirements(catalog)
    while changed:
        changed = False
        for lane in list(selected_lanes):
            for requirement in requirements.get(lane, []):
                if requirement in selected:
                    continue
                if requirement in lane_ids:
                    selected_lanes.append(requirement)
                elif requirement in discipline_ids:
                    selected_disciplines.append(requirement)
                else:
                    raise ValueError(f"catalog requirement {lane!r}->{requirement!r} is unknown")
                selected.add(requirement)
                changed = True
    return dedupe(selected_lanes), dedupe(selected_disciplines)


def select_guidance(
    repo_root: Path,
    catalog: dict[str, Any],
    *,
    profile: str | None = None,
    lanes: list[str] | None = None,
    disciplines: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    selected_lanes: list[str] = []
    selected_disciplines: list[str] = []
    if profile:
        profile_lanes, profile_disciplines = _profile(catalog, profile)
        selected_lanes.extend(profile_lanes)
        selected_disciplines.extend(profile_disciplines)
    if lanes:
        selected_lanes.extend(lanes)
    if disciplines:
        selected_disciplines.extend(disciplines)
    if not selected_lanes and not selected_disciplines:
        inferred_lanes, inferred_disciplines = infer_repo_selection(repo_root)
        selected_lanes.extend(inferred_lanes)
        selected_disciplines.extend(inferred_disciplines)

    valid_lanes = set(collection_ids(catalog, "lanes"))
    valid_disciplines = set(collection_ids(catalog, "disciplines"))
    unknown_lanes = sorted(set(selected_lanes) - valid_lanes)
    unknown_disciplines = sorted(set(selected_disciplines) - valid_disciplines)
    if unknown_lanes or unknown_disciplines:
        parts = []
        if unknown_lanes:
            parts.append("unknown lanes: " + ", ".join(unknown_lanes))
        if unknown_disciplines:
            parts.append("unknown disciplines: " + ", ".join(unknown_disciplines))
        raise ValueError("; ".join(parts))
    return close_requirements(selected_lanes, selected_disciplines, catalog)


def _policy_document(
    lanes: list[str],
    disciplines: list[str],
    *,
    ref: str,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = dict(existing or {})
    engineering_core = dict(policy.get("engineering_core", {})) if isinstance(policy.get("engineering_core"), dict) else {}
    old_lanes, _lane_status, _stack, old_disciplines, _old_ref, _commands = extract_policy(policy)
    merged_lanes = dedupe([*old_lanes, *lanes])
    merged_disciplines = dedupe([*old_disciplines, *disciplines])
    engineering_core.update(
        {
            "schema_version": ADOPTION_SCHEMA_VERSION,
            "tool": "engineering-core",
            "lanes": merged_lanes,
            "disciplines": merged_disciplines,
            "ref": engineering_core.get("ref") or ref,
            "catalog_command": engineering_core.get("catalog_command") or "engineering-core catalog --pretty",
            "list_disciplines_command": engineering_core.get("list_disciplines_command") or "engineering-core list-disciplines",
            "list_templates_command": engineering_core.get("list_templates_command") or "engineering-core list-templates",
            "deviations": engineering_core.get("deviations") if isinstance(engineering_core.get("deviations"), list) else [],
        }
    )
    policy["engineering_core"] = engineering_core
    if len(merged_lanes) == 1:
        policy["lane"] = merged_lanes[0]
    elif "lane" in policy and policy["lane"] not in merged_lanes:
        policy.pop("lane", None)
    return policy


def _render_doc(lanes: list[str], disciplines: list[str], deviations: list[Any]) -> str:
    lines = [
        "---",
        'summary: "Repository-local engineering-core selections, commands, and deviations."',
        "read_when:",
        '  - "Before changing repository engineering conventions or validation commands."',
        'type: "policy"',
        "---",
        "",
        MANAGED_MARKER,
        "",
        "# Repository engineering contract",
        "",
        "## Selected lanes and addenda",
        "",
    ]
    lines.extend(f"- `{lane}`" for lane in lanes)
    if not lanes:
        lines.append("- No language lane selected; choose one before enforcement.")
    lines.extend(["", "## Selected disciplines", ""])
    lines.extend(f"- `{discipline}`" for discipline in disciplines)
    if not disciplines:
        lines.append("- No disciplines selected.")
    lines.extend(
        [
            "",
            "## Canonical local commands",
            "",
            "- Catalog: `engineering-core catalog --pretty`",
            "- List disciplines: `engineering-core list-disciplines`",
            "- List templates: `engineering-core list-templates`",
            "- Diagnose adoption: `engineering-core doctor --repo .`",
            "",
            "## Validation evidence before handoff",
            "",
            "Run the repository-local check/test/build commands selected by the applicable lane and validation discipline, then report the commands and outcomes.",
            "",
            "## Deliberate deviations",
            "",
        ]
    )
    if deviations:
        for deviation in deviations:
            if isinstance(deviation, dict):
                lines.append(f"- `{deviation.get('id', '<unnamed>')}` — {deviation.get('reason', '<reason required>')}")
    else:
        lines.append("- None recorded. Add structured entries under `engineering_core.deviations` in `policy/engineering-lane.json`.")
    lines.append("")
    return "\n".join(lines)


def _text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def _change(path: Path, repo_root: Path, before: str | None, after: str | None) -> FileChange | None:
    if before == after:
        return None
    action = "create" if before is None else "delete" if after is None else "update"
    return FileChange(str(path.relative_to(repo_root)), action, before, after)


def plan_init(
    repo_root: Path,
    catalog: dict[str, Any],
    *,
    profile: str | None = None,
    lanes: list[str] | None = None,
    disciplines: list[str] | None = None,
    ref: str = "workspace-local-unpinned",
    force: bool = False,
) -> AdoptionPlan:
    repo_root = repo_root.resolve()
    selected_lanes, selected_disciplines = select_guidance(
        repo_root,
        catalog,
        profile=profile,
        lanes=lanes,
        disciplines=disciplines,
    )
    policy_path = repo_root / ENGINEERING_POLICY
    doc_path = repo_root / ENGINEERING_DOC
    existing_policy, policy_error = load_json(policy_path)
    conflicts: list[str] = []
    if policy_error:
        conflicts.append(f"invalid existing policy: {policy_error}")
        existing_policy = None

    policy = _policy_document(selected_lanes, selected_disciplines, ref=ref, existing=existing_policy)
    engineering_core = policy["engineering_core"]
    final_lanes = list(engineering_core["lanes"])
    final_disciplines = list(engineering_core["disciplines"])
    policy_after = json.dumps(policy, indent=2, sort_keys=True) + "\n"
    policy_before = _text(policy_path)

    doc_before = _text(doc_path)
    if doc_before is not None and MANAGED_MARKER not in doc_before and not force:
        conflicts.append("docs/engineering.local.md is unmanaged; rerun with --force only after reviewing the diff")
        doc_after = doc_before
    else:
        doc_after = _render_doc(final_lanes, final_disciplines, list(engineering_core.get("deviations", [])))

    changes = [
        item
        for item in (
            _change(policy_path, repo_root, policy_before, policy_after),
            _change(doc_path, repo_root, doc_before, doc_after),
        )
        if item is not None
    ]
    return AdoptionPlan(
        repo=str(repo_root),
        mode="init",
        lanes=final_lanes,
        disciplines=final_disciplines,
        changes=changes,
        conflicts=conflicts,
    )


def plan_migration(
    repo_root: Path,
    catalog: dict[str, Any],
    *,
    ref: str = "workspace-local-unpinned",
    force: bool = False,
    remove_legacy: bool = False,
) -> AdoptionPlan:
    repo_root = repo_root.resolve()
    legacy_policy_path = repo_root / LEGACY_POLICY
    legacy_doc_path = repo_root / LEGACY_DOC
    legacy_policy, legacy_error = load_json(legacy_policy_path)
    conflicts: list[str] = []
    if legacy_error:
        conflicts.append(f"invalid legacy policy: {legacy_error}")
    lanes, _lane_status, _stack, disciplines, _legacy_ref, _commands = extract_policy(legacy_policy)
    if not lanes and not disciplines:
        lanes, disciplines = infer_repo_selection(repo_root)
    base_plan = plan_init(
        repo_root,
        catalog,
        lanes=lanes,
        disciplines=disciplines,
        ref=ref,
        force=force,
    )
    conflicts.extend(base_plan.conflicts)
    changes = list(base_plan.changes)
    if remove_legacy and not conflicts:
        for path in (legacy_policy_path, legacy_doc_path):
            before = _text(path)
            if before is not None:
                change = _change(path, repo_root, before, None)
                if change:
                    changes.append(change)
    return AdoptionPlan(
        repo=str(repo_root),
        mode="migrate",
        lanes=base_plan.lanes,
        disciplines=base_plan.disciplines,
        changes=changes,
        conflicts=dedupe(conflicts),
    )


def apply_plan(plan: AdoptionPlan) -> None:
    if plan.conflicts:
        raise ValueError("cannot apply adoption plan with conflicts")
    repo_root = Path(plan.repo)
    for change in plan.changes:
        path = repo_root / change.path
        if change.after is None:
            path.unlink(missing_ok=True)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(change.after, encoding="utf-8")


def render_diff(plan: AdoptionPlan) -> str:
    chunks: list[str] = []
    for change in plan.changes:
        before = (change.before or "").splitlines(keepends=True)
        after = (change.after or "").splitlines(keepends=True)
        chunks.extend(
            difflib.unified_diff(
                before,
                after,
                fromfile=f"a/{change.path}",
                tofile=f"b/{change.path}",
            )
        )
    return "".join(chunks)


def render_plan(plan: AdoptionPlan) -> str:
    lines = [
        f"engineering-core {plan.mode}: {plan.repo}",
        f"safe_to_apply: {str(plan.safe_to_apply).lower()}",
        f"changes: {len(plan.changes)}",
    ]
    for conflict in plan.conflicts:
        lines.append(f"conflict: {conflict}")
    diff = render_diff(plan)
    if diff:
        lines.extend(["", diff.rstrip()])
    return "\n".join(lines)
