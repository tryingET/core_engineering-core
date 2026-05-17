---
summary: "Cross-language performance discipline for budgets, profiling, benchmark hygiene, regression gates, and evidence."
read_when:
  - "Work makes or affects latency, throughput, frame-rate, memory, startup, build-time, GPU, cost, or scalability claims."
  - "A repo adds benchmarks, profiles, performance budgets, regression gates, or optimization work."
type: "guide"
---

# Discipline — Performance

## Purpose

Performance guidance owns cross-language invariants for budgets, measurement, profiling, benchmark hygiene, regression gates, and claims. Lanes choose profilers, benchmark harnesses, browser tooling, runtime flags, and command syntax.

Performance work is evidence work. Optimization without a measured bottleneck is speculative unless the change is a small, obvious removal of waste with no added complexity.

## Load when

Load this discipline when work touches:

- latency, throughput, frame rate, memory, startup time, CPU/GPU utilization, bundle size, binary size, or cost
- benchmarks, profiling, load tests, flamegraphs, browser performance, GPU measurements, or regression gates
- service SLOs, frontend interaction budgets, CLI responsiveness, import/startup cost, model inference speed, or build/test time
- claims such as faster, scalable, real-time, low-latency, lightweight, memory-efficient, or production-ready under load

Do not load it for routine code changes with no material performance claim or budget impact.

## Decision rules

Performance guidance applies to claims and budgets, not every local cleanup. Choose the level of evidence by risk:

- local optimization: benchmark or profile the affected path; no broad product claim
- regression prevention: stable budget/gate or tracked metric for a known risk
- product/runtime claim: representative workload, representative environment, and comparison to baseline
- capacity/cost decision: load/soak/cost evidence plus operational assumptions

Do not add complexity for a theoretical speedup unless the bottleneck is measured or the simplicity win is independently valuable.

## Budget rule

A performance budget is a contract, not a vibe. Name:

- metric: p95 latency, max frame time, memory peak, startup wall time, throughput, GPU occupancy, bundle size, cost per job, etc.
- scope: endpoint, screen, command, kernel, job, import path, workflow, or build target
- environment: device/browser/runtime/hardware/data shape/concurrency/data distribution
- threshold: target and failure threshold
- measurement command or dashboard
- owner and review/exception path

If the environment or workload is not named, the number is not portable.

## Profiling before optimizing

Default sequence:

1. State the user/runtime symptom or budget at risk.
2. Measure a representative path.
3. Identify the bottleneck with a profiler, trace, or structured timing.
4. Change the narrowest high-leverage code/config/path.
5. Re-measure the same scenario and report the delta.
6. Add a regression gate only when the metric is stable enough to automate.

Skip directly to implementation only for trivial removals of accidental waste, and still avoid broad claims without measurement.

## Benchmark hygiene

Benchmark reports should include:

- exact command, git revision, artifact/build type, dependency/tool versions, and relevant config
- hardware/OS/runtime/browser/GPU/driver/toolkit details when they affect results
- input sizes, data distribution, concurrency, warmup, repeat count, and summary statistics
- whether setup, IO, allocation, network, host-device transfer, cache warming, and teardown are included
- machine-readable output when tracked over time
- baseline comparison and confidence/variance notes where practical

Never report a single fastest run as truth.

## Frontend budgets

Frontend performance usually needs both lab and interaction evidence:

- preserve frame budget: 60 Hz implies about 16.7 ms/frame; leave room for browser/layout/paint, so long JS tasks should be much shorter
- avoid main-thread model/media/data work; use Workers or incremental scheduling when user interaction can jank
- track input latency for critical interactions, not only page load
- watch bundle size, hydration/startup time, route transition time, media/model asset load time, and memory growth
- test on representative low/mid target devices or throttled profiles, not only a developer workstation
- include accessibility-compatible reduced-motion behavior when animation is performance-sensitive

Cross-reference `observability` for field signals and `validation` for browser/E2E evidence.

## Backend/service budgets

Backend performance budgets should distinguish:

- request latency: p50/p95/p99, timeout, and error rate
- throughput/capacity: concurrency, queue depth, saturation, and backpressure
- dependency latency: database, cache, external APIs, model inference, filesystem, object store
- background jobs: enqueue-to-start age, execution time, retries, and dead-letter rate
- cold start and deploy readiness time
- resource use: memory, file descriptors, connections, CPU, GPU, and cost

Do not optimize p50 while p99, retries, or saturation are the real user problem.

## Memory and startup time

Memory/startup regressions deserve first-class treatment when they affect CLIs, browser apps, services, native tools, tests, or serverless/edge deployments:

- measure peak and steady-state memory separately
- separate import/module load, initialization, asset/model load, network warmup, and first useful response
- track leaks with long-enough runs, not only short unit tests
- keep large assets lazy or explicit when startup matters
- avoid caching that converts latency into unbounded memory growth

## GPU measurements

GPU evidence must state:

- GPU model, driver, toolkit/runtime, precision/dtype, shapes, batch sizes, streams, and build flags
- warmup and synchronization policy
- whether timings include host-device transfer, allocation, preprocessing, framework dispatch, and postprocessing
- CUDA events or appropriate device timing for kernel/device work
- profiler evidence for kernel-level claims and integrated application evidence for product claims

Standalone kernel speedups do not prove end-to-end user or service improvement. Cross-reference `engineering-cpp.cuda.md` and `ai-ml` when applicable.

## Regression gates

Add automated performance gates only when the signal is stable and cheap enough to keep green:

- prefer budget checks on deterministic units, bundle size, startup smoke, or stable benchmark subsets
- use trend dashboards or scheduled runs for noisy load/GPU/browser benchmarks
- fail CI on large/clear regressions; warn and record for noisy metrics until variance is understood
- keep gate thresholds documented and reviewed; stale thresholds are worse than no gate
- store machine-readable results or links, not only screenshots

Performance gates complement correctness gates; they do not replace tests.

## When microbenchmarks mislead

Microbenchmarks are useful for tight algorithms, parsers, serialization, kernels, allocators, and known hotspots. They mislead when:

- the production bottleneck is IO, network, database, layout, scheduling, cache misses, or contention
- inputs are tiny, uniform, hot-cache, or shaped differently than real data
- setup/allocation/transfer is excluded but dominates reality
- compiler/runtime optimizations remove the measured work
- a local kernel/function improves while downstream integration gets slower or more complex

Use microbenchmarks to explain a hotspot, not to make broad product claims.

## Cross-references

- `observability` owns runtime signals, dashboards, traces, profiles, health, and SLO evidence.
- `validation` owns command tiers and handoff evidence.
- `testing` owns correctness tests; performance tests do not prove correctness.
- `service-api` owns service latency/readiness/rollback context.
- `ai-ml` owns model quality/latency tradeoffs and eval evidence.
- `data-governance` owns data shape, lineage, quality, and representativeness for benchmark/evidence datasets.
- `domain-modeling` owns the product/domain meaning of "fast enough" for workflows and state transitions.
- `build-graph-acceleration` owns build/test-time acceleration decisions.

## Validation expectations

For performance-affecting changes, report:

- baseline and after measurements, or why baseline is unavailable
- command/environment/workload used
- representative artifact/build mode
- whether the result supports a local optimization, regression prevention, or product/runtime claim
- follow-up gate/dashboard if the budget is durable

## Failure modes

- Optimizing code that profiling never identified as hot.
- Claiming "fast" from a local happy-path run without workload, hardware, or variance.
- Treating microbenchmarks as product evidence.
- Improving p50 while p99/user-perceived latency regresses.
- Moving work off the request path into an invisible queue with no backlog/age budget.
- Browser feature works on a workstation but janks on target devices.
- Benchmark data is tiny, clean, hot-cache, or unrepresentative of the domain workload.
- GPU timing omits synchronization or transfer cost.
