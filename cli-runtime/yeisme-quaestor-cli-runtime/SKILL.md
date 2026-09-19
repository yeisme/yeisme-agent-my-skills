---
name: yeisme-quaestor-cli-runtime
description: Use when changing, testing, reviewing, documenting, designing, or operating the Quaestor research product runtime under cli/quaestor, including product workflows, evidence ledgers, quantitative validation, CLI behavior, app-service/API/client contracts, adapters, redaction, and Go validation.
---

# Yeisme Quaestor CLI Runtime

Use this skill for `cli/quaestor`, the Yeisme research product engine whose current operator surface is the CLI and whose future services or approved clients must consume the same evidence and application-service contracts.

## Boundary

- Quaestor owns its local CLI workflows, query/research orchestration, output rendering, and evidence boundaries.
- Product PRDs, research workflow design, API projections, and approved client contract gaps are in scope; independent frontend implementation requires its own approved client owner.
- Internet access, crawling, and provider calls must stay behind explicit adapters and redact credentials, raw prompts, provider payloads, private tool arguments, and full chain-of-thought.
- Do not move Quaestor behavior into Connectors; skill profiles may select it or invoke it through stable command/API surfaces.

## Workflow

1. Enter `cli/quaestor` before concrete implementation.
2. Read local `AGENTS.md` and use Quaestor OpenSpec changes for behavior changes.
3. Preserve CLI output contracts for human summaries, `--json`, `--agent`, stderr diagnostics, and redaction.
4. Reuse existing local test and fixture patterns before adding new test systems.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Implementation request | Enter `cli/quaestor`; read local `AGENTS.md` | Do not implement from root |
| Internet, crawl, or provider call | Keep it behind an explicit adapter | Redact credentials, raw prompts, payloads, and chain-of-thought |
| Independent frontend requested | Needs its own approved client owner | Do not put frontend implementation in this CLI |
| Move Quaestor behavior into Connectors | Stop | Invoke only through stable command or API surfaces |

## Validation

```bash
cd cli/quaestor
gofmt -w ./cmd ./internal ./tests
go test ./...
go build -trimpath ./cmd/quaestor
```
