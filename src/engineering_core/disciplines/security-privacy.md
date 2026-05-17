# Discipline — Security and Privacy

## Purpose

Protect secrets, users, devices, supply chain, and local data across languages and deployment styles.

## Invariants

- No secrets in git.
- Secrets come from declared secret/config surfaces, not hardcoded paths or defaults.
- Permissions are least-privilege and revocable where platform allows.
- User data is minimized, classified, and retained only as long as justified.
- Dependency additions are reviewed for necessity, maintenance, license, and supply-chain risk.
- Sensitive logs and telemetry are redacted by default.
- Destructive operations require confirmation/recovery proportional to risk.

## Data classification

| Class | Examples | Rule |
|---|---|---|
| public | docs, marketing screenshots | safe to publish |
| internal | non-secret config, architecture notes | repo policy controls sharing |
| user data | preferences, workout history, profile data | minimize, export/delete posture |
| sensitive user data | health, biometrics, camera/media-derived data | explicit consent, strict retention |
| secrets | tokens, credentials, private keys | never commit, redact everywhere |

## Decision rules

- Treat camera, microphone, location, biometrics, and health-adjacent data as high-sensitivity even when local.
- Prefer local processing when remote processing is not required.
- Before adding remote sync, define identity, consent, retention, deletion, breach impact, and offline behavior.
- Before adding native/device integration, document permission model and failure mode.
- Before adding a dependency, ask whether platform/native code already solves the problem safely.

## Failure modes

- `.env` committed or copied into examples with real values
- logs include bearer tokens or raw user payloads
- analytics added without consent/retention story
- broad filesystem/device permissions for convenience
- dependencies added for trivial wrappers
- privacy claims stronger than implementation
