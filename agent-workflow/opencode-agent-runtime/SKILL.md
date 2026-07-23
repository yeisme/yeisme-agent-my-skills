---
name: opencode-agent-runtime
description: Use when configuring, operating, or instructing opencode in Yeisme projects, including MCP Gateway render commands, skill/profile runtime expectations, tool boundaries, and safe command examples.
---

# opencode Agent Runtime

Use this skill when opencode is the active agent runtime or when Yeisme instructions need opencode setup guidance.

## Workflow

1. Use `scripts/skills.sh profile show <owner>` to inspect desired skill assignments before assuming runtime skill availability.
2. Configure MCP through Gateway render commands for opencode.
3. Prefer Yeisme CLI `--json` and `--agent` output for automation.
4. Keep external side effects behind the owning CLI, MCP Gateway policy, or explicit user approval.

## Commands

```bash
opencode
mcp-gateway client doctor --client opencode --registry ../registry.json
mcp-gateway client config opencode --registry ../registry.json --instructions
mcp-gateway client commands opencode --registry ../registry.json
scripts/skills.sh list-runtime
```

## Boundaries

- Do not hand-write generated MCP client config when Gateway can render it.
- Do not let opencode own Connectors provider behavior or MCP implementation details.
