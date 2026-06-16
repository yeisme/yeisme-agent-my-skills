---
name: yeisme-taskbridge-cli-runtime
description: Use when changing, testing, reviewing, or shipping TaskBridge CLI behavior under cli/taskbridge, including task control-plane commands, project planning, sync diff/audit, action files, Agent JSON contracts, provider sync, and Go release checks.
---

# Yeisme TaskBridge CLI Runtime

Use this skill for `cli/taskbridge`, the Go CLI that bridges local task control-plane workflows with multiple Todo providers and Agent-safe automation.

## Boundary

- CLI entrypoint: `cli/taskbridge/main.go`.
- Commands live in `cli/taskbridge/cmd/`.
- Core task model and storage live in `cli/taskbridge/internal/model` and `cli/taskbridge/internal/storage`.
- Control-plane behavior lives in `internal/controlplane`, `internal/actionfile`, `internal/syncaudit`, `internal/projectservice`, and `internal/agentcontract`.
- Provider adapters live in `internal/provider/*`; never bypass provider interfaces for remote writes.

## Workflow

1. Start inside `cli/taskbridge` and read `AGENTS.md`, the command file, and the owning `internal/` package before editing.
2. Preserve TaskBridge product semantics:
   - `today`, `next`, `inbox`, `review`, and `sync diff` are safe read/preview surfaces.
   - `agent *` stdout must remain valid `taskbridge.agent-result.v1` JSON.
   - new general CLI output surfaces must follow `ai-native-cli-output-contract`: concise human summaries by default, strict machine JSON, stable agent mode, NDJSON events for streams, and no logs mixed into machine stdout.
   - dangerous actions require `--confirm` or an action-file confirmation gate.
   - `--dry-run` must not mutate local storage or call remote write APIs.
   - sync/audit output must describe what was compared or written, not just that a command ran.
3. Keep CLI help, docs, text output, and user-facing errors in English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
4. Add tests close to the behavior:
   - command wiring and envelope behavior in `cmd/`
   - control-plane classification in `internal/controlplane`
   - action-file execution in `internal/actionfile`
   - sync diff/audit semantics in `internal/syncaudit`
   - project lifecycle behavior in `internal/projectservice`
5. For integration checks, build a temporary binary and run it against a temporary `--storage-path`; parse JSON outputs with `node` or Go rather than relying on text matching.

## Validation

Run the focused gate after code changes:

```bash
cd cli/taskbridge
go test ./cmd ./internal/actionfile ./internal/controlplane ./internal/syncaudit ./internal/projectservice
go build ./...
```

Run a smoke integration sequence when command behavior changes:

```bash
cd cli/taskbridge
tmp=$(mktemp -d)
go build -o "$tmp/taskbridge" .
"$tmp/taskbridge" --storage-path "$tmp/storage" doctor --format json
"$tmp/taskbridge" --storage-path "$tmp/storage" demo today --format json
"$tmp/taskbridge" --storage-path "$tmp/storage" agent plan "学习 OpenClaw" --dry-run=false
```

`go test ./...` is desirable before release, but if it hangs in unrelated provider/loader paths, record the package and keep the focused gate plus smoke evidence.
