---
summary: "G2 candidate-bound fixture materialization and installed-wheel entrypoint proof against b313bec. Does not claim G2 PASS."
read_when:
  - "Continuing Gate G2 after G0-B candidate freeze."
  - "Checking which G2 cells are materialized vs actually executed."
type: "implementation-plan"
---

# G2 materialization (no PASS)

Candidate: `proof/v1-candidate-2` `b313becf7f1bf5261843d7b29c939b0bc5072ef1`.
Harness: `scripts/v1/g2_materialize.py` (does not edit the frozen G2 template harness).

## This slice

- Bind every frozen fixture class to the candidate SHA (`candidate_binding` no longer `unassigned`)
- Validate each instance with `federated_interoperation.py validate-fixture`
- Fill every entrypoint × threat cell as `materialized` or `not_executed`
- Install the **candidate wheel** into an empty venv and run no-effect public entrypoints
  (`list`, `list-disciplines`, `catalog`, `--help`)

## Explicitly not G2 PASS

Hostile filesystem/Git/TOCTOU/injection cells are materialized with frozen
expected outcomes but **not** executed against the wheel in this slice.
Two-owner identical-aggregate consumption is not run. Do not treat this
record as Gate G2 PASS.
