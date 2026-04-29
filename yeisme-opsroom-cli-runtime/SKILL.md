---
name: yeisme-opsroom-cli-runtime
description: Use when changing, testing, reviewing, or designing Opsroom CLI behavior under cli/opsroom, including workflow execution, daemon JSON-RPC, Team Room, trace, TUI, templates, evals, command-center actions, and Generic CLI Runtime workers.
---

# Yeisme Opsroom CLI Runtime

Use this skill for `cli/opsroom`, the local-first agent team command system.

## Boundary

- CLI entrypoint: `cli/opsroom/cmd/opsroom/main.go`.
- Command layer: `cli/opsroom/internal/cli/`.
- Runtime, daemon, projection, trace, store, templates, evals, TUI, and worker logic live under `cli/opsroom/internal/`.
- Workflow fixtures live in `cli/opsroom/testdata/workflows/`.
- Opsroom is a Go project with its own Taskfile and release guardrails.

## Workflow

1. Read `cli/opsroom/README.md` and the nearest package before editing.
2. Preserve local-first behavior:
   - durable evidence under `.opsroom/runs/<run_id>/`
   - daemon uses Unix socket JSON-RPC
   - commands should work with `--json` for scripts and concise human output by default
   - TUI is read-only for dangerous actions and should show copyable commands
3. For Generic CLI Runtime changes:
   - use structured argv, not shell string concatenation
   - keep prompt modes explicit: `stdin`, `file`, or `arg`
   - require fenced `yeisme-result` when structured output is expected
   - emit useful trace events for failures, approvals, locks, and sandbox violations
4. Keep user-visible docs, logs, help text, and reports in Chinese unless the string is a protocol field, code identifier, or third-party term.
5. Add tests at the package closest to the behavior. Prefer fixtures in `testdata/workflows/` for workflow contracts.

## Validation

```bash
cd cli/opsroom
task test
task test-race
task lint
task snapshot
```

For narrower checks:

```bash
cd cli/opsroom
go test ./internal/...
task demo-dry-run
```

If CI or release behavior changes, also use the Go/GitHub release guardrails skill.
