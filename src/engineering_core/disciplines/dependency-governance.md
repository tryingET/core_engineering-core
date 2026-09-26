---
summary: "Cross-language dependency addition, pinning, review, upgrade, and removal discipline."
read_when:
  - "Adding, upgrading, replacing, or removing dependencies or toolchains."
  - "Reviewing dependency risk, reproducibility, provenance, or cleanup posture."
type: "guide"
---

# Discipline — Dependency Governance

## Purpose

Keep dependencies deliberate, reproducible, reviewable, and removable.

## Invariants

- Every dependency has a job.
- Lockfiles are committed where the ecosystem uses them.
- CI/release installs are deterministic.
- Generated/vendor/build-output paths are excluded from quality tools intentionally.
- Dependencies that touch secrets, networking, native code, telemetry, crypto, auth, parsing, or build execution receive higher scrutiny.

## Add-dependency checklist

- What problem does this solve?
- Is it runtime, dev, test, build, or optional?
- Is platform/native functionality enough?
- Is the package maintained?
- Does license fit the repo?
- Does it add native install/build risk?
- Does it execute code at install/build time?
- What is the removal/rollback path?
- What validation proves integration?

## Versioning rules

- Prefer exact/pinned/toolchain-governed versions for reproducibility.
- Use ecosystem-native freshness/risk gates where available.
- Review major upgrades as behavior changes, not chores.
- Remove unused dependencies promptly.

## Release-age quarantine and your own packages

A release-age quarantine (uv `exclude-newer`, Bun `minimumReleaseAge`, npm `min-release-age`) delays third-party releases so a compromised upload can be caught before you install it. Your own work should get a green light, but only by verified ownership:

- Quarantines apply to registry uploads only. Anything consumed by git or path pin (a commit SHA, a local path source) is never quarantined, so pinning your own repos by commit is a green light by construction.
- Exempt a registry package only after you've verified that you publish it: an npm scope registered to you (`@your-scope/*`), or on PyPI and crates.io, which have no namespaces, each exact package name whose publisher and project links are yours. Exemptions are keyed to verified ownership, never by a local project name: a local project can share its name with someone else's registry package, and exempting that name lets the stranger's releases skip the quarantine.
- If a local project's name belongs to someone else on a public registry, rename the distribution (the import package and command name can stay). Otherwise anything that resolves the name from the registry installs the stranger's code: dependency confusion, with or without a quarantine. Build backends that infer the package directory from the distribution name (Hatchling, uv_build) then need it declared explicitly.
- An exemption covers only your package. If your fresh release requires a fresh third-party release, that dependency still waits out the quarantine, and the install fails loudly until it clears.
- Declare the quarantine and its exemptions where the lockfile sees them (project config, not only a user-level file), or the lock depends on the machine that wrote it.

## Failure modes

- dependency added for one helper function
- transitive native build surprises CI/users
- package manager lockfile drift
- dev dependency becomes runtime dependency
- unreviewed postinstall/build scripts
- abandoned package becomes critical path
- a quarantine exemption keyed to a local project name lets someone else's same-named registry package through
- a local project shares its distribution name with an unrelated registry package (dependency confusion)
