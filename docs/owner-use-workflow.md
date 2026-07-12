---
summary: "Deterministic prepare, finalize, and verify workflow for owner-use engineering packets and evidence bundles."
read_when:
  - "Preparing bounded engineering work from owner task context."
  - "Joining external advice, owner dispositions, and receipts without authority promotion."
  - "Verifying whether a work bundle still matches a repository."
type: "guide"
---

# Owner-use engineering workflow

Engineering-core v0.8 connects planning, bounded advice, owner disposition, receipts, and repository drift verification without becoming an execution engine or authority store.

```text
owner task context + explicit repository
  -> prepare-work
  -> engineering-work-packet-v1
  -> optional external model or human advice
  -> owner disposition / owner receipt
  -> finalize-work
  -> engineering-evidence-bundle-v1
  -> verify-work
  -> matched | stale | mismatched
```

The commands invoke no model, execute no consumer command, apply no patch, open no receipt observation reference during finalization, and mutate no AK, CI, release, compliance, rollout, approval, or doctrine state. Output is deterministic JSON on stdout; the caller chooses whether and where to store it.

## Owner context

`prepare-work` accepts one bounded, no-follow `engineering-work-context-v1` JSON file:

```json
{
  "schema": "engineering-work-context-v1",
  "authority": "owner-supplied task context; repository and task authorities remain external",
  "repository_id": "softwareco/owned/example",
  "work": {
    "id": "task-123",
    "title": "Implement a bounded slice",
    "objective": "State the intended outcome without embedding secrets."
  },
  "mode": "advisor-ready",
  "scope": {
    "focus_paths": ["src/example.py", "tests/test_example.py"],
    "constraints": ["Do not widen beyond the owner task."],
    "validation": ["Run the owner-selected gate after implementation."]
  },
  "provenance": {
    "owner": "softwareco/owned/example",
    "owner_type": "repository",
    "produced_at": "2026-07-12T00:00:00Z",
    "source": "AK task projection prepared by the owner"
  }
}
```

The context is a projection. AK or another declared owner remains authoritative for task state. Paths are exact repository-relative focus files, not globs or command declarations. `plan-only` omits an advisor request; `advisor-ready` includes one.

## Prepare

```bash
engineering-core prepare-work \
  --repo /path/to/repository \
  --repo-id softwareco/owned/example \
  --context context.json \
  --pretty > work-packet.json
```

`engineering-work-packet-v1` binds:

- explicit repository identity and physical Git root;
- full Git commit ID;
- owner context and canonical digest;
- no-follow SHA-256 snapshots of focused files;
- bounded Git-status fingerprint for those paths;
- deterministic `engineering-plan-v1`;
- optional task-bound `engineering-work-advice-request-v1`, including redacted focused-file evidence and a bounded work plan;
- catalog, repository-facts, plan, context, scope, revision, and request digests.

Preparation reads the focused scope twice and compiles the plan/request twice. Revision, scope, or deterministic-output drift fails closed.

## External advice and owner review

Engineering-core does not call a provider. An owner may give the packet's task-bound advisor request to a human or an external adapter, then validate the returned `engineering-advice-response-v1` through `finalize-work`. Two different owner contexts in one unchanged repository produce different request bindings, preventing advice from silently crossing tasks.

Advice remains advisory. Patch proposals remain inert text. A disposition remains an owner claim and must bind the exact request, canonical advice, plan, catalog, repository facts, repository identity, revision, and recommendation ID.

## Finalize

```bash
engineering-core finalize-work \
  --packet work-packet.json \
  --advice advice.json \
  --disposition disposition.json \
  --receipt receipt.json \
  --pretty > evidence-bundle.json
```

Advice, dispositions, and receipts are optional, but joins fail closed:

- dispositions require exact supplied advice;
- one recommendation cannot have ambiguous dispositions;
- advisor receipts require one exact supplied disposition;
- owner, repository, revision, plan, catalog, facts, request, and advice bindings must agree;
- owner receipt states are preserved verbatim and never renamed to independent verification.

The bundle records both raw input-content and canonical-object SHA-256 lineage. Each supplied recommendation appears as an explicit record even while its decision is pending. Owner-use receipts require an exact supplied advice/disposition chain. Finalization does not open receipt observation references; use `reconcile-evidence` separately when tracked artifact and Git-blob reconciliation is required.

## Owner handoff summary

```bash
engineering-core summarize-work \
  --bundle evidence-bundle.json \
  --verification verification.json \
  --format markdown
```

The summary exposes objective, focus paths, pending recommendations, owner validation expectations, drift posture, and the next authority handoff without requiring JSON archaeology. It remains a projection; it cannot author an owner decision.

## Verify

```bash
engineering-core verify-work \
  --repo /path/to/repository \
  --repo-id softwareco/owned/example \
  --bundle evidence-bundle.json \
  --pretty
```

Results:

- `matched` — exact current revision, focused scope, plan, and optional request still match;
- `stale` — the packet revision remains an ancestor but revision, scope, or deterministic bindings drifted;
- `mismatched` — invalid bundle, wrong repository identity/path, unavailable or unrelated revision, or another hard trust-boundary failure.

`verify-work` exits non-zero for `stale` and `mismatched`. It is read-only and does not promote owner evidence.

## Input safety

All workflow JSON uses bounded, no-follow, regular-file-only, duplicate-member-rejecting UTF-8 reads. Workflow packets/bundles have compatible 4 MiB/8 MiB output and input ceilings, and repeated owner records are capped. Symlinked parents/final components (including absent leaves below symlinks), FIFOs, sockets, devices, oversized files, read races, non-finite JSON numbers, Git pathspec magic, unsafe focus paths, duplicate identities, and obvious secret-bearing records are rejected. Fixed Git status probes disable fsmonitor, untracked-cache integration, pathspec magic, and optional locks.

## Relationship to other commands

- `plan` and `advise` remain standalone compiler/adapter surfaces.
- `doctor` and `scan-capabilities` remain static and receipt-free.
- `reconcile-evidence` remains the tracked artifact/Git reconciliation surface.
- `prepare-work`, `finalize-work`, and `verify-work` provide deterministic glue over explicit owner inputs; they do not replace those commands or their authority boundaries.
