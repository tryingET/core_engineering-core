---
summary: "Proposed cross-owner contract, proof population, and cumulative evidence gates for engineering-core v1.0."
read_when:
  - "Reviewing or executing any engineering-core v1.0 convergence work."
  - "Selecting owner canaries, empirical protocols, release evidence, or rollback criteria for v1.0."
  - "Assessing whether a claimed v1 pillar is demonstrated rather than merely implemented."
type: "rfc"
system4d:
  container:
    boundary: "engineering-core's public product contract plus explicitly accepted, owner-local AI Society proof tasks."
    edges:
      - "Agent Kernel decision, task, direction, evidence, and artifact references"
      - "owner-repository validation and canary receipts"
      - "DSPx/Oracle empirical protocol and results"
  compass:
    driver: "Earn a trustworthy semver v1.0 baseline without centralizing consumer authority or treating mechanisms as outcomes."
    outcome: "One cumulative, evidence-gated v1.0 contract across dependable adoption, federation, calibration, and governed evolution."
  engine:
    invariants:
      - "All four pillars are required for v1.0; strength in one cannot waive another."
      - "Repository owners retain execution, validation, adoption, rollback, and landing authority."
      - "No document, loop, scanner, model, receipt, or empirical result self-authorizes a release or doctrine change."
  fog:
    risks:
      - "Cross-owner evidence may be confused with central rollout authority."
      - "A broad implementation surface may pass proxies without proving complete operator journeys."
      - "Post-hoc thresholds could turn exploratory results into an unjustified v1 claim."
---

# RFC: engineering-core v1.0 convergence contract

## Status and authority

- **RFC state:** proposed; not accepted and not an execution or release authorization.
- **AK decision:** `128` (`review_pending`; strict convergence with multi-lane synthesis).
- **Durable product intent:** `docs/project/vision.md`.
- **Maturity contract:** `docs/project/product_posture.md`.
- **Draft baseline:** repository commit `57dcab0` above published `v0.10.0` commit `9038d1ed3d443f44e18624d908d266e5e6dfd934`.

The words **MUST**, **MUST NOT**, **REQUIRED**, and **PASS** describe the proposed v1 gate. They become an accepted execution membrane only through the linked Agent Kernel decision workflow. An accepted RFC still does not authorize mutation in a participant repository; every owner repository requires its own exact AK task, local instructions, validation contract, and landing decision.

## Decision requested

Adopt **Model A**: one cumulative semver `v1.0` contract with four required pillars:

1. **Dependable Adoption**
2. **Federated Interoperation**
3. **Evidence Calibration**
4. **Review-Governed Evolution**

All four MUST reach the bounded baseline below before v1.0 is declared. Compatible maturation may continue through v1.x. This RFC defines no v2, v3, or v4 contract. A future major version requires a compatibility break or materially different product constitution and a new decision.

## Why a convergence contract is needed

Version `v0.10.0` already contains mechanisms across all four pillars. The unresolved risk is therefore not simply missing feature surface. It is whether those mechanisms work together under complete operator journeys, independent owner boundaries, realistic version skew and hostile inputs, prospective empirical comparison, and reversible doctrine review.

A source implementation, unit test, static adoption flag, matched bundle, or successful visible loop can support one part of that proof. None establishes the cumulative product claim by itself.

## Scope

### In scope

- freezing the public v1 compatibility and authority contract;
- proving complete adoption, upgrade, recovery, rollback, and removal journeys;
- proving bounded cross-owner production and consumption under skew and partial information;
- prospectively testing evidence-informed advice against a static baseline;
- exercising proposal, pilot, review, promotion, rejection, revision, deprecation, and retirement paths;
- preserving counterevidence, abstentions, negative results, privacy, and owner exit;
- producing a release-readiness assessment through AK and owner evidence.

### Non-goals

- inventing a hosted control plane or society-wide repository denominator;
- bulk adoption or mutation from scanner output;
- making Agent Kernel, DSPx, ROCS, Prompt Vault, Pi, or engineering-core absorb another owner's authority;
- requiring external organizations for v1.0;
- claiming causal effectiveness from schema conformance or owner-authored receipts;
- using model agreement, review rhetoric, or loop count as a release metric;
- defining v2+;
- merging or pushing a `1.0.0` release-candidate commit to `main`, creating a tag, publishing, or rolling out consumers without the explicit operator and owner actions defined by G5.

## Predeclared proof population

### Producer and coordination owner

| Role | Repository | Purpose | Counts as an independent positive adopter? |
|---|---|---|---|
| Product producer | `core/engineering-core` | Freeze candidate contracts, provide deterministic harnesses, validate artifacts, and integrate bounded references. | No |

Engineering-core may validate portable records and coordinate the product-level assessment. It MUST NOT execute participant commands by default, own participant dashboards, or convert supplied evidence into participant approval.

### Positive owner groups and participant baselines

Three independently governed owner groups and four positive participant baselines are REQUIRED. The extra TeachingCo baseline supplies the new-adopter journey that the three current adopters cannot.

| Owner group | Exact repository/baseline | Pre-RFC observed posture | Required proof role |
|---|---|---|---|
| HoldingCo | `holdingco/fcos-control-board` | Governance product; v0.8.0 local immutable pin; declared planning/advisor/owner-use capabilities; historical owner-round-trip receipt. | Existing-adopter governed owner-use and lifecycle canary; replay against the selected v1 candidate without authority promotion. |
| TeachingCo | `teachingco/mathe` | Content-heavy project; v0.7.0 local immutable pin; planning declared; prior static adoption history. | Small existing-adopter upgrade, portability, stale-posture detection, rollback, and removal canary. |
| TeachingCo | `teachingco/wib@316c45747560392fdab03498849652e8d7e94fcb` | Immutable historical product-content baseline immediately before its first engineering-core adoption; the three adoption surfaces are absent at this commit. | Owner-approved historical clean-slate adoption, failure recovery, removal, and restoration canary. It does not claim current `wib` is unadopted. |
| SoftwareCo | `softwareco/owned/pi-extensions` | Large TypeScript/Pi monorepo; immutable v0.8-era remote commit; heterogeneous package adoption surfaces. | Existing-adopter federation, package-boundary, version-skew, partial-population, and hostile-input canary. |

These are dated routing observations, not durable participant truth or successful proof. G0 MUST replace them with a reviewed population manifest containing exact full revisions, roles, immutable-source references, owner task IDs, validation contracts, baseline posture, and an authority ceiling. Every participant refreshes its Git, AK, policy, and validation state before owner acceptance.

### Required negative control

| Owner group | Exact repository | Pre-RFC observed posture | Required proof role |
|---|---|---|---|
| HealthCo | `healthco/agents` | No tracked engineering-core adoption surface or immutable pin at the assessed root. | Remain a truthful missing/non-adopter control during federation scans. No adoption mutation is required for v1. |

A missing participant MUST remain missing or unknown, not be inferred as adopted, unhealthy, or consenting. A later HealthCo adoption would require its own owner task and is outside this gate unless the RFC is revised before evidence capture.

### Population manifest and changes

G0 MUST freeze `docs/project/v1-proof-population.json` and record its canonical SHA-256 in every G1–G5 artifact. The manifest identifies the four positive baselines and untouched negative control by owner, physical repository identity, full Git revision, starting adoption state, accepted AK task, validation contract, evidence custody, and permitted role.

A participant may decline, become unavailable, or prove structurally unsuitable. Replacement requires, before any replacement evidence is captured:

1. an RFC revision naming the replacement and preserving the reason;
2. an **accepted AK decision revision** referencing the new RFC and population manifest;
3. an exact accepted task in the replacement repository;
4. a fresh preflight, protocol, and metric declaration;
5. a new population-manifest digest.

If population-dependent evidence has begun, every affected population gate restarts against the new digest. Silent substitution, a supporting artifact without accepted decision revision, or post-result population changes invalidate G1–G5 fan-in.

## Universal proof rules

Every gate applies these rules:

1. **Immutable binding.** Evidence binds the exact engineering-core candidate, population-manifest digest, participant revision, configuration, protocol version, commands, timestamps, and content digests.
2. **Owner-local authority.** Participant commands and mutations run only under participant tasks and instructions. Owner outputs remain owner-local unless a redacted, bounded artifact is deliberately published.
3. **Clean or declared baseline.** Each run records tracked, untracked, ignored, and active-task posture. Pre-existing state is never silently absorbed into a candidate commit.
4. **No hidden workspace dependency.** Portability runs use an immutable remote source from a clean environment and MUST NOT resolve through a local engineering-core checkout.
5. **Negative evidence retained.** Failures, unknowns, missingness, abstentions, rejected proposals, and counterevidence are first-class inputs.
6. **No authority promotion.** Structural validity, `matched`, owner acceptance, empirical superiority, and governance acceptance remain separate facts.
7. **Reproducibility.** Deterministic outputs are run twice from the same inputs and MUST be byte-identical. Non-deterministic empirical outputs bind seeds/configuration and are replayable to the extent declared by the empirical owner.
8. **Data minimization before transfer.** Before any external model, provider, or empirical-owner transfer, the participant owner approves an exact digest-bound redacted request manifest, data classification, minimum fields, endpoint, model/adapter identity, retention, training-use, network, custody, and access policy. Raw cross-owner repository or task snapshots MUST NOT be transmitted.
9. **Privacy after transfer.** No secrets or private source payloads are committed to this repository. External evidence is referenced by bounded identity, digest, scope, capture time, and authority ceiling.
10. **No waivers by aggregation.** A failed required participant or pillar blocks v1.0. A new decision may revise a flawed gate prospectively; it may not relabel failed evidence after results are known.
11. **Independent review.** The artifact producer cannot be the sole reviewer of its own gate. Review identities and conflicts are recorded before closure.
12. **Candidate drift restarts proof.** Any release-candidate change creates a new immutable candidate. A predeclared impact matrix determines which gates must rerun; no generic reviewed-descendant exception exists.

## Gate G0 — contract, authority, and candidate freeze

G0 has two ordered checkpoints.

### G0-A — execution membrane

G0-A passes only when:

- the AK decision referencing this exact RFC commit is accepted as **Model A** and linked to active direction `AK.V5.SF01`;
- the reviewed population manifest and canonical digest exist;
- participant owners accept exact scoped tasks and declare validation commands, baseline state, evidence custody, reviewers, data-transfer policy, and rollback boundary;
- the public command, exit-code, schema, catalog-ID, content-lifecycle, support-platform, artifact-name, migration, and removal surfaces are inventoried;
- the G2 fixture/resource manifest and G3 prospective protocol, power/sensitivity analysis, case manifest, metrics, thresholds, missingness rules, model strata, and analysis code are frozen before outcomes are visible;
- an impact matrix maps each possible candidate change to mandatory gate reruns;
- the ten-iteration engineering-core budget below is mapped to exact tasks rather than one broad objective;
- `ak direction check` and the decision passport report no unresolved structural issue for bounded convergence execution.

Only G0-A releases bounded convergence/proof-harness tasks and separately owner-accepted G4-A pilot tasks. G0-A does not by itself authorize participant mutation, a release candidate, or publication.

### G0-B — immutable release candidate

After accepted convergence work is complete, G0-B passes only when:

- one `1.0.0` release-candidate commit exists on a non-`main` branch or pull request;
- package version, package `__version__`, root and packaged catalogs, required catalog history, changelog, migration notes, dated release notes, support/docs, and lockfile are synchronized at that exact commit;
- `UV_NO_CONFIG=1 uv run python scripts/release-local.py verify --version 1.0.0` passes at that commit;
- the candidate is available by immutable remote commit for G1 portability runs but has no `v1.0.0` tag or GitHub Release;
- G0-B records the exact candidate commit and frozen population digest that every future G1–G5 artifact MUST bind.

**Failure rule:** no convergence implementation begins merely because this RFC exists or an RFC-review task completes. Before G0-B, only separately accepted G4-A pilot tasks may mutate participant worktrees; G1, G2, G3, and G4-B proof cannot begin until both G0-A and G0-B pass.

## Gate G1 — Dependable Adoption

### Required journeys

Each of the four positive participant baselines MUST execute all of these journeys in an isolated owner-controlled clone or worktree:

1. install or invoke the immutable v1 candidate from its remote source;
2. retrieve and explain applicable guidance without hidden workspace context;
3. dry-run initialization or migration and review the exact proposed diff;
4. apply an owner-approved adoption or migration while preserving declared deviations;
5. diagnose and scan the resulting adoption without executing undeclared consumer commands;
6. for existing adopters, upgrade from the recorded prior pin; for the historical clean-slate baseline, repeat plan/apply and prove the documented idempotence behavior;
7. inject at least one recoverable bad-pin or malformed-policy failure, observe a bounded failure, and recover without manual state fabrication;
8. roll back to the recorded starting posture—prior pin for existing adopters and no adoption surfaces for the clean-slate baseline—and pass validation;
9. remove engineering-core adoption surfaces in an isolated branch/worktree and prove repository runtime authority and operational truth remain intact;
10. restore the owner-selected final test posture and pass validation again.

The HealthCo negative control MUST be classified as missing/non-adopted without mutation or invented denominator membership.

### Exact pass threshold

G1 passes only if:

- all ten journeys pass for all four positive baselines: **40/40 required participant-journeys**;
- the historical `teachingco/wib` run begins from exact commit `316c45747560392fdab03498849652e8d7e94fcb`, under a current TeachingCo owner task that authorizes only an isolated historical worktree;
- the negative control is classified truthfully in every scan: **100%**;
- every planned failure is detected before an unsafe apply or consumer-command effect: **100%**;
- every participant's declared pre-change, post-change, rollback, removal, and final validation command completes successfully;
- remote-source portability succeeds for all four positive baselines, with zero local `git+file` or workspace-checkout resolution in the portability runs;
- there are zero unresolved objective error diagnostics, silent deviation losses, secret disclosures, or authority-loss events;
- all observed failure and recovery artifacts remain available to reviewers.

Usability timings and operator commentary are retained as descriptive evidence. They cannot compensate for a failed required journey.

## Gate G2 — Federated Interoperation

### Required cross-owner matrix

A canonical fixture manifest, expected-result digest, and harness version MUST freeze before the first conformance run. The corpus includes:

- released inputs from v0.7.0, v0.8.0, v0.10.0, and the immutable v1 candidate;
- all four positive participant outputs plus the HealthCo missing control;
- complete, partial, unavailable, permission-denied, and privacy-redacted populations;
- reordered and duplicate population entries;
- unknown future fields and unsupported schema identifiers;
- malformed JSON, duplicate members, invalid UTF-8, oversized files, symlinks and symlinked parents, FIFO/special files, traversal/control paths, stale revisions, catalog skew, and hostile Markdown/table content.

The isolated managed-scratch corpus is bounded to **64 population entries, 2,048 filesystem entries, depth 16, 1 MiB per file, 16 MiB total, and a 60-second per-command deadman**. Lower owning-schema limits still apply. FIFO and special-file probes run only inside the fixture root and MUST complete through no-follow/type rejection rather than blocking reads.

### Exact pass threshold

G2 passes only if:

- all four positive participant baselines produce an owner-local bounded observation at their accepted task revision;
- at least two of the three positive owner groups independently consume the same bounded aggregate inputs and produce semantically equivalent normalized status/count/digest results;
- deterministic producer and consumer outputs are byte-identical across two runs with the same ordered inputs;
- normalized results are invariant to permitted population ordering;
- all valid compatibility fixtures pass and all invalid or unsupported fixtures fail closed with structured diagnostics: **100% of the frozen corpus**;
- missing, unavailable, private, stale, and unsupported records remain explicitly incomplete and are never coerced to adopted, healthy, current, or verified;
- duplicate identities cannot inflate denominators or evidence counts;
- no consumer command, model, URL, observation reference, or supplied patch is executed by scan/aggregation paths;
- generated reports and remediation queues remain in the consuming owner scope;
- the system operates with no required hosted control plane or centrally invented society denominator;
- there are zero cross-owner secret disclosures, path escapes, authority promotions, limit overruns, or blocking special-file reads.

Any corpus or expected-result change after the first conformance run creates a new protocol revision and restarts G2.

## Gate G3 — Evidence Calibration

G3 is an empirical gate owned by DSPx/Oracle or another explicitly accepted empirical owner. Engineering-core supplies bounded schemas and candidate artifacts; it does not score itself or turn study results into release authority.

### Frozen prospective study

Before treatment output, the empirical owner MUST freeze:

- a prospective paired-binary power/sensitivity analysis with at least **80% power** at the declared 15-percentage-point improvement and two-sided `alpha=0.10`, explicitly modeling the assumed discordant-pair rate, owner/task clustering, model allocation, missingness, and attrition; the sample is at least **48 paired task cases** and at least **12 from each positive participant baseline**, but any larger computed sample is mandatory;
- immutable repository/task snapshots, owner-authored expected constraints, and at least **8 deliberately insufficient-evidence cases** included in the sample;
- a static arm using deterministic engineering-core plan/recommendation output without owner-evidence advice;
- an evidence-informed arm using the same base plan plus request-bound provider-neutral advice;
- owner-authorized isolated replicas for **both arms of every case**, with randomized, blinded review order and no shared candidate branch or production effect;
- one primary binary outcome per arm/case: the arm satisfies the frozen owner rubric, its declared participant validation, and the predeclared verified evidence condition;
- one probabilistic forecast per evidence-informed arm/case for that exact primary outcome; multiple recommendations are reduced by a frozen joint-success rule and cannot increase the sample count;
- at least **two distinct base-model families/identities**, each in a separately bound provider/model/adapter configuration, assigned at least 24 cases and represented in every positive owner group; prompt, seed, temperature, quantization, endpoint, or adapter-only variants of one base model do not count as model diversity;
- exact confidence semantics, ECE bins `[0.00,0.20)`, `[0.20,0.40)`, `[0.40,0.60)`, `[0.60,0.80)`, and `[0.80,1.00]`, scoring code, seeds, exclusion rules, missingness policy, owner/model stratification, cluster-aware or paired analysis, and bootstrap procedure;
- owner dispositions, validation results, empirical outcomes, and later receipts kept distinct from one another and from governance decisions;
- for every external transfer, the participant-approved digest-bound redacted request manifest and the endpoint, retention, training-use, network, custody, and access controls required by the universal rules.

Deferred, rejected, unsupported, missing, failed-validation, or unverifiable outcomes are non-positive and MUST NOT be dropped. Owner preference alone and a stored `evidence-verified` claim alone are insufficient.

### Exact pass threshold

G3 passes only if:

- every frozen paired case is reported at the case level, including negative and missing outcomes, with no recommendation-level pseudoreplication;
- the evidence-informed arm's paired net-win rate over the static arm is at least **15 percentage points**;
- the lower bound of the predeclared **90% paired-bootstrap interval** for that net improvement is greater than `0.00`;
- owner-group and model-configuration effects are reported separately, and no required stratum has net effect below **-5 percentage points**;
- the evidence-informed case forecasts have **Brier score <= 0.20** and **expected calibration error <= 0.15** under the frozen bins;
- all insufficient-evidence cases return `abstain` or `unknown` with no recommendation or patch proposal: **100%**;
- there are zero secret disclosures, invalid citations, unbound patches, owner-identity mixups, unauthorized network transfers, or authority-promotion events;
- the empirical owner publishes a bounded result, replay/configuration receipt, limitations, exclusions, and counterevidence reference;
- an independent reviewer confirms that cases, exclusions, forecasts, metrics, and transfer policies were not changed after outcomes were visible.

If the frozen or effective reported sample fails the 80% prospective-power requirement, an interval crosses the required boundary, one stratum is materially harmed, calibration misses threshold, or safety fails, G3 remains failed. A prospective revised protocol requires an accepted AK decision revision and a fresh held-out corpus; the failed study remains in lineage.

## Gate G4 — Review-Governed Evolution

### Authority split

Participant owners authorize only their local proposal, pilot, evidence, rollback, and disposition. They cannot promote shared engineering-core content. The engineering-core content owner alone may accept, reject, revise, deprecate, retire, or promote shared content under an exact engineering-core AK task, accepted decision where required, and repository validation.

### G4-A — pre-candidate lifecycle execution

After G0-A, each positive owner group MUST originate one substantial shared-content candidate under exact owner tasks, for **three total candidates**. Every candidate includes the minimum decision record from `docs/content-lifecycle.md` and proceeds through proposal, bounded pilot, rollback exercise, and owner review. Participant pilot evidence binds exact pilot revisions and content digests. Any ordinary pilot-to-stable promotion MUST have evidence from at least **two independent participant contexts**; the documented narrow emergency exception remains precautionary, explicitly uncertain, and time-bounded.

All participant pilot mutations, engineering-core content-owner dispositions, accepted shared-content landings, and rejected/retired history complete before G0-B. G0-B MUST contain the final accepted G4-A state.

Across the three final outcomes, the set MUST include:

- at least one engineering-core-owner promotion to stable or accepted stable revision after the two-context gate;
- at least one rejection, retirement, or reversion after pilot;
- at least one material revision, split, or scope narrowing caused by counterevidence;
- at least one exercised rollback from a pilot/default selection without erasing history.

One candidate may satisfy more than one outcome category, but all three owner groups must complete a full reviewed cycle.

### G4-B — post-candidate verification

After G0-B, G4 closure is non-mutating verification that the exact candidate contains the accepted G4-A dispositions, preserves rejected/retired lineage, remains compatible as declared, and reproduces the recorded rollback and participant-validation evidence. A defect requiring content or code change creates a new candidate and invokes the impact matrix; G4-B never lands a fix into the candidate it is assessing.

### Exact pass threshold

G4 passes only if:

- all three candidates preserve problem, scope, strongest alternative, evidence, counterevidence, falsification, compatibility, migration, rollback, review trigger, and retirement signal;
- each pilot is opt-in, bounded, expires or reaches a named review event, and cannot silently become default;
- participant-local dispositions and engineering-core shared-content decisions remain separate, and every final shared transition is recorded by the engineering-core owner surface and linked to immutable owner evidence;
- accepted shared changes landed before G0-B only through their exact engineering-core task and complete repository validation, and G4-B performs no repository mutation;
- stable catalog/docs/package projections remain synchronized after accepted changes;
- rejected, retired, and superseded material remains historically interpretable;
- an older supported consumer receives either compatible behavior or the documented structured migration/downgrade result;
- no telemetry threshold, model output, KES candidate, doctrine proposal, loop completion, participant disposition, or popularity count performs automatic promotion;
- all participant validations pass after final disposition and after the exercised rollback;
- there are zero unowned defaults, irreversible migrations, or erased negative results.

## Gate G5 — cumulative v1 release readiness

G5 is a fan-in gate over the exact G0-B commit, not an automatic release command.

It passes only if:

1. G0, G1, G2, G3, and G4 each have a PASS artifact and independent review with no open blocker;
2. every artifact binds the same exact `1.0.0` candidate commit and population-manifest digest; any candidate change creates a new candidate and triggers the frozen impact-matrix reruns;
3. these candidate checks pass from a clean checkout:
   - `UV_NO_CONFIG=1 uv sync --locked`;
   - the validation commands in `AGENTS.md`;
   - `UV_NO_CONFIG=1 uv run python scripts/release-local.py verify --version 1.0.0`;
   - `node ~/ai-society/core/agent-scripts/scripts/docs-list.mjs --docs docs --strict`;
   - `git diff --check`;
   - `cd dist && sha256sum ./*.whl ./*.tar.gz > SHA256SUMS && sha256sum -c SHA256SUMS`;
4. the G0-B candidate-head SHA and GitHub pull-request merge-test SHA are both recorded; pull-request `CI / required` passes on the merge-test SHA as integration evidence, including Ubuntu Python 3.10–3.13 and rolling Arch installed-wheel lanes, without being mislabeled as candidate-SHA evidence;
5. public README, support policy, changelog, migration notes, dated release notes, catalogs, schemas, and built artifacts tell the same v1 story;
6. all four positive baselines install the exact remote candidate and the untouched negative control remains truthful;
7. the AK decision passport, direction check, task closure checks, evidence references, counterevidence, rollback record, protocol digests, and rerun obligations are complete;
8. a final independent review confirms the exact candidate and population digest and that no target state is described as shipped merely because a component or proxy passed;
9. the operator separately authorizes an exact-SHA, fast-forward update of `main` to the G0-B commit after confirming current remote `main` is its ancestor; merge commits, squash/rebase results, intervening commits, or any different `main` head create a new candidate and require impact-matrix reruns. The operator understands that successful `main` CI on that exact pushed SHA automatically creates `v1.0.0` and the GitHub Release; downstream rollout remains separately owner-authorized.

After publication, a post-release task MUST confirm that tag `v1.0.0` resolves to the exact candidate, the successful `main` workflow head equals that candidate, the GitHub Release was built from that commit, and downloaded wheel/sdist assets pass their published `SHA256SUMS`. Only then may status language say v1.0 was published and verified.

If post-publication identity or checksum verification fails, status becomes **published-but-unverified**, downstream rollout stops, owners are notified, local/downstream copies are quarantined, and an explicit corrective-release or withdrawal decision preserves rather than rewrites published lineage.

A G5 PASS means only that the exact candidate may proceed to the explicit merge/push release action. It does not itself tag, publish, bulk-upgrade consumers, close external owner work, or define v2.

## Rollback and stop rules

- Rejection of this RFC leaves `v0.10.0` as the latest stable product and archives/defer-closes dependent tasks without rewriting evidence.
- Before the operator-authorized exact-SHA push, a failed candidate remains isolated from `main`; candidate fixes create a new commit and mandatory impact-matrix reruns.
- A G1 failure rolls back only the affected owner worktree/branch and preserves the failure artifact.
- A G2 failure disables or withholds the incompatible aggregate path; owner-local source records remain untouched.
- A G3 failure leaves evidence-informed advice advisory/experimental and MUST NOT be reframed as a governance success.
- A G4 failure keeps candidates at proposal/pilot/deprecated state as appropriate and restores the prior stable selection.
- A participant withdrawal invalidates the population digest and requires the accepted replacement process before population proof resumes.
- Any secret disclosure or unauthorized transfer triggers immediate containment, owner notification, endpoint/token revocation or rotation where applicable, artifact quarantine, incident preservation, and a fresh-corpus restart after owner clearance.
- Any path escape, unauthorized mutation, fabricated evidence, silent participant substitution, or authority promotion is an immediate stop condition and blocks cumulative readiness.
- Expected G1/G2 negative fixtures count as planned observations. Visible-loop, peer, and subagent work stops on task-scope drift, unresolved pre-existing changes, **unexpected** validation failure, or inability to bind proof to the exact owner task.

## AK execution shape

The intended task graph is:

```text
RFC adversarial review/freeze
  -> accepted decision + population/protocol freeze (G0-A)
    -> dependable-adoption harness -----------------\
    -> federated-interoperation harness -------------+
    -> evidence-calibration empirical handoff -------+-> G4-A owner pilots + final dispositions
    -> review-governed-evolution harness ------------/        -> 1.0.0 candidate freeze (G0-B)
                                                                  -> G1/G2/G3 + non-mutating G4-B
                                                                    -> cumulative G5 readiness
```

The G0-A execution-release task is a manual authority membrane: convergence tasks MUST depend on it and it cannot complete until the AK decision is accepted. Separately accepted G4-A owner tasks may run before G0-B; all other participant proof waits for G0-B. Cross-repository tasks are created in their owning repositories after the owner accepts the exact handoff; they are not shadow tasks in engineering-core.

## Visible-loop budget

Ten is a maximum **engineering-core coordination** review/implementation budget, not one broad `--count 10` invocation and not a cap on owner proof:

| Iteration budget | Bounded use |
|---:|---|
| 1 | Adversarial RFC review and freeze |
| 2–3 | Dependable-adoption protocol, harness, and fixup |
| 4–5 | Federation/skew/hostile-input protocol, harness, and fixup |
| 6 | Evidence-calibration integration and empirical-owner handoff |
| 7 | Review-governed lifecycle protocol and harness |
| 8 | `1.0.0` candidate freeze and release-proof fixup |
| 9 | Cross-gate integration fixup |
| 10 | Cumulative readiness audit |

Every positive participant baseline receives its own exact owner-repository task and target-root loop or equivalent owner execution **outside** this ten-iteration coordination budget. No iteration limit may combine repositories, waive an owner task, reduce the frozen population, or substitute for the empirical campaign. Each loop normally uses `--count 1` or `--count 2`, begins from an owner-approved baseline, and reports/commits only within its exact task.

## Alternatives considered

### One broad visible loop with count 10

Rejected. It would bind sixty staged prompts and ten commits to one objective while crossing repositories, authority owners, and empirical modes. Later iterations would operate on stale assumptions and could silently mix unrelated work.

### One major version per pillar

Rejected. The pillars are cumulative properties of one coherent product. Strategy horizons are not semver majors.

### Declare v1 from existing mechanism coverage

Rejected. v0.10.0 implementation breadth is not complete operator, federation, calibration, or lifecycle proof.

### Require an external organization

Deferred. Public portability is mandatory, but the initial v1 proof population is independently governed AI Society owner groups. External evidence may strengthen a later v1.x claim.

### Allow a strong pillar to offset a weak pillar

Rejected. Authority safety, dependable use, federation, empirical truth, and legitimate evolution fail differently; an average score would hide a categorical failure.

## Review questions

1. Are the three positive owner groups and four participant baselines meaningfully independent, representative, and feasible without central execution authority?
2. Are 40/40 adoption journeys and the frozen federation/resource corpus strict enough to prevent proxy success while remaining executable?
3. Does G3 define one coherent per-case estimand, adequate power, model diversity, calibration target, and preventive data-transfer membrane?
4. Do the G4 authority split and outcome requirements force real cross-context promotion, rejection/retirement, and rollback evidence?
5. Are any commands, schemas, participant payloads, or owner decisions being absorbed into engineering-core improperly?
6. Can every gate fail visibly, contain an incident, and roll back without weakening the product's public authority boundaries?
7. Does the branch/PR-to-automatic-release sequence preserve exact-candidate proof and explicit operator control?
8. Does any wording imply v1 is current, accepted, released, or scheduled before the cumulative gate and explicit release action?
