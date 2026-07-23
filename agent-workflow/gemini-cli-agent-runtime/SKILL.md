---
name: gemini-cli-agent-runtime
description: Use when configuring, operating, or instructing Gemini CLI in Yeisme projects, including skill activation, MCP Gateway client rendering, tool mapping, profile sync, and safe command examples.
---

# Gemini CLI Agent Runtime

Use this skill when Gemini CLI is the active agent runtime or when Yeisme docs need Gemini-specific setup and usage guidance.

## Workflow

1. Activate applicable skills with Gemini's skill activation mechanism when available.
2. Use runtime homes generated from profiles by `scripts/skills.sh`; do not copy Yeisme source skills into ad hoc locations.
3. Render MCP Gateway instructions for Gemini and follow registry route policy.
4. Prefer structured Yeisme CLI output over prose parsing.

## Commands

```bash
gemini
mcp-gateway client doctor --client gemini --registry ../registry.json
mcp-gateway client config gemini --registry ../registry.json --instructions
mcp-gateway client commands gemini --registry ../registry.json
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
```

## Boundaries

- Do not hand-write MCP endpoint blocks when Gateway can render them.
- Do not bypass official Connectors for chat-provider payloads or conversation delivery.
- Do not store unsafe model internals or private tool arguments in evidence.
