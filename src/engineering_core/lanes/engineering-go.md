---
summary: "Go engineering lane for ecosystem-specific tooling, commands, and implementation defaults."
read_when:
  - "Working in a repo or package whose selected engineering-core lane is go."
  - "Choosing Go tooling, command surfaces, quality defaults, or ecosystem-specific validation."
type: "guide"
---

# Go lane — modules, CLIs, services, and low-latency backends

Use this lane when Go is the requested implementation language or when simple static binaries, concurrency, low operational overhead, or network-service performance make Go the best fit.

## Baseline toolchain
- **Toolchain / module system:** stable Go toolchain pinned by the `toolchain` line in `go.mod` + modules
- **Format:** `go fmt ./...` (fixer; it rewrites files and always exits 0) or `goimports -w` where imports need management; the gate is the `fmt` check below
- **Analysis:** `go vet ./...`
- **Typecheck/build:** built-in compiler via `go test ./...` and `go build ./...`
- **Module integrity:** `go mod tidy -diff` plus `go mod verify`; keep `go.sum` committed. `go mod verify` only checks the module cache against recorded hashes and passes even with a missing `go.sum`; `go mod tidy -diff` fails on missing, stale, or unused requirements.
- **Testing:** stdlib `testing`; built-in fuzzing when useful, one package at a time with a time bound: `go test -run='^$' -fuzz='^FuzzX$' -fuzztime=30s ./pkg` (without `-fuzztime` it runs until killed; `-fuzz` rejects multiple packages)
- **Template/rendering:** stdlib `text/template` / `html/template` by default

## Optional service defaults
Use these only when the repo is actually a service/backend that needs them:

- **Web/API:** Chi or Gin
- **Data:** PostgreSQL • sqlc (compile-time SQL) or GORM
- **Async/Jobs:** Asynq (Redis) or NATS JetStream
- **Contracts:** OpenAPI (REST), AsyncAPI (events)
- **Observability:** OpenTelemetry Go SDK → OTel Collector → Prometheus/Grafana + Jaeger/Tempo
- **Security:** OIDC; secrets manager; SAST/dep/container scans
- **Deployment:** Static binaries in Docker; Fly.io/Render/Cloud Run or k8s later

## Code quality and supply-chain guidance
- Prefer the Go standard toolchain before third-party tools.
- Use `golangci-lint` or `staticcheck` only when the repo pins and documents a reviewed invocation path. The lane's reviewed path is `go install` of an exact version (the **Tool install** block below) plus a checked-in `.golangci.yml`; validate config changes with `golangci-lint config verify`.
- Avoid curl-pipe-shell or unreviewed installer scripts for lint/tools.
- Keep `go.sum` committed and review new transitive modules in code review.
- Prefer repo-local scripts/CI wrappers for third-party tools so agents do not rely on ambient global installs.

## Testing / rendering guidance
- Default unit/integration runner: stdlib `testing`
- Property/fuzz testing: built-in fuzzing via `go test -fuzz`
- Race testing: use `go test -race ./...` for concurrency-heavy repos where runtime cost is acceptable; it requires cgo (`CGO_ENABLED=1`)
- Behavior/Gherkin testing: `godog` only when executable workflow scenarios materially improve shared understanding
- Template rendering: stdlib `text/template` / `html/template` by default; use `templ` only when typed HTML/component ergonomics justify extra tooling
- Prefer the smallest deterministic surface that proves the contract


## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers and test-form choices.
- `dependency-governance` and `security-privacy` for modules, tool installs, secrets, and supply chain.
- `service-api` for service boundaries, request/response contracts, auth, idempotency, jobs/events, migrations, deployment, and rollback.
- `observability` for services, CLIs with runtime evidence, and benchmarks.
- `performance` for latency/throughput/memory/startup budgets, profiling, and regression gates.
- `ai-ml` when Go services host, route, or wrap model inference/LLM/tooling behavior.
- `data-governance` for canonical data, schemas, identifiers, lineage, migrations/backfills, projections, retention, and quality.
- `domain-modeling` for vocabulary, invariants, workflows, state transitions, and anti-corruption boundaries.
- `design-patterns` when reviewing named patterns such as factory, adapter, actor, repository, saga, state machine, or policy object.
- `local-first-data` for files, embedded DBs, migrations, projections, and sync.
- `release-package` for binaries, containers, modules, changelogs, artifact provenance, compatibility, and rollback.
- `documentation` for docs authority and generated artifacts.
- `design-system` and `accessibility` if the Go repo emits HTML/docs, TUI, or user-facing UI.

## Command baseline

`go fmt ./...` is the fixer. The gates below fail instead of rewriting; the `fmt` check lists unformatted package files through `go list`, so `testdata/` and `vendor/` are skipped (files excluded by the current build tags are skipped too). `go build ./...` alone is not a gate: it passes when tests fail or don't compile.

**go.mod:**
```text
module example.com/service

go 1.27

toolchain go1.27.1
```

Replace the module path. The `toolchain` line pins the Go release; with the default `GOTOOLCHAIN=auto`, an older local Go downloads that release.

**.golangci.yml:**
```yaml
version: "2"
```

**Tool install:**
```bash
go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@v2.13.2
```

**Quality gates:**
```bash
# toolchain
go version | grep -E 'go1\.27\.1([^0-9]|$)' && golangci-lint version | grep -F 'version 2.13.2 '
# fmt
test -z "$(go list -f '{{range .GoFiles}}{{$.Dir}}/{{.}} {{end}}{{range .TestGoFiles}}{{$.Dir}}/{{.}} {{end}}{{range .XTestGoFiles}}{{$.Dir}}/{{.}} {{end}}' ./... | xargs -r gofmt -l | tee /dev/stderr)"
# vet
go vet ./...
# test
go test ./...
# build
go build ./...
# mod
go mod tidy -diff && go mod verify
# lint
golangci-lint run ./...
```

`scripts/lane-conformance.py go` runs these gates on a fixture module at every engineering-core release.

## Service SLO seed

Use `disciplines/observability.md` for runtime evidence and SLO discipline. Example seed for latency-sensitive service repos: p95 key journey `< 150–200ms`, 99.9% availability, and explicit error-budget gates. Treat these numbers as repo-local policy only after the product/runtime contract accepts them.

## Fit with 6E → CLARITY
- Strong edges/contracts, reversible slices, explicit rollback—support constraints‑first, risk‑aware delivery.

## Conditionally loaded addenda

### Justfile addendum

Read the lane-specific Justfile addendum only when:
- `Justfile` is missing
- the standardized targets are absent or drifting
- you are explicitly establishing or reconciling the repo-local `Justfile`

Otherwise, do not load the addendum by default.

Companion doc:
- `engineering-go.justfile.md`
