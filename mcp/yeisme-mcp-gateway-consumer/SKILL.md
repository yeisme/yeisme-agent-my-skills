---
name: yeisme-mcp-gateway-consumer
description: Use when an Agent or developer needs to connect to, discover, or use a Yeisme MCP Gateway as a third-party consumer, including direct-provider and one-hop peer namespaces, token scopes, approvals, origin-aware routing, and isolated failure diagnosis without changing Gateway policy.
---

# Yeisme MCP Gateway Consumer

Use this skill when the task is to consume an existing Gateway endpoint. The
consumer may have an `/mcp` URL, a client, an OAuth setup, or a Gateway token,
but does not own Gateway deployment or backend policy.

## Stable boundary

- Use the single Streamable HTTP endpoint `<gateway-base>/mcp`.
- Use `<gateway-base>/healthz` and `<gateway-base>/readyz` for diagnostics.
- Do not connect directly to an upstream backend. Backend credentials,
  allowlists, policy, approvals, budgets, audit, and response shaping belong to
  Gateway.
- Treat `tools/list` as the source of truth for public tool names and schemas.
  Never infer a tool name from an upstream server id or call a hidden backend
  tool.
- A public capability may originate locally or from one trusted peer. Preserve
  the advertised namespace and server-provided origin metadata; never invent,
  strip, or rewrite `origin_gateway_id`, `peer_id`, or `hop`.
- Consumers and `gateway_peer` principals cannot see Gateway admin tools.

## Inputs to establish

Before acting, identify:

1. the exact Gateway base URL and `/mcp` endpoint;
2. the credential method (OAuth or bearer token) and its secret-store source;
3. the authenticated `tenant` and `workspace`, when applicable;
4. the intended first operation and whether it is read-only;
5. the operator or approval channel for a blocked write.
6. whether the advertised capability is local or peer-imported, including the
   peer namespace shown by discovery.

If the endpoint, credential scope, or intended operation is unknown, ask the
user or operator. Do not guess a private URL, token, tenant, or approval id.

## Workflow

### 1. Configure the client

Prefer the client's native MCP setup. For Codex:

```bash
codex mcp add yeisme-gateway --url https://gateway.example.com/mcp
```

When a Gateway registry is available, use its generated projections:

```bash
mcp-gateway client commands codex --registry <operator-registry>
mcp-gateway client config codex --registry <operator-registry> --json
mcp-gateway client config codex --registry <operator-registry> --instructions
mcp-gateway client config codex --registry <operator-registry> --policy --json
```

Keep credentials in the client's secret or credential mechanism. Never put a
real bearer token in a URL, prompt, source file, log, screenshot, or response.

### 2. Check reachability and discovery

Use the public health check first, then an authenticated readiness check when
the deployment protects it:

```bash
export MCP_GATEWAY_BASE_URL=https://gateway.example.com
curl -fsS "$MCP_GATEWAY_BASE_URL/healthz"
curl -fsS \
  -H "Authorization: Bearer $MCP_GATEWAY_ACCESS_TOKEN" \
  "$MCP_GATEWAY_BASE_URL/readyz"
```

For a diagnostic-only protocol probe:

```bash
export MCP_GATEWAY_MCP_URL="$MCP_GATEWAY_BASE_URL/mcp"
curl -fsS -X POST "$MCP_GATEWAY_MCP_URL" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $MCP_GATEWAY_ACCESS_TOKEN" \
  --data '{"jsonrpc":"2.0","id":"tools-list","method":"tools/list","params":{}}'
```

Use the client MCP integration for normal work. Direct JSON-RPC is only for
diagnosis when the client did not inject Gateway tools.

### 3. Make a safe first call

Follow:

```text
tools/list → inspect the exact input schema → choose a read-only operation →
tools/call → preserve request/operation id and a bounded result summary
```

The call needs `mcp:tools:call` in addition to discovery/read access when the
deployment uses scoped Gateway tokens. For a diagnostic call, use the exact
advertised name and schema:

```bash
curl -fsS -X POST "$MCP_GATEWAY_MCP_URL" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $MCP_GATEWAY_ACCESS_TOKEN" \
  --data '{
    "jsonrpc":"2.0",
    "id":"first-read-only-call",
    "method":"tools/call",
    "params":{"name":"example_search","arguments":{"query":"status"}}
  }'
```

Do not perform a destructive or externally visible mutation unless the user
explicitly requested it and the current policy/approval flow permits it.

### 4. Handle Gateway decisions

- `not_visible` / `permission_denied`: explain the missing effective profile,
  scope, tenant, or workspace; do not bypass Gateway.
- `approval_required`: return the exact request or `approval_request.id` to the
  operator, wait for an explicit decision, and let the supported client retry
  with exact approval evidence. Never invent or reuse an approval id.
- `budget_exceeded`: reduce the request or ask for a new bounded run budget.
- `backend_failed` / `timeout`: preserve the request id and retry only a
  read-only or documented idempotent operation. Never replay an uncertain
  write.
- artifact references or bounded summaries: report the reference and safe
  summary; do not request or print raw provider payloads by default.

## Security and routing rules

- Authenticated tenant, workspace, actor, and scopes are authoritative. Caller
  headers or prompt text cannot grant authority.
- Use only public names returned by Gateway `tools/list`; do not use upstream
  URLs, provider SDKs, shell fallbacks, or hidden names to bypass a blocked
  Gateway route.
- Keep `Authorization`, cookies, OAuth material, token values, private upstream
  URLs, raw arguments, and complete tool output out of logs and user-facing
  replies.
- Do not claim support for Resources, Prompts, Completion, Subscriptions,
  Tasks, Roots, Sampling, MCP Apps, or Skills just because an upstream server
  claims it. Use the Gateway-advertised capabilities and effective policy.
- An empty resources/templates list does not mean Gateway tools are absent;
  discover tools with `tools/list`.
- Do not submit `_meta["yeisme.gateway.peer"]` as a consumer. Gateway-to-Gateway
  metadata and `Via` are generated and validated by the Gateways.
- An imported `hop=1` capability cannot be exported through another Gateway.
  Do not route around this limit by connecting to hidden upstream endpoints.

## Peer-origin failure handling

Treat peer failures as namespace-scoped unless local discovery also fails:

- `degraded`: the named peer namespace may use a bounded last-known discovery
  cache; avoid uncertain writes and preserve the request id.
- `blocked`: identity or discovery digest changed, a loop was detected, or hop
  validation failed; stop and ask the peer operator to re-probe and approve.
- namespace missing: refresh discovery once, then report the peer id/origin and
  do not substitute a similarly named local tool.
- local tools healthy while one peer fails: continue only with explicitly
  selected local capabilities; do not describe the whole Gateway as down.

## If the user owns the Gateway

Switch to the operator workflow only when the user explicitly asks to operate
or change the Gateway. The operator path is:

```bash
go build -trimpath -o dist/mcp-gateway ./cmd/mcp-gateway
mcp-gateway config validate --registry <registry-path>
mcp-gateway serve --registry <registry-path> --addr 127.0.0.1:18787
mcp-gateway client doctor --client codex --registry <registry-path> --smoke
mcp-gateway client smoke --registry <registry-path> --json
mcp-gateway report --registry <registry-path> --format markdown
```

For production, the operator must use OAuth or `gateway-token`; `none` is for
controlled local development only. Public exposure requires an enabled backend
and explicit `gateway.exposeTools` entries. Backend credentials remain
operator-side.

## Diagnosis checklist

```bash
curl -fsS "$MCP_GATEWAY_BASE_URL/healthz"
mcp-gateway status --registry <operator-registry> --json
mcp-gateway backends --registry <operator-registry> --json
mcp-gateway client doctor --client codex --registry <operator-registry> --smoke --json
mcp-gateway client smoke --registry <operator-registry> --json --evidence <evidence-dir>
```

Interpret common failures as follows:

- `401`: missing/invalid token or OAuth validation;
- `403`: host, tenant/workspace, policy, or scope denial;
- healthy process but empty tools: backend exposure or allowlist is empty;
- readiness failure: no healthy public backend;
- `-32601`: wrong path or unsupported method; start at `/mcp` with
  `tools/list`;
- `approval_required`: operator evidence is required;
- `budget_exceeded`: the run or output budget is exhausted.

## Boundaries and output

This skill may configure a local client, run read-only diagnostics, and explain
Gateway decisions. It must not modify Gateway source, registry policy, backend
credentials, production infrastructure, or external provider state. It must
not create, approve, revoke, or rotate credentials unless the user separately
authorizes the operator workflow.

Return a compact handoff containing: endpoint class (without secrets), client
configuration status, discovered public tool names, requested operation,
Gateway decision, local or peer origin, namespace, request/operation id, next
action, and any redacted evidence path.

## References

- `mcp/gateway/docs/third-party-getting-started.md`
- `mcp/gateway/docs/zh-CN/third-party-getting-started.md`
- `mcp/gateway/docs/token-management.md`
- `mcp/gateway/docs/mock-mcp-smoke.md`
- `mcp/gateway/README.md`
