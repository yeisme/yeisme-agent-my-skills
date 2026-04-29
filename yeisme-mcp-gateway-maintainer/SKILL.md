---
name: yeisme-mcp-gateway-maintainer
description: Use when changing, debugging, testing, or reviewing the TypeScript MCP Gateway under mcp/gateway, including CLI rendering, health checks, config loading, upstream routing, audit logging, and gateway container lifecycle.
---

# Yeisme MCP Gateway Maintainer

Use this skill for code or behavior changes inside `mcp/gateway/`.

## Boundary

- Gateway implementation lives in `mcp/gateway/src/`.
- Tests live in `mcp/gateway/tests/`.
- Shared MCP facts live in `mcp/registry.json` and `mcp/registry.schema.json`.
- Product and interface plans live in `docs/mcp-gateway/`.
- Do not put gateway implementation code in `skills/`.
- Do not add per-server Taskfiles for remote MCPs; prefer registry entries.

## Workflow

1. Read the closest existing files before designing:
   - `mcp/gateway/README.md`
   - `mcp/gateway/package.json`
   - changed files under `mcp/gateway/src/`
   - relevant tests under `mcp/gateway/tests/`
2. Preserve the current architecture:
   - registry-driven config
   - one public `/mcp` gateway endpoint
   - Streamable HTTP backends via gateway
   - stdio backends rendered for direct client use, not hosted by v1 gateway
   - compact CLI output by default, JSON when requested
3. Keep failure boundaries isolated. A failed backend must not break unrelated backends.
4. Keep audit output compact and secret-safe. Do not log full tokens, headers, large payloads, or complete tool outputs.
5. Update tests near the changed behavior before broad refactors.

## Validation

Run the narrowest useful checks, then broaden if shared behavior changed:

```bash
cd mcp/gateway
bun run build
bun test tests/*.test.ts
bun --no-env-file src/cli.ts validate
bun --no-env-file src/cli.ts render codex
```

For lifecycle or compose changes:

```bash
task -d mcp/gateway config
task -d mcp/gateway health
```

If a command cannot run because local services or credentials are missing, report that explicitly and include the next runnable smoke command.
