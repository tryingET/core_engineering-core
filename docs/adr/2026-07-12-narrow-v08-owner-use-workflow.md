---
summary: "Decision to retain engineering-core v0.8 owner-use packets narrowly as deterministic derived projections, not source, task, disposition, receipt, or evidence authority."
read_when:
  - "Changing prepare-work, finalize-work, verify-work, or owner-use evidence bundles."
  - "Deciding whether engineering-core should acquire context or persist operational authority."
type: "adr"
---

# ADR — Narrow engineering-core v0.8 owner-use workflow

## Decision

Retain engineering-core v0.8 narrowly as a deterministic validation, packaging, and freshness-verification membrane over explicit owner-approved inputs.

The retained contract is:

- callers supply an explicit repository, owner task projection, and exact focus paths;
- `prepare-work` binds those inputs to repository identity, revision, bounded snapshots, and deterministic digests;
- advice remains optional and inert;
- `finalize-work` validates exact joins and emits a derived bundle chosen by the caller;
- `verify-work=matched` proves only binding and currentness, never execution, test success, approval, release readiness, or canonical evidence;
- source acquisition and budgeted selection remain delegated to context-packer or another explicit source owner;
- canonical task, decision, lineage, receipt, and evidence facts remain in Agent Kernel or the declared source-owner surface;
- engineering-core packets and bundles must not become a backlog, disposition inbox, receipt store, or parallel evidence database.

## Review disposition

The v0.8 release and validation are accepted with narrowing rather than adopted as a complete owner lifecycle.

Existing canaries prove deterministic preparation, exact binding, stale/mismatch detection, non-execution, and cross-repository rejection. They do not prove a complete owner disposition/receipt round trip: the recorded canaries contain pending recommendations and zero owner dispositions or receipts. That limitation is preserved as evidence rather than upgraded by inference.

The source-list/SCI experiment is outside engineering-core authority. Its current owner evidence rejects automatic source-list wiring and explicitly defers the unavailable SCI arm; this decision does not reopen or override that result.

## Consequences

Positive:

- engineering-core retains useful deterministic engineering-contract and drift checks;
- context acquisition is not duplicated;
- AK and source owners remain the only operational authority surfaces;
- consumers can use packets as bounded handoffs without interpreting them as completion evidence.

Costs:

- callers must explicitly project owner context and persist authoritative outcomes elsewhere;
- a future full owner-use adoption requires a real disposition/receipt canary;
- documentation and consumer guidance must continue to distinguish `matched` from validation or acceptance.

## Validation and adoption gate

A future expansion beyond this narrow posture requires all of:

1. an owner-approved end-to-end canary with at least one real disposition and receipt;
2. canonical disposition/evidence recorded through AK or the source owner;
3. proof that engineering-core bundles remain derived projections;
4. an explicit decision for any source-acquisition behavior;
5. regression, security, and rollback validation owned by engineering-core.

## Rollback

If the narrow membrane creates authority confusion, remove the additive owner-use commands/modules and retain the earlier doctor, scan, planning, receipt-validation, and closed-loop behavior described by the v0.8 RFC rollback. No consumer authority schema or canonical runtime state depends on engineering-core bundles.

## Evidence

- `docs/rfc/2026-07-11-evidence-reconciliation.md`
- `docs/releases/2026-07-12-v0.8.0-local-release.md`
- `docs/evidence/2026-07-12-v0.8.0-validation.md`
- `docs/evidence/2026-07-12-owner-use-canaries.md`
- AK decision `55`
