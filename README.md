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
- User-visible skill guidance defaults to English. Use another language only when explicitly requested for that artifact, for Chinese-language product/content domains, or for quoted/source material.

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
- `yeisme-mcp-builder`: create, organize, review, and record self-built MCP capabilities under `mcp/`.
- `yeisme-mcp-gateway-operator`: operate deployed MCP Gateway instances through `mcp-gateway` CLI, Web UI, TUI, API, and the `/mcp` endpoint.
- `yeisme-mcp-gateway-maintainer`: maintain `mcp/gateway` Go Gateway behavior, CLI rendering, health checks, routing, audit, and tests.
- `yeisme-mcp-registry-onboarding`: add or review MCP backends, credentials, client rendering, Gateway exposure, and permission policies in `mcp/registry.json`.
- `yeisme-apigateway-auth-sync`: maintain Codex/Gemini CLI auth sync sidecars and new-api channel behavior in `apigateway`.
- `yeisme-cohors-cli-runtime`: develop `cli/cohors` workflow, daemon, Team Room, trace, CLI/TUI output, eval, Generic CLI Runtime, and Pi/OMP package boundaries.
- `yeisme-auctra-cli-runtime`: develop `cli/auctra` text creation pipelines, material/brief/review/export workflows, runtime provider contracts, run evidence, agent-facing CLI contracts, and TUI behavior.
- `yeisme-eikona-cli-runtime`: develop `cli/eikona` generation, reference-image editing, provider adapters, run evidence, project library, Web UI, and release behavior.
- `yeisme-indagator-cli-runtime`: develop and document `agent/indagator` CLI commands, generated command docs, Cobra/Viper config, parser/manifest/download workflows, and output contracts.
- `yeisme-taskbridge-cli-runtime`: develop `cli/taskbridge` task control plane, provider sync, action files, Agent JSON contract, and Go CLI behavior.
- `performance-profiler`: establish performance baselines, locate bottlenecks, and produce before/after optimization evidence.
- `project-integration-test-evidence`: require integration, component, system, and e2e test runs to write redacted evidence under the owning project's `temp/integration-test-runs/<run-id>/` directory.
- `ui-spec-frontend-workflow`: turn PRDs, wireframes, screenshots, or high-fidelity UI images into React UI specs, component trees, implementation constraints, animation rules, and screenshot regression loops.
- `yeisme-frontend-quality-workflow`: maintain Storybook, Tailwind stories, Chromatic, addon-designs, Lighthouse, Axe, Playwright, and browser-use frontend quality gates.
- `backend-system-workflow`: design, implement, or review backend APIs, workers, state machines, ORM/database access, Go GORM-only persistence, concurrency, permissions, observability, migrations, tests, and performance gates.
- `go-rust-implementation-defaults`: decide whether Yeisme tools, backends, CLI, MCP, daemons, workers, Gateway, and system capabilities should stay on TypeScript/Bun or move to prebuilt native packages, Pi/OMP forked packages, Go, or Rust.
- `codegraph-cli-code-intelligence`: use CodeGraph CLI to index code, query context, inspect call graphs, and analyze impact before implementation.
- `yeisme-repo-routing`: decide where new files, workflows, skills, MCP code, CLI code, agent assets, Gateway assets, and docs belong.
- `yeisme-claude-skills-layout`: design, migrate, or review the `.claude/skills` and `.agents/skills` dual active runtime managed by `skillctl`.
- `yeisme-git-worktree-flow`: use Git flow, `git worktree`, `Taskfile`, and `nerdctl compose.yml` for development.
- `yeisme-coding-execution-driver`: turn coding tasks into live checklists, execution loops, verification checkpoints, and explicit stop conditions.
- `golang-cobra-viper-cli-architecture`: enforce Yeisme Go CLI defaults around Cobra/Viper, command/config/output boundaries, and shared module extraction.
- `golang-github-release-guardrails`: enforce GitHub Actions, golangci-lint, and GoReleaser release guardrails for Go projects.
- `golang-goreleaser-distribution`: configure GoReleaser package-manager distribution, cross-repository release credentials, signing, SBOMs, and post-release install verification for Go projects.
- `internet-access`: guide agents to use local CLI-first internet research, extraction, and verification workflows before escalating to browsers.
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
