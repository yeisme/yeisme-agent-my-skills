---
name: yeisme-cohors-cli-runtime
description: Use when changing, testing, reviewing, or designing Cohors CLI behavior under cli/cohors, including workflow execution, daemon JSON-RPC, Team Room, trace, TUI, templates, evals, command-center actions, and Generic CLI Runtime workers.
---

# Yeisme Cohors CLI Runtime

Use this skill for `cli/cohors`, the local-first agent team command system.

## Boundary

- CLI entrypoint: `cli/cohors/cmd/cohors/main.go`.
- Command layer: `cli/cohors/internal/cli/`.
- Runtime, daemon, projection, trace, store, templates, evals, TUI, and worker logic live under `cli/cohors/internal/`.
- Workflow fixtures live in `cli/cohors/testdata/workflows/`.
- Cohors is a Go project with its own Taskfile and release guardrails.
- Cohors checklist lifecycle follows repository-wide `docs/workflows/execution-slice-lifecycle.md`; Cohors-specific notes live in `docs/cohors/checklists/README.md`. `docs/cohors/work-items/` is not an execution checklist owner.

## Workflow

1. Read `cli/cohors/README.md` and the nearest package before editing.
2. Preserve local-first behavior:
   - durable evidence under `.cohors/runs/<run_id>/`
   - daemon uses Unix socket JSON-RPC
   - commands should work with `--json` for scripts and concise human output by default
   - CLI output changes must also follow `ai-native-cli-output-contract`
   - TUI is read-only for dangerous actions and should show copyable commands
   - CLI and TUI output follows `docs/cohors/operator-experience/terminal-output-style-system.md`
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
7. For Cohors plan/work-item execution, keep `implementation-plan.md`, `checklist.md`, `evidence.md`, and `decisions.md` together under `docs/cohors/checklists/active/<topic>/`. If a checklist appears under `docs/cohors/work-items/active/<topic>/` or another ad hoc directory, migrate it to `docs/cohors/checklists/active/<topic>/` before continuing. Close ordinary completed slices by synchronizing docs and moving `docs/cohors/checklists/active/<topic>/` to `docs/cohors/checklists/done/<topic>/`.

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
task test-race
task lint
task snapshot
```

For narrower checks:

```bash
cd cli/cohors
go test ./internal/...
task demo-dry-run
```

If CI or release behavior changes, also use the Go/GitHub release guardrails skill.

For output style changes, also verify:

```bash
cd cli/cohors
task snapshot
go test ./internal/cli ./internal/tui ./internal/output
```

If a package does not exist in the current checkout, run the closest available package tests and report the substitution.
