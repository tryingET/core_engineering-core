# summary: "Validates externally supplied advice, owner dispositions, and owner receipts into a deterministic non-authoritative evidence bundle bound to one work packet."
# read_when:
#   - "When changing finalize-work joins, evidence-bundle schemas, owner-state wording, or advice/disposition/receipt authority separation."

from __future__ import annotations

import json
import math
import re
from typing import Any

from engineering_core.advisor import AdviceError, validate_response
from engineering_core.closed_loop import ClosedLoopError, canonical_digest, validate_disposition, validate_receipt
from engineering_core.work_packet import WorkPacketError, validate_packet

BUNDLE_SCHEMA = "engineering-evidence-bundle-v1"
AUTHORITY = "derived owner-use bundle; not authenticated execution, CI, release, AK, compliance, rollout, approval, or doctrine authority"
_SHA = re.compile(r"^[0-9a-f]{64}$")
MAX_BUNDLE_BYTES = 8_388_608
MAX_RECORDS = 100


class WorkBundleError(ValueError):
    pass


def _finite_json(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value): raise WorkBundleError("bundle contains a non-finite number")
    if isinstance(value, dict):
        for item in value.values(): _finite_json(item)
    elif isinstance(value, list):
        for item in value: _finite_json(item)


def _check_bundle_size(bundle: dict[str, Any]) -> None:
    compact = json.dumps(bundle, sort_keys=True, separators=(",", ":")).encode()
    pretty = (json.dumps(bundle, indent=2, sort_keys=True) + "\n").encode()
    if max(len(compact), len(pretty)) > MAX_BUNDLE_BYTES:
        raise WorkBundleError("evidence bundle exceeds protocol byte budget")


def _exact(value: Any, keys: set[str], where: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise WorkBundleError(f"{where} must contain exactly: {', '.join(sorted(keys))}")


def _content_digests(value: Any, *, has_advice: bool, dispositions: int, receipts: int) -> dict[str, Any]:
    _exact(value, {"packet", "advice", "dispositions", "receipts"}, "input_content_sha256")
    expected = ((value["packet"], True), (value["advice"], has_advice))
    for item, required in expected:
        if required and (not isinstance(item, str) or not _SHA.fullmatch(item)):
            raise WorkBundleError("required input content digest is invalid")
        if not required and item is not None:
            raise WorkBundleError("absent advice must have a null content digest")
    for key, count in (("dispositions", dispositions), ("receipts", receipts)):
        items = value[key]
        if not isinstance(items, list) or len(items) != count or any(not isinstance(item, str) or not _SHA.fullmatch(item) for item in items):
            raise WorkBundleError(f"{key} content digests do not match inputs")
    return value


def _validate_inputs(packet: dict[str, Any], advice: dict[str, Any] | None, dispositions: list[dict[str, Any]], receipts: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(dispositions, list) or not isinstance(receipts, list) or len(dispositions) > MAX_RECORDS or len(receipts) > MAX_RECORDS:
        raise WorkBundleError(f"dispositions and receipts must be arrays with at most {MAX_RECORDS} entries")
    try:
        packet = validate_packet(packet)
        if advice is not None:
            request = packet["advice_request"]
            if not isinstance(request, dict):
                raise WorkBundleError("plan-only packet cannot accept advice")
            validate_response(request, advice)
        elif dispositions:
            raise WorkBundleError("dispositions require advice")
        validated_dispositions = [validate_disposition(item, advice) for item in dispositions]
        validated_receipts = [validate_receipt(item) for item in receipts]
    except (AdviceError, ClosedLoopError, WorkPacketError) as exc:
        raise WorkBundleError(str(exc)) from exc
    repository_id = packet["repository"]["id"]
    revision = packet["repository"]["revision"]
    bindings = packet["bindings"]
    advice_sha = canonical_digest(advice) if advice is not None else None
    disposition_ids: set[str] = set()
    recommendation_ids: set[str] = set()
    for item in validated_dispositions:
        if item["disposition_id"] in disposition_ids or item["recommendation_id"] in recommendation_ids:
            raise WorkBundleError("duplicate or ambiguous recommendation disposition rejected")
        disposition_ids.add(item["disposition_id"]); recommendation_ids.add(item["recommendation_id"])
        if item["provenance"]["owner"] != repository_id or item["target"] != {"repository": repository_id, "revision": revision}:
            raise WorkBundleError("disposition owner or target does not match packet repository")
        expected = {
            "request_sha256": bindings["request_sha256"],
            "advice_sha256": advice_sha,
            "plan_sha256": bindings["plan_sha256"],
            "catalog_sha256": bindings["catalog_sha256"],
            "repository_facts_sha256": bindings["repository_facts_sha256"],
        }
        if item["bindings"] != expected:
            raise WorkBundleError("disposition binding chain does not match packet and advice")
    receipt_ids: set[str] = set()
    by_recommendation = {item["recommendation_id"]: item for item in validated_dispositions}
    for item in validated_receipts:
        if item["receipt_id"] in receipt_ids:
            raise WorkBundleError("duplicate receipt_id rejected")
        receipt_ids.add(item["receipt_id"])
        if item["provenance"]["owner"] != repository_id or item["target"]["repository"] != repository_id or item["target"]["revision"] != revision:
            raise WorkBundleError("receipt owner or target does not match packet repository")
        expected = {key: bindings[key] for key in ("plan_sha256", "catalog_sha256", "repository_facts_sha256")}
        if item["bindings"] != expected:
            raise WorkBundleError("receipt binding chain does not match packet")
        if advice is None or item["target"]["recommendation_id"] not in by_recommendation:
            raise WorkBundleError("owner-use receipt requires supplied advice and one exact supplied disposition")
    return validated_dispositions, validated_receipts


def _derive(packet: dict[str, Any], advice: dict[str, Any] | None, dispositions: list[dict[str, Any]], receipts: list[dict[str, Any]], content: dict[str, Any]) -> dict[str, Any]:
    dispositions, receipts = _validate_inputs(packet, advice, dispositions, receipts)
    receipt_by_recommendation: dict[str, list[dict[str, Any]]] = {}
    for item in receipts:
        receipt_by_recommendation.setdefault(item["target"]["recommendation_id"], []).append(item)
    records: list[dict[str, Any]] = []
    disposition_by_recommendation = {item["recommendation_id"]: item for item in dispositions}
    for recommendation in sorted(advice.get("recommendations", []) if advice else [], key=lambda row: row["id"]):
        item = disposition_by_recommendation.get(recommendation["id"])
        related = sorted(receipt_by_recommendation.get(recommendation["id"], []), key=lambda row: row["receipt_id"])
        records.append({
            "subject": {"kind": "recommendation", "recommendation_id": recommendation["id"]},
            "recommendation": recommendation["recommendation"],
            "disposition": {"id": item["disposition_id"], "decision": item["decision"], "reason_code": item["reason_code"]} if item else None,
            "owner_receipts": [{"id": row["receipt_id"], "state": row["state"]} for row in related],
            "posture": "owner-reviewed" if item else "awaiting-owner-review",
        })
    if not records:
        records.append({"subject": {"kind": "plan", "recommendation_id": None}, "recommendation": None, "disposition": None, "owner_receipts": [], "posture": "awaiting-advice" if packet["context"]["mode"] == "advisor-ready" else "prepared"})
    decisions = ("accepted", "deferred", "rejected", "abstained")
    summary = {
        "mode": packet["context"]["mode"],
        "advice_supplied": advice is not None,
        "recommendations": len(advice.get("recommendations", [])) if advice else 0,
        "dispositions": len(dispositions),
        "receipts": len(receipts),
        "decision_counts": {key: sum(item["decision"] == key for item in dispositions) for key in decisions},
        "owner_state_counts": {key: sum(item["state"] == key for item in receipts) for key in sorted({item["state"] for item in receipts})},
    }
    return {
        "schema": BUNDLE_SCHEMA,
        "authority": AUTHORITY,
        "repository": packet["repository"],
        "work": packet["context"]["work"],
        "packet": packet,
        "advice": advice,
        "dispositions": dispositions,
        "receipts": receipts,
        "input_digests": {
            "content_sha256": content,
            "canonical_sha256": {
                "packet": canonical_digest(packet),
                "advice": canonical_digest(advice) if advice is not None else None,
                "dispositions": [canonical_digest(item) for item in dispositions],
                "receipts": [canonical_digest(item) for item in receipts],
            },
        },
        "summary": summary,
        "records": records,
        "effects": {"observation_references_opened": False, "consumer_commands_executed": False, "external_models_invoked": False, "patches_applied": False, "authority_promotions": [], "mutations_performed": []},
    }


def finalize_work(packet: dict[str, Any], advice: dict[str, Any] | None, dispositions: list[dict[str, Any]], receipts: list[dict[str, Any]], input_content_sha256: dict[str, Any]) -> dict[str, Any]:
    content = _content_digests(input_content_sha256, has_advice=advice is not None, dispositions=len(dispositions), receipts=len(receipts))
    bundle = _derive(packet, advice, dispositions, receipts, content)
    bundle["bundle_sha256"] = canonical_digest(bundle)
    _check_bundle_size(bundle)
    return bundle


def validate_bundle(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict): raise WorkBundleError("bundle must be an object")
    _finite_json(value); _check_bundle_size(value)
    _exact(value, {"schema", "authority", "repository", "work", "packet", "advice", "dispositions", "receipts", "input_digests", "summary", "records", "effects", "bundle_sha256"}, "bundle")
    if value["schema"] != BUNDLE_SCHEMA or value["authority"] != AUTHORITY:
        raise WorkBundleError("unsupported evidence bundle schema or authority")
    unsigned = dict(value); claimed = unsigned.pop("bundle_sha256")
    if not isinstance(claimed, str) or canonical_digest(unsigned) != claimed:
        raise WorkBundleError("bundle self-digest mismatch")
    if not isinstance(value["dispositions"], list) or not isinstance(value["receipts"], list):
        raise WorkBundleError("bundle dispositions and receipts must be arrays")
    _exact(value["input_digests"], {"content_sha256", "canonical_sha256"}, "input_digests")
    content = _content_digests(value["input_digests"]["content_sha256"], has_advice=value["advice"] is not None, dispositions=len(value["dispositions"]), receipts=len(value["receipts"]))
    rebuilt = _derive(value["packet"], value["advice"], value["dispositions"], value["receipts"], content)
    for key in ("repository", "work", "input_digests", "summary", "records", "effects"):
        if value[key] != rebuilt[key]:
            raise WorkBundleError(f"bundle {key} is inconsistent with embedded inputs")
    return value
