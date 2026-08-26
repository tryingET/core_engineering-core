---
name: engineering-core
description: Adopt, diagnose, validate, and scan engineering-core guidance while preserving repository-local authority and unrelated work.
---

# Engineering Core

Use engineering-core as a versioned guidance and adoption-visibility substrate. Do not treat it as the runtime authority for every repository.

## Procedure

1. Read the repository's `AGENTS.md` and any local engineering instructions. Inspect existing work before changing files.
2. Run `engineering-core recommend --repo <repo>` and treat inferred selections as proposals, not facts.
3. Run `engineering-core doctor --repo <repo> --format json` and separate objective failures from warnings and semantic advisories.
4. Run `engineering-core init --repo <repo> ...` without `--apply` first. Review the unified diff and preserve hand-written local policy.
5. Apply only when the task authorizes repository changes. Never add `--force` without reviewing why an unmanaged document would be replaced.
6. For legacy migration, plan first. Delete legacy surfaces only with both `--remove-legacy` and `--apply` after the new files are valid.
7. Run repository-local validation and `engineering-core doctor` after application. Report commands, outcomes, selected guidance, deviations, and unresolved diagnostics.
8. For fleet work, use `scan-adoption` baselines and `--fail-on` selectors to ratchet new objective debt. Keep semantic findings advisory unless a scope owner explicitly promotes a rule.

## Deviation evidence

A deliberate deviation should record a stable ID, reason, owner, evidence paths or links, and a review date. Do not invent evidence or silently suppress objective catalog and policy failures.

## Advice responses (engineering-advice-response-v1)

When producing an advice response for `engineering-core advise --response`, the
compiled request carries a `response_contract` block with the full grammar; the
binding rules are:

- Top level requires exactly: `schema`, `request_sha256`, `provenance`,
  `status`, `summary`, `recommendations`, `critiques`, `patch_proposals`.
- `status` is `advice`, `abstain`, or `unknown`; abstain/unknown carry no
  recommendations or patches.
- Every recommendation requires exactly: `id`, `catalog_ids`, `recommendation`,
  `confidence` (0..1), `unknowns`, `counterevidence`, `falsification`,
  `citations`, `competes_with`; `catalog_ids` must be a subset of the request's
  `allowed_catalog_ids`; citations index captured evidence with
  `0 <= start < end`.
- Every critique requires exactly: `recommendation_id`, `critique`, `severity`
  (`low|medium|high`), `falsification`.
- `falsification` is a bounded string or an array of bounded strings, in every
  position — the same rule for recommendations and critiques.
- Patch proposals are owner-local, recommendation-bound unified diffs.
- Budgets: at most 20 recommendations, 20 critiques, 10 patches.

## Default discipline set

When nothing narrower is declared, adoption recommends five default
disciplines: `validation`, `testing`, `security-privacy`, `documentation`,
`dependency-governance` (plus `design-system` and `accessibility` when a
frontend lane is selected, and `specification-and-dsls` when a `schema`/
`schemas`/`contracts` directory exists).
