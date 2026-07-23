---
name: windsurf-agent-runtime
description: Use when configuring, operating, or instructing Windsurf agent workflows in Yeisme projects, including skill/profile expectations, MCP Gateway setup, local CLI contracts, and safe command examples.
---

# Windsurf Agent Runtime

Use this skill when Windsurf is the active coding agent or when Yeisme instructions need Windsurf setup guidance.

## Workflow

1. Use profile-managed skills as the workflow source; do not fork skill instructions into Windsurf-only copies.
2. Render MCP Gateway generic client instructions where direct Windsurf rendering is unavailable.
3. Prefer owning subproject commands and machine-readable output modes for automation.
4. Keep external side effects behind explicit approval and redacted evidence.

## Commands

```bash
windsurf
mcp-gateway client doctor --client generic --registry ../registry.json
mcp-gateway client config generic --registry ../registry.json --instructions
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
```

## Boundaries

- Do not duplicate Yeisme skill source into Windsurf-specific folders.
- Do not bypass Connectors, MCP Gateway, or subproject ownership boundaries.
- Do not persist secrets, raw prompts, hidden prompts, provider payloads, private tool arguments, or full chain-of-thought.
