---
summary: "Validation, rollout, and rollback contract for capability observation."
read_when:
  - "Validating or rolling out doctor and capability scans."
type: "validation-rollout-rollback"
---

# Capability observation — Validation, rollout, rollback

## Validation

- Unit-test every parser transition, report shape, pin posture, population bound, and CLI exit.
- Run both deterministic dogfood scripts twice and compare bytes.
- Confirm command and external-model sentinels remain untouched.
- Verify existing plan, advise, closed-loop, and scan-adoption commands.
- Run strict docs checks and build/artifact inspection.

## Rollout

1. Ship the additive package version and tag.
2. Dogfood in engineering-core with a temporary declared fixture; the owner repo need not pretend to be a consumer.
3. Canary explicit owner-selected repositories across language/archetype lanes.
4. Generate owner-local warning-only reports.
5. Add repository declarations deliberately; do not bulk mutate from scanner output.
6. Attach runtime evidence through repo/AK owner surfaces before claiming execution closure.

## Rollback

- Revert the additive command/modules and optional policy interpretation.
- Existing policies without the capability block require no migration.
- Existing policies with the block are ignored by older versions and contain no executable fields.
- Delete owner-local generated reports if their schema is withdrawn; no canonical runtime state is owned by engineering-core.
