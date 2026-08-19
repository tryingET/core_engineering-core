---
summary: "Repository CI, release, branch-cleanup, and GitHub settings contract for engineering-core."
read_when:
  - "Changing GitHub Actions, merging pull requests, preparing a release, or diagnosing leftover branches."
type: "reference"
---

# Repository automation

## CI

`.github/workflows/ci.yml` runs on pull requests and pushes to `main`. Its aggregate `required` job succeeds only when the Python 3.10–3.13 test matrix, self-checks, release-lineage check, dogfood checks, package build, and installed-wheel smoke tests all succeed.

CI validates code and release state. GitHub branch protection or a repository ruleset must require the `CI / required` check to prevent an administrator or direct push from bypassing that evidence.

## Release

A package version is a release candidate only when all checked version surfaces agree, the newest prior stable tag is an ancestor, the version is not lower than an existing stable tag, and release documentation exists.

`.github/workflows/auto-release.yml` runs only after the `CI` workflow succeeds for a push to `main`. It checks out the triggering workflow's exact commit, confirms that commit is contained in `main`, and performs the complete release proof before creating a tag. When a version tag already exists but its GitHub Release is missing, the workflow builds and publishes from the exact tagged commit rather than from a later `main` checkout. Release assets include the wheel, source distribution, and `SHA256SUMS`.

Manually pushed version tags are independently validated by `.github/workflows/release.yml`. The automatic and manual release workflows share one non-cancelling concurrency group so only one release mutation runs at a time.

## Branch cleanup

`.github/workflows/cleanup-branches.yml` deletes merged `agent/*` and `recovery/*` branches after confirming that their tips are contained in `main` and that no open pull request still uses the branch. This provides deterministic cleanup even when GitHub's repository-level automatic branch deletion option is disabled.

## Required GitHub repository settings

The repository owner should keep these settings enabled:

- protect `main` with a ruleset;
- require pull requests for changes to `main`;
- require `CI / required` before merge;
- require branches to be current before merge;
- require review-conversation resolution;
- block force pushes and deletion of `main`;
- minimize or disable ruleset bypasses;
- optionally enable GitHub's built-in automatic head-branch deletion as a second cleanup layer.

The workflows cannot grant themselves repository-administration permissions, so these settings remain repository-owner controls rather than code-owned automation.
