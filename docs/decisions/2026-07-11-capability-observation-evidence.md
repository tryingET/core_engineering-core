---
summary: "Evidence supporting native doctor and capability observation architecture."
read_when:
  - "Reviewing evidence for the capability observation decision."
type: "evidence-note"
---

# Evidence note — Capability observation

## Current product evidence

- `engineering-core --help` exposes plan, explain, advise, receipt, disposition, calibration, patterns, doctrine-propose, and scan-adoption; it has no doctor or capability scan.
- Self-dogfood produced a complete `engineering-plan-v1` with stable digest inputs and a bounded `engineering-advice-request-v1`.
- `scripts/dogfood-closed-loop.py` proves the v0.5 closed loop deterministically, but scripts are not a reusable cross-repo product contract.
- `scan-adoption` classifies existing structural policy/docs and optional loop-validation declarations; it does not inspect v0.5 capability declarations.

## Workspace orientation evidence

A read-only scan over 84 explicit git repository paths across core, softwareco/owned, softwareco/infra, holdingco, teachingco, and healthco found:

- 44 structurally adopted under the existing scanner;
- 29 missing;
- 8 legacy-only;
- 1 doc-only;
- 1 partial;
- 1 invalid policy;
- 41 complete loop-validation declarations;
- zero inspected policy/docs references to v0.5 capability schemas or commands.

A broad recursive scan exhausted its shared file budget before reaching later scopes, demonstrating that engineering-core should consume an explicit owner-produced population rather than claim canonical society discovery.

## Review evidence

Adversarial architecture review required and closed blockers around proof transitions, CLI exit behavior, nested schema exactness, pin compatibility, no-follow population files, empty/omitted capability semantics, and release/dogfood obligations. Final outcome: `ready_for_implementation`.
