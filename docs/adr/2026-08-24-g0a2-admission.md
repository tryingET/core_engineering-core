---
summary: "Accepted G0-A2 admission: candidate-independent freezes bound; convergence-implementation and G4-A pilots admitted; no 1.0.0 candidate."
read_when:
  - "Deciding whether G0-A2 has passed or whether a candidate may be prepared."
type: "adr"
---

# ADR — Admit G0-A2 (protocol, population, and schema freeze)

## Status

Accepted under decision created with this record. Binding file:
`docs/project/v1-g0a2-admission.json`, validated by `scripts/v1/g0a2_admission.py`.

## Decision

Admit G0-A2. The candidate-independent constitution is frozen: G1–G4
protocols/harnesses, population manifest rev 2 (decision 131), G3 protocol
(decision 132), compatibility and rendered-product schemas, impact matrix, and
transition templates. Candidate commit, candidate digest, and package version
remain `unassigned`.

This admits exact convergence-implementation tasks and owner-accepted G4-A
pilots. It does not admit a release candidate, G1–G4 outcome capture,
publication, or any participant mutation beyond those exact owner tasks.

## Consequences

- Task 4876 (G0-B candidate) stays blocked until a G0-A3 admission record
  exists after G4-A live cycles and implementation fan-in.
- Changing a bound freeze requires a new admission digest and the impact
  matrix's mandatory reruns.

## Rollback

Withdrawing this decision leaves G0-A2 unadmitted. No candidate exists.
