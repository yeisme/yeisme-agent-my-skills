---
name: yeisme-mcp-registry-onboarding
description: Use when adding, updating, reviewing, or removing MCP backends in mcp/registry.json, mcp/mcp.env.example, client render behavior, gateway exposure, groups, permissions, credentials, and health policies.
---

# Yeisme MCP Registry Onboarding

Use this skill for registry-driven MCP onboarding and maintenance.

## Boundary

- Registry source of truth: `mcp/registry.json`.
- Schema: `mcp/registry.schema.json`.
- Credential template: `mcp/mcp.env.example`.
- Real secrets: `mcp/.env.mcp`, `mcp/gateway/.env`, service-specific `.env` files. Do not commit real secrets.
- Add `mcp/<name>/` only for self-hosted code or lifecycle owned by this repo.
- Remote or package-managed MCPs should normally be registry-only.
- 联网搜索默认不接入 BigModel/Zai `web-search-prime`；保持该 backend disabled，并让 agent 通过 Firecrawl CLI 直连 `/home/yeshugen/workplace/backend-server-firecrawl`。

## Workflow

1. Classify the backend:
   - `remote`
   - `managed-upstream`
   - `self-hosted`
   - `local-package`
   - `local-command`
2. Decide exposure:
   - Streamable HTTP can be gateway-exposed when `gateway.enabled=true`.
   - stdio stays direct-rendered for clients unless gateway support has been explicitly implemented.
   - Firecrawl CLI is a direct CLI workflow, not a Gateway MCP backend; do not wrap it in registry unless a real Firecrawl MCP server is intentionally introduced.
3. Define permission and response policy before enabling:
   - `permission.mode`
   - `credentialSource`
   - `destructiveActions`
   - concise `notes`
   - compact default response policy
4. Keep `clients` explicit for Codex, Gemini, OpenCode, and Crush.
5. Place the backend in an existing group or add a group with English title/description and a docs path.
6. If adding env vars, update `mcp/mcp.env.example` with placeholders only.
7. Avoid broad rewrites of `registry.json`; preserve existing formatting and ordering where practical.

## Validation

```bash
mcp-gateway validate
mcp-gateway list
mcp-gateway render codex
mcp-gateway render gemini
mcp-gateway render opencode
mcp-gateway health
```

If `mcp-gateway` is not on `PATH`, use:

```bash
cd mcp/gateway
bun --no-env-file src/cli.ts validate
bun --no-env-file src/cli.ts render codex
```

Report any skipped health checks caused by missing credentials or unreachable private network services.
