#!/usr/bin/env bash
set -euo pipefail

VAULT="${PWD}"
STRATEGY="auto"
DRY_RUN_ONLY="false"

usage() {
  cat <<'USAGE'
Usage: pinax-update.sh [--vault PATH] [--strategy auto|keep-local|keep-remote|manual] [--dry-run-only]

Pull latest Pinax Cloud Sync state, resolve safe conflicts by policy, validate the vault, and refresh the local index.

Strategies:
  auto         Resolve only safe config/runtime conflicts with keep-local; stop for note-body conflicts.
  keep-local   Resolve all conflicts by keeping the conflict/local version.
  keep-remote  Resolve all conflicts by discarding the conflict/local version.
  manual       Pull and report conflicts without resolving.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vault)
      VAULT="${2:?missing --vault value}"
      shift 2
      ;;
    --strategy)
      STRATEGY="${2:?missing --strategy value}"
      shift 2
      ;;
    --dry-run-only)
      DRY_RUN_ONLY="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

case "$STRATEGY" in
  auto|keep-local|keep-remote|manual) ;;
  *) echo "invalid strategy: $STRATEGY" >&2; exit 64 ;;
esac

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "missing dependency: $1" >&2; exit 127; }
}

need pinax
need jq

run_json() {
  local name="$1"
  shift
  echo "==> $name"
  "$@"
}

conflicts_json() {
  pinax sync conflicts list --vault "$VAULT" --json
}

safe_conflict_path() {
  local file="$1"
  local main_path="$2"

  case "$main_path" in
    AGENTS.md|CLAUDE.md|README.md|OPERATIONS.md|.gitignore|.pinaxignore) return 0 ;;
    .agents/skills/*|.claude/skills/*) return 0 ;;
    notes/*|daily/*|inbox/*|drafts/*|journal/*|assets/*) return 1 ;;
  esac

  case "$file" in
    AGENTS.*.conflict.md|CLAUDE.*.conflict.md|README.*.conflict.md|OPERATIONS.*.conflict.md) return 0 ;;
    .agents/skills/*.conflict.md|.claude/skills/*.conflict.md) return 0 ;;
  esac

  return 1
}

resolve_conflicts() {
  local conflicts
  conflicts="$(conflicts_json)"
  local count
  count="$(jq -r '.data.conflicts | length' <<<"$conflicts")"
  if [[ "$count" == "0" ]]; then
    echo "conflicts=0"
    return 0
  fi

  if [[ "$STRATEGY" == "manual" ]]; then
    echo "$conflicts" | jq -r '.data.conflicts[] | "manual_conflict file=\(.file) main_path=\(.main_path)"'
    return 2
  fi

  local unsafe
  unsafe="$(jq -r '.data.conflicts[] | [.file, .main_path] | @tsv' <<<"$conflicts" | while IFS=$'\t' read -r file main_path; do
    if [[ "$STRATEGY" == "auto" ]] && ! safe_conflict_path "$file" "$main_path"; then
      printf '%s\t%s\n' "$file" "$main_path"
    fi
  done)"

  if [[ -n "$unsafe" ]]; then
    echo "unsafe_conflicts_detected=true"
    printf '%s\n' "$unsafe" | while IFS=$'\t' read -r file main_path; do
      echo "unsafe_conflict file=$file main_path=$main_path"
    done
    return 2
  fi

  local flag
  case "$STRATEGY" in
    auto|keep-local) flag="--keep-local" ;;
    keep-remote) flag="--keep-remote" ;;
  esac

  jq -r '.data.conflicts[].file' <<<"$conflicts" | while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    echo "resolving_conflict strategy=$STRATEGY file=$file"
    pinax sync conflicts resolve "$file" "$flag" --vault "$VAULT" --yes --json >/dev/null
  done
}

echo "pinax_update vault=$VAULT strategy=$STRATEGY"
run_json "vault list" pinax vault list --agent
run_json "cloud status" pinax cloud status --vault "$VAULT" --agent
run_json "cloud doctor" pinax cloud doctor --vault "$VAULT" --json
run_json "conflicts before" pinax sync conflicts list --vault "$VAULT" --json
run_json "pull dry-run" pinax sync pull --target cloud --vault "$VAULT" --dry-run --json

if [[ "$DRY_RUN_ONLY" == "true" ]]; then
  echo "dry_run_only=true"
  exit 0
fi

run_json "pull" pinax sync pull --target cloud --vault "$VAULT" --yes --json

resolve_conflicts || {
  code="$?"
  if [[ "$code" == "2" ]]; then
    echo "next_action=choose_conflict_strategy keep-local|keep-remote|manual-merge" >&2
  fi
  exit "$code"
}

run_json "conflicts after" pinax sync conflicts list --vault "$VAULT" --json
run_json "vault validate" pinax vault validate --vault "$VAULT" --json
run_json "index refresh" pinax index refresh --vault "$VAULT" --json
run_json "sync status" pinax sync status --vault "$VAULT" --agent

echo "pinax_update status=success"
