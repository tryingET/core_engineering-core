---
summary: "Policy for engineering-core generated build artifacts and source-controlled release authority."
read_when:
  - "Deciding whether to commit engineering-core dist/ wheels or source distributions."
  - "Preparing, reviewing, or auditing an engineering-core release."
type: "reference"
---

# Artifact policy

`engineering-core` treats packaged files under `dist/` as reproducible proof output, not source-controlled release authority.

## Tracked authority

Track these release inputs and records:

- source files under `src/engineering_core/`
- `pyproject.toml`
- `catalog.json`
- `CHANGELOG.md`
- release notes under `docs/releases/`
- release workflow scripts under `scripts/`
- annotated git tags named `v<version>`

## Untracked/generated output

Do not commit:

- `dist/*.whl`
- `dist/*.tar.gz`
- `build/`
- `*.egg-info/`
- virtual environments or Python cache directories

`uv build` should regenerate distribution artifacts during release verification.

## Policy change gate

Committing distribution artifacts would be a release-policy change, not routine release work. If that becomes necessary, update this document and `docs/releases/release-workflow.md` in the same change and explain why git tags plus regenerated artifacts are no longer sufficient.
