---
name: cursor-agent-runtime
description: Use when configuring, operating, or instructing Cursor agent workflows in Yeisme projects, including skill/profile expectations, MCP Gateway setup, local CLI contracts, and safe command examples.
---

# Cursor Agent Runtime

Use this skill when Cursor is the active coding agent or when Yeisme instructions need Cursor setup guidance.

## Workflow

1. Treat Yeisme skills as profile-managed runtime guidance. Source remains under `.skills/yeisme/` or `.skills/imported/`.
2. Render MCP Gateway client instructions where Cursor supports MCP configuration; otherwise use the rendered commands as setup guidance.
3. Prefer subproject CLIs and `--json` output for repeatable actions.
4. Keep implementation inside the owning subproject and follow its `AGENTS.md`.

## Commands

```bash
cursor
mcp-gateway client doctor --client generic --registry ../registry.json
mcp-gateway client config generic --registry ../registry.json --instructions
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
```

## Boundaries

- Do not make Cursor-specific docs the source of truth for Yeisme skill assignments.
- Do not store unsafe model internals, secrets, provider payloads, or private tool arguments.
