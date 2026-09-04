#!/usr/bin/env bash
# gitea-mcp-quickstart card: live gateway tools/list + digest.
# Env: MCP_GATEWAY_MCP_URL (default http://127.0.0.1:18787/mcp), MCP_GATEWAY_ACCESS_TOKEN (optional).
# Exit codes: 0 card printed; 2 gateway unreachable (embedded UNVERIFIED card below); 3 curl/jq missing.
set -euo pipefail

BASE="${MCP_GATEWAY_BASE_URL:-http://127.0.0.1:18787}"
URL="${MCP_GATEWAY_MCP_URL:-$BASE/mcp}"
TOK="${MCP_GATEWAY_ACCESS_TOKEN:-}"

embedded() {
  echo "# gitea-mcp card (UNVERIFIED — gateway unreachable)"
  echo "generated_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  cat <<'EOF'
gitea_mcp_search   {query, limit?, mode?(summary|verbose), scope?, include_write?}   discover canonical actions
gitea_mcp_exec     {action, arguments, view?/mode?(summary|standard|verbose)}        run one catalog action
gitea_mcp_health_check       {}   server/policy/metrics snapshot
gitea_mcp_capability_self_check {checks?, owner?, repo?}   capability diagnostics
gitea_mcp_get_gitea_mcp_server_version {}   server version
# golden path: search -> copy exec_example -> exec (2 calls). Never guess action names.
EOF
}

for bin in curl jq; do
  command -v "$bin" >/dev/null 2>&1 || { embedded >&2; exit 3; }
done

body='{"jsonrpc":"2.0","id":"card","method":"tools/list","params":{}}'
if [ -n "$TOK" ]; then
  out="$(curl -fsS -m 10 -X POST "$URL" -H 'Content-Type: application/json' -H "Authorization: Bearer $TOK" --data "$body" 2>/dev/null)" || { embedded; exit 2; }
else
  out="$(curl -fsS -m 10 -X POST "$URL" -H 'Content-Type: application/json' --data "$body" 2>/dev/null)" || { embedded; exit 2; }
fi

digest="$(printf '%s' "$out" | jq -r '[.result.tools[]?.name] | sort | join("\n")' | (sha256sum 2>/dev/null || shasum -a 256) | cut -c1-16)"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

rows() { printf '%s' "$out" | jq -r '.result.tools | sort_by(.name)[] | "\(.name)\t\((.description | split("\n")[0] | .[0:110]))"'; }

{
  echo "# gateway tools card"
  echo "generated_utc: $ts"
  echo "tool_count: $(printf '%s' "$out" | jq -r '.result.tools | length')"
  echo "digest_sha256_16: $digest"
  echo "source: JSON-RPC tools/list $URL"
  echo "# view is principal-scoped: set MCP_GATEWAY_ACCESS_TOKEN for your entitled tools"
  echo "# digest changed => tool set drifted; re-verify before guessing names"
  echo
  rows
} | column -t -s $'\t' 2>/dev/null || rows
