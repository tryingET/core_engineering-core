# summary: "Parses typed engineering-lane policy selections, command declarations, release references, and optional capability contracts."
# read_when:
#   - "Changing policy field validation, lane or discipline extraction, command mapping, capability-contract handoff, or parse errors."

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EngineeringPolicy:
    raw: dict[str, Any]
    engineering_core: dict[str, Any]
    lanes: tuple[str, ...]
    lane_status: str | None
    implementation_stack: tuple[str, ...]
    disciplines: tuple[str, ...]
    ref: str | None
    commands: dict[str, bool]
    capability_contract: Any | None


def _strings(value: Any, field: str, errors: list[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{field} must be an array")
        return []
    bad = [index for index, item in enumerate(value) if not isinstance(item, str) or not item]
    if bad:
        errors.append(f"{field} entries must be non-empty strings")
    return [item for item in value if isinstance(item, str) and item]


def parse_policy(value: Any) -> tuple[EngineeringPolicy | None, list[str]]:
    if not isinstance(value, dict):
        return None, [f"invalid json type: expected object, got {type(value).__name__}"]
    errors: list[str] = []
    ec_value = value.get("engineering_core", {})
    if not isinstance(ec_value, dict):
        errors.append("engineering_core must be an object")
        ec: dict[str, Any] = {}
    else:
        ec = ec_value
    lanes: list[str] = []
    for candidate in (value.get("lane"), ec.get("lane")):
        if candidate is not None and not isinstance(candidate, str):
            errors.append("lane must be a string")
        elif candidate:
            lanes.append(candidate)
    raw_lanes = ec.get("lanes", [])
    if not isinstance(raw_lanes, list):
        errors.append("engineering_core.lanes must be an array")
    else:
        for entry in raw_lanes:
            candidate = entry.get("lane") if isinstance(entry, dict) else entry
            if isinstance(candidate, str) and candidate:
                lanes.append(candidate)
            else:
                errors.append("engineering_core.lanes entries must be strings or objects with a lane string")
    def dedupe(items: list[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(items))
    commands = {name: isinstance(ec.get(name), str) and bool(ec.get(name).strip()) for name in (
        "catalog_command", "list_disciplines_command", "list_templates_command"
    )}
    policy = EngineeringPolicy(
        value, ec, dedupe(lanes),
        ec.get("lane_status") if isinstance(ec.get("lane_status"), str) else None,
        dedupe(_strings(ec.get("implementation_stack"), "engineering_core.implementation_stack", errors)),
        dedupe(_strings(ec.get("disciplines"), "engineering_core.disciplines", errors)),
        ec.get("ref") if isinstance(ec.get("ref"), str) else None,
        commands,
        ec.get("capability_contract"),
    )
    return policy, errors


def parse_policy_text(text: str) -> tuple[EngineeringPolicy | None, list[str]]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, [f"invalid json: {exc}"]
    return parse_policy(value)


def load_policy(path: Path) -> tuple[EngineeringPolicy | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, [f"unable to read policy: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid json: {exc}"]
    return parse_policy(value)
