---
name: yeisme-eikona-cli-runtime
description: Use when the user explicitly asks to use Eikona/eikona, needs post-install setup or environment discovery, or when changing, testing, reviewing, documenting, or designing Eikona CLI/runtime behavior under cli/eikona, including public distribution, Agent Skills, generation, external artifact capture, project/global asset scope, Visual Library promotion, download grants, OpenAPI/SDK contracts, prompt files, provider adapters, run evidence, project registry, replacement safety, MCP, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the headless image-generation and image-asset-management foundation for agents and services.

If the user explicitly says to use Eikona, `eikona`, or the Eikona CLI for image generation, this route takes precedence over generic built-in image generation tools. Enter `cli/eikona`, follow local `AGENTS.md`, and use Eikona commands such as `eikona generate ... --agent`. Only fall back to another image tool if the user explicitly changes the route or Eikona is unavailable and the user approves the fallback.

## Installed-binary bootstrap

An installed Eikona binary is self-describing. Do not search for, clone, or require access to the private `yeisme/eikona` repository to determine environment names, configuration files, Skills, or next actions.

Start every fresh Homebrew, Scoop, package, archive, or public Bash installation with:

```bash
eikona setup --agent
```

Follow `action.next`. The default setup is a no-write preview. Only after local-write authority is clear may the Agent run:

```bash
eikona setup --yes --agent
```

Setup creates only missing user configuration and installs Agent Skills from the public `https://github.com/yeisme/yeisme-dist` release that exactly matches the running released CLI. It must not fall back to latest, replace a package-manager-owned binary, accept credentials, edit shell startup files, change Codex/Claude MCP configuration, probe a provider, or generate an image. `SKILLS_RELEASE_NOT_MIRRORED` is a real public-distribution blocker; config-only recovery is:

```bash
eikona setup --yes --skip-skills --agent
```

Persistent local credentials use stdin and the user-owned auth store:

```bash
eikona auth set openai --protocol openai --api-key-stdin --agent
```

Environment discovery must remain metadata-only:

```bash
eikona config env --provider openai --agent
eikona config env --all --json
```

These commands may expose variable names, sensitivity, set/unset state, source, and precedence, but never values. Ordinary Agents must not call `eikona auth env` because it is an advanced raw secret-export surface.

After configuration, inspect adapted models and local channel defaults before any probe. Missing credentials are configuration status, not lack of adapter support:

```bash
eikona models list --source adapted --all --agent
eikona models list --source adapted --provider openai --all
eikona models default show --agent
eikona auth list --agent
eikona providers show openai --agent
```

Bare `eikona models list` reads `models.lock` (`--source manifest`). An empty manifest is not an empty adapter catalog; next action is `--source adapted`. `auth list` shows channel `default_model` values, not every adapted model.

A user may then authorize the explicit non-generating probe:

```bash
eikona doctor --channel openai --model openai/gpt-5.4-image-2 --probe --agent
```

Do not run `--smoke` or any generation command during bootstrap without explicit user approval for the provider/model and potential cost.


## Current surfaces

- v0.6.9 adds first-class xAI Grok Imagine **image** models on top of v0.6.7 release provenance. Product default paid image model remains `openai/gpt-5.4-image-2`. Grok **video** refs are rejected and owned by Scaena.
- Grok Imagine image: `--model xai:grok-imagine-image` or `xai:grok-imagine-image-quality` (aliases `grok-imagine-image-pro`, `grok-imagine-image-quality-latest`, `grok-imagine-image-quality-20260403`). Official default `https://api.x.ai/v1` + `XAI_API_KEY`; a user-local channel whose name and protocol are both `xai` auto-binds; a channel named `gateway` stays explicit (`--use-channel`). Doctor/readiness may emit `endpoint_class=official|custom` without printing host or key. Map `--aspect` → `aspect_ratio`, `--size 1k|2k` → `resolution`; JSON edits only, max 3 refs. Official USD rows apply even on a custom host for known Imagine image models.
- LAN serve: `eikona serve --api-key-file <absolute-0600-file>` is the recommended LAN token source; there is no `EIKONA_SERVE_TOKEN`. Private-service `--config` remains the production path.
- Version/update: `internal/update` owns release discovery (dist catalog + pinned upstream, ETag/bounded bodies/credential-guarded redirects); `internal/runtimeinfo` is the shared read-only version and cached update-status projection behind `eikona version`, `/api/v1/runtime/*`, and `eikona://runtime/*` with no remote apply authority. CLI family: `version`, `update --check|status|--dry-run|--yes`, `update policy show/set/reset`. Update notices decorate compact JSON (`facts.cli_update`) and agent (`notice.update.*`) output only, with the full suppression matrix in `internal/cli/update_notice.go`.
- Command catalog: `eikona commands --emit-catalog` writes the release asset; `eikona commands diff --target <ver>` compares against `eikona-command-catalog_<version>.json` published with each release. A removed stable path without a recorded replacement fails `COMMAND_CATALOG_INCOMPATIBLE`.
- Private service: `internal/serviceauth` owns the CLI-authored service config and scoped access-key store (salted-hash-only persistence, 0600 secret files). `eikona service config/access-key/doctor` author them; `eikona serve --config` mounts the TLS/trusted-proxy guard (`TLS_REQUIRED` before any side effect) and access-key authentication. `GET /api/v1/readiness` (`internal/api/runtimesurface`) projects ten independent readiness dimensions; repository test evidence must never promote live provider or public-hosting readiness.
- MCP: `eikona mcp --transport stdio` runs the real protocol lifecycle on the official MCP Go SDK v1.7.0 (`internal/mcptransport`; stdout protocol-only, redacted stderr, stdin-EOF shutdown; the hand-rolled `internal/mcp/stdio.go` is deleted and no sibling adapter exists). Default stdio serves the in-process owner services; `--endpoint`+`--key-file` (absolute 0600) consumes the owner HTTPS backing statelessly with startup discovery that fails typed `OWNER_BACKING_UNAVAILABLE` when unreachable. `eikona mcp --json|--agent` stay one-shot projections; `eikona mcp doctor` and `eikona mcp capabilities` (tools/actions/resources/prompts plus `yeisme.media.capability.v1` links) are the diagnostics; `mcp_streamable_http` stays blocked.
- Prompt repository: `internal/promptrepository` consumes public promptrepo v0.4.0 (repository scope, deny-wins policy-review, structured document selectors). Template and rendered bodies never enter output, events, or evidence.

## Boundary

- Eikona owns image generation, provider execution, run/artifact evidence, review, reuse memory, asset catalog, binding, handoff, stage/apply, replacement/rollback, delivery outcomes, and consumer-neutral headless contracts.
- Eikona does not own a Web app, dashboard, browser shell, frontend navigation/auth shell, or frontend design system. Display requirements belong to an explicitly approved external consumer and must use Eikona's stable CLI/API/SDK/MCP/event/resource contracts.
- The existing `ui` discovery command and embedded root page are frozen compatibility surfaces. Do not add features to them; removing them requires a separate compatibility change with named consumers, at least one release of deprecation, migration guidance, and rollback.
- CLI entrypoint: `cli/eikona/cmd/eikona`.
- Command and JSON envelope wiring live in `cli/eikona/internal/cli`.
- Config precedence and provider credential resolution live in `internal/config`.
- Provider protocol adapters live in `internal/adapters/*`; adapters must not print CLI output or bypass runtime storage.
- Run/job/artifact evidence lifecycle lives in `internal/runtime` and `internal/runstore`.
- External capture, path-free delivery, and project service boundaries live in `internal/api/artifactimport`, `internal/api/artifactdelivery`, and `internal/api/projectservice`; they must reuse app/runstore/index facades instead of creating parallel persistence.
- Project library, prompt memory, prompt skills, prompt decks, sessions, replacement ledger, index, HTTP playground helpers, storage backup/restore, and MCP integration live under their matching `internal/*` modules.
- Multi-scenario prompt behavior is layered: `internal/prompts` owns prompt memory and prompt-skill records; `internal/promptdeck` owns immutable deck versions; workflow draw owns deterministic card-pull evidence; `internal/visualmemory` and `internal/stylepack` own authorized reference/style constraints; `internal/assessment` owns structured scoring/tag evidence; `internal/recipe` owns explainable reusable combinations. These layers consume one another through stable projections instead of creating parallel stores.
- In a `cli/eikona` session, human-facing product, design, runtime, protocol, governance, evaluation, command, and delivery docs live in local `docs/**`; code behavior docs live in `README.md` and `AGENTS.md`. Root project-doc mirrors are not valid owners and must not be required for closeout.
- Agent-facing command guidance lives in `cli/eikona/docs/commands/README.md`; cross-agent invocation rules live in `cli/eikona/docs/commands/agent-integration.md`.
- Eikona task lifecycle follows the repository-wide OpenSpec rules in `docs/workflows/execution-slice-lifecycle.md`; migrated Eikona notes live in `cli/eikona/openspec/changes/archive/2026-05-11-eikona-checklists-index/legacy/README.md`. Execution task state must stay under `cli/eikona/openspec/changes/eikona-<slug>/` or its archive, not docs checklists, plans, or ad hoc work-item directories.

## Workflow

1. Start inside `cli/eikona` and read `AGENTS.md`, `README.md`, and the nearest package or command doc before editing.
   - For an installed-binary usage or setup request, run `eikona setup --agent` first. Repository access is not a prerequisite for operating a released CLI.
   - For CLI command documentation, read `docs/commands/README.md` and the matching `docs/commands/<command>.md` first.
   - For other agents calling Eikona, read `docs/commands/agent-integration.md` first and prefer CLI `--json`/`--agent` contracts before adding MCP-only behavior.
  - For storage backup/restore work, read `docs/commands/storage.md`, `docs/runtime/storage/storage-and-projection.md`, and root `docs/workflows/local-first-backup-sync.md` before changing code or docs.
  - For multi-scenario prompt work, read `docs/product/scenario-playbook.md`, `docs/commands/prompts.md`, `docs/commands/workflow.md`, and `docs/commands/style.md` before changing code or docs.
   - For creative visual generation requests, read the on-demand `eikona-visual-router` skill first. It will route Scaena subject/readiness work, Auctra handoff, subject asset direction, Xiaohongshu static visuals, ultrawide storyboards, or plain CLI/runtime work to the smallest owner skill.
   - For temporary image persistence, Visual Library promotion, project/global scope, download grants, or asset APIs, load `eikona-asset-lifecycle` and read `docs/product/external-asset-capture.md` plus `docs/interfaces/api/openapi.yaml`.
   - For active design tracks around scoring/tags or recipe reuse, read `openspec/changes/eikona-visual-assessment-tags/` and `openspec/changes/eikona-prompt-skill-reuse-recipes/` if they exist, then keep new implementation tasks in the owning Eikona OpenSpec change.
2. Preserve Eikona product contracts:
   - keep product planning and documentation headless: new roadmap items may improve generation quality, provider coverage, evidence, review/reuse, asset lifecycle, delivery, or consumer-neutral interfaces, but must not add an Eikona-owned Web/frontend backlog;
   - `--json` output must remain machine-readable and stable for scripts, Ordo, CI, and shell pipelines: since v0.6.0 bare `--json` is the bounded compact default, `--json --compact` is its explicit equivalent, and `--json --full` is the permanent forensic projection. Routine agents still prefer `--agent`.
   - new or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
   - local project docs and OpenSpec artifacts should be Chinese by default; human CLI output, help text, logs, and user-visible errors should be English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
   - every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
   - provider requests in tests must use `httptest` or repository test adapters; do not call real remote providers in automated tests.
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
   - the canonical Eikona model ref is `openai/gpt-5.4-image-2`; gateway-native IDs must copy `/v1/models` exactly. The main CLI ingress rejects the removed bare aliases `gpt-5.4-image-2` and `gpt-image-2`. Only explicitly scoped historical handoff ingress may read them, emit `MODEL_ALIAS_LEGACY_INGESTED`, and immediately normalize to the canonical slash form.
   - `codex:imagegen` is the implicit preview fallback when the caller leaves `--model` unset, the paid OpenAI/gateway API is unavailable, and a local Codex session is ready. It does not take an Eikona provider key and is hard-capped at the 1K size family. Project `model_selection`, `capability_class=preview`, `size_class=1k`, `auth_class=codex_session`, and `resolution_control=prompt_instruction` so agents do not treat the ceiling or prompt-delivery mode as a tool defect. Recommended Codex commands omit `--size 1k`; an explicit admitted size remains compatible, is injected into the execution prompt, and must return `PROMPT_CONTROLLED_RESOLUTION`. Explicit `--model`, `--use-channel`, edit/reference, or an explicit oversized canvas never fall back.
   - reject provider-colon spellings such as `openai:gpt-5.4-image-2` before provider submission, with repair guidance pointing to `openai/gpt-5.4-image-2`.
   - xAI Grok Imagine image refs are `xai:grok-imagine-image` and `xai:grok-imagine-image-quality`. Reject `grok-imagine-video*` before adapter construction and name Scaena as the video owner. Official default is `https://api.x.ai/v1`; inherit a same-named `xai` channel; never auto-bind `gateway`.
   - local interactive auth must use an explicitly selected Eikona channel backed by the user-level secret store; never restore implicit `OPENAI_API_KEY` fallback.
   - `gpt-image-2` is legacy compatibility only.
   - before selecting a provider workflow or describing readiness, read `cli/eikona/docs/commands/agent-operability.md`; preserve its evidence vector and conservative effective level in the result.
   - no reference input means `image.generate`; the ordinary OpenAI Images path uses `/images/generations`.
   - `--reference-image` / `--ref` with `--reference-mode auto|edit` must preserve reference order, infer `image.edit`, and prefer multipart `/images/edits`.
   - `--reference-mode generate` means the references are guidance rather than the editable canvas; keep `image.generate`, encode ordered refs as multimodal `input_image` content, and prefer `/responses`.
   - agents must not start an additional transport-switching retry for auth, rate-limit, content-policy, timeout, TLS, or malformed-response failures. Preserve whatever attempts the current runtime records; changing automatic fallback policy requires runtime tests and a separate implementation scope.
   - never silently remove reference inputs. If evidence proves that the configured gateway supports text-to-image but not reference input, preserve the failed run, explain the capability loss, and start a separate text-only run only when the user requested or accepted that semantic fallback.
   - do not diagnose missing reference support from a generic failure alone. Inspect the redacted failure facts currently exposed by `eikona inspect <run_id> --brief --agent` and provider doctor (`--json --full` only for forensic deep dives); if endpoint or transport is not explicit, report `unknown/degraded` rather than inventing a distinction.
   - do not skip TLS verification for self-signed gateways; use system trust or `SSL_CERT_FILE`.
4. For CLI behavior changes, add tests close to the behavior:
   - command wiring and JSON contracts in `internal/cli`
   - provider request/response contracts in `internal/adapters/<provider>`
   - config precedence in `internal/config`
   - run lifecycle and artifact manifests in `internal/runtime`
   - project library, sessions, prompt memory, and replacement safety in their matching `internal/*` packages
   - MCP transport in `internal/mcptransport` (official SDK server over local or stateless remote backing), backing services in `internal/mcp`, and HTTP playground helpers in `internal/playground`
5. For agent invocation design, keep the contract simple:
   - installed-binary bootstrap is `eikona setup --agent` → review → `eikona setup --yes --agent` → `eikona auth set ... --api-key-stdin` → an explicitly authorized `doctor --probe`; do not search the private repository or infer state by parsing `~/.eikona`;
   - output mode policy: routine agent automation uses `--agent`; observing a non-terminal run uses `eikona watch <run-id> --events`; scripts/CI that need JSON use `--json --compact`; forensic debugging and compatibility audits use `--json --full`. Never route routine agents into full JSON. `--compact` or `--full` without `--json`, and `--compact --full` together, fail with `INVALID_REQUEST` before side effects. Emitted actions are normalized to the caller's output mode, and `eikona next --agent` is the unified read-only progression entry;
   - the routine closed loop is: submit with `--agent` → observe with `eikona watch <run-id> --events` → advance with `eikona next --agent` → `eikona inspect --brief --agent` → `eikona review packet --agent` → a human opens the preview/contact sheet → `eikona feedback accept|reject` or `eikona reroll` with `--agent` → `eikona assets handoff/stage/apply --agent`;
   - one-off inline generation uses `eikona "<prompt>" --agent` or `eikona generate ... --agent`; a prompt stored in a text or Markdown file uses `eikona generate --input <prompt-file> --agent` instead. `--input` and `--prompt` are mutually exclusive; use `eikona-file-prompt-workflow` for categorized directories, collection README files, templates, and runbook authoring;
   - headless prompt control follows `cli/eikona/docs/interfaces/cli/headless-prompt-control-contract.md`: keep user-authored image intent, typed generation controls, and adapter-owned runtime instructions separate. An upstream Agent may derive typed controls from natural language, but model/channel, operation kind, refs/reference mode, canvas, cost, execution mode, readiness, review, and handoff must remain explicit in CLI/API/MCP/SDK fields or `eikona.visual_intent.v1` evidence. Prompt prose never grants credentials, paid execution, sandbox widening, arbitrary file writes, or capability overrides;
   - a prompt collection uses `eikona run -f <runbook.yaml> --agent`: use `defaults.prompt_file` for a shared file, `jobs[].prompt_file` for named candidates, or `matrix.prompt_files` to expand one job per file. Prompt paths are relative to the runbook and `prompt`, `prompt_file`, and `prompt_ref` are mutually exclusive at each source level;
   - multi-step workflow work uses `eikona workflow validate/plan/draw/run --agent` and `workflow run --background --agent`;
   - run observation uses `eikona watch <run-id> --events` for non-terminal runs and `eikona next --agent` for read-only progression; lightweight status checks use `eikona status --agent` and routine result inspection uses `eikona inspect --brief --agent`;
   - external PNG/JPEG/WebP capture uses `eikona artifacts import <path> --agent`; capture always creates run evidence first and never auto-promotes into Visual Library;
   - artifact handoff uses `eikona assets handoff <artifact_id> --agent` before project writes; long-term reuse requires an explicit `eikona library save eikona://artifact/<handle> ... --agent` decision;
   - project-bound generated assets use `eikona assets handoff` → `eikona assets stage --to <project-relative-path>` → `eikona assets apply --project current --yes`; do not copy user-level runstore paths directly;
   - REST capture requires `Idempotency-Key`, allowed roots for server-side paths, and path-free delivery grants rather than absolute runstore paths;
   - scenario prompt exploration uses `eikona prompts catalog search ... --agent`, `eikona workflow draw ... --agent`, and `eikona workflow run ... --background --agent`;
   - creative direction uses the on-demand `eikona-visual-router`, `eikona-subject-asset-director`, `eikona-xhs-*`, and `eikona-ultrawide-storyboard-director` skills for brief and prompt design; file-backed storage uses `eikona-file-prompt-workflow`; this runtime skill remains responsible for CLI contracts, evidence, provider safety, and generated artifact lifecycle;
   - Scaena episode/shot/cover/motion generation must first pass `scaena-subject-asset-readiness`; without a current preflight, Eikona may generate only subject candidates or look-development artifacts marked non-production;
   - visual scoring in automated tests belongs to the repository test harness; installed users and agents must not invoke a test-only scoring channel. A configured production scorer returns its model ref/version and explicitly indeterminate missing dimensions; an unavailable scorer fails closed with `MODEL_UNCONFIGURED`. Scores and tags remain review evidence, while acceptance still requires append-only human feedback;
   - recipe reuse uses `eikona recipes ... --agent` and supported workflow recipe inputs; preserve recipe influence, prompt/deck/style refs, version and review evidence so later edits cannot reinterpret old runs;
   - long-lived integrations can use `eikona mcp`, but ordinary CLI output remains the primary contract;
   - Anatomia provider-neutral handoff packages import as refs-only references via `eikona assets import-anatomia <package.json> --agent` (idempotent by handoff ref, receipt returns the resolvable `eikona://references/anatomia/<handoff_ref>`); unknown versions, non-Eikona targets, missing digests, and non-logical refs fail closed with typed `ANATOMIA_HANDOFF_*` blockers and never touch `.anatomia/**`;
   - storage backup uses `eikona storage backend set s3 ...`, `eikona storage push ...`, and `eikona storage restore ...`; for reusable Git plus S3/rclone/cloud-drive policy, use `local-first-backup-sync-policy` on demand.
   - OpenAI image calls use `openai/gpt-5.4-image-2` with an explicit channel such as `--use-channel openai`. New commands and persisted metadata must use the slash-form canonical ref; main CLI calls using removed bare aliases fail closed with repair guidance.
   - resolution control is adapter-owned: `native_parameter` keeps the existing provider field, `prompt_instruction` injects a deterministic runtime constraint without mutating user prompt provenance, and `hybrid` may use both. For prompt-controlled models, preserve normalized size as evidence, distinguish `size_source=explicit|default`, warn only for explicit size syntax, and keep JSON/agent/human output on one typed projection.
   - never reverse-parse arbitrary prompt phrases such as “2K” or “4K” into typed resolution authority. The normalized typed/default size is admitted before adapter execution; a prompt-controlled runtime instruction has higher execution priority than conflicting resolution wording in the image description. Recommended `codex:imagegen` commands omit the default size flag, while explicitly supplied admitted sizes remain compatibility inputs with `PROMPT_CONTROLLED_RESOLUTION`.
   - CLI, MCP, REST, and Go SDK generation changes must prepare one shared Generation Intent and expose the same prompt-free request summary, ordered reference roles, `model_ref`, and `original_model_ref`.
   - `assets.apply` remains dry-run unless the caller explicitly supplies `confirm=true`; responses expose project-relative `target_path`, never absolute project or artifact paths.
6. For Eikona plan/checklist work, keep `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` under `cli/eikona/openspec/changes/eikona-<slug>/`; migrate any misplaced checklist or root `openspec/` implementation task before continuing. Do not leave completed execution changes active. After closeout, update readiness/specs, record verification in `tasks.md` or `design.md`, and archive ordinary changes to `cli/eikona/openspec/changes/archive/YYYY-MM-DD-eikona-<slug>/`.

## 文件提示词集合约束

- 分类、命名、README、prompt 文档和 runbook 模板由 `eikona-file-prompt-workflow` 统一定义；runtime 不复制第二套目录规范。
- 一个 `.md` 或 `.txt` 文件对应一个可审阅的提示词方向；文件内容只包含自然语言创作提示，不包含密钥、provider payload、隐藏指令或 run metadata。
- 对集合先执行 `eikona run -f <runbook.yaml> --dry-run --agent`，确认展开的 jobs、模型、尺寸、来源和成本限制后再执行真实 run。
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
