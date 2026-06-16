---
name: yeisme-eikona-cli-runtime
description: Use when changing, testing, reviewing, documenting, or designing Eikona CLI behavior under cli/eikona, including image generation, reference-image editing, command docs, agent invocation contracts, provider adapters, run evidence, project library, replacement safety, MCP integration, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the agent-facing visual asset runtime and evidence-backed generation CLI.

## Boundary

- CLI entrypoint: `cli/eikona/cmd/eikona`.
- Command and JSON envelope wiring live in `cli/eikona/internal/cli`.
- Config precedence and provider credential resolution live in `internal/config`.
- Provider protocol adapters live in `internal/adapters/*`; adapters must not print CLI output or bypass runtime storage.
- Run/job/artifact evidence lifecycle lives in `internal/runtime` and `internal/runstore`.
- Project library, prompt memory, sessions, replacement ledger, index, HTTP playground helpers, and MCP integration live under their matching `internal/*` modules.
- In a `cli/eikona` session, human-facing product, design, runtime, protocol, governance, evaluation, command, and delivery docs live in local `docs/**`; code behavior docs live in `README.md` and `AGENTS.md`. Root project-doc mirrors are not valid owners and must not be required for closeout.
- Agent-facing command guidance lives in `cli/eikona/docs/commands/README.md`; cross-agent invocation rules live in `cli/eikona/docs/commands/agent-integration.md`.
- Eikona task lifecycle follows the repository-wide OpenSpec rules in `docs/workflows/execution-slice-lifecycle.md`; migrated Eikona notes live in `cli/eikona/openspec/changes/archive/2026-05-11-eikona-checklists-index/legacy/README.md`. Execution task state must stay under `cli/eikona/openspec/changes/eikona-<slug>/` or its archive, not docs checklists, plans, or ad hoc work-item directories.

## Workflow

1. Start inside `cli/eikona` and read `AGENTS.md`, `README.md`, and the nearest package or command doc before editing.
   - For CLI command documentation, read `docs/commands/README.md` and the matching `docs/commands/<command>.md` first.
   - For other agents calling Eikona, read `docs/commands/agent-integration.md` first and prefer CLI `--json`/`--agent` contracts before adding MCP-only behavior.
2. Preserve Eikona product contracts:
   - `--json` output must remain machine-readable and stable for agents, Cohors, CI, and shell scripts.
   - new or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
   - human output, help text, docs, logs, and user-visible errors should be English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
   - every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
   - provider requests in tests must use `httptest` or fixture adapters; do not call real remote providers in automated tests.
   - secrets must never be written to YAML examples, traces, provider jobs, artifact manifests, test snapshots, or README output.
   - command examples in docs, help, skills, plans, reviews, and final responses must be real user-runnable commands such as `eikona workflow run ...`; do not expose local wrappers or agent-only prefixes.
   - command docs must cover every visible subcommand and explicitly mark hidden/internal entries such as `models`, `worker`, and disabled `video` when relevant.
3. For OpenAI-compatible image generation:
   - new docs, examples, defaults, and prompts must recommend `openai:gpt-image-2`.
   - `openai:gpt_image_2` is legacy compatibility only.
   - `--reference-image` should preserve reference order and infer `image.edit`.
   - keep `/images/edits` multipart as the preferred path, and use `/chat/completions` multimodal fallback only for clear gateway compatibility failures.
   - do not skip TLS verification for self-signed gateways; use system trust or `SSL_CERT_FILE`.
4. For CLI behavior changes, add tests close to the behavior:
   - command wiring and JSON contracts in `internal/cli`
   - provider request/response contracts in `internal/adapters/<provider>`
   - config precedence in `internal/config`
   - run lifecycle and artifact manifests in `internal/runtime`
   - project library, sessions, prompt memory, and replacement safety in their matching `internal/*` packages
   - MCP and HTTP playground helpers in `internal/mcp`, `internal/playground`, and related request/projection packages
5. For agent invocation design, keep the contract simple:
   - one-off generation uses `eikona "<prompt>" --json` or `eikona generate ... --json`;
   - multi-step work uses `eikona workflow validate/plan/draw/run --json` and `workflow run --background`;
   - status polling uses `eikona wait/status/inspect --json` or low-token `--agent`;
   - artifact handoff uses `eikona assets handoff <artifact_id> --json` before project writes;
   - long-lived integrations can use `eikona mcp`, but ordinary CLI output remains the primary contract.
6. For Eikona plan/checklist work, keep `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` under `cli/eikona/openspec/changes/eikona-<slug>/`; migrate any misplaced checklist or root `openspec/` implementation task before continuing. Do not leave completed execution changes active. After closeout, update readiness/specs, record verification in `tasks.md` or `design.md`, and archive ordinary changes to `cli/eikona/openspec/changes/archive/YYYY-MM-DD-eikona-<slug>/`.

## Validation

Run focused Go checks for the area changed:

```bash
cd cli/eikona
go test ./internal/adapters/openai ./internal/config ./internal/cli
go build -trimpath -o dist/eikona ./cmd/eikona
```

For broader backend/runtime changes:

```bash
cd cli/eikona
go test ./... -timeout 180s
go build -trimpath -o dist/eikona ./cmd/eikona
```

If CI, tags, or release artifacts change, also use the Go/GitHub release guardrails skill.
