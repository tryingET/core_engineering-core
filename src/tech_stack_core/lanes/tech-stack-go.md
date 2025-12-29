# Go lane — low-latency services (switch here when Go is requested)

## Core stack
- **Web/API:** Chi or Gin
- **Data:** PostgreSQL • sqlc (compile‑time SQL) or GORM
- **Async/Jobs:** Asynq (Redis) or NATS JetStream
- **Contracts:** OpenAPI (REST), AsyncAPI (events)
- **Testing:** stdlib `testing` • Ginkgo/Gomega • k6 for load • CDC with Pact
- **Observability:** OpenTelemetry Go SDK → OTel Collector → Prometheus/Grafana + Jaeger/Tempo
- **Security:** OIDC; secrets manager; SAST/dep/container scans
- **Deployment:** Static binaries in Docker; Fly.io/Render/Cloud Run or k8s later

## SLO seed & policy
- p95 key journey `< 150–200ms`, 99.9% availability; error‑budget gates

## Fit with 6E → CLARITY
- Strong edges/contracts, reversible slices, explicit rollback—support constraints‑first, risk‑aware delivery. :contentReference[oaicite:18]{index=18} :contentReference[oaicite:19]{index=19}
