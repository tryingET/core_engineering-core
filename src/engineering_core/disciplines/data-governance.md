---
summary: "Cross-language data governance discipline for authority, schema, lineage, lifecycle, quality, privacy, and migration."
read_when:
  - "Work changes data models, schemas, identifiers, canonical stores, projections, imports/exports, retention, lineage, backups, or analytics feeds."
  - "A repo needs to decide what data is authoritative, derived, cached, migrated, retained, deleted, or safe to use for product/AI/analytics claims."
type: "guide"
---

# Discipline — Data Governance

## Purpose

Data governance owns cross-language invariants for data authority, modeling, schema evolution, lineage, quality, lifecycle, privacy, retention, import/export, backup, and migration. Language lanes choose databases, ORMs, serializers, migration tools, and query libraries.

This discipline is broader than `local-first-data`: it applies to services, batch jobs, CLIs, browser apps, ML datasets, event streams, generated projections, analytics stores, and release artifacts. `local-first-data` owns offline/local persistence and sync details.

## Load when

Load this discipline when work touches:

- canonical records, schemas, identifiers, ownership, or data authority
- migrations, backfills, imports, exports, retention, deletion, archival, or recovery
- derived data, caches, projections, reports, search indexes, analytics, events, or materialized views
- data quality, lineage, provenance, deduplication, reconciliation, or auditability
- datasets used for AI/ML, evaluation, analytics, product decisions, or external claims
- cross-service data flow, two-writer risk, replication, sync, or consistency boundaries

Do not load it for ephemeral in-memory state with no persistence, no external consumer, and no product/evidence claim.

## Authority rule

Every durable data shape must declare its authority class:

| Class | Rule |
|---|---|
| canonical record | The source of truth; migrations, ownership, and recovery required. |
| derived projection | Regenerable from authority; must not become hidden truth. |
| cache | Disposable; eviction/corruption must not lose truth. |
| event/audit log | Append-oriented evidence; correction is usually additive, not destructive. |
| import/export artifact | Boundary contract; schema, provenance, and compatibility matter. |
| analytics/eval dataset | Evidence substrate; lineage, sampling, and bias limits matter. |
| configuration/reference data | Precedence, ownership, and rollout semantics must be explicit. |

If two stores can mutate the same fact, the system needs conflict policy or one writer must be removed.

## Controlled data and semantic references

Controlled vocabularies, ontology terms, and semantic identifiers are data dependencies with an owner. Do not copy their definitions into local docs or database tables unless the repo owns that vocabulary.

- Store stable references to controlled terms when runtime data needs them.
- Keep display labels, descriptions, and ontology definitions with the semantic owner.
- Treat local lookup tables as caches/projections unless explicitly owned by the repo.
- Validate references through the repo's accepted semantic/ROCS path when shared meaning matters.

For the AI Society authority split, link rather than duplicate:

- [[~/ai-society/softwareco/owned/agent-kernel/docs/project/ai-society-convergence-architecture.md|AI Society Convergence Architecture]]
- [[~/ai-society/softwareco/owned/agent-kernel/docs/project/2026-04-25-layer-12-operator-vocabulary-boundary.md|Layer-12 Operator Vocabulary Boundary]]

## Schema and identifier invariants

- Name stable identifiers deliberately; do not overload display names, slugs, paths, or timestamps as identity unless that is the domain rule.
- Separate internal IDs, external IDs, tenant/user IDs, correlation IDs, and idempotency keys.
- Make null/unknown/default/deleted states explicit.
- Version schemas that cross process, repo, artifact, or time boundaries.
- Record compatibility expectations for readers and writers before changing persisted shape.
- Treat enum/value-set changes as compatibility changes when consumers branch on them.

## Lineage and provenance

Data used for decisions or claims needs traceability:

- source system or collection method
- ingestion/import command or pipeline
- transformation steps and code version where practical
- timestamp/version/window
- filtering, sampling, deduplication, and join semantics
- known gaps, bias, quality limits, and privacy constraints

A dashboard, eval score, or product decision based on untraceable data is weak evidence.

## Lifecycle and retention

Durable data needs lifecycle rules:

- create/update/delete/archive ownership
- retention period and deletion path
- backup/restore posture for canonical stores
- export path when users/operators need portability or review
- recovery behavior for partial imports, failed migrations, and corrupt records
- privacy classification and redaction/minimization rules

Delete must mean something precise: soft delete, tombstone, redaction, cryptographic erasure, archive, or irreversible removal.

## Migrations and backfills

Migrations are changes to time, not just schema:

- prefer expand/contract for rolling compatibility
- make backfills idempotent and resumable when data volume or risk is material
- record ordering relative to deploys, jobs, generated clients, and readers
- verify representative old data, empty data, malformed data, and high-volume data
- decide whether rollback restores old schema, keeps forward-compatible readers, or requires compensating migration

Do not write destructive migrations without backup/export/recovery posture.

## Data quality

Quality checks should match the risk:

- referential integrity and uniqueness for canonical relationships
- range/domain checks for values that drive behavior
- freshness checks for time-sensitive projections and analytics
- completeness checks for imports and reports
- reconciliation checks between canonical and derived stores
- anomaly checks for metrics/eval datasets where claims depend on them

Quality checks belong in deterministic validation or observability, not only in human inspection.

## Operational vs analytical data

Operational data serves product behavior. Analytical data supports measurement and decisions. Do not silently swap them.

- Operational stores optimize correctness, transactions, latency, and recovery.
- Analytical stores optimize historical queries, aggregation, sampling, and reproducibility.
- Events may feed both, but event semantics must be stable enough for each use.
- Analytics derived from operational exhaust still needs privacy review and lineage.

## Cross-references

- `domain-modeling` owns vocabulary, invariants, workflows, and aggregate boundaries.
- `service-api` owns transport contracts, idempotency, health, and deployment boundaries.
- `local-first-data` owns offline/local storage, sync, corruption, and export/reset behavior.
- `ai-ml` owns dataset/eval/model-specific evidence and safety claims.
- `security-privacy` owns data classification, minimization, secrets, and privacy posture.
- `release-package` owns compatibility and migration releases for distributed artifacts.

## Validation expectations

For material data changes, provide the smallest truthful evidence set:

- declared authority class and owner
- schema/migration/backfill path and rollback/repair posture
- representative fixture or dry-run evidence for old/new/malformed/empty data
- quality checks for invariants that matter to product or evidence claims
- privacy/retention review when user or sensitive data is involved
- regeneration/drift check for derived projections where applicable

## Failure modes

- A cache, report, markdown file, or search index becomes hidden authority.
- Two services write the same fact with no conflict policy.
- A migration works on new fixtures but corrupts old production-shaped data.
- A dashboard/eval claim depends on data with no lineage.
- Delete means different things in product, database, backups, and exports.
- Enum/string values become a silent cross-repo API with no compatibility policy.
