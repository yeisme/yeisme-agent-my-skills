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
| Human-facing repository-level docs, cross-project indexes, governance, migration notes | `docs/` |
| Subproject-owned product, design, operator, runtime, protocol, and implementation docs | `<subproject>/docs/` |
| Root OpenSpec design plans, governance, handoff, and migration records | `openspec/changes/<design-id>/` or `openspec/changes/archive/YYYY-MM-DD-<design-id>/` |
| Subproject OpenSpec implementation tasks, execution evidence, and closeout decisions | `<subproject>/openspec/changes/<change-id>/` or `<subproject>/openspec/changes/archive/YYYY-MM-DD-<change-id>/` |
| Automation shared by the repository | `scripts/` |

## Decision Flow

1. If it exposes or implements MCP protocol behavior, put it in `mcp/`.
2. If it teaches an agent a reusable workflow owned by this repository, put it in `my-skills/`.
3. If it is a third-party skill installed from skills.sh, gstack, clawhub, or a similar source, put it in `skills/`.
4. If it is a command entry point tightly coupled to one MCP, keep it under `mcp/<mcp-name>/cli/`.
5. If it is a shared command entry point for humans or automation, put it in `cli/` or `scripts/` based on scope.
6. If it belongs to the API gateway runtime, put it in `apigateway/`.
7. If it belongs to a concrete agent runtime or integration, put it in `agent/`.
8. If it is a repository-level design plan, PRD, architecture decision, governance workflow, cross-project handoff, or migration record, put `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` together under `openspec/changes/<design-id>/`, then archive to `openspec/changes/archive/YYYY-MM-DD-<design-id>/` after closeout.
9. If it tracks concrete implementation, tests, CLI/Web/TUI behavior, execution evidence, or release closeout, put the OpenSpec change under the owning subproject, for example `cli/cohors/openspec/changes/cohors-<slug>/`.
10. If it explains a concrete subproject's product, design, operator experience, runtime, protocol, implementation, QA, or release behavior, put it under that subproject's `docs/`, for example `cli/cohors/docs/`.
11. If it only explains the repository as a whole, cross-project governance, or where subproject docs live, put it in root `docs/`.

## Guardrails

- Do not bury project-wide skills under implementation directories.
- Do not put executable MCP code inside a skill directory.
- Do not use `.agents/skills/` or `.codex/skills/` as the publishing source for custom skills.
- Do not put self-built skills in `skills/`; that directory is reserved for third-party skill sources.
- Do not put third-party skills in `my-skills/`.
- Prefer one clear owner directory over duplicating the same workflow in multiple places.
- Prefer CLI plus skills over MCP when an existing CLI already solves the task with less context and no cross-service reuse requirement.
- Do not track subproject code implementation in root `openspec/`; root changes may link to subproject OpenSpec paths as handoff targets.
- Do not require subproject OpenSpec tasks to update root `docs/<project>/**`; update the owning subproject `docs/**` instead, and keep root docs as indexes or handoff links.
- Do not create execution task packages under `docs/**/checklists`, `work-items/active/`, `plans/active/`, implementation directories, or temporary directories. Those locations may link to OpenSpec changes but do not own task state.
- When creating a new subproject, bootstrap `AGENTS.md`, `CLAUDE.md`, `skills.profile`, local `openspec/`, and local `docs/README.md` before non-trivial implementation. Then run `scripts/skills.sh validate-profiles`, `scripts/skills.sh sync-subprojects`, `scripts/openspec.sh sync-tools`, and `scripts/openspec.sh validate` from the repository root.

## Output Style

When asked where something belongs, answer with:

- destination path
- reason
- any companion files that should be updated
- commands to validate or sync, if relevant
