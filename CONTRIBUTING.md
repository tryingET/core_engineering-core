# Contributing to engineering-core

Thank you for improving the shared engineering lanes, disciplines, templates, catalog, scanner semantics, or CLI.

## Before proposing a change

First identify the authority level of the change:

- **Lane**: ecosystem-specific tools, commands, packaging, and runtime conventions.
- **Discipline**: durable cross-language invariants and evidence expectations.
- **Addendum**: conditional guidance for a narrower concern.
- **Repo-local override**: product- or repository-specific truth that should not become shared doctrine.
- **CLI or schema**: deterministic retrieval, planning, scanning, evidence, or work-packet behavior.

Prefer the narrowest authority surface that solves the repeated problem. A useful shared rule should name its audience, trigger, invariant, counterexample, and expected evidence. Do not promote a one-repository preference into doctrine without evidence that it recurs.

## Development setup

The project supports Python 3.10 through 3.13 and uses `uv` for locked environments and builds.

```bash
uv sync --locked
uv run engineering-core --help
```

The runtime package intentionally has no third-party dependencies. Do not add one without documenting the operational benefit, security and maintenance cost, alternatives considered, and removal conditions.

## Making changes

For package-visible catalog or content changes, keep these surfaces synchronized:

1. canonical files under `src/engineering_core/`;
2. root projections such as `catalog.json` and readable lane/discipline/template surfaces;
3. CLI registries and command help where applicable;
4. examples and adoption documentation;
5. tests and package version/release notes when compatibility changes.

Use the repository sync/check commands rather than hand-editing generated projections where a generator exists:

```bash
uv run engineering-core sync --repo-root .
uv run engineering-core sync --check --repo-root .
```

Do not commit `dist/`, virtual environments, caches, host-local paths, credentials, generated adoption dashboards owned by another scope, or evidence that overstates its authority.

## Validation

Run the smallest relevant checks while iterating and the complete required set before requesting review:

```bash
uv sync --locked
uv run python -m unittest discover -s tests -v
uv run python -m engineering_core.self_check --repo-root .
uv run python scripts/check-release-lineage.py --mode ci
uv run python scripts/check-justfile-addenda.py
uv run python scripts/sync-skill-assets.py --check
uv build
```

For release-affecting work, also run:

```bash
uv run python scripts/release-local.py verify
```

Record the commands actually run and their outcomes. Do not mark unrun checks as passing.

## Pull-request expectations

Keep pull requests narrowly scoped and explain:

- the problem and affected users;
- why this authority surface is correct;
- alternatives and counterevidence considered;
- compatibility, migration, and rollback implications;
- generated/projection changes;
- validation evidence;
- whether a semantic version change is required.

Content changes should distinguish normative requirements from recommendations and examples. Claims about tools, platforms, security, performance, or accessibility should include durable evidence or be explicitly qualified.

## Compatibility and release discipline

The command-line interface and versioned JSON protocol identifiers are consumer-facing contracts. Avoid silently changing field meaning, exit-code meaning, defaults, or deterministic ordering. Breaking changes require a migration path and release-note entry.

A pull request should not create a pseudo-release version merely because it is one item in a stack. The integrated release chooses one coherent semantic version after the intended changes are assembled and validated.
