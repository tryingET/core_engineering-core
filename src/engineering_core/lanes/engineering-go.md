# Go lane — modules, CLIs, services, and low-latency backends

Use this lane when Go is the requested implementation language or when simple static binaries, concurrency, low operational overhead, or network-service performance make Go the best fit.

## Baseline toolchain
- **Toolchain / module system:** stable Go toolchain + modules
- **Format:** `go fmt ./...` or `gofmt`/`goimports` where imports need management
- **Analysis:** `go vet ./...`
- **Typecheck/build:** built-in compiler via `go test ./...` and `go build ./...`
- **Module integrity:** `go mod verify`; keep `go.sum` committed
- **Testing:** stdlib `testing`; built-in fuzzing via `go test -fuzz` when useful
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
- Use `golangci-lint` or `staticcheck` only when the repo pins and documents a reviewed invocation path.
- Avoid curl-pipe-shell or unreviewed installer scripts for lint/tools.
- Keep `go.sum` committed and review new transitive modules in code review.
- Prefer repo-local scripts/CI wrappers for third-party tools so agents do not rely on ambient global installs.

## Testing / rendering guidance
- Default unit/integration runner: stdlib `testing`
- Property/fuzz testing: built-in fuzzing via `go test -fuzz`
- Race testing: use `go test -race ./...` for concurrency-heavy repos where runtime cost is acceptable
- Behavior/Gherkin testing: `godog` only when executable workflow scenarios materially improve shared understanding
- Template rendering: stdlib `text/template` / `html/template` by default; use `templ` only when typed HTML/component ergonomics justify extra tooling
- Prefer the smallest deterministic surface that proves the contract


## Applicable cross-language disciplines

Load disciplines when the concern applies:

- `validation` and `testing` for command tiers and test-form choices.
- `dependency-governance` and `security-privacy` for modules, tool installs, secrets, and supply chain.
- `observability` for services, CLIs with runtime evidence, and benchmarks.
- `local-first-data` for files, embedded DBs, migrations, projections, and sync.
- `documentation` for docs authority and generated artifacts.
- `design-system` and `accessibility` if the Go repo emits HTML/docs, TUI, or user-facing UI.

## Command baseline

```bash
go fmt ./...
go vet ./...
go test ./...
go build ./...
go mod verify
```

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
