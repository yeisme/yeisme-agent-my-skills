---
name: yeisme-gitpulse-cli-runtime
description: Use when changing, testing, reviewing, documenting, or operating GitPulse under cli/gitpulse, including Git workflow orchestration, worktrees, PR flow, TUI behavior, output contracts, and Go CLI validation.
---

# Yeisme GitPulse CLI Runtime

Use this skill for `cli/gitpulse`, the Git workflow orchestration CLI for Yeisme repositories.

## Boundary

- GitPulse owns Git workflow commands, branch/worktree orchestration, PR preparation, release checks, and TUI workflow surfaces.
- GitHub/Gitea provider writes should go through stable CLI or forge adapter boundaries, not ad hoc scripts hidden in agent output.
- TUI behavior must keep domain logic in testable state transitions and render functions.

## Workflow

1. Enter `cli/gitpulse` before concrete implementation.
2. Read its local `AGENTS.md` and use local OpenSpec changes for implementation work.
3. Preserve CLI output contracts: human summaries, `--json`, `--agent`, stderr diagnostics, and redaction.
4. Prefer GitPulse itself for future Yeisme branch, worktree, PR, and pre-release checks when it covers the operation.

## Validation

```bash
cd cli/gitpulse
gofmt -w ./cmd ./internal ./tests
go test ./...
go build -trimpath ./cmd/gitpulse
```
