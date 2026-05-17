---
summary: "Local release workflow for engineering-core version, proof, and git tag authority."
read_when:
  - "Preparing or verifying an engineering-core release."
  - "Deciding whether to tag or publish engineering-core artifacts."
type: "how-to"
---

# Release workflow

`engineering-core` uses a local-first release workflow. The public authority is the git commit plus annotated tag; package artifacts are built locally with `uv build` and are not committed.

## Authority chain

```text
local release prep
  -> version/changelog/release notes
  -> package proof
  -> release commit
  -> annotated git tag
  -> optional downstream pin to tag
```

There is no compatibility alias and no registry publish step in the normal local workflow.

## Plan

```bash
python scripts/release-local.py plan --version <next-version>
```

The plan reports current version, tag presence, dirty-worktree state, and follow-up commands.

## Verify

```bash
python scripts/release-local.py verify --version <next-version>
```

The verifier checks:

- `pyproject.toml`, `src/engineering_core/__init__.py`, and `catalog.json` versions match;
- `CHANGELOG.md` has a section for the version;
- release notes exist under `docs/releases/`;
- CLI compile, Justfile addendum checks, CLI tests, key CLI smoke commands, and `uv build` pass.

## Commit and tag

After verification passes, commit the release metadata and tag from a clean worktree:

```bash
git add CHANGELOG.md uv.lock docs/releases scripts/release-local.py README.md
git commit -m "chore(release): v<next-version>"
python scripts/release-local.py tag --version <next-version> --apply
```

The tag must be annotated and named `v<version>`.

## Artifact policy

`dist/` is generated output. Build it for proof with `uv build`, but do not commit wheels or source distributions unless the release policy changes explicitly.

## Downstream adoption

Downstream consumers should either:

- record `workspace-local-unpinned` while using the local checkout; or
- pin to the release tag once the tag is available.

Breaking-change migration details live in versioned migration maps under `docs/releases/migrations/`.
