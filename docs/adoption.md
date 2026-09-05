---
summary: "How repositories adopt engineering-core lanes, addenda, disciplines, and repo-local overrides."
read_when:
  - "A repo is adding or refreshing docs/engineering.local.md."
  - "An agent needs to choose engineering-core lanes, addenda, or disciplines for a concrete repo."
  - "Reconciling opt-in repo skills or a KES-derived improvement with recipient-owned adoption."
type: "guide"
---

# engineering-core adoption

Use engineering-core as a versioned upstream source for shared engineering guidance, not as a compatibility shim for legacy names.

Related governance docs:

- `docs/authority-map.md` — where shared guidance, repo-local deviations, templates, validation policy, and runtime truth belong.
- `docs/discipline-lifecycle.md` — when to add, split, merge, or relocate discipline guidance.

## Adoption surface

A repo that adopts engineering-core should carry:

1. `policy/engineering-lane.json` when a machine-readable lane declaration is useful.
2. `docs/engineering.local.md` for human-readable local overrides.
3. A local validation command surface (`just`, package scripts, or equivalent) that records what must pass before handoff.

## Read order

1. Repo-local `docs/engineering.local.md`.
2. Declared lane(s), for example `engineering-core show ts --prefer-repo` from this repo.
3. Conditional addenda only when relevant, for example `ts-frontend` for browser UI work.
4. Cross-language disciplines only when they own the current concern.

## Selection rule

Choose the smallest truthful upstream set:

- one or more language lanes for implementation ecosystems;
- conditional lane addenda for narrower surfaces;
- cross-language disciplines for invariants such as validation, testing, accessibility, documentation, or security/privacy.

Do not load every lane or every discipline by default.

Common Lisp repositories should select `common-lisp` explicitly in `policy/engineering-lane.json` or local guidance. ASDF system files are project-named `*.asd` files, so bounded repository inference does not guess this lane from an unbounded wildcard search.

## Safe initialization

`engineering-core init` plans repository adoption without writing by default. It combines an optional catalog profile, explicit `--lane` and `--discipline` values, or conservative repository inference, then closes catalog requirements such as `ts-frontend -> ts`.

```bash
engineering-core init --repo . --profile service-api
engineering-core init --repo . --lane ts --discipline validation --format json
engineering-core init --repo . --lane ts --discipline validation --apply
```

The command emits a unified diff, preserves existing machine-readable fields and structured deviations, and is idempotent after application. It refuses to replace an existing hand-written `docs/engineering.local.md` unless `--force` is supplied after reviewing the proposed diff.

Generated policies reserve `engineering_core.deviations` for evidence-bearing local exceptions. A useful entry records at least an ID, reason, owner, evidence paths or links, and a review date:

```json
{
  "id": "validation.no-browser-e2e",
  "reason": "This package has no browser or external-process boundary.",
  "owner": "platform-tooling",
  "evidence": ["docs/architecture/package-boundaries.md"],
  "review_after": "2027-02-17"
}
```

## Legacy migration

`engineering-core migrate` plans a transition from `docs/tech-stack.local.md` and `policy/stack-lane.json`. It does not delete legacy files unless both `--remove-legacy` and `--apply` are present, and it will not apply a plan that contains conflicts.

```bash
engineering-core migrate --repo .
engineering-core migrate --repo . --remove-legacy --apply
```

## Rollback and removal

Every successful `init`/`migrate --apply` writes an adoption journal at
`.engineering-core/adoption-journal.json` recording the exact before/after bytes
of each changed file. Two public commands consume it:

```bash
engineering-core rollback --repo .   # restore exact pre-adoption bytes, then remove the journal
engineering-core remove --repo .      # delete adoption surfaces (policy + managed doc), then remove the journal
```

Both refuse fail-closed with exit 2 when there is no journal, when current file
bytes drift from the applied transaction (owner edits are preserved, never
clobbered), or when there is nothing to act on (no noop success). Refusals print
a JSON receipt with the reasons.


## Ownership rule

Adoption should preserve the authority map:

- engineering-core owns shared lanes and disciplines;
- repo docs own local deviations and selected subsets;
- governance-kernel owns canonical validation policy;
- templates own generated defaults;
- Agent Kernel owns runtime task/evidence/decision truth.

Do not move repo-specific commands into shared disciplines, and do not fork shared doctrine into generated templates.

## Hard rename rule

The rename to `engineering-core` is intentionally breaking. Do not recreate old CLI aliases, package aliases, file names, or policy names. Consumers should update references directly.

## Adoption scanning

Use `engineering-core scan-adoption` for reusable adoption mechanics across repo, lane, company, or workspace scopes, including `~/ai-society/core` itself. The scanner reports structural adoption, legacy surfaces, invalid policy JSON, catalog/list command presence, selected lanes/disciplines, heuristic semantic discipline flags, and optional `repo-loop-validation-v1` coverage when declared in `policy/engineering-lane.json`.

Examples:

```bash
engineering-core scan-adoption --scope /path/to/lane-root --include-packages --format json
engineering-core scan-adoption --scope ~/ai-society/core --repo-discovery recursive --include-scope-root --include-packages
engineering-core scan-adoption --scope ~/ai-society/core --scope ~/ai-society/softwareco/infra --repo-discovery recursive --include-scope-root --include-packages --format json
```

Keep generated rollout state in the scope owner, not in engineering-core. For example, a lane root may write `governance/engineering-core-adoption-scan.json` and `docs/project/engineering-core-adoption-dashboard.md`, but engineering-core owns the scanner semantics and generic report shape. Start with warning/ratchet use before hard CI gates so scope owners can distinguish true adoption debt from intentional local posture.

Loop validation visibility is optional. `absent` does not make a repo structurally partial; `partial`, `invalid`, or `unknown-version` only means the repo declared a loop validation contract that needs review.

Scanner traversal is explicitly bounded. Defaults are 1,000 repositories, depth 12, 100,000 visited files, and 10 MiB of policy/doc reads; override them with `--max-repositories`, `--max-depth`, `--max-files`, and `--max-read-bytes`. JSON and Markdown report `completeness`, budget `limits`/`usage`, `omissions`, and per-path `failures`. A `partial` result is truthful usable evidence, not complete coverage. Paths and policy-derived text are escaped before Markdown table rendering. Discovery and policy reads are advisory only: the scanner never executes commands found in consumer repositories.

Both scanning and `recommend --repo` use the same typed policy parser. Malformed policy is reported as `invalid-policy` by scanning and rejected by recommendation rather than being interpreted differently.

## Capability observation

The older structural scanner and the v0.6 capability observer answer different questions:

- `scan-adoption` observes local docs, policy, lane/discipline declarations, command mappings, and optional loop-validation structure.
- `doctor` observes whether one repository can be inspected deterministically and whether declared planning/advisor schemas are statically compatible.
- `scan-capabilities` aggregates doctor results over repeated explicit `--repo` paths and/or bounded owner-produced `--repo-file` lists.

A repository may optionally add exact `engineering-core-capabilities-v1` metadata under `engineering_core.capability_contract`. The contract contains protocol identifiers and declaration status only—never shell commands, argv, URLs, credentials, or executable hooks. Missing declarations remain valid and report `absent/not-declared/not-supplied`.

Static observation is not execution evidence. Doctor and capability scan v1 remain receipt-free and cannot emit `execution-observed` or `evidence-verified`. Keep canonical repository populations, rollout dashboards, exceptions, tasks, and runtime evidence with their owner surfaces.

Use `reconcile-evidence` only when an owner explicitly supplies stable repository-id/path mappings and receipt paths. Its matched result means the supplied receipt, bounded artifact, plan bindings, and revision ancestry reconcile; it does not authenticate the owner or promote evidence into AK, CI, release, compliance, or rollout authority.

```bash
engineering-core doctor --repo /path/to/repo --pretty
engineering-core scan-capabilities --repo /path/to/repo --repo-file owner-repositories.txt --pretty
```

Architecture and exact schemas: `docs/rfc/2026-07-11-capability-observation-and-doctor.md`.

## Owner-use packets

After static adoption, an owner may connect a real task to planning and externally supplied advice without changing capability-observation semantics:

```bash
engineering-core prepare-work --repo . --repo-id <stable-owner-id> --context context.json --pretty > packet.json
engineering-core finalize-work --packet packet.json --advice advice.json --disposition disposition.json --pretty > bundle.json
engineering-core verify-work --repo . --repo-id <stable-owner-id> --bundle bundle.json --pretty
```

These commands use only explicit owner inputs. They do not discover AK tasks, invoke models, execute declared commands, apply patches, or promote receipts. Keep canonical task/evidence state with AK or the declared owner; store generated packets and bundles only when the owner finds them useful. See `docs/owner-use-workflow.md`.

## Version pinning

For skill-method adoption, also see the distinct source and recipient revision requirements below; a method pin is not an engineering-core release pin.

For released adoption, prefer an immutable remote commit coordinate over a workspace path or `git+file` URL. The v0.9.0 release resolves to `d74cdcc27a0fe2839707502655c77365ade5cc3a`:

```json
{
  "engineering_core": {
    "repository": "https://github.com/tryingET/core_engineering-core.git",
    "ref": "v0.9.0",
    "command": "uv tool -n run --from 'git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a' engineering-core show <lane>",
    "release_pin": {
      "kind": "git-commit",
      "ref": "v0.9.0",
      "resolved_commit": "d74cdcc27a0fe2839707502655c77365ade5cc3a",
      "source": "git+https://github.com/tryingET/core_engineering-core.git@d74cdcc27a0fe2839707502655c77365ade5cc3a"
    }
  }
}
```

This keeps the human-readable release tag while making retrieval reproducible from the accessible remote commit. A package-version pin is also valid when the package is published from the intended release.

For explicitly local self-development, record the source honestly as `workspace-local-unpinned` and run from the checkout (for example, `uv tool -n run --from . engineering-core ...`). Do not present that local workflow as a released adoption pin.

## Opt-in repo skills and KES improvement

This is the AK5428 design reconciliation, not an implemented learning service or
fleet requirement. A repository may adopt a skill for a qualified workflow, retain
an existing skill, or choose no skill. Engineering-core adoption does not require
one universal maintainer skill per repo and does not install the authoring method.

### Qualify the workflow, then compose owners

The canonical method is `softwareco/contrib/procesio-cli/skills/agent-skill-engineer/`
(workspace-relative), reviewed version `2.0.1` at
`ef56eeecdc21a153c91b047af0e02c0b68924a4c`. Its current source owns the method;
this reference records an adoption baseline, not a copied procedure or automatic
update channel. Consult its `SKILL.md`, `references/decision-framework.md`, and
`references/evaluation-standard.md` for qualification and evaluation requirements.

Before authoring, identify a real recurrent workflow or evidenced costly failure,
the decision that should change, an observable outcome, and explicit non-trigger
neighbors. Reject a one-off topic summary, volatile policy copy, or unbounded
portfolio overlap. Prefer types, permissions, validators, scripts, and regression
tests wherever those can enforce the requirement. Keep context-dependent judgment
in the smallest skill, with conditional references rather than always-loaded prose.

COMPASS-C illustrates three separate owners, not three competing default skills:

| Primary deliverable | Owner | Composition and return condition |
|---|---|---|
| Conditional decision analysis | `compass` | Return an advisory comparison, not implementation permission. |
| Skill design, routing, authoring or evaluation | `agent-skill-engineer` in procesio-cli | Return a reviewed candidate plus evidence and missing proof to the recipient maintainer. |
| COMPASS-C code, packaging, validation or approved skill integration | `.pi/skills/compass-c-maintainer` in COMPASS-C | Integrate only within the exact repo task; verify canonical runtime/generated artifacts and report to its owner. |

Unavailable specialist guidance is an explicit handoff/limitation, not permission
to install globally or paste another owner's method. Reading/source interpretation
and another repository's work are negative routes for COMPASS-C maintenance.

### First-consumer evidence and alternative comparison

AK5424 evidence **8326/8327**, implementation
`9726d109212d54cea252d5f340cf6494720ff7c2` and posture
`56066fc06ae8358cfa81fe7700be28382bb68ddc`, establish a bounded first consumer in
`softwareco/owned/compass-c`. Inspect its maintainer `SKILL.md`,
`references/improvement.md`, `evals/cases.json`, and `tests/test_skill_validation.py`.
The validator had trusted malformed JSON shapes and empty contracts; the evidence
records 15 failing/3 passing new regression tests before repair, then 93 tests and
17 subtests passing with native checks, build and strict skill audit. These are
recorded local deterministic results, not a rerun or a model effect-size estimate.
The eight routing/pressure cases are author-visible development material, not a
hidden holdout or observed host selection results.

| Alternative | Direct benefit and cost | Downstream risk and disposition |
|---|---|---|
| Minimal opt-in composition plus executable enforcement | Local maintainer names specialist handoffs; validator repair fixes the actual malformed-input defect. Costs explicit owner coordination and missing-specialist handling. | Limits trigger/context footprint and localizes withdrawal. Preferred design from this evidence, not empirically proven behavioral superiority. |
| Mandatory universal skill in every repo, copied by template | Superficially uniform availability and fewer handoffs. No first-consumer evidence establishes a need for every recipient. | Risks domain/authoring trigger collisions, extra discovery metadata and unnecessary body/reference loading through over-triggering (host-dependent); can propagate stale policy as apparent authority, obscure recipient consent and expand rollback blast radius. Rejected as a default. |
| Source-method installation treated as improvement | Makes method files available, but cannot repair an executable validator by itself. | Confuses generation, adoption, activation and efficacy; feeds self-grading and holdout leakage if examples become training. Not an acceptance criterion. |

The causal lesson is to repair the executable requirement rather than add prose.
Structural audits and generated artifacts remain useful regression gates; neither
proves fresh-host discovery/use, A/A stability, A/B improvement, KES promotion, or
fleet adoption. Those gaps remain open, not prerequisites retroactively imposed on
AK5424's completed integrity slice.

### Evidence-to-intervention review

Use the following evidence questions in existing owner tasks and references, not
as a new status ladder, mandatory form, or learning database:

1. **Signal and permitted source:** KES signal, explicit correction, or recurring
   failure -> source-owned sanitized evidence with locator, revision/digest,
   observation context, counterexamples, access/retention restrictions and owner.
   A session summary is candidate input, not accepted knowledge. Sanitization must
   preserve causal meaning without copying secrets, private human notes or holdouts;
   if safe sharing is impossible, abstain or route a restricted owner reference.
2. **Causal attribution:** distinguish need/ownership, domain truth, routing,
   instructions, resources, tool/runtime, observation and evaluation failures.
   Record the hypothesis, competing explanation and disconfirming observation.
   Do not fix host loading, auth or validator bugs with generic skill prose.
3. **Bounded intervention:** identify source revision, recipient repo/skill and
   knowledge scope, exact target paths, intended changed behavior, compatibility,
   permission/side-effect limits and withdrawal condition. Compare no change and
   a stronger executable alternative. A source promotion does not grant adoption.
4. **Fixed baseline and evaluation:** preserve the no-skill or old-skill/portfolio
   fingerprint, baseline successes and reproduced failures. Freeze corpus splits,
   rubric, evaluator, host/model settings, thresholds and stopping rules before
   formal results. Keep development examples separate from independently held
   validation/final tests; never train on a revealed holdout or let the acting
   candidate grade itself. Use A/A noise checks and paired A/B for improvement
   claims, through separately authorized empirical/host owners. Deterministic
   integrity repairs instead need direct failure/repaired behavior and regressions;
   they do not require inventing behavioral gains.
5. **Review and recipient acceptance:** supply independent review, negative and
   overlap routing cases, context cost, repairs/regressions and unresolved dissent.
   The recipient records acceptance, deferral, rejection or abstention through its
   authority, with exact accepted revision, applicable scope, evidence, deviations,
   freshness/review condition and responsible owner. Source approval alone cannot
   choose the recipient's revision or broaden its task.
6. **Discovery and use observation:** after separately authorized host activation,
   bind host/client/version, trust/loading settings, repo and skill revision to a
   fresh-context discovery observation; record actual selection/loading and task
   use separately, including abstentions and forbidden-neighbor collisions. A
   committed package, install receipt or generated registry is not measured use;
   observed use alone does not establish improvement.
7. **Contradiction and withdrawal:** attach contrary evidence to the affected
   source/accepted revision, identify recipients through existing owner references,
   and ask each responsible owner to stop recommendation, withdraw or supersede as
   appropriate. Missing recipient visibility stays unknown. Revalidate host removal
   or rollback separately; never overwrite local deviations, erase failed reports,
   or mechanically retry an effect-indeterminate write. A later experiment needs a
   new prospective contract, not relabeling the original failure.

Agent-personal, society, company, project, frame, wave and task are applicability
scopes, not access grants or automatic inheritance paths. Private human memory is a
separate owner surface. Publication, cross-scope transfer and recipient access each
require their own authorization; a sanitized derivative does not waive those gates.

### Reuse existing membranes, keep missing interfaces explicit

- `plan`/`prepare-work` may bind explicit recipient task context, focus paths and
  revisions. They do not acquire KES or discover tasks; source owners supply inputs.
- Optional advice remains inert. `disposition` and `receipt` validate supported
  recommendation decisions and owner observations; `finalize-work` joins their
  exact bindings. Owner-use receipts require the supplied advice/disposition chain;
  do not fabricate advice just to represent a deterministic repair or KES fact.
- `verify-work` and `reconcile-evidence` check freshness/bindings, not acceptance,
  causality, discovery or use. `calibration` separates confidence, acceptance and
  evidence; `patterns`/`doctrine-propose` remain explicit-input, unapplied review aids.
- These strict schemas are not a general KES record format. Keep source/learning,
  evaluation, host and withdrawal facts in existing KES/AK/recipient owner evidence
  and reference them where supported. Do not add undeclared fields, invent catalog
  IDs for repo skills, or persist a parallel adoption ledger. Any missing adapter
  requires an exact separately reviewed owner task before a schema/code extension.

Template reconciliation uses `holdingco/infra/template-propagator/README.md` and
`docs/project/production-rollout-readiness-gate.md` in that owner repo, not a new
engineering-core propagator. Its manifest/plan, explicit-scope preview, trusted-source
apply, authenticated validation/recovery lineage and derived reports already own
rollout mechanics. A readiness packet's validation does not authorize live writes;
owner-approved execution is separate. `core/tpl-template-repo` retains L0/layer
architecture. Generation-graph restrictions do not prohibit reviewed upstream or
peer learning proposals, but learning references cannot bypass generation policy or
grant recipient mutation. No propagation command was exercised for AK5428, and no
skill-specific extension is proposed without a demonstrated owner-interface gap.

See [owner-use workflow](owner-use-workflow.md), [closed-loop contracts](closed-loop.md)
and the [narrow owner-use decision](adr/2026-07-12-narrow-v08-owner-use-workflow.md).
The historical owner-use canaries had pending recommendations and zero real owner
dispositions/receipts; successful fixture or bundle validation cannot close that gap.
Owner handoffs and traceability consumers are specified in the
[authority map](authority-map.md#repo-skill-and-learning-handoffs).
