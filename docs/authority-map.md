---
summary: "Authority boundaries for engineering-core, repo-local overrides, templates, validation policy, ontology, evidence, and runtime task truth."
read_when:
  - "Deciding where engineering guidance, validation policy, generated defaults, evidence, semantics, or repo-local deviations should live."
  - "Reviewing whether a proposed change belongs in engineering-core or another owner surface."
type: "reference"
---

# Authority map

Engineering-core is a shared guidance source, not the runtime authority for every engineering decision in the workspace.

## Ownership table

| Concern | Owner surface | Notes |
|---|---|---|
| Shared language lane guidance | `core/engineering-core` | Ecosystem defaults, command surface patterns, conditional addenda, and CLI retrieval. |
| Shared cross-language engineering invariants | `core/engineering-core` disciplines | Portable decision rules that apply across languages and repo shapes. |
| Engineering-specific plans, receipts, dispositions, work bundles, and reconciliation schemas | `core/engineering-core` | Defines and validates portable records while preserving owner state and authority ceilings. It does not execute consumer commands or persist canonical runtime truth. |
| Reusable adoption scanner semantics | `core/engineering-core scan-adoption` | Structural status taxonomy, catalog-aware lane/discipline validation, optional repo-loop-validation visibility, generic package/member discovery, and generic JSON/Markdown rendering. |
| Repo/package-local deviations, selected subset, and loop command semantics | repo-local `docs/engineering.local.md` | Higher priority than shared lane/discipline docs for that repo. Should explain local commands, loop validation mappings when adopted, deviations, and evidence expectations. |
| Machine-readable lane declaration | repo-local `policy/engineering-lane.json` when needed | Useful for generated repos, package validation, and provenance. Do not create it when local docs are enough. |
| Generated adoption snapshots and rollout dashboards | scanned scope owner | Examples: lane/company `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`. These are projections, not core doctrine. |
| Canonical validation-tier policy | `holdingco/governance-kernel` | Engineering-core may reference and summarize validation tiers, but governance-kernel owns the canonical policy source. |
| Generated defaults and propagation behavior | template owner repos | Templates decide what new repos emit. They should reference engineering-core, not fork its doctrine. |
| Runtime tasks, evidence, governance receipts, decisions, artifacts, and lineage | `agent-kernel` / active AK DB | Runtime persistence and custody do not by themselves establish semantic correctness or owner approval. |
| Canonical shared concepts, labels, aliases, relations, and term lifecycle | `core/ontology-kernel` | Engineering-core may reference stable ontology IDs but should keep protocol-specific state machines in their owning schemas. |
| Ontology admission, ref resolution, validation, packing, and source-conformance receipts | `core/rocs-cli` | ROCS implements the operational contract; it does not own the meanings or establish adoption/currentness. |
| Reusable prompts/procedures | Prompt Vault | Engineering-core docs should not become prompt registry truth. |
| Harness instruction selection and hierarchical repository guidance | Pi plus repo-local `AGENTS.md` hierarchy | Engineering-core does not flatten or replace harness-selected instructions. |

See `docs/evidence-semantics-boundaries.md` for the end-to-end integration contract.

## Short form

```text
engineering-core owns shared lane/discipline guidance and its portable engineering protocols.
Repo docs own local deviations and selected subsets.
Scope owners own generated adoption snapshots and rollout dashboards.
governance-kernel owns validation policy source.
Templates own generated defaults and propagation behavior.
agent-kernel owns runtime task/evidence/receipt/decision persistence.
ontology-kernel owns shared semantic definitions.
rocs-cli validates and resolves ontology material without owning its meaning.
Pi and repo-local AGENTS.md own hierarchical harness instructions.
```

## Placement rules

Put a change in engineering-core when it:

- applies across more than one repo or package family;
- describes a reusable engineering invariant or ecosystem default;
- is stable enough to version and distribute;
- can be consumed by repo-local overrides without knowing one repo's private context;
- implements a bounded engineering-specific protocol or generic scanner mechanic without company-specific rollout assumptions.

Keep a change repo-local when it:

- depends on one product's architecture, migration state, dependencies, or operator workflow;
- names repo-specific commands, paths, exceptions, or evidence gates;
- documents a temporary deviation from shared guidance;
- would make shared guidance noisy or false for other repos;
- is a generated scan result, dashboard, wave plan, or scope-specific adoption interpretation.

Put a change in templates when it:

- changes what new repos/packages are generated with;
- changes validation of generated defaults;
- changes propagation mechanics or fixture expectations.

Escalate a change when its primary question is outside guidance ownership:

- to governance-kernel for policy authority and validation-tier legality;
- to agent-kernel for runtime task, evidence, receipt, decision, artifact, or lineage truth;
- to ontology-kernel for canonical shared meaning, aliases, relations, or term deprecation;
- to rocs-cli for ontology source admission, resolution, validation, packing, or conformance mechanics;
- to the Pi/repository instruction owners for hierarchical `AGENTS.md` behavior.
