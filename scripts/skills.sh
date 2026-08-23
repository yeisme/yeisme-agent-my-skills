#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
ENGINE="$ROOT_DIR/agent-workflow/yeisme-skill-routing-governance/scripts/skills.sh"

if [[ ! -x "$ENGINE" ]]; then
  printf 'Portable Skill manager is unavailable because agent-workflow is not initialized.\n' >&2
  printf 'Run: git submodule update --init --recursive agent-workflow\n' >&2
  exit 1
fi

exec "$ENGINE" --source "$ROOT_DIR" "$@"
