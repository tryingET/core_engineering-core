---
summary: "G0-A2 admission freeze: remaining candidate-independent schemas, impact matrix, transition templates, and bound protocol digests. Releases no candidate and no G1-G4 execution."
read_when:
  - "Assessing whether G0-A2 has admitted convergence-implementation or G4-A work."
  - "Changing a frozen protocol, population, compatibility class, or impact-matrix mapping."
type: "implementation-plan"
---

# G0-A2 admission freeze

Controlling contract: RFC R5 / ADR `docs/adr/2026-08-23-v1-convergence-contract.md`.
Record: `docs/project/v1-g0a2-admission.json`.
Harness: `scripts/v1/g0a2_admission.py`.

## What this gate admits

G0-A2 admits **convergence-implementation** tasks and separately owner-accepted
**G4-A pilots**. It does **not** admit a `1.0.0` candidate, G1–G4 outcome capture,
publication, or participant mutation beyond those exact owner tasks.

Already frozen and bound by digest:

- G1–G4 protocol plans and harnesses (tasks 4871–4874)
- Population manifest rev 2 (decision 131) and owner admissions 4931–4935
- G3 prospective protocol (decision 132, dspx task 4936)

Added by this freeze:

- compatibility-manifest schema and candidate-independent surface inventory
- rendered-product schema and inventory method
- transition-template manifest (templates vs future G0-B instances)
- impact matrix (change class → mandatory reruns)
- gate-conformance entrypoint inventory (the four `scripts/v1/*.py` CLIs)

## Still not admitted

- G0-A3 candidate-preparation (needs G4-A live cycles + implementation fan-in)
- G0-B / task 4876 (needs the G0-A3 admission record)
- G1–G4 production and G5 / task 4877
