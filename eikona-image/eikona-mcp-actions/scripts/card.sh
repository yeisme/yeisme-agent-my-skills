#!/usr/bin/env bash
# eikona-mcp-actions card: live action map + digest from `eikona mcp capabilities`.
# Uses --json --full (compact mode caps the array at a 5-item sample plus a count).
# Exit codes: 0 card printed; 2 discovery failed (fall back to references/action-map.md, marked UNVERIFIED); 3 eikona CLI absent.
set -euo pipefail

if ! command -v eikona >/dev/null 2>&1; then
  echo "eikona CLI not found. Use references/action-map.md (UNVERIFIED) or GET /api/v1/mcp/actions when a service endpoint is known." >&2
  exit 3
fi

out="$(eikona mcp capabilities --json --full 2>/dev/null)" || {
  echo "eikona mcp capabilities --json --full failed. Fall back to references/action-map.md (UNVERIFIED)." >&2
  exit 2
}

count="$(printf '%s' "$out" | jq -r '.data.execute_actions_count // (.data.execute_actions | length)')"
nrows="$(printf '%s' "$out" | jq -r '.data.execute_actions | length')"
digest="$(printf '%s' "$out" | jq -r '.data.execute_actions | map(.action) | sort | join("\n")' | (sha256sum 2>/dev/null || shasum -a 256) | cut -c1-16)"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

rows() { printf '%s' "$out" | jq -r '.data.execute_actions | sort_by(.action)[] | "\(.action)\t\(.kind)\t\(.audience)\t\(.safety)"'; }

{
  echo "# eikona mcp action card"
  echo "generated_utc: $ts"
  echo "actions_count: $count (rows: $nrows)"
  echo "digest_sha256_16: $digest"
  echo "source: eikona mcp capabilities --json --full"
  echo "# digest changed => action set drifted; re-read the navigation map before guessing names"
  [ "$nrows" != "$count" ] && echo "# WARNING: sample only (rows != count); full live list needs a newer eikona or GET /api/v1/mcp/actions"
  echo
  rows
} | column -t -s $'\t' 2>/dev/null || rows
