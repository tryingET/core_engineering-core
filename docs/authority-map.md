---
summary: "Authority boundaries for engineering-core, repo-local overrides, templates, validation policy, and runtime task truth."
read_when:
  - "Deciding where engineering guidance, validation policy, generated defaults, or repo-local deviations should live."
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
| Reusable adoption scanner semantics | `core/engineering-core scan-adoption` | Structural status taxonomy, catalog-aware lane/discipline validation, generic package/member discovery, and generic JSON/Markdown rendering. |
| Repo/package-local deviations and selected subset | repo-local `docs/engineering.local.md` | Higher priority than shared lane/discipline docs for that repo. Should explain local commands, deviations, and evidence expectations. |
| Machine-readable lane declaration | repo-local `policy/engineering-lane.json` when needed | Useful for generated repos, package validation, and provenance. Do not create it when local docs are enough. |
| Generated adoption snapshots and rollout dashboards | scanned scope owner | Examples: lane/company `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`. These are projections, not core doctrine. |
| Canonical validation-tier policy | `holdingco/governance-kernel` | Engineering-core may reference and summarize validation tiers, but governance-kernel owns the canonical policy source. |
| Generated defaults and propagation behavior | template owner repos | Templates decide what new repos emit. They should reference engineering-core, not fork its doctrine. |
| Runtime tasks, evidence, decisions, and lineage | Agent Kernel / active AK DB | Docs and templates are not task/evidence authority. |
| Reusable prompts/procedures | Prompt Vault | Engineering-core docs should not become prompt registry truth. |
| Ontology / controlled semantics | ROCS / ontology owner repos | Engineering-core can use terms, but ontology owners govern controlled semantics. |

## Short form

```text
engineering-core owns shared lane/discipline guidance and reusable adoption scanner semantics.
Repo docs own local deviations and selected subsets.
Scope owners own generated adoption snapshots and rollout dashboards.
governance-kernel owns validation policy source.
Templates own generated defaults and propagation behavior.
Agent Kernel owns runtime task/evidence/decision truth.
```

## Placement rules

Put a change in engineering-core when it:

- applies across more than one repo or package family;
- describes a reusable engineering invariant or ecosystem default;
- is stable enough to version and distribute;
- can be consumed by repo-local overrides without knowing one repo's private context;
- implements generic adoption scanner mechanics without company-specific rollout assumptions.

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

Escalate to governance-kernel or AK when the change is about policy authority, lifecycle legality, task/evidence truth, or decision records rather than guidance text.
