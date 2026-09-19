---
name: eikona-visual-router
description: Use when the user explicitly requests Eikona/eikona visual generation, temporary image persistence, durable asset management, categorized file-backed prompt libraries or collections, gateway setup, Scaena subject or production visuals, or cross-project product assets, and when routing requests across asset lifecycle, prompt-file workflow, Scaena readiness, Auctra handoff, subject asset direction, Xiaohongshu static assets, ultrawide storyboards, general image generation, and CLI/runtime work.
---

# Eikona 视觉路由器

先读取 `cli/eikona/docs/commands/agent-operability.md` 的 evidence vector 和 conservative effective level，再判断 provider 是否可用、视觉请求的 owner、用途和证据链，并加载最小的 Eikona workflow/director skill。路由器不直接包办最终 prompt 或图像生成；effective level 未达到 live-ready 时，不得把配置、repository test harness 或 model probe 描述为已可付费生成。

用户明确说“用 Eikona / eikona 出图 / Eikona 生成”时，本路由优先于通用 `imagegen` 或内置图片工具。先进入 `cli/eikona` 并使用 Eikona CLI；只有 Eikona 不可用且用户确认 fallback 时，才允许改用其他图片工具。

当用户没有付费 OpenAI/gateway key，但本机已登录 Codex 时，隐式 `eikona generate --prompt ... --agent` 会默认走 `codex:imagegen` 预览回退。结果会带 `model_selection`、`capability_class=preview`、`size_class=1k`、`auth_class=codex_session`、`resolution_control=prompt_instruction`。推荐省略 `--size 1k`：Eikona 会把默认 1K 约束注入 `codex exec` 的 stdin 提示词；显式传入受支持尺寸仍兼容，但会返回 `PROMPT_CONTROLLED_RESOLUTION` warning。请求 `2k`/`4k`、参考图或 edit 不会静默降级。生产级 2K/编辑仍走 `openai/gpt-5.4-image-2`。先跑 `eikona providers doctor codex --agent`，不要把 1K 上限说成工具故障。

用户说“提示词文档”“提示词库”“分门别类”“提示词集合”“从文件加载提示词”或“一组 prompt 批量出图”时，加载 `eikona-file-prompt-workflow`。单张读取一个 text/Markdown 文件；多张通过 runbook 的 `prompt_file` / `prompt_files` 引用一组文件。不要把集合拼成长命令行字符串，也不要把提示词正文塞进 run evidence 或 provider 配置。

自然语言到 Eikona 的对接遵循 `cli/eikona/docs/interfaces/cli/headless-prompt-control-contract.md`：router/director 可以把用户请求拆成 image intent 与 provider-neutral typed controls，但不能把 model/channel、operation kind、refs/reference mode、canvas、cost、execution mode、readiness、review 或 handoff 隐藏在最终 prompt 中。单次简单生图直接走 prompt-first/generate CLI；复杂请求输出 `eikona.visual_intent.v1`，再由 Eikona workflow compiler 执行。Provider runtime instruction 始终由 Eikona adapter 构造。

## 精准区域编辑路由

先区分参考图指导生成与严格编辑。定妆、姿态变化、多人组合、开场构图和允许重绘的场景校正优先明确指定 `--reference-mode generate`，保留有序图片与identity/wardrobe/layout用途；蒙版、局部修补及画布保持要求才路由严格编辑。不要依赖 `auto` 猜测，也不要把这条Skill建议宣称成CLI已改变默认行为。

通道的文生图、单/多参考图生成、严格编辑、蒙版和透明输出能力分开判断。已授权重绘且编辑明确不可用时，可新建参考图生成run并关联原失败来源；不得丢图改纯文生图。单次HTTP 500只证明失败，不证明能力不支持；认证、限流、超时或提交结果未知不能触发自动接口切换。用户已有对应授权时不重复问；缺少授权且会损失明确保持要求时才询问。

做剧请求先消费 `ai-drama-router` 的本轮目标，按demo、单集交付、跨集复用或模块化资产库选择必要资产。快速demo不以透明通道、六视图或完整拆层为默认前提；复用和正式接受门禁仍由对应owner管理。

用户提供原图与圈线、箭头、编号标注，或要求蒙版局部修改时，加载 `eikona-mcp-image` 的精准编辑流程；CLI 操作由 `yeisme-eikona-cli-runtime` 配套。先确认已安装版本实际提供 precision controls。保留用户／Agent 指定的模型和渠道，不强制 Sunburst、最高质量或更换全局默认。Agent 已理解区域时直接提供 typed regions，避免重复识图；只在目标、说明或重叠冲突不明确时要求预览澄清。清楚请求默认合并为单轮编辑，不逐区生成或自动重做。

## 输入

- 用户请求、目标平台、视觉用途、已有项目上下文和素材来源。
- 可选：网关 base URL、API key、channel、准确 model ID 和 transport。
- 可选：Auctra content unit / Story Bible source entity、参考图、期望比例、是否要本地 `--dry-run` 验证、是否需要转视频。
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
| Auctra accepted content、Story Bible、小说设定、创作者素材导出视觉 brief | `eikona-file-prompt-workflow` | 仅从已接受的 Auctra brief/source refs 建立可追溯候选；Eikona 负责 provider workflow、run evidence 和 artifact handoff。 |
| Scaena 角色定妆、主体参考资产、人物一致性、服装/地点/道具/风格包、剧集/镜头/封面/动态视觉 | `eikona-subject-asset-director` | 必须携带 production owner 提供的 current passed preflight evidence；未冻结/无 preflight 时只允许主体候选/lookdev/correction，不得直接生成剧集资产。 |
| 小红书封面、3/6/9 图文卡片、信息图、漫画静态图文 | `eikona-xhs-visual-router` | 继续分派到 cover/card/infographic/comic director。 |
| 非 Scaena 的超宽连续空间故事看板、动作调度图、影视预演、历史战役推演长卷、从看板转视频镜头 | `eikona-ultrawide-storyboard-director` | 用一个连续背景空间表达多个时间点；Scaena production context 必须先通过 subject readiness/preflight。 |
| 夏日抓拍写真批量候选、多维随机组合、批内去重、seed 复现 | `eikona-candid-photo-director` | 随机矩阵采样；正文模板在模板仓库 `solutions/image/candid-portrait-matrix`，技能只做采样与绑定。 |
| 城市地标系列海报/封面（ICONIC LANDMARK SERIES）、城市 spec、系列编号与变体 | `eikona-iconic-landmark-poster-director` | 固定视觉系统 + 城市参数化；正文模板在模板仓库 `solutions/image/iconic-landmark-poster`。 |
| 单镜头精调抓拍、量化机位/占幅/色板/光源、shot spec | `eikona-precision-candid-director` | 全量化单镜头；正文模板在模板仓库 `solutions/image/precision-candid-shot`，规范投递语言为英文。 |
| 付费出图、GPT Image 2.5、Sunburst、Flare、高质量 | CLI 走 `yeisme-eikona-cli-runtime`；MCP 走 `eikona-mcp-image` | 默认 `openai/gpt-image-2.5-sunburst` + `--quality high` + 像素 `--size`；复用已有 GPT Image 渠道（本机 `noemi`）；不要 `--size 2k`、不要新建渠道。 |
| 单张通用图片、参考图编辑、provider 适配、run evidence、workflow/prompt deck/recipe/assessment/runtime 行为 | `yeisme-eikona-cli-runtime` | 这是 CLI/runtime owner，不替代文件提示词组织或具体创意导演。 |

## 工作流

逐步命令、尺寸/通道例外和文件提示词集合见 [workflow.md](references/workflow.md)。正文只保留必须规则：

1. 无付费 key 且 Codex 可用时，普通文生图走 `codex:imagegen` 1K preview；付费 2K/编辑交给 `eikona-gateway-bootstrap`。
2. 先定 owner，再定 purpose。Scaena episode/shot/cover/motion 必须有 current passed preflight；否则只允许 candidate/lookdev/correction。
3. Auctra 来源必须已 review；临时图片先走 `eikona-asset-lifecycle`。只选一个创意 director；文件落盘同时加载 `eikona-file-prompt-workflow`。
4. 离线用 `--dry-run`。付费未指定模型时默认 `openai/gpt-image-2.5-sunburst`、`--quality high`、像素画布，渠道用已配置的 GPT Image 网关（本机 `noemi`），不新建 key/渠道。2.5 不可用才回退 `openai/gpt-5.4-image-2`。Flare 仅在用户要快稿。不得使用 bare alias、provider-colon 或隐式 `OPENAI_API_KEY`。
5. 精准编辑保持原图画布，优先 Sunburst。2.5 禁止 `--size 2k`。Codex preview 不写 `--size 1k`。不从 prompt 文本反推 typed controls。

命令骨架（含 2.5 像素示例）：[command-skeletons.md](references/command-skeletons.md)。视觉意图：[visual-intent-contract.md](references/visual-intent-contract.md)、[role-outputs.md](references/role-outputs.md)。编译：`eikona workflow import intent`。GPT Image 2.5 身份/尺寸：`cli/eikona/docs/commands/models.md`；MCP 无 CLI 时读 `eikona://docs/image25-mcp`。加载 `yeisme-eikona-cli-runtime` 后可读其 `references/gpt-image-2.5.md`。

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Effective level 未 live-ready | 报告 evidence vector；只做 `--dry-run` 或配置 | 不把 probe/harness 说成已可付费生成 |
| 缺凭据被说成模型未适配 | `eikona models list --source adapted` 与 `eikona auth list --agent` | 不改模型 ID 掩盖缺 key |
| Scaena 未冻结/无 preflight | 只路由 candidate/lookdev；交给 `scaena-subject-asset-readiness` | 不直接 storyboard/generic generate |
| Auctra 来源未 accept | 先走 Auctra review / visual brief | 不降级成无来源通用出图 |
| 参考图/编辑失败或 HTTP 500 | 分开判断 generate vs edit；inspect 原 run | 不丢图改纯文生图，不轮换接口 |
| `2k`/`4k` 在 Codex preview 被拒 | 说明通道上限；付费走 gateway | 不静默降级或改 prompt 尺寸 |
| 付费出图仍走 Image 2 或 `--size 2k` | 改成 Sunburst + 像素 `--size` + `--quality high` + 现有渠道 | 不新建渠道、不另要 key |

## 边界

- 不直接调用 provider SDK，不绕过 Eikona CLI evidence。
- 不把 key 放入命令参数、项目文件、日志或结构化输出；配置凭据必须使用默认用户级 `eikona auth set <channel> --api-key-stdin` 流程。
- 不猜测 Nano Banana、Gemini 或其他网关模型 ID。
- 不把 Auctra 的 accepted canon、review 决策或 `.auctra/**` 状态手写到文件里。
- Auctra 上下文的视觉请求必须保留 accepted brief/source refs，并经 `eikona-file-prompt-workflow` 建立 prompt、review 与 handoff 链路；不能降级成无来源的通用图片工具。
- Scaena 上下文不能因“先出几张看看”直接路由 storyboard/generic generate；未通过 readiness 时只允许 non-production candidate/lookdev，并明确标注不可绑定 episode/shot。
- 不把 Eikona accepted candidate、图片相似度或文件数量描述成 Scaena frozen/production accepted。
- 不把用户级 runstore 的临时输出路径直接写入项目；项目落盘必须走 `assets handoff` → `assets stage` → `assets apply`。
- 不把原始提示词、供应商载荷、私密素材、隐藏系统提示或完整思维链写入结构化资产。
- 提示词正文模板的 canonical owner 是模板仓库 promptrepo 解决方案包（`data/yeisme-prompt-templates/solutions/**`）；director 技能只持有数据 spec、编译器、采样/去重/变体合并与 tags，不在技能内复制模板正文；模板改动必须走模板仓库并用 template-registry `contract refresh` 更新 digest。语言约定：编译与投递只用 `prompts/main.en.md`，`docs/template-zh-CN.md` 为人工审阅译文、不进入编译；Scaena 项目模板遵循同一约定。
- 付费默认使用 `openai/gpt-image-2.5-sunburst`（高质量）；不要静默换回 Image 2。用户点名 Flare / Image 2 / 其他已适配模型时保留该选择。复用已有 GPT Image 渠道和 key。

## 验证

- 推荐必须匹配 owner 和视觉用途。
- router 不直接产出最终 prompt；它只输出分派、边界和下一步。
- 展示给用户的命令必须是真实可运行命令。
