---
name: yeisme-repo-routing
description: Use when deciding where new files, workflows, skills, MCP code, CLI wrappers, agent assets, gateway assets, or documentation should live in this repository.
---

# Yeisme Repo Routing

Use this skill when the user is adding new repository content and the correct location is unclear.

## Routing Table

| Content | Location |
| --- | --- |
| Self-built publishable skills | `my-skills/` |
| Third-party skills from skills.sh, gstack, clawhub, or similar sources | `skills/` |
| Local project agent skill installs | `.agents/skills/` |
| Local Codex skill installs | `.codex/skills/` |
| MCP servers, tools, schemas, transports, adapters | `mcp/` |
| Developer, deploy, or maintenance command wrappers | `cli/` |
| Agent runtime, product agent integrations, agent-specific assets | `agent/` |
| API gateway deployment, sidecars, runtime orchestration | `apigateway/` |
| Human-facing repository docs | `docs/` |
| Automation shared by the repository | `scripts/` |

## Decision Flow

1. If it exposes or implements MCP protocol behavior, put it in `mcp/`.
2. If it teaches an agent a reusable workflow owned by this repository, put it in `my-skills/`.
3. If it is a third-party skill installed from skills.sh, gstack, clawhub, or a similar source, put it in `skills/`.
4. If it is a command entry point tightly coupled to one MCP, keep it under `mcp/<mcp-name>/cli/`.
5. If it is a shared command entry point for humans or automation, put it in `cli/` or `scripts/` based on scope.
6. If it belongs to the API gateway runtime, put it in `apigateway/`.
7. If it belongs to a concrete agent runtime or integration, put it in `agent/`.
8. If it only explains the repository, put it in `docs/`.

## Guardrails

- Do not bury project-wide skills under implementation directories.
- Do not put executable MCP code inside a skill directory.
- Do not use `.agents/skills/` or `.codex/skills/` as the publishing source for custom skills.
- Do not put self-built skills in `skills/`; that directory is reserved for third-party skill sources.
- Do not put third-party skills in `my-skills/`.
- Prefer one clear owner directory over duplicating the same workflow in multiple places.
- Prefer CLI plus skills over MCP when an existing CLI already solves the task with less context and no cross-service reuse requirement.

## Output Style

When asked where something belongs, answer with:

- destination path
- reason
- any companion files that should be updated
- commands to validate or sync, if relevant
