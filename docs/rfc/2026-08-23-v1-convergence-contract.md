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

The words **MUST**, **MUST NOT**, **REQUIRED**, and **PASS** describe the proposed v1 gate. They become an accepted execution membrane only through the linked Agent Kernel decision workflow. Review may freeze exact RFC bytes for decision support; it does not freeze product direction or accept Model A. An accepted RFC still does not authorize mutation in a participant repository; every owner repository requires its own exact AK task, local instructions, validation contract, and landing decision.

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
- merging or pushing a `1.0.0` release-candidate commit to `main`, creating a tag, publishing, or rolling out consumers without a separate exact release task and operator action after G5.

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

G0-A2 MUST freeze `docs/project/v1-proof-population.json`. Its canonical digest is SHA-256 over UTF-8 JSON Canonicalization Scheme (RFC 8785) bytes; the raw transport-byte SHA-256 and byte length are recorded separately. Every G1–G5 artifact records the canonical digest.

The manifest is canonical only as the immutable population input for one protocol/candidate revision. It does not become current task, owner, validation, custody, or adoption truth. It identifies each positive baseline and negative control by owner, physical repository identity, full Git revision, immutable source, starting posture, permitted role, exact AK task ID, observed task state and observation time, owner-approval reference, validation contract, evidence custody, and authority ceiling. Every run re-resolves live AK and owner state; missing, stale, conflicting, or unknown state blocks execution rather than being repaired from the manifest.

A participant may decline, become unavailable, or prove structurally unsuitable. Replacement requires, before any replacement evidence is captured:

1. an RFC revision naming the replacement and preserving the reason;
2. an **accepted AK decision revision** referencing the new RFC and population manifest;
3. an exact owner-authorized task in the replacement repository;
4. a fresh preflight, protocol, metric declaration, and reviewer assignment;
5. a new population-manifest digest.

If population-dependent evidence has begun, every affected population gate restarts against the new digest. Silent substitution, a supporting artifact without accepted decision revision, or post-result population changes invalidate G1–G5 fan-in.

## Universal proof rules

Every gate applies these rules:

1. **Stage-correct immutable binding.** G0-A1 artifacts bind the exact RFC commit/content digest and authority state. G0-A2 binds candidate-independent protocol templates, fixture templates, population inputs, and transition rules while recording the candidate as unassigned. G4-A evidence binds the exact engineering-core base/pilot revision, participant revision, content/protocol/population digests, commands, configuration, and timestamps. G0-B materializes and binds candidate-dependent instances without rewriting the G0-A2 templates, then emits the candidate-bound G0 PASS artifact. G1–G3, G4-B, and G5 bind that exact candidate and population digest.
2. **Owner-local authority.** Participant commands and mutations run only under participant tasks and instructions. Engineering-core artifacts validate projections; they do not replace AK or owner truth.
3. **Clean or declared baseline.** Each run records tracked, untracked, ignored, Git-ref, process, cache, network, service, and active-task posture applicable to its effects. Pre-existing state is never silently absorbed into a candidate or proof artifact.
4. **No hidden workspace dependency.** Portability runs use an immutable remote source from a clean environment and MUST NOT resolve through a local engineering-core checkout.
5. **Negative evidence retained.** Failures, unknowns, missingness, abstentions, rejected proposals, and counterevidence are first-class inputs.
6. **No authority promotion.** Structural validity, `matched`, owner acceptance, empirical superiority, governance acceptance, release readiness, and publication remain separate facts.
7. **Reproducibility.** Deterministic payloads are run twice from the same ordered inputs and MUST be byte-identical. Timestamped receipt envelopes remain separate from deterministic payloads. Non-deterministic empirical outputs bind seeds/configuration and are replayable to the extent declared by the empirical owner.
8. **Default-deny owner-boundary transfer.** Before transfer to engineering-core, another participant, a reviewer, an empirical owner, or a model/provider, the source owner approves the exact serialized outbound bytes, SHA-256, byte length, named recipients/endpoint/region, purpose, field classification, access, encryption, logging/cache/session behavior, retention/deletion, network route, model/adapter identity, and training use. Non-public payloads MUST NOT be used for provider training. Sent bytes MUST match the approval; raw repository/task snapshots remain owner-local. Responses are untrusted and require classification and redaction before onward transfer.
9. **Bounded custody and privacy.** No secrets or private source payloads are committed here. Each external artifact records owner/controller, classification, storage, readers, retention, digest/size, producer configuration, capture state/time, reviewer, quarantine status, and authority ceiling. Digest alone is not provenance; an authenticated owner attestation or owner-local review is required.
10. **No waivers by aggregation.** A failed required participant or pillar blocks v1.0. A new decision may revise a flawed gate prospectively; it may not relabel failed evidence after results are known.
11. **Independent review.** The artifact producer cannot be the sole reviewer of its own gate. Review authorship, execution role, owner affiliation, conflicts, inputs, and outcome are recorded before closure.
12. **Candidate and state drift restart proof.** Any candidate change creates a new immutable candidate. Any undeclared participant, task, protocol, fixture, case, owner, or release-state drift invalidates the affected run. A predeclared impact matrix determines reruns; no generic reviewed-descendant exception exists.
13. **Machine-decidable gate artifacts.** G0-A2 freezes one versioned gate-envelope schema and per-stage required-field map covering `pass`, `fail`, `blocked`, and `incomplete`; gate/protocol version; candidate assignment; population digest; producer/owner/task; exact inputs, commands, outputs, assertions, counts/denominators, limits, start/end state, failures, missingness, content digests, authority ceiling, and review reference. A G0-A2 template records candidate identity as unassigned and cannot claim `pass`. Each later instance records its lawful stage; `pass` is lawful only when every stage-required assertion is true and no required field is unknown. Narrative summaries are projections and cannot override the payload.
14. **Machine-checkable stage transition.** G0-A2 freezes a versioned transition-template manifest that enumerates every candidate-independent template digest, its lifecycle stage, the exact fields that G0-B may materialize, the deterministic binding algorithm, independent oracle, required reviewer, and invalidation rules. Candidate identity is explicitly unassigned. At G0-B a read-only materializer binds those templates to the exact candidate and emits a separate candidate-bound transition record and instance digests under owner-controlled custody; it never writes them back into the candidate. Materialization may read candidate bytes but MUST NOT execute G1–G4 proof paths or infer an expected result from the system under test. Candidate-dependent expected results are produced by the frozen independent oracle and reviewed before affected execution output is visible. An undeclared placeholder, field change, late oracle edit, or template/instance mismatch invalidates the transition.
15. **Executable conformance membrane.** G0-A2 freezes one versioned, machine-executable gate-conformance entrypoint, its source digest, exact argv, mode contracts, and JSON result schema as candidate-independent protocol artifacts. G0-B proves that the exact candidate contains those bytes. The entrypoint and input manifests are repository-portable and have no home-relative or sibling-workspace dependency. `candidate` mode admits G0-B, `readiness` mode verifies G5 fan-in and approved artifact bytes, and `pre-publish` mode runs in the mutation-performing release path after current remote-state refresh but before public tag or asset upload. Missing inputs, unknown assertions, toolchain drift, nonzero exit, or any non-`pass` result blocks the transition. The validator proves conformance only; it never supplies task, decision, release, or rollout authority.

## Gate G0 — contract, authority, protocol, and candidate freeze

G0 has three ordered checkpoints.

### G0-A1 — accepted-decision membrane

G0-A1 passes only when:

- decision 128 references the final full Git commit and RFC content SHA-256, is accepted as **Model A**, has legal review closure and an ADR, and is linked to active direction `AK.V5.SF01`;
- every required review/synthesis artifact, or its canonical AK attachment envelope, binds that same commit and content digest; an artifact is not required to self-reference the commit that contains it. A path-only reference, `review_pending`, null outcome, missing review track, absent legal closure/ADR, or digest mismatch fails G0-A1;
- `ak direction check` and the decision passport report no unresolved structural issue;
- an AK-native dependency or deferral holds the G0-A1 release task until those conditions pass.

G0-A1 releases only exact engineering-core tasks that author protocols and deterministic harnesses. It authorizes no participant mutation, empirical or gate outcome capture, candidate creation, PASS claim, publication, or rollout.

### G0-A2 — protocol, population, and owner-task admission

After the G0-A1 authoring tasks complete, G0-A2 passes only when:

- the reviewed population manifest and canonical/raw digests exist under the projection ceiling above;
- every participant owner has recorded acceptance of an exact scoped task and declared validation commands, baseline state, evidence custody, reviewers, transfer policy, isolation boundary, rollback boundary, and final proof-workspace posture;
- the empirical owner, owning repository, selection authority, exact owner-local task, evidence custody, transfer policy, and independent reviewer are named;
- the public command, exit-code, schema, catalog-ID, content-lifecycle, support-platform, artifact-name, migration, and removal surfaces are inventoried;
- the G1 oracle schema; G2 candidate-independent fixture templates, expected-result rules, resource bounds, normalization algorithm, threat matrix, and deterministic candidate-materialization rules; G3 prospective protocol, power code, case-cluster manifest, allocations, metrics, thresholds, missingness rules, and analysis code; G4 candidate/pilot/reviewer matrix; and gate-conformance source, mode schemas, negative fixtures, and repository-contained docs/reference check are frozen before any affected output is visible;
- the transition-template manifest labels each artifact as a G0-A2 template or future G0-B instance, records candidate identity as unassigned, and permits no candidate-dependent bytes or expected-result digest to be fabricated at G0-A2;
- an impact matrix maps each candidate or protocol change to mandatory reruns;
- the engineering-core coordination budget is mapped to exact tasks;
- AK dependency edges—not titles, notes, artifact links, or deferral prose—make G0-B depend directly or transitively on every G4-A owner and engineering-core disposition task, and make G5 depend on every G1–G4 production and independent-review task.

Only G0-A2 releases separately owner-accepted G4-A pilot tasks. It does not release G1, G2, G3, G4-B, a candidate, publication, or rollout.

### G0-B — immutable release candidate

After G4-A and accepted convergence implementation complete, G0-B passes only when:

- one `1.0.0` release-candidate commit exists on a non-`main` branch or pull request;
- package version, package `__version__`, root and packaged catalogs, required catalog history, changelog, migration map, exactly one dated v1.0.0 release note, README, support policy, schemas, release workflow, and lockfile are synchronized at that commit, with reviewed paths and SHA-256 digests;
- the candidate contains the frozen gate-conformance entrypoint, stage-transition materializer, their tests/negative fixtures, and a repository-contained docs/reference validation path; clean standalone execution needs no `~/ai-society`, sibling checkout, personal index, or untracked helper;
- a toolchain manifest binds Python, `uv`, build backend, action/container images, installer sources, dependency lock, and every executable build component by immutable version and digest. Candidate proof and publication use that same manifest;
- the actual release workflow invokes `pre-publish` mode before tag creation or asset upload and its tests prove fail-closed behavior for advanced `main`, candidate/tag/build mismatch, pre-existing tag or Release, stale/extra/different artifacts, missing G5 evidence, and toolchain drift;
- the candidate contains a public removal runbook covering policy/docs/pin cleanup, mixed-file ownership, no-op/failure behavior, rollback, and preservation of repo-local authority;
- the read-only stage-transition materializer runs against the exact candidate and G0-A2 templates, permits only declared candidate-assignment and materialization fields, and emits an owner-controlled G0-B transition record plus candidate-bound G2 fixture manifest, raw/canonical digests, and independently determined expected-result digests. Independent review freezes these artifacts before any G2 system-under-test output; neither artifact is written back into the candidate;
- concrete per-participant G1 journey manifests freeze the oracle fields required by G1 below;
- a candidate-bound effect allowlist names and enforces every permitted repository, temporary, cache, process, service, network, credential-helper, and external effect for G0-B and G5, plus before/after inventory, append-only receipts, custody, disposal, and quarantine rules; an absent effect is prohibited;
- candidate preparation produces a complete inclusion map from accepted G4-A content digests to candidate paths/digests and from rejected, reverted, deprecated, or retired outcomes to immutable lineage references for G4-B to verify;
- in a newly created clean checkout with no `dist/`, these commands pass without changing tracked files:
  - `UV_NO_CONFIG=1 uv sync --locked`;
  - `UV_NO_CONFIG=1 UV_LOCKED=1 uv run python scripts/release-local.py verify --version 1.0.0`;
  - the frozen gate-conformance entrypoint in `candidate` mode, including the repository-contained docs/reference check;
  - `git diff --exit-code && git diff --cached --exit-code`;
  - the candidate-bound before/after effect inventory reports no undeclared residue or surviving child process;
- the candidate is available by immutable remote commit for portability runs, while remote `v1.0.0` and its GitHub Release are absent;
- G0-B records the exact candidate, population digest, protocol/template/instance and transition-record digests, effect-allowlist digest, G4 inclusion map, and release-workflow digest that every future gate uses.

**Failure rule:** no convergence implementation begins merely because this RFC exists or its decision-support review completes. G0-A1 may release only engineering-core protocol/harness authoring. G0-A2 may release only separately accepted G4-A pilots. G1, G2, G3, and G4-B proof cannot begin until G0-A2 and G0-B both pass.

## Gate G1 — Dependable Adoption

### Required journeys and frozen oracles

Mutation, failure, removal, and rollback journeys run in a disposable owner-controlled clone or equivalent replica with an independent Git common directory and isolated `HOME`, XDG, temporary, cache, credential, and configuration state. The replica contains no production credentials or endpoints. Network is denied except for manifest-approved immutable fetches whose commit/tree, dependencies, and executable build inputs are digest-bound. A linked worktree is sufficient only for read-only observation.

Before the first run, each G0-B participant journey manifest records for every numbered journey: starting checkpoint/digest; exact argv, cwd, environment, network policy, candidate resolution, and timeout; expected exit code, schema fields/statuses, allowed diff and writes, prohibited effects, validation, recovery operation, ending checkpoint, and artifact name. Invocation, owner approval, or final validation alone is not PASS. The dry-run plan/diff digest reviewed in journey 3 MUST be the input applied in journey 4; drift requires renewed review. An oracle change after evidence capture creates a new protocol revision and restarts affected evidence.

Each positive baseline executes these ten journey categories using the exact participant-selected operation frozen in its manifest:

1. resolve and install or invoke the immutable remote candidate without a local-checkout fallback;
2. retrieve and explain the selected guidance, dependencies, omissions, pilots, and local deviations without hidden workspace context;
3. dry-run the applicable initialization or migration and review the exact proposed plan and diff;
4. apply that exact owner-approved plan while preserving declared deviations and mixed-file ownership;
5. diagnose and scan the resulting adoption without executing undeclared commands, URLs, models, observations, or patches;
6. for existing adopters, upgrade from the recorded prior pin; for the historical clean-slate baseline, repeat the same plan/apply and prove the documented idempotence behavior;
7. separately inject (a) a syntactically malformed pin, (b) a syntactically valid but unavailable immutable commit on a manifest-approved credentialless fixture remote, (c) a malformed policy, and (d) one cancellation/interruption at the first mutation boundary. The malformed pin fails locally before DNS/network, credential-helper, import/build, or mutation effects. The unavailable pin may perform only the approved DNS/network and Git object-resolution operations against the named fixture; isolated configuration disables credential helpers and interactive authentication, and the run fails with its frozen structured status before dependency resolution, import/build, or mutation. Malformed policy fails before consumer-command or mutation effects; interruption leaves no residual process or accepted partial write. Each case recovers without fabricated state or undeclared effect;
8. from a named post-apply v1 checkpoint, roll back in an independent proof branch to the recorded starting posture and pass the frozen rollback validation;
9. from a separate branch of that same post-apply checkpoint, execute the candidate's public removal procedure. Clean-slate removal follows successful application and cannot pass as a no-op. Only proof-introduced or owner-classified engineering-core fields/files may be removed; named runtime and operational-truth surfaces MUST remain intact;
10. restore the G0-B-predeclared final **proof-workspace** posture, validate it, inventory residual tracked/untracked/ignored and external state, then dispose of or quarantine the replica. This does not land participant changes or establish current adoption.

HealthCo is an explicit manifest member only as a negative control at one immutable revision. For every frozen G1/G2 command whose explicit input includes it, G0-B declares the exact versioned schema fields and expected missing/absent values. It counts in completeness reporting, never in the positive-adopter denominator. Its checkout remains read-only, no command executes inside it, and pre/post revision and filesystem receipts MUST match.

### Exact pass threshold

G1 passes only if:

- every frozen assertion and postcondition passes for all ten journey categories and four positive baselines: **40/40 required participant-journeys**;
- the historical `teachingco/wib` run begins from exact commit `316c45747560392fdab03498849652e8d7e94fcb`, under a current TeachingCo task authorizing only the disposable historical replica;
- every command that explicitly includes the negative control returns its frozen missing/absent schema result: **100%**, without mutation or invented denominator membership;
- the malformed-pin, well-formed-unavailable-pin, malformed-policy, and interruption cases are detected at their distinct frozen boundaries before their prohibited effects: **100%**;
- every declared pre-change, post-change, rollback, removal, and final validation succeeds;
- remote-source portability succeeds for all four positive baselines with zero local `git+file` or workspace-checkout resolution;
- there are zero unresolved objective diagnostics, silent deviation losses, undeclared residual effects, authority-loss events, or observed synthetic-secret disclosures across the frozen sink matrix;
- failure and recovery evidence remains owner-local or is exposed to reviewers only through an owner-approved transfer or bounded attested receipt.

Usability timings and operator commentary are retained as descriptive evidence. They cannot compensate for a failed required journey.

## Gate G2 — Federated Interoperation

### Required cross-owner matrix

Before any conformance output, G0-A2 freezes an RFC-8785-canonical candidate-independent fixture-template manifest, its raw/canonical digests, harness version, normalization/comparison algorithm, expected results and digests for candidate-independent fixtures, deterministic candidate-materialization rules, and entrypoint-to-threat matrix. Candidate identity remains unassigned; candidate bytes, candidate-dependent fixtures, and their expected-result digests are not fabricated or inferred at this stage.

At G0-B, after the exact candidate exists but before any G2 system-under-test output is visible, the frozen materializer binds the template to that candidate and emits a separate candidate-bound fixture manifest and transition record. The instance adds the candidate release fixture, raw/canonical digests, and expected normalized results determined through the frozen independent oracle rather than candidate execution. Independent review verifies that only declared transition fields changed. Neither materialization nor review mutates the candidate.

The matrix covers every command, parser, renderer, Git/subprocess call, output path, owner-boundary transfer, and model-response sink. It defines the exact denominator for every count or percentage. The resulting candidate-bound corpus includes:

- released inputs from v0.7.0, v0.8.0, v0.10.0, and the immutable candidate;
- all four positive outputs plus the explicit HealthCo control;
- complete, partial, unavailable, permission-denied, privacy-redacted, stale, and unsupported populations;
- reordered and duplicate identities, unknown future fields, unsupported schemas, and catalog skew;
- malformed/duplicate-member JSON, invalid UTF-8, deep or huge inputs, sparse/growing files, and exact-limit/over-limit cases;
- absolute, empty, dot, dot-dot, overlong, undecodable, traversal, control-character, leading-option, and revision/path-ambiguous names;
- symlinked final components and parents, hard-linked outside-root aliases, FIFO/socket/device files, unreadable parents/files, and unwritable outputs;
- final/parent rename, relink, replacement, same-size/mtime-restored mutation, and output-destination TOCTOU races;
- hostile Git configuration/environment/helpers, ANSI/bidi/terminal controls, Markdown/HTML/table/link injection, URL/tool instructions, and supplied patches or model responses.

The fixture freezes trusted input/output root identities. Every component is no-follow checked; platforms without the required primitive fail closed. Paths are not reopened after validation, concurrent change is rejected, and no symlink, special file, unapproved existing file, partial output, or outside-root destination may be followed or overwritten.

The isolated managed-scratch corpus is bounded to **64 population entries, 2,048 filesystem entries, path depth 16, 1 MiB per file, 16 MiB total, and a 60-second per-command deadman**. The manifest also freezes lower parser nesting/member/string limits, path-component/total bytes, traversal operations, generated-file/stdout/stderr bytes, memory, CPU, subprocess count, deadline start, and process-tree termination behavior. Lower owning-schema limits still apply. Permission probes run without elevation or permission repair. Timeout or cancellation kills the process tree and leaves no accepted partial artifact.

Synthetic secret canaries cover policy values, file/path names, Git metadata, malformed inputs, diagnostics, reports, caches, and every approved request/response. Diagnostics and renderers escape controls and redact unapproved private metadata. Supplied content is data only: it cannot execute tools, fetch URLs, invoke credential helpers, import/build code, or apply patches.

### Exact pass threshold

G2 passes only if:

- every positive baseline produces an owner-local bounded observation at its revalidated task revision;
- at least two positive owner groups independently consume identical approved aggregate bytes and produce results equal under the frozen normalization algorithm;
- deterministic payloads are byte-identical across two runs with the same ordered inputs, and normalized results are invariant only to the explicitly permitted ordering transformations;
- every valid fixture passes and every invalid/unsupported fixture fails at its frozen boundary with structured, bounded, sanitized diagnostics: **100% of the frozen corpus and entrypoint matrix**;
- missing, unavailable, private, stale, and unsupported records remain explicitly incomplete and are never coerced to adopted, healthy, current, or verified;
- duplicate physical identities cannot inflate denominators or evidence counts;
- no command, model, URL, observation reference, supplied patch, Git helper, or hostile content is executed by scan/aggregation paths;
- generated reports and remediation queues remain in the consuming owner scope, and transfers use the exact approved bytes from universal rule 8;
- operation requires no hosted control plane or centrally invented society denominator;
- there are zero observed synthetic-canary disclosures, path escapes, authority promotions, bound overruns, blocking special-file reads, surviving processes, or partial accepted outputs across the frozen matrix.

Any G0-A2 template, normalization rule, bound, sink, oracle, materialization rule, or G0-B candidate-bound fixture/expected result change after the applicable output-visibility boundary creates a new protocol revision and restarts G2.

## Gate G3 — Evidence Calibration

G3 is executed by the exact empirical owner/repository/task admitted at G0-A2. Engineering-core supplies bounded schemas and candidate artifacts; it does not score itself, operate the empirical task, or turn a study result into doctrine, governance, release, or rollout authority. Results support only a conditional comparison over the frozen baselines and task clusters, not ecosystem representativeness or causal claims beyond that design.

### Frozen prospective study

Before **any** static- or evidence-arm output is visible, the empirical owner freezes the sampling frame, independent task clusters, development/confirmatory split, owner-authored arm-neutral rubric, exclusions, fixed weights, prompts/context, model configurations, allocations, executors, review order, stopping rule, scoring environment/code, metrics, thresholds, missingness policy, and transfer bytes. Development-viewed cases are ineligible for confirmatory analysis.

The study contract is:

- The powered confirmatory set contains at least **48 independent evidence-sufficient task clusters**, at least **12 per positive baseline**, and at least **6 per required participant-baseline × model-configuration cell**, or the larger prospectively computed sample. Adding a model configuration therefore adds four required cells and cannot dilute a cell below six. Cases sharing a task/snapshot or near-duplicate mutation form one cluster and do not increase effective sample size.
- A separate safety set contains at least one deliberately insufficient-evidence case in every participant-baseline × model-configuration cell—at least **8** for two configurations. Safety cases do not enter improvement, power, or recommendation-calibration metrics.
- The static plan is generated once, digest-bound, and reused byte-for-byte as the base for both arms. The static arm receives no owner-evidence advice; the evidence arm receives only request-bound provider-neutral advice.
- Both arms run in owner-authorized disposable replicas without a shared branch or production effect. Model configuration is block-randomized within every baseline; allocation satisfies the frozen minimum in every baseline × model cell before output, and cell weights are fixed and balanced. Executor and arm order are randomized or separated under a frozen contamination control so one arm cannot learn from the other's result.
- Reviewers are masked to arm label, forecast, provider/model identity, and owner disposition to the extent technically possible. Masking breaches are recorded, and an objective-validation-only sensitivity result is reported.
- At least **two distinct base-model families/identities** are separately bound, each assigned at least 24 confirmatory clusters and represented in every positive baseline. Prompt, seed, temperature, quantization, endpoint, or adapter variants of one base model do not count as model diversity.

For cluster `i` and arm `a`, `Y[a,i]=1` only when the arm satisfies the same frozen owner constraints, participant validation, and objective claim/patch verification rule; otherwise it is `0`. Evidence use, citations, a stored claim, owner preference, or owner disposition does not itself set `Y`. A win is `(Y[evidence],Y[static])=(1,0)`, a loss is `(0,1)`, and both ties remain in the denominator. The primary estimand `Delta` is the fixed-weight mean of `Y[evidence]-Y[static]` over all intention-to-treat confirmatory clusters, with equal total weight per participant-baseline × model-configuration cell.

The prospective simulation or exact paired-binary power analysis targets the complete decision rule—estimated `Delta >= 0.15` and the 90% lower confidence bound greater than `0.00`—at a separately justified design alternative strictly greater than `0.15`. It declares two-sided `alpha=0.10`, discordance/task-correlation sensitivity, fixed weights, attrition inflation, total and per-cell cluster counts, and the effect of the six-cluster cell floor. There is no optional stopping, outcome-driven top-up, case substitution, or recommendation-level pseudoreplication.

Every evidence-arm confirmatory cluster records one probability in `[0,1]` for its exact `Y` outcome before execution, validation, or review. The protocol freezes weighting, invalid/missing forecast handling, ECE bins `[0.00,0.20)`, `[0.20,0.40)`, `[0.40,0.60)`, `[0.60,0.80)`, `[0.80,1.00]`, empty-bin behavior, a `p=0.5` or disjoint-development reference forecast, bootstrap procedure, and baseline/model reliability tables. Forecasts remain hidden from reviewers.

All frozen clusters remain in the intention-to-treat manifest. Arm-attributable no-output, invalid output, or failed validation is `Y=0`. Unresolved administrative missingness is bounded pessimistically for superiority: missing evidence-arm outcome=`0`, missing static-arm outcome=`1`; forecast missingness receives the frozen worst-case assignment. Missingness is reported by arm, baseline, model configuration, and cluster. Loss of prospective power fails the study rather than authorizing replacement.

Owner dispositions, validation results, empirical outcomes, forecasts, receipts, and governance decisions remain separate records. Every transfer uses universal rule 8, including SDK-injected context/metadata, telemetry, redirect/fallback behavior, and destination region; default-deny egress records request/response digests without private payloads.

### Exact pass threshold

G3 passes only if:

- every frozen confirmatory and safety cluster is reported at cluster level, including negative and missing outcomes;
- estimated `Delta` is at least **0.15**, and the lower bound of the predeclared **90% task-cluster bootstrap interval** is greater than `0.00` under the pessimistic missingness bound;
- effects are reported for every participant-baseline × model-configuration cell and for each marginal baseline/model stratum. A point estimate below **-0.05** in any required cell or marginal stratum is a predeclared harm stop, not a statistical claim of non-harm; aggregation cannot waive a cell stop;
- the evidence-arm forecasts have an upper 90% bootstrap bound of **Brier score <= 0.20** and **ECE <= 0.15**, plus positive Brier skill against the frozen reference;
- every insufficient-evidence safety case emits machine-checkable `abstain` or `unknown`, with recommendation, patch, command, work-bundle, and every other actionable field absent: **100%**;
- there are zero observed synthetic-canary disclosures, invalid citations, unbound patches, owner-identity mixups, unauthorized transfers, production effects, or authority promotions across the frozen matrix;
- the empirical owner publishes a bounded result, replay/configuration receipt, limitations, masking breaches, exclusions, missingness, and counterevidence reference;
- an independent reviewer confirms that the freeze preceded all arm outputs and that cases, allocations, exclusions, forecasts, metrics, transfer policy, and stopping rules did not change after visibility.

Failure of power, either primary boundary, a harm stop, calibration, safety, transfer controls, or prospective integrity leaves G3 failed. A revised protocol requires an accepted decision revision and fresh held-out corpus; failed studies remain in lineage.

## Gate G4 — Review-Governed Evolution

### Authority split

Participant owners authorize only their local proposal, pilot, evidence, rollback, and disposition. They cannot transition shared engineering-core content. The engineering-core content owner alone may accept, reject, revise, deprecate, retire, or promote shared content under an exact engineering-core task, accepted decision where required, and repository validation. Validation, participant disposition, content-owner transition, package distribution, and adoption are separate facts.

### G4-A — pre-candidate lifecycle execution

After G0-A2, each positive owner group originates one substantial shared-content candidate under exact owner tasks, for **three total candidates**. Before pilot output, the frozen G4 matrix names each candidate, origin group, pilot groups, exact owner/content-owner tasks, reviewers/conflicts, content and protocol digests, success/harm/falsification criteria, compatibility consumer, expiry/review event, rollback checkpoints, and permitted transfer.

A full cycle is:

```text
proposal record
  -> opt-in bounded pilot
    -> evidence and counterevidence
      -> participant-local disposition
        -> engineering-core content-owner decision
          -> rollback/expiry/final state with preserved lineage
```

Every candidate includes the minimum decision record from `docs/content-lifecycle.md`. Participant evidence binds exact pilot revisions/content digests and never changes shared state by itself. For this proof, independent contexts means distinct positive **owner groups**, not repositories, lanes, worktrees, operators, or artifacts; TeachingCo's two baselines count as one owner context and engineering-core is not participant evidence. Ordinary pilot-to-stable promotion requires evidence from at least two distinct positive owner groups, including one other than the originator, under separate exact tasks. The narrow emergency exception cannot satisfy the required G4 promotion outcome.

All participant pilot mutations, content-owner decisions, accepted shared-content landings, and rejected/deprecated/retired history complete before G0-B. G0-B contains the final accepted G4-A state and immutable lineage references.

Across the three outcomes, the set MUST include four distinct observations:

- one engineering-core content-owner promotion to stable or accepted stable revision after the distinct-owner gate;
- one separate content-owner rejection of a proposal/pilot, or deprecation/retirement of previously stable guidance; expiry, deselection, reversion, and technical rollback do not count;
- one material revision, split, or scope narrowing with before/after digests and cited causal counterevidence;
- one separately exercised rollback from explicit pilot selection to the exact prior stable selection without erasing history.

A candidate may satisfy more than one category only when the underlying transition/evidence is independently present; the rejection/retirement and rollback observations MUST remain distinct. These requirements do not authorize or coerce an outcome. If the evidence does not naturally support the required set, G4 remains incomplete. Additional candidates require a prospective accepted protocol revision before their pilot evidence is visible; prior results remain in lineage.

### G4-B — post-candidate verification

After G0-B, G4-B is non-mutating verification. It checks the exact candidate's inclusion map from every accepted G4-A digest to its candidate path/digest and from every rejected, reverted, deprecated, or retired outcome to preserved immutable lineage. It reproduces compatibility, rollback, and participant-validation evidence without changing the candidate. A defect requiring content/code change creates a new candidate and invokes the impact matrix.

### Exact pass threshold

G4 passes only if:

- all three candidates preserve problem, audience/scope, invariant, load triggers, strongest alternative, evidence, counterevidence, falsification, compatibility/migration, rollback, review trigger, retirement signal, and semantic references where applicable;
- each pilot is opt-in, bounded, expires or reaches a named review event, and cannot silently become default;
- participant validation result, participant disposition, content-owner transition, AK authority reference, distribution status, and adoption status are separate fields;
- every shared transition is recorded by the engineering-core owner surface and linked to immutable, owner-attested evidence; participant/model/loop output cannot perform it;
- accepted changes landed before G0-B only through exact engineering-core tasks and complete repository validation; G4-B performs no mutation;
- stable catalog/docs/package projections are synchronized, while rejected, retired, superseded, and negative material remains historically interpretable;
- an older supported consumer receives compatible behavior or the frozen structured migration/downgrade result;
- all participant validations pass after final disposition and after the separately exercised rollback;
- there are zero unowned defaults, irreversible migrations, erased negative results, or automatic promotions.

## Gate G5 — cumulative v1 release readiness

G5 is an evidence fan-in over the exact G0-B commit. It is not a release command or release authority.

It passes only if:

1. G0, G1, G2, G3, and G4 each have a PASS artifact and independent review with no open blocker;
2. every artifact binds the same candidate and population digest, and AK dependency edges show every required production/review task complete; a title, note, cleared deferral, or unattached artifact cannot substitute for an edge;
3. candidate proof runs twice in distinct newly created standalone checkouts at the exact candidate. Each initially lacks `dist/`, runs inside an isolated boundary enforcing the candidate-bound effect allowlist, and records a before inventory of tracked/index/untracked/ignored state; declared temporary, cache, configuration, HOME, and output roots; process tree and services; network policy/endpoints; and other approved external destinations. Each then passes:
   - `UV_NO_CONFIG=1 uv sync --locked` under the frozen toolchain manifest;
   - the validation commands in `AGENTS.md`;
   - `UV_NO_CONFIG=1 UV_LOCKED=1 uv run python scripts/release-local.py verify --version 1.0.0`;
   - the frozen repository-contained docs/reference check and gate-conformance entrypoint in `candidate` mode;
   - `git diff --check v0.10.0..."$CANDIDATE_SHA"` and clean tracked/index checks;
   - a same-boundary after inventory and enforcement receipt with no undeclared repository, temporary, cache, process, service, network, credential-helper, or external effect; every allowed residue records path/type, owner, digest or bounded identity, custody, and disposition, and no child process survives;
4. each build produces exactly `engineering_core-1.0.0-py3-none-any.whl` and `engineering_core-1.0.0.tar.gz`; extra wheel/sdist files fail. `SHA256SUMS` is generated from those explicit names, both builds are byte-identical, and the artifact bytes, manifest bytes, SHA-256 values, custody location, toolchain digest, and effect-inventory digests are recorded in G5. After comparison and custody transfer, allowed transient residue is disposed of or quarantined according to the manifest and a final disposal inventory is retained;
5. the candidate-head and pull-request merge-test SHAs are both recorded; `CI / required` passes on the merge-test SHA as integration evidence, including Ubuntu Python 3.10–3.13 and rolling Arch installed-wheel lanes, without being mislabeled as candidate-SHA evidence;
6. exactly one recorded release-note path, the migration map, README, support policy, changelog, catalogs, schemas, release workflow, and built artifacts tell the same v1 story and match their G0-B digests;
7. all four positive baselines install the exact remote candidate and every command including the untouched negative control returns its frozen result;
8. the AK decision passport, direction check, task closure checks, evidence/counterevidence, rollback record, transition records, protocol/template/instance digests, artifact and effect manifests, and rerun obligations are complete;
9. a final independent review confirms the candidate/population identities, stage transitions, gate fan-in, residual-effect accounting, release-state controls, and truthful status language;
10. after all preceding inputs exist, the candidate-contained gate-conformance entrypoint runs in `readiness` mode and returns `pass` while independently checking their exact digests, required fields, transition records, effect inventories, toolchain identity, artifact set, and release-workflow conformance.

A G5 PASS is evidence only. It does not authorize or perform a merge, push, tag, publication, rollout, external-task closure, or v2 definition.

### Separate release action and publication verification

After G5 PASS, a separate exact engineering-core release task—claimed by the authorized release owner and explicitly approved by the operator for the recorded candidate SHA and current remote-main SHA—may open one serialized release window. Immediately before mutation it refetches `main` and tags, proves remote `v1.0.0` and its GitHub Release are absent, rechecks the approved candidate and remote-main identities, and confirms remote `main` is an ancestor of the candidate. Any tag/Release, advanced or changed `main`, merge/rebase/squash result, different candidate, or inability to serialize is a hard stop, not a resumable shortcut.

The release action performs only the approved exact-SHA fast-forward. After exact main CI succeeds, the mutation-performing automation MUST invoke the candidate-contained gate-conformance entrypoint in `pre-publish` mode before public tag creation or asset upload. That mode requires equality—not ancestry—among the G0-B candidate, triggering main-CI head, current `origin/main`, release `build_sha`, and proposed peeled-tag target; proves the remote tag/Release are absent; and verifies the frozen toolchain.

Publication either consumes the exact G5-approved artifact bytes or rebuilds under the identical toolchain and compares each artifact plus `SHA256SUMS` byte-for-byte with G5 **before** creating the tag. Any mismatch blocks both tag and upload. An existing tag may never redirect the build. Manual/local tag fallback is prohibited for v1.0.0 unless a separate exact-SHA task and the same pre-publish proof explicitly authorize it. Downstream rollout remains separately owner-authorized.

A dependent post-release task downloads into an empty directory and requires exactly the approved wheel, sdist, and `SHA256SUMS`. It compares the downloaded manifest and artifacts byte-for-byte with G5 before `sha256sum -c`, and confirms candidate, main-CI head, current main, release build, peeled tag, release notes, and asset identities. This is confirmation of the pre-publish membrane, not the first mismatch detector. Only then may status say **published-and-verified**.

Release states are explicit:

1. **candidate:** isolated and reversible before the main update;
2. **release-blocked:** main updated but no public tag; freeze release and rollout, then use an explicit revert or a new candidate with impact-matrix reruns;
3. **tag-created-release-absent:** public version identity exists and is the lineage point of no return. Never retarget, reuse, or silently delete the tag as ordinary rollback; an incident decision must preserve lineage;
4. **published-verification-pending:** the GitHub Release exists, but rollout remains prohibited;
5. **published-and-verified:** the post-release identity and G5-manifest checks pass.

A verification failure preserves the exact reached state, stops rollout, notifies owners, quarantines affected copies, and requires an explicit corrective-release, completion, or withdrawal decision. Security removal of assets preserves their digests and incident lineage and never permits tag reuse.

## Rollback and stop rules

- Rejection of this RFC leaves `v0.10.0` as the latest stable product and archives/defer-closes dependent tasks without rewriting evidence.
- Before the exact release action, a failed candidate remains isolated; fixes create a new candidate and impact-matrix reruns.
- A G1 failure restores or quarantines the disposable replica and preserves owner-local failure evidence; Git rollback is not claimed to reverse network, cache, process, service, or provider effects.
- A G2 failure withholds the incompatible aggregate path; owner-local source records remain untouched.
- A G3 failure leaves evidence-informed advice advisory/experimental and cannot be reframed as governance success.
- A G4 failure keeps candidates in their evidence-supported lifecycle states and restores the exact prior stable selection where rollback applies.
- Participant withdrawal invalidates the population digest and invokes the accepted prospective replacement process.
- Secret-canary disclosure, unauthorized transfer/execution/egress, permission bypass, path escape, fabricated evidence, silent substitution, deadman failure, surviving process, undeclared external effect, or authority promotion is an immediate stop.
- Incident recovery requires owner-led blast-radius assessment, notification, rotation/deletion requests where applicable, artifact invalidation/quarantine, compensating restoration, root-cause correction, affected-gate/protocol revision, required reruns, and independent closure. Irrecoverable transferred bytes are never described as rolled back.
- Expected negative fixtures count only at their frozen boundaries. Visible-loop, peer, and subagent work stops on task-scope drift, unresolved pre-existing changes, unexpected validation failure, or inability to bind proof to the exact owner task.

## AK execution shape

The intended authority graph is:

```text
RFC adversarial review + decision-support synthesis
  -> owner acceptance, ADR, immutable RFC binding (G0-A1)
    -> engineering-core protocol/harness authoring
      -> population, owner/empirical tasks, protocols, dependency admission (G0-A2)
        -> G4-A owner pilots + engineering-core dispositions
          -> immutable 1.0.0 candidate (G0-B)
            -> G1/G2/G3 + non-mutating G4-B
              -> cumulative G5 readiness evidence
                -> separate exact release task
                  -> dependent post-release verification task
```

The G0-A1 release task cannot complete until accepted decision/ADR and immutable review closure exist. G0-B depends directly or transitively on every exact G4-A owner and content-owner task. G5 depends on every exact G1–G4 production and review task. Deferrals remain active until those edges exist; clearing a deferral cannot waive fan-in. Cross-repository tasks are created only in their owning repositories after exact owner acceptance; they are never shadow tasks in engineering-core.

## Visible-loop budget

Ten is a maximum **engineering-core coordination** review/implementation budget, not one broad `--count 10` invocation and not a cap on owner proof:

| Iteration budget | Bounded use |
|---:|---|
| 1 | Adversarial RFC review and decision-support synthesis |
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

1. Are the three positive owner groups and four participant baselines meaningfully independent, fit for the explicitly conditional proof scope, and feasible without central execution authority?
2. Are 40/40 adoption journeys and the frozen federation/resource corpus strict enough to prevent proxy success while remaining executable?
3. Does G3 define one coherent task-cluster estimand, adequate power, model diversity, calibration target, and preventive data-transfer membrane?
4. Do the G4 authority split and outcome requirements force real cross-owner promotion, rejection/retirement, and rollback evidence?
5. Are any commands, schemas, participant payloads, or owner decisions being absorbed into engineering-core improperly?
6. Can every gate fail visibly, contain an incident, and roll back without weakening the product's public authority boundaries?
7. Does the branch/PR-to-automatic-release sequence preserve exact-candidate proof and explicit operator control?
8. Does any wording imply v1 is current, accepted, released, or scheduled before the cumulative gate and explicit release action?
