---
summary: "Lifecycle rules for adding, splitting, merging, and relocating engineering-core discipline guidance."
read_when:
  - "Adding or changing an engineering-core discipline."
  - "Deciding whether guidance belongs in a lane, discipline, addendum, or repo-local override."
type: "reference"
---

# Discipline lifecycle

Disciplines are cross-language engineering contracts. They should remain portable, versioned, and small enough that agents can choose the relevant subset without loading everything.

All substantial discipline proposals also follow `docs/content-lifecycle.md`, including evidence references, counterevidence, falsification conditions, review triggers, and retirement signals. This document adds discipline-specific placement and packaging rules.

## Add a discipline when

Add a new discipline only when all of these are true:

1. The concern crosses multiple language lanes or repo shapes.
2. The concern has durable invariants or decision rules, not just tool recipes.
3. Keeping the concern inside one lane would create duplicated guidance in other lanes.
4. Repo-local overrides alone would hide a shared risk or quality bar.
5. The discipline can name clear load triggers and evidence expectations.
6. A proposal or pilot record identifies the strongest alternative, known exceptions, falsification conditions, review trigger, and retirement signal.

Good discipline candidates:

- security/privacy posture across browser, CLI, service, and local data surfaces;
- accessibility across web UI, docs, TUI, native UI, and custom renderers;
- validation and testing concepts that lanes map into ecosystem-native commands;
- local-first data authority and migration rules across frontend, desktop, and backend code.

Do not add a discipline for one package, one framework preference, one temporary migration, or one tool's setup instructions.

## Split a discipline when

Split an existing discipline when at least one condition is true:

- It has two audiences that are commonly loaded separately.
- It mixes distinct invariants with different evidence gates.
- Agents routinely need only one section and loading the whole doc creates noise.
- One part changes frequently while the other should remain stable.
- The doc starts duplicating lane recipes to stay understandable.
- Evidence repeatedly supports one part while falsifying or narrowing another.

After a split:

- update `src/engineering_core/disciplines/README.md`;
- update the CLI discipline list in `src/engineering_core/cli.py`;
- update `catalog.json` and its package projection;
- update adoption examples in `README.md` or `docs/adoption.md` when affected;
- add or update CLI tests when the public list changes;
- preserve the evidence and migration lineage from the original discipline.

## Merge or retire a discipline when

Merge or retire a discipline when it is no longer independently useful:

- its load triggers are indistinguishable from another discipline;
- it only repeats lane guidance;
- it has no current consumers and no clear future consumer;
- it encodes old migration history instead of current guidance;
- repeated exceptions or counterevidence show that its scope is wrong;
- a replacement expresses the invariant more clearly or with lower adoption cost.

Retirement is a breaking guidance change when consumers reference the discipline ID. Document the replacement or migration path in release notes, and preserve historical evidence rather than rewriting it as current.

## Move lane guidance into a discipline when

Move guidance from a lane into a discipline when the lane text is really stating a cross-language invariant.

Signals:

- the same paragraph appears or wants to appear in multiple lanes;
- the guidance says what must remain true but not how one ecosystem implements it;
- the concern applies to non-code surfaces too, such as docs, CLI/TUI, native UI, generated UI, or operations;
- the evidence expectation is portable even if commands differ.

When moving guidance:

1. Put the invariant and decision rule in the discipline.
2. Keep ecosystem-specific command/tool mapping in the lane.
3. Link or name the discipline from the lane only when it is a normal companion for that lane.
4. Avoid requiring every repo to load the discipline by default.
5. Carry forward evidence references, counterexamples, and review/retirement conditions.

## Keep guidance in a lane when

Keep guidance in a language lane when it is ecosystem-specific:

- package manager and runtime choices;
- compiler/typechecker/linter/test command choices;
- framework defaults for that ecosystem;
- file layout conventions tied to a language or runtime;
- ecosystem-native realization of a discipline invariant.

A lane may point to a discipline but should not copy its whole doctrine.

## Keep guidance repo-local when

Keep guidance in `docs/engineering.local.md` when it depends on a repo's local truth:

- existing migration state or deliberate technical debt;
- local commands and validation gates;
- product-specific architecture or data authority;
- exceptions to shared defaults;
- package-specific dependency choices;
- temporary rollout notes or owner-specific handoff instructions.

Repo-local guidance can select disciplines and explain deviations. It should not redefine shared doctrine for other repos.

## Evidence and semantic references

When live evidence is stored in agent-kernel, reference the stable evidence/receipt/artifact ID and digest instead of copying private payloads into shared guidance. Public contributors may use equivalent digest-bound artifacts; AK is not a required dependency.

Keep discipline-specific states and reason codes in engineering-core. Reference ontology-kernel IDs only when the term already has an accepted cross-system meaning. Use rocs-cli to resolve or validate that ontology material, without treating source conformance as semantic approval.

See `docs/evidence-semantics-boundaries.md`.

## Review checklist for discipline changes

Before committing a discipline lifecycle change, check:

- Does the change preserve the authority map in `docs/authority-map.md`?
- Is the guidance portable across more than one repo or lane?
- Are load triggers clear enough for agents to avoid over-loading docs?
- Are lane-specific commands kept in lanes rather than disciplines?
- Are repo-specific exceptions kept in repo-local docs?
- Are evidence, counterevidence, falsification, review, and retirement conditions explicit?
- Do external evidence references include stable IDs, digests, scope, and authority ceilings?
- Are ontology references accepted IDs rather than invented global meanings?
- If the discipline ID/list changed, were CLI constants, catalogs, README/adoption docs, history, version surfaces, and tests updated?
- Did the repository and harness-selected documentation checks pass?

## Validation

Minimum repository validation for discipline-only documentation changes:

```bash
uv run python -m engineering_core.self_check --repo-root .
uv run python scripts/check-justfile-addenda.py
```

Run any additional documentation task selected by the local Pi/hierarchical `AGENTS.md` harness through that harness. Do not hardcode one workstation's absolute validation-script path into this shared document.

If the public CLI list, catalog, package version, or packaged files change, also run:

```bash
uv run python -m unittest discover -s tests -v
uv run engineering-core list-disciplines
uv run python scripts/check-release-lineage.py --mode ci
uv build
```
