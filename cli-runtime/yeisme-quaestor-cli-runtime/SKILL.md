---
name: yeisme-quaestor-cli-runtime
description: Use when changing, testing, reviewing, documenting, or operating Quaestor under cli/quaestor, including query/research workflows, local CLI behavior, output contracts, evidence, and Go CLI validation.
---

# Yeisme Quaestor CLI Runtime

Use this skill for `cli/quaestor`, the Yeisme query and research-oriented CLI surface.

## Boundary

- Quaestor owns its local CLI workflows, query/research orchestration, output rendering, and evidence boundaries.
- Internet access, crawling, and provider calls must stay behind explicit adapters and redact credentials, raw prompts, provider payloads, private tool arguments, and full chain-of-thought.
- Do not move Quaestor behavior into Oh My Hermes; OMH may select profiles or invoke it through stable command/API surfaces.

## Workflow

1. Enter `cli/quaestor` before concrete implementation.
2. Read local `AGENTS.md` and use Quaestor OpenSpec changes for behavior changes.
3. Preserve CLI output contracts for human summaries, `--json`, `--agent`, stderr diagnostics, and redaction.
4. Reuse existing local test and fixture patterns before adding new test systems.

## Validation

```bash
cd cli/quaestor
gofmt -w ./cmd ./internal ./tests
go test ./...
go build -trimpath ./cmd/quaestor
```
