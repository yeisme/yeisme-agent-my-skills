---
name: yeisme-mcp-gateway-operator
description: Use when operating the deployed Yeisme MCP Gateway through the mcp-gateway CLI, Web UI, TUI, /api endpoints, or /mcp client endpoint, including status checks, tool discovery, diagnostics, reports, client config rendering, and routine service lifecycle checks without changing gateway code or registry definitions.
---

# Yeisme MCP Gateway Operator

Use this skill to operate the already deployed MCP Gateway as a user or runtime operator.

## Scope

- Gateway service: `http://10.10.1.101:18787`
- MCP endpoint: `http://10.10.1.101:18787/mcp`
- Web console: `http://10.10.1.101:18787/`
- Source project: `mcp/gateway`
- Long-running service: `nerdctl compose` via `mcp/gateway/Taskfile.yml`

## Boundaries

- Do not change gateway TypeScript code here; use `yeisme-mcp-gateway-maintainer`.
- Do not edit `mcp/registry.json`, credentials, groups, permissions, or exposure policy here; use `yeisme-mcp-registry-onboarding`.
- Do not print secrets, tokens, raw Authorization headers, or env file values.
- Prefer `mcp-gateway` CLI for human operations and `--json` for machine-readable inspection.
- Do not use or troubleshoot BigModel/Zai `web-search-prime` for 联网搜索; it is intentionally disabled in Gateway. Use Firecrawl CLI against the configured `backend-server/firecrawl` backend instead.
- Use destructive MCP tools only when the user explicitly asks for that action and the target server has been identified.

## Quick Workflow

1. Confirm the CLI is available:

```bash
which mcp-gateway
mcp-gateway --help
```

2. Check gateway health:

```bash
mcp-gateway status
cd mcp/gateway && task health
```

3. Inspect available groups, backends, and tools:

```bash
mcp-gateway groups
mcp-gateway backends
mcp-gateway tools
mcp-gateway tools --server gitea-mcp
```

For 联网搜索, bypass Gateway and use Firecrawl CLI:

```bash
firecrawl view-config
firecrawl search "query" --api-url http://localhost:32741 --limit 5 -o .firecrawl/search.json --json
```

4. Diagnose a backend before retrying tool work:

```bash
mcp-gateway diagnose --server gitea-mcp
mcp-gateway diagnose --server gitea-mcp --refresh-tools
```

5. Use structured output when an agent needs to parse results:

```bash
mcp-gateway status --json
mcp-gateway tools --server gitea-mcp --json
curl -fsS http://10.10.1.101:18787/api/projection
```

## Client Configuration

Render client configs instead of hand-writing MCP endpoint blocks:

```bash
mcp-gateway render codex
mcp-gateway render gemini
mcp-gateway render opencode
mcp-gateway render crush
mcp-gateway commands codex
```

For direct client wiring, the canonical MCP URL is:

```text
http://10.10.1.101:18787/mcp
```

## Interactive Surfaces

Use the Web console for visual inspection:

```text
http://10.10.1.101:18787/
```

Use the TUI for terminal inspection:

```bash
mcp-gateway tui
mcp-gateway tui --server gitea-mcp --refresh 5s
```

## Service Lifecycle

For the long-running gateway service:

```bash
cd mcp/gateway
task ps
task health
task logs
task restart
```

Use `task down` only when the user explicitly asks to stop the service.

## Troubleshooting

- If `mcp-gateway` is missing, run commands from source:

```bash
cd mcp/gateway
bun run cli -- status
```

- If `/api/projection` fails but the container is running, check logs:

```bash
cd mcp/gateway
task logs
```

- If a backend is degraded, diagnose that backend first and avoid broad restarts:

```bash
mcp-gateway diagnose --server <backend>
```

## Output

When reporting status, include:

- gateway URL and MCP endpoint
- health summary: backend count, exposed tool count, auth mode
- any degraded backend and the next diagnostic command
- commands actually run and whether they passed
