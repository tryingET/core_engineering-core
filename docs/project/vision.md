---
summary: "Durable vision for engineering-core as AI Society's shared, evidence-bounded engineering guidance and adoption substrate."
read_when:
  - "Aligning engineering-core strategy, product boundaries, adoption mechanics, or shared-content evolution."
  - "Checking whether proposed work serves the durable product direction."
type: "reference"
---

# Vision

## Purpose

Engineering-core makes shared engineering judgment easy to find, adopt, inspect, and improve without copying doctrine into every repository or centralizing authority over local engineering work.

It is a versioned, portable substrate of language lanes, conditional addenda, cross-language disciplines, templates, recommendation profiles, catalog metadata, and deterministic CLI protocols. Repository owners choose what applies, preserve local deviations, and retain authority over commands, validation, rollout, and evidence.

## Product promise

The intended operator experience is:

1. pin an immutable engineering-core release or commit;
2. retrieve only the guidance relevant to a repository and concern;
3. initialize or migrate adoption through an inspectable, dry-run-first plan;
4. review the selected lanes, disciplines, profiles, dependencies, and repo-local deviations;
5. obtain deterministic explanations and static diagnostics without executing consumer commands;
6. inspect adoption and capability posture across an explicitly supplied repository population;
7. optionally exchange bounded, provider-neutral advice and owner-produced evidence artifacts;
8. route decisions, execution, evidence, exceptions, and rollout actions to their owning repository or authority surface.

A fresh operator should be able to understand both what engineering-core recommends and what it explicitly does **not** prove or control.

## North star

```text
shared engineering doctrine
  -> explicit repo-local adoption and deviation
    -> deterministic explanation and visibility
      -> owner-controlled execution and evidence
        -> reviewed, reversible doctrine evolution
```

Engineering-core succeeds when shared engineering knowledge becomes easier to apply consistently while local ownership, uncertainty, and authority boundaries become more visible—not less.

## Durable outcomes

1. **One inspectable shared core.** Reusable guidance is versioned once and retrieved selectively instead of copied across prompts, templates, companies, and repositories.
2. **Explicit local truth.** Each consumer can state its selected subset, commands, deviations, release pin, and evidence expectations in repo-owned surfaces.
3. **Deterministic adoption.** Planning, explanation, initialization, migration, scanning, and diagnostics have stable machine-readable contracts and safe defaults.
4. **Evidence-bounded improvement.** Proposals, pilots, promotions, deprecations, and retirements remain reviewable, reversible, and connected to representative evidence and counterevidence.
5. **Federated visibility without central control.** Scope owners can inspect adoption and gaps across explicit populations while retaining ownership of dashboards, remediation, and rollout decisions.
6. **Truthful integration.** Advice, receipts, and work packets preserve provenance and authority ceilings instead of converting supplied claims into execution, CI, release, compliance, or governance truth.

## Product model

Engineering-core combines four complementary surfaces:

- **Guidance:** lanes, addenda, disciplines, templates, and recommendation profiles.
- **Catalog and protocols:** stable identifiers, dependencies, schemas, explanations, and compatibility rules.
- **Adoption mechanics:** dry-run initialization and migration, structural scans, capability diagnostics, baselines, and warning-first ratchets.
- **Owner-use membranes:** bounded planning, advice validation, receipts, dispositions, work packets, and reconciliation that remain inert until an owner acts through the proper authority surface.

These surfaces should reinforce one another while remaining independently understandable and replaceable.

## Recipient-owned learning and skill quality

The intended improvement loop connects permitted KES/source evidence to causal
attribution, the strongest bounded intervention, fixed baseline/regression evidence,
independent review, recipient acceptance, observed discovery/use, and reversible
contradiction handling. Repo skills serve qualified recurrent workflows; they are
not a mandatory universal policy layer. Deterministic requirements belong in code
or validators rather than accumulated instructions. Methodology remains with the
skill-engineering source owner; engineering-core supplies adoption guidance and
existing inert engineering membranes, not a competing learning or status database.

This supports the larger foundry and LeseOS/MathOS ambition without making a grand
foundry a prerequisite for useful repo-skill quality work or reducing that ambition
to a disposable linear MVP. Source meaning, reader intent, critique, application
proposals, review and accepted knowledge must remain distinct. Learning may inform
another owner by reviewed reference; template generation does not carry approval,
access or automatic activation. Source promotion, recipient adoption and measured
use require separate evidence, including the ability to decline and withdraw.

See [adoption](../adoption.md#opt-in-repo-skills-and-kes-improvement) and
[owner handoffs](../authority-map.md#repo-skill-and-learning-handoffs) for the bounded
reconciliation. They specify an intended composition, not a shipped automatic loop.

## Hard scope boundaries

Engineering-core must not:

- become a second runtime task, decision, evidence, exception, or compliance authority beside repository owners and Agent Kernel;
- execute consumer validation commands or apply proposed patches by default;
- embed a model provider, credentials, or a hosted control plane as a requirement for core use;
- invent a society-wide repository denominator or hardcode company-specific rollout policy;
- absorb generated fleet dashboards, repo-local exceptions, or adoption queues from their owning scopes;
- own canonical cross-system semantics that belong in ontology-kernel and ROCS;
- become a prompt registry, orchestration harness, or replacement for repo-local `AGENTS.md` loading;
- promote popular tooling, telemetry, model output, or repeated prose into stable doctrine without owner review, compatibility analysis, and falsifiable evidence.

## Design principles

- Keep shared guidance portable across languages, repository shapes, organizations, and harnesses.
- Keep repository-specific commands, architecture, exceptions, and landing policy repo-local.
- Prefer deterministic, bounded, offline-capable behavior for core inspection and planning paths.
- Default to read-only output; make every mutation or external effect explicit and owner-controlled.
- Separate static compatibility, observed execution, supplied evidence, and authority-bearing decisions.
- Preserve stable IDs and schema meaning; introduce explicit migrations for incompatible changes.
- Keep pilots visibly separate from stable defaults and require evidence-backed promotion or retirement.
- Prefer warnings, baselines, and ratchets before broad hard gates.
- Make uncertainty, omissions, counterevidence, and unsupported claims visible.
- Keep generated adoption outputs in the scope being scanned.
- Optimize for selective retrieval and low cognitive overhead rather than maximal doctrine volume.

## Success tests

The vision is being realized when:

- a new repository can adopt an immutable release without hidden workspace knowledge;
- a maintainer can explain why each selected item applies and where local policy overrides it;
- a scope owner can inspect a bounded repository population and distinguish adopted, partial, invalid, legacy, pilot, and unknown states;
- advisory and evidence workflows fail closed on provenance or binding drift and never self-authorize execution;
- representative consumer evidence can revise, split, deprecate, or retire shared guidance without erasing history;
- release artifacts, catalogs, docs, and compatibility records tell the same story;
- consumers can decline or remove engineering-core without losing their repository's runtime authority or operational truth.

## Authority and freshness

This document states durable intent, not shipped status or an execution queue. Current maturity and the evidence-gated semver v1.0 target are described in `docs/project/product_posture.md`. Current behavior is established by source, tests, the README, support policy, release records, and published artifacts. Live direction, tasks, decisions, and evidence are authoritative only when represented in Agent Kernel or another explicitly owning runtime surface.
