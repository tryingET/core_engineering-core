from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

REQUEST_SCHEMA = "engineering-advice-request-v1"
RESPONSE_SCHEMA = "engineering-advice-response-v1"
MAX_FILES = 12
MAX_FILE_BYTES = 65_536
MAX_TOTAL_BYTES = 262_144
_SECRET = re.compile(
    r"(?i)([\"']?(?:api[_-]?key|token|password|secret|authorization)[\"']?)"
    r"(\s*[=:]\s*[\"']?|\s+)([^\s,;}\"']+)([\"']?)"
)
_EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")

class AdviceError(ValueError):
    pass


def _digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def _exact(value: Any, keys: set[str], where: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise AdviceError(f"{where} must be an object with exactly: {', '.join(sorted(keys))}")


def _text(value: Any, where: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()) or len(value.encode()) > 16_384:
        raise AdviceError(f"{where} must be bounded text")
    return value


def _redact(text: str) -> tuple[str, int]:
    text, secrets = _SECRET.subn(
        lambda m: m.group(1) + m.group(2) + "[REDACTED]" + m.group(4), text
    )
    text, emails = _EMAIL.subn("[REDACTED_EMAIL]", text)
    return text, secrets + emails



def _read_owner_local(root: Path, relative: str, limit: int) -> bytes:
    """Read through no-follow directory descriptors so path races fail closed."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(part in ("", ".", "..") for part in parts):
        raise OSError("invalid owner-local path")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    directory_flags = flags | getattr(os, "O_DIRECTORY", 0)
    fd = os.open(root, directory_flags)
    try:
        for part in parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        file_fd = os.open(parts[-1], flags, dir_fd=fd)
        try:
            info = os.fstat(file_fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise OSError("evidence is not a bounded regular file")
            raw = os.read(file_fd, limit + 1)
            if len(raw) > limit or os.read(file_fd, 1):
                raise OSError("evidence exceeds byte budget")
            return raw
        finally:
            os.close(file_fd)
    finally:
        os.close(fd)


def _owner_local_path(value: str, where: str) -> str:
    # Unified-diff paths are a portable protocol surface, not host-native paths.
    # Reject Windows separators/drives and control characters even on POSIX.
    if not value or "\\" in value or any(ord(char) < 32 for char in value):
        raise AdviceError(f"{where} is not a portable owner-local path")
    candidate = Path(value)
    if candidate.is_absolute() or value.startswith("~") or ":" in candidate.parts[0] or any(part in ("", ".", "..") for part in candidate.parts):
        raise AdviceError(f"{where} is not a portable owner-local path")
    return candidate.as_posix()


def _diff_path(header: str) -> str | None:
    value = header.split("\t", 1)[0].strip()
    if value == "/dev/null":
        return None
    if value.startswith(("a/", "b/")):
        value = value[2:]
    return _owner_local_path(value, "diff header")


def _validate_diff(diff: str, target: str) -> None:
    headers = [(line[:3], line[4:]) for line in diff.splitlines() if line.startswith(("--- ", "+++ "))]
    if len(headers) != 2 or [kind for kind, _ in headers] != ["---", "+++"]:
        raise AdviceError("patch must contain exactly one unified diff file pair")
    paths = [_diff_path(value) for _, value in headers]
    if all(path is None for path in paths) or any(path is not None and path != target for path in paths):
        raise AdviceError("diff headers must match patch.path")


def build_request(repo: Path, plan: dict[str, Any], catalog_ids: set[str], *, max_files: int = MAX_FILES, max_file_bytes: int = MAX_FILE_BYTES, max_total_bytes: int = MAX_TOTAL_BYTES) -> dict[str, Any]:
    if plan.get("schema") != "engineering-plan-v1":
        raise AdviceError("advisor requires engineering-plan-v1")
    if not (1 <= max_files <= MAX_FILES and 1 <= max_file_bytes <= MAX_FILE_BYTES and 1 <= max_total_bytes <= MAX_TOTAL_BYTES):
        raise AdviceError("requested context budget exceeds protocol ceiling")
    root = repo.resolve()
    evidence = []
    total = 0
    redactions = 0
    for item in plan.get("evidence", []):
        if len(evidence) >= max_files:
            break
        relative = item.get("path")
        if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
            continue
        try:
            raw = _read_owner_local(root, relative, min(max_file_bytes, max_total_bytes - total))
        except OSError:
            continue
        if total + len(raw) > max_total_bytes or hashlib.sha256(raw).hexdigest() != item.get("sha256"):
            continue
        try:
            content, count = _redact(raw.decode("utf-8"))
        except UnicodeDecodeError:
            continue
        encoded = content.encode()
        # Redaction placeholders may be larger than the source token. Enforce
        # budgets on the disclosed representation, not only the source file.
        if len(encoded) > max_file_bytes or total + len(encoded) > max_total_bytes:
            continue
        evidence.append({"id": f"e{len(evidence) + 1}", "path": relative, "content": content, "bytes": len(encoded), "sha256": hashlib.sha256(encoded).hexdigest(), "span": {"start": 0, "end": len(content)}})
        total += len(encoded)
        redactions += count
    request: dict[str, Any] = {
        "schema": REQUEST_SCHEMA,
        "authority": "advisory-only; owner review required; never execute or apply patches",
        "plan": plan,
        "allowed_catalog_ids": sorted(catalog_ids),
        "evidence": evidence,
        "budgets": {"max_files": max_files, "max_file_bytes": max_file_bytes, "max_total_bytes": max_total_bytes, "files": len(evidence), "bytes": total},
        "safeguards": {"redactions": redactions, "secret_pii_redaction": True},
        "prompt": {"id": "engineering-core-bounded-advisor", "version": "1", "instructions": "Advise only from allowed catalog IDs and captured evidence. Express uncertainty, counterevidence, and falsification. Abstain when evidence is insufficient. Patches are proposals only."},
    }
    request["request_sha256"] = _digest(request)
    return request


def validate_response(request: dict[str, Any], response: Any) -> dict[str, Any]:
    top = {"schema", "request_sha256", "provenance", "status", "summary", "recommendations", "critiques", "patch_proposals"}
    _exact(response, top, "response")
    if response["schema"] != RESPONSE_SCHEMA or response["request_sha256"] != request.get("request_sha256"):
        raise AdviceError("response schema or request digest mismatch")
    _exact(response["provenance"], {"provider", "model", "model_version", "adapter", "adapter_version", "prompt_id", "prompt_version"}, "provenance")
    for key, value in response["provenance"].items():
        _text(value, f"provenance.{key}")
    prompt = request["prompt"]
    if response["provenance"]["prompt_id"] != prompt["id"] or response["provenance"]["prompt_version"] != prompt["version"]:
        raise AdviceError("prompt provenance mismatch")
    if response["status"] not in ("advice", "abstain", "unknown"):
        raise AdviceError("status must be advice, abstain, or unknown")
    _text(response["summary"], "summary")
    evidence = {item["id"]: item for item in request["evidence"]}
    allowed = set(request["allowed_catalog_ids"])
    if not all(isinstance(response[k], list) for k in ("recommendations", "critiques", "patch_proposals")):
        raise AdviceError("recommendations, critiques, and patch_proposals must be arrays")
    if response["status"] != "advice" and (response["recommendations"] or response["patch_proposals"]):
        raise AdviceError("abstain/unknown cannot contain recommendations or patches")
    if len(response["recommendations"]) > 20 or len(response["critiques"]) > 20 or len(response["patch_proposals"]) > 10:
        raise AdviceError("response item budget exceeded")
    recommendation_ids: set[str] = set()
    for index, rec in enumerate(response["recommendations"]):
        _exact(rec, {"id", "catalog_ids", "recommendation", "confidence", "unknowns", "counterevidence", "falsification", "citations", "competes_with"}, f"recommendations[{index}]")
        rid = _text(rec["id"], "recommendation.id")
        if rid in recommendation_ids:
            raise AdviceError("duplicate recommendation id")
        recommendation_ids.add(rid)
        if not isinstance(rec["confidence"], (int, float)) or isinstance(rec["confidence"], bool) or not 0 <= rec["confidence"] <= 1:
            raise AdviceError("confidence must be between 0 and 1")
        for key in ("catalog_ids", "unknowns", "counterevidence", "falsification", "citations", "competes_with"):
            if not isinstance(rec[key], list): raise AdviceError(f"{key} must be an array")
        for key in ("catalog_ids", "unknowns", "counterevidence", "falsification", "competes_with"):
            for item in rec[key]:
                _text(item, f"recommendation.{key} item")
        if not set(rec["catalog_ids"]).issubset(allowed): raise AdviceError("unknown catalog id")
        _text(rec["recommendation"], "recommendation")
        for citation in rec["citations"]:
            _exact(citation, {"evidence_id", "path", "start", "end"}, "citation")
            source = evidence.get(citation["evidence_id"])
            if source is None or citation["path"] != source["path"] or type(citation["start"]) is not int or type(citation["end"]) is not int or not 0 <= citation["start"] < citation["end"] <= source["span"]["end"]:
                raise AdviceError("citation is not within request-bound evidence")
    for rec in response["recommendations"]:
        if not set(rec["competes_with"]).issubset(recommendation_ids): raise AdviceError("competes_with references unknown recommendation")
    for critique in response["critiques"]:
        _exact(critique, {"recommendation_id", "critique", "severity", "falsification"}, "critique")
        if critique["recommendation_id"] not in recommendation_ids or critique["severity"] not in ("low", "medium", "high"): raise AdviceError("invalid critique reference or severity")
        _text(critique["critique"], "critique"); _text(critique["falsification"], "critique.falsification")
    for patch in response["patch_proposals"]:
        _exact(patch, {"path", "unified_diff", "rationale", "recommendation_id"}, "patch proposal")
        path = _owner_local_path(_text(patch["path"], "patch.path"), "patch.path")
        if patch["recommendation_id"] not in recommendation_ids: raise AdviceError("patch must be owner-local and recommendation-bound")
        diff = _text(patch["unified_diff"], "patch.diff")
        _validate_diff(diff, Path(path).as_posix())
        _text(patch["rationale"], "patch.rationale")
    return response


def load_json(path: Path) -> Any:
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_TOTAL_BYTES:
            raise AdviceError("response JSON exceeds byte budget")
        return json.loads(raw.decode("utf-8"))
    except AdviceError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdviceError(f"invalid JSON: {exc}") from exc
