# summary: "Renders concise owner-facing JSON or Markdown handoffs from validated work bundles and optional read-only verification results."
# read_when:
#   - "When changing summarize-work owner UX, pending-decision rendering, validation handoffs, or drift explanations."

from __future__ import annotations

from typing import Any

from engineering_core.work_bundle import WorkBundleError, validate_bundle
from engineering_core.work_verify import validate_verification

SUMMARY_SCHEMA = "engineering-work-summary-v1"
AUTHORITY = "owner handoff projection; owning task and repository remain authoritative"


def build_summary(bundle: dict[str, Any], verification: dict[str, Any] | None = None) -> dict[str, Any]:
    bundle = validate_bundle(bundle)
    if verification is not None:
        verification = validate_verification(verification)
        if verification.get("bundle_sha256") != bundle["bundle_sha256"]:
            raise WorkBundleError("summary verification does not bind the supplied bundle")
    recommendations = []
    for record in bundle["records"]:
        if record["subject"]["kind"] != "recommendation":
            continue
        disposition = record["disposition"]
        recommendations.append({
            "id": record["subject"]["recommendation_id"],
            "recommendation": record["recommendation"],
            "decision": disposition["decision"] if disposition else "pending-owner-review",
            "reason_code": disposition["reason_code"] if disposition else None,
            "owner_receipt_states": [item["state"] for item in record["owner_receipts"]],
        })
    if any(item["decision"] == "pending-owner-review" for item in recommendations):
        next_action = "Owner reviews each pending recommendation and may author a bound disposition; advice does not self-authorize."
    elif recommendations and not any(item["owner_receipt_states"] for item in recommendations):
        next_action = "Owner selects and runs validation outside engineering-core, then may author a truthful receipt."
    elif bundle["packet"]["context"]["mode"] == "advisor-ready" and bundle["advice"] is None:
        next_action = "Owner may send the bound request to an external advisor or continue without advice."
    else:
        next_action = "Owner checks constraints and stop conditions, then uses the bounded plan only under the named next authority."
    return {
        "schema": SUMMARY_SCHEMA,
        "authority": AUTHORITY,
        "repository_id": bundle["repository"]["id"],
        "work": bundle["work"],
        "revision": bundle["repository"]["revision"],
        "mode": bundle["summary"]["mode"],
        "focus_paths": bundle["packet"]["context"]["scope"]["focus_paths"],
        "constraints": bundle["packet"]["context"]["scope"]["constraints"],
        "validation": bundle["packet"]["bounded_work_plan"]["validation"],
        "stop_conditions": bundle["packet"]["bounded_work_plan"]["stop_conditions"],
        "next_authority": bundle["packet"]["bounded_work_plan"]["next_authority"],
        "recommendations": recommendations,
        "verification": None if verification is None else {"result": verification["result"], "revision_relation": verification["revision_relation"], "scope_match": verification["scope_match"], "binding_match": verification["binding_match"], "findings": verification["findings"]},
        "next_action": next_action,
        "bundle_sha256": bundle["bundle_sha256"],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# Work handoff — {summary['work']['title']}", "",
        f"- Repository: `{summary['repository_id']}`",
        f"- Work: `{summary['work']['id']}`",
        f"- Revision: `{summary['revision']}`",
        f"- Mode: `{summary['mode']}`",
        f"- Authority: {summary['authority']}", "",
        "## Objective", "", summary["work"]["objective"], "",
        "## Focus paths", "",
    ]
    lines.extend(f"- `{path}`" for path in summary["focus_paths"])
    lines.extend(["", "## Constraints", ""])
    lines.extend(f"- {item}" for item in summary["constraints"])
    lines.extend(["", "## Stop conditions", ""])
    lines.extend(f"- {item}" for item in summary["stop_conditions"])
    lines.extend(["", f"Next authority: **{summary['next_authority']}**", "", "## Recommendations", ""])
    if summary["recommendations"]:
        for item in summary["recommendations"]:
            lines.extend([f"### `{item['id']}` — {item['decision']}", "", item["recommendation"], ""])
    else:
        lines.extend(["- No external recommendation supplied.", ""])
    lines.extend(["## Validation expected by owner context", ""])
    lines.extend(f"- {item}" for item in summary["validation"])
    if summary["verification"] is not None:
        verify = summary["verification"]
        lines.extend(["", "## Verification", "", f"- Result: `{verify['result']}`", f"- Revision relation: `{verify['revision_relation']}`", f"- Scope match: `{str(verify['scope_match']).lower()}`", f"- Binding match: `{str(verify['binding_match']).lower()}`"])
    lines.extend(["", "## Next action", "", summary["next_action"], ""])
    return "\n".join(lines)
