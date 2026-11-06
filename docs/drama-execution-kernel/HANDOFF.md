# 做剧执行内核 · 总览与交接（DEK v1）

> 本文件是**单一总览入口**：研究结论 → 抽象 → 执行单元 → 自动化流程 → 能力抽象 → Skills → 提示词 → 落地状态 → 后续路线。各专题细节仍以 `docs/drama-execution-kernel/` 下对应文档为唯一真源，本文件不复制正文，只做索引与状态汇总。

## 一句话

把一份剧本或小说交给 Agent 后，从环境安装到生成前准备全程**可自动推进、可审计、可恢复**；三类生成（`image|video|audio`）统一为**一个作用** `GenerationCapability<kind>`，入口差异只在 `GenerationBinding`；一次 `ApprovalWindow` 覆盖窗口内全自动（含有界重试），越界重新审批；**停在正片提交前**。

## 演进与版本

| 阶段 | 产出 | 落点 |
| --- | --- | --- |
| 1 研究 | 外部「糯米中枢技能包」只提取**流程编排纪律**，不搬角色/脚本/平台 CLI | 本文件 + `automation-core.md` 第一节 |
| 2 抽象 | 六个抽象 + 一条调度律，全部用现有工具真实合同表达 | `abstract-design.md` |
| 3 执行单元 | 9 个领域 EU + 2 个横切层 + DAG | `execution-units.md` |
| 4 合同 | C1 动作收据 / C2 抽卡批量 / C3 有界替换 | `contracts/` |
| 5 自动化 | `automation_profile` 六阶段、完成分级、门禁矩阵 | `automation-core.md` |
| 6 引导 | `ai-drama-bootstrap` + 三版提示词 + 安装连接命令全表 | `ai-drama-skills` |
| 7 能力抽象 | **一个作用三类 kind**：`GenerationCapability<kind>` + `GenerationBinding`、能力发现矩阵、`retry_budget=2`、`ApprovalWindow` | `capability-abstraction.md` |
| 8 落地 | Skills 对齐、索引整合、后续实现路线 | 本文件 + `implementation-roadmap.md` |

策略变更记录：**`SURFACE=cli|mcp|both` 已从流程门禁降级为 binding 参考**（`surface-choice.md`）；入口差异不再需要用户选择，由 resolver 自动选 `executable` binding。

## 唯一真源表

| 文档 | 内容 | 仓库 |
| --- | --- | --- |
| `README.md` | DEK 模块索引、对应 Skills、提示词版本 | 聚合仓 |
| `HANDOFF.md`（本文件） | **总览、版本、状态、后续路线** | 聚合仓 |
| `abstract-design.md` | A1–A6 + B1 定义、真实承载、不变量总图、能力/绑定分离 | 聚合仓 |
| `execution-units.md` | EU 通用形状、9 EU + 2 横切、DAG、三场景组合 | 聚合仓 |
| `automation-core.md` | 流程纪律映射、`automation_profile`、六阶段、门禁、完成分级 | 聚合仓 |
| `capability-abstraction.md` | **4 对象、等价准则、三类合同、能力发现矩阵、有界重试、审批窗口** | 聚合仓 |
| `contracts/owner-action.v1.md` | C1 动作收据（含 5 个能力字段） | 聚合仓 |
| `contracts/draw-batch.v1.md` | C2 抽卡批量与 identity-equal 快路径 | 聚合仓 |
| `contracts/replacement-bound.v1.md` | C3 有界替换与失败受控修复 | 聚合仓 |
| `integration.md` | 三仓关系、profile 分配、验证命令、落地顺序 | 聚合仓 |
| `implementation-roadmap.md` | **C1/C2/C3 后续实现规格与交接** | 聚合仓 |
| `ai-drama/docs/drama-execution-kernel/README.md` | 独立仓指针（不复制正文） | `ai-drama-skills` |
| `scaena/docs/drama-execution-kernel/README.md` | 独立仓指针（不复制正文） | `scaena-skills` |
| `ai-drama-bootstrap/references/*` | 三版提示词、选择指南、binding 参考、命令全表 | `ai-drama-skills` |
| `ai-drama-action-receipt/references/capability-invocation.md` | 能力调用合同速查 | `ai-drama-skills` |

## 三个独立仓库

| 仓库 | 挂载 | 承担 |
| --- | --- | --- |
| `yeisme/yeisme-agent-my-skills` | 主仓 `.skills/yeisme` submodule（`develop`） | 聚合源层、**全部设计真源**、`eikona-image/` |
| `yeisme/ai-drama-skills` | 内层 submodule | 做剧路由、`ai-drama-bootstrap`、动作收据、远程操作 |
| `yeisme/scaena-skills` | 内层 submodule | 抽卡批量、有界替换、生产操作 |

`yeisme/ai-drama-skills` 另有做剧 skills 的便携云安装入口；两者**不得维护同一 skill 的不同正文**。主仓 `.skills/profiles/**` 由 `scripts/skills.sh` 管理，runtime 副本由脚本生成，不手写。

## 抽象一览

| 层 | 抽象 | 状态 |
| --- | --- | --- |
| 引用 | A1 `FrozenRef`（`ref + digest`） | 已有实现 |
| 动作 | A2 `CapabilityInvocation`（原 `OwnerAction`，细化为一次能力调用） | 已有实现 + 本轮细化 |
| 结果 | A3 `Outcome`（ACCEPTED/COMPLETED/BOUND/REVIEWED/UNKNOWN/PARTIAL） | 已有实现 |
| 授权 | A4 `IdempotentGrant` + `ApprovalWindow` | 窗口为本轮新增 |
| 复用 | A5 `LineageReuse` + `identity_equal` 快路径 | 已有实现 |
| 人工 | A6 `HumanGate`（`select --actor human` / `freeze --confirm`） | 已有实现，不可放松 |
| 调度 | B1 `WaveBatch`（一次确认、依赖波次、统一回查、写入预算） | 已有实现 |
| **能力** | `GenerationCapability<kind>` + `GenerationBinding` + `GenerationReceipt` | 本轮新增设计 |

**四类能力合同都写全**：`image`（Eikona）、`video`（Scaena/Aigora）、`audio`（Sonora）各自的 operations / typed controls / 真实入口 / 约束源 / receipt 锚 / 特有门禁，见 `capability-abstraction.md` 第二节。

## 五个 DEK Skills（不建第二套 owner）

| Skill | 仓 | 职责 | 本轮对齐 |
| --- | --- | --- | --- |
| `ai-drama-bootstrap` | ai-drama | Router 之前的环境准备、三版提示词 | ✅ 审批窗口 / 自动重试 / 三类能力 |
| `ai-drama-action-receipt` | ai-drama | 合同层 + **能力调用收据 owner** | ✅ 新增 `capability-invocation.md`、GenerationReceipt、窗口与重试 |
| `ai-drama-remote-operations` | ai-drama | binding 发现、连接准备、控制中心投影对齐 | ✅ 不再分 CLI/MCP 流程 |
| `scaena-asset-draw-batch` | scaena | 批量抽卡、wave、统一回查、快覆盖 | ✅ `GenerationCapability<image>` / 窗口 / 重试 |
| `scaena-bounded-replacement` | scaena | 三类资产替换、identity_equal、失败修复 | ✅ 扩到 image/video/audio / 窗口 / 重试 |

`ai-drama-router` 仍是**唯一语义入口**（`ai-drama.route-plan.v1`）；`ai-drama-production-orchestrator` 负责完整链路编排；`scaena-subject-asset-readiness` 独占单槽位门禁；`eikona-asset-lifecycle` 独占 Eikona 资产生命周期。

## 三份合同状态

| 合同 | 内容 | 状态 | 交接路径 |
| --- | --- | --- | --- |
| C1 `yeisme.owner_action.v1` | 跨 owner 动作收据 + 5 个能力字段 | **设计完成，已交接，待 owner 实施** | `agent/scaena/openspec/changes/scaena-dek-typed-action-v1/`、`cli/eikona/openspec/changes/eikona-dek-action-receipt-v1/` |
| C2 `scaena.draw_batch.v1` | 抽卡批量 + identity-equal 快覆盖 | **设计完成，已交接，待 owner 实施** | `agent/scaena/openspec/changes/scaena-dek-draw-batch-v1/` |
| C3 `yeisme.replacement_bound.v1` | 有界替换 + 失败受控修复 | **设计完成，已交接，待 owner 实施** | `cli/eikona/openspec/changes/eikona-dek-action-receipt-v1/`、`agent/scaena/openspec/changes/scaena-dek-bounded-replacement-v1/` |

实现规格、依赖顺序与验收命令见 [implementation-roadmap.md](implementation-roadmap.md)。

## OpenSpec 交接（根级，2026-11-06）

根 `openspec/changes/drama-execution-kernel-handoff-v1/` 已建立并通过 `openspec validate <change-id>`：

- `proposal.md`：为什么做、做什么、不做什么、影响哪些子项目，含五个 owner change 路径；
- `design.md`：Mermaid 分层图与 D1–D5 依赖图、**capability ledger**（七项 `fit` / 四项 `split-owner` / 一项 `reject-now`）、跨 owner 不变式、风险取舍；
- `tasks.md`：只记设计评审、文档同步、跨项目 handoff 与治理验证；实现任务全部转入 owner change；
- `specs/cross-project-drama-execution-handoff/spec.md`：5 条 Requirement + 7 个 Scenario，约束唯一真源、能力不删减、根不承载实现、合同状态不冒充实现、治理验证与真实验收分离。

**根 change 不改任何代码 owner 的工作树**；D1–D4 的 `proposal.md` / `design.md` / `tasks.md` / `specs/**/spec.md` 及实现、测试、closeout 由各 owner 在自己的 OpenSpec 中承接。

## 三版引导提示词

| 版本 | 位置（`ai-drama-skills/ai-drama-bootstrap/references/`） | 特点 |
| --- | --- | --- |
| 完整版 | `bootstrap-prompt.md` | 逐条命令 + 全部门禁 |
| 简短版 | `bootstrap-prompt-short.md` | ~20 行，委托给 Skill |
| 渐进式 | `bootstrap-prompt-progressive.md` | L0 发现 / L0.5 审批 / L1 skills / L2 工具 / L3 连接 / L4 交接，每层可停 |
| 选择指南 | `prompt-variants.md` | 三版对照 |

三版共有：不询问 `cli|mcp|both`、一次 `ApprovalWindow`、`retry_budget=2`、UNKNOWN 只 `reconcile`、凭据只给 0600 路径、停在正片提交前、换 binding 不增加权限。

## 已知缺口（如实报告，不绕过）

- `scaena remote` v1 slice 只路由 `remote/upload/mcp/doctor/board`；生产写返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND` → 属 C1 typed action 路由缺口；
- `eikona mcp --transport http` 只投影监听地址，不是 TLS / production-ready 证据；Scaena Streamable HTTP 为 `blocked`；
- 远程参考输入必须是 `eikona://` URI，客户端绝对路径拒绝 `invalid_reference`；
- MCP `tools/list` 中 `planned/readonly/unavailable` 不进 executable descriptors；worker 已 claim 且失败必须投影 `failed`，不得继续 `queued`。

## 验证入口

```bash
# 主仓
scripts/skills.sh validate-custom
scripts/skills.sh validate-runtime
scripts/skills.sh resolve ai-drama-bootstrap

# 聚合仓
python3 scripts/validate_repository.py

# ai-drama-skills
python3 scripts/validate_skills.py
python3 ai-drama-router/scripts/validate_drama_matrix.py

# scaena-skills
python3 scripts/validate_skills.py
```

按两个子仓 `AGENTS.md` 执行本地结构检查；**不执行 race、不自动安装外部 Skills、不生产访问、不发布、不推送**。

## 明确不做

- 不新建第二个做剧 router、不建跨 owner 网关、不把 `cli/mcp` 或产品名做成流程分支；
- 不自动付费、不自动发布、不自动派生子代理、不跑 race；
- 不把凭据值写进日志 / stdout / 仓库 / evidence；不把 `ACCEPTED` 写成完成；
- 不把客户端路径当远端可读文件、不把 `planned/readonly` 升级为可写；
- 不在 UNKNOWN 写 / 已受理 / 业务拒绝 / 创意输入变化时重试；
- 不在独立仓复制设计正文，不手写 runtime 副本或结构化资产。

## 后续路线与完成状态

| 阶段 | 状态 |
| --- | --- |
| D0 根交接 | ✅ 已完成（`openspec/changes/drama-execution-kernel-handoff-v1/`） |
| D1 C1 typed action | ✅ **已实现owner 侧切片**（`agent/scaena` `scaena-dek-typed-action-v1`）：公开契约、canonical 路由、handler、typed SDK、`scaena dek invoke\|reconcile`、routed 分类、单元测试；EU 执行面仍 `needs_contract`，`cli/eikona` 侧对齐待做 |
| D2 C2 抽卡批 | ⏳ 已交接，待 `agent/scaena` 实施 |
| D3 C3 有界替换 | ⏳ 已交接，待 `cli/eikona` + `agent/scaena` 实施 |
| D4 控制中心投影 | ⏳ 已交接，待 `client/yeisme-control-center` 实施 |
| D5 Skills/profile 收口 | ✅ Skills 源层已完成（5 个 Skills 对齐、三版提示词、索引整合、三仓校验全绿） |

见 [implementation-roadmap.md](implementation-roadmap.md)。owner 侧实现分别归 `agent/scaena`、`cli/eikona`、`client/yeisme-control-center` 的 OpenSpec，**主仓只留合同与交接**；不在根 `openspec/` 写实现任务，不在本轮修改代码 owner 的工作树。
