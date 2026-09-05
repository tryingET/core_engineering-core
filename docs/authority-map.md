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
| Skill-authoring and evaluation methodology | `softwareco/contrib/procesio-cli/skills/agent-skill-engineer` | Current source owns the method; engineering-core references it without copying or installing it. |
| Repo skills and recipient adoption | recipient repo maintainers | Qualify workflows, own trigger boundaries, exact accepted revision, integration, local regressions and withdrawal. No universal skill requirement. |
| Learning signals and accepted knowledge | KES/source owners; AK knowledge where landed | Candidate capture is not promotion. Source promotion and recipient acceptance remain separate owner decisions. |
| Skill activation, discovery, loading and use | selected host/runtime owner, including Pi | Files in Git or installation do not prove fresh-host discovery or observed use. |
| Causal/effectiveness analysis | DSPx/Oracle or explicitly designated empirical owner | Independent evaluation and frozen baselines, not author self-grading or acceptance by popularity. |

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

## Repo-skill and learning handoffs

The [adoption reconciliation](adoption.md#opt-in-repo-skills-and-kes-improvement)
composes existing mechanisms. The following are actionable interface requests,
not new assignments, grants of access, or claims that recipients have accepted work.
AK5428 authorizes only the existing-doc design; successors require exact owner scope.

| Receiving owner | Input and requested action | Return evidence / stop boundary |
|---|---|---|
| procesio-cli method owner | Refer to `skills/agent-skill-engineer` version/revision and a sanitized causal defect or method question; review only a genuine method gap. | Source-owned disposition and exact revision. COMPASS-C integrity evidence alone does not justify upstream edits or method installation. |
| COMPASS-C / another opted-in recipient | Supply qualified workflow, source evidence, baseline, bounded proposal and independent review; choose applicability and accepted revision locally. | Owner disposition, native regression evidence, deviations and withdrawal condition. Decline/no skill is valid; no fleet population is inferred from the first consumer. |
| KES source owner and Agent Kernel owner | Bind sanitized source/learning identity, applicability, causal attribution, accepted recipient revision and contradiction references through existing authorized knowledge/evidence surfaces. | Durable owner readback and explicit claim limits. A missing reference/adapter is a scoped design question, not permission for a new DB, automatic promotion or private-memory access. |
| Pi / selected host owner | Given separately accepted recipient revision and authorized target, inspect trust/discovery configuration and design a bounded fresh-context selection/use observation. | Host version/config, exact loaded revision, actual selection/use and negative-route observations; report unknown or absent separately. No provider run, install or activation is authorized by this reconciliation. |
| Empirical owner with recipient/evaluator | Given the intended behavior, preserved baseline successes/failures and development corpus, predeclare independent splits, fixed rubric, A/A noise and paired comparison protocol. | Prospective accepted protocol before execution; subsequent repairs, regressions, costs, uncertainty and failed evidence. Structural audit does not stand in for behavioral proof. |
| Template / template-propagator owner | Review only an explicit recipient population and proposed opt-in source reference/default, including pin, local deviations, refresh and withdrawal behavior. Reuse the owner's current plan/review/propagation mechanics. | Owner dry-run/disposition and per-recipient acceptance if later authorized. Generation or propagation receipts do not prove learning, host activation or use; no blanket template copy. |
| Design traceability owner (AK5425) | Consume source revision/evidence -> causal hypothesis -> bounded intervention -> fixed baseline/evaluation -> review -> recipient accepted revision, with separate host-use and contradiction references. | Preserve source meaning, reader intent, critique, application proposal, review and accepted knowledge as distinct linked claims. Missing/denied source access stays explicit; a traceability record never grants promotion or execution. |

Source promotion, consumer adoption, host activation and measured use are separate
relationships, not a new shared status ladder. Keep agent-personal, society, company,
project, frame, wave and task applicability explicit without automatic access or
inheritance; private human memory remains separate. Template generation is not
learning propagation. Missing interfaces return to their source owner by reference.

AK3351 is a historical parked SF13 gate scoped to explorer artifacts, not current
repo-skill/fleet authority. This reconciliation neither revives that chain nor
bypasses the separately deferred FCOS coordination intake (AK5420).
