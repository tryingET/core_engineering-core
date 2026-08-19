# Security policy

## Supported versions

Security fixes are prepared for the latest stable GitHub Release and the current `main` branch. Pre-1.0 releases do not receive a guaranteed long-term support window; older releases may require upgrading to receive a fix.

The currently validated runtime surface is the Python CLI and packaged data on Python 3.10 through 3.13. Consumer repositories, model providers, and commands named by consumer policy remain outside this project's runtime authority.

## Reporting a vulnerability

Use GitHub's private vulnerability-reporting flow from the repository **Security** tab when it is available. Include:

- affected version or commit;
- attack prerequisites and trust boundary;
- minimal reproduction or proof of concept;
- expected and observed behavior;
- impact, including data or credential exposure;
- suggested mitigation, if known.

Do not publish exploit details, secrets, private repository content, or vulnerable consumer data in a public issue. If private reporting is unavailable, open a minimal issue titled `Security contact requested` without technical details so the maintainer can establish a private channel.

Reports are handled on a best-effort basis; no response or remediation service-level agreement is currently offered. The maintainer should acknowledge receipt privately, confirm scope, coordinate a fix and release, and agree on disclosure timing with the reporter.

## Security-sensitive areas

Changes deserve explicit adversarial review when they affect:

- reading untrusted repository paths, symlinks, FIFOs, or oversized files;
- redaction and bounded advisory payloads;
- JSON/schema validation and authority labels;
- patch-path or evidence-digest validation;
- subprocess or Git invocation;
- GitHub Actions permissions, tags, releases, and artifacts;
- dependency or action version selection;
- generated files that could be mistaken for current compliance or health evidence.

A successful static diagnostic, test run, or artifact attestation is evidence about a defined property; it is not a general claim that the software or a consumer repository is secure.
