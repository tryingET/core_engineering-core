from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from engineering_core.adoption_scan import (
    ENGINEERING_DOC,
    ENGINEERING_POLICY,
    LEGACY_DOC,
    LEGACY_POLICY,
    extract_policy,
    load_json,
    record_for,
)
from engineering_core.catalog_model import collection_entries, collection_ids

DIAGNOSTIC_SCHEMA_VERSION = "1"
STATUSES = ("pass", "advisory", "warn", "fail")


@dataclass(frozen=True)
class Diagnostic:
    rule_id: str
    status: str
    message: str
    evidence: list[str]
    remediation: str | None = None


def _diagnostic(
    rule_id: str,
    status: str,
    message: str,
    *,
    evidence: list[str] | None = None,
    remediation: str | None = None,
) -> Diagnostic:
    if status not in STATUSES:
        raise ValueError(f"unknown diagnostic status: {status}")
    return Diagnostic(rule_id, status, message, evidence or [], remediation)


def _rule_suffix(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", ".", value.lower()).strip(".")
    return normalized or "unknown"


def _overall_status(diagnostics: list[Diagnostic]) -> str:
    present = {diagnostic.status for diagnostic in diagnostics}
    for status in ("fail", "warn", "advisory", "pass"):
        if status in present:
            return status
    return "pass"


def _catalog_requirements(catalog: dict[str, Any]) -> dict[str, list[str]]:
    requirements: dict[str, list[str]] = {}
    for entry in collection_entries(catalog, "lanes"):
        entry_id = entry.get("id")
        raw_requires = entry.get("requires", [])
        if isinstance(entry_id, str) and isinstance(raw_requires, list):
            requirements[entry_id] = [item for item in raw_requires if isinstance(item, str)]
    return requirements


def doctor_repo(repo_root: Path, catalog: dict[str, Any]) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    diagnostics: list[Diagnostic] = []
    policy_path = repo_root / ENGINEERING_POLICY
    doc_path = repo_root / ENGINEERING_DOC
    policy, json_error = load_json(policy_path)

    valid_lanes = set(collection_ids(catalog, "lanes"))
    valid_disciplines = set(collection_ids(catalog, "disciplines"))
    record = record_for(
        repo_root,
        scope=repo_root,
        kind="repo",
        valid_lanes=valid_lanes,
        valid_disciplines=valid_disciplines,
        name=repo_root.name,
    )

    if not policy_path.exists():
        diagnostics.append(
            _diagnostic(
                "policy.missing",
                "warn",
                "No policy/engineering-lane.json file was found.",
                remediation="Create or adopt a repository policy before enforcing engineering-core selections.",
            )
        )
    elif json_error:
        diagnostics.append(
            _diagnostic(
                "policy.invalid-json",
                "fail",
                "The engineering policy is not a valid JSON object.",
                evidence=[json_error],
                remediation="Repair policy/engineering-lane.json before relying on adoption results.",
            )
        )
    else:
        diagnostics.append(_diagnostic("policy.parse", "pass", "The engineering policy is valid JSON."))

    if doc_path.exists():
        diagnostics.append(_diagnostic("docs.present", "pass", "docs/engineering.local.md is present."))
    else:
        diagnostics.append(
            _diagnostic(
                "docs.missing",
                "warn",
                "No docs/engineering.local.md file was found.",
                remediation="Add the human-readable local selection, command surface, and deviations document.",
            )
        )

    if policy_path.exists() == doc_path.exists():
        diagnostics.append(_diagnostic("adoption.surface-pair", "pass", "Policy and human-readable adoption surfaces are paired."))
    else:
        diagnostics.append(
            _diagnostic(
                "adoption.surface-pair",
                "warn",
                "Policy and human-readable adoption surfaces are incomplete as a pair.",
                evidence=[record.status],
                remediation="Keep docs/engineering.local.md and policy/engineering-lane.json together.",
            )
        )

    lanes, lane_status, _stack, disciplines, ref_value, commands = extract_policy(policy)
    unknown_lanes = sorted(set(lanes) - valid_lanes)
    unknown_disciplines = sorted(set(disciplines) - valid_disciplines)
    for lane in unknown_lanes:
        diagnostics.append(
            _diagnostic(
                "catalog.unknown-lane",
                "fail",
                f"The policy selects unknown lane {lane!r}.",
                evidence=[lane],
                remediation="Choose a lane ID from the active engineering-core catalog.",
            )
        )
    for discipline in unknown_disciplines:
        diagnostics.append(
            _diagnostic(
                "catalog.unknown-discipline",
                "fail",
                f"The policy selects unknown discipline {discipline!r}.",
                evidence=[discipline],
                remediation="Choose a discipline ID from the active engineering-core catalog.",
            )
        )
    if not unknown_lanes and not unknown_disciplines and policy is not None:
        diagnostics.append(_diagnostic("catalog.known-selections", "pass", "All selected catalog IDs are known."))

    selected = set(lanes) | set(disciplines)
    missing_requirements: list[str] = []
    for lane, requirements in _catalog_requirements(catalog).items():
        if lane not in selected:
            continue
        for requirement in requirements:
            if requirement not in selected:
                missing_requirements.append(f"{lane}->{requirement}")
                diagnostics.append(
                    _diagnostic(
                        "catalog.unsatisfied-requirement",
                        "fail",
                        f"Selected lane/addendum {lane!r} requires {requirement!r}.",
                        evidence=[lane, requirement],
                        remediation=f"Select {requirement!r} or remove {lane!r}.",
                    )
                )
    if policy is not None and not missing_requirements:
        diagnostics.append(_diagnostic("catalog.requirements", "pass", "All selected lane/addendum requirements are satisfied."))

    for command_name, present in commands.items():
        if not present:
            diagnostics.append(
                _diagnostic(
                    f"policy.missing-command.{_rule_suffix(command_name)}",
                    "warn",
                    f"The policy does not declare {command_name}.",
                    remediation="Record the reproducible engineering-core command in policy/engineering-lane.json.",
                )
            )
    if policy is not None and all(commands.values()):
        diagnostics.append(_diagnostic("policy.command-surface", "pass", "Catalog/list command fields are declared."))

    if policy is not None and not ref_value:
        diagnostics.append(
            _diagnostic(
                "policy.missing-ref",
                "warn",
                "The policy does not record the engineering-core ref it follows.",
                remediation="Record a tag, commit, workspace-local marker, or other explicit provenance reference.",
            )
        )
    elif ref_value:
        diagnostics.append(_diagnostic("policy.ref", "pass", "The engineering-core provenance ref is recorded.", evidence=[ref_value]))

    legacy_paths = [
        str(relative)
        for relative in (LEGACY_DOC, LEGACY_POLICY)
        if (repo_root / relative).exists()
    ]
    if legacy_paths:
        diagnostics.append(
            _diagnostic(
                "legacy.surfaces",
                "warn",
                "Legacy tech-stack adoption surfaces remain.",
                evidence=legacy_paths,
                remediation="Migrate the legacy files and remove them after reviewing the generated diff.",
            )
        )
    else:
        diagnostics.append(_diagnostic("legacy.surfaces", "pass", "No legacy adoption surfaces were found."))

    if doc_path.exists() and selected:
        doc_text = doc_path.read_text(encoding="utf-8", errors="replace").lower()
        absent_from_doc = sorted(item for item in selected if item.lower() not in doc_text)
        if absent_from_doc:
            diagnostics.append(
                _diagnostic(
                    "docs.selection-visibility",
                    "advisory",
                    "Some machine-selected IDs are not visible in the local engineering document.",
                    evidence=absent_from_doc,
                    remediation="Review whether the human-readable document should enumerate these selections explicitly.",
                )
            )
        else:
            diagnostics.append(_diagnostic("docs.selection-visibility", "pass", "Selected IDs are visible in the local engineering document."))

    if lane_status and not lanes:
        diagnostics.append(
            _diagnostic(
                "policy.lane-status-only",
                "advisory",
                "The policy declares a lane status without selecting a concrete lane.",
                evidence=[lane_status],
            )
        )

    for flag in record.semantic_flags:
        diagnostics.append(
            _diagnostic(
                f"semantic.{_rule_suffix(flag)}",
                "advisory",
                "The adoption scanner raised a semantic review signal.",
                evidence=[flag],
                remediation="Review the signal with repository context; semantic diagnostics are not automatic policy failures.",
            )
        )

    counts = {status: sum(item.status == status for item in diagnostics) for status in STATUSES}
    return {
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "repo": str(repo_root),
        "outcome": _overall_status(diagnostics),
        "summary": counts,
        "record_status": record.status,
        "semantic_status": record.semantic_status,
        "diagnostics": [asdict(item) for item in diagnostics],
    }


def render_human(report: dict[str, Any]) -> str:
    lines = [
        f"engineering-core doctor: {report['repo']}",
        f"outcome: {report['outcome']}",
        "",
    ]
    for diagnostic in report["diagnostics"]:
        lines.append(f"[{diagnostic['status'].upper()}] {diagnostic['rule_id']}: {diagnostic['message']}")
        for evidence in diagnostic.get("evidence", []):
            lines.append(f"  evidence: {evidence}")
        if diagnostic.get("remediation"):
            lines.append(f"  remediation: {diagnostic['remediation']}")
    lines.extend(["", f"summary: {json.dumps(report['summary'], sort_keys=True)}"])
    return "\n".join(lines)


def exit_code(report: dict[str, Any]) -> int:
    return 1 if report["summary"].get("fail", 0) else 0
