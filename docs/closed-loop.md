---
summary: "Read-only closed-loop receipt, disposition, calibration, pattern, and doctrine proposal contracts."
read_when:
  - "Producing or reviewing engineering evidence after advisory planning."
type: "reference"
---
# Closed-loop engineering evidence

Engineering-core ingests owner-produced JSON; it does not execute discovered commands, mutate consumer repositories, establish CI/release/AK truth, or apply proposals. Every output is deterministic JSON and retains source digests.

## Contracts and commands

- `engineering-evidence-receipt-v1`: binds owner provenance and observations to plan, catalog, repository-facts, revision, and recommendation. States are `declared`, `schema-valid`, `target-resolved`, `execution-observed`, `evidence-verified`, `stale`, `mismatched`, and `unknown`. State validation checks record consistency, never external truth.
- `engineering-recommendation-disposition-v1`: records `accepted`, `deferred`, `rejected`, or `abstained` with explicit owner provenance and a controlled reason: `adopted`, `needs-evidence`, `needs-owner-decision`, `out-of-scope`, `conflicting-evidence`, `superseded`, `not-applicable`, or `insufficient-evidence`.
- `receipt validate|summarize --receipt FILE`: validates or deterministically aggregates receipts.
- `disposition validate --disposition FILE [--advice FILE]`: optionally verifies advice digest and recommendation identity.
- `calibration --advice FILE --disposition FILE [--receipt FILE]`: keeps model confidence, owner acceptance, and verified-evidence outcomes separate.
- `patterns --plan FILE ...`: synthesizes only explicitly supplied records and preserves their canonical digests.
- `doctrine-propose --patterns FILE`: emits an `unapplied` review proposal with no mutations.

Inputs are capped at 256 KiB each, arrays are bounded, schemas reject extra fields, SHA-256 bindings are mandatory, and obvious secret-bearing input (including JSON key/value syntax) fails closed. These records are evidence and review aids, not authority promotion mechanisms.

## Persistence and shared semantics

The JSON artifacts remain portable and may be stored by any owner-controlled system. In the AI Society environment, agent-kernel is the appropriate canonical runtime store for evidence rows, governance receipts, artifact references, decisions, and lineage. Engineering-core remains the schema producer and validator; persistence in AK does not convert a claim into independent verification or owner approval.

Receipt state and disposition values remain versioned engineering-core protocol terms. They should not be given a broader global meaning merely because another system uses similar words. When a concept is genuinely shared across systems, ontology-kernel owns the canonical definition and rocs-cli validates and resolves the corresponding ontology material. ROCS source conformance does not upgrade evidence state or prove semantic correctness, adoption, activation, or currentness.

See `docs/evidence-semantics-boundaries.md` for the complete responsibility and reference contract.

## Relationship to capability observation

`engineering-core-capabilities-v1` may declare the closed-loop receipt and disposition schema identifiers, but doctor/capability scanning remains receipt-free and reports that capability as `not-observed/not-supplied`. It does not discover or ingest receipts.

v0.7 adds a separate explicit reconciliation surface:

```bash
engineering-core reconcile-evidence \
  --repo <stable-repository-id> /path/to/repo \
  --receipt /path/to/repo/governance/engineering-core-evidence-receipt-v1.json \
  --pretty
```

The command validates bounded no-follow receipt/artifact inputs, exact repository identity, current plan bindings, artifact schemas and digests, advice recommendation identity, and Git revision ancestry. It emits only `matched`, `stale`, or `mismatched` reconciliation results and preserves the supplied owner state without upgrading it. It never changes doctor health, capability declarations, AK evidence, CI/release state, or compliance authority. See `docs/rfc/2026-07-11-evidence-reconciliation.md`.

## Owner-use workflow

v0.8 adds `prepare-work`, `finalize-work`, and `verify-work` as deterministic glue over explicit owner context, plans, optional external advice, dispositions, and receipts. It preserves owner states verbatim and does not treat bundle validation as tracked-artifact reconciliation or independent evidence verification. See `docs/owner-use-workflow.md`.

## Reproducible dogfood

Run `python scripts/dogfood-closed-loop.py`. The temporary, deterministic fixture executes the complete read-only flow: two plans, request-bound advisor validation, all four owner dispositions, verified/failed/stale/mismatched receipt records, calibration, recurring multi-plan patterns, and an unapplied doctrine proposal. It also proves malformed, secret-bearing, hallucinated-path, unknown-ID, and provenance-mismatched inputs are rejected. A sentinel consumer command is declared but never executed; proposed patches are never applied. Running the command twice must produce byte-identical JSON.
