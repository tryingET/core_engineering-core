from __future__ import annotations

import json
from typing import Any


def yes(value: bool) -> str:
    return "yes" if value else "no"


def md_table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| Scope | Path | Name | Kind | Structural | Semantic | Lanes | Disciplines | Policy | Docs | Legacy | Catalog/list | Justfile | Notes |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for record in records:
        legacy = "yes" if record["has_legacy_doc"] or record["has_legacy_policy"] else "no"
        catalog = "yes" if record["has_catalog_command"] and record["has_list_disciplines_command"] and record["has_list_templates_command"] else "no"
        notes = "; ".join(record["notes"])
        lane_display = ", ".join(record["lanes"]) or (f"lane_status:{record.get('lane_status')}" if record.get("lane_status") else "-")
        scope_name = record["scope"].rstrip("/").split("/")[-1] or record["scope"]
        lines.append(
            "| "
            f"`{scope_name}` | "
            f"`{record['path']}` | "
            f"`{record['name']}` | "
            f"{record['kind']} | "
            f"{record['status']} | "
            f"{record.get('semantic_status', '-')} | "
            f"{lane_display} | "
            f"{', '.join(record['disciplines']) or '-'} | "
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
        f"Generated: `{scan['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Scopes: `{len(scan['scopes'])}`",
        f"- Repo discovery: `{scan['repo_discovery']}`",
        f"- Include scope root: `{scan['include_scope_root']}`",
        f"- Package/member surfaces included: `{scan['include_packages']}`",
        f"- Repos: `{summary['repos']}`",
        f"- Packages/member surfaces: `{summary['packages']}`",
        f"- Total records: `{summary['total']}`",
        f"- Structural status counts: `{json.dumps(summary['status_counts'], sort_keys=True)}`",
        f"- Semantic status counts: `{json.dumps(summary['semantic_status_counts'], sort_keys=True)}`",
        "",
        "## Scope summaries",
        "",
        "| Scope | Repos | Packages | Total | Structural counts | Semantic counts |",
        "|---|---:|---:|---:|---|---|",
    ]
    for scope_summary in scan["scope_summaries"]:
        lines.append(
            f"| `{scope_summary['scope']}` | "
            f"{scope_summary['repos']} | "
            f"{scope_summary['packages']} | "
            f"{scope_summary['total']} | "
            f"`{json.dumps(scope_summary['status_counts'], sort_keys=True)}` | "
            f"`{json.dumps(scope_summary['semantic_status_counts'], sort_keys=True)}` |"
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
