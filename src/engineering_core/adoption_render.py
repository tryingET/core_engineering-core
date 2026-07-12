from __future__ import annotations

import json
from typing import Any


def yes(value: bool) -> str:
    return "yes" if value else "no"


def escape_cell(value: Any) -> str:
    """Render untrusted scanner data as inert Markdown table text."""
    text = str(value).replace("\\", "\\\\").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("|", "\\|").replace("`", "\\`").replace("[", "\\[").replace("]", "\\]").replace("\r", " ").replace("\n", "<br>")


def md_table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| Scope | Path | Name | Kind | Structural | Semantic | Loop validation | Lanes | Disciplines | Policy | Docs | Legacy | Catalog/list | Justfile | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for record in records:
        legacy = "yes" if record["has_legacy_doc"] or record["has_legacy_policy"] else "no"
        catalog = "yes" if record["has_catalog_command"] and record["has_list_disciplines_command"] and record["has_list_templates_command"] else "no"
        notes = escape_cell("; ".join(record["notes"]))
        lane_display = escape_cell(", ".join(record["lanes"]) or (f"lane_status:{record.get('lane_status')}" if record.get("lane_status") else "-"))
        loop_display = record.get("loop_validation_status", "absent")
        missing_loop_commands = record.get("loop_validation_missing_commands") or []
        if missing_loop_commands:
            loop_display = f"{loop_display}: missing {', '.join(missing_loop_commands)}"
        scope_name = escape_cell(record["scope"].rstrip("/").split("/")[-1] or record["scope"])
        lines.append(
            "| "
            f"{scope_name} | "
            f"{escape_cell(record['path'])} | "
            f"{escape_cell(record['name'])} | "
            f"{escape_cell(record['kind'])} | "
            f"{record['status']} | "
            f"{record.get('semantic_status', '-')} | "
            f"{loop_display} | "
            f"{lane_display} | "
            f"{escape_cell(', '.join(record['disciplines']) or '-')} | "
            f"{yes(record['has_engineering_policy'])} | "
            f"{yes(record['has_engineering_doc'])} | "
            f"{legacy} | "
            f"{catalog} | "
            f"{yes(record['has_justfile'])} | "
            f"{notes or '-'} |"
        )
    return "\n".join(lines)


def render_markdown(scan: dict[str, Any]) -> str:
    summary = scan["summary"]
    records = scan["records"]
    review_candidates = scan["review_candidates"]
    lines = [
        "---",
        'summary: "Engineering-core adoption coverage report."',
        "read_when:",
        '  - "Reviewing engineering-core adoption coverage across one or more repo scopes."',
        'type: "generated-report"',
        "---",
        "",
        "# Engineering-core adoption coverage",
        "",
        f"Generated: {escape_cell(scan['generated_at'])}",
        "",
        "## Summary",
        "",
        f"- Scopes: `{len(scan['scopes'])}`",
        f"- Repo discovery: `{escape_cell(scan['repo_discovery'])}`",
        f"- Completeness: `{escape_cell(scan.get('completeness', 'unknown'))}`",
        f"- Omissions: `{len(scan.get('omissions', []))}`",
        f"- Per-path failures: `{len(scan.get('failures', []))}`",
        f"- Include scope root: `{scan['include_scope_root']}`",
        f"- Package/member surfaces included: `{scan['include_packages']}`",
        f"- Repos: `{summary['repos']}`",
        f"- Packages/member surfaces: `{summary['packages']}`",
        f"- Total records: `{summary['total']}`",
        f"- Structural status counts: `{json.dumps(summary['status_counts'], sort_keys=True)}`",
        f"- Semantic status counts: `{json.dumps(summary['semantic_status_counts'], sort_keys=True)}`",
        f"- Loop validation status counts: `{json.dumps(summary.get('loop_validation_status_counts', {}), sort_keys=True)}`",
        "",
        "## Scope summaries",
        "",
        "| Scope | Repos | Packages | Total | Structural counts | Semantic counts | Loop validation counts |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    for scope_summary in scan["scope_summaries"]:
        lines.append(
            f"| {escape_cell(scope_summary['scope'])} | "
            f"{scope_summary['repos']} | "
            f"{scope_summary['packages']} | "
            f"{scope_summary['total']} | "
            f"`{json.dumps(scope_summary['status_counts'], sort_keys=True)}` | "
            f"`{json.dumps(scope_summary['semantic_status_counts'], sort_keys=True)}` | "
            f"`{json.dumps(scope_summary.get('loop_validation_status_counts', {}), sort_keys=True)}` |"
        )
    lines.extend(["", "## Review candidates", ""])
    if review_candidates:
        lines.append(md_table(review_candidates))
    else:
        lines.append("No structural or semantic review candidates found.")
    lines.extend(["", "## Full coverage", ""])
    if records:
        lines.append(md_table(records))
    else:
        lines.append("No repo or package records found for the selected scope/discovery options.")
    lines.append("")
    return "\n".join(lines)
