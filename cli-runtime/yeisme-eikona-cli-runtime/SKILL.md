---
name: yeisme-eikona-cli-runtime
description: Use when the user explicitly asks to use Eikona/eikona, or when changing, testing, reviewing, documenting, or designing Eikona CLI/runtime behavior under cli/eikona, including generation, external artifact capture, project/global asset scope, Visual Library promotion, download grants, OpenAPI/SDK contracts, prompt files, provider adapters, run evidence, project registry, replacement safety, MCP, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the agent-facing visual asset runtime and evidence-backed generation CLI.

If the user explicitly says to use Eikona, `eikona`, or the Eikona CLI for image generation, this route takes precedence over generic built-in image generation tools. Enter `cli/eikona`, follow local `AGENTS.md`, and use Eikona commands such as `eikona generate ... --json` / `--agent`. Only fall back to another image tool if the user explicitly changes the route or Eikona is unavailable and the user approves the fallback.

## Boundary

- CLI entrypoint: `cli/eikona/cmd/eikona`.
- Command and JSON envelope wiring live in `cli/eikona/internal/cli`.
- Config precedence and provider credential resolution live in `internal/config`.
- Provider protocol adapters live in `internal/adapters/*`; adapters must not print CLI output or bypass runtime storage.
- Run/job/artifact evidence lifecycle lives in `internal/runtime` and `internal/runstore`.
- External capture, path-free delivery, and project service boundaries live in `internal/api/artifactimport`, `internal/api/artifactdelivery`, and `internal/api/projectservice`; they must reuse app/runstore/index facades instead of creating parallel persistence.
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
   - For creative visual generation requests, read the on-demand `eikona-visual-router` skill first. It will route Scaena subject/readiness work, Auctra handoff, subject asset direction, Xiaohongshu static visuals, ultrawide storyboards, or plain CLI/runtime work to the smallest owner skill.
   - For temporary image persistence, Visual Library promotion, project/global scope, download grants, or asset APIs, load `eikona-asset-lifecycle` and read `docs/product/external-asset-capture.md` plus `docs/interfaces/api/openapi.yaml`.
   - For active design tracks around scoring/tags or recipe reuse, read `openspec/changes/eikona-visual-assessment-tags/` and `openspec/changes/eikona-prompt-skill-reuse-recipes/` if they exist, then keep new implementation tasks in the owning Eikona OpenSpec change.
2. Preserve Eikona product contracts:
   - `--json` output must remain machine-readable and stable for agents, Cohors, CI, and shell scripts.
   - new or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
   - local project docs and OpenSpec artifacts should be Chinese by default; human CLI output, help text, logs, and user-visible errors should be English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
   - every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
   - provider requests in tests must use `httptest` or fixture adapters; do not call real remote providers in automated tests.
   - user-level local Eikona config or the local auth store may store plaintext provider keys when the user explicitly configures them; secrets must never be written to project YAML, YAML examples with real values, traces, provider jobs, artifact manifests, test snapshots, or README output.
   - Eikona must not create, recommend, or read shell credential scripts for provider keys; use direct user config, `eikona auth set <channel> --api-key-stdin`, or process environment for CI and temporary overrides.
   - command examples in docs, help, skills, plans, reviews, and final responses must be real user-runnable commands such as `eikona workflow run ...`; do not expose local wrappers or agent-only prefixes.
   - command docs must cover every visible subcommand and explicitly mark hidden/internal entries such as `models`, `worker`, and disabled `video` when relevant.
   - do not add isolated scenario commands for Xiaohongshu, short-drama, product, game, docs, or graphic-design variants; scenario differences belong in workflow templates, prompt decks, prompt skills, profiles, style packs, assessment criteria, review policy, and recipe influence evidence.
  - prompt skills are provenance-bearing reusable prompt sources; prompt decks are versioned card-pull assets; workflows snapshot prompt refs and deck selections into run evidence. Later edits to prompt skills, decks, style packs, or recipes must not reinterpret old runs.
  - storage sync is backup/restore only by default: local output root remains the source of truth, S3-compatible storage is a mirror, `storage push` must produce encrypted content-addressed objects and receipts, and `pull`/`restore` must stage output instead of overwriting project files.
  - do not add real-time sync, file watchers, automatic bidirectional merge, or multi-device conflict resolution to Eikona without a separate OpenSpec change.
  - visual assessment and recipe reuse must be evidence-backed and explainable: store scores/tags/corrections/recipe influence as structured evidence, never as hidden reasoning or unbounded prose. Machine-only scores must not silently select winners without append-only human feedback.
3. For OpenAI-compatible image generation:
   - the canonical Eikona model ref is `openai/gpt-5.4-image-2`; gateway-native IDs must copy `/v1/models` exactly. The accepted short aliases are `gpt-5.4-image-2` and `gpt-image-2`; persisted `openai:gpt-image-2` is a legacy compatibility spelling only.
   - reject the ambiguous `openai:gpt-5.4-image-2` before provider submission with a repair message pointing to `openai/gpt-5.4-image-2`.
   - local interactive auth must use an explicitly selected Eikona channel backed by the user-level secret store; never restore implicit `OPENAI_API_KEY` fallback.
   - `openai:gpt_image_2` is legacy compatibility only.
   - before selecting a provider workflow or describing readiness, read `cli/eikona/docs/commands/agent-operability.md`; preserve its evidence vector and conservative effective level in the result.
   - no reference input means `image.generate`; the ordinary OpenAI Images path uses `/images/generations`.
   - `--reference-image` / `--ref` with `--reference-mode auto|edit` must preserve reference order, infer `image.edit`, and prefer multipart `/images/edits`.
   - `--reference-mode generate` means the references are guidance rather than the editable canvas; keep `image.generate`, encode ordered refs as multimodal `input_image` content, and prefer `/responses`.
   - agents must not start an additional transport-switching retry for auth, rate-limit, content-policy, timeout, TLS, or malformed-response failures. Preserve whatever attempts the current runtime records; changing automatic fallback policy requires runtime tests and a separate implementation scope.
   - never silently remove reference inputs. If evidence proves that the configured gateway supports text-to-image but not reference input, preserve the failed run, explain the capability loss, and start a separate text-only run only when the user requested or accepted that semantic fallback.
   - do not diagnose missing reference support from a generic failure alone. Inspect the redacted failure facts currently exposed by `eikona inspect <run_id> --json` and provider doctor; if endpoint or transport is not explicit, report `unknown/degraded` rather than inventing a distinction.
   - do not skip TLS verification for self-signed gateways; use system trust or `SSL_CERT_FILE`.
4. For CLI behavior changes, add tests close to the behavior:
   - command wiring and JSON contracts in `internal/cli`
   - provider request/response contracts in `internal/adapters/<provider>`
   - config precedence in `internal/config`
   - run lifecycle and artifact manifests in `internal/runtime`
   - project library, sessions, prompt memory, and replacement safety in their matching `internal/*` packages
   - MCP and HTTP playground helpers in `internal/mcp`, `internal/playground`, and related request/projection packages
5. For agent invocation design, keep the contract simple:
   - one-off inline generation uses `eikona "<prompt>" --json` or `eikona generate ... --json`; a prompt stored in a text or Markdown file uses `eikona generate --input <prompt-file> --json` instead. `--input` and `--prompt` are mutually exclusive; use `eikona-file-prompt-workflow` for categorized directories, collection README files, templates, and runbook authoring;
   - a prompt collection uses `eikona run -f <runbook.yaml> --json`: use `defaults.prompt_file` for a shared file, `jobs[].prompt_file` for named candidates, or `matrix.prompt_files` to expand one job per file. Prompt paths are relative to the runbook and `prompt`, `prompt_file`, and `prompt_ref` are mutually exclusive at each source level;
   - multi-step workflow work uses `eikona workflow validate/plan/draw/run --json` and `workflow run --background`;
   - status polling uses `eikona wait/status/inspect --json` or low-token `--agent`;
   - external PNG/JPEG/WebP capture uses `eikona artifacts import <path> --json`; capture always creates run evidence first and never auto-promotes into Visual Library;
   - artifact handoff uses `eikona assets handoff <artifact_id> --json` before project writes; long-term reuse requires an explicit `eikona library save eikona://artifact/<handle> ... --json` decision;
   - project-bound generated assets use `eikona assets handoff` → `eikona assets stage --to <project-relative-path>` → `eikona assets apply --project current --yes`; do not copy user-level runstore paths directly;
   - REST capture requires `Idempotency-Key`, allowed roots for server-side paths, and path-free delivery grants rather than absolute runstore paths;
   - scenario prompt exploration uses `eikona prompts catalog search ... --json`, `eikona workflow draw ... --json`, and `eikona workflow run ... --background --json`;
   - creative direction uses the on-demand `eikona-visual-router`, `eikona-subject-asset-director`, `eikona-xhs-*`, and `eikona-ultrawide-storyboard-director` skills for brief and prompt design; file-backed storage uses `eikona-file-prompt-workflow`; this runtime skill remains responsible for CLI contracts, evidence, provider safety, and generated artifact lifecycle;
   - Scaena episode/shot/cover/motion generation must first pass `scaena-subject-asset-readiness`; without a current preflight, Eikona may generate only subject candidates or look-development artifacts marked non-production;
   - planned visual scoring uses `eikona assess ... --json` after the assessment change lands; until then, use `review`, `feedback`, and objective `quality.check` evidence;
   - planned recipe reuse uses `eikona recipes ...` and `workflow --recipe` only after the recipe change lands; until then, keep reuse explicit through prompt skills, deck versions, style packs, and feedback evidence;
   - long-lived integrations can use `eikona mcp`, but ordinary CLI output remains the primary contract.
   - storage backup uses `eikona storage backend set s3 ...`, `eikona storage push ...`, and `eikona storage restore ...`; for reusable Git plus S3/rclone/cloud-drive policy, use `local-first-backup-sync-policy` on demand.
   - OpenAI image calls use `openai/gpt-5.4-image-2` with an explicit channel such as `--use-channel openai`. `gpt-5.4-image-2` and `gpt-image-2` are accepted aliases; new commands and persisted metadata must use the slash-form canonical ref.
   - CLI, MCP, REST, and Go SDK generation changes must prepare one shared Generation Intent and expose the same prompt-free request summary, ordered reference roles, `model_ref`, and `original_model_ref`.
   - `assets.apply` remains dry-run unless the caller explicitly supplies `confirm=true`; responses expose project-relative `target_path`, never absolute project or artifact paths.
6. For Eikona plan/checklist work, keep `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` under `cli/eikona/openspec/changes/eikona-<slug>/`; migrate any misplaced checklist or root `openspec/` implementation task before continuing. Do not leave completed execution changes active. After closeout, update readiness/specs, record verification in `tasks.md` or `design.md`, and archive ordinary changes to `cli/eikona/openspec/changes/archive/YYYY-MM-DD-eikona-<slug>/`.

## 文件提示词集合约束

- 分类、命名、README、prompt 文档和 runbook 模板由 `eikona-file-prompt-workflow` 统一定义；runtime 不复制第二套目录规范。
- 一个 `.md` 或 `.txt` 文件对应一个可审阅的提示词方向；文件内容只包含自然语言创作提示，不包含密钥、provider payload、隐藏指令或 run metadata。
- 对集合先执行 `eikona run -f <runbook.yaml> --dry-run --json`，确认展开的 jobs、模型、尺寸、来源和成本限制后再执行真实 run。
- CLI 会为单文件和 runbook job 记录 prompt source provenance 与 run-owned snapshot。不得手改 `prompt_sources.json`、snapshot、batch plan、queue 或 run evidence；通过 Eikona CLI 重建或推进它们。
- Auctra 来源先交给 `eikona-auctra-visual-router`：只能从已接受的 brief/source refs 派生 prompt 文件；Eikona 是 Auctra 生图的默认和优先执行路径。

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

## Visual Intent Evidence

The runtime consumes validated `eikona.visual_intent.v1` evidence through `eikona workflow import intent`. It is the only Skill responsible for provider execution and artifact lifecycle. Evidence files (`visual_intent.json`, `skill_receipt.json`, `intent_compile.json`) are written under each run directory and linked through existing runstore paths.

The runtime distinguishes claimed from verified skill identity; unverified receipts cannot support promoted/core evidence. Default model: `openai/gpt-5.4-image-2`.

Contract reference: `../eikona-visual-router/references/visual-intent-contract.md`.
