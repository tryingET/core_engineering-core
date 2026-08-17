---
summary: "RFC for explicit, read-only owner-evidence reconciliation without changing doctor or capability-scan authority."
read_when:
  - "Reviewing or changing reconcile-evidence, receipt joins, or evidence authority boundaries."
type: "rfc"
system4d:
  container:
    boundary: "Explicit owner receipts, mapped repository identities, bounded artifacts, and current deterministic plans."
    edges:
      - "engineering-evidence-receipt-v1"
      - "engineering-plan-v1"
      - "engineering-advice-response-v1"
  compass:
    driver: "Join real owner-produced artifacts without converting self-reported evidence into independent authority."
    outcome: "Matched, stale, and mismatched evidence projections with deterministic fail-closed behavior."
  engine:
    invariants:
      - "Existing doctor and scan-capabilities v1 outputs remain receipt-free and unchanged."
      - "No consumer commands, models, patches, or observation references are executed."
      - "Owner states are preserved but never upgraded."
  fog:
    risks:
      - "Receipt provenance is self-reported rather than authenticated."
      - "Loose repository or revision matching could manufacture evidence promotion."
---

# RFC: explicit owner-evidence reconciliation

## Problem

Engineering-core v0.6 separates declarations, deterministic static observation, and evidence. Five owner-local actual-use canaries now produce plans, bounded advice, dispositions, and `engineering-evidence-receipt-v1` records, but `doctor` and `scan-capabilities` intentionally report evidence as `not-supplied`.

Directly inserting receipts into those v1 commands would be unsafe. Receipt provenance and states are owner-authored strings, receipt v1 validates internal consistency rather than authenticity, and doctor health describes static repository readiness rather than runtime proof.

## Decision

Add a separate command:

```bash
engineering-core reconcile-evidence \
  --repo <stable-repository-id> <local-path> \
  --receipt <explicit-receipt.json>
```

The command emits `engineering-evidence-reconciliation-v1`. It does not change `engineering-doctor-v1`, `engineering-capability-scan-v1`, declarations, AK evidence, CI/release state, or compliance authority.

## Input membrane

- Repositories are supplied as exact stable-id/path pairs. No basename, remote, suffix, or path inference is allowed.
- Receipts are explicit CLI inputs. No repository discovery, globs, URLs, policy paths, or observation-reference execution is allowed.
- Receipt and artifact reads are bounded to 256 KiB, regular-file-only, no-follow, UTF-8 JSON reads.
- Symlinks, symlinked parents, FIFO/device/socket inputs, controls, traversal, malformed JSON, oversized inputs, and secret-bearing records fail closed.
- Duplicate `(repository, receipt_id)` keys fail closed.

## Join contract

For each receipt:

1. validate `engineering-evidence-receipt-v1` exactly;
2. require `target.repository == provenance.owner == supplied repository id`;
3. require the receipt and artifact paths to remain beneath the mapped repository;
4. select exactly one packaged or repo-local catalog snapshot whose canonical digest equals the receipt binding;
5. compile the current plan twice against that snapshot and require deterministic completion;
6. compare plan, catalog, and repository-facts digests exactly;
7. validate the artifact bytes against the observation SHA-256 from the same bounded read used for parsing;
8. validate either:
   - an `engineering-plan-v1` self-digest and bindings; or
   - an `engineering-advice-response-v1` against a freshly rebuilt bounded request and exact recommendation id;
9. require a full lowercase Git object id and probe Git with fixed arguments only to compare it with a stable current `HEAD` snapshot.

Revision relations:

- `current`: target equals `HEAD`;
- `advanced-compatible`: target is an ancestor and all bounded bindings still match;
- `stale`: ancestry is valid but bounded repository facts drifted;
- `mismatched`: target is missing/non-ancestor, identity differs, an artifact is unsafe, or a schema/digest/recommendation join fails.

Precedence is `mismatched > stale > matched`.

## Evidence meaning

A matched record preserves the owner state, such as `schema-valid`. It never upgrades it. Even `owner-reported evidence-verified` would remain a supplied owner claim, not independent verification.

The command returns:

- result counts for `matched`, `stale`, and `mismatched`;
- matched capability counts for planning and advisor artifacts;
- matched owner-state counts;
- deterministic records, findings, input digests, and structured failures;
- explicit `consumer_commands_executed=false`, `external_models_invoked=false`, and `mutations_performed=[]`.

## Non-goals

- authenticating owners or signatures;
- discovering receipts;
- accepting URLs or repository-declared commands;
- modifying doctor/scan evidence fields;
- claiming execution from an artifact-only receipt;
- applying advice or patches;
- aggregating a society-wide evidence dashboard before single-repository joins are stable.

## Rollback

Remove the additive command/modules and retain v0.6 doctor, scan, receipt-validation, and closed-loop behavior. No consumer repository or authority schema requires migration.
