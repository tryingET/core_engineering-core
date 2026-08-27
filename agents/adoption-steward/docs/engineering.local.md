---
summary: "Repository-local engineering-core selections, commands, and deviations."
read_when:
  - "Before changing repository engineering conventions or validation commands."
type: "policy"
---

<!-- engineering-core-managed:v1 -->

# Repository engineering contract

## Selected lanes and addenda

- No language lane is selected deliberately (`lane_status: no_language_lane`): this repository ships persona docs, prompts, and governance, not language-specific software.

## Selected disciplines

- `validation`
- `security-privacy`
- `documentation`

## Canonical local commands

- Catalog: `engineering-core catalog --pretty`
- List disciplines: `engineering-core list-disciplines`
- List templates: `engineering-core list-templates`
- Diagnose adoption: `engineering-core doctor --repo .`
- Repo validation: `./scripts/ci/smoke.sh` and `./scripts/ci/full.sh`

## Validation evidence before handoff

Run the repository-local check/test/build commands selected by the applicable lane and validation discipline, then report the commands and outcomes.

## Deliberate deviations

- None recorded. Add structured entries under `engineering_core.deviations` in `<repo>/policy/engineering-lane.json`.
