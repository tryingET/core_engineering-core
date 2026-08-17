# summary: "Verifies owner-use evidence bundles against an explicit repository's current Git revision, focused scope snapshot, deterministic plan, and optional advisor request without mutation."
# read_when:
#   - "When changing verify-work matched, stale, or mismatched semantics and current-repository drift checks."

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from engineering_core.advisor import build_request
from engineering_core.catalog import Catalog
from engineering_core.engineering_plan import compile_plan
from engineering_core.work_bundle import WorkBundleError, validate_bundle
from engineering_core.work_packet import WorkPacketError, build_work_request, git_read, resolve_repository, scope_snapshot

SCHEMA = "engineering-work-verification-v1"
AUTHORITY = "read-only owner-use bundle verification; not execution, CI, release, AK, compliance, rollout, approval, or doctrine authority"
MAX_VERIFICATION_BYTES = 1_048_576
_SHA = re.compile(r"^[0-9a-f]{64}$")
_EFFECTS = {"consumer_commands_executed": False, "external_models_invoked": False, "patches_applied": False, "authority_promotions": [], "mutations_performed": []}


def _finding(code: str, message: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def _ancestor(repo: Path, target: str, current: str) -> tuple[str, list[dict[str, str]]]:
    if target == current:
        return "current", []
    try:
        resolved = str(git_read(repo, "rev-parse", "--verify", "--end-of-options", f"{target}^{{commit}}"))
        if resolved != target:
            return "mismatched", [_finding("revision-resolution-mismatch", "packet revision did not resolve exactly")]
        git_read(repo, "merge-base", "--is-ancestor", target, current)
        return "ancestor", []
    except WorkPacketError:
        return "mismatched", [_finding("revision-not-ancestor", "packet revision is unavailable or not an ancestor of current HEAD")]


def verify_work(repo: Path, repository_id: str, bundle: dict[str, Any], catalog: Catalog) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    try:
        bundle = validate_bundle(bundle)
        root, current = resolve_repository(repo)
    except (WorkBundleError, WorkPacketError, KeyError, TypeError, ValueError) as exc:
        return validate_verification({
            "schema": SCHEMA, "authority": AUTHORITY, "result": "mismatched",
            "repository": {"id": repository_id, "path": str(repo.absolute()), "packet_revision": "unavailable", "current_revision": "unavailable"},
            "revision_relation": "mismatched", "binding_match": False, "scope_match": False, "bundle_sha256": None,
            "findings": [_finding("input-invalid", str(exc))], "effects": dict(_EFFECTS),
        })
    packet = bundle["packet"]
    if packet["repository"]["id"] != repository_id:
        findings.append(_finding("repository-id-mismatch", "explicit repository id does not match bundle"))
    if Path(packet["repository"]["path"]) != root:
        findings.append(_finding("repository-path-mismatch", "bundle path does not match the physical Git root"))
    relation, revision_findings = _ancestor(root, packet["repository"]["revision"], current)
    findings.extend(revision_findings)
    current_snapshot: dict[str, Any] | None = None
    try:
        current_snapshot = scope_snapshot(root, list(packet["context"]["scope"]["focus_paths"]))
        scope_match = current_snapshot["scope_sha256"] == packet["scope_snapshot"]["scope_sha256"]
    except WorkPacketError as exc:
        scope_match = False
        findings.append(_finding("scope-unavailable", str(exc)))
    try:
        first, second = compile_plan(root, catalog), compile_plan(root, catalog)
        if first["status"] != "complete" or first["digests"]["plan_sha256"] != second["digests"]["plan_sha256"]:
            raise WorkPacketError("current plan is incomplete or nondeterministic")
        request_sha: str | None = None
        if packet["context"]["mode"] == "advisor-ready":
            if current_snapshot is None:
                raise WorkPacketError("current focused scope is unavailable")
            ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
            focus_files = {item["path"]: item["sha256"] for item in current_snapshot["files"] if item["state"] == "regular"}
            one = build_work_request(build_request(root, first, ids, focus_files=focus_files), packet["context"], current_snapshot, current)
            two = build_work_request(build_request(root, second, ids, focus_files=focus_files), packet["context"], current_snapshot, current)
            if one["request_sha256"] != two["request_sha256"]:
                raise WorkPacketError("current advisor request is nondeterministic")
            request_sha = one["request_sha256"]
        current_bindings = {
            "catalog_sha256": first["digests"]["catalog_sha256"],
            "repository_facts_sha256": first["digests"]["repository_facts_sha256"],
            "plan_sha256": first["digests"]["plan_sha256"],
            "request_sha256": request_sha,
        }
        binding_match = current_bindings == packet["bindings"]
    except (WorkPacketError, OSError, ValueError, KeyError) as exc:
        binding_match = False
        findings.append(_finding("bindings-unavailable", str(exc)))
    hard = any(item["severity"] == "error" for item in findings)
    if hard or relation == "mismatched":
        result = "mismatched"
    elif relation == "current" and scope_match and binding_match:
        result = "matched"
    else:
        result = "stale"
        if relation != "current": findings.append(_finding("revision-drifted", "repository HEAD advanced after preparation", "warning"))
        if not scope_match: findings.append(_finding("scope-drifted", "focused owner scope differs from the packet", "warning"))
        if not binding_match: findings.append(_finding("bindings-drifted", "current plan or request bindings differ from the packet", "warning"))
    findings.sort(key=lambda item: (item["severity"], item["code"], item["message"]))
    return validate_verification({
        "schema": SCHEMA, "authority": AUTHORITY, "result": result,
        "repository": {"id": repository_id, "path": str(root), "packet_revision": packet["repository"]["revision"], "current_revision": current},
        "revision_relation": relation, "binding_match": binding_match, "scope_match": scope_match,
        "bundle_sha256": bundle["bundle_sha256"], "findings": findings,
        "effects": dict(_EFFECTS),
    })


def validate_verification(value: Any) -> dict[str, Any]:
    try:
        serialized = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    except (TypeError, ValueError) as exc:
        raise WorkBundleError("verification is not bounded JSON") from exc
    if len(serialized) > MAX_VERIFICATION_BYTES: raise WorkBundleError("verification exceeds protocol byte budget")
    keys = {"schema", "authority", "result", "repository", "revision_relation", "binding_match", "scope_match", "bundle_sha256", "findings", "effects"}
    if not isinstance(value, dict) or set(value) != keys or value["schema"] != SCHEMA or value["authority"] != AUTHORITY or value["result"] not in ("matched", "stale", "mismatched"):
        raise WorkBundleError("verification schema or result is invalid")
    repository = value["repository"]
    if not isinstance(repository, dict) or set(repository) != {"id", "path", "packet_revision", "current_revision"} or not all(isinstance(item, str) and item and len(item.encode()) <= 4096 for item in repository.values()):
        raise WorkBundleError("verification repository is invalid")
    if value["revision_relation"] not in ("current", "ancestor", "mismatched") or type(value["binding_match"]) is not bool or type(value["scope_match"]) is not bool:
        raise WorkBundleError("verification posture fields are invalid")
    if not (value["bundle_sha256"] is None or isinstance(value["bundle_sha256"], str) and _SHA.fullmatch(value["bundle_sha256"])):
        raise WorkBundleError("verification bundle digest is invalid")
    if not isinstance(value["findings"], list): raise WorkBundleError("verification findings must be an array")
    for item in value["findings"]:
        if not isinstance(item, dict) or set(item) != {"code", "severity", "message"} or item["severity"] not in ("error", "warning") or not all(isinstance(item[key], str) and item[key] and len(item[key].encode()) <= 4096 for key in item):
            raise WorkBundleError("verification finding is invalid")
    errors = any(item["severity"] == "error" for item in value["findings"])
    if value["result"] == "matched" and (value["revision_relation"] != "current" or not value["binding_match"] or not value["scope_match"] or errors or value["bundle_sha256"] is None): raise WorkBundleError("matched verification posture is incoherent")
    if value["result"] == "stale" and (value["revision_relation"] == "mismatched" or errors or value["binding_match"] and value["scope_match"] and value["revision_relation"] == "current"): raise WorkBundleError("stale verification posture is incoherent")
    if value["result"] == "mismatched" and not (errors or value["revision_relation"] == "mismatched"): raise WorkBundleError("mismatched verification posture is incoherent")
    if value["effects"] != _EFFECTS: raise WorkBundleError("verification effect boundary is invalid")
    return value
