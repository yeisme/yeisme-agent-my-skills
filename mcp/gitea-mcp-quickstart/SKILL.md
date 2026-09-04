---
name: gitea-mcp-quickstart
description: "Use when an agent operates Gitea through the compact gitea-mcp tool surface (gitea_mcp_search/gitea_mcp_exec via the Yeisme MCP Gateway, or a direct gitea-mcp server): discovering the canonical action, filling required arguments, respecting read-only/allowlist/guard policy, or recovering from shape and unknown-action errors. Gateway connection, tokens, and approvals stay in yeisme-mcp-gateway-consumer; server deployment stays with the operator."
---

# Gitea MCP quickstart

gitea-mcp exposes a deliberately tiny tool surface and hides a ~370-action
catalog behind two tools. Every real job is two calls: `search` to get the
canonical action, then `exec` with the copied template. Fumbling `exec` with
guessed actions or arguments is the dominant failure mode (server metrics show
UNKNOWN_ACTION / MISSING_REQUIRED_ARGUMENTS / UNEXPECTED_ARGUMENTS dominating
exec errors) — this skill exists to make the two-call path the default.

## Tool surface (compact mode)

| Tool | Purpose |
| --- | --- |
| `gitea_mcp_search` | Discover catalog actions: `query`, `limit`, `mode` (summary/verbose), `scope`, `include_write` |
| `gitea_mcp_exec` | Run one canonical action: `action`, `arguments` (nested object), `view`/`mode` (summary/standard/verbose) |
| `gitea_mcp_health_check` | Server snapshot: auth, policy (`read_only`, `guard_mode`), tool inventory, metrics |
| `gitea_mcp_capability_self_check` | Capability checks: auth, projects, packages, actions, wiki, activity; `owner`/`repo` scope repo checks |
| `gitea_mcp_get_gitea_mcp_server_version` | Server version |

Names are gateway-namespaced (`gitea_mcp_*`); on a direct server they are
`search`/`exec`/…. This table is navigation: confirm live names with one
`tools/list` (or `scripts/card.sh`) per session before first use.

## Golden path: search → exec

1. `gitea_mcp_search` with a short query, `limit: 3`. Phrase the query with
   canonical verb words (`"issue create"`, `"list branches"`,
   `"merge pull request"`, `"list_my_repos"`) — natural phrasing like
   "repositories I own" measurably misses; canonical verbs hit in one call.
   Add `scope: "<module>"` (repo/issue/pull/…) to narrow, and
   `include_write: true` only when a write is actually needed.
2. Each hit returns `canonical_action`, `required_args`,
   `arguments_template`, and a ready-to-copy `exec_example`.
3. `gitea_mcp_exec` with the `exec_example` verbatim, filling placeholders.
   Keep the default `summary` view for lists; use `standard`/`verbose` only
   when the summary proves insufficient.

Verified example (real server response for `query: "issue create"`, `limit: 3`):

```json
{
  "action": "issue.get",
  "arguments": {"owner": "<owner>", "repo": "<repo>", "index": 1}
}
```

with `required_args: ["index", "owner", "repo"]` and
`optional_args_preview: ["commentID"]` — copy that object into
`gitea_mcp_exec.arguments`, never invent sibling keys.

## Policy guardrails

- Deployment default is **read-only** (`policy_profile: read-only`): write
  actions exist in the catalog but the server refuses them until an operator
  enables write mode in a trusted window. Do not retry a write denial; report
  it as an operator action.
- `GITEA_REPO_ALLOWLIST` may pin accessible `owner/repo` pairs; broad reads
  without explicit repo parameters are rejected when it is set.
- Guard runs before the Gitea call; destructive operations (delete/transfer
  repository) are hard-refused in every mode.
- Shape errors (missing/unexpected arguments) return `expected_shape` and an
  `exec_example` before any request reaches Gitea — treat them as the
  correction, then fix `arguments` in place.

## Error recovery

| Error | Recovery |
| --- | --- |
| `UNKNOWN_ACTION` | Re-`search` with different terms; never guess or pluralize action names |
| `MISSING_REQUIRED_ARGUMENTS` / `UNEXPECTED_ARGUMENTS` | Copy `arguments_template`/`exec_example` from the last search hit; remove invented keys |
| Write/guard denial | Stop; report the operator action (enable write window or extend allowlist) |
| Timeout / backend failure | Retry read-only or documented idempotent operations only; never replay an uncertain write |

## Card script

`scripts/card.sh` prints the live gateway tool list (JSON-RPC `tools/list`)
with a digest and timestamp. Configure with `MCP_GATEWAY_MCP_URL` and
`MCP_GATEWAY_ACCESS_TOKEN` (token is passed as a header, never echoed); on
failure it degrades to the embedded tool table above, marked `UNVERIFIED`.
