---
summary: "Cross-language AI/ML discipline for model assets, inference boundaries, evals, provenance, safety claims, and reproducibility."
read_when:
  - "A repo trains, evaluates, serves, embeds, downloads, packages, or calls ML/AI/LLM models."
  - "Work changes datasets, prompts, model versions, inference runtime, browser ML, GPU acceleration, safety/privacy claims, or eval evidence."
type: "guide"
---

# Discipline — AI/ML

## Purpose

AI/ML guidance owns cross-language invariants for model behavior, assets, datasets, prompts, inference boundaries, evals, privacy, safety claims, and reproducibility. It applies whether the implementation is Python, TypeScript/browser ML, C++/CUDA kernels, Rust/Go services, Elixir orchestration, or LLM/tooling repos.

Language lanes choose frameworks, package managers, GPU build flags, browser APIs, serving libraries, and concrete commands. This discipline decides what must be true before AI/ML behavior is trusted or claimed.

## Load when

Load this discipline when a repo does any of the following:

- trains, fine-tunes, distills, quantizes, converts, downloads, caches, embeds, or ships model assets
- runs local, browser, edge, server, batch, GPU, or hosted inference
- calls LLMs, agents, tools, retrieval, rerankers, embeddings, classifiers, recommenders, or computer-vision/audio models
- changes prompts, system instructions, model routing, decoding parameters, safety filters, tool schemas, or evals
- stores datasets, labels, traces, model outputs, human feedback, or benchmark/eval reports
- makes quality, safety, performance, medical, legal, security, productivity, or automation claims based on model behavior

Do not load it for ordinary deterministic code just because a human used an AI assistant to write it.

## Decision rules

AI/ML guidance applies when probabilistic/model behavior becomes part of the product, runtime, evidence, or automation contract. It does not apply merely because a repo contains generated code or because an agent assisted implementation.

Use deterministic code instead of AI/ML when:

- the rule is known, stable, and cheaply expressible
- correctness is more important than fuzzy recall or generation quality
- failure cannot be safely detected, bounded, reviewed, or rolled back
- the model would only obscure a simple schema, parser, search, ranking, or rules problem

Use AI/ML only when model behavior earns its uncertainty cost: ambiguous inputs, perception/language tasks, ranking/recommendation, compression of messy examples, or workflows where evals and fallback can bound harm.

## Model asset invariants

Model assets are build/runtime artifacts with provenance, compatibility, and risk:

- record source, license/terms, checksum or immutable revision, expected format, and intended runtime
- keep large binary assets out of source unless repo policy explicitly allows them
- define download/cache path, offline behavior, eviction, and integrity checks
- version conversions, quantization, pruning, adapters, tokenizer/vocabulary files, and preprocessing steps with the model
- document hardware/runtime constraints: CPU/GPU, browser APIs, CUDA/toolkit/driver, memory, precision, batch/shape limits
- provide fallback/degraded behavior when the asset is missing, incompatible, slow, or unavailable

A model file without provenance is an unreviewed dependency.

## Inference/runtime boundaries

Every inference boundary should name:

- caller contract: input schema, preprocessing, output schema, confidence/score semantics, and error/degraded states
- runtime contract: local/browser/server/hosted, CPU/GPU, concurrency, batching, timeout, cancellation, and resource limits
- privacy contract: what user data leaves the process/device/browser/org, what is logged, retained, or used for improvement
- safety contract: claims made, claims not made, escalation/handoff behavior, and known unsafe cases
- observability contract: latency, errors, model/version/prompt identifiers, quality counters, and redacted traces

Do not let a prompt string, notebook cell, or vendor SDK call be the only boundary definition.

## Dataset and label provenance

Datasets are governed data, not loose test fixtures. Cross-reference `data-governance` for authority, lineage, lifecycle, retention, quality, and privacy. Datasets require evidence before they justify behavior claims:

- source, license/consent, collection date, sampling method, known biases, and allowed use
- schema/version, splits, deduplication, leakage checks, and label provenance
- preprocessing pipeline and deterministic regeneration path where practical
- privacy classification and retention/deletion policy
- train/eval/test separation; do not tune on the reported test set
- human feedback instructions and reviewer agreement/quality posture when labels are subjective

Generated/synthetic data must be labeled as such and cannot silently stand in for real-world coverage.

## Prompt, model, and version tracking

For LLM/tooling systems, track enough to reproduce or explain behavior:

- model/provider/runtime identifier and version/date where available
- prompt/system/developer/tool schemas and retrieval corpus version
- decoding parameters, tool-choice policy, guardrails, and routing logic
- evaluation dataset version and scoring rubric
- migration notes when changing models, prompts, context windows, embeddings, or tool contracts

Treat prompts and tool schemas as executable contracts. Cross-reference `specification-and-dsls` when prompt/tool/file formats become implicit DSLs.

## Evals and evidence

Evals are the AI/ML equivalent of tests plus measurement. Choose them by claim:

- deterministic correctness: golden cases, schema/property checks, differential tests, reference implementations
- model quality: held-out sets, rubric-scored examples, pairwise comparisons, human review where needed
- safety/privacy: adversarial prompts, disallowed-content probes, PII/secret leakage checks, jailbreak/tool misuse cases
- regression: fixed eval suites run before model/prompt/routing changes ship
- production behavior: sampled redacted traces, user feedback, incident review, latency/error trends

Do not claim "better" from anecdotes, cherry-picked examples, one-off demos, or benchmark sets that were used to tune the change.

## CPU/GPU/browser fallback

AI/ML features need an explicit degradation plan:

- CPU fallback when GPU/CUDA/WebGPU/WebGL is unavailable, unless product requirements forbid it
- browser fallback for unsupported APIs, low memory, denied permissions, worker failure, or model download failure
- timeout/cancellation for slow inference and background model loading
- smaller model/quantized mode when quality tradeoff is accepted and documented
- clear user/product behavior when the feature is unavailable rather than silently failing

Cross-reference `performance` for latency/memory/startup budgets and `engineering-cpp.cuda.md` for CUDA/GPU evidence.

## Latency/quality/resource tradeoffs

AI/ML choices are usually tradeoffs, not universal upgrades. Record the chosen balance when changing:

- model size, quantization, precision, context length, retrieval depth, batch size, or decoding parameters
- local vs hosted inference
- synchronous vs background inference
- cache behavior and staleness
- quality threshold vs latency/cost/memory/privacy

Performance evidence must use realistic inputs and deployment hardware. Quality evidence must match the claim and user population.

## Privacy and safety claims

- Minimize user data sent to hosted models; disclose and gate sensitive flows.
- Redact secrets/PII in prompts, traces, logs, eval fixtures, and screenshots unless explicitly approved for that evidence store.
- Do not train, fine-tune, or retain user data without an accepted policy and consent/legal basis.
- Never imply medical, legal, financial, security, or employment decision accuracy beyond validated product claims.
- Keep human override/escalation behavior explicit where model error can harm users or systems.

Cross-reference `security-privacy` for data classification and `service-api` when inference is exposed as a service.

## Reproducibility

The required reproducibility level depends on the claim:

- product inference: reproduce artifact identity, prompt/model/config, runtime, and validation evidence
- research benchmark: reproduce data split, environment, seed, hardware, command, metrics, and result parsing
- safety claim: reproduce probes, policy/rubric, failure thresholds, and review disposition
- release claim: reproduce artifact provenance, checksums, changelog, and rollback path

When exact reproducibility is impossible because of hosted nondeterminism or vendor changes, state that limitation and rely on regression evals plus runtime monitoring instead of pretending determinism.

## Cross-language mapping

- Python often owns training/eval/prototyping; keep notebooks from becoming the only authority.
- TypeScript/browser ML owns permissions, asset loading, Workers, WebGPU/WebGL/WASM degradation, UX, and privacy disclosure.
- C++/CUDA owns kernels, native extensions, device correctness, profiler evidence, and hardware-specific claims.
- Rust/Go services own inference boundaries, resource limits, deployment, and SLOs.
- LLM/tooling repos own prompt/tool schema versioning, eval suites, trace redaction, and safety claims.

The invariant is the same: model behavior must have provenance, a typed/trusted boundary, evidence matched to claims, and an honest fallback/rollback story.

## Validation expectations

Before shipping material AI/ML changes, collect the smallest truthful evidence set:

- asset provenance/checksum or immutable model/provider identifier
- eval/test results tied to the changed model/prompt/runtime/config
- latency/memory/startup evidence on representative hardware when user/runtime experience is affected
- privacy/safety review when sensitive data, automation, or high-impact claims are involved
- rollback/fallback plan for model, prompt, route, asset, or vendor failure

Use `validation`, `testing`, `observability`, `performance`, `security-privacy`, `release-package`, `data-governance`, `domain-modeling`, and `documentation` as applicable.

## Failure modes

- A demo transcript becomes a quality claim.
- Model/prompt changes ship without eval fixtures or version identifiers.
- Browser ML blocks the main thread or fails on unsupported hardware without degraded UX.
- GPU benchmarks omit synchronization, warmup, hardware, precision, or downstream integration evidence.
- Hosted model calls leak user secrets through prompts, logs, traces, or vendor retention.
- Safety language says "will" when evidence only supports "may" or "best effort".
- Model output crosses into a domain decision without a named policy, threshold, escalation path, or invariant boundary.
- Dataset leakage or prompt tuning contaminates the reported eval set.
