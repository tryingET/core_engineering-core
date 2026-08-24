---
summary: "G2 federated-interoperation conformance protocol and deterministic fixture/negotiation/bounds harness for engineering-core v1.0 convergence."
read_when:
  - "Executing, reviewing, or validating Gate G2 interoperation proof under decision 128."
  - "Authoring or binding a G2 fixture corpus, negotiation transcript, or resource-bound manifest."
type: "implementation-plan"
---

# G2 federated-interoperation proof protocol

Controlling contract: `docs/rfc/2026-08-23-v1-convergence-contract-r5.md` (Gate G2),
accepted as `docs/adr/2026-08-23-v1-convergence-contract.md`.
Harness: `scripts/v1/federated_interoperation.py` (internal qualification tooling).
Tests: `tests/test_v1_federated_interoperation.py`.

## Authority boundaries

- **Candidate-independent at G0-A2.** The fixture *template* manifest, threat matrix,
  normalization algorithm, negotiation rules, and resource-bound ceilings are frozen
  here. Candidate bytes, candidate-dependent fixtures, and their expected-result digests
  are `unassigned` and bind only at G0-B through the frozen materializer and independent
  oracle. The harness never fabricates expected results from candidate execution.
- The harness validates records; it executes no consumer command, model, URL, Git helper,
  or observation reference, and mutates no participant repository. Generated reports and
  remediation remain with consuming owners.
- No hosted control plane and no centrally invented society denominator: every count or
  percentage carries its exact frozen denominator.

## Frozen fixture classes

Compatibility records: `pre_v1_clean_transition`, `pre_v1_explicit_migration`,
`pre_v1_unsupported`, `canonical_candidate_v1`, `additive_v1x`, `unsupported_future_major`,
`unknown_critical_extension`. Population completeness: `complete`, `partial`,
`unavailable`, `denied`, `redacted`, `stale`, `unsupported`. Structure/duplication:
`duplicate_json`, `reordering`, `unknown_fields`, `unknown_schema`, `catalog_skew`.
Malformed/hostile: `malformed_json`, `invalid_utf8`, `depth_limit`, `size_limit`,
`growth_limit`, `exact_limit`, `path_absolute`, `path_empty`, `path_dot`,
`path_traversal`, `path_control_chars`, `path_option_injection`, `revision_ambiguous`,
`symlink_target`, `hardlink_target`, `special_file`, `unreadable_file`, `unwritable_file`,
`parent_replacement`, `toctou_race`, `hostile_git_helper`, `terminal_injection`,
`markdown_injection`, `html_injection`, `link_injection`, `url_payload`,
`tool_instruction`, `hostile_patch`, `hostile_model_response`.

Every valid-class fixture MUST pass; every invalid/unsupported-class fixture MUST fail at
its frozen boundary with structured, bounded, sanitized diagnostics. Missing, private,
stale, or unsupported records stay explicitly `incomplete`/`unsupported` and are never
coerced to adopted, healthy, current, or verified. Duplicate physical identities cannot
inflate denominators.

## Entrypoint × threat matrix

Rows: every command, parser, renderer, Git/subprocess call, output path, owner-boundary
transfer, and model-response sink. Columns: the threat families above. Every cell carries
a fixture or an independently reviewed `not_applicable` rationale; an empty cell fails
validation.

## Version negotiation (frozen algorithm)

A peer authenticates its **complete offer**: peer identities, offer ID, freshness/replay
scope, channel/artifact binding, payload digest. The reader intersects the offer with its
trusted allowlist, rejects stale/replayed/stripped offers, selects the highest common
version at or above its declared floor, and binds offer, selection, identities, floor,
and payload digest in the result. Parse errors, attacker claims, and unknown critical
extensions never trigger fallback; unknown non-critical fields follow the owning
protocol's declared preserve/ignore rule.

## Adapter chain (frozen invariants)

Conversion occurs once at bounded ingress; egress renders only a declared target and
appends to the same lineage. Each conversion binds input/output digests, adapter
executable/configuration digest, trust decision, identity/version, defaults,
transformations/losses, and prior chain. Double conversion and chain truncation fail.

## Resource bounds

G0-A2 derives qualification-only population, filesystem, output, memory, CPU, subprocess,
and wall-clock budgets from measured supported-platform baselines plus a declared safety
margin, and freezes benchmark/toolchain/rationale before any output. Bounds cannot be
raised after the output-visibility flag is set and cannot undercut the frozen
**public** parser/schema acceptance guarantees. Permission probes never elevate/repair;
timeout/cancellation kills the process tree and leaves no accepted partial artifact.

## Pass threshold (frozen)

G2 passes only when validated records show: **100%** of the frozen corpus and
entrypoint × threat matrix at their boundaries; at least two positive owner groups
independently consuming identical approved aggregate bytes with equal normalized results;
deterministic payloads byte-identical across two runs from identical ordered inputs;
missing/unavailable/private/stale/unsupported never coerced; no executed command, model,
URL, helper, or hostile content in scan/aggregation paths; transfers only under the
default-deny rule; and zero synthetic-canary disclosures, path escapes, authority
promotions, bound overruns, blocking special-file reads, surviving processes, or partial
accepted outputs.

## Rollback

The additive conformance harness can be withdrawn without changing owner records. Any
template, normalization rule, bound, sink, oracle, or materialization change after the
applicable visibility boundary creates a new protocol revision and restarts G2.
