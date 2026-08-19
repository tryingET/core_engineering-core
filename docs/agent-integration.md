---
summary: "Agent workflow for safe engineering-core recommendation, diagnosis, adoption, migration, and fleet ratcheting."
read_when:
  - "An agent is applying engineering-core in a repository or scanning a fleet."
type: "guide"
---

# Agent integration

The packaged engineering-core skill is a procedural interface over the CLI, not a second source of doctrine. Its canonical source lives at `src/engineering_core/skill/SKILL.md`; `skills/engineering-core/SKILL.md` is a checked projection.

Harness-selected instructions remain authoritative for the active agent session. In particular, Pi may load hierarchical repository `AGENTS.md` files; engineering-core does not flatten, regenerate, or replace that hierarchy. Agents should apply the skill only within the scope and precedence established by the harness and owning repository.

Agents should inspect repository instructions and current work, propose recommendations with evidence, run `doctor`, review `init` or `migrate` dry-run diffs, apply only within the authorized scope, and report validation evidence. Fleet scans should baseline existing debt and fail only newly introduced diagnostics matching explicit selectors.

Objective policy/catalog failures may be gated. Semantic discipline suggestions remain suppressible advisories unless the owning scope deliberately promotes them.

When integration needs durable runtime evidence, use the boundaries in `docs/evidence-semantics-boundaries.md`: engineering-core defines the portable engineering record, agent-kernel persists runtime evidence and lineage, ontology-kernel owns shared meanings, and rocs-cli resolves and validates ontology material without promoting authority.
