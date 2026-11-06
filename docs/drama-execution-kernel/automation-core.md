# 自动化做剧核心流程（DEK v1 扩展）

> 本文把外部「糯米工作流程」里**可迁移的流程编排纪律**（不是角色、脚本或平台 CLI）提取出来，与 `ai-drama-router` 的 `DramaRoutePlan v1` 和 DEK 执行单元结合，形成自动化做剧核心流程。真源在本聚合仓；两个独立仓只放指针。

## 一、提取出的十条流程核心纪律

| # | 糯米包原文要点 | 现有工具承载 | 落地方式 |
| --- | --- | --- | --- |
| 1 | 单一正式入口；询问/规划/审计/单字段修改不扩为生产任务 | `ai-drama-router` 唯一入口 | Router 保持唯一；bootstrap 只做环境准备，完成后立即交接 |
| 2 | 一次理解、按阶段交接：列出必需阶段、冻结产物、责任技能、完成依据、停止边界；不增加第二套项目状态文件 | `DramaRoutePlan.stage_plans[]` / `gates[]` / `canonical_owner` | 新增 `automation_profile`，用有序 stage plan 表达，不新建状态文件 |
| 3 | 清单不等于已读；逐页读正文，hash 变化刷新 | `ai-drama-context-pack-builder` 最小版本化 ContextPack；`FrozenRef` digest | ContextPack 必须实际消费 `input_refs[]`，digest 变化标 `stale` |
| 4 | 每集六阶段：原文与跨集接续 → 资产/音源缺口 → 导演结构化组件与提示词组装 → raw-first 语义与导演验收 → 写前预检/写入/回读 → 逐集与全范围完成核对 | Router 阶段矩阵 + DEK EU-01..EU-08 | 六阶段 stage_plan 模板（下表） |
| 5 | 判断与执行分离；执行器只执行冻结计划 | `OwnerAction` / `IdempotentGrant` / EU 写入口 | 创作判断在 skill，写入只在 owner CLI 受控入口 |
| 6 | 完成分级：文件已创建 ≠ 写入成功 ≠ 阶段完成 ≠ 生成前全部完成 | `Outcome` 代数（ACCEPTED/COMPLETED/BOUND/REVIEWED/…） | 报告按级分开，禁止互相冒充 |
| 7 | 准备任务停在正片提交前；素材制作依自身授权 | `generation` gate、`--confirm` 费用确认 | `stop_before_final_submit: true`；付费生成需独立显式授权 |
| 8 | 正常已授权步骤连续推进；询问进度不暂停；未知先核对不重发 | `UNKNOWN` / `reconcile` 只读恢复 | `continuous_advance: true`；进度询问不重置授权，不重提 |
| 9 | 默认不看图，优先文字档案；只在影响剧情正确性时定向看 | `eikona.asset_handoff.v2` 的 refs/文字档案 | `visual_review_default: text_first` |
| 10 | 单主控；子代理默认关闭，只有用户明确要求才启用 | root `codex-subagent-feature-delivery` 限制 | `subagents: disabled_unless_explicit` |

**不迁移**：九份文件清单的逐页 `--read` 问答、`noemi-cli.exe` 5 分钟超时、Windows 绝对路径、`start_preparation.cjs`、项目专用一次性授权脚本、blind eval、模型白名单、单主控 Codex 会话快照。

## 二、`DramaRoutePlan` 新增 `automation_profile`

`ai-drama.route-plan.v1` 增加一个可选字段，不改变现有字段语义：

```text
automation_profile?:
  mode: continuous | gated                  # 默认 continuous（已授权阶段连续推进）
  stop_before_final_submit: boolean         # 默认 true
  continuous_advance: boolean               # 默认 true；进度询问不暂停、不重置授权
  visual_review_default: text_first         # 默认不看图
  subagents: disabled_unless_explicit      # 默认关闭
  unknown_policy: reconcile_readonly       # UNKNOWN 不重投、不换幂等键
  retry_budget: 2                          # 可重试错误自动重试上限；UNKNOWN 不消耗
  approval_window_ref: <FrozenRef>          # 一次审批 = 一个自动化窗口
  binding_policy: auto_executable           # resolver 自动选 executable binding，不问 cli/mcp
  completion_evidence:
    per_stage: stage_receipt               # 逐阶段 receipt
    per_episode: verify_preparation_complete
    full_scope: verify_full_request_scope
  gates_ref: <FrozenRef>
```

Router 的解析顺序不变：先 `OriginalityDecision` → 十五轴 → `context_pack_profile` → 一个 primary + 最多一个 constraint → `owner_action` / `next_action`。`automation_profile` 只控制**执行推进方式**，不改变路由选择，也不新增 canonical owner。

## 三、六阶段 stage_plan 模板

| # | `stage_kind` | Primary Skill | 可选 constraint | Canonical owner | 输入 `FrozenRef` | 阶段 receipt | 停止条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `source_admission` | `ai-drama-router` + `ai-drama-context-pack-builder` | `ai-drama-producer` | Auctra（`story_canon_owner`） | 剧本/小说文件、`canon_digest`、`OriginalityDecision` | ContextPack + `source_revision` | 原文未读完、hash 漂移、原创性 blocker |
| 2 | `asset_gap` | `scaena-subject-asset-readiness`（单槽位）/ `scaena-asset-draw-batch`（批量）+ `GenerationCapability<image>` | `ai-drama-visual-language` | Scaena / Eikona | `GenerationIntent` + `ApprovalWindow`、frozen slots | `batch_ref` / `frozen_subject_version_ref` / `GenerationReceipt` | wave 上游未 frozen、无审批窗口、binding 非 executable、重试耗尽 |
| 3 | `director_compose` | `ai-drama-director` | `ai-drama-visual-language` | Auctra planning proposal | ContextPack、frozen assets | `ShotDesign` / `ShotAudioIntent` / 正式提示词组件 | 对白/mention/时长未冻结 |
| 4 | `semantic_acceptance` | `ai-drama-continuity-supervisor` / `ai-drama-assessment` | `ai-drama-producer` | story_canon_owner | 阶段 3 正文 + 原文 | raw-first 复核结论、导演验收证据 | 语义异议未解决、rights/cost blocker |
| 5 | `controlled_write` | `GenerationCapability<video\|audio>` + DEK `ai-drama-action-receipt` + `scaena-production-operator` | `ai-drama-remote-operations` | Scaena / Eikona / Sonora / Aigora（各自 EU） | 冻结 execution / bundle / `ShotAudioIntent` | `GenerationReceipt`（`action_id` + `readback_ref` + `event_cursor` + `binding_ref` + `retry_used`） | UNKNOWN、写前状态不符、无 idempotency key、越审批窗口、重试耗尽 |
| 6 | `scope_completion` | `ai-drama-production-orchestrator` | `ai-drama-producer` | Scaena delivery | 逐集 receipt 汇总 | 逐集证据 + 全请求范围核对 | 任一集未收口；**停在正片提交前** |

规则：

- 每阶段只有上阶段产物 `ref + digest` 与结论齐全才进入下阶段；不得用临时脚本另起提示词 / 复核 / 执行路线。
- 已完成阶段不重做；`source_digest` 未变且无新冲突时复用已审结果，只失效受影响分支。
- 跨阶段不等于同时加载全部 Skills；不把能力参考包变成额外 primary。
- 每阶段的判断与写入分离；生成、选图、绑定、备案各自保留真实结果。

## 四、门禁矩阵

| 门禁 | 触发 | 行为 |
| --- | --- | --- |
| `originality_gate` | 参考作品 / 改编 / 风格指向 | refs-only `OriginalityDecision`；blocker 停 ProductionGraph |
| `cost_gate` | 任何付费生成（image / video / audio） | 一次 `ApprovalWindow` 授权 + 按动作独立凭证；准备任务默认不触发 |
| `approval_gate` | 凡 agent 发起的非只读动作 | 必须有 `ApprovalWindow` 且 `intent_digest` / `capability_kinds[]` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget` 全部匹配；漂移重新审批 |
| `retry_gate` | 可重试错误 | `retry_budget=2` 内自动重试，同 `action_id` + 同 `idempotency_key` + 同 `intent_digest`；禁止重试 UNKNOWN 写 / 已受理 / 业务拒绝 / 创意变化；耗尽交 `needs_decision` |
| `binding_gate` | 选择执行入口 | resolver 只选 `executable` binding；`planned/readonly/unavailable` fail-closed；选择理由写 `receipt.binding_ref`；不问 `cli/mcp` |
| `human_gate` | `select` / `freeze` / `review decide` | `--actor <human>` / `--confirm`；自动跃迁不可达 |
| `submission_gate` | 正片视频提交 | `stop_before_final_submit: true`；独立授权 |
| `unknown_gate` | 超时 / 断线 / `unknown_accept` | 只读 `reconcile` 原 `action_id`，不重投 |
| `rights_gate` | 素材 / 参考视频 | `permission licensed`；不把未审素材标 `owned` |
| `continuity_gate` | 跨集接续 | 前集未冻结时后集只能是草案 |

## 五、与 DEK 执行单元的衔接

| 阶段 | 对应 EU |
| --- | --- |
| 1 | EU-01 `CanonIntake` |
| 2 | EU-02/03/04/05 `DrawBatch` → `GenerationInvoke<image>` → `CandidateRecord` → `HumanSelectFreeze` |
| 3 | EU-06 `ShotBind`（frozen intent/spec/bundle） |
| 4 | `Outcome.REVIEWED` 证据，不产生新写入 |
| 5 | EU-07/08 `VideoSubmit` → `Reconcile`（准备任务停在此前）、EU-09 替换、EU-31 修复 |
| 6 | `scaena workflow status` / `quality check` / `continuity check` / `release readiness` |

## 六、完成分级与报告口径

```text
ACCEPTED            已返回稳定 action_id / submission_ref / run_id
COMPLETED           有权威 readback_ref 且回读一致
BOUND               replacement_status: applied + binding_digest 一致
REVIEWED            复核 / 验收证据已记录
STAGE_COMPLETE      该阶段全部产物 ref+digest 与结论齐全
EPISODE_PREPARED    逐集 verify 证据齐全
FULL_SCOPE_PREPARED 全请求范围核对通过
```

`FULL_SCOPE_PREPARED` **不等于**正片已提交、成片完成或审美验收。报告只给紧凑 receipt + 精确 next command + 预期副作用 + 停止条件；新会话从 refs 恢复，不重读全仓库或 provider 输出。

## 六之二、全自动化与审批窗口

**一个作用**：`GenerationCapability<kind>`（`image|video|audio`）；CLI / MCP / HTTP / SDK / Sonora / 第三方只是 `GenerationBinding`。流程不感知入口，`SURFACE=cli|mcp|both` 不再是门禁。

```text
DISCOVERED → APPROVED → INVOKING → (RETRY×≤2) → ACCEPTED → COMPLETED
                                    └→ TERMINAL_REJECTED / UNKNOWN / NEEDS_DECISION
```

- 用户在任务开始给**一次审批**生成 `ApprovalWindow`（`capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget=2` / `stop_before_final_submit`）；窗口内全自动：自动发现 binding、自动选 `executable`、自动重试、连续推进六阶段。
- 免审批只读：`probe` / `discover` / `tools/list` / `resources/read` / `status` / `reconcile`。必须审批：三类付费生成、绑定 / 替换 / 回滚、`select` / `freeze`、导出 / 发布、凭据 / 连接变更、正片提交、新增 kind 或超预算。
- 可重试：瞬时网络 / 5xx / 429 / 超时且 `mutationAttempted=false`、`binding=unavailable` 换另一个 executable binding。禁止重试：UNKNOWN 写、`ACCEPTED`/付费已受理、业务/权限/语义拒绝、创意输入变化、模型/正文/时长/渠道变化。
- 每次重试保持同一 `action_id` + `idempotency_key` + `intent_digest` + 审批窗口；换 binding 记理由；不新建 state、不改预算。`reconcile` 只读，不消耗预算。
- 越界（新 kind / 超预算 / 漂移 / 新增动作 / 正片提交）或重试耗尽 → `needs_decision` 交回人，保留全部尝试证据；「继续」/ 进度询问不重置也不扩大授权。

三类合同、能力发现矩阵、等价准则与完整规则见 [capability-abstraction.md](capability-abstraction.md)。

## 七、明确不做

- 不把 `cli` / `mcp` / 具体产品名做成流程分支或必答问题；入口差异只在 `GenerationBinding` 层，由 resolver 自动选择。

- 不新建第二个做剧 router；`ai-drama-bootstrap` 只是 Router 之前的环境准备层，完成后立即交接。
- 不把「文件已创建 / 命令退出 0 / 检查表生成」写成任务完成。
- 不因进度询问、上下文恢复或技能升级重做已审阶段。
- 不自动派生子代理、不自动跑 race 检测、不自动付费、不自动发布。
- 不把凭据、provider payload、raw prompt、全链路推理写进 stdout / logs / evidence。
- 不解析人类可读输出；一律用 `--json` / `--agent` / `--events`。
