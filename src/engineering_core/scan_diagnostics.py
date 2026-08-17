from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from engineering_core.catalog_model import collection_entries

DIAGNOSTIC_SCHEMA_VERSION = "1"
BASELINE_SCHEMA_VERSION = "1"
SEVERITIES = ("error", "warning", "advisory")
SEVERITY_RANK = {severity: index for index, severity in enumerate(SEVERITIES)}


@dataclass(frozen=True)
class ScanDiagnostic:
    fingerprint: str
    rule_id: str
    severity: str
    confidence: float
    scope: str
    scope_label: str
    path: str
    kind: str
    message: str
    evidence: list[str]
    remediation: str | None
    suppressible: bool


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def _scope_label(scope: str) -> str:
    path = Path(scope)
    return path.name or str(path)


def _fingerprint(*, rule_id: str, scope_label: str, path: str, kind: str, evidence: Iterable[str]) -> str:
    payload = {
        "rule_id": rule_id,
        "scope": scope_label,
        "path": path,
        "kind": kind,
        "evidence": sorted(str(item) for item in evidence),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def diagnostic(
    record: dict[str, Any],
    *,
    rule_id: str,
    severity: str,
    confidence: float,
    message: str,
    evidence: Iterable[str] = (),
    remediation: str | None = None,
    suppressible: bool = False,
) -> ScanDiagnostic:
    if severity not in SEVERITIES:
        raise ValueError(f"unknown severity: {severity}")
    scope = str(record.get("scope", ""))
    scope_label = _scope_label(scope)
    path = str(record.get("path", "."))
    kind = str(record.get("kind", "repo"))
    normalized_evidence = sorted({str(item) for item in evidence if str(item)})
    return ScanDiagnostic(
        fingerprint=_fingerprint(
            rule_id=rule_id,
            scope_label=scope_label,
            path=path,
            kind=kind,
            evidence=normalized_evidence,
        ),
        rule_id=rule_id,
        severity=severity,
        confidence=confidence,
        scope=scope,
        scope_label=scope_label,
        path=path,
        kind=kind,
        message=message,
        evidence=normalized_evidence,
        remediation=remediation,
        suppressible=suppressible,
    )


def _requirements(catalog: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for entry in collection_entries(catalog, "lanes"):
        entry_id = entry.get("id")
        raw = entry.get("requires", [])
        if isinstance(entry_id, str) and isinstance(raw, list):
            result[entry_id] = [item for item in raw if isinstance(item, str)]
    return result


def _structural_diagnostics(record: dict[str, Any]) -> list[ScanDiagnostic]:
    status = str(record.get("status", ""))
    diagnostics: list[ScanDiagnostic] = []
    status_rules = {
        "invalid-policy": (
            "policy.invalid-json",
            "error",
            "The repository policy is invalid JSON or not a JSON object.",
            "Repair policy/engineering-lane.json before relying on adoption results.",
        ),
        "missing": (
            "adoption.missing",
            "warning",
            "The repository has no current engineering-core adoption surfaces.",
            "Create docs/engineering.local.md and policy/engineering-lane.json.",
        ),
        "doc-only": (
            "adoption.surface-pair",
            "warning",
            "The human-readable adoption document exists without policy metadata.",
            "Add policy/engineering-lane.json or explicitly remove the incomplete adoption surface.",
        ),
        "policy-only": (
            "adoption.surface-pair",
            "warning",
            "The policy exists without a human-readable local engineering document.",
            "Add docs/engineering.local.md so local choices and deviations remain reviewable.",
        ),
        "legacy-only": (
            "legacy.surfaces",
            "warning",
            "Only legacy tech-stack adoption surfaces are present.",
            "Plan migration to engineering-core and review the generated diff.",
        ),
        "legacy-mixed": (
            "legacy.surfaces",
            "warning",
            "Current and legacy adoption surfaces coexist.",
            "Remove legacy files after the migration has been reviewed and validated.",
        ),
        "partial": (
            "adoption.partial",
            "warning",
            "The repository adoption contract is structurally incomplete.",
            "Review the structural evidence and complete the missing objective fields.",
        ),
    }
    if status in status_rules:
        rule_id, severity, message, remediation = status_rules[status]
        diagnostics.append(
            diagnostic(
                record,
                rule_id=rule_id,
                severity=severity,
                confidence=1.0,
                message=message,
                evidence=record.get("structural_notes", []),
                remediation=remediation,
            )
        )

    for note in record.get("structural_notes", []):
        if note.startswith("unknown lane(s):"):
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="catalog.unknown-lane",
                    severity="error",
                    confidence=1.0,
                    message="The policy selects one or more unknown lane IDs.",
                    evidence=[note.partition(":")[2].strip()],
                    remediation="Select lane IDs from the active engineering-core catalog.",
                )
            )
        elif note.startswith("unknown discipline(s):"):
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="catalog.unknown-discipline",
                    severity="error",
                    confidence=1.0,
                    message="The policy selects one or more unknown discipline IDs.",
                    evidence=[note.partition(":")[2].strip()],
                    remediation="Select discipline IDs from the active engineering-core catalog.",
                )
            )
        elif note == "missing one or more catalog/list command fields":
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="policy.command-surface",
                    severity="warning",
                    confidence=1.0,
                    message="The policy omits one or more reproducible catalog/list commands.",
                    remediation="Record the catalog, discipline-list, and template-list commands.",
                )
            )
        elif note == "no lane declared":
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="policy.missing-lane",
                    severity="warning",
                    confidence=1.0,
                    message="No language lane or explicit lane status is declared.",
                )
            )
        elif note == "no disciplines declared":
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="policy.missing-disciplines",
                    severity="warning",
                    confidence=1.0,
                    message="No cross-language disciplines are declared.",
                )
            )
    return diagnostics


def _requirement_diagnostics(record: dict[str, Any], catalog: dict[str, Any]) -> list[ScanDiagnostic]:
    selected = set(record.get("lanes", [])) | set(record.get("disciplines", []))
    diagnostics: list[ScanDiagnostic] = []
    for lane in record.get("lanes", []):
        for requirement in _requirements(catalog).get(lane, []):
            if requirement in selected:
                continue
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id="catalog.unsatisfied-requirement",
                    severity="error",
                    confidence=1.0,
                    message=f"Selected lane/addendum {lane!r} requires {requirement!r}.",
                    evidence=[lane, requirement],
                    remediation=f"Select {requirement!r} or remove {lane!r}.",
                )
            )
    return diagnostics


def _semantic_diagnostics(record: dict[str, Any]) -> list[ScanDiagnostic]:
    diagnostics: list[ScanDiagnostic] = []
    for flag in record.get("semantic_flags", []):
        if flag.startswith("missing_expected_discipline:"):
            parts = flag.split(":", 2)
            discipline = parts[1] if len(parts) > 1 else "unknown"
            reason = parts[2] if len(parts) > 2 else "unknown"
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id=f"semantic.expected-discipline.{_slug(discipline)}",
                    severity="advisory",
                    confidence=0.70,
                    message=f"Repository signals suggest reviewing whether {discipline!r} applies.",
                    evidence=[reason],
                    remediation="Review with repository context; do not auto-select a discipline from this heuristic alone.",
                    suppressible=True,
                )
            )
        else:
            diagnostics.append(
                diagnostic(
                    record,
                    rule_id=f"semantic.{_slug(flag)}",
                    severity="advisory",
                    confidence=0.55,
                    message="The scanner raised a heuristic semantic review signal.",
                    evidence=[flag],
                    remediation="Review the signal with repository context before changing policy.",
                    suppressible=True,
                )
            )
    return diagnostics


def build_diagnostics(scan: dict[str, Any], catalog: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[ScanDiagnostic] = []
    for record in scan.get("records", []):
        if not isinstance(record, dict):
            continue
        diagnostics.extend(_structural_diagnostics(record))
        diagnostics.extend(_requirement_diagnostics(record, catalog))
        diagnostics.extend(_semantic_diagnostics(record))
    unique = {item.fingerprint: item for item in diagnostics}
    ordered = sorted(
        unique.values(),
        key=lambda item: (
            SEVERITY_RANK[item.severity],
            item.scope_label,
            item.path,
            item.rule_id,
            item.fingerprint,
        ),
    )
    return [asdict(item) for item in ordered]


def make_baseline(diagnostics: list[dict[str, Any]], *, generated_at: str | None = None) -> dict[str, Any]:
    issues = [
        {
            "fingerprint": item["fingerprint"],
            "rule_id": item["rule_id"],
            "severity": item["severity"],
            "scope_label": item["scope_label"],
            "path": item["path"],
        }
        for item in diagnostics
    ]
    return {
        "schema_version": BASELINE_SCHEMA_VERSION,
        "generated_at": generated_at,
        "issues": sorted(issues, key=lambda item: item["fingerprint"]),
    }


def load_baseline(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != BASELINE_SCHEMA_VERSION:
        raise ValueError(f"unsupported scan baseline: {path}")
    issues = value.get("issues")
    if not isinstance(issues, list):
        raise ValueError(f"baseline issues must be a list: {path}")
    return value


def evaluate(
    diagnostics: list[dict[str, Any]],
    *,
    baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    baseline_issues = baseline.get("issues", []) if baseline else []
    baseline_by_fingerprint = {
        item.get("fingerprint"): item
        for item in baseline_issues
        if isinstance(item, dict) and isinstance(item.get("fingerprint"), str)
    }
    current_by_fingerprint = {item["fingerprint"]: item for item in diagnostics}
    new_diagnostics = [
        item for item in diagnostics if item["fingerprint"] not in baseline_by_fingerprint
    ]
    resolved = [
        item
        for fingerprint, item in sorted(baseline_by_fingerprint.items())
        if fingerprint not in current_by_fingerprint
    ]
    counts = {
        severity: sum(item["severity"] == severity for item in diagnostics)
        for severity in SEVERITIES
    }
    new_counts = {
        severity: sum(item["severity"] == severity for item in new_diagnostics)
        for severity in SEVERITIES
    }
    return {
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "baseline_supplied": baseline is not None,
        "summary": {
            "total": len(diagnostics),
            "counts": counts,
            "new": len(new_diagnostics),
            "new_counts": new_counts,
            "resolved": len(resolved),
        },
        "diagnostics": diagnostics,
        "new_diagnostics": new_diagnostics,
        "resolved_baseline_issues": resolved,
    }


def normalize_selectors(values: Iterable[str]) -> list[str]:
    selectors: list[str] = []
    for value in values:
        selectors.extend(part.strip() for part in value.split(",") if part.strip())
    return sorted(set(selectors))


def selector_matches(item: dict[str, Any], selector: str) -> bool:
    if selector in SEVERITIES:
        return item.get("severity") == selector
    if selector.endswith("*"):
        return str(item.get("rule_id", "")).startswith(selector[:-1])
    return item.get("rule_id") == selector


def failing_diagnostics(evaluation: dict[str, Any], selectors: Iterable[str]) -> list[dict[str, Any]]:
    normalized = normalize_selectors(selectors)
    if not normalized:
        return []
    candidates = (
        evaluation.get("new_diagnostics", [])
        if evaluation.get("baseline_supplied")
        else evaluation.get("diagnostics", [])
    )
    return [
        item
        for item in candidates
        if any(selector_matches(item, selector) for selector in normalized)
    ]


def render_markdown(evaluation: dict[str, Any]) -> str:
    summary = evaluation["summary"]
    lines = [
        "## Stable diagnostics and ratchet",
        "",
        f"- Baseline supplied: `{evaluation['baseline_supplied']}`",
        f"- Current diagnostics: `{summary['total']}`",
        f"- Current counts: `{json.dumps(summary['counts'], sort_keys=True)}`",
        f"- New diagnostics: `{summary['new']}`",
        f"- New counts: `{json.dumps(summary['new_counts'], sort_keys=True)}`",
        f"- Resolved baseline issues: `{summary['resolved']}`",
        "",
    ]
    diagnostics = evaluation["diagnostics"]
    if not diagnostics:
        lines.append("No stable diagnostics were emitted.")
        return "\n".join(lines) + "\n"
    lines.extend(
        [
            "| Severity | Rule | Scope | Path | Confidence | New | Evidence |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    new_fingerprints = {item["fingerprint"] for item in evaluation["new_diagnostics"]}
    for item in diagnostics:
        evidence = "; ".join(item.get("evidence", [])) or "-"
        lines.append(
            f"| {item['severity']} | `{item['rule_id']}` | `{item['scope_label']}` | "
            f"`{item['path']}` | {item['confidence']:.2f} | "
            f"{'yes' if item['fingerprint'] in new_fingerprints else 'no'} | {evidence} |"
        )
    return "\n".join(lines) + "\n"
