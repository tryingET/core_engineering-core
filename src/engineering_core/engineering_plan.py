# summary: "Compiles deterministic engineering plans by resolving repository evidence, policy selections, catalog requirements, and diagnostics."
# read_when:
#   - "When changing plan selection provenance, dependency resolution, completeness rules, explanations, or plan digests."

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from engineering_core.catalog import Catalog
from engineering_core.policy import parse_policy_text
from engineering_core.repository_facts import extract_repository_facts

PLAN_SCHEMA = "engineering-plan-v1"
_DEFAULT_DISCIPLINES = ("dependency-governance", "documentation", "security-privacy", "testing", "validation")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def compile_plan(repo: Path, catalog: Catalog) -> dict[str, Any]:
    facts = extract_repository_facts(repo)
    diagnostics: list[dict[str, Any]] = list(facts["diagnostics"])
    unknowns: list[dict[str, Any]] = []
    selected_lanes: list[str] = []
    selected_disciplines: list[str] = []
    source = "inference"
    policy_ref: str | None = None
    policy_text = facts["policy"]["text"]
    if policy_text is not None:
        source = "policy"
        policy, errors = parse_policy_text(policy_text)
        for error in errors:
            diagnostics.append({"code": "policy-malformed", "message": error, "path": "policy/engineering-lane.json", "severity": "error"})
        if policy is not None:
            selected_lanes.extend(policy.lanes)
            selected_disciplines.extend(policy.disciplines)
            policy_ref = policy.ref
            raw_top = policy.raw.get("lane")
            raw_nested = policy.engineering_core.get("lane")
            if isinstance(raw_top, str) and isinstance(raw_nested, str) and raw_top != raw_nested:
                diagnostics.append({"code": "policy-contradiction", "message": f"lane is {raw_top!r} but engineering_core.lane is {raw_nested!r}", "path": "policy/engineering-lane.json", "severity": "error"})
    else:
        selected_lanes.extend(facts["inferred_lanes"])
        if selected_lanes:
            selected_disciplines.extend(_DEFAULT_DISCIPLINES)
        else:
            unknowns.append({"code": "lane-undetermined", "message": "No supported manifest or explicit policy selected a lane."})
    lane_by_id = {item.id: item for item in catalog.lanes}
    discipline_by_id = {item.id: item for item in catalog.disciplines}
    known = set(lane_by_id) | set(discipline_by_id)
    requested = set(selected_lanes) | set(selected_disciplines)
    for item_id in sorted(requested - known):
        unknowns.append({"code": "unknown-catalog-id", "id": item_id, "message": f"Catalog does not define {item_id!r}."})
    # Resolve transitive catalog requirements without silently pretending explicitly
    # omitted addendum prerequisites were selected by the consumer.
    resolved = set(requested & known)
    queue = sorted(resolved)
    dependencies: list[dict[str, Any]] = []
    while queue:
        item_id = queue.pop(0)
        item = lane_by_id.get(item_id) or discipline_by_id.get(item_id)
        if item is None:
            continue
        for requirement in sorted(item.requires):
            dependencies.append({"from": item_id, "to": requirement, "provenance": "catalog.requires"})
            if requirement not in requested:
                diagnostics.append({"code": "required-selection-missing", "id": item_id, "message": f"{item_id!r} requires {requirement!r}; requirement was added by catalog resolution.", "path": "catalog.json", "severity": "warning"})
            if requirement not in resolved:
                resolved.add(requirement)
                queue.append(requirement)
                queue.sort()
    selections = []
    for item_id in sorted(resolved):
        item = lane_by_id.get(item_id) or discipline_by_id.get(item_id)
        selections.append({
            "id": item_id,
            "kind": item.kind if item else "unknown",
            "requested": item_id in requested,
            "provenance": [{"path": "policy/engineering-lane.json" if source == "policy" else next((e["path"] for e in facts["evidence"] if e["kind"] == "manifest" and item_id in facts["inferred_lanes"]), "repository facts"), "source": source if item_id in requested else "catalog.requires"}],
        })
    catalog_digest = _digest(catalog.raw)
    omission_codes = {"file-symlink-rejected", "file-not-regular", "file-budget-exceeded", "file-unreadable"}
    status = "incomplete" if unknowns or any(item["severity"] == "error" or item["code"] in omission_codes for item in diagnostics) else "complete"
    plan: dict[str, Any] = {
        "schema": PLAN_SCHEMA,
        "authority": {"mode": "advisory", "statement": "Compiled projection of repository evidence and engineering-core catalog implications; not runtime or compliance authority."},
        "status": status,
        "source": source,
        "policy_ref": policy_ref,
        "selections": selections,
        "dependencies": sorted(dependencies, key=lambda item: (item["from"], item["to"])),
        "diagnostics": sorted(diagnostics, key=lambda item: (item["code"], item.get("path", ""), item["message"])),
        "unknowns": sorted(unknowns, key=lambda item: (item["code"], item.get("id", ""))),
        "evidence": facts["evidence"],
        "digests": {"catalog_sha256": catalog_digest, "repository_facts_sha256": facts["digest"]},
    }
    plan["digests"]["plan_sha256"] = _digest(plan)
    return plan


def explain_plan(plan: dict[str, Any], subject: str | None = None) -> dict[str, Any]:
    if subject is None:
        return {"schema": "engineering-plan-explanation-v1", "status": plan["status"], "authority": plan["authority"], "selections": plan["selections"], "diagnostics": plan["diagnostics"], "unknowns": plan["unknowns"], "plan_sha256": plan["digests"]["plan_sha256"]}
    selections = [item for item in plan["selections"] if item["id"] == subject]
    dependencies = [item for item in plan["dependencies"] if subject in (item["from"], item["to"])]
    unknowns = [item for item in plan["unknowns"] if item.get("id") == subject]
    return {"schema": "engineering-plan-explanation-v1", "subject": subject, "found": bool(selections or dependencies or unknowns), "selections": selections, "dependencies": dependencies, "unknowns": unknowns, "plan_sha256": plan["digests"]["plan_sha256"]}
