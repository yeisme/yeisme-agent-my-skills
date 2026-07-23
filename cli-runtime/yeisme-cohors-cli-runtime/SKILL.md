---
name: yeisme-cohors-cli-runtime
description: Use when changing, testing, reviewing, or designing the accepted Cohors Personal Company product runtime under cli/cohors, including its current CLI/read-only TUI scope, run projections, bounded adapters, evidence, and any explicitly approved workflow, daemon, Team Room, trace, template, eval, or command-center expansion.
---

# Yeisme Cohors CLI Runtime

Use this skill for `cli/cohors`, the local-first Personal Company product runtime currently delivered through a bounded CLI and read-only single-screen TUI. Product framing does not authorize deferred daemon, Team Room, worker, memory, or Web scope without an accepted OpenSpec change.

## Boundary

- CLI entrypoint: `cli/cohors/src/bin/cohors.ts`.
- Command layer: `cli/cohors/src/cli/`.
- Pi kernel, projections, run state, trace, sandbox, worker contracts, and scheduler logic live under `cli/cohors/src/pi/`.
- Runtime, daemon, store, templates, evals, TUI, and worker integrations live under `cli/cohors/src/`.
- Workflow fixtures live in `cli/cohors/testdata/workflows/`.
- Cohors is a Bun-first TypeScript project. Bun 1.3.14+ remains the default runtime and package manager. Native/system capabilities may consume `@oh-my-pi/pi-natives`, `@oh-my-pi/pi-tui`, or a `packages/natives` TS wrapper only when performance or system capability requires it; local Rust crates and vendored Pi / OMP source trees are not the default Cohors development path. Node.js is only a compatibility build target, not the default runtime path.
- Cohors task lifecycle follows repository-wide OpenSpec rules in root `docs/workflows/execution-slice-lifecycle.md`; migrated Cohors notes live in `openspec/changes/archive/2026-05-11-cohors-checklists-index/legacy/README.md`. In a `cli/cohors` session, Cohors product/design/operator docs live in local `docs/**`; root project-doc mirrors are not task-state owners and must not be required for closeout.

## Workflow

1. Read `cli/cohors/README.md` and the nearest package before editing.
2. Preserve local-first behavior:
   - durable evidence under `.cohors/runs/<run_id>/`
   - daemon uses Unix socket JSON-RPC
   - commands should work with `--json` for scripts and concise human output by default
   - agent-facing commands should expose `--agent` key=value output where useful
   - CLI output changes must also follow `ai-native-cli-output-contract`
   - TUI is read-only for dangerous actions and should show copyable commands
   - CLI and TUI output follows `docs/operator-experience/terminal-output-style-system.md`
   - CLI, TUI, daemon, and tests consume Pi projections instead of parsing localized human output
3. For Generic CLI Runtime changes:
   - use structured argv, not shell string concatenation
   - keep prompt modes explicit: `stdin`, `file`, or `arg`
   - require fenced `yeisme-result` when structured output is expected
   - emit useful trace events for failures, approvals, locks, and sandbox violations
4. For CEO readiness and CEO Cockpit behavior:
   - `cohors status --ceo` may stay as a fast read-only projection, but it must not be described as CEO reasoning.
   - use `cohors status --ceo --think` when the product needs a real CEO agent to inspect current progress and decide next work.
   - the CEO agent prompt must explicitly ask for current work progress, next work content, and skill/prompt improvements; it must cite local evidence paths or run ids.
   - CEO thinking must go through Generic CLI Runtime and leave durable evidence under `.cohors/runs/<run_id>/`, including workflow, logs, trace, and normalized `yeisme-result`.
   - dangerous actions remain previews; the CEO agent does not approve, delete, push, deploy, or mutate project files unless a separate explicit workflow grants that boundary.
5. Keep local project docs and OpenSpec artifacts in Chinese by default. Keep CLI help text, CLI output, logs, user-visible errors, public reports, and `--explain` summaries in English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
6. Add tests at the package closest to the behavior. Prefer fixtures in `testdata/workflows/` for workflow contracts.
7. For Cohors plan/work-item execution, keep task state in `openspec/changes/cohors-<topic>/` with `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md`. If a task checklist appears under `docs/checklists`, `docs/work-items/active/<topic>/`, `docs/plans/active`, root project-doc mirrors, root `openspec/` for code work, or another ad hoc directory, migrate it to `openspec/changes/cohors-<topic>/` before continuing. Close ordinary completed changes by synchronizing local `docs/**` and specs, then moving the change to `openspec/changes/archive/YYYY-MM-DD-cohors-<topic>/`.

## Terminal Output Constraints

When designing or changing Cohors CLI/TUI output:

- Use the high-level human output skeleton: `Status`, `Highlights`, optional `Risks`, optional `Evidence`, and one `Recommended next step`.
- Keep default text output human-oriented; scripts must use `--json`.
- Do not mix ANSI color, progress text, logs, or suggestions into `--json` stdout.
- Use stable projection data, not parsed localized CLI text, as the source for CLI, TUI, tests, and snapshots.
- Treat `--agent` as the preferred new agent-facing flag; keep `--format ai` compatibility where existing Cohors commands already expose it.
- Preserve English visible text by default; command names, flags, schema fields, paths, and third-party names remain English or existing stable names.
- Provide `NO_COLOR` / `--color never` safe rendering when color is involved.
- TUI must keep dangerous actions as copyable command previews unless daemon-audited structured actions and confirmation paths exist.
- TUI mouse support is required for tabs, rows, scrolling, focus changes, and visible clickable regions.

## Agent Report Contracts

When Cohors asks an agent to produce review, platform, content, metadata, or handoff reports, prefer YAML over raw JSON:

- Agent-authored reports should be fenced as `yaml` and remain readable by humans in run evidence, handoff notes, and review artifacts.
- Do not ask agents to emit bare JSON as the primary report format. If a CLI command needs `--json`, Cohors should parse or project the structured report into the normal AI Native JSON envelope itself.
- Keep field names stable ASCII and snake_case so YAML reports can be validated and converted to CLI projections without localized-key parsing.
- For content platform review, include one report item per publishable unit. Use 0-10 integer scores where 10 means strongest or lowest risk for `risk`.
- Findings should point to a stable span such as `title`, `hook`, `body.p2`, `cta`, `cover_text`, or `tags[2]`, and recommendations should be concrete enough for the next editing pass.

Content platform report shape:

```yaml
unit_id: note_001
platform: xiaohongshu
score:
  hook: 8
  concreteness: 7
  audience_fit: 8
  platform_fit: 7
  risk: 9
findings:
  - severity: medium
    type: generic_claim
    span: body.p2
    issue: 观点成立，但缺少可感知细节。
    recommendation: 补入具体场景、价格、时间、路线或个人判断依据。
```

## TypeScript CLI/TUI Preset

When designing or changing Cohors CLI or TUI internals, use `cli/cohors/docs/design/cli-toolkit-and-tui-standards.md` as the default implementation standard.
For backend daemon, CLI target selection, optional remote server, and opencode-style C/S behavior, also use `cli/cohors/docs/design/backend-cli-remote-runtime.md`.
For Pi native package boundaries, native/fallback policy, and performance gates, also use `cli/cohors/docs/design/pi-native-package-integration.md`.

Default stack:

- Bun 1.3.14+ is the runtime, package manager, test runner, and binary build path.
- TypeScript/Bun owns the mainline: CLI UX, Pi projection, provider/protocol adapters, config, plugins, TUI glue, output renderers, run evidence, worker contracts, and typed facades.
- Native/system capabilities may use `@oh-my-pi/pi-natives` or `packages/natives` only as an optional external/native package boundary for measured hotspots or system primitives: AST, shell/PTY/process primitive, task isolation, filesystem primitive, hashline/search hot paths, and large-file hashing.
- Pi / OMP dependency ownership is package-first: use released npm packages by default; use a fixed Git ref or patch only as a short-lived bridge to an upstream release; fork only when Cohors must maintain native/runtime differences and publish a scoped package; do not add `earendil-works/pi`, `oh-my-pi`, or similar upstream source repositories as default `cli/cohors` submodules.
- Local Rust development is only for fork/patch/upstream work on that native package. Go is not the default Cohors native layer; use Go for other Yeisme backend/CLI/MCP/gateway projects or clearly separate services.
- TypeScript runs in strict mode; public argv, config, projection, protocol, provider, and event inputs need typed boundaries.
- Keep the current lightweight command registry until the command tree needs a full framework. If a framework is justified, prefer Clipanion for type-safe command trees or Commander for simple Cobra-like UX. Do not default to Yargs or Oclif without a clear product reason.
- Use Zod for external input validation when argv/config/projection/protocol payloads cross trust boundaries.
- Use yoctocolors or chalk for color, with `NO_COLOR=1` and `--color auto|always|never` support.
- Use string-width, wrap-ansi, and slice-ansi for terminal width handling when rendering help, lists, tables, or TUI text.
- Use @inquirer/prompts only for low-risk interactive CLI prompts; dangerous actions stay as command previews unless audited daemon actions exist.
- Use `@oh-my-pi/pi-tui` for OMP-like Cohors command center work by default: differential rendering, synchronized output, Editor, Markdown, SelectList, SettingsList, Loader, VirtualTerminal, autocomplete, key detection, and width utilities. Ink + React is optional for isolated React-style experiments, not the default TUI engine.
- For UI detail, component states, performance budgets, and development monitoring, also follow `cli/cohors/docs/design/tui-ui-performance-standards.md`.

Cobra-like CLI requirements:

- Every command exposes stable metadata: command id, path, summary, description, usage, aliases, flags, examples, and exit codes.
- Help text is generated from metadata and uses English descriptions with runnable command examples.
- Unknown commands and invalid flags should return usage errors with a concrete suggestion when possible.
- Commands return typed Pi projections; renderers produce human summary, `--json`, `--agent`, `--events`, and `--explain` from that same projection.
- `--json` stdout is JSON only. `--agent` stdout is stable ASCII `key=value`. Human output uses `Status`, `Highlights`, optional `Risks`, optional `Evidence`, and one `Recommended next step`.

OMP-like TUI requirements:

- TUI is an interactive command center, not formatted logs.
- Visual direction is calm, precise, Apple-like, and utility-focused: light separators, stable spacing, restrained color, no noisy banners or decorative clutter.
- Layouts must remain usable at `80x24` and comfortable at `120x40`.
- Tabs, rows, buttons, scroll areas, and focus panes must work by keyboard and mouse.
- Hover, selected, focused, disabled, loading, empty, degraded, error, and success states must be visually distinct.
- Mouse events produce intents such as `switchTab`, `selectRow`, `openDetail`, `scrollPane`, or `copyCommand`; they must not directly execute destructive side effects.
- Dangerous actions in TUI remain copyable command previews until daemon-audited confirmation and trace evidence exist.
- The bottom prompt editor is the primary input surface. It should support slash commands, file attach/autocomplete, multi-line editing, cancellable loaders, command palette, and artifact/markdown rendering.
- Add TUI dependencies only when the first TUI implementation slice starts. The preferred first install set is `@oh-my-pi/pi-tui`, `zod`, and `chalk`; add `clipanion` only when the command tree outgrows the lightweight registry.
- TUI work must include performance budgets and probes: startup, render duration, input latency, changed lines, full repaint count, event queue depth, trace ingest lag, markdown/width cache hit rates, and RSS/heap usage.
- Keep perf diagnostics out of `--json` and `--agent` stdout. Use `.cohors/perf/` for local evidence and redact prompts, provider payloads, tokens, credentials, and private request data.

Backend/remote requirements:

- Direct CLI commands such as `status`, `version`, and `config path` must not start daemon or remote services.
- Long-running run, worker, trace, approval, and protocol gateway commands may use a local daemon with lazy start and idle timeout.
- Local daemon uses Unix socket or Windows named pipe JSON-RPC by default; it must not bind a network port unless `cohors serve` is explicitly used.
- Optional remote server follows opencode-style C/S shape: headless HTTP server, OpenAPI 3.1 schema, SSE events, `attach` clients, and typed SDK compatibility.
- Remote server is disabled by default. Non-localhost bind requires explicit `--remote` and authentication through `COHORS_SERVER_TOKEN` or a documented auth mode.
- Local provider credentials may be stored only in user-level local config, a user-level secret store, or the configured auth backend. Workspace/project config should store account handles, env names, secret refs, route policy, and readiness metadata, not literal secret values.
- Remote CORS and mDNS are off by default and must be explicitly enabled.
- Remote endpoints must expose Cohors projections and audited actions, not arbitrary file read, arbitrary shell execution, raw provider payloads, or unredacted secrets.
- Resource control is part of the design: idle timeout, worker TTL, max concurrency, provider/protocol health TTL, bounded SSE clients, and event ring buffers.
- CLI target selection order is explicit `--attach`/URL, configured remote profile, local daemon, then direct fast path.

Pi native package requirements:

- Cohors must be treated as TypeScript/Bun-first. Native package integration is optional and evidence-driven.
- Native package access must be lazy loaded through `src/native/**` and optional `packages/natives/**` facades and must not be required for direct `status`, `version`, or `config path`.
- Native features need capability projection and fallback state: at least `native_package`, `ast`, `shell`, `iso`, `sandbox`, `search`, and `hashline`.
- Native package wrappers must not implement provider adapters, localized CLI/TUI rendering, provider prompt policy, approval product policy, or Pi projection ownership.
- Native package APIs accept structured options and return typed data; no shell string APIs.
- Native package errors must be converted to redacted typed errors before reaching CLI, JSON, agent, trace, or run evidence.
- Prefer staying in TypeScript/Bun unless there is measured performance pressure or a system primitive that a maintained package already solves. Add `packages/natives` only when Cohors needs a stable wrapper surface, compatibility shim, or feature projection.
- Do not create `native/Cargo.toml`, local Rust crates, vendored `brush-*`, or Pi / OMP source submodules by default. Add local Rust only for an explicit fork/patch/upstream plan with license, version lock, prebuild CI, fallback, and rollback strategy.
- If a native/runtime capability needs upstream source changes, prefer fork + scoped package over a Cohors submodule. The fork must keep product policy out of native code and expose typed APIs back to TypeScript/Bun.

Preferred source layout:

```text
src/cli/command.ts
src/cli/execute.ts
src/cli/errors.ts
src/cli/help.ts
src/cli/render.ts
src/cli/color.ts
src/cli/width.ts
src/tui/app.ts
src/tui/theme.ts
src/tui/layout.ts
src/tui/input.ts
src/tui/editor.ts
src/tui/perf.ts
src/tui/mouse.ts
src/tui/registry.ts
src/daemon/server.ts
src/daemon/socket.ts
src/daemon/lease.ts
src/server/http.ts
src/server/openapi.ts
src/remote/client.ts
src/remote/profile.ts
src/native/client.ts
src/native/capabilities.ts
src/native/ast.ts
src/native/shell.ts
src/native/iso.ts
src/native/hashline.ts
packages/natives/package.json
packages/natives/src/index.ts
```

## Validation

```bash
cd cli/cohors
task test
task build
bun run typecheck
./dist/cohors status --json
bun run perf:discover
```

For narrower checks:

```bash
cd cli/cohors
bun run test
bun run build
./dist/cohors status --json
bun src/bin/cohors.ts status --json
bun src/bin/cohors.ts status --agent
bun run perf:build
bun run perf:test
```

For output style changes, also verify:

```bash
cd cli/cohors
bun run test
bun run build
./dist/cohors status --json
bun src/bin/cohors.ts status --json
bun src/bin/cohors.ts status --agent
```

If a package does not exist in the current checkout, run the closest available package tests and report the substitution.
