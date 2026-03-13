# Go lane — low-latency services (switch here when Go is requested)

## Core stack
- **Toolchain / module system:** stable Go toolchain + modules
- **Web/API:** Chi or Gin
- **Data:** PostgreSQL • sqlc (compile‑time SQL) or GORM
- **Async/Jobs:** Asynq (Redis) or NATS JetStream
- **Contracts:** OpenAPI (REST), AsyncAPI (events)
- **Template/rendering:** stdlib `text/template` / `html/template`; `templ` when typed HTML components materially improve maintainability
- **Code quality:** gofmt/goimports (format) • go vet (analysis) • golangci-lint (lint) • staticcheck (optional)
- **Typecheck:** built-in compiler via `go test` / `go build`
- **Testing:** stdlib `testing` • built-in fuzzing via `go test -fuzz` • Ginkgo/Gomega when a richer test DSL is justified • `godog` for Gherkin/BDD when executable scenarios matter • k6 for load • CDC with Pact
- **Observability:** OpenTelemetry Go SDK → OTel Collector → Prometheus/Grafana + Jaeger/Tempo
- **Security:** OIDC; secrets manager; SAST/dep/container scans
- **Deployment:** Static binaries in Docker; Fly.io/Render/Cloud Run or k8s later

## Testing / rendering guidance
- Default unit/integration runner: stdlib `testing`
- Property/fuzz testing: built-in fuzzing via `go test -fuzz`
- Behavior/Gherkin testing: `godog` only when executable workflow scenarios materially improve shared understanding
- Template rendering: stdlib `text/template` / `html/template` by default; use `templ` only when typed HTML/component ergonomics justify extra tooling
- Prefer the smallest deterministic surface that proves the contract

## SLO seed & policy
- p95 key journey `< 150–200ms`, 99.9% availability; error‑budget gates

## Fit with 6E → CLARITY
- Strong edges/contracts, reversible slices, explicit rollback—support constraints‑first, risk‑aware delivery.
