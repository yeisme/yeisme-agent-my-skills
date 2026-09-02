## Why

现有 `scaena-storyboard-breakdown` Skill 已覆盖 source、run、review、revise、patch、accept 和 export，但它把 `skill:scaena-storyboard-breakdown` 同时当作操作流程和模型 instruction profile，且默认命令只能入队，用户需要自行猜测何时查询、如何选择 profile、何时读取 findings。

本变更演进现有 Skill，不创建第二个 writer：Skill 输出一个最小 `DramaRoutePlan`，选择 typed direction 与 immutable PromptRepo solution，然后调用 Scaena 的真实 foreground/async CLI 或 MCP，保留所有成本、canonical mutation 和导出门禁。

## Owner Fit

- **Admission：`fit`（workflow instruction）。** Skill 拥有意图路由、交互顺序、审批提醒、review checklist 和 next action。
- Prompt 正文属于 `data/yeisme-prompt-templates`；source/candidate/review/export 状态属于 Scaena；model/provider 执行属于 Dramaturge。
- Skill 不持有 credential，不手写结构化状态，也不把聊天文本视为 accepted canon。

## What Changes

- 保留 Skill 名称、目录和 frontmatter；不 rename、不新增竞争 Skill。
- 在 intake 生成 `director_plan` 的 `DramaRoutePlan`：`medium=short_drama`、一个 primary `ai-drama-director`、最多一个 `ai-drama-continuity-supervisor` constraint、`artifact=candidate`、`acceptance_state=unreviewed`。
- 根据用户输入选择 `vertical-short-drama-v1` first-support 或三个 exploratory profile；若 format/duration/aspect 会改变结构且缺失，先返回 `needs_input`，不让模型猜。
- 通过 Scaena provider-free preflight 检查 owner readiness、PromptRepo ref/digest、direction bounds、source digest 和估计成本，再请求一次明确 run/revise 授权。
- 本地交互优先使用 `run --foreground --events`；远程/MCP 保持 async `run -> status/resource`，不在 tool call 中长时间阻塞。
- 增加 `watch`、`diff`、`show --view findings` 的选择规则；safe summary 优先，只有显式 prompt/dialogue review 才读取 private content。
- `skill:scaena-storyboard-breakdown` version 1 继续作为 compatibility ingress；Skill 将它解析为固定 PromptRepo solution + direction profile，但不复制 Prompt body。
- 在 accept 前显式呈现故事脊柱、逐镜节拍、对白主干、视觉基调和时长合同；未获当前用户确认不得 materialize 或进入任何付费图片/视频生成。
- 更新 validator fixtures，覆盖 ready、owner missing、prompt stale、format missing、foreground timeout、blocking findings、revision drift 和 MCP async route。

## Capabilities

### New Capabilities

- `scaena-storyboard-breakdown-operation-skill`: 现有 Skill 的 PromptRepo/direction 路由、foreground/async 交互、review/approval 和 typed handoff 合同。

### Modified Capabilities

无。本 skills repo 当前没有已发布 OpenSpec capability；Skill name/frontmatter 和既有用户动作保持兼容。

## Non-Goals

- 不把 Prompt 正文、provider payload、source body、candidate JSON 或 full reasoning 写进 Skill 输出。
- 不自动安装/启用 Skill、提高预算、选择 fallback model、重试有歧义 mutation、accept/reject/export 或创建图片。
- 不实现 CLI/MCP/HTTP/worker；这些属于 Scaena 和 Dramaturge。

## Impact

- 修改 `.skills/yeisme/scaena/scaena-storyboard-breakdown/` 的 Skill 与 references，并在需要时更新 `agents/openai.yaml` 的简短默认提示。
- Profile 名称保持不变；发布后通过 root `scripts/skills.sh sync-target agent/scaena` 生成 runtime copies，禁止直接编辑 `.agents/skills` 或 `.claude/skills`。
- 验证必须运行 Scaena skills validator、通用 skill validator、profile/runtime sync checks；不执行真实 provider call。
