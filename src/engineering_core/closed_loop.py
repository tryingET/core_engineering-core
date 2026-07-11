"""Deterministic, read-only processing of owner-authored closed-loop evidence."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

MAX_INPUT_BYTES = 262_144
MAX_ITEMS = 1000
RECEIPT_SCHEMA = "engineering-evidence-receipt-v1"
DISPOSITION_SCHEMA = "engineering-recommendation-disposition-v1"
STATES = ("declared", "schema-valid", "target-resolved", "execution-observed", "evidence-verified", "stale", "mismatched", "unknown")
DECISIONS = ("accepted", "deferred", "rejected", "abstained")
REASONS = ("adopted", "needs-evidence", "needs-owner-decision", "out-of-scope", "conflicting-evidence", "superseded", "not-applicable", "insufficient-evidence")
_SECRET = re.compile(r'''(?ix)["']?(api[_-]?key|access[_-]?token|password|secret|authorization)["']?\s*[=:]\s*["']?[^\s,;"'}]+''')
_SHA = re.compile(r"^[0-9a-f]{64}$")

class ClosedLoopError(ValueError):
    pass

def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def load_record(path: Path) -> Any:
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_INPUT_BYTES: raise ClosedLoopError(f"input exceeds {MAX_INPUT_BYTES} bytes")
        text = raw.decode("utf-8")
        if _SECRET.search(text): raise ClosedLoopError("secret-bearing input rejected")
        return json.loads(text)
    except ClosedLoopError: raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc: raise ClosedLoopError(f"invalid JSON: {exc}") from exc

def _exact(value: Any, keys: set[str], where: str) -> None:
    if not isinstance(value, dict) or set(value) != keys: raise ClosedLoopError(f"{where} must contain exactly: {', '.join(sorted(keys))}")

def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.encode()) > 4096: raise ClosedLoopError(f"{where} must be bounded text")
    return value

def _digest(value: Any, where: str) -> str:
    if not isinstance(value, str) or not _SHA.fullmatch(value): raise ClosedLoopError(f"{where} must be a lowercase sha256")
    return value

def _provenance(value: Any, where: str) -> None:
    _exact(value, {"owner", "owner_type", "produced_at", "source"}, where)
    for key in value: _text(value[key], f"{where}.{key}")

def validate_receipt(value: Any) -> dict[str, Any]:
    _exact(value, {"schema", "receipt_id", "authority", "provenance", "bindings", "target", "observations", "state", "reason"}, "receipt")
    if value["schema"] != RECEIPT_SCHEMA: raise ClosedLoopError("unsupported receipt schema")
    _text(value["receipt_id"], "receipt_id"); _provenance(value["provenance"], "provenance")
    if value["authority"] != "owner-evidence-only; not CI, release, AK, or compliance authority": raise ClosedLoopError("invalid receipt authority boundary")
    _exact(value["bindings"], {"plan_sha256", "catalog_sha256", "repository_facts_sha256"}, "bindings")
    for key in value["bindings"]: _digest(value["bindings"][key], f"bindings.{key}")
    _exact(value["target"], {"repository", "revision", "recommendation_id"}, "target")
    for key in value["target"]: _text(value["target"][key], f"target.{key}")
    if not isinstance(value["observations"], list) or len(value["observations"]) > 100: raise ClosedLoopError("observations must be a bounded array")
    for i, item in enumerate(value["observations"]):
        _exact(item, {"kind", "outcome", "evidence_sha256", "reference"}, f"observations[{i}]")
        if item["kind"] not in ("execution", "artifact", "review", "unknown") or item["outcome"] not in ("passed", "failed", "observed", "unknown"): raise ClosedLoopError("invalid observation kind or outcome")
        _digest(item["evidence_sha256"], "observation.evidence_sha256"); _text(item["reference"], "observation.reference")
    if value["state"] not in STATES: raise ClosedLoopError("invalid receipt state")
    _text(value["reason"], "reason")
    # State claims require corresponding owner evidence; this validates consistency, not truth.
    if value["state"] == "execution-observed" and not any(x["kind"] == "execution" for x in value["observations"]): raise ClosedLoopError("execution-observed requires an execution observation")
    if value["state"] == "evidence-verified" and not any(x["outcome"] == "passed" for x in value["observations"]): raise ClosedLoopError("evidence-verified requires passed evidence")
    return value

def validate_disposition(value: Any, advice: dict[str, Any] | None = None) -> dict[str, Any]:
    _exact(value, {"schema", "disposition_id", "authority", "provenance", "bindings", "target", "recommendation_id", "decision", "reason_code", "rationale"}, "disposition")
    if value["schema"] != DISPOSITION_SCHEMA: raise ClosedLoopError("unsupported disposition schema")
    _text(value["disposition_id"], "disposition_id"); _provenance(value["provenance"], "provenance")
    if value["authority"] != "owner disposition; advisory inputs do not self-authorize": raise ClosedLoopError("invalid disposition authority boundary")
    _exact(value["bindings"], {"request_sha256", "advice_sha256", "plan_sha256", "catalog_sha256", "repository_facts_sha256"}, "bindings")
    for key in value["bindings"]: _digest(value["bindings"][key], f"bindings.{key}")
    _exact(value["target"], {"repository", "revision"}, "target")
    for key in value["target"]: _text(value["target"][key], f"target.{key}")
    _text(value["recommendation_id"], "recommendation_id")
    if value["decision"] not in DECISIONS or value["reason_code"] not in REASONS: raise ClosedLoopError("invalid decision or controlled reason code")
    _text(value["rationale"], "rationale")
    if advice is not None:
        if canonical_digest(advice) != value["bindings"]["advice_sha256"] or advice.get("request_sha256") != value["bindings"]["request_sha256"]: raise ClosedLoopError("advice binding mismatch")
        ids = {r.get("id") for r in advice.get("recommendations", [])}
        if value["recommendation_id"] not in ids: raise ClosedLoopError("hallucinated recommendation id")
    return value

def summarize_receipts(receipts: Iterable[dict[str, Any]]) -> dict[str, Any]:
    items = sorted((validate_receipt(x) for x in receipts), key=lambda x: (x["target"]["repository"], x["receipt_id"]))
    if len(items) > MAX_ITEMS: raise ClosedLoopError("receipt item budget exceeded")
    counts = {state: sum(x["state"] == state for x in items) for state in STATES}
    return {"schema": "engineering-receipt-summary-v1", "authority": "read-only owner evidence summary", "counts": counts, "receipts": [{"receipt_id": x["receipt_id"], "repository": x["target"]["repository"], "state": x["state"], "bindings": x["bindings"]} for x in items]}

def _reject_duplicate(records: list[dict[str, Any]], key: str, where: str) -> None:
    values = [item[key] for item in records]
    if len(values) != len(set(values)):
        raise ClosedLoopError(f"duplicate {where} rejected")


def _validate_advice_shape(value: Any) -> dict[str, Any]:
    _exact(value, {"schema", "request_sha256", "provenance", "status", "summary", "recommendations", "critiques", "patch_proposals"}, "advice")
    if value["schema"] != "engineering-advice-response-v1": raise ClosedLoopError("unsupported advice schema")
    _digest(value["request_sha256"], "advice.request_sha256")
    _exact(value["provenance"], {"provider", "model", "model_version", "adapter", "adapter_version", "prompt_id", "prompt_version"}, "advice.provenance")
    for key in value["provenance"]: _text(value["provenance"][key], f"advice.provenance.{key}")
    if value["status"] not in ("advice", "abstain", "unknown"): raise ClosedLoopError("invalid advice status")
    _text(value["summary"], "advice.summary")
    if not all(isinstance(value[key], list) for key in ("recommendations", "critiques", "patch_proposals")): raise ClosedLoopError("advice collections must be arrays")
    if len(value["recommendations"]) > 20 or len(value["critiques"]) > 20 or len(value["patch_proposals"]) > 10: raise ClosedLoopError("advice item budget exceeded")
    recommendation_ids: set[str] = set()
    for index, item in enumerate(value["recommendations"]):
        _exact(item, {"id", "catalog_ids", "recommendation", "confidence", "unknowns", "counterevidence", "falsification", "citations", "competes_with"}, f"advice.recommendations[{index}]")
        recommendation_id = _text(item["id"], "advice recommendation id")
        if recommendation_id in recommendation_ids: raise ClosedLoopError("duplicate advice recommendation id")
        recommendation_ids.add(recommendation_id)
        if not isinstance(item["confidence"], (int, float)) or isinstance(item["confidence"], bool) or not 0 <= item["confidence"] <= 1: raise ClosedLoopError("invalid advice confidence")
        if not all(isinstance(item[key], list) for key in ("catalog_ids", "unknowns", "counterevidence", "falsification", "citations", "competes_with")): raise ClosedLoopError("advice recommendation collections must be arrays")
        _text(item["recommendation"], "advice recommendation")
    if value["status"] != "advice" and (value["recommendations"] or value["patch_proposals"]): raise ClosedLoopError("abstain/unknown advice cannot recommend or patch")
    return value


def _receipt_matches_disposition(receipt: dict[str, Any], disposition: dict[str, Any]) -> bool:
    return (
        receipt["target"]["recommendation_id"] == disposition["recommendation_id"]
        and receipt["target"]["repository"] == disposition["target"]["repository"]
        and receipt["target"]["revision"] == disposition["target"]["revision"]
        and all(receipt["bindings"][key] == disposition["bindings"][key]
                for key in ("plan_sha256", "catalog_sha256", "repository_facts_sha256"))
    )


def calibration(advice: dict[str, Any], dispositions: Iterable[dict[str, Any]], receipts: Iterable[dict[str, Any]]) -> dict[str, Any]:
    advice = _validate_advice_shape(advice)
    ds = [validate_disposition(x, advice) for x in dispositions]; rs = [validate_receipt(x) for x in receipts]
    _reject_duplicate(ds, "disposition_id", "disposition_id")
    _reject_duplicate(rs, "receipt_id", "receipt_id")
    recommendation_ids = [x["recommendation_id"] for x in ds]
    if len(recommendation_ids) != len(set(recommendation_ids)):
        raise ClosedLoopError("ambiguous duplicate recommendation disposition rejected")
    recs = {x["id"]: x for x in advice.get("recommendations", [])}
    rows = []
    for d in sorted(ds, key=lambda x: x["recommendation_id"]):
        related = [r for r in rs if _receipt_matches_disposition(r, d)]
        rows.append({"recommendation_id": d["recommendation_id"], "model_confidence": recs[d["recommendation_id"]]["confidence"], "owner_decision": d["decision"], "accepted": d["decision"] == "accepted", "evidence_verified": any(r["state"] == "evidence-verified" for r in related), "receipt_states": sorted({r["state"] for r in related}), "advice_sha256": d["bindings"]["advice_sha256"], "receipt_ids": sorted(r["receipt_id"] for r in related)})
    return {"schema": "engineering-calibration-v1", "authority": "descriptive metrics; not model quality or compliance authority", "metrics": {"recommendations": len(rows), "accepted": sum(x["accepted"] for x in rows), "evidence_verified": sum(x["evidence_verified"] for x in rows)}, "outcomes": rows}

def synthesize_patterns(plans: Iterable[dict[str, Any]], advice: Iterable[dict[str, Any]], dispositions: Iterable[dict[str, Any]], receipts: Iterable[dict[str, Any]]) -> dict[str, Any]:
    ps, ads, raw_ds, raw_rs = list(plans), list(advice), list(dispositions), list(receipts)
    if any(len(x) > MAX_ITEMS for x in (ps, ads, raw_ds, raw_rs)): raise ClosedLoopError("pattern input budget exceeded")
    plans_by_digest: dict[str, dict[str, Any]] = {}
    for p in ps:
        if not isinstance(p, dict) or p.get("schema") != "engineering-plan-v1": raise ClosedLoopError("patterns require engineering-plan-v1")
        digests = p.get("digests")
        if not isinstance(digests, dict): raise ClosedLoopError("plan digests must be an object")
        claimed = digests.get("plan_sha256"); _digest(claimed, "plan digest")
        if not isinstance(p.get("selections"), list): raise ClosedLoopError("plan selections must be an array")
        for selection in p["selections"]:
            if not isinstance(selection, dict): raise ClosedLoopError("plan selection must be an object")
            _text(selection.get("id"), "plan selection id")
        unsigned = dict(p); unsigned["digests"] = dict(digests); del unsigned["digests"]["plan_sha256"]
        if canonical_digest(unsigned) != claimed: raise ClosedLoopError("plan digest mismatch")
        if claimed in plans_by_digest: raise ClosedLoopError("duplicate plan digest rejected")
        plans_by_digest[claimed] = p
    advice_by_digest = {}
    for item in ads:
        item = _validate_advice_shape(item)
        digest = canonical_digest(item)
        if digest in advice_by_digest: raise ClosedLoopError("duplicate advice digest rejected")
        advice_by_digest[digest] = item
    ds = [validate_disposition(item) for item in raw_ds]
    rs = [validate_receipt(item) for item in raw_rs]
    _reject_duplicate(ds, "disposition_id", "disposition_id")
    _reject_duplicate(rs, "receipt_id", "receipt_id")
    for d in ds:
        bound = d["bindings"]["advice_sha256"]
        if bound not in advice_by_digest: raise ClosedLoopError("disposition has no explicitly supplied bound advice")
        validate_disposition(d, advice_by_digest[bound])
        plan = plans_by_digest.get(d["bindings"]["plan_sha256"])
        if plan is None: raise ClosedLoopError("disposition has no explicitly supplied bound plan")
        if any(d["bindings"][key] != plan["digests"][key] for key in ("catalog_sha256", "repository_facts_sha256")):
            raise ClosedLoopError("disposition plan provenance mismatch")
    for r in rs:
        plan = plans_by_digest.get(r["bindings"]["plan_sha256"])
        if plan is None: raise ClosedLoopError("receipt has no explicitly supplied bound plan")
        if any(r["bindings"][key] != plan["digests"][key] for key in ("catalog_sha256", "repository_facts_sha256")):
            raise ClosedLoopError("receipt plan provenance mismatch")
    # Conservative pattern: catalog selections recurring across explicitly supplied plans.
    occurrences: dict[str, list[str]] = {}
    for digest, p in sorted(plans_by_digest.items()):
        _digest(digest, "plan digest")
        for selection in p["selections"]:
            occurrences.setdefault(selection["id"], []).append(digest)
    patterns = [{"catalog_id": key, "occurrences": len(vals), "plan_sha256s": sorted(vals)} for key, vals in sorted(occurrences.items()) if len(vals) >= 2]
    return {"schema": "engineering-pattern-synthesis-v1", "authority": "review-only synthesis; no source mutation", "input_digests": {"plans": sorted(canonical_digest(x) for x in ps), "advice": sorted(canonical_digest(x) for x in ads), "dispositions": sorted(canonical_digest(x) for x in ds), "receipts": sorted(canonical_digest(x) for x in rs)}, "patterns": patterns}

def doctrine_proposal(patterns: dict[str, Any]) -> dict[str, Any]:
    if patterns.get("schema") != "engineering-pattern-synthesis-v1": raise ClosedLoopError("proposal requires pattern synthesis v1")
    candidates = [{"catalog_id": x["catalog_id"], "proposal": f"Review recurring selection {x['catalog_id']} for doctrine/catalog clarification.", "evidence": {"occurrences": x["occurrences"], "plan_sha256s": x["plan_sha256s"]}} for x in patterns.get("patterns", [])]
    return {"schema": "engineering-doctrine-proposal-v1", "status": "unapplied", "authority": "proposal only; doctrine owner review required; cannot self-authorize", "patterns_sha256": canonical_digest(patterns), "candidates": candidates, "mutations_performed": []}
