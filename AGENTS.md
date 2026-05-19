---
summary: "Repo-local guardrails for engineering-core lane, discipline, catalog, template, adoption scanner, and CLI work."
read_when:
  - "Before changing engineering-core lanes, disciplines, templates, catalog, adoption scanner, CLI, or tests."
---

# AGENTS.md — engineering-core

## Scope

`engineering-core` owns shared language lanes, conditional lane addenda, cross-language engineering disciplines, adoption templates, the machine-readable catalog, reusable adoption scanner semantics, and the CLI used to retrieve or audit them.

## Ownership boundaries

- Repo consumers own deviations in `docs/engineering.local.md` and, when useful, `policy/engineering-lane.json`.
- Scope owners own generated adoption snapshots and rollout dashboards, for example `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`.
- Engineering-core owns generic `scan-adoption` mechanics, status taxonomy, catalog-aware lane/discipline validation, and generic rendering.
- Disciplines own cross-language invariants.
- Lanes own ecosystem-specific tooling, command mappings, and package-manager conventions.
- Do not turn lane docs into dumping grounds for cross-language concerns; move recurring invariants into disciplines.
- Do not hardcode company/lane-specific scanner heuristics in core; make scanner behavior portable or configurable.
- Do not recreate legacy `tech-stack-core` console-script or `tech_stack_core` import aliases unless explicitly requested as a migration task.

## Change discipline

When adding or renaming a lane, addendum, discipline, template, profile, or adoption scanner contract, update these together:

1. source docs under `src/engineering_core/`
2. root symlinked/readable docs where applicable (`lanes/`, `disciplines/`, `templates/`)
3. `catalog.json` and `src/engineering_core/catalog.json`
4. CLI constants/commands in `src/engineering_core/cli.py`
5. scanner modules when adoption behavior changes (`src/engineering_core/adoption_scan.py`, `src/engineering_core/adoption_render.py`)
6. README examples, `docs/adoption.md`, and `docs/vision.md` when user-facing behavior changes
7. tests under `tests/`
8. package version when the change is package-visible

## Validation

Run from repo root before handoff:

```bash
python -m py_compile src/engineering_core/cli.py src/engineering_core/adoption_scan.py src/engineering_core/adoption_render.py
python -m unittest discover -s tests
python scripts/check-justfile-addenda.py
uv run engineering-core list
uv run engineering-core catalog --pretty --prefer-repo
uv run engineering-core scan-adoption --scope /home/tryinget/ai-society/core --repo-discovery recursive --include-scope-root --include-packages --format json --prefer-repo
uv build
```

`dist/` is generated proof output from `uv build`; do not commit wheels or source distributions unless release policy changes explicitly.
