---
summary: "Validation evidence for native capability observation and doctor implementation."
read_when:
  - "Reviewing implementation closure for AK decision 51."
type: "evidence"
---

# Capability observation implementation evidence

Controlling decision: AK decision `51`; ADR `docs/adr/2026-07-11-native-capability-observation.md`.

## Results

- `python -m unittest discover -s tests` — 83 tests passed.
- `python scripts/dogfood-capabilities.py` — passed; no consumer commands/models/mutations; CLI exits and path probes verified.
- Repeated capability dogfood output was byte-identical: SHA-256 `4c292885d3fc6537d940c6e5225ec2bb8fef1b189a476bc0ecac7e4629b6afa3`.
- `python scripts/dogfood-closed-loop.py` — passed.
- Repeated closed-loop dogfood output was byte-identical: SHA-256 `07904d58982e879d723a87fc1081fe06a00fefcbd89699a86d0556381f55b2f6`.
- `python scripts/release-local.py verify --version 0.6.0` — passed.
- Strict docs validation — passed for 80 documents.
- `git diff --check` — passed.
- All touched code files remain at or below 500 LOC.
- `uv build` produced and the verifier inspected the v0.6.0 wheel and sdist, including capability modules and both dogfood harnesses.

## Dogfood posture

The engineering-core owner repo reports `degraded` under doctor because it intentionally has no consumer capability declaration. This is truthful: product implementation is not consumer adoption. Temporary fixtures prove valid, absent, malformed, unsupported, mismatched-pin, and mismatched-catalog states.

## Authority boundary

No consumer repository, policy, receipt, patch, AK task, external model, CI/release authority, or society rollout state was mutated by doctor/capability dogfood. The AK decision record was updated separately as lifecycle authority.
