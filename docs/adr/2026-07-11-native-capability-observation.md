---
summary: "ADR adopting native read-only doctor and explicit-population capability observation."
read_when:
  - "Changing doctor, capability declarations, or cross-repo capability reports."
type: "adr"
---

# ADR — Native capability observation

## Decision

Adopt the architecture in `docs/rfc/2026-07-11-capability-observation-and-doctor.md`:

- stable doctor, capability parsing, and capability scan semantics ship as package modules and native CLI commands;
- scripts remain dogfood/release orchestration only;
- `engineering-core-capabilities-v1` is an optional exact nested policy contract;
- `doctor` performs deterministic static checks and never executes consumer commands or invokes a model;
- `scan-capabilities` consumes explicit owner-produced repository paths and reports declaration, static observation, and evidence dimensions separately;
- v1 does not ingest receipts or emit evidence promotion states;
- existing policy and `scan-adoption` behavior remain compatible.

## Consequences

Positive:

- operators gain reusable commands rather than copied shell snippets;
- capability maturity becomes measurable without overclaiming adoption;
- society-wide denominators remain owner-controlled;
- outputs are deterministic and suitable for owner-local dashboards.

Costs:

- repositories must deliberately add the optional capability contract;
- static observability does not prove execution or rollout closure;
- a later owner-approved receipt integration is required for evidence maturity.

## Validation

Implementation must satisfy `docs/plans/2026-07-11-capability-observation-implementation.md`, including deterministic dogfood, negative path/security probes, full regression tests, docs validation, and build artifact inspection.

## Rollback

Revert the additive modules, CLI parsers, and capability parser fields. Existing policies continue to parse and existing commands remain unaffected.
