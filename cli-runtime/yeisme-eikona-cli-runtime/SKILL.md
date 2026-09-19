---
name: yeisme-eikona-cli-runtime
description: Use when the user explicitly asks to use Eikona/eikona, needs post-install setup or environment discovery, or when changing, testing, reviewing, documenting, or designing Eikona CLI/runtime behavior under cli/eikona, including public distribution, Agent Skills, generation, external artifact capture, project/global asset scope, Visual Library promotion, download grants, OpenAPI/SDK contracts, prompt files, provider adapters, run evidence, project registry, replacement safety, MCP, and Go release checks.
---

# Yeisme Eikona CLI Runtime

Use this skill for `cli/eikona`, the headless image-generation and image-asset-management foundation for agents and services.

If the user explicitly says to use Eikona, `eikona`, or the Eikona CLI for image generation, this route takes precedence over generic built-in image generation tools. Enter `cli/eikona`, follow local `AGENTS.md`, and use Eikona commands such as `eikona generate ... --agent`. Only fall back to another image tool if the user explicitly changes the route or Eikona is unavailable and the user approves the fallback.

## Precision, canvas, and recovery

Read `references/precision-and-canvas.md` for precision edit, OpenRouter Image API, full-body composition, and recovery policy.

## Installed-binary bootstrap

An installed Eikona binary is self-describing. Do not search for, clone, or require the private `yeisme/eikona` repository.

Start every fresh Homebrew, Scoop, package, archive, or public Bash installation with:

```bash
eikona setup --agent
```

Follow `action.next`. Default setup is a no-write preview.

🔴 CHECKPOINT · 🛑 STOP: without the current user's explicit authority for this local write, credential, or paid generation, do not run `eikona setup --yes`, `eikona auth set`, `--smoke`, or any generate/edit command.

After local-write authority is clear:

```bash
eikona setup --yes --agent
eikona auth set openai --protocol openai --api-key-stdin --agent
eikona models list --source adapted --all --agent
```

`SKILLS_RELEASE_NOT_MIRRORED` recovery: `eikona setup --yes --skip-skills --agent`. Discovery is metadata-only (`eikona config env --all --json`); never call `eikona auth env` in ordinary agent flows. Empty `eikona models list` reads `models.lock`; next action is `--source adapted`. Missing credentials are config status, not missing adapters. Probe only when the user authorizes `eikona doctor --channel openai --model openai/gpt-5.4-image-2 --probe --agent`.

Full bootstrap catalog: `references/bootstrap.md`.

## Remote upload and current surfaces

Read `references/upload.md` for client image upload. Read `references/surfaces.md` for Grok Imagine, LAN serve, MCP, and promptrepo.

## Boundary

- Eikona owns image generation, provider execution, run/artifact evidence, review, reuse memory, asset catalog, binding, handoff, stage/apply, replacement/rollback, delivery outcomes, and consumer-neutral headless contracts.
- Eikona does not own a Web app, dashboard, browser shell, frontend navigation/auth shell, or frontend design system. Display requirements belong to an explicitly approved external consumer and must use Eikona's stable CLI/API/SDK/MCP/event/resource contracts.
- The existing `ui` discovery command and embedded root page are frozen compatibility surfaces. Do not add features to them; removing them requires a separate compatibility change with named consumers, at least one release of deprecation, migration guidance, and rollback.
- CLI entrypoint: `cli/eikona/cmd/eikona`. Command/JSON wiring: `internal/cli`. Config/credentials: `internal/config`. Adapters: `internal/adapters/*` (no CLI output, no bypassing storage). Run evidence: `internal/runtime` and `internal/runstore`.
- External capture, path-free delivery, and project service live in `internal/api/artifactimport`, `internal/api/artifactdelivery`, and `internal/api/projectservice`; reuse app/runstore/index facades instead of parallel persistence.
- Prompt layers consume one another through stable projections (`internal/prompts`, `internal/promptdeck`, workflow draw, `internal/visualmemory`, `internal/stylepack`, `internal/assessment`, `internal/recipe`). Do not create parallel stores.
- In a `cli/eikona` session, human-facing product, design, runtime, protocol, governance, evaluation, command, and delivery docs live in local `docs/**`; code behavior docs live in `README.md` and `AGENTS.md`. Root project-doc mirrors are not valid owners.
- Agent-facing command guidance: `cli/eikona/docs/commands/README.md` and `docs/commands/agent-integration.md`. Task lifecycle follows `docs/workflows/execution-slice-lifecycle.md`. Execution state stays under `cli/eikona/openspec/changes/eikona-<slug>/` or its archive.

## Workflow

1. Start inside `cli/eikona` and read `AGENTS.md`, `README.md`, and the nearest command doc. Installed-binary usage starts with `eikona setup --agent`; repository access is not required. Read-before-edit map: `references/agent-invocation.md`.
2. Preserve product contracts in `references/product-contracts.md`: headless planning only; `--json` compact default / `--json --full` forensic / routine `--agent`; artifacts under `runs/<run_id>/outputs/`; tests use `httptest`; secrets only in the user auth store; no shell credential scripts; no isolated scenario commands; storage is backup/restore only; assessment/recipe evidence is never a silent machine winner.
3. For generation and models, follow `references/generation-and-models.md` and `references/gpt-image-2.5.md`. Live paid default is `openai/gpt-image-2.5-sunburst` with `--quality high` and pixel `--size` on the existing GPT Image channel (`noemi` here). Reuse the existing key; do not create a channel. Fall back to `openai/gpt-5.4-image-2` only if 2.5 is not ready. Reject provider-colon spellings, bare `gpt-image-2.5`, and `--size 2k` on 2.5. Never silently drop reference inputs or skip TLS. Do not run paid generate without approval.
4. For CLI behavior changes, add tests next to the behavior: `internal/cli`, `internal/adapters/<provider>`, `internal/config`, `internal/runtime`, matching `internal/*`, and MCP transport.
5. Agent closed loop: submit `--agent` → `eikona watch <run-id> --events` → `eikona next --agent` → `eikona inspect --brief --agent` → `eikona review packet --agent` → human preview → `eikona feedback` / `reroll` → `eikona assets handoff/stage/apply --agent`. `assets.apply` is dry-run unless `confirm=true`. Full catalog: `references/agent-invocation.md`.
6. Keep OpenSpec under `cli/eikona/openspec/changes/eikona-<slug>/`. Migrate misplaced root `openspec/` implementation tasks before continuing. Archive completed changes to `cli/eikona/openspec/changes/archive/YYYY-MM-DD-eikona-<slug>/`.

Example (live default on the existing GPT Image gateway):

```bash
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --size 1152x2048 --aspect 9:16 --quality high --prompt "a product still life on a studio table" --agent
```

## 文件提示词集合约束

- 分类、命名、README、prompt 文档和 runbook 模板由 `eikona-file-prompt-workflow` 统一定义；runtime 不复制第二套目录规范。
- 一个 `.md` 或 `.txt` 文件对应一个可审阅的提示词方向；文件内容只包含自然语言创作提示，不包含密钥、provider payload、隐藏指令或 run metadata。
- 对集合先执行 `eikona run -f <runbook.yaml> --dry-run --agent`，确认展开的 jobs、模型、尺寸、来源和成本限制后再执行真实 run。
- CLI 会为单文件和 runbook job 记录 prompt source provenance 与 run-owned snapshot。不得手改 `prompt_sources.json`、snapshot、batch plan、queue 或 run evidence；通过 Eikona CLI 重建或推进它们。
- Auctra 来源必须携带已接受的 brief/source refs；只可从这些 refs 经 `eikona-file-prompt-workflow` 派生 prompt 文件。Eikona 是 Auctra 生图的默认和优先执行路径。

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

## Visual intent, pricing, DriveBridge

Read `references/visual-intent.md` for visual-intent evidence, canvas recovery, official pricing, and DriveBridge remote CLI.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| User said Eikona but a generic image tool ran | Stop; enter `cli/eikona` and use `eikona generate ... --agent` | Fall back only if the user approves |
| Fresh install, unknown env | `eikona setup --agent` | `eikona setup --yes --skip-skills --agent` on `SKILLS_RELEASE_NOT_MIRRORED` |
| Empty `eikona models list` | `eikona models list --source adapted --all --agent` | Missing credentials are config status, not missing adapter |
| Paid generate without approval | Do not run `--smoke` or generate | Ask for provider/model/cost authority |
| Secret in output | Redact; use `--api-key-stdin` / auth store | Never `eikona auth env` in ordinary agent flows |
| Library auto-promote after import | Keep run evidence only | Explicit `eikona library save` |
| `assets.apply` wrote files | Must be dry-run unless `confirm=true` | Restore via owner CLI, do not copy runstore paths |
| Generic provider error | `eikona inspect <run_id> --json --full` for `fail_reason` | Do not silently reword prompts and retry |
| Live generate used Image 2 or `--size 2k` | Switch to `openai/gpt-image-2.5-sunburst`, pixel `--size`, `--quality high`, existing channel | Do not create a new channel or request a new key |
| Bare `gpt-image-2.5` | Use Sunburst | Do not guess Flare unless the user wants speed |
| `xhigh`/`max` on gpt-5.4-image-2 | Reject before submit | Those quality values are 2.5-only |
