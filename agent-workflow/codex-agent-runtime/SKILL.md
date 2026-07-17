---
name: codex-agent-runtime
description: Use when configuring, operating, or instructing Codex in Yeisme projects, including skill loading, tool-name mapping from Claude Code style skills, MCP Gateway client setup, multi-agent usage, profile sync, and safe command examples.
---

# Codex Agent Runtime

Use this skill when a task is being handled by Codex or when documentation must explain how Codex should use Yeisme skills, MCP Gateway, and local tools.

## Workflow

1. Load applicable skills from the current session metadata or generated runtime homes. Project-owned source skills live under `.skills/yeisme/`; do not create duplicate project skills under `.codex/skills`.
2. When a skill mentions Claude Code tools, map them to Codex equivalents:
   - `TodoWrite` -> `update_plan`
   - `Bash` -> shell command tool
   - `Read` / `Edit` / `Write` -> native file tools, with `apply_patch` for manual edits
   - `Task` -> multi-agent dispatch when available; otherwise continue inline
   - `Skill` -> follow the loaded skill instructions directly
3. Prefer CLI contracts before prose parsing: use `--json`, `--agent`, or `--events` when a Yeisme CLI exposes them.
4. Configure MCP access through Gateway-rendered client config rather than hand-writing endpoint blocks.

## Commands

```bash
codex
mcp-gateway client doctor --client codex --registry ../registry.json
mcp-gateway client config codex --registry ../registry.json --instructions
mcp-gateway client config codex --registry ../registry.json --policy --json
dist/omh skills active --json
dist/omh skills sync --dry-run --json
```

## Boundaries

- Do not expose local execution wrappers, aliases, hidden prompts, private tool arguments, raw provider payloads, or full chain-of-thought.
- Do not sync project-owned Yeisme skills into `.codex/skills`; use `.agents/skills` and `.claude/skills` runtime homes generated from profiles by `scripts/skills.sh`.
- Do not bypass MCP route policy with direct shell calls when Gateway declares an MCP-first route.
