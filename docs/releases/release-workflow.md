---
summary: "Validated engineering-core version, tag, artifact, and GitHub Release workflow."
read_when:
  - "Preparing or verifying an engineering-core release."
  - "Changing version consistency, tag ancestry, release artifacts, or GitHub release automation."
type: "how-to"
---

# Release workflow

`engineering-core` treats the commit on `main`, its annotated semantic-version tag, and its GitHub Release artifacts as one release unit. The version may never move below an existing stable tag, and every release candidate must contain the newest prior stable release in its Git ancestry.

## Authority chain

```text
version + changelog + release notes
  -> CI and release-lineage proof
  -> reviewed merge to main
  -> repeated release proof
  -> annotated v<version> tag
  -> GitHub Release with wheel and sdist
  -> optional downstream pin to tag
```

No package registry is currently authoritative. GitHub Release artifacts are generated proof outputs and are not committed.

## Prepare and plan

Choose one coherent version for the integrated release. A PR stack does not receive a separate release number for every layer.

```bash
uv run python scripts/check-release-lineage.py --mode ci
uv run python scripts/release-local.py plan --version <next-version>
```

The lineage check verifies that all package/catalog/lock surfaces agree, the version is not older than an existing stable tag, the newest prior stable tag is an ancestor, its catalog-history snapshot is exact, and the new changelog/release notes exist.

## Verify

```bash
uv run python scripts/release-local.py verify --version <next-version>
```

The verifier checks:

- package, lock, stable catalog, packaged catalog, and import versions;
- stable-tag ancestry and semantic-version monotonicity;
- changelog and versioned release notes;
- historical catalog snapshots against their actual tags;
- Python compilation, the full unittest suite, addendum and agent-skill projections;
- closed-loop, capability, evidence-reconciliation, and owner-use dogfoods;
- catalog, doctor, scan, reconciliation, owner-use, lane, and discipline CLI surfaces;
- wheel and source-distribution contents.

## Automated tag and GitHub Release

After a validated new version lands on `main`, `.github/workflows/auto-release.yml` repeats the release proof. When the corresponding tag is absent, it creates and pushes an annotated tag and then creates a GitHub Release containing the wheel and source distribution.

A manually pushed `v*.*.*` tag is handled by `.github/workflows/release.yml`, which independently verifies that:

- the tag matches the package version;
- the tag points to the checked-out commit;
- the tagged commit is contained in `origin/main`;
- the full release proof and artifact inspection pass.

## Local tag fallback

The local tag command remains available for an owner-controlled fallback after a clean verification:

```bash
uv run python scripts/release-local.py tag --version <next-version> --apply
```

Push the annotated tag explicitly. The tag-triggered workflow will validate it before creating a GitHub Release.

## Artifact policy

`dist/` is generated output. Build it for proof with `uv build`, but do not commit wheels or source distributions. Canonical policy: `docs/releases/artifact-policy.md`.

## Downstream adoption

Downstream consumers should either:

- record `workspace-local-unpinned` while using the local checkout; or
- pin to the release tag once the GitHub Release is available.

Breaking-change migration details live in versioned migration maps under `docs/releases/migrations/`.
