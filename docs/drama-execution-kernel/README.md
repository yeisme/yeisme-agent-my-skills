# 做剧执行内核（Drama Execution Kernel, DEK v1）

本目录是做剧 skills 的**抽象设计与执行单元设计**真源，属于独立仓库 `yeisme/yeisme-agent-my-skills` 的一个自包含模块。它不新建生成引擎、不新建 router、不复制任何外部技能包的角色或脚本，只把散落在 Auctra / Scaena / Eikona / Aigora / 控制中心里的既有合同归纳成统一语义，并组装成可组合执行单元。

## 定位

| 项 | 值 |
| --- | --- |
| 版本 | `drama-execution-kernel.v1` |
| 范围 | 短剧 / 漫剧 / AI drama 的「创作判断 → 冻结 → 受控写入 → 权威回读 → 恢复」执行链 |
| 不是 | canonical story、ProductionGraph、visual artifact、provider 执行、跨 owner 网关、第二个做剧 router |
| 唯一语义入口 | `ai-drama-router`（`ai-drama.route-plan.v1`）保持不变 |
| owner 边界 | Auctra 持有 canonical screenplay；Scaena 持有 ProductionGraph / DrawSession / video task / delivery；Eikona 持有 run/artifact/replacement；Aigora 持有视频执行；控制中心只做只读投影与人工门禁 receipt |

## 设计原则

1. **抽象来自现有实现，不来自外部技能包**。所有词汇都能在现有 CLI / 文档 / 代码里找到对应承载点，见 [abstract-design.md](abstract-design.md)。
2. **判断与写入分离**。`DramaRoutePlan` / `creative.owner-handoff.v0.1` 只产出允许动作与 next command，不写 owner state。
3. **跨 owner 只传 `ref + digest`**，不传 bytes、路径、provider payload；沿用 `eikona.asset_handoff.v2` 的 path-free 契约。
4. **一次动作一个 receipt**，统一走 `ai-native-cli-output-contract` envelope；结构化运行资产由 owner CLI 产出，agent 不手写。
5. **UNKNOWN 单调**：`unknown_accept` 之后只允许只读 `reconcile`，不换幂等键、不换模型、不创建替代任务。
6. **人工跃迁不可自动化**：`select --actor <human>` / `freeze --confirm` / `review decide --confirm` 保持原样。

## 文档索引

| 文件 | 内容 |
| --- | --- |
| [abstract-design.md](abstract-design.md) | 六个抽象 + 一条调度律的定义、真实承载点、不变量总图 |
| [execution-units.md](execution-units.md) | EU 通用形状、9 个领域 EU、2 个横切层、编排 DAG、三场景组合 |
| [automation-core.md](automation-core.md) | 自动化做剧核心流程：流程纪律提取、`automation_profile`、六阶段 stage_plan、门禁矩阵、完成分级 |
| [capability-abstraction.md](capability-abstraction.md) | **一个作用**：`GenerationCapability<kind>`（`image\|video\|audio`）与 `GenerationBinding`；三类合同、能力发现矩阵、`retry_budget=2`、`ApprovalWindow` |
| [contracts/owner-action.v1.md](contracts/owner-action.v1.md) | C1 跨 owner 动作收据 |
| [contracts/draw-batch.v1.md](contracts/draw-batch.v1.md) | C2 抽卡批量合同 |
| [contracts/replacement-bound.v1.md](contracts/replacement-bound.v1.md) | C3 有界替换合同 |
| [integration.md](integration.md) | 与 root profile / runtime / 三个 owner 的接入与验证命令 |

## 对应 Skills

| Skill | 承载 |
| --- | --- |
| `ai-drama-bootstrap` | Router 之前的环境准备层：安装 skills / CLI、配置连接、交接 Router；可复制的主提示词在 `ai-drama-skills` 的 `ai-drama-bootstrap/references/bootstrap-prompt.md` |
| `ai-drama-action-receipt` | EU 通用形状、C1、A1/A3/A4 词汇与 UNKNOWN 决策表 |
| `scaena-asset-draw-batch` | EU-02/03/04、C2、B1 |
| `scaena-bounded-replacement` | EU-09、EU-31、C3、A5 判定门 |
| `ai-drama-remote-operations` | L-Transport / L-Projection、G1/G2 |

## 引导提示词与接入方式

`ai-drama-bootstrap`（`yeisme/ai-drama-skills`）提供可复制的引导提示词，让新机器/新会话自动完成「安装 skills + 安装工具 + 配置连接 + 接剧本开做」：

| 版本 | 位置（`ai-drama-skills/ai-drama-bootstrap/references/`） | 特点 |
| --- | --- | --- |
| 完整版 | `bootstrap-prompt.md` | 逐条命令 + 全部门禁，一次跑完 |
| 简短版 | `bootstrap-prompt-short.md` | ~20 行，委托给 Skill |
| 渐进式 | `bootstrap-prompt-progressive.md` | L0 / L0.5 / L1 / L2 / L3 / L4，每层可独立发送、可停 |
| 选择指南 | `prompt-variants.md` | 三版对照 |
| binding 参考 | `surface-choice.md` | CLI / MCP / HTTP / SDK 命令与差异；**已降级为参考，不再是流程门禁** |
| 命令全表 | `install-and-connect.md` | 安装与连接真实命令 |

**审批窗口（替代方式门禁）**：不再询问 `cli|mcp|both`。流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding，理由写入 `receipt.binding_ref`。凡 agent 发起的非只读动作都要审批，但用**一次带边界的 `ApprovalWindow`** 实现：窗口绑定 `capability_kinds[] / intent_digest / binding_allowlist / count / cost_ceiling / retry_budget=2 / stop_before_final_submit`，窗口内全自动（含自动重试、自动换 binding、连续推进六阶段）；越界或重试耗尽 → `needs_decision`。UNKNOWN 只 `reconcile` 且不消耗预算；付费生成与正片提交仍是独立新授权。三类合同与完整规则见 [capability-abstraction.md](capability-abstraction.md)。

## 独立分发

本模块按 `yeisme-skill-publisher` 规范组织，可单独安装单个 skill，不需要激活整套做剧矩阵。四个 skill 分别位于两个独立仓，**安装入口指向 skill 实际所在的仓**，不要指向带嵌套 submodule 的聚合仓：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-action-receipt --yes
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-remote-operations --yes
npx --yes skills add https://github.com/yeisme/scaena-skills \
  --skill scaena-asset-draw-batch --yes
npx --yes skills add https://github.com/yeisme/scaena-skills \
  --skill scaena-bounded-replacement --yes
```

设计正文只在聚合仓 `yeisme/yeisme-agent-my-skills` 的 `docs/drama-execution-kernel/` 维护；两个独立仓各放一份指针文件，**不得同时维护两份不同正文**。发布关系见 [integration.md](integration.md)。

## 明确不做

- 不引入外部技能包的术语、模型白名单、Windows 路径、桌面 CLI 或单主控会话快照。
- 不建跨 owner 凭据/生产网关（root `owner-hosted-remote-profile` 已判 `reject-now`）。
- 不把 `eikona accepted` 写成 `production_ready`（`asset_handoff.v2` 已固定 `handoff_candidate`）。
- 不放宽 `--actor <human>` / `--confirm`；不把控制中心 Preview 当 Owner 写入。
