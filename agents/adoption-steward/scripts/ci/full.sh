#!/bin/sh
set -eu

script_dir="$(cd "$(dirname "$0")" && pwd)"
"$script_dir/smoke.sh"

repo_root="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "error: not a git repo" >&2; exit 1; }
cd "$repo_root"

AK_CMD="${AK_CMD:-ak}"
command -v "$AK_CMD" >/dev/null 2>&1 || {
  echo "error: missing required AK command: $AK_CMD" >&2
  exit 2
}

if [ -x "./scripts/check-task-scope-snapshots.sh" ]; then
  AK_CMD="$AK_CMD" ./scripts/check-task-scope-snapshots.sh
fi

if [ -x "./scripts/rocs.sh" ] && [ -f "./ontology/manifest.yaml" ]; then
  ./scripts/rocs.sh version
  ./scripts/rocs.sh validate --repo . --resolve-refs
fi

printf '%s\n' "ok: full"
