---
name: yeisme-auctra-cli-runtime
description: Use when changing, testing, reviewing, documenting, or designing the Auctra CLI-first text creation product runtime under cli/auctra, including product workflows, CLI/TUI behavior, app-service boundaries, material/brief/review/export contracts, runtime providers, run evidence, and approved independent-client handoffs.
---

# Yeisme Auctra CLI Runtime

Use this skill for `cli/auctra`, the local-first text creation product engine whose owned interactive surfaces are CLI/TUI and whose stable projections may support approved independent clients.

## Product Identity Lock

Auctra is a specialized text creation product engine, not a generic agent and not a provider router. CLI/TUI remain its owned direct user interfaces; product PRDs, workflow design, and client contract gaps are still in scope even when frontend implementation belongs to a separate approved client.

```text
External agent / script -> auctra CLI -> .auctra state -> evidence -> review -> version/export
```

Auctra owns materials, briefs, text runs, review items, versions, export manifests, and redaction. Codex, Claude, Cohors, and Yeisme subagents are callers of `auctra`; they are not embedded providers inside Auctra.

## Boundary

- CLI entrypoint: `cli/auctra/cmd/auctra`.
- Command parsing and mode wiring: `internal/cli` and `internal/cli/command`.
- Shared output projections/renderers: `internal/presenter`; CLI output changes must follow `ai-native-cli-output-contract`.
- App workflows: `internal/app`.
- Project identity and `.auctra/project.yaml`: `internal/project`.
- Text units, briefs, generators, templates, versions, and exports: `internal/content` and `internal/manuscript`.
- Materials and links: `internal/material`.
- Review queue, decisions, and adoption: `internal/review`.
- Runtime provider contract and runtime selection: `internal/runtime`.
- Cohors fixture/subprocess integration only: `internal/cohors`; do not modify `cli/cohors`.
- TUI workbench: `internal/tui`, `internal/tui/pages`, and `internal/workspace`.
- Persistent index: `internal/store` with SQLite/GORM.

## Non-Negotiable Invariants

- **Human review first:** generation creates pending review items. Only `review accept` or `review partial` may create accepted versions. No `--auto-accept`, unattended overwrite, or publish bypass.
- **Shared text engine:** novel chapters, Xiaohongshu notes, WeChat articles, short-video scripts, and screenplay scenes use one text unit / brief / run evidence / review / export core. Do not create independent per-kind generator stacks.
- **Local-first evidence:** project state, materials, drafts, versions, run receipts, review decisions, and export manifests stay under `.auctra/` by default.
- **CLI/TUI only:** no Web UI, local service API, MCP server, platform login, scraper, or auto-publisher in Auctra.
- **Structured asset boundary:** agents may write user prose files, but must mutate `.auctra/project.yaml`, `.auctra/profile/**`, `.auctra/runs/**`, `.auctra/review/**`, `.auctra/exports/**`, and SQLite rows only through Auctra commands or app services.

## Runtime Provider Contract

Provider IDs are closed for current work: `pi`, `omp`, `cohors`, and `fixture`. Adding a provider or changing provider semantics requires an Auctra OpenSpec change.

Runtime providers are projection adapters, not model SDK integrations:

- `pi` is the default real runtime priority.
- `omp` is explicit through `--runtime omp` or `AUCTRA_RUNTIME=omp`.
- `fixture` is the only deterministic offline test/demo path.
- `cohors` remains planned/unavailable until a separate Auctra change makes it real.

Provider implementations must consume a versioned text projection such as `auctra.provider.text_projection.v1`. Do not import provider SDKs, save provider secrets, parse human-readable provider output, or silently fall back to fixture while claiming a requested provider succeeded.

Run evidence must keep redaction enabled. Secrets, auth headers, raw prompts, hidden prompts, provider payloads, private tool arguments, and chain-of-thought must not appear in CLI output, receipts, fixtures, golden files, or docs.

## Agent-Facing CLI Contract

Agent workflows must use real commands with `--json` or `--agent`:

```bash
auctra material add --kind note --title "咖啡店观察" --from ./notes/cafe.md --json
auctra content new xhs_note --title "这家咖啡店为什么适合一个人待一下午" --platform xiaohongshu --json
auctra content generate note_001 --runtime pi --agent
auctra review --status pending --json
auctra content export note_001 --format markdown --to ./dist --json
```

`--json` must emit one envelope. `--agent` must emit stable `key=value` facts. Diagnostics go to stderr. Tests must parse machine output directly, never default human summaries.

## Language Rule

Local project docs and OpenSpec artifacts default to Chinese. CLI help, errors, command run summaries, logs, and `--explain` reports default to English. Chinese remains valid product content for Xiaohongshu, WeChat, Douyin, manuscripts, source notes, fixtures, and quoted material.

## OpenSpec And Docs Ownership

Auctra implementation plans live under `cli/auctra/openspec/changes/auctra-<slug>/` or an existing active change such as `agent-cli-redesign`. Product, operator, runtime, command, and module docs live under `cli/auctra/docs/**`. Do not create root doc mirrors for Auctra implementation state.

## Validation

For output/review/runtime contract changes:

```bash
cd cli/auctra
go test -tags=nomsgpack ./internal/cli ./internal/cli/command ./internal/app ./internal/runtime
openspec validate agent-cli-redesign --strict
```

For broader code or command behavior changes:

```bash
cd cli/auctra
go test -tags=nomsgpack ./...
task build
```

If runtime, evidence, fixture demo, or main creation flows change, also run:

```bash
cd cli/auctra
task fixture-demo
task test:integration
```
