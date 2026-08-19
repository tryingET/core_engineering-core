---
summary: "Repository CI, local-first and PR-assisted workflows, release, branch-cleanup, and GitHub settings contract for engineering-core."
read_when:
  - "Changing GitHub Actions, pushing to main, using a pull request, preparing a release, or diagnosing leftover branches."
type: "reference"
---

# Repository automation

## Maintainer workflows

The repository supports two maintainer workflows. Neither changes the release proof.

### Local-first direct push

Routine, isolated, and reversible work may be developed and validated locally, then pushed directly to `main`. Run the relevant checks before pushing; run `uv run python scripts/release-local.py verify` for release-affecting changes.

A direct push can leave `main` temporarily red when GitHub CI finds something missed locally. Fix forward or revert promptly. Automatic release remains blocked because it starts only after the complete `CI` workflow succeeds for that exact push.

### Branch and pull request

Use a branch or pull request when it materially improves safety or clarity, especially for external contributions, release automation, security boundaries, versioned schemas or CLI compatibility, broad doctrine changes, large generated diffs, or an AI-assisted patch whose effects are not yet easy to inspect.

A pull request is a structured review and CI surface, not a mandatory ceremony for routine maintainer work.

## CI

`.github/workflows/ci.yml` runs on pull requests and pushes to `main`. Its aggregate `required` job succeeds only when the Python 3.10–3.13 test matrix, self-checks, release-lineage check, dogfood checks, package build, and installed-wheel smoke tests all succeed.

On a pull request, `CI / required` is pre-merge evidence. On a direct push, it is post-push evidence and the gate that prevents an unvalidated commit from being released. Local validation reduces the chance of a red `main`; GitHub CI remains the independent release gate.

## Release

A package version is a release candidate only when all checked version surfaces agree, the newest prior stable tag is an ancestor, the version is not lower than an existing stable tag, and release documentation exists.

`.github/workflows/auto-release.yml` runs only after the `CI` workflow succeeds for a push to `main`. It checks out the triggering workflow's exact commit, confirms that commit is contained in `main`, and performs the complete release proof before creating a tag. When a version tag already exists but its GitHub Release is missing, the workflow builds and publishes from the exact tagged commit rather than from a later `main` checkout. Release assets include the wheel, source distribution, and `SHA256SUMS`.

Manually pushed version tags are independently validated by `.github/workflows/release.yml`. The automatic and manual release workflows share one non-cancelling concurrency group so only one release mutation runs at a time.

## Branch cleanup

`.github/workflows/cleanup-branches.yml` deletes merged `agent/*` and `recovery/*` branches after confirming that their tips are contained in `main` and that no open pull request still uses the branch. This provides deterministic cleanup even when GitHub's repository-level automatic branch deletion option is disabled.

## Suggested GitHub settings for a solo, local-first maintainer

Keep the repository controls aligned with the actual workflow:

- protect `main` against force pushes and deletion;
- keep default GitHub Actions token permissions restricted, granting write access only in the release and cleanup workflows that need it;
- optionally enable GitHub's automatic merged-head-branch deletion as a second cleanup layer;
- do not require pull requests, human approvals, or required pre-update checks on `main` while direct pushes are the normal maintainer path;
- when using a pull request, treat `CI / required` as the merge criterion and resolve material review conversations before merge;
- if the project later becomes branch-first or gains additional maintainers, tighten the ruleset to require pull requests, current branches, and `CI / required` before merge.

The compensating controls for direct pushes are deterministic local validation, small reversible changes, CI on every `main` push, and release automation that cannot run before that CI succeeds. Repository-administration settings remain owner controls rather than code-owned automation.
