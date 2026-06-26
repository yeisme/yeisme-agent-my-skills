# Project Skills

`.skills/yeisme/` is the source directory for this repository's self-built, publishable, syncable skills. These skills guide agent execution. They are not ordinary product docs, MCP implementations, CLI code, agent runtime code, or Gateway implementation code.

## Directory Contract

- `.skills/yeisme/`: publishable source for project-owned skills.
- `.skills/imported/`: local source for third-party skills installed from `skills.sh`, gstack, clawhub, or similar sources.
- `.skills/profiles/root.txt`: root-session skill profile.
- `.skills/profiles/targets/<subproject>.txt`: subproject skill profiles.
- `.agents/skills/`: generated agent runtime copies for this repository, produced by `scripts/skills.sh sync-root` from the root profile.
- `.claude/skills/`: generated Claude Code runtime copies mirrored from the same `scripts/skills.sh` workflow.
- `.codex/skills/`: not used for this repository's self-built skills.
- `docs/skills/`: skill authoring rules, indexes, and layering docs.
- `mcp/`: MCP servers, tools, transports, schemas, adapters, and debug entrypoints.

Do not put MCP implementations in `.skills/yeisme/`. A skill may explain how to create or review an MCP, but actual MCP code belongs under `mcp/`.
Do not put external skills installed from `skills.sh`, gstack, clawhub, or other sources in `.skills/yeisme/`. Third-party/imported skills belong in `.skills/imported/`; profile files assign them; runtime copies belong in `.agents/skills/` and `.claude/skills/`.

## Self-built Skill Shape

Yeisme self-built skills must use this structure:

```text
.skills/yeisme/<module>/<skill-name>/
  SKILL.md
  agents/openai.yaml
```

Optional directories may be added only when directly useful:

- `scripts/`: stable, repeatable helper scripts that need deterministic execution.
- `references/`: detailed material loaded only when needed.
- `assets/`: templates, images, fonts, or sample files copied into or used to generate output.

Do not add extra `README.md`, `CHANGELOG.md`, or `QUICK_REFERENCE.md` files inside an individual skill directory. `SKILL.md` is the agent-facing contract.

## `SKILL.md` Requirements

Frontmatter must include:

```yaml
---
name: skill-name
description: Use when ...
---
```

Requirements:

- `name` must match the directory name.
- `description` must state trigger conditions, task object, and scope.
- `description` should start with `Use when ...`.
- `description` must not be generic, such as "Helpful skill for developers".
- The body must describe when to use the skill, inputs, outputs, workflow, boundaries, and validation.
- Keep the body concise; move detailed background into `references/`.
- Examples must show real commands a user can run. Do not put local execution wrappers, shell aliases, or agent-only prefixes in skill bodies, docs, or final replies.
- Skill trigger metadata and command examples should stay English or existing stable names for portability. When a skill produces or updates human-authored project docs, plans, reviews, handoffs, or OpenSpec artifacts, those artifacts default to Chinese unless a subproject explicitly marks them as public English documentation.

## `agents/openai.yaml` Requirements

Required fields:

```yaml
display_name: Human Friendly Name
short_description: One-sentence visible summary.
default_prompt: A concrete starting prompt for this skill.
```

Requirements:

- `display_name` is human-readable.
- `short_description` must match the scope of `SKILL.md description`.
- `default_prompt` must be a directly executable starting task.
- When changing `SKILL.md` trigger scope, also review `agents/openai.yaml`.

## Duplicate Skill Guardrail

Project-owned skills have one source and profile-generated runtime copies:

```text
.skills/yeisme/<module>/<skill-name>/       self-built publishable source
.agents/skills/<skill-name>/                root profile runtime copy
.claude/skills/<skill-name>/                Claude Code root profile runtime copy
<subproject>/.agents/skills/<skill-name>/   subproject profile runtime copy
```

Do not create or maintain:

```text
.codex/skills/<skill-name>/
```

Duplicate checks:

```bash
find .codex/skills -maxdepth 2 -name SKILL.md 2>/dev/null | sort
find .skills/yeisme -maxdepth 2 -mindepth 2 -type l -print
```

If Codex/Agent sees duplicate self-built skills, keep only the `.skills/yeisme/<module>/<skill-name>/` source and let profiles decide whether to generate root or subproject runtime copies. Do not put external packages, symlinks, or runtime copies in `.skills/yeisme/`.

## Current Self-built Skills

- `yeisme-skill-publisher`: create, validate, sync, and publish self-built skills under `.skills/yeisme/`.
- `ai-native-cli-output-contract`: shared CLI contract for default summaries, `--agent`, `--json`, `--events`, `--explain`, envelopes, redaction, and contract tests.
- `yeisme-evolutionary-change-policy`: block generation-breaking (断代) updates across CLI output, RPC/API, database migrations, config/registry, public Go/TS APIs, and skill schemas; force incremental backward-compatible evolution with an OpenSpec gate.
- `yeisme-mcp-builder`: create, organize, review, and record self-built MCP capabilities under `mcp/`.
- `yeisme-mcp-gateway-operator`: operate deployed MCP Gateway instances through `mcp-gateway` CLI, Web UI, TUI, API, and the `/mcp` endpoint.
- `yeisme-mcp-gateway-maintainer`: maintain `mcp/gateway` Go Gateway behavior, CLI rendering, health checks, routing, audit, and tests.
- `yeisme-mcp-registry-onboarding`: add or review MCP backends, credentials, client rendering, Gateway exposure, and permission policies in `mcp/registry.json`.
- `yeisme-cohors-cli-runtime`: develop `cli/cohors` workflow, daemon, Team Room, trace, CLI/TUI output, eval, Generic CLI Runtime, and Pi/OMP package boundaries.
- `yeisme-auctra-cli-runtime`: develop `cli/auctra` text creation pipelines, material/brief/review/export workflows, runtime provider contracts, run evidence, agent-facing CLI contracts, and TUI behavior.
- `yeisme-eikona-cli-runtime`: develop or document `cli/eikona` generation, prompt skills/decks, visual assessment, recipe reuse, provider adapters, run evidence, project library, Web/API/MCP surfaces, and release behavior.
- `eikona-xhs-visual-router`: route Xiaohongshu static visual requests to the smallest Eikona image director while preserving review, feedback, and handoff evidence.
- `eikona-xhs-cover-director`: design Xiaohongshu title-safe cover visuals, candidate directions, Eikona commands, and review handoff steps.
- `eikona-xhs-card-series-director`: split Xiaohongshu posts into 3/6/9-page static card series with page plans, prompts, Eikona commands, and review handoff steps.
- `eikona-xhs-infographic-director`: turn sourced facts, processes, comparisons, or checklists into Xiaohongshu infographics with fact-preserving Eikona evidence.
- `eikona-xhs-comic-director`: design original-character Xiaohongshu comic-style static posts with page briefs, Eikona commands, and review handoff steps.
- `yeisme-indagator-cli-runtime`: develop and document `agent/indagator` CLI commands, generated command docs, Cobra/Viper config, parser/manifest/download workflows, and output contracts.
- `yeisme-gitpulse-cli-runtime`: develop, review, or operate `cli/gitpulse` Git workflow orchestration, worktrees, PR flow, TUI behavior, output contracts, and Go validation.
- `yeisme-pinax-cli-runtime`: develop, review, or operate `cli/pinax` local indexing, proof-loop, project workspace, templates, assets/prompt collections, plugin/API/MCP, profile management, publish/sync daemon, backend client behavior, credentials, evidence, and Go validation.
- `pinax-agent-router`: route generic note completion and Pinax operational tasks, including writing/saving notes, retrieval, memory, proof, project, template, asset/prompt, sync/storage, publish, API, plugin, and MCP work, to the narrowest operator skill.
- `pinax-vault-operator`: safely initialize/select Pinax vaults, write or capture notes through `notes/index`, append inbox/journal content, manage drafts, import/export Markdown, and handle ordinary note lifecycle through real Pinax commands.
- `pinax-retrieval-operator`: retrieve bounded context from Pinax indexes, search, links/backlinks/orphans, KB, saved views, folders, database/dataview, and controlled query commands.
- `pinax-memory-operator`: capture and recall deterministic Pinax memory records for facts, decisions, events, and tasks; avoid reserved `memory link/prune` workflows.
- `pinax-sync-storage-operator`: configure and operate Pinax Cloud Sync, sync daemon/logs/conflicts, S3/rclone storage, backend profiles, backend object diagnostics, sync plans, and storage diagnostics without exposing credentials.
- `pinax-proof-maintenance-operator`: run Pinax proof loops, doctor/stats, metadata/repair/organize plans and applies, version snapshot/restore, and record-ledger maintenance with snapshot and approval gates.
- `pinax-project-workspace-operator`: manage Pinax project workspaces, learning packs, subprojects, boards, work items, personal plans, TaskBridge action drafts, and plan snapshots.
- `pinax-template-authoring-operator`: manage Pinax templates, template-backed note creation, template previews/renders/runs, managed index pages, inbox/draft indexes, and journal template workflows.
- `pinax-asset-prompt-operator`: manage Pinax assets, note attachments, prompt assets, content collections, and local graph projections through bounded commands.
- `pinax-integration-publish-operator`: operate Pinax publish, plugin, local API, API token, profile alias, MCP, and briefing workflows with read-only defaults and credential-safe approvals.
- `yeisme-quaestor-cli-runtime`: develop, review, or operate `cli/quaestor` query/research workflows, output contracts, evidence boundaries, adapters, and Go validation.
- `yeisme-taskbridge-cli-runtime`: develop `cli/taskbridge` task control plane, provider sync, action files, Agent JSON contract, and Go CLI behavior.
- `yeisme-hermes-communication-routing`: design or review provider-neutral Yeisme communication delivery through Hermes across notifications, commands, approvals, artifacts, handoffs, and future chat providers.
- `yeisme-feishu-hermes-integration`: design or review Feishu/Lark collaboration integration through Hermes provider-neutral commands, events, routing, credential safety, and redacted evidence.
- `yeisme-telegram-hermes-integration`: design or review Telegram integration through Hermes provider-neutral commands, Bot API boundaries, credential safety, chat/thread identity, and redacted evidence.
- `performance-profiler`: establish performance baselines, locate bottlenecks, and produce before/after optimization evidence.
- `project-integration-test-evidence`: require integration, component, system, and e2e test runs to write redacted evidence under the owning project's `temp/integration-test-runs/<run-id>/` directory.
- `ui-spec-frontend-workflow`: turn PRDs, wireframes, screenshots, or high-fidelity UI images into React UI specs, component trees, implementation constraints, animation rules, and screenshot regression loops.
- `yeisme-frontend-quality-workflow`: maintain Storybook, Tailwind stories, Chromatic, addon-designs, Lighthouse, Axe, Playwright, and browser-use frontend quality gates.
- `yeisme-frontend-design-router`: route frontend design, UI generation, redesign, Open Design, Taste, Impeccable, browser visual QA, component sourcing, and canvas UI tasks to the smallest non-conflicting skill chain.
- `backend-system-workflow`: design, implement, or review backend APIs, workers, state machines, ORM/database access, Go GORM-only persistence, concurrency, permissions, observability, migrations, tests, and performance gates.
- `go-rust-implementation-defaults`: decide whether Yeisme tools, backends, CLI, MCP, daemons, workers, Gateway, and system capabilities should stay on TypeScript/Bun or move to prebuilt native packages, Pi/OMP forked packages, Go, or Rust.
- `codegraph-cli-code-intelligence`: use CodeGraph CLI to index code, query context, inspect call graphs, and analyze impact before implementation.
- `yeisme-repo-routing`: decide where new files, workflows, skills, MCP code, CLI code, agent assets, Gateway assets, and docs belong.
- `yeisme-local-backup-sync-policy`: guide cross-project Git-managed local state plus S3-compatible, rclone, and cloud-drive backup/restore policy for `.eikona`, `.auctra`, `.indagator`, `.scaena`, `.pinax`, and `.gitpulse`, while keeping real-time sync as a separate design.
- `yeisme-claude-skills-layout`: design, migrate, or review the `.claude/skills` and `.agents/skills` dual active runtime managed by `skillctl`.
- `yeisme-git-worktree-flow`: use Git flow, `git worktree`, `Taskfile`, and `nerdctl compose.yml` for development.
- `yeisme-coding-execution-driver`: turn coding tasks into live checklists, execution loops, verification checkpoints, and explicit stop conditions.
- `golang-cobra-viper-cli-architecture`: enforce Yeisme Go CLI defaults around Cobra/Viper, command/config/output boundaries, and shared module extraction.
- `golang-github-release-guardrails`: enforce GitHub Actions, golangci-lint, and GoReleaser release guardrails for Go projects.
- `golang-goreleaser-distribution`: configure GoReleaser package-manager distribution, cross-repository release credentials, signing, SBOMs, and post-release install verification for Go projects.
- `internet-access`: guide agents to use Agent Reach platform routing plus local CLI-first internet research, extraction, verification, and browser escalation workflows.
- `tui-design-standards`: require mouse support and polished, restrained, Apple-like terminal UI quality when reviewing or implementing TUIs.

## Validation And Sync

Run after adding or changing self-built skills:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
scripts/skills.sh list-custom
```

Install self-built skills from a remote repository:

```bash
scripts/skills.sh install-custom <repo-url> [ref]
```

For detailed authoring rules, see [docs/skills/skills-authoring.md](../../docs/skills/skills-authoring.md).
