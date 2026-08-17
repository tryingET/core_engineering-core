---
summary: "Status, use, and promotion rules for the opt-in TypeScript quality pilots."
read_when:
  - "Evaluating Ultracite or anti-slop-inspired evidence rules for TypeScript."
type: "reference"
---

# TypeScript quality pilots

No measured pilot result is recorded in engineering-core yet, so this change does not replace the TypeScript lane's existing default. It adds opt-in, machine-readable pilot surfaces for gathering comparable evidence.

Use:

```bash
engineering-core show ts-ultracite-pilot
engineering-core show ts-evidence-safety
engineering-core show-template typescript-quality-pilot
engineering-core recommend typescript-quality-pilot
engineering-core recommend typescript-high-assurance
```

The stable catalog and the pilot overlay are intentionally separate. A pilot entry may be selected by a repository, but promotion into the stable catalog requires representative evidence, a reviewed default-scope decision, migration/rollback guidance, and removal of the pilot status in a later change.

The Ultracite pilot measures productized setup, diagnosis, presets, runtime, diagnostics, and migration cost. The evidence-safety pilot measures a narrow high-signal rule subset and keeps architecture-dependent or naming opinions conditional. Neither pilot should be enabled fleet-wide solely because an upstream project is popular or fast.
