---
name: copilot-cli-agent-runtime
description: Use when configuring, operating, or instructing Copilot CLI in Yeisme projects, including skill tool usage, Claude Code tool-name mapping, MCP/GitHub workflow choices, profile sync, and safe command examples.
---

# Copilot CLI Agent Runtime

Use this skill when Copilot CLI is the active agent runtime or when instructions must explain how Copilot CLI should run Yeisme workflows.

## Workflow

1. Invoke applicable skills with Copilot CLI's `skill` tool.
2. Map common Claude Code tool names to Copilot CLI equivalents:
   - `Read` -> `view`
   - `Write` -> `create`
   - `Edit` -> `edit`
   - `Bash` -> `bash`
   - `Grep` -> `grep`
   - `Glob` -> `glob`
   - `Task` -> `task`
3. Use `gh` for GitHub-specific work and MCP Gateway for registry-routed external systems.
4. Keep skill runtime copies generated from profiles.

## Commands

```bash
copilot
gh auth status
mcp-gateway client doctor --client codex --registry ../registry.json
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
```

## Boundaries

- Do not confuse GitHub CLI convenience with Gateway route policy when a task requires MCP.
- Do not write secrets, raw prompts, hidden prompts, provider payloads, or private tool arguments to run evidence.
