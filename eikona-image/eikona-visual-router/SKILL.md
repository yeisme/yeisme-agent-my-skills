---
name: eikona-visual-router
description: Use when the user explicitly requests Eikona/eikona visual generation, temporary image persistence, durable asset management, categorized file-backed prompt libraries or collections, gateway setup, Scaena subject or production visuals, or cross-project product assets, and when routing requests across asset lifecycle, prompt-file workflow, Scaena readiness, Auctra handoff, subject asset direction, Xiaohongshu static assets, ultrawide storyboards, general image generation, and CLI/runtime work.
---

# Eikona 视觉路由器

先读取 `cli/eikona/docs/commands/agent-operability.md` 的 evidence vector 和 conservative effective level，再判断 provider 是否可用、视觉请求的 owner、用途和证据链，并加载最小的 Eikona workflow/director skill。路由器不直接包办最终 prompt 或图像生成；effective level 未达到 live-ready 时，不得把配置、fixture 或 model probe 描述为已可付费生成。

用户明确说“用 Eikona / eikona 出图 / Eikona 生成”时，本路由优先于通用 `imagegen` 或内置图片工具。先进入 `cli/eikona` 并使用 Eikona CLI；只有 Eikona 不可用且用户确认 fallback 时，才允许改用其他图片工具。

用户说“提示词文档”“提示词库”“分门别类”“提示词集合”“从文件加载提示词”或“一组 prompt 批量出图”时，加载 `eikona-file-prompt-workflow`。单张读取一个 text/Markdown 文件；多张通过 runbook 的 `prompt_file` / `prompt_files` 引用一组文件。不要把集合拼成长命令行字符串，也不要把提示词正文塞进 run evidence 或 provider 配置。

## 输入

- 用户请求、目标平台、视觉用途、已有项目上下文和素材来源。
- 可选：网关 base URL、API key、channel、准确 model ID 和 transport。
- 可选：Auctra content unit / Story Bible source entity、参考图、期望比例、是否要本地 fixture 验证、是否需要转视频。
- 可选：Scaena project/ProductionGraph/subject/shot refs、purpose、frozen subject versions、generation preflight 或 correction plan。
- 可选：Web/App/docs/developer tool 的目标页面、资产用途和交付路径。
- 可选：单个 prompt 文件，或 prompt collection 的 runbook、文件清单、目标模型、尺寸与候选数量。
- 可选：Codex/imagegen 或其他工具临时生成的 PNG/JPEG/WebP、目标 project/global scope、来源 metadata 和长期复用意图。

缺 owner 或用途时，先从请求中提取；仍无法区分时，只问一个最小澄清问题。

## 输出

- 推荐 skill、推荐理由、owner 边界和下一步动作。
- 需要运行的真实 Eikona/Auctra 命令骨架。
- review、feedback、handoff 证据链要求。

## 路由表

| 用户意图或素材来源 | 路由目标 | 说明 |
| --- | --- | --- |
| 提示词文档化、分类提示词库、从文件出图、批量 prompt collection、迁移长 `--prompt` 命令 | `eikona-file-prompt-workflow` → `yeisme-eikona-cli-runtime` | 前者负责目录、文档、模板与 runbook；后者负责 CLI schema、provenance、provider 和 run evidence。需要创意方向时再配对一个领域 director。 |
| 提供 base URL、API key、channel、模型 ID，要求安装/配置/调通 Eikona，或诊断网关是否支持编辑/参考图输入 | `eikona-gateway-bootstrap` | 用户级安全接入；分别验证纯文生图、`/images/edits` 和 `/responses` multimodal；key 只走 stdin，不进入参数或项目文件；Nano Banana 使用网关准确 ID。 |
| 临时图片持久化、Codex/imagegen 文件回收、project/global scope、长期资产库、下载授权、资产 REST/OpenAPI | `eikona-asset-lifecycle` | 先捕获为 synthetic import run，再显式保存进 Visual Library；不得把临时文件直接当长期资产。 |
| Web、App、docs、developer tool、landing page、hero、feature、empty state、social card、product mockup | `eikona-product-asset-director` | 从项目上下文形成 visual brief，经 Eikona review/feedback/handoff/apply 交付仓库。 |
| Auctra accepted content、Story Bible、小说设定、创作者素材导出视觉 brief | `eikona-auctra-visual-router` | Auctra 负责内容上下文、brief、review 和 import-handoff；Eikona 负责 provider workflow、run evidence 和 artifact handoff。 |
| Scaena 角色定妆、主体参考资产、人物一致性、服装/地点/道具/风格包、剧集/镜头/封面/动态视觉 | `scaena-subject-asset-readiness` → `eikona-subject-asset-director` | 先由 Scaena 判定 candidate-only 或 production-ready；未冻结/无 preflight 时只允许主体候选/lookdev/correction，不得直接生成剧集资产。 |
| 小红书封面、3/6/9 图文卡片、信息图、漫画静态图文 | `eikona-xhs-visual-router` | 继续分派到 cover/card/infographic/comic director。 |
| 非 Scaena 的超宽连续空间故事看板、动作调度图、影视预演、历史战役推演长卷、从看板转视频镜头 | `eikona-ultrawide-storyboard-director` | 用一个连续背景空间表达多个时间点；Scaena production context 必须先通过 subject readiness/preflight。 |
| 单张通用图片、参考图编辑、provider 适配、run evidence、workflow/prompt deck/recipe/assessment/runtime 行为 | `yeisme-eikona-cli-runtime` | 这是 CLI/runtime owner，不替代文件提示词组织或具体创意导演。 |

## 工作流

1. 判断是否已有可用 provider。提供网关或缺少凭据时先交给 `eikona-gateway-bootstrap`。
2. 判断 owner：外部资产生命周期、Scaena production、产品仓库、Auctra 内容链、小红书、影视/故事看板、还是 Eikona CLI/runtime。
3. Scaena context 先判定 purpose。episode/shot/cover/motion 必须路由 `$scaena-subject-asset-readiness`；只有 candidate/lookdev/correction 或 current passed preflight 才可继续 Eikona。
4. 判断是否已有 accepted source。Auctra 来源必须先通过 Auctra review；外部临时图片先交给 `eikona-asset-lifecycle` 捕获，普通素材必须确认权限和禁用项。
5. 选择最小 skill；需要文件落盘时同时加载 `eikona-file-prompt-workflow`，但只选择一个创意 director。当已有可复用的视觉方向或资产集合时，优先用 `eikona themes` 和 `eikona library collections` 引用既有 theme/asset refs，而不是重新描述或复制素材：先 `eikona themes list` / `eikona library collections list` 查找匹配 alias，再在 workflow 的 `theme_bindings` / `collection_bindings` 里绑定 canonical URI，让 plan 记录不可变 snapshot。
6. 要求下游输出：visual brief、推荐命令、review packet、feedback、handoff/apply 下一步，以及 Scaena context 的 freeze/preflight/consistency 下一步。
7. 本地验证默认用 `fixture:image`；Eikona 真实远程默认用 canonical ref `openai/gpt-5.4-image-2`。短别名 `gpt-5.4-image-2` 与 `gpt-image-2` 可接受；历史 `openai/gpt-5.4-image-2` 只为兼容读取。网关其他模型必须复制准确完整 model ID。
8. 尺寸参数必须显式设置：用户未指定尺寸时统一使用 `--size 2k` 或 runbook `size: 2k`；用户明确给出其他 size 时原样设置，不换算、不降级。比例继续用 `--aspect` 单独表达，不能用 1024/1536 示例替代 2K 请求。

新的 Eikona 调用默认绑定用户级 channel，不依赖项目内复制的 credential 或 `.env`：

```bash
eikona providers doctor --channel openai --model openai/gpt-5.4-image-2 --probe --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input ./prompt.md --size 2k --aspect 2:3 --agent
```

`gpt-5.4-image-2` 与 `gpt-image-2` 是兼容短名；新 skills、prompt 文件、runbook 和文档一律写 `openai/gpt-5.4-image-2`。`openai/gpt-5.4-image-2` 只允许出现在 legacy migration 或兼容性测试说明中。

韩国转绘网关使用 slash ID，并显式选择已保存密钥的 channel：

```bash
eikona models readiness openai/gpt-5.4-image-2 --channel openai --agent
eikona providers doctor openai --channel openai --model openai/gpt-5.4-image-2 --probe --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input ./prompt.md --size 2k --aspect 2:3 --agent
```

不得把 slash ID 改成 `openai/gpt-5.4-image-2`，不得隐式读取 `OPENAI_API_KEY`。

## 文件提示词与出图集合

- 先按 `eikona-file-prompt-workflow` 的 `owner/asset-type/collection/candidate` 规范建立目录、README、prompt 文件和 runbook。
- 每个提示词文件只放可审阅的自然语言提示词；推荐使用 `.md` 或 `.txt`，并以一个文件对应一个可追踪的视觉方向或候选。
- 单文件生成使用 `generate --input`。`--input` 与 `--prompt` 互斥。
- 集合生成使用一个已有 runbook；`defaults.prompt_file` 适合共享基础提示词，`jobs[].prompt_file` 适合命名候选，`matrix.prompt_files` 适合逐个展开同一批提示词文件。文件路径相对于 runbook 所在目录解析。
- `prompt`、`prompt_file`、`prompt_ref` 在同一 defaults、matrix entry 或 job 中互斥。先 `--dry-run` 检查扩展结果，再批准真实 provider run。
- prompt 文件是可编辑的创作输入；runbook、`prompt_sources.json`、队列和 run evidence 是结构化资产，必须通过 Eikona CLI 创建或推进，不能由 agent 直接改写。

输出模式政策：例行自动化一律用 `--agent`；非终态 run 用 `eikona watch <run_id> --events` 观察，`eikona next --agent` 是统一只读推进入口；脚本/CI 需要 JSON 时用 `--json --compact`；取证/兼容性审计用 `--json --full`。共存期内裸 `--json` 仍是 legacy full，不要把例行 agent 推向 full JSON；`--compact`/`--full` 不带 `--json` 或两者同给会在副作用前报 `INVALID_REQUEST`。emitted actions 会按调用方输出模式自动归一化。

## 命令骨架

普通 Eikona 文件生成：

```bash
eikona generate --model fixture:image --aspect 3:1 --size 2k --input prompts/story/storyboard/scene/prompts/01-planning-board.md --dry-run --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --aspect 3:1 --size 2k --input prompts/story/storyboard/scene/prompts/01-planning-board.md --agent
eikona review packet <run_id> --agent
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --agent
eikona assets handoff <artifact_id> --agent
```

直接从提示词文件出图：

```bash
eikona generate --model fixture:image --input prompts/product/landing-hero/launch/prompts/01-clean-editorial.md --size 2k --dry-run --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input prompts/product/landing-hero/launch/prompts/01-clean-editorial.md --size 2k --agent
```

从提示词集合批量出图。runbook 中使用 `defaults.prompt_file`、`jobs[].prompt_file` 或 `matrix.prompt_files` 引用 `prompts/*.md`；先验证计划，再执行：

```bash
eikona run -f prompts/product/landing-hero/launch/runbook.yaml --dry-run --agent
eikona run -f prompts/product/landing-hero/launch/runbook.yaml --background --agent
eikona watch <run_id> --events
```

网关首次接入：

```bash
eikona init --user --agent
eikona auth check gateway --agent
eikona projects register . --agent
```

Auctra 来源必须先走 brief/export/import：

```bash
auctra visual brief <unit-id> --profile short_video_storyboard --json
auctra review accept <review_item_id> --json
auctra visual export-brief <brief-id> --for eikona --to .auctra/exports/<brief-id>.json --json
eikona workflow import auctra -f .auctra/exports/<brief-id>.json --out .eikona/workflows/<brief-id>.workflow.yaml --agent
```

## 边界

- 不直接调用 provider SDK，不绕过 Eikona CLI evidence。
- 不把 key 放入命令参数、项目文件、日志或结构化输出；配置凭据必须使用默认用户级 `eikona auth set <channel> --api-key-stdin` 流程。
- 不猜测 Nano Banana、Gemini 或其他网关模型 ID。
- 不把 Auctra 的 accepted canon、review 决策或 `.auctra/**` 状态手写到文件里。
- Auctra 上下文的视觉请求优先进入 `eikona-auctra-visual-router`；不能把它降级成通用图片工具或绕过其 brief/review/export/handoff 链路。
- Scaena 上下文不能因“先出几张看看”直接路由 storyboard/generic generate；未通过 readiness 时只允许 non-production candidate/lookdev，并明确标注不可绑定 episode/shot。
- 不把 Eikona accepted candidate、图片相似度或文件数量描述成 Scaena frozen/production accepted。
- 不把用户级 runstore 的临时输出路径直接写入项目；项目落盘必须走 `assets handoff` → `assets stage` → `assets apply`。
- 不把原始提示词、供应商载荷、私密素材、隐藏系统提示或完整思维链写入结构化资产。
- 不新增 Eikona 默认图像模型；真实远程示例使用 `openai/gpt-5.4-image-2`，别名只用于兼容输入。

## 验证

- 推荐必须匹配 owner 和视觉用途。
- router 不直接产出最终 prompt；它只输出分派、边界和下一步。
- 展示给用户的命令必须是真实可运行命令。

## 视觉意图契约 (visual_intent.v1)

本路由器是推荐的公共入口。路由后输出 `eikona.visual_intent.v1` 意图的 `skill_chain`、`scenario` 和未决输入，不直接产出最终 prompt 或调用 provider。

详见 `references/visual-intent-contract.md`（意图契约）和 `references/role-outputs.md`（角色输出模板）。

编译意图到工作流：

```bash
eikona workflow import intent -f visual-intent.yaml --out workflow.yaml --agent
eikona workflow validate -f workflow.yaml --agent
eikona workflow plan -f workflow.yaml --agent
```
