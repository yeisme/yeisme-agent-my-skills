---
name: yeisme-cohors-cli-runtime
description: Use when changing, testing, reviewing, or designing Cohors CLI behavior under cli/cohors, including workflow execution, daemon JSON-RPC, Team Room, trace, TUI, templates, evals, command-center actions, and Generic CLI Runtime workers.
---

# Yeisme Cohors CLI Runtime

Use this skill for `cli/cohors`, the local-first agent team command system.

## Boundary

- CLI entrypoint: `cli/cohors/src/bin/cohors.ts`.
- Command layer: `cli/cohors/src/cli/`.
- Pi kernel, projections, run state, trace, sandbox, worker contracts, and scheduler logic live under `cli/cohors/src/pi/`.
- Runtime, daemon, store, templates, evals, TUI, and worker integrations live under `cli/cohors/src/`.
- Workflow fixtures live in `cli/cohors/testdata/workflows/`.
- Cohors is a TypeScript project using Node.js 22+, npm, and its own Taskfile.
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
5. Keep user-visible docs, logs, help text, and reports in Chinese unless the string is a protocol field, code identifier, or third-party term.
6. Add tests at the package closest to the behavior. Prefer fixtures in `testdata/workflows/` for workflow contracts.
7. For Cohors plan/work-item execution, keep task state in `openspec/changes/cohors-<topic>/` with `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md`. If a task checklist appears under `docs/checklists`, `docs/work-items/active/<topic>/`, `docs/plans/active`, root project-doc mirrors, root `openspec/` for code work, or another ad hoc directory, migrate it to `openspec/changes/cohors-<topic>/` before continuing. Close ordinary completed changes by synchronizing local `docs/**` and specs, then moving the change to `openspec/changes/archive/YYYY-MM-DD-cohors-<topic>/`.

## Terminal Output Constraints

When designing or changing Cohors CLI/TUI output:

- Use the high-level human output skeleton: `状态`, `重点`, optional `风险`, optional `证据`, and one `推荐下一步`.
- Keep default text output human-oriented; scripts must use `--json`.
- Do not mix ANSI color, progress text, logs, or suggestions into `--json` stdout.
- Use stable projection data, not parsed Chinese CLI text, as the source for CLI, TUI, tests, and snapshots.
- Treat `--agent` as the preferred new agent-facing flag; keep `--format ai` compatibility where existing Cohors commands already expose it.
- Preserve Chinese-visible text by default; command names, flags, schema fields, paths, and third-party names may remain English.
- Provide `NO_COLOR` / `--color never` safe rendering when color is involved.
- TUI must keep dangerous actions as copyable command previews unless daemon-audited structured actions and confirmation paths exist.
- TUI mouse support is required for tabs, rows, scrolling, focus changes, and visible clickable regions.

## Validation

```bash
cd cli/cohors
task test
task build
npm run typecheck
```

For narrower checks:

```bash
cd cli/cohors
npm test
node dist/src/bin/cohors.js status --json
node dist/src/bin/cohors.js status --agent
```

For output style changes, also verify:

```bash
cd cli/cohors
npm test
node dist/src/bin/cohors.js status --json
node dist/src/bin/cohors.js status --agent
```

If a package does not exist in the current checkout, run the closest available package tests and report the substitution.
