---
summary: "Lifecycle rules for adding, splitting, merging, and relocating engineering-core discipline guidance."
read_when:
  - "Adding or changing an engineering-core discipline."
  - "Deciding whether guidance belongs in a lane, discipline, addendum, or repo-local override."
type: "reference"
---

# Discipline lifecycle

Disciplines are cross-language engineering contracts. They should remain portable, versioned, and small enough that agents can choose the relevant subset without loading everything.

## Add a discipline when

Add a new discipline only when all of these are true:

1. The concern crosses multiple language lanes or repo shapes.
2. The concern has durable invariants or decision rules, not just tool recipes.
3. Keeping the concern inside one lane would create duplicated guidance in other lanes.
4. Repo-local overrides alone would hide a shared risk or quality bar.
5. The discipline can name clear load triggers and evidence expectations.

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

After a split:

- update `src/engineering_core/disciplines/README.md`;
- update the CLI discipline list in `src/engineering_core/cli.py`;
- update `catalog.json`;
- update adoption examples in `README.md` or `docs/adoption.md` when affected;
- add or update CLI tests when the public list changes.

## Merge or retire a discipline when

Merge or retire a discipline when it is no longer independently useful:

- its load triggers are indistinguishable from another discipline;
- it only repeats lane guidance;
- it has no current consumers and no clear future consumer;
- it encodes old migration history instead of current guidance.

Retirement is a breaking guidance change. Document the migration path in release notes when consumers may reference the old discipline id.

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

## Review checklist for discipline changes

Before committing a discipline lifecycle change, check:

- Does the change preserve the authority map in `docs/authority-map.md`?
- Is the guidance portable across more than one repo or lane?
- Are load triggers clear enough for agents to avoid over-loading docs?
- Are lane-specific commands kept in lanes rather than disciplines?
- Are repo-specific exceptions kept in repo-local docs?
- If the discipline id/list changed, were CLI constants, `catalog.json`, README, and tests updated?
- Did docs strict pass?

## Validation

Minimum validation for discipline-only documentation changes:

```bash
node /home/tryinget/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs . --strict
python scripts/check-justfile-addenda.py
```

If the public CLI list or packaged files change, also run:

```bash
python -m py_compile src/engineering_core/cli.py
PYTHONPATH=src python -m unittest discover -s tests -v
uv run engineering-core list-disciplines
uv build
```
