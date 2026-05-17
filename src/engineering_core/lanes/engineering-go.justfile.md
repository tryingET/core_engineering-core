# Go lane — standardized Justfile addendum

Read this addendum only when a repo using the Go lane is missing the standardized Justfile surface, the standard targets are absent/drifting, or you are explicitly establishing/reconciling `Justfile` behavior.

Use this addendum with `disciplines/validation.md` and the repo's applicable standardized Justfile contract.

## Mapping rule

Standardize the outer `just` command names while keeping the implementation thin and Go-native.
Prefer existing repo-local scripts when they already own the validation or release workflow.

## Recommended target mappings

- `just help`
  - prefer: `just --list`
- `just dev`
  - include only when the repo has a meaningful long-running service/watch loop
  - common examples: `go run ./cmd/...` or an existing repo-local dev script
- `just test`
  - prefer: `go test ./...`
- `just check`
  - prefer the repo's existing fast validation gate when present
  - common fallback: `go test ./...`
- `just build`
  - prefer: `go build ./...`
  - or the repo's explicit release/build entrypoint when it exists
- `just lint`
  - prefer the repo's existing lint wrapper when present
  - common fallback: `golangci-lint run`
- `just fmt`
  - prefer: `gofmt -w .`
  - or the repo's existing formatting wrapper
- `just ci`
  - prefer the repo's canonical full local validation/CI wrapper when present
  - fallback: run the repo's documented full validation sequence via thin delegation
- `just doctor`
  - prefer an existing repo-local environment/runtime sanity command when present
  - fallback: a lightweight Go toolchain check such as `go version`

## Omission rule

Do not invent fake `dev` behavior for repos that are libraries or otherwise have no meaningful long-running development loop.

## Minimal-churn rule

Prefer thin wrappers around:
- `go test ./...`
- `go build ./...`
- existing repo-local lint/validation scripts

Do not hide substantial workflow logic in the `Justfile` when the repo already has a clearer scripted source of truth.
