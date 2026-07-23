---
name: claude-code-agent-runtime
description: Use when configuring, operating, or instructing Claude Code in Yeisme projects, including generated .claude/skills runtime homes, Skill tool usage, MCP Gateway config, profile sync, and safe command examples.
---

# Claude Code Agent Runtime

Use this skill when a task is being handled by Claude Code or when instructions must explain how Claude Code should use Yeisme skills and tools.

## Workflow

1. Treat `.claude/skills/` as a generated runtime home, not as the source of truth.
2. Use the `Skill` tool before acting whenever an applicable skill exists.
3. Keep `.claude/skills/` aligned with `.agents/skills/` by syncing from profile assignments.
4. Use MCP Gateway-rendered config and instructions for MCP access.
5. Prefer Yeisme CLI machine modes for agent parsing: `--json`, `--agent`, and `--events`.

## Commands

```bash
claude
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
mcp-gateway client doctor --client codex --registry ../registry.json
mcp-gateway client config codex --registry ../registry.json --instructions
```

## Boundaries

- Do not edit generated `.claude/skills/` copies as source.
- Do not store secrets, raw prompts, hidden prompts, provider payloads, private tool arguments, or full chain-of-thought in docs, logs, or evidence.
- Do not make Claude Code the owner of Connectors provider adapters, MCP implementation, or Yeisme subproject business logic.
