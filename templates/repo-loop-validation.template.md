---
summary: "Template defining a repo-local loop validation command contract for agent/orchestration loops."
read_when:
  - "A repo wants slash-command, visible-loop, nexus-loop, or agent-loop validation guidance."
  - "Mapping repo-local validation commands to generic loop phases."
type: "template"
---

# Repo Loop Validation Contract v1

Repo: `<repo/path>`
Owner surface: `docs/engineering.local.md` or the repo's workflow doc

## Purpose

Expose repo-local validation phases that orchestration prompts can ask for without becoming a validation or authority system.

Loop commands produce evidence for an agent/operator handoff. They do not replace AK task scope, repo decisions, CI, release approval, or production activation authority.

## Commands

| Command | Required behavior | Failure posture | Maps to |
|---|---|---|---|
| `loop-doctor` | Non-failing diagnostic for environment, dirty tree, task scope, and obvious blockers. | Always exits successfully; reports blockers in output. | `<repo command>` |
| `loop-verify-fast` | Focused inner-loop validation for the current slice. | Fails when the slice is not locally valid. | `<repo command>` |
| `loop-impact-plan` | Classify changed-file risk and name the checks that should run. | Fails only for invalid inputs/tooling; wide risk is a reported plan result. | `<repo command>` |
| `loop-impact-run` | Run bounded or expanded impact checks selected by the plan. | Fails on check failure or refused wide scope. | `<repo command>` |
| `loop-impact-wide` | Explicitly accepted wide validation when the plan says broad/full checks are needed. | Fails on check failure; caller must state why wide validation is accepted. | `<repo command>` |
| `loop-landing-check` | Repo-declared authoritative landing/readiness gate before handoff, merge, or commit finalization. | Fails closed when repo scope, evidence, or required gates are incomplete. | `<repo command>` |

If a command is intentionally unavailable, document `n/a` and the closest repo-local fallback.

## Machine-readable declaration

When a repo wants `engineering-core scan-adoption` to report loop validation coverage, declare the optional policy block in `policy/engineering-lane.json`:

```json
{
  "engineering_core": {
    "loop_validation": {
      "version": "repo-loop-validation-v1",
      "contract_doc": "docs/engineering.local.md#repo-loop-validation",
      "commands": {
        "loop-doctor": "just loop-doctor",
        "loop-verify-fast": "just loop-verify-fast",
        "loop-impact-plan": "just loop-impact-plan",
        "loop-impact-run": "just loop-impact-run",
        "loop-impact-wide": "just loop-impact-wide",
        "loop-landing-check": "just loop-landing-check"
      }
    }
  }
}
```

Use a value beginning with `n/a:` only when a phase is intentionally unavailable and the fallback/escalation path is documented, for example `"n/a: wide validation is CI-only"`.

## Phase guidance

- Before implementation: run or inspect `loop-doctor` when scope, environment, or task binding may be stale.
- During iteration: use `loop-verify-fast` for the cheapest truthful signal.
- Before claiming done: run `loop-impact-plan`, then `loop-impact-run` or `loop-impact-wide` according to the plan and operator risk acceptance.
- Before landing/handoff: run `loop-landing-check` and record command, scope, result, warnings, and artifact paths.


## Loop command output contract

Loop commands may print human-readable logs, but their handoff evidence should make these fields recoverable from stdout, a receipt, or the final agent report:

- phase command invoked;
- validation scope, such as changed files, selected slice, package, repo, or CI-equivalent;
- result: `passed`, `failed`, `blocked`, `diagnostic`, or `not-run`;
- fallback or escalation used when a loop phase maps to `n/a:` or a closest local equivalent;
- warnings accepted and why;
- artifact or receipt paths when generated;
- authority boundary that remains outside the loop command.

Phase-specific expectations:

- `loop-doctor` is diagnostic even when it exits successfully; do not report it as validation pass.
- `loop-verify-fast` should name the focused slice it covered.
- `loop-impact-plan` should classify impact as bounded, expanded, or wide and name the next command.
- `loop-impact-run` should refuse wide plans unless wide validation was explicitly accepted.
- `loop-impact-wide` should state the acceptance reason for broad validation.
- `loop-landing-check` should name the repo-declared gate it maps to and any remaining AK, CI, release, or governance handoff.

## Authority boundary

- Slash commands and visible-loop/nexus-loop prompts may request these commands by phase.
- The repo owns command semantics, mappings, and landing policy.
- Runtime authority remains with the repo's declared owner surfaces, AK task/decision/evidence where applicable, CI/release systems, and human/governance approvals.
- Do not claim semantic completion, merge approval, production activation, or task closure from loop command success alone.
