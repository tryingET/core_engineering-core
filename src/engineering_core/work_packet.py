# summary: "Builds and validates deterministic owner-use work packets bound to explicit task context, repository identity, Git revision, scoped bytes, plans, and optional advisor requests."
# read_when:
#   - "When changing prepare-work context, packet schemas, repository snapshots, or advisor-ready packet bindings."

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any

from engineering_core.advisor import build_request
from engineering_core.catalog import Catalog
from engineering_core.closed_loop import canonical_digest
from engineering_core.engineering_plan import compile_plan
from engineering_core.safe_git import SafeGitError, read_git
from engineering_core.safe_io import SafeInputError, read_bounded_bytes, validate_nofollow_parent

CONTEXT_SCHEMA = "engineering-work-context-v1"
PACKET_SCHEMA = "engineering-work-packet-v1"
WORK_REQUEST_SCHEMA = "engineering-work-advice-request-v1"
AUTHORITY = "owner-use preparation projection; not execution, CI, release, AK, compliance, or approval authority"
MODES = ("plan-only", "advisor-ready")
MAX_FOCUS_PATHS = 100
MAX_FOCUS_FILE_BYTES = 1_048_576
MAX_FOCUS_TOTAL_BYTES = 4_194_304
MAX_PACKET_BYTES = 4_194_304
_GIT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


class WorkPacketError(ValueError):
    pass


def _finite_json(value: Any, where: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise WorkPacketError(f"{where} contains a non-finite number")
    if isinstance(value, dict):
        for item in value.values(): _finite_json(item, where)
    elif isinstance(value, list):
        for item in value: _finite_json(item, where)


def _exact(value: Any, keys: set[str], where: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise WorkPacketError(f"{where} must contain exactly: {', '.join(sorted(keys))}")


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.encode("utf-8")) > 4096 or any(ord(char) < 32 for char in value):
        raise WorkPacketError(f"{where} must be bounded text without controls")
    return value


def _texts(value: Any, where: str, *, limit: int) -> list[str]:
    if not isinstance(value, list) or len(value) > limit:
        raise WorkPacketError(f"{where} must be an array with at most {limit} entries")
    return [_text(item, f"{where} item") for item in value]


def _relative_path(value: Any, where: str) -> str:
    text = _text(value, where)
    path = PurePosixPath(text)
    if path.is_absolute() or text.startswith(("-", ":", "~")) or ".." in path.parts or text in (".", ""):
        raise WorkPacketError(f"{where} must be a safe repository-relative path")
    return path.as_posix()


def validate_context(value: Any) -> dict[str, Any]:
    _exact(value, {"schema", "authority", "repository_id", "work", "mode", "scope", "provenance"}, "context")
    if value["schema"] != CONTEXT_SCHEMA:
        raise WorkPacketError("unsupported work context schema")
    if value["authority"] != "owner-supplied task context; repository and task authorities remain external":
        raise WorkPacketError("invalid work context authority boundary")
    _text(value["repository_id"], "repository_id")
    _exact(value["work"], {"id", "title", "objective"}, "work")
    for key in value["work"]:
        _text(value["work"][key], f"work.{key}")
    if value["mode"] not in MODES:
        raise WorkPacketError("mode must be plan-only or advisor-ready")
    _exact(value["scope"], {"focus_paths", "constraints", "validation"}, "scope")
    paths = [_relative_path(item, "scope.focus_paths item") for item in _texts(value["scope"]["focus_paths"], "scope.focus_paths", limit=MAX_FOCUS_PATHS)]
    if len(paths) != len(set(paths)):
        raise WorkPacketError("duplicate focus path rejected")
    _texts(value["scope"]["constraints"], "scope.constraints", limit=100)
    _texts(value["scope"]["validation"], "scope.validation", limit=100)
    _exact(value["provenance"], {"owner", "owner_type", "produced_at", "source"}, "provenance")
    for key in value["provenance"]:
        _text(value["provenance"][key], f"provenance.{key}")
    if value["provenance"]["owner"] != value["repository_id"]:
        raise WorkPacketError("context provenance owner must equal repository_id")
    return value


def git_read(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    try:
        return read_git(repo, *args, binary=binary)
    except SafeGitError as exc:
        raise WorkPacketError(str(exc)) from exc


def resolve_repository(repo: Path) -> tuple[Path, str]:
    try:
        root = repo.resolve(strict=True)
    except OSError as exc:
        raise WorkPacketError("repository path is unavailable") from exc
    if not root.is_dir():
        raise WorkPacketError("repository path is not a directory")
    git_root = Path(str(git_read(root, "rev-parse", "--show-toplevel"))).resolve(strict=True)
    if git_root != root:
        raise WorkPacketError("repository path must equal the physical Git top-level")
    revision = str(git_read(root, "rev-parse", "HEAD"))
    if not _GIT_ID.fullmatch(revision):
        raise WorkPacketError("repository HEAD is not a full lowercase Git commit id")
    return root, revision


def scope_snapshot(repo: Path, focus_paths: list[str]) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    total = 0
    for relative in focus_paths:
        path = repo / relative
        try:
            validate_nofollow_parent(path)
            if not os.path.lexists(path):
                files.append({"path": relative, "state": "absent", "bytes": 0, "sha256": None})
                continue
            raw = read_bounded_bytes(path, max_bytes=MAX_FOCUS_FILE_BYTES)
        except SafeInputError as exc:
            raise WorkPacketError(f"focus path rejected: {relative}: {exc}") from exc
        total += len(raw)
        if total > MAX_FOCUS_TOTAL_BYTES:
            raise WorkPacketError("focus file total byte budget exceeded")
        files.append({"path": relative, "state": "regular", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    status = git_read(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *focus_paths, binary=True)
    if not isinstance(status, bytes) or len(status) > 1_048_576:
        raise WorkPacketError("bounded Git status output exceeded")
    snapshot: dict[str, Any] = {
        "focus_paths": focus_paths,
        "files": files,
        "git_status_sha256": hashlib.sha256(status).hexdigest(),
        "git_status_bytes": len(status),
    }
    snapshot["scope_sha256"] = canonical_digest(snapshot)
    return snapshot


def _validate_snapshot(value: Any, focus_paths: list[str]) -> dict[str, Any]:
    _exact(value, {"focus_paths", "files", "git_status_sha256", "git_status_bytes", "scope_sha256"}, "scope_snapshot")
    if value["focus_paths"] != focus_paths or not isinstance(value["files"], list) or len(value["files"]) != len(focus_paths):
        raise WorkPacketError("scope snapshot does not match context focus paths")
    total_bytes = 0
    for expected, item in zip(focus_paths, value["files"]):
        _exact(item, {"path", "state", "bytes", "sha256"}, "scope_snapshot file")
        if item["path"] != expected or item["state"] not in ("regular", "absent") or type(item["bytes"]) is not int or item["bytes"] < 0:
            raise WorkPacketError("scope snapshot file entry is invalid")
        if item["state"] == "regular" and (not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or item["bytes"] > MAX_FOCUS_FILE_BYTES):
            raise WorkPacketError("regular scope snapshot file requires bounded bytes and sha256")
        total_bytes += item["bytes"]
        if item["state"] == "absent" and (item["sha256"] is not None or item["bytes"] != 0):
            raise WorkPacketError("absent scope snapshot file cannot carry bytes")
    if total_bytes > MAX_FOCUS_TOTAL_BYTES or not isinstance(value["git_status_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["git_status_sha256"]) or type(value["git_status_bytes"]) is not int or not 0 <= value["git_status_bytes"] <= 1_048_576:
        raise WorkPacketError("scope snapshot byte or Git status metadata is invalid")
    unsigned = dict(value); claimed = unsigned.pop("scope_sha256")
    if not isinstance(claimed, str) or canonical_digest(unsigned) != claimed:
        raise WorkPacketError("scope snapshot self-digest mismatch")
    return value


def _request_digest(request: dict[str, Any], plan: dict[str, Any], context: dict[str, Any], snapshot: dict[str, Any], revision: str) -> str:
    required = {"schema", "authority", "plan", "allowed_catalog_ids", "evidence", "budgets", "safeguards", "prompt", "work", "request_sha256"}
    _exact(request, required, "work advice request")
    if request["schema"] != WORK_REQUEST_SCHEMA or request["authority"] != "advisory-only; owner review required; never execute or apply patches" or request["plan"] != plan:
        raise WorkPacketError("work advice request schema, authority, or plan binding is invalid")
    work = request["work"]
    _exact(work, {"context", "context_sha256", "scope_sha256", "repository_revision", "bounded_work_plan", "work_binding_sha256"}, "work advice binding")
    if work["context"] != context or work["context_sha256"] != canonical_digest(context) or work["scope_sha256"] != snapshot["scope_sha256"] or work["repository_revision"] != revision:
        raise WorkPacketError("work advice context or scope binding mismatch")
    binding = {key: work[key] for key in ("context_sha256", "scope_sha256", "repository_revision")}
    binding["plan_sha256"] = plan["digests"]["plan_sha256"]
    if work["work_binding_sha256"] != canonical_digest(binding):
        raise WorkPacketError("work advice transitive binding mismatch")
    bounded_plan = work["bounded_work_plan"]
    _exact(bounded_plan, {"schema", "objective", "focus_paths", "constraints", "validation", "stop_conditions", "next_authority"}, "bounded work plan")
    if bounded_plan["schema"] != "engineering-bounded-work-plan-v1" or bounded_plan["objective"] != context["work"]["objective"] or bounded_plan["focus_paths"] != context["scope"]["focus_paths"] or bounded_plan["constraints"] != context["scope"]["constraints"] or bounded_plan["validation"] != context["scope"]["validation"]:
        raise WorkPacketError("bounded work plan does not match owner context")
    _texts(bounded_plan["stop_conditions"], "bounded work plan stop_conditions", limit=20); _text(bounded_plan["next_authority"], "bounded work plan next_authority")
    allowed = request["allowed_catalog_ids"]
    if not isinstance(allowed, list) or allowed != sorted(set(allowed)) or not all(isinstance(item, str) and item for item in allowed):
        raise WorkPacketError("work advice allowed catalog ids are invalid")
    evidence = request["evidence"]
    if not isinstance(evidence, list) or len(evidence) > 12:
        raise WorkPacketError("work advice evidence is invalid")
    evidence_ids: set[str] = set(); evidence_bytes = 0
    for item in evidence:
        _exact(item, {"id", "path", "content", "bytes", "sha256", "span"}, "work advice evidence")
        evidence_id = _text(item["id"], "evidence.id"); _relative_path(item["path"], "evidence.path")
        content = item["content"]
        if evidence_id in evidence_ids or not isinstance(content, str) or type(item["bytes"]) is not int or item["bytes"] != len(content.encode()) or item["sha256"] != hashlib.sha256(content.encode()).hexdigest():
            raise WorkPacketError("work advice evidence bytes or identity are invalid")
        evidence_ids.add(evidence_id); evidence_bytes += item["bytes"]
        _exact(item["span"], {"start", "end"}, "evidence.span")
        if item["span"] != {"start": 0, "end": len(content)}:
            raise WorkPacketError("work advice evidence span is invalid")
    _exact(request["budgets"], {"max_files", "max_file_bytes", "max_total_bytes", "files", "bytes"}, "work advice budgets")
    budgets = request["budgets"]
    if any(type(budgets[key]) is not int for key in budgets) or any(budgets[key] < 1 for key in ("max_files", "max_file_bytes", "max_total_bytes")) or any(budgets[key] < 0 for key in ("files", "bytes")) or budgets["max_files"] > 12 or budgets["max_file_bytes"] > 65_536 or budgets["max_total_bytes"] > 262_144 or budgets["files"] != len(evidence) or budgets["files"] > budgets["max_files"] or budgets["bytes"] != evidence_bytes or evidence_bytes > budgets["max_total_bytes"]:
        raise WorkPacketError("work advice budget usage is inconsistent")
    _exact(request["safeguards"], {"redactions", "secret_pii_redaction"}, "work advice safeguards")
    if type(request["safeguards"]["redactions"]) is not int or request["safeguards"]["redactions"] < 0 or request["safeguards"]["secret_pii_redaction"] is not True:
        raise WorkPacketError("work advice safeguards are invalid")
    _exact(request["prompt"], {"id", "version", "instructions"}, "work advice prompt")
    for key in request["prompt"]: _text(request["prompt"][key], f"prompt.{key}")
    if request["prompt"]["id"] != "engineering-core-owner-use-advisor" or request["prompt"]["version"] != "1": raise WorkPacketError("work advice prompt identity is invalid")
    unsigned = dict(request); claimed = unsigned.pop("request_sha256", None)
    if not isinstance(claimed, str) or canonical_digest(unsigned) != claimed:
        raise WorkPacketError("advisor request self-digest mismatch")
    return claimed


def _plan_digest(plan: dict[str, Any]) -> str:
    _finite_json(plan, "packet plan")
    _exact(plan, {"schema", "authority", "status", "source", "policy_ref", "selections", "dependencies", "diagnostics", "unknowns", "evidence", "digests"}, "packet plan")
    if plan["schema"] != "engineering-plan-v1" or plan["status"] not in ("complete", "incomplete") or plan["source"] not in ("policy", "inference") or not (plan["policy_ref"] is None or isinstance(plan["policy_ref"], str)):
        raise WorkPacketError("packet plan scalar fields are invalid")
    _exact(plan["authority"], {"mode", "statement"}, "plan authority")
    if plan["authority"]["mode"] != "advisory": raise WorkPacketError("plan authority mode is invalid")
    _text(plan["authority"]["statement"], "plan authority statement")
    for key in ("selections", "dependencies", "diagnostics", "unknowns", "evidence"):
        if not isinstance(plan[key], list) or len(plan[key]) > 1000: raise WorkPacketError(f"plan {key} must be a bounded array")
    selection_ids: set[str] = set()
    for item in plan["selections"]:
        _exact(item, {"id", "kind", "requested", "provenance"}, "plan selection")
        selection_id = _text(item["id"], "selection.id"); kind = _text(item["kind"], "selection.kind")
        if selection_id in selection_ids or kind not in ("lane", "addendum", "discipline") or type(item["requested"]) is not bool or not isinstance(item["provenance"], list) or not item["provenance"]: raise WorkPacketError("plan selection is invalid or duplicated")
        selection_ids.add(selection_id)
        for provenance in item["provenance"]:
            _exact(provenance, {"path", "source"}, "selection provenance"); _relative_path(provenance["path"], "selection provenance path"); _text(provenance["source"], "selection provenance source")
    dependency_keys: set[tuple[str, str, str]] = set()
    for item in plan["dependencies"]:
        _exact(item, {"from", "to", "provenance"}, "plan dependency")
        for key in item: _text(item[key], f"dependency.{key}")
        key = (item["from"], item["to"], item["provenance"])
        if key in dependency_keys: raise WorkPacketError("duplicate plan dependency rejected")
        dependency_keys.add(key)
    for item in plan["diagnostics"]:
        allowed = {"code", "message", "path", "severity"} | ({"id"} if isinstance(item, dict) and "id" in item else set())
        _exact(item, allowed, "plan diagnostic")
        for key in item: _text(item[key], f"diagnostic.{key}")
        if item["severity"] not in ("warning", "error"): raise WorkPacketError("plan diagnostic severity is invalid")
    for item in plan["unknowns"]:
        allowed = {"code", "message"} | ({"id"} if isinstance(item, dict) and "id" in item else set())
        _exact(item, allowed, "plan unknown")
        for key in item: _text(item[key], f"unknown.{key}")
    for item in plan["evidence"]:
        _exact(item, {"kind", "path", "sha256", "size"}, "plan evidence")
        _text(item["kind"], "evidence.kind"); _relative_path(item["path"], "plan evidence path")
        if not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or type(item["size"]) is not int or item["size"] < 0: raise WorkPacketError("plan evidence metadata is invalid")
    _exact(plan["digests"], {"catalog_sha256", "repository_facts_sha256", "plan_sha256"}, "plan digests")
    if any(not isinstance(plan["digests"][key], str) or not re.fullmatch(r"[0-9a-f]{64}", plan["digests"][key]) for key in plan["digests"]): raise WorkPacketError("plan digest field is invalid")
    unsigned = dict(plan); unsigned["digests"] = dict(plan["digests"]); claimed = unsigned["digests"].pop("plan_sha256")
    if canonical_digest(unsigned) != claimed: raise WorkPacketError("plan self-digest mismatch")
    return claimed


def build_bounded_work_plan(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "engineering-bounded-work-plan-v1", "objective": context["work"]["objective"],
        "focus_paths": context["scope"]["focus_paths"], "constraints": context["scope"]["constraints"],
        "validation": context["scope"]["validation"],
        "stop_conditions": ["repository revision changes", "focused scope changes", "deterministic plan or request becomes unavailable", "owner scope or authority is ambiguous"],
        "next_authority": "repository owner or owning task runtime",
    }


def build_work_request(base: dict[str, Any], context: dict[str, Any], snapshot: dict[str, Any], revision: str) -> dict[str, Any]:
    request = dict(base); request.pop("request_sha256")
    request["schema"] = WORK_REQUEST_SCHEMA
    bounded_plan = build_bounded_work_plan(context)
    binding = {"context_sha256": canonical_digest(context), "scope_sha256": snapshot["scope_sha256"], "repository_revision": revision, "plan_sha256": base["plan"]["digests"]["plan_sha256"]}
    request["work"] = {"context": context, "context_sha256": binding["context_sha256"], "scope_sha256": binding["scope_sha256"], "repository_revision": revision, "bounded_work_plan": bounded_plan, "work_binding_sha256": canonical_digest(binding)}
    request["prompt"] = {"id": "engineering-core-owner-use-advisor", "version": "1", "instructions": "Advise only on the bound owner objective and focus paths using supplied evidence and allowed catalog IDs. Preserve constraints and validation expectations. Express uncertainty, counterevidence, and falsification. Abstain when evidence is insufficient. Patches are inert proposals only."}
    request["request_sha256"] = canonical_digest(request)
    return request


def _check_packet_size(packet: dict[str, Any]) -> None:
    compact = json.dumps(packet, sort_keys=True, separators=(",", ":")).encode()
    pretty = (json.dumps(packet, indent=2, sort_keys=True) + "\n").encode()
    if max(len(compact), len(pretty)) > MAX_PACKET_BYTES:
        raise WorkPacketError("work packet exceeds protocol byte budget")


def prepare_work(repo: Path, repository_id: str, context: dict[str, Any], catalog: Catalog) -> dict[str, Any]:
    context = validate_context(context)
    if context["repository_id"] != repository_id:
        raise WorkPacketError("explicit repository id does not match context")
    root, revision_before = resolve_repository(repo)
    focus_paths = list(context["scope"]["focus_paths"])
    snapshot_before = scope_snapshot(root, focus_paths)
    plan_one, plan_two = compile_plan(root, catalog), compile_plan(root, catalog)
    if plan_one["status"] != "complete" or plan_one["digests"]["plan_sha256"] != plan_two["digests"]["plan_sha256"]:
        raise WorkPacketError("work packet requires a complete deterministic plan")
    request: dict[str, Any] | None = None
    if context["mode"] == "advisor-ready":
        ids = set(catalog.ids("lanes")) | set(catalog.ids("disciplines"))
        focus_files = {item["path"]: item["sha256"] for item in snapshot_before["files"] if item["state"] == "regular"}
        first = build_work_request(build_request(root, plan_one, ids, focus_files=focus_files), context, snapshot_before, revision_before)
        second = build_work_request(build_request(root, plan_two, ids, focus_files=focus_files), context, snapshot_before, revision_before)
        if first["request_sha256"] != second["request_sha256"]:
            raise WorkPacketError("advisor request is nondeterministic")
        request = first
    snapshot_after = scope_snapshot(root, focus_paths)
    _, revision_after = resolve_repository(root)
    if revision_before != revision_after or snapshot_before["scope_sha256"] != snapshot_after["scope_sha256"]:
        raise WorkPacketError("repository revision or focused scope changed during preparation")
    packet: dict[str, Any] = {
        "schema": PACKET_SCHEMA,
        "authority": AUTHORITY,
        "repository": {"id": repository_id, "path": str(root), "revision": revision_before},
        "context": context,
        "context_sha256": canonical_digest(context),
        "scope_snapshot": snapshot_before,
        "bounded_work_plan": build_bounded_work_plan(context),
        "plan": plan_one,
        "advice_request": request,
        "bindings": {
            "catalog_sha256": plan_one["digests"]["catalog_sha256"],
            "repository_facts_sha256": plan_one["digests"]["repository_facts_sha256"],
            "plan_sha256": plan_one["digests"]["plan_sha256"],
            "request_sha256": request["request_sha256"] if request else None,
        },
        "effects": {"consumer_commands_executed": False, "external_models_invoked": False, "patches_applied": False, "mutations_performed": []},
    }
    packet["packet_sha256"] = canonical_digest(packet)
    _check_packet_size(packet)
    return packet


def validate_packet(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict): raise WorkPacketError("packet must be an object")
    _finite_json(value, "packet")
    _check_packet_size(value)
    _exact(value, {"schema", "authority", "repository", "context", "context_sha256", "scope_snapshot", "bounded_work_plan", "plan", "advice_request", "bindings", "effects", "packet_sha256"}, "packet")
    if value["schema"] != PACKET_SCHEMA or value["authority"] != AUTHORITY:
        raise WorkPacketError("unsupported packet schema or authority")
    claimed = value["packet_sha256"]
    unsigned = dict(value); unsigned.pop("packet_sha256")
    if not isinstance(claimed, str) or canonical_digest(unsigned) != claimed:
        raise WorkPacketError("packet self-digest mismatch")
    context = validate_context(value["context"])
    if canonical_digest(context) != value["context_sha256"]:
        raise WorkPacketError("context digest mismatch")
    _exact(value["repository"], {"id", "path", "revision"}, "packet.repository")
    repository_path = _text(value["repository"]["path"], "repository.path")
    if not Path(repository_path).is_absolute() or value["repository"]["id"] != context["repository_id"] or not _GIT_ID.fullmatch(_text(value["repository"]["revision"], "repository.revision")):
        raise WorkPacketError("packet repository identity, path, or revision is invalid")
    snapshot = _validate_snapshot(value["scope_snapshot"], list(context["scope"]["focus_paths"]))
    if value["bounded_work_plan"] != build_bounded_work_plan(context): raise WorkPacketError("packet bounded work plan does not match context")
    plan_sha = _plan_digest(value["plan"])
    request = value["advice_request"]
    request_sha = _request_digest(request, value["plan"], context, snapshot, value["repository"]["revision"]) if isinstance(request, dict) else None
    if (context["mode"] == "advisor-ready") != isinstance(request, dict):
        raise WorkPacketError("packet mode and advice request disagree")
    expected = {"catalog_sha256": value["plan"]["digests"]["catalog_sha256"], "repository_facts_sha256": value["plan"]["digests"]["repository_facts_sha256"], "plan_sha256": plan_sha, "request_sha256": request_sha}
    if value["bindings"] != expected:
        raise WorkPacketError("packet bindings mismatch")
    if value["effects"] != {"consumer_commands_executed": False, "external_models_invoked": False, "patches_applied": False, "mutations_performed": []}:
        raise WorkPacketError("packet effect boundary is invalid")
    return value
