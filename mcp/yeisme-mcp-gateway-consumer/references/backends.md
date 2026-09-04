# Gateway backend quick cards

**These cards are navigation, not the source of truth.** Gateway `tools/list`
remains authoritative for public tool names and schemas (see the Stable
boundary rules in the parent skill): run one `tools/list` (or
`gitea-mcp-quickstart`'s `scripts/card.sh`) at session start and reconcile any
difference before calling. A card entry that disagrees with `tools/list` is
stale — trust the live discovery and treat the drift as a signal to re-read
this file's owning skill.

Current public surface (per `mcp/registry.json`): 7 tools across two enabled
backends — `gitea-mcp` (5) and `cloudflare-api` (2). `open-design` is
enabled-but-default-deny (0 exposed tools); `anatomia-video` is disabled.

## gitea-mcp (namespace `gitea_mcp_`, group code-collaboration)

| Intent | Tool + arguments | Notes |
| --- | --- | --- |
| Find the action for a Gitea job | `gitea_mcp_search {query, limit?, mode?, scope?, include_write?}` | Returns `canonical_action`, `required_args`, `arguments_template`, `exec_example` — copy, don't invent |
| Run the action | `gitea_mcp_exec {action, arguments, view?}` | ~370-action catalog behind one tool; default `summary` view; writes need an operator-enabled window |
| Server/policy snapshot | `gitea_mcp_health_check {}` | `read_only`, `guard_mode`, tool inventory, error metrics |
| Capability diagnostics | `gitea_mcp_capability_self_check {checks?, owner?, repo?}` | auth/projects/packages/actions/wiki/activity |
| Server version | `gitea_mcp_get_gitea_mcp_server_version {}` | |

Golden path is exactly two calls (`search` → `exec` with the copied
`exec_example`). Deeper policy, recovery, and worked examples live in the
`gitea-mcp-quickstart` skill.

## cloudflare-api (namespace `cloudflare_api_`, group infrastructure-ops)

| Intent | Tool + arguments | Notes |
| --- | --- | --- |
| Find a Cloudflare API endpoint | `cloudflare_api_search {query, ...}` | Searches the Cloudflare OpenAPI spec; `$refs` pre-resolved |
| Run code against the API | `cloudflare_api_execute {code, ...}` | Execute JavaScript against the Cloudflare API; search first to find the right endpoint |

Cloudflare tool arguments are token-scoped upstream: actual authority equals
the `CLOUDFLARE_API_TOKEN` scope held gateway-side. Consumers never see or
send that token.

## Context-cost rules (why the cards are short)

- Gateway `tools/list` returns compact entries only — field names, not full
  schemas. Full input schema is fetched per tool on demand via
  `GET /v1/tools/{name}`; do not assume the discovery entry is sufficient for
  a write call.
- One `tools/list` per session is enough; the namespaced view is
  principal-scoped (an anonymous probe legitimately shows fewer tools than an
  entitled principal — that is policy, not an outage).
- Responses are budgeted (compact detail by default, `maxOutputBytes` ~12KB
  per backend); prefer `limit`/pagination and the `summary` view, and escalate
  to `standard`/`verbose` only when the summary cannot answer the question.
- Per-backend timeout is ~30s with failure isolation: one backend failing does
  not degrade the others; retry only read-only or documented idempotent
  operations after a `backend_failed`/`timeout` decision.
