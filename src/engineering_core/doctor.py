from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from engineering_core import __version__
from engineering_core.advisor import build_request
from engineering_core.capabilities import capability_results, parse_capability_contract
from engineering_core.catalog import Catalog, load_catalog
from engineering_core.engineering_plan import compile_plan
from engineering_core.policy import parse_policy_text
from engineering_core.repository_facts import extract_repository_facts

AUTHORITY = "static diagnostic only; no command execution or authority promotion"


def _safe_text(value: object) -> str:
    text = str(value)
    raw = text.encode("utf-8")
    if len(raw) <= 4096:
        return text
    return f"[over-bound text omitted; sha256={hashlib.sha256(raw).hexdigest()}]"


def _check(identifier: str, status: str, summary: str, evidence: list[str] | None = None) -> dict[str, Any]:
    return {"id": _safe_text(identifier), "status": status, "summary": _safe_text(summary), "evidence": sorted(_safe_text(item) for item in (evidence or []))}


def _fallback_protocols() -> Any:
    return SimpleNamespace(
        engineering_plan="engineering-plan-v1",
        advice_request="engineering-advice-request-v1",
        advice_response="engineering-advice-response-v1",
        evidence_receipt="engineering-evidence-receipt-v1",
        recommendation_disposition="engineering-recommendation-disposition-v1",
    )


def _blocked_target(repo: Path, reason: object) -> dict[str, Any]:
    protocols = _fallback_protocols()
    contract = parse_capability_contract({"capability_contract": {"version": "invalid", "capabilities": {}}}, protocols)
    return {
        "schema": "engineering-doctor-v1", "authority": AUTHORITY,
        "repository": _safe_text(repo), "package_version": __version__,
        "catalog": {"version": __version__, "source": "packaged"}, "pin_posture": "absent",
        "status": "blocked",
        "checks": sorted([
            _check("advisor", "fail", "advisor request is blocked"),
            _check("capability-schemas", "fail", "capability schemas unavailable"),
            _check("catalog", "not-observed", "catalog was not inspected"),
            _check("package-version", "not-observed", "package/catalog compatibility was not inspected"),
            _check("pin", "warn", "pin posture: absent"),
            _check("plan", "fail", "plan compilation is blocked"),
            _check("policy", "not-observed", "policy was not inspected"),
            _check("target", "fail", "target path is invalid or unavailable", [_safe_text(reason)]),
        ], key=lambda item: item["id"]),
        "capabilities": capability_results(contract, protocols),
        "consumer_commands_executed": False, "external_models_invoked": False, "mutations_performed": [],
    }


def _pin(ref: str | None, version: str) -> str:
    if ref is None: return "absent"
    if ref == f"v{version}": return "released-match"
    if ref == "workspace-local-unpinned": return "workspace-local-unpinned"
    import re
    if re.fullmatch(r"v\d+\.\d+\.\d+", ref): return "released-mismatch"
    return "other"


def build_doctor(repo: Path, *, repo_root: Path | None = None, prefer_repo: bool = False) -> dict[str, Any]:
    try:
        supplied = str(repo)
        if len(supplied.encode("utf-8")) > 4096 or any(ord(char) < 32 for char in supplied):
            raise ValueError("target path exceeds bounds or contains control characters")
        root = repo.resolve()
        target_is_dir = root.is_dir()
    except (OSError, ValueError) as exc:
        return _blocked_target(repo, exc)
    checks: list[dict[str, Any]] = []
    catalog: Catalog | None = None
    policy = None
    contract = None
    plan_ok = request_ok = False
    if not target_is_dir:
        checks.append(_check("target", "fail", "target is not a readable directory", [str(root)]))
    else:
        checks.append(_check("target", "pass", "target is a readable directory", [str(root)]))
    source = "packaged"
    try:
        if prefer_repo and repo_root is not None and (repo_root.resolve() / "catalog.json").exists():
            source = "repo"
        catalog = load_catalog(repo_root, prefer_repo=prefer_repo)
        checks.append(_check("catalog", "pass", "catalog and typed protocols loaded"))
    except (OSError, ValueError) as exc:
        checks.append(_check("catalog", "fail", "catalog failed to load", [str(exc)]))
    policy_present = False
    errors: list[str] = []
    if target_is_dir:
        facts = extract_repository_facts(root)
        policy_present = facts["policy"]["present"]
        policy_text = facts["policy"]["text"]
        if policy_text is not None:
            policy, errors = parse_policy_text(policy_text)
        elif policy_present:
            errors = [item["message"] for item in facts["diagnostics"] if item.get("path") == "policy/engineering-lane.json"] or ["policy could not be read safely"]
    if errors or (policy_present and policy is None):
        checks.append(_check("policy", "fail", "policy is invalid", errors))
    else:
        checks.append(_check("policy", "pass" if policy else "warn", "policy loaded" if policy else "policy is absent"))
    pin = _pin(policy.ref if policy else None, catalog.version if catalog else __version__)
    checks.append(_check("pin", "pass" if pin == "released-match" else "warn", f"pin posture: {pin}"))
    if catalog is None:
        checks.append(_check("package-version", "fail", "package/catalog compatibility is blocked"))
    elif catalog.version != __version__:
        checks.append(_check("package-version", "fail", "package and catalog versions differ", [__version__, catalog.version]))
    else:
        checks.append(_check("package-version", "pass", "package and catalog versions match"))
    if target_is_dir and catalog is not None:
        try:
            first, second = compile_plan(root, catalog), compile_plan(root, catalog)
            plan_ok = first["status"] == second["status"] == "complete" and first["digests"]["plan_sha256"] == second["digests"]["plan_sha256"]
            checks.append(_check("plan", "pass" if plan_ok else "fail", "plan compiled deterministically" if plan_ok else "plan is incomplete or nondeterministic"))
            ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
            one, two = build_request(root, first, ids), build_request(root, second, ids)
            request_ok = plan_ok and one["request_sha256"] == two["request_sha256"]
            checks.append(_check("advisor", "pass" if request_ok else "fail", "advisor request built deterministically" if request_ok else "advisor request is blocked"))
        except (OSError, ValueError, KeyError) as exc:
            checks.extend([_check("plan", "fail", "plan compilation failed", [str(exc)]), _check("advisor", "fail", "advisor request is blocked")])
    else:
        checks.extend([_check("plan", "fail", "plan compilation is blocked"), _check("advisor", "fail", "advisor request is blocked")])
    if catalog is not None:
        contract = parse_capability_contract(policy.engineering_core if policy else {}, catalog.protocols)
        capabilities = capability_results(contract, catalog.protocols, {"planning": plan_ok, "advisor": request_ok})
        checks.append(_check("capability-schemas", "fail" if contract.status in ("invalid", "unsupported") else "pass", f"capability contract: {contract.status}"))
    else:
        fallback = _fallback_protocols()
        invalid = parse_capability_contract({"capability_contract": {"version": "invalid", "capabilities": {}}}, fallback)
        capabilities = capability_results(invalid, fallback)
        checks.append(_check("capability-schemas", "fail", "capability schemas unavailable"))
    checks.sort(key=lambda item: item["id"])
    blocked = any(item["status"] == "fail" for item in checks) or any(item.get("observation_status") == "blocked" for item in capabilities.values())
    warning = any(item["status"] in ("warn", "not-observed") for item in checks)
    declared = bool(contract and contract.declarations)
    not_observed = any(item.get("observation_status") == "not-observed" for item in capabilities.values())
    status = "blocked" if blocked else ("degraded" if warning or not declared or not_observed else "healthy")
    return {"schema": "engineering-doctor-v1", "authority": AUTHORITY, "repository": _safe_text(root), "package_version": __version__, "catalog": {"version": _safe_text(catalog.version if catalog else __version__), "source": source}, "pin_posture": pin, "status": status, "checks": checks, "capabilities": capabilities, "consumer_commands_executed": False, "external_models_invoked": False, "mutations_performed": []}
