from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

CONTRACT_VERSION = "engineering-core-capabilities-v1"
CAPABILITY_NAMES = ("planning", "advisor", "closed_loop")


@dataclass(frozen=True)
class CapabilityDeclaration:
    name: str
    status: str
    schemas: dict[str, str]


@dataclass(frozen=True)
class CapabilityContract:
    status: str
    declarations: tuple[CapabilityDeclaration, ...]
    findings: tuple[dict[str, Any], ...]


def _bounded(value: object) -> str:
    text = str(value)
    raw = text.encode("utf-8")
    if len(raw) <= 4096:
        return text
    return f"[over-bound text omitted; sha256={hashlib.sha256(raw).hexdigest()}]"


def _finding(code: str, message: str, evidence: list[str] | None = None) -> dict[str, Any]:
    return {"code": _bounded(code), "severity": "error", "message": _bounded(message), "evidence": sorted(_bounded(item) for item in (evidence or []))}


def expected_schemas(protocols: Any) -> dict[str, dict[str, str]]:
    return {
        "planning": {"plan": protocols.engineering_plan},
        "advisor": {"request": protocols.advice_request, "response": protocols.advice_response},
        "closed_loop": {"receipt": protocols.evidence_receipt, "disposition": protocols.recommendation_disposition},
    }


def parse_capability_contract(engineering_core: dict[str, Any], protocols: Any) -> CapabilityContract:
    raw = engineering_core.get("capability_contract")
    if raw is None:
        return CapabilityContract("absent", (), ())
    if not isinstance(raw, dict):
        return CapabilityContract("invalid", (), (_finding("contract-invalid", "capability_contract must be an object"),))
    if set(raw) != {"version", "capabilities"}:
        return CapabilityContract("invalid", (), (_finding("contract-fields-invalid", "capability_contract fields must be exactly capabilities and version"),))
    if raw.get("version") != CONTRACT_VERSION:
        return CapabilityContract("unsupported", (), (_finding("contract-version-unsupported", "capability contract version is unsupported", [str(raw.get("version"))]),))
    values = raw.get("capabilities")
    if not isinstance(values, dict):
        return CapabilityContract("invalid", (), (_finding("capabilities-invalid", "capabilities must be an object"),))
    expected = expected_schemas(protocols)
    declarations: list[CapabilityDeclaration] = []
    findings: list[dict[str, Any]] = []
    for name in sorted(values):
        value = values[name]
        if name not in CAPABILITY_NAMES:
            findings.append(_finding("capability-unknown", f"unknown capability: {name}", [name]))
            continue
        schema_fields = {
            "planning": {"schema": "plan"},
            "advisor": {"request_schema": "request", "response_schema": "response"},
            "closed_loop": {"receipt_schema": "receipt", "disposition_schema": "disposition"},
        }[name]
        allowed = {"status", *schema_fields}
        if not isinstance(value, dict) or set(value) != allowed or value.get("status") != "declared":
            findings.append(_finding("capability-invalid", f"{name} declaration has invalid fields or status"))
            continue
        supplied = {output: value[field] for field, output in schema_fields.items()}
        if supplied != expected[name]:
            findings.append(_finding("capability-schema-invalid", f"{name} schema identifiers do not match the catalog", [str(item) for item in supplied.values()]))
            continue
        declarations.append(CapabilityDeclaration(name, "declared", supplied))
    status = "invalid" if findings else "valid"
    return CapabilityContract(status, tuple(declarations), tuple(findings))


def capability_results(contract: CapabilityContract, protocols: Any, observations: dict[str, bool] | None = None) -> dict[str, dict[str, Any]]:
    observations = observations or {}
    declared = {item.name for item in contract.declarations}
    result: dict[str, dict[str, Any]] = {}
    for name in CAPABILITY_NAMES:
        declaration_status = contract.status if contract.status in ("invalid", "unsupported") else ("valid" if name in declared else "absent")
        if declaration_status == "valid":
            observation_status = "not-observed" if name == "closed_loop" else ("observable" if observations.get(name) else "blocked")
            findings = [] if observation_status in ("observable", "not-observed") else [_finding(f"{name}-observation-blocked", f"{name} deterministic observation failed")]
        elif declaration_status == "absent":
            observation_status, findings = "not-declared", []
        else:
            observation_status, findings = "blocked", list(contract.findings)
        result[name] = {"declaration_status": declaration_status, "observation_status": observation_status, "evidence_status": "not-supplied", "schemas": expected_schemas(protocols)[name], "findings": findings}
    return result
