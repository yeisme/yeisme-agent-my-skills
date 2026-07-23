---
name: crush-agent-runtime
description: Use when configuring, operating, or instructing Crush in Yeisme projects, including MCP Gateway render commands, skill/profile runtime expectations, tool boundaries, and safe command examples.
---

# Crush Agent Runtime

Use this skill when Crush is the active agent runtime or when Yeisme instructions need Crush setup guidance.

## Workflow

1. Inspect the active skill runtime before assuming local capability.
2. Configure MCP through Gateway-rendered Crush commands.
3. Prefer CLI `--json`, `--agent`, and `--events` outputs for machine parsing.
4. Use explicit approval for mutations, deploys, credential changes, or external writes.

## Commands

```bash
crush
mcp-gateway client doctor --client crush --registry ../registry.json
mcp-gateway client config crush --registry ../registry.json --instructions
mcp-gateway client commands crush --registry ../registry.json
scripts/skills.sh list-runtime
```

## Boundaries

- Do not bypass Gateway route policy for configured external systems.
- Do not persist secrets, raw prompts, hidden prompts, provider payloads, private tool arguments, or full chain-of-thought.
