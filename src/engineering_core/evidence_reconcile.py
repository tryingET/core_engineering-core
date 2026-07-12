from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from engineering_core.advisor import AdviceError, build_request, validate_response, validate_response_intrinsic
from engineering_core.catalog import Catalog, load_catalog, load_catalog_history
from engineering_core.closed_loop import STATES, ClosedLoopError, canonical_digest, load_record_with_bytes, validate_receipt
from engineering_core.engineering_plan import compile_plan
from engineering_core.safe_io import SafeInputError

SCHEMA = "engineering-evidence-reconciliation-v1"
AUTHORITY = "read-only owner-evidence reconciliation; not CI, release, AK, compliance, or rollout authority"
RESULTS = ("matched", "stale", "mismatched")
CAPABILITIES = ("planning", "advisor")
MAX_RECEIPTS = 1000
MAX_REPOSITORIES = 1000
HISTORICAL_CATALOGS = ("0.6.0",)
_GIT_OBJECT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


def _finding(code: str, message: str, *, severity: str = "error", evidence: list[str] | None = None) -> dict[str, Any]:
    return {"code": code, "severity": severity, "message": message, "evidence": sorted(evidence or [])}


def _git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL, timeout=10).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError(f"fixed git probe failed: {' '.join(args)}") from exc


def _git_blob(repo: Path, revision: str, relative_path: Path) -> bytes:
    text = relative_path.as_posix()
    if not text or text.startswith("-") or ":" in text or ".." in relative_path.parts or any(ord(char) < 32 for char in text):
        raise ValueError("tracked artifact path is unsafe for fixed Git blob lookup")
    try:
        return subprocess.check_output(["git", "-C", str(repo), "show", "--no-ext-diff", "--no-textconv", f"{revision}:{text}"], stderr=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("tracked artifact blob is unavailable at the stable HEAD") from exc


def _revision(repo: Path, target: str, current: str) -> tuple[str, list[dict[str, Any]]]:
    if not _GIT_OBJECT_ID.fullmatch(target):
        return "mismatched", [_finding("revision-format-invalid", "target revision must be a full lowercase Git object id")]
    try:
        resolved = _git(repo, "rev-parse", "--verify", "--end-of-options", f"{target}^{{commit}}")
    except ValueError:
        return "mismatched", [_finding("revision-unavailable", "target revision is not an available commit")]
    if resolved != target:
        return "mismatched", [_finding("revision-resolution-mismatch", "target revision did not resolve exactly")]
    if resolved == current:
        return "current", []
    try:
        subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", resolved, current], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return "mismatched", [_finding("revision-not-ancestor", "target revision is not an ancestor of current HEAD")]
    return "ancestor", []


def _artifact_path(repo: Path, reference: str) -> tuple[Path | None, list[dict[str, Any]]]:
    candidate = Path(reference)
    if candidate.is_absolute() or ".." in candidate.parts or any(ord(char) < 32 for char in reference):
        return None, [_finding("artifact-path-invalid", "artifact reference must be a bounded repository-relative path")]
    path = (repo / candidate).absolute()
    try:
        path.relative_to(repo.absolute())
    except ValueError:
        return None, [_finding("artifact-path-escape", "artifact reference escapes repository root")]
    return path, []


def _plan_artifact(value: dict[str, Any], receipt: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if value.get("schema") != "engineering-plan-v1" or not isinstance(value.get("digests"), dict):
        return [_finding("artifact-schema-unsupported", "planning receipt requires engineering-plan-v1")]
    unsigned = dict(value)
    unsigned["digests"] = dict(value["digests"])
    claimed = unsigned["digests"].pop("plan_sha256", None)
    if not isinstance(claimed, str) or canonical_digest(unsigned) != claimed:
        findings.append(_finding("plan-self-digest-mismatch", "plan artifact self-digest is invalid"))
    for key in ("plan_sha256", "catalog_sha256", "repository_facts_sha256"):
        if value["digests"].get(key) != receipt["bindings"][key]:
            findings.append(_finding("artifact-binding-mismatch", f"plan artifact {key} does not match receipt binding"))
    return findings


def _advice_artifact(value: dict[str, Any], request: dict[str, Any], receipt: dict[str, Any], *, binding_match: bool, allowed_catalog_ids: set[str]) -> list[dict[str, Any]]:
    try:
        if binding_match:
            validate_response(request, value)
        else:
            validate_response_intrinsic(value, allowed_catalog_ids)
    except (AdviceError, ClosedLoopError) as exc:
        return [_finding("advice-validation-failed", "advice artifact is invalid for its reconciliation posture", evidence=[str(exc)])]
    ids = {item.get("id") for item in value.get("recommendations", [])}
    if receipt["target"]["recommendation_id"] not in ids:
        return [_finding("recommendation-unresolved", "receipt recommendation_id is not present in the advice artifact")]
    if not binding_match:
        return [_finding("advice-request-drifted", "advice request is not revalidated because current bounded bindings drifted", severity="warning")]
    return []


def _empty_output(catalog_version: str, catalog_sha256: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "catalog": {"version": catalog_version, "sha256": catalog_sha256},
        "summary": {
            "result_counts": {key: 0 for key in RESULTS},
            "capability_counts": {key: 0 for key in CAPABILITIES},
            "owner_state_counts": {key: 0 for key in STATES},
        },
        "records": [],
        "failures": [],
        "consumer_commands_executed": False,
        "external_models_invoked": False,
        "mutations_performed": [],
    }


def reconcile_evidence(repositories: list[tuple[str, Path]], receipt_paths: list[Path], *, repo_root: Path | None = None, prefer_repo: bool = False) -> dict[str, Any]:
    try:
        current_catalog = load_catalog(repo_root, prefer_repo=prefer_repo)
    except ValueError as exc:
        output = _empty_output("unavailable", "0" * 64)
        output["failures"].append({"path": str(repo_root or "."), "code": "catalog-invalid", "message": str(exc)})
        return output
    output = _empty_output(current_catalog.version, canonical_digest(current_catalog.raw))
    if not repositories or len(repositories) > MAX_REPOSITORIES:
        output["failures"].append({"path": "", "code": "repository-count-invalid", "message": f"repository count must be between 1 and {MAX_REPOSITORIES}"})
        return output
    if not receipt_paths or len(receipt_paths) > MAX_RECEIPTS:
        output["failures"].append({"path": "", "code": "receipt-count-invalid", "message": f"receipt count must be between 1 and {MAX_RECEIPTS}"})
        return output

    candidates: list[tuple[str, Path]] = []
    for repository_id, supplied in repositories:
        lexical = supplied.absolute()
        if not repository_id or len(repository_id.encode()) > 4096 or any(ord(char) < 32 for char in repository_id):
            output["failures"].append({"path": str(lexical), "code": "repository-id-invalid", "message": "repository id is empty, over-bound, or contains controls"})
            continue
        try:
            path = supplied.resolve(strict=True)
        except OSError:
            output["failures"].append({"path": str(lexical), "code": "repository-unavailable", "message": "repository path is unavailable"})
            continue
        if not path.is_dir():
            output["failures"].append({"path": str(path), "code": "repository-unavailable", "message": "repository path is not a directory"})
            continue
        try:
            git_root = Path(_git(path, "rev-parse", "--show-toplevel")).resolve(strict=True)
        except (ValueError, OSError):
            output["failures"].append({"path": str(path), "code": "repository-git-root-unavailable", "message": "repository path is not an available Git root"})
            continue
        if git_root != path:
            output["failures"].append({"path": str(path), "code": "repository-subroot-rejected", "message": "repository mapping must equal the physical Git top-level"})
            continue
        candidates.append((repository_id, path))
    id_counts = {item: sum(repository_id == item for repository_id, _ in candidates) for item in {item[0] for item in candidates}}
    path_counts = {item: sum(path == item for _, path in candidates) for item in {item[1] for item in candidates}}
    colliding_ids = {item for item, count in id_counts.items() if count > 1}
    colliding_paths = {item for item, count in path_counts.items() if count > 1}
    for repository_id in sorted(colliding_ids):
        output["failures"].append({"path": "", "code": "repository-id-duplicate", "message": f"duplicate repository id rejected: {repository_id}"})
    for path in sorted(colliding_paths, key=str):
        output["failures"].append({"path": str(path), "code": "repository-path-duplicate", "message": "duplicate repository path rejected"})
    repo_map = {repository_id: path for repository_id, path in candidates if repository_id not in colliding_ids and path not in colliding_paths}

    parsed: list[tuple[Path, dict[str, Any], str, bytes]] = []
    for supplied in receipt_paths:
        path = supplied.absolute()
        try:
            value, raw = load_record_with_bytes(path)
            parsed.append((path, validate_receipt(value), hashlib.sha256(raw).hexdigest(), raw))
        except (ClosedLoopError, SafeInputError, OSError) as exc:
            output["failures"].append({"path": str(path), "code": "receipt-invalid", "message": str(exc)})
    key_counts: dict[tuple[str, str], int] = {}
    for _, receipt, _, _ in parsed:
        key = (receipt["target"]["repository"], receipt["receipt_id"])
        key_counts[key] = key_counts.get(key, 0) + 1
    duplicate_keys = {key for key, count in key_counts.items() if count > 1}
    for repository_id, receipt_id in sorted(duplicate_keys):
        output["failures"].append({"path": "", "code": "receipt-key-duplicate", "message": f"duplicate receipt key rejected: {repository_id}/{receipt_id}"})
    loaded = [(path, receipt, digest, raw) for path, receipt, digest, raw in parsed if (receipt["target"]["repository"], receipt["receipt_id"]) not in duplicate_keys]
    if not loaded:
        output["failures"].sort(key=lambda item: (item["path"], item["code"], item["message"]))
        return output

    binding_digests = {receipt["bindings"]["catalog_sha256"] for _, receipt, _, _ in loaded}
    if len(binding_digests) != 1:
        output["failures"].append({"path": "", "code": "catalog-bindings-mixed", "message": "one reconciliation run requires one catalog binding"})
        return output
    required_catalog_digest = next(iter(binding_digests))
    catalogs: list[Catalog] = [current_catalog]
    for version in HISTORICAL_CATALOGS:
        try:
            catalogs.append(load_catalog_history(version, repo_root, prefer_repo=prefer_repo))
        except ValueError:
            continue
    matching_catalogs = [catalog for catalog in catalogs if canonical_digest(catalog.raw) == required_catalog_digest]
    if len(matching_catalogs) != 1:
        output["failures"].append({"path": "", "code": "catalog-binding-unavailable", "message": "receipt catalog binding does not match one available catalog snapshot"})
        return output
    catalog = matching_catalogs[0]
    output["catalog"] = {"version": catalog.version, "sha256": required_catalog_digest}

    for path, receipt, receipt_sha, receipt_raw in loaded:
        repository_id = receipt["target"]["repository"]
        repo = repo_map.get(repository_id)
        if repo is None:
            output["failures"].append({"path": str(path), "code": "repository-unmapped", "message": "receipt repository id has no unique explicit mapping"})
            continue
        findings: list[dict[str, Any]] = []
        if receipt["provenance"]["owner"] != repository_id:
            findings.append(_finding("owner-identity-mismatch", "receipt provenance owner does not equal repository id"))
        try:
            receipt_rel = path.relative_to(repo)
        except ValueError:
            receipt_rel = None
            findings.append(_finding("receipt-outside-repository", "receipt path is outside the explicitly mapped repository"))
        try:
            head_before = _git(repo, "rev-parse", "HEAD")
            if receipt_rel is not None and _git_blob(repo, head_before, receipt_rel) != receipt_raw:
                findings.append(_finding("receipt-head-blob-mismatch", "receipt bytes do not match the tracked blob at stable HEAD"))
            plan = compile_plan(repo, catalog)
            second_plan = compile_plan(repo, catalog)
            relation, revision_findings = _revision(repo, receipt["target"]["revision"], head_before)
        except ValueError as exc:
            head_before, relation, revision_findings = "unavailable", "mismatched", [_finding("revision-probe-failed", str(exc))]
            plan = second_plan = {"status": "incomplete", "digests": {}}
        findings.extend(revision_findings)
        if plan["status"] != "complete" or plan["digests"].get("plan_sha256") != second_plan["digests"].get("plan_sha256"):
            findings.append(_finding("current-plan-unavailable", "current plan is incomplete or nondeterministic"))
        binding_match = all(receipt["bindings"][key] == plan["digests"].get(key) for key in ("plan_sha256", "catalog_sha256", "repository_facts_sha256"))
        observation = receipt["observations"][0] if len(receipt["observations"]) == 1 else None
        capability, artifact_rel, artifact_schema, artifact_sha = "planning", "", "unknown", ""
        if observation is None or observation["kind"] != "artifact" or observation["outcome"] not in ("observed", "passed"):
            findings.append(_finding("artifact-observation-invalid", "v0.7 requires exactly one observed or passed artifact observation"))
        else:
            artifact_rel = observation["reference"]
            artifact_path, path_findings = _artifact_path(repo, artifact_rel)
            findings.extend(path_findings)
            if artifact_path is not None:
                try:
                    artifact, artifact_raw = load_record_with_bytes(artifact_path)
                    artifact_sha = hashlib.sha256(artifact_raw).hexdigest()
                    if head_before != "unavailable" and _git_blob(repo, head_before, Path(artifact_rel)) != artifact_raw:
                        findings.append(_finding("artifact-head-blob-mismatch", "artifact bytes do not match the tracked blob at stable HEAD"))
                    artifact_schema = artifact.get("schema") if isinstance(artifact, dict) else "unknown"
                    if artifact_sha != observation["evidence_sha256"]:
                        findings.append(_finding("artifact-sha256-mismatch", "artifact bytes do not match receipt observation"))
                    if artifact_schema == "engineering-plan-v1":
                        findings.extend(_plan_artifact(artifact, receipt))
                    elif artifact_schema == "engineering-advice-response-v1":
                        capability = "advisor"
                        ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
                        request = build_request(repo, plan, ids)
                        second_request = build_request(repo, second_plan, ids)
                        if request["request_sha256"] != second_request["request_sha256"]:
                            findings.append(_finding("current-request-nondeterministic", "current advice request is nondeterministic"))
                        else:
                            findings.extend(_advice_artifact(artifact, request, receipt, binding_match=binding_match, allowed_catalog_ids=ids))
                    else:
                        findings.append(_finding("artifact-schema-unsupported", "artifact schema is not recognized by v0.7"))
                except (ClosedLoopError, SafeInputError, OSError, AdviceError, ValueError) as exc:
                    findings.append(_finding("artifact-invalid", "artifact could not be safely loaded or validated", evidence=[str(exc)]))
        try:
            head_after = _git(repo, "rev-parse", "HEAD")
            if head_before != head_after:
                findings.append(_finding("repository-changed", "repository HEAD changed during reconciliation"))
        except ValueError as exc:
            head_after = "unavailable"
            findings.append(_finding("revision-probe-failed", str(exc)))
        if any(item["severity"] == "error" for item in findings) or relation == "mismatched":
            result = "mismatched"
        elif not binding_match:
            result = "stale"
            findings.append(_finding("current-bindings-drifted", "current bounded plan bindings differ from the receipt", severity="warning"))
        else:
            result = "matched"
            relation = "advanced-compatible" if relation == "ancestor" else relation
        owner_evidence_state = receipt["state"]
        output["records"].append({
            "repository": {"id": repository_id, "path": str(repo)},
            "receipt": {"path": str(path), "receipt_id": receipt["receipt_id"], "sha256": receipt_sha, "owner_state": receipt["state"]},
            "capability": capability,
            "artifact": {"path": artifact_rel, "schema": artifact_schema, "sha256": artifact_sha},
            "revision": {"target": receipt["target"]["revision"], "current": head_after, "relation": relation},
            "bindings": receipt["bindings"],
            "result": result,
            "owner_evidence_state": owner_evidence_state,
            "findings": sorted(findings, key=lambda item: (item["code"], item["message"])),
        })
    output["records"].sort(key=lambda item: (item["repository"]["id"], item["receipt"]["receipt_id"], item["capability"], item["artifact"]["path"]))
    output["failures"].sort(key=lambda item: (item["path"], item["code"], item["message"]))
    output["summary"]["result_counts"] = {key: sum(item["result"] == key for item in output["records"]) for key in RESULTS}
    output["summary"]["capability_counts"] = {key: sum(item["capability"] == key and item["result"] == "matched" for item in output["records"]) for key in CAPABILITIES}
    output["summary"]["owner_state_counts"] = {key: sum(item["receipt"]["owner_state"] == key and item["result"] == "matched" for item in output["records"]) for key in STATES}
    return output
