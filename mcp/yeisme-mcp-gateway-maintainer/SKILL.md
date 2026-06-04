---
name: yeisme-mcp-gateway-maintainer
description: Use when changing, debugging, testing, or reviewing the Go MCP Gateway under mcp/gateway, including CLI/API behavior, health checks, config loading, upstream routing, audit safety, and gateway lifecycle.
---

# Yeisme MCP Gateway Maintainer

Use this skill for code or behavior changes inside `mcp/gateway/`.

## Boundary

- CLI entrypoint lives in `mcp/gateway/cmd/mcp-gateway/`.
- Gateway HTTP/API implementation lives in `mcp/gateway/internal/gateway/`.
- Registry loading and validation lives in `mcp/gateway/internal/registry/`.
- Tests live beside the Go packages they cover.
- Shared MCP facts live in `mcp/registry.json` and `mcp/registry.schema.json`.
- In an `mcp/gateway` session, product, interface, runtime, observability, logging, and long-lived implementation plans live in local `docs/**`. Root project-doc mirrors are not valid owners and must not be required for closeout.
- Do not put gateway implementation code in `.skills/imported/`.
- Do not add per-server Taskfiles for remote MCPs; prefer registry entries.
- Do not add Web UI, TUI, mobile, or frontend marketplace code to `mcp/gateway`; this project is CLI/API only.
- BigModel/Zai `web-search-prime` is intentionally disabled for 联网搜索. Preserve that policy; use Firecrawl CLI against `/home/yeshugen/workplace/backend-server-firecrawl` for search workflows unless a separate plan explicitly introduces a Firecrawl MCP backend.

## Workflow

1. Read the closest existing files before designing:
   - `mcp/gateway/README.md`
   - `mcp/gateway/go.mod`
   - changed files under `mcp/gateway/cmd/` or `mcp/gateway/internal/`
   - relevant package tests
2. Preserve the current architecture:
   - registry-driven config
   - one public `/mcp` gateway endpoint
   - Streamable HTTP backends via gateway
   - stdio backends remain registry facts, not hosted by the Go API gateway
   - compact CLI output by default, JSON when requested
   - CLI output changes must also follow `ai-native-cli-output-contract`
3. Keep failure boundaries isolated. A failed backend must not break unrelated backends.
4. Keep audit output compact and secret-safe. Do not log full tokens, headers, large payloads, or complete tool outputs.
5. Update tests near the changed behavior before broad refactors.

## Validation

Run the narrowest useful checks, then broaden if shared behavior changed:

```bash
cd mcp/gateway
go test ./...
go build ./cmd/mcp-gateway
go run ./cmd/mcp-gateway validate --registry ../registry.json
go run ./cmd/mcp-gateway status --registry ../registry.json
```

For lifecycle or compose changes:

```bash
task -d mcp/gateway config
task -d mcp/gateway health
```

If a command cannot run because local services or credentials are missing, report that explicitly and include the next runnable smoke command.
