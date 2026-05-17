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

## Failure modes

- dependency added for one helper function
- transitive native build surprises CI/users
- package manager lockfile drift
- dev dependency becomes runtime dependency
- unreviewed postinstall/build scripts
- abandoned package becomes critical path
