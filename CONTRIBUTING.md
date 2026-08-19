# Contributing to engineering-core

Thank you for improving the shared engineering lanes, disciplines, templates, catalog, scanner semantics, or CLI.

## Working model

This repository is maintained primarily by a solo builder using a local-first, AI-assisted workflow.

The maintainer may validate locally and push routine changes directly to `main`. Pull requests are optional for maintainer work and are used when they add useful isolation, CI preview, review structure, or rollback clarity. External contributions should use a pull request.

AI-generated material is a draft, not execution evidence or independent review. The person publishing a change remains responsible for inspecting the final diff, checking important assumptions, running the claimed validation, protecting sensitive data, and recording unresolved uncertainty. For a high-risk or hard-to-inspect AI-assisted change, use a separate branch or pull request even when no second human reviewer is available. Its value is a stable comparison surface and an easier revert.

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

The runtime package intentionally has no third-party dependencies. Do not add one without documenting the operational benefit, maintenance cost, alternatives considered, and removal conditions.

## Making changes

For package-visible catalog or content changes, keep these surfaces synchronized:

1. canonical files under `src/engineering_core/`;
2. root projections such as `catalog.json` and readable lane, discipline, and template surfaces;
3. CLI registries and command help where applicable;
4. examples and adoption documentation;
5. tests and package version or release notes when compatibility changes.

Use the repository sync and check commands rather than hand-editing generated projections where a generator exists:

```bash
uv run engineering-core sync --repo-root .
uv run engineering-core sync --check --repo-root .
```

Do not commit `dist/`, virtual environments, caches, host-local paths, generated adoption dashboards owned by another scope, or evidence that overstates its authority.

## Validation

Run the smallest relevant checks while iterating. Before a direct push or pull request that can affect packaged behavior, shared content, compatibility, or release state, run the complete local validation set:

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

For documentation-only or repository-metadata changes, run the relevant syntax and consistency checks; GitHub CI still executes the complete suite after a pull-request update or direct push to `main`.

Record commands actually run and their outcomes when material to review or recovery. Do not mark unrun checks as passing, and do not treat an AI prediction that a check should pass as execution evidence.

## Choosing direct push or pull request

A direct push is appropriate for routine work that is small, understood, locally validated, and easy to revert.

Prefer a branch or pull request for release automation, sensitive trust boundaries, versioned schemas or CLI compatibility, broad doctrine changes, large generated changes, external contributions, and changes whose AI-generated implementation remains difficult to inspect confidently.

A failed CI run on a direct push can temporarily leave `main` red, but automatic release is gated on successful CI for that exact push. Fix forward or revert promptly.

## When using a pull request

Keep it small enough to inspect and revert. Explain the problem, authority surface, alternatives, compatibility and rollback implications, generated changes, validation evidence, remaining uncertainty, and version impact.

Content changes should distinguish normative requirements from recommendations and examples. Claims about tools, platforms, performance, accessibility, or other externally verifiable behavior should include durable evidence or be explicitly qualified.

## Compatibility and release discipline

The command-line interface and versioned JSON protocol identifiers are consumer-facing contracts. Avoid silently changing field meaning, exit-code meaning, defaults, or deterministic ordering. Breaking changes require a migration path and release-note entry.

Do not create a pseudo-release version merely because one change is isolated on a branch or pull request. The integrated release chooses one coherent semantic version after the intended changes are assembled and validated.
