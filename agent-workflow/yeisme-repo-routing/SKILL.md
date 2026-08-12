---
name: yeisme-repo-routing
description: Use when deciding whether a proposed capability fits a Yeisme project, whether it needs split ownership, and where product surfaces, clients, services, files, workflows, skills, MCP code, CLI entrypoints, agent assets, gateway assets, or documentation should live.
---

# Yeisme Repo Routing

Use this skill when a capability is first proposed, when the user wants to merge multiple experiences into one product, or when the correct owner and repository location are unclear.

## Capability Admission Gate

Run this gate before PRD, OpenSpec, CEO review, or implementation:

1. Capture every capability the user explicitly requires in a required-capability ledger. Do not reinterpret a required capability as optional merely because delivery will be staged.
2. Classify the proposal immediately:
   - `fit`: the proposed project owns the capability's canonical state, rules, permissions, evidence, and lifecycle.
   - `split-owner`: one project owns the domain capability while another approved client or control plane composes its visual interaction, navigation, and safe actions through typed contracts.
   - `reject-now`: the capability should not be built as proposed because it violates a hard product, safety, legal, permission, or repository boundary. State this immediately, with the reason and the nearest viable alternative.
3. If the proposed project is the wrong owner, say so now. Name the correct owner, consumer, contract boundary, and how the requested user experience remains available.
4. Treat “merge into one project”, “one workspace”, and “one console” as experience composition by default. They do not authorize feature deletion, canonical-state migration, or copied domain state machines.
5. Carry the admission decision and required-capability ledger into later PRD, CEO, architecture, engineering, design, and OpenSpec work. Do not wait until the spec is complete to raise a known ownership mismatch.

Full continuity rules are in `docs/workflows/product-capability-admission-and-scope-governance.md`.

## Routing Table

| Content | Location |
| --- | --- |
| Self-built publishable skills | `.skills/yeisme/` |
| Third-party skills from skills.sh, gstack, clawhub, or similar sources | `.skills/imported/` |
| Local project agent skill installs | `.agents/skills/` |
| Local Codex skill installs | `.codex/skills/` |
| MCP servers, tools, schemas, transports, adapters | `mcp/` |
| CLI-first product owners, domain runtimes, operator and automation entrypoints | `cli/` |
| Agent products, orchestration runtimes, product-agent integrations, agent-specific assets | `agent/` |
| Approved independent Web, desktop, mobile, or cross-platform product clients | `client/` |
| Long-running product backends, workers, bridges, and service APIs | `backend-server/` |
| API gateway deployment, sidecars, runtime orchestration | `apigateway/` |
| Human-facing repository-level docs, cross-project indexes, governance, migration notes | `docs/` |
| Subproject-owned product, design, operator, runtime, protocol, and implementation docs | `<subproject>/docs/` |
| Root OpenSpec design plans, governance, handoff, and migration records | `openspec/changes/<design-id>/` or `openspec/changes/archive/YYYY-MM-DD-<design-id>/` |
| Subproject OpenSpec implementation tasks, execution evidence, and closeout decisions | `<subproject>/openspec/changes/<change-id>/` or `<subproject>/openspec/changes/archive/YYYY-MM-DD-<change-id>/` |
| Automation shared by the repository | `scripts/` |

## Decision Flow

1. If it exposes or implements MCP protocol behavior, put it in `mcp/`.
2. If it teaches an agent a reusable workflow owned by this repository, put it in `.skills/yeisme/`.
3. If it is a third-party skill installed from skills.sh, gstack, clawhub, or a similar source, put it in `.skills/imported/`.
4. If it is a command entry point tightly coupled to one MCP, keep it under `mcp/<mcp-name>/cli/`.
5. If it is an approved independent product client consuming stable owner APIs, events, resources, or SDKs, put it in `client/<name>/`; do not put domain business rules there.
6. If it is a long-running product backend, worker, bridge, or service API with its own state and operations boundary, put it in `backend-server/<name>/`.
7. If it is a CLI-first domain product or a shared operator/automation entrypoint, put it in `cli/<name>/`; the directory name does not limit the product to command-line UX, but independent clients still require their own owner.
8. If it belongs to the API gateway runtime, put it in `apigateway/`.
9. If it belongs to a concrete agent product, orchestration runtime, or integration, put it in `agent/`.
10. If it is a repository-level design plan, PRD, architecture decision, governance workflow, cross-project handoff, or migration record, put `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` together under `openspec/changes/<design-id>/`, then archive to `openspec/changes/archive/YYYY-MM-DD-<design-id>/` after closeout.
11. If it tracks concrete implementation, tests, CLI/API/Web/TUI behavior, execution evidence, or release closeout, put the OpenSpec change under the owning subproject, for example `cli/cohors/openspec/changes/cohors-<slug>/`.
12. If it explains a concrete subproject's product, design, operator experience, runtime, protocol, implementation, QA, or release behavior, put it under that subproject's `docs/`, for example `cli/cohors/docs/`.
13. If it only explains the repository as a whole, cross-project governance, or where subproject docs live, put it in root `docs/`.

## Guardrails

- Do not bury project-wide skills under implementation directories.
- Do not put executable MCP code inside a skill directory.
- Do not use `.agents/skills/` or `.codex/skills/` as the publishing source for custom skills.
- Do not put self-built skills in `.skills/imported/`; that directory is reserved for third-party skill sources.
- Do not put third-party skills in `.skills/yeisme/`.
- Prefer one clear owner directory over duplicating the same workflow in multiple places.
- Preserve user-required capabilities across owner routing. Moving a capability behind a typed owner contract is not permission to remove it from the product experience.
- If new evidence later changes an admission decision, state the evidence, affected capabilities, migration or compatibility impact, and required user decision before changing scope.
- Treat CLI/API/event/resource contracts as reusable product interfaces, not as proof that a project must remain CLI-only.
- Route independent UI implementations to an approved `client/<name>` owner; keep durable domain state, provider adapters, evidence, and business rules in the domain subproject.
- Prefer CLI plus skills over MCP when an existing CLI already solves the task with less context and no cross-service reuse requirement.
- Do not track subproject code implementation in root `openspec/`; root changes may link to subproject OpenSpec paths as handoff targets.
- Do not require subproject OpenSpec tasks to update root `docs/<project>/**`; update the owning subproject `docs/**` instead, and keep root docs as indexes or handoff links.
- Do not create execution task packages under `docs/**/checklists`, `work-items/active/`, `plans/active/`, implementation directories, or temporary directories. Those locations may link to OpenSpec changes but do not own task state.
- When creating a new subproject, bootstrap `AGENTS.md`, `CLAUDE.md`, the root-level `.skills/profiles/targets/<subproject>.txt`, local `openspec/`, and local `docs/README.md` before non-trivial implementation. Then run `scripts/skills.sh validate-profiles`, `scripts/skills.sh sync-subprojects`, `scripts/openspec.sh sync-tools`, and `scripts/openspec.sh validate` from the repository root.

## Output Style

When asked where something belongs, answer with:

- admission decision: `fit`, `split-owner`, or `reject-now`
- destination path
- reason
- required-capability impact: retained, staged, moved behind a contract, or explicitly awaiting a user removal decision
- experience composition: where the user sees and controls the capability
- any companion files that should be updated
- commands to validate or sync, if relevant
