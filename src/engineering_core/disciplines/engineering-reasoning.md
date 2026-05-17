---
summary: "Lightweight router for choosing engineering reasoning modes without turning engineering-core into a prompt library."
read_when:
  - "An engineering task needs a reasoning style such as deduction, abduction, induction, adversarial review, or many-of-the-greats."
  - "A repo-local engineering decision needs to cite a cognitive method without copying prompt templates."
type: "reference"
---

# Discipline — Engineering Reasoning

## Purpose

Engineering-core should name when different reasoning modes are useful. It should not become the canonical store for prompt bodies.

Prompt Vault owns reusable prompt/procedure text. Engineering-core owns the engineering selection rule: which reasoning mode fits which kind of technical situation.

## Owner boundary

| Concern | Owner |
|---|---|
| Reasoning-mode selection for engineering work | engineering-core |
| Reusable prompt/procedure bodies | Prompt Vault |
| Runtime task, decision, evidence, direction truth | Agent Kernel |
| Semantic ontology | ROCS |
| Empirical behavior analysis | Oracle/DSPx |

## Reasoning modes

| Mode | Use when | Engineering example | Prompt Vault support |
|---|---|---|---|
| deduction | rules/specs are fixed and consequences must be derived | Does this implementation violate the schema or lane contract? | procedure/checklist prompts as needed |
| abduction | symptoms exist and the best explanation is needed | Why is CI green locally but failing in release? | diagnostic prompts as needed |
| induction | repeated examples suggest a pattern | What convention emerges across these repos? | synthesis/review prompts as needed |
| adversarial review | failure modes matter more than agreement | What breaks if this package boundary is wrong? | review/crisis prompts as needed |
| many-of-the-greats | first-rate schools of thought disagree | Should frontend state be explicit state machines, framework-local, or server-driven? | `many-of-the-greats` |
| implicit-explicit audit | hidden languages/conventions are suspected | Is `catalog.json` now a DSL requiring schema/checks? | `implicit-explicit` |
| formalization threshold | deciding whether convention deserves tooling | Should Justfile targets become schema-checked? | `formalization-threshold` |
| OODA / iteration | fast sensing-action loops are required | Need repeated observe/orient/decide/act on a failing integration | orchestrator-bound loop prompts where available |

## Selection rules

- Use deduction when the accepted contract is clear.
- Use abduction when evidence is incomplete and explanation quality matters.
- Use induction when multiple cases should produce a reusable pattern.
- Use adversarial review when downside risk, security, migration, or operator confusion matters.
- Use many-of-the-greats when multiple strong architectures or schools can each explain part of reality.
- Use implicit-explicit when conventions are doing hidden work.
- Use formalization-threshold when a hidden/conventional language might deserve schema/tooling.

## Practical rule

Do not paste a large reasoning prompt into engineering docs. Instead:

1. name the reasoning need;
2. retrieve or cite the Prompt Vault template when needed;
3. keep the engineering artifact focused on the resulting decision, contract, or validation rule;
4. record evidence through the repo's normal validation/decision surfaces.

## Failure modes

- using “balanced analysis” when the task requires adjudication
- using deductive checking before the governing contract exists
- using abduction as excuse for speculation without evidence
- formalizing every convention instead of scoring damage and tooling leverage
- copying Prompt Vault procedure bodies into repo docs until they drift
- treating a reasoning mode as runtime authority rather than decision support
