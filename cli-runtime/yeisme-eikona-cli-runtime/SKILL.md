---
name: yeisme-eikona-cli-runtime
description: Use when changing, testing, reviewing, documenting, or designing Eikona CLI behavior under cli/eikona, including image generation, reference-image editing, prompt skills, prompt decks, visual assessment, recipe reuse, command docs, agent invocation contracts, provider adapters, run evidence, project library, replacement safety, MCP integration, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the agent-facing visual asset runtime and evidence-backed generation CLI.

## Boundary

- CLI entrypoint: `cli/eikona/cmd/eikona`.
- Command and JSON envelope wiring live in `cli/eikona/internal/cli`.
- Config precedence and provider credential resolution live in `internal/config`.
- Provider protocol adapters live in `internal/adapters/*`; adapters must not print CLI output or bypass runtime storage.
- Run/job/artifact evidence lifecycle lives in `internal/runtime` and `internal/runstore`.
- Project library, prompt memory, prompt skills, prompt decks, sessions, replacement ledger, index, HTTP playground helpers, storage backup/restore, and MCP integration live under their matching `internal/*` modules.
- Multi-scenario prompt behavior is layered: `internal/prompts` owns prompt memory and prompt-skill records; `internal/promptdeck` owns immutable deck versions; workflow draw owns deterministic card-pull evidence; `internal/visualmemory` and `internal/stylepack` own authorized reference/style constraints; planned `internal/assessment` and `internal/recipe` work must consume these projections rather than creating parallel stores.
- In a `cli/eikona` session, human-facing product, design, runtime, protocol, governance, evaluation, command, and delivery docs live in local `docs/**`; code behavior docs live in `README.md` and `AGENTS.md`. Root project-doc mirrors are not valid owners and must not be required for closeout.
- Agent-facing command guidance lives in `cli/eikona/docs/commands/README.md`; cross-agent invocation rules live in `cli/eikona/docs/commands/agent-integration.md`.
- Eikona task lifecycle follows the repository-wide OpenSpec rules in `docs/workflows/execution-slice-lifecycle.md`; migrated Eikona notes live in `cli/eikona/openspec/changes/archive/2026-05-11-eikona-checklists-index/legacy/README.md`. Execution task state must stay under `cli/eikona/openspec/changes/eikona-<slug>/` or its archive, not docs checklists, plans, or ad hoc work-item directories.

## Workflow

1. Start inside `cli/eikona` and read `AGENTS.md`, `README.md`, and the nearest package or command doc before editing.
   - For CLI command documentation, read `docs/commands/README.md` and the matching `docs/commands/<command>.md` first.
   - For other agents calling Eikona, read `docs/commands/agent-integration.md` first and prefer CLI `--json`/`--agent` contracts before adding MCP-only behavior.
  - For storage backup/restore work, read `docs/commands/storage.md`, `docs/runtime/storage/storage-and-projection.md`, and root `docs/workflows/local-first-backup-sync.md` before changing code or docs.
  - For multi-scenario prompt work, read `docs/product/scenario-playbook.md`, `docs/commands/prompts.md`, `docs/commands/workflow.md`, and `docs/commands/style.md` before changing code or docs.
   - For Xiaohongshu static visual creation tasks, read the on-demand `eikona-xhs-visual-router` skill first, then keep execution on Eikona `generate` or `workflow` commands with review, feedback, and handoff evidence.
   - For active design tracks around scoring/tags or recipe reuse, read `openspec/changes/eikona-visual-assessment-tags/` and `openspec/changes/eikona-prompt-skill-reuse-recipes/` if they exist, then keep new implementation tasks in the owning Eikona OpenSpec change.
2. Preserve Eikona product contracts:
   - `--json` output must remain machine-readable and stable for agents, Cohors, CI, and shell scripts.
   - new or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
   - local project docs and OpenSpec artifacts should be Chinese by default; human CLI output, help text, logs, and user-visible errors should be English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
   - every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
   - provider requests in tests must use `httptest` or fixture adapters; do not call real remote providers in automated tests.
   - user-level local Eikona config or the local auth store may store plaintext provider keys when the user explicitly configures them; secrets must never be written to project YAML, YAML examples with real values, traces, provider jobs, artifact manifests, test snapshots, or README output.
   - Eikona must not create, recommend, or read shell credential scripts for provider keys; use direct user config, `eikona auth set --api-key-stdin`, or process environment for CI and temporary overrides.
   - command examples in docs, help, skills, plans, reviews, and final responses must be real user-runnable commands such as `eikona workflow run ...`; do not expose local wrappers or agent-only prefixes.
   - command docs must cover every visible subcommand and explicitly mark hidden/internal entries such as `models`, `worker`, and disabled `video` when relevant.
   - do not add isolated scenario commands for Xiaohongshu, short-drama, product, game, docs, or graphic-design variants; scenario differences belong in workflow templates, prompt decks, prompt skills, profiles, style packs, assessment criteria, review policy, and recipe influence evidence.
  - prompt skills are provenance-bearing reusable prompt sources; prompt decks are versioned card-pull assets; workflows snapshot prompt refs and deck selections into run evidence. Later edits to prompt skills, decks, style packs, or recipes must not reinterpret old runs.
  - storage sync is backup/restore only by default: local output root remains the source of truth, S3-compatible storage is a mirror, `storage push` must produce encrypted content-addressed objects and receipts, and `pull`/`restore` must stage output instead of overwriting project files.
  - do not add real-time sync, file watchers, automatic bidirectional merge, or multi-device conflict resolution to Eikona without a separate OpenSpec change.
  - visual assessment and recipe reuse must be evidence-backed and explainable: store scores/tags/corrections/recipe influence as structured evidence, never as hidden reasoning or unbounded prose. Machine-only scores must not silently select winners without append-only human feedback.
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
   - scenario prompt exploration uses `eikona prompts catalog search ... --json`, `eikona workflow draw ... --json`, and `eikona workflow run ... --background --json`;
   - Xiaohongshu creative direction uses the on-demand `eikona-xhs-*` skills for brief and prompt design, while this runtime skill remains responsible for CLI contracts, evidence, provider safety, and generated artifact lifecycle;
   - planned visual scoring uses `eikona assess ... --json` after the assessment change lands; until then, use `review`, `feedback`, and objective `quality.check` evidence;
   - planned recipe reuse uses `eikona recipes ...` and `workflow --recipe` only after the recipe change lands; until then, keep reuse explicit through prompt skills, deck versions, style packs, and feedback evidence;
  - long-lived integrations can use `eikona mcp`, but ordinary CLI output remains the primary contract.
  - storage backup uses `eikona storage backend set s3 ...`, `eikona storage push ...`, and `eikona storage restore ...`; for cross-project Git plus S3/rclone/cloud-drive policy, use `yeisme-local-backup-sync-policy` on demand.
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

For documentation, prompt-skill, deck, assessment, or recipe design changes, also run:

```bash
cd cli/eikona
openspec validate --all
```

If CI, tags, or release artifacts change, also use the Go/GitHub release guardrails skill.
