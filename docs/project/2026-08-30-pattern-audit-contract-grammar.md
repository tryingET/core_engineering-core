---
summary: "Pattern audit applying the 5082 template (symmetric grammar, self-describing payloads, type-explicit errors) to work_packet, work_verify, and evidence_reconcile contracts."
read_when:
  - "Changing validator error messages, packet schemas, or grammar documentation for work context/receipt/disposition and evidence reconciliation."
type: "audit"
---

# Contract grammar pattern audit (AK #5083, 5082 template)

Scope audited: `work_packet.py` (context / advice-request / bounded-plan /
scope-snapshot grammars), `work_verify.py` (verification contract),
`evidence_reconcile.py` (evidence receipts). The 5082 template has three
pillars; findings are classified per pillar and each has a disposition:
**applied** (landed with this audit), **deferred** (needs wire-format change,
schema-v2 item), or **documented** (invariant already held).

## Pillar 1 — Symmetric grammar (grammar must ship, not just enforce)

| ID | Finding | Disposition |
|---|---|---|
| G1 | No shipped machine-readable grammar: every grammar lives only in Python validators. A consumer cannot construct a valid context/request/receipt without reading source code. | Deferred: publish a `schemas/` companion (JSON Schema per shipped schema id) or a generated grammar annex in docs; generation should be deterministic from the validators so it cannot drift. |
| G2 | `scope_snapshot` and its file entries carry no schema identity at all (unlike context/request/plan/reconciliation, which each embed a schema id). | Deferred to snapshot schema-v2: adding a `schema` key changes `scope_sha256` digest input, i.e. a wire change; must ride a version bump, not a patch. |

## Pillar 2 — Self-describing payloads

| ID | Finding | Disposition |
|---|---|---|
| P1 | context (`CONTEXT_SCHEMA`), advice request (`WORK_REQUEST_SCHEMA`), bounded plan (`engineering-bounded-work-plan-v1`), reconciliation (`engineering-evidence-reconciliation-v1`) all embed schema ids. | Documented: invariant held. |
| P2 | `scope_snapshot` (see G2). | Deferred (same v2). |

## Pillar 3 — Type-explicit errors (the 5082 falsification lesson)

The falsification defect class: a consumer sends the wrong *type* and the
rejection neither names the expected type nor the observed type, so the error
cannot be acted on without source archaeology. Audit of every raise site:

| Validator | Before | After (applied) |
|---|---|---|
| `_finite_json` | "contains a non-finite number" | names path-relative `where` and the observed float (already near-compliant; kept) |
| `_exact` | "must contain exactly: <keys>" — no observed shape | "expected object with exactly <keys>; got <observed-kind>" incl. missing/extra key sets when input is a dict |
| `_text` | one message conflating 4 violations (non-str, blank, >4096B, control chars) | per-violation message naming expected type+constraint and observed type |
| `_texts` | "must be an array with at most N entries" | adds observed kind for the non-list case |
| `_relative_path` | "must be a safe repository-relative path" | adds which safety property failed (absolute/escape/prefix/empty) |
| composite mushers ("scope snapshot file entry is invalid", "work advice evidence is invalid", "verification schema or result is invalid") | bundle 3–8 distinct checks per message | split at the highest-traffic sites; remainder listed below for mechanical follow-up |
| `evidence_reconcile._git` | raises bare `ValueError` (not a domain error class) | Documented E1: introduce `EvidenceReconcileError` or adopt the packet error family in a follow-up; changing the raise type is caller-visible |

Remaining mechanical follow-up (same rewrite recipe, no design decisions):
the per-field composites inside `_validate_snapshot`, `_request_digest`,
`validate_packet`'s evidence/safeguard branches, and `work_verify`'s
verification posture checks.

## Tests

No test asserts validator message text (verified by grep over
`tests/test_work_packet.py`, `test_work_bundle.py`, `test_evidence_reconcile.py`);
rejections are asserted via exception type. The applied rewrites are
behavior-preserving for type, raise class, and validation outcomes.
