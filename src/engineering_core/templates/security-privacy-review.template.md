---
summary: "Template for security and privacy review of repo changes."
read_when:
  - "A change touches secrets, permissions, user data, telemetry, native/device access, or risky dependencies."
type: "template"
---

# Security and Privacy Review

Repo: `<repo/path>`
Change: `<summary>`

## Trigger

- [ ] secrets/config
- [ ] user data
- [ ] sensitive user data / health-adjacent data
- [ ] camera/microphone/location/device permission
- [ ] telemetry/logging/analytics
- [ ] native code or install/build scripts
- [ ] auth/session/crypto/network boundary
- [ ] new dependency with elevated risk

## Data and permission posture

- Data collected/stored: `<none or list>`
- Data class: `<public/internal/user/sensitive/secret>`
- Permission requested: `<none or list>`
- Consent/recovery path: `<policy>`
- Retention/delete/export: `<policy>`

## Dependency/supply-chain posture

- New dependencies: `<none or list>`
- Runtime/build/dev classification: `<classification>`
- License/maintenance reviewed: `<yes/no>`
- Native/postinstall/network risk: `<yes/no>`
- Rollback/removal path: `<path>`

## Telemetry/logging posture

- Secrets redacted: `<yes/no>`
- User payloads minimized/redacted: `<yes/no>`
- Sensitive local paths excluded: `<yes/no>`

## Decision

- Accepted: `<yes/no>`
- Conditions: `<none or list>`
- Evidence command/artifact: `<command/path>`
