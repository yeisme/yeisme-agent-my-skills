# Eikona 视觉路由工作流细节

Router 正文只保留必须规则。本文件保存逐步命令、尺寸/通道例外和文件提示词集合。

## 逐步路由

1. 判断是否已有可用 provider。付费 OpenAI/gateway 不可用且本机 Codex session 可用时，普通文生图走 `codex:imagegen` 预览回退，并明确告诉用户这是 1K preview。提供网关或用户明确要付费 2K/编辑时交给 `eikona-gateway-bootstrap`。
2. 判断 owner：外部资产生命周期、Scaena production、产品仓库、Auctra 内容链、小红书、影视/故事看板、还是 Eikona CLI/runtime。
3. Scaena context 先判定 purpose。episode/shot/cover/motion 必须提供 production owner 的 current passed preflight evidence；否则只允许 candidate/lookdev/correction，不得继续 production Eikona generation。
4. 判断是否已有 accepted source。Auctra 来源必须先通过 Auctra review；外部临时图片先交给 `eikona-asset-lifecycle` 捕获，普通素材必须确认权限和禁用项。
5. 选择最小 skill；需要文件落盘时同时加载 `eikona-file-prompt-workflow`，但只选择一个创意 director。当已有可复用的视觉方向或资产集合时，优先用 `eikona themes` 和 `eikona library collections` 引用既有 theme/asset refs，而不是重新描述或复制素材：先 `eikona themes list` / `eikona library collections list` 查找匹配 alias，再在 workflow 的 `theme_bindings` / `collection_bindings` 里绑定 canonical URI，让 plan 记录不可变 snapshot。
6. 要求下游输出：visual brief、推荐命令、review packet、feedback、handoff/apply 下一步，以及 Scaena context 的 freeze/preflight/consistency 下一步。
7. 本地离线验证使用 `--dry-run`，不提交 provider 请求；repository test harness 不属于 installed-user/agent workflow。付费未指定模型时使用 `openai/gpt-image-2.5-sunburst`、`--quality high`、像素 `--size`，渠道复用已配置 GPT Image 网关（本机 `noemi`）。Flare 仅在用户要快稿；2.5 不可用才回退 `openai/gpt-5.4-image-2`。禁止 `--size 2k` 和裸 `gpt-image-2.5`。不要新建渠道或另要 key。
8. 精准区域编辑保持原图画布，由 owner 做最小补齐及裁回，不自动附加 `--size 2k` 或改变比例；需要缩放时先明确准备新原图。普通生成的尺寸参数按 provider 控制方式处理：付费 OpenAI/gateway 原生参数路径在用户未指定尺寸时统一使用 `--size 2k` 或 runbook `size: 2k`；用户明确给出其他 size 时原样设置，不换算、不降级。`codex:imagegen` 是 `prompt_instruction` 路径，推荐不写 `--size 1k`，由 runtime 自动向提示词注入 1K 约束；只有确需指定受支持画布时才保留显式 `--size` 并接受 warning。请求 2k/4k 会在提交前失败，这是通道上限。比例继续用 `--aspect` 单独表达，不能用 1024/1536 示例替代 2K 请求。
9. 用户点名 Grok 或 Midjourney 时先确认通道能力再发命令：Midjourney（如 huanwang 通道）没有原生分辨率控制，`--size 1k|2k|4k` 会在提交前失败、`--aspect` 当前被适配器丢弃——画幅改用 `--set aspect_ratio=W:H` 或 `--size WxH`，原生 2K 需求直接说明 MJ 给不了并建议 openai 通道；Grok Imagine 编辑对写实人物的换装/泳装类请求容易被 provider 内容审核拒绝（`CONTENT_REJECTED`），被拒后如实报告审核归因，不要静默改写提示词反复重试。详见 `yeisme-eikona-cli-runtime` 的 provider flag 支持矩阵。
10. 不从最终 prompt 文本反向推断 provider 权限或 typed controls。用户说“不要付费”“使用参考图”“编辑背景”“竖版 2K”时，router 必须把这些决定映射到明确的 model/channel、reference mode、canvas 或 execution policy；若无法安全映射，就保留为未决输入而不是让 provider 自行猜测。

## 模型与凭据探测

选模型前先分清「代码已适配」和「本机已配置」。缺凭据不得说成模型未适配：

```bash
eikona models list --source adapted --all --agent
eikona models list --source adapted --provider openai --all
eikona models default show --agent
eikona auth list --agent
```

新的 Eikona 调用默认绑定用户级 channel，不依赖项目内复制的 credential 或 `.env`：

```bash
eikona providers doctor codex --agent
eikona generate --prompt "preview icon" --agent
eikona providers doctor --channel openai --model openai/gpt-5.4-image-2 --probe --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input ./prompt.md --size 2k --aspect 2:3 --agent
```

新 Skills、prompt 文件、runbook、文档和 evidence 在引用旧默认模型时使用 `openai/gpt-5.4-image-2`，其他明确选择的模型保留其 canonical ref。不要在新示例中使用旧默认模型的 bare aliases；兼容入口由 owner 负责归一化。

韩国转绘网关使用 slash ID，并显式选择已保存密钥的 channel：

```bash
eikona models readiness openai/gpt-5.4-image-2 --channel openai --agent
eikona providers doctor openai --channel openai --model openai/gpt-5.4-image-2 --probe --agent
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --input ./prompt.md --size 2k --aspect 2:3 --agent
```

不得使用 bare `gpt-5.4-image-2`、`gpt-image-2` 或 provider-colon/重复前缀/下划线变体；不得隐式读取 `OPENAI_API_KEY`。

## 文件提示词与出图集合

- 先按 `eikona-file-prompt-workflow` 的 `owner/asset-type/collection/candidate` 规范建立目录、README、prompt 文件和 runbook。
- 每个提示词文件只放可审阅的自然语言提示词；推荐使用 `.md` 或 `.txt`，并以一个文件对应一个可追踪的视觉方向或候选。
- 单文件生成使用 `generate --input`。`--input` 与 `--prompt` 互斥。
- 集合生成使用一个已有 runbook；`defaults.prompt_file` 适合共享基础提示词，`jobs[].prompt_file` 适合命名候选，`matrix.prompt_files` 适合逐个展开同一批提示词文件。文件路径相对于 runbook 所在目录解析。
- `prompt`、`prompt_file`、`prompt_ref` 在同一 defaults、matrix entry 或 job 中互斥。先 `--dry-run` 检查扩展结果，再批准真实 provider run。
- prompt 文件是可编辑的创作输入；runbook、`prompt_sources.json`、队列和 run evidence 是结构化资产，必须通过 Eikona CLI 创建或推进，不能由 agent 直接改写。

输出模式政策：例行自动化一律用 `--agent`；非终态 run 用 `eikona watch <run_id> --events` 观察，`eikona next --agent` 是统一只读推进入口；脚本/CI 需要 JSON 时用 `--json --compact`；取证/兼容性审计用 `--json --full`。从 v0.6.0 起裸 `--json` 已是 compact 默认投影（等价 `--json --compact`），不要把例行 agent 推向 full JSON；`--compact`/`--full` 不带 `--json` 或两者同给会在副作用前报 `INVALID_REQUEST`。emitted actions 会按调用方输出模式自动归一化。

命令骨架见 [command-skeletons.md](command-skeletons.md)。
