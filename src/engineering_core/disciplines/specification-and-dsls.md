---
summary: "Discipline for finding implicit engineering DSLs and deciding when to formalize them."
read_when:
  - "A repo has conventions, schemas, naming rules, generated files, policy files, or command surfaces that agents/operators must follow."
  - "A hidden convention repeatedly causes review comments, onboarding tax, drift, or silent failures."
  - "Deciding whether a convention should become documentation, schema, linter, generator, parser, or executable policy."
type: "reference"
---

# Discipline — Specification and DSLs

## Purpose

Engineering work always creates languages. Some are explicit: schemas, CLIs, type systems, grammars, policy files. Others are hidden: naming conventions, folder shapes, generated-file rituals, review phrases, command target vocabularies, and “everybody knows” patterns.

This discipline makes those languages visible and chooses the lightest truthful formalization.

## Owner boundary

Engineering-core owns the engineering discipline:

- where implicit DSLs appear in repos;
- how to classify their risk;
- when to formalize them;
- which engineering artifact should carry the formalization.

Prompt Vault owns reusable cognitive procedures such as:

- `implicit-explicit`
- `formalization-threshold`
- `many-of-the-greats`

Use those prompts when deeper reasoning is needed. Do not copy prompt bodies into engineering-core as runtime authority.

## Load when

- Naming carries meaning beyond readability.
- Directory layout implies behavior.
- Config has conditional semantics.
- Generated files or projections must not be hand-edited.
- A command surface has standardized target names.
- A policy file decides allowed behavior.
- Review keeps catching the same convention violation.
- Agents need tribal knowledge to make safe changes.
- A natural-language instruction is acting like executable intent.

## DSL classes

| Class | Description | Examples | Default handling |
|---|---|---|---|
| implicit | invisible until violated | “frontend state belongs in XState when complex” | audit and name it |
| convention | documented/socially enforced | `just check` means fast validation | document and test lightly |
| typed | represented in types/interfaces | discriminated unions, enum states | keep type source authoritative |
| schema | machine-validated shape | JSON Schema, Cue, Pydantic, Zod | validate in CI/check |
| generated | source produces projection | catalog, docs, policy exports | regenerate + drift check |
| executable | tool enforces behavior | linter, parser, generator, policy check | make command canonical |

## Audit questions

For each suspected DSL:

1. What domain does it constrain?
2. Who must understand it to participate safely?
3. What happens when it is violated?
4. Is violation detectable without human review?
5. Is the language stable or still changing?
6. Would a schema, type, linter, generator, parser, or executable check reduce damage?

## Formalization threshold

Score each candidate 0-2:

| Factor | Question |
|---|---|
| repetition | How often must people apply it? |
| damage | How bad is failure when someone gets it wrong? |
| detection cost | How hard is violation to catch without human review? |
| onboarding tax | How much tribal knowledge is required? |
| tooling leverage | How much would schema/tooling help? |
| volatility | How stable is the language? High volatility lowers full-formalization confidence. |

Interpretation:

- `0-4`: keep implicit or clarify locally.
- `5-7`: keep as explicit convention.
- `8-12`: formalize now.

Override:

- If violations are costly, silent, and tooling can prevent them, formalize even if the total is borderline.
- If the language is still changing quickly, document a convention first and defer heavier tooling.

## Formalization ladder

Choose the lightest artifact that prevents the real failure:

1. glossary or naming note
2. README/AGENTS/engineering.local convention
3. decision record or architecture note
4. type/interface/enum
5. schema/config contract
6. lint/check script
7. generator/projection with drift check
8. parser/interpreter
9. executable policy/gate

Do not jump to parsers and generators when a naming contract would solve the problem. Do not leave costly silent failures as prose when a check can prevent them.

## Cross-language mapping

- TypeScript: discriminated unions, Zod/JSON Schema, typed config, package scripts, Biome/custom checks.
- Python: dataclasses, Pydantic, TypedDict, pyproject config, Ruff/custom checks.
- Go: typed structs, enums via constants, validation functions, `go generate`, schema checks.
- Rust: enums, traits, serde schemas, build scripts, clippy/custom tests.
- C++: enum classes, typed config structs, CMake presets, generated headers, compile-time checks.
- Elixir: Ecto changesets, NimbleOptions, behaviours, Mix tasks, config schemas.

## Common engineering DSLs

- lane IDs and addendum IDs
- discipline IDs
- `Justfile` target vocabulary
- validation tier names
- repo layout conventions
- generated/projection file conventions
- policy file schemas
- environment variable names
- route names and event names
- state-machine event names
- migration names
- evidence artifact names

## Validation

A formalized DSL should have at least one of:

- docs strict check
- schema validation
- typecheck
- generator check mode
- lint/check command
- focused regression tests
- CI gate for drift

## Failure modes

- hidden convention becomes agent trap
- schema exists but docs say something else
- generated projection is hand-edited as truth
- naming convention carries semantics no one documented
- generator has write mode but no check mode
- full formalization freezes a language that is still evolving
- prompt procedure gets treated as engineering authority instead of reasoning support
