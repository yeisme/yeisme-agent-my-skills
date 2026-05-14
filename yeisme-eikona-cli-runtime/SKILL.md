---
name: yeisme-eikona-cli-runtime
description: Use when changing, testing, reviewing, or designing Eikona CLI behavior under cli/eikona, including image generation, reference-image editing, provider adapters, run evidence, project library, replacement safety, Web UI, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the agent-facing visual asset runtime and evidence-backed generation CLI.

## Boundary

- CLI entrypoint: `cli/eikona/cmd/eikona`.
- Command and JSON envelope wiring live in `cli/eikona/internal/cli`.
- Config precedence and provider credential resolution live in `internal/config`.
- Provider protocol adapters live in `internal/adapters/*`; adapters must not print CLI output or bypass runtime storage.
- Run/job/artifact evidence lifecycle lives in `internal/runtime` and `internal/runstore`.
- Project library, prompt memory, sessions, replacement ledger, index, Web API, and Web UI live under their matching `internal/*` or `web/` modules.
- In a `cli/eikona` session, human-facing product, design, runtime, protocol, governance, evaluation, and delivery docs live in local `docs/**`; code behavior docs live in `README.md` and `AGENTS.md`. Root project-doc mirrors are not valid owners and must not be required for closeout.
- Eikona task lifecycle follows the repository-wide OpenSpec rules in `docs/workflows/execution-slice-lifecycle.md`; migrated Eikona notes live in `cli/eikona/openspec/changes/archive/2026-05-11-eikona-checklists-index/legacy/README.md`. Execution task state must stay under `cli/eikona/openspec/changes/eikona-<slug>/` or its archive, not docs checklists, plans, or ad hoc work-item directories.

## Workflow

1. Start inside `cli/eikona` and read `AGENTS.md`, `README.md`, and the nearest package before editing.
2. Preserve Eikona product contracts:
   - `--json` output must remain machine-readable and stable for agents, Cohors, CI, and shell scripts.
   - new or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
   - human output, help text, docs, logs, and user-visible errors should be Chinese unless the string is a protocol key, command, model id, provider id, or code identifier.
   - every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
   - provider requests in tests must use `httptest` or fixture adapters; do not call real remote providers in automated tests.
   - secrets must never be written to YAML examples, traces, provider jobs, artifact manifests, test snapshots, or README output.
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
   - Web API behavior in `internal/webapi`
   - Web UI behavior in `web/src`
5. For Web UI changes, follow existing React/Vite patterns, keep operational density, and verify with the Web UI test stack rather than relying on static inspection.
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

For Web UI changes:

```bash
cd cli/eikona/web
npm test
npm run build
```

If CI, tags, or release artifacts change, also use the Go/GitHub release guardrails skill.
