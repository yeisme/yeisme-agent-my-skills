---
name: dsh-plugin-grill-me
description: Use when the user explicitly wants a direct dependency-aware interview to stress-test a DeepSeek Harness (DSH) plugin, tab, pane, overlay, header action, preset, storage domain, projection, or upstream seam design in agent/harness-plugins before any OpenSpec change, scaffolding, or implementation.
---

# DSH 插件 Grill Me

直接进入 DSH 插件开发决策 frontier，不再询问平台或通用性。与 `grill-me` 成对激活：决策树、frontier、轮次、提问格式与完成条件全部沿用 `grill-me` 协议；本 Skill 只替换领域问题集、事实来源和绊线。运行前加载 `grill-me` 与 [references/dsh-plugin-frontiers.md](references/dsh-plugin-frontiers.md)。

## 启动

1. 固定 `domain=dsh-plugin`。被质询对象可以是新插件想法、既有 change 的 proposal/design、一次 seam 决策、一次重构或一次验收前的设计复核。
2. 仓库事实由当前 Agent 内联收集，不创建子 Agent：本仓 `AGENTS.md` 边界、`docs/plugin-tab-development.md`、`docs/plugin-host-protocol.md`、`docs/design/dsh-unified-panel-visual-system.md`、相关 `openspec/changes/` 现状与 `packages/` 既有实现。事实不足时先读文件再提问，不把仓库可查事实抛给用户。
3. 按变更量选择深度：单一窄问题用 `quick`；既有 surface 上的新能力用 `standard`；新 surface/archetype、新增存储域、upstream seam、合同或 schema 变更默认 `deep`。
4. 按 [references/dsh-plugin-frontiers.md](references/dsh-plugin-frontiers.md) 的阶段进入条件重建决策树：上游阶段未定时不预问下游阶段。
5. 逐轮提出当前 frontier 中彼此不依赖的问题，每题给可反驳的推荐答案；等整轮回答后重算 frontier 再进入下一轮。
6. 任何答案触碰 `AGENTS.md` 禁止项（core fork、第二 scheduler/task ledger、浏览器侧 domain store、raw prompt 或凭据过界、把官方合入当验收）时立即指出并给合规替代，不沿该分支继续扩张。

## DSH 插件范围

- 表面选择：conversation.view tab、pane、overlay 兜底、header action、preset、纯 host CLI 面。
- Owner 边界：Ordo 唯一账本与 DSH core 所有权内的事实归 owner；本仓插件只做安全只读投影、命令入口与组合摘要。
- 数据与投影：作用域、safe projection 过界字段面、存储域、纯回放 fold 与有界窗口的诚实标注。
- Seam 与宿主：已发布 surface vs `upstream-prs/` 通道、capability probe、unknown/cancel_unknown 的禁改策略。
- 形态与组合：shape A/B、cordis.patch 语法、preset-root 注册、vendoring 规则。
- 界面契约：ui-surface/ui-visual-kit token、双语、焦点返回、可读禁用原因。
- 生命周期：mount/dispose 对称、HMR、profile 切换、会话切换、死 tab 防护。
- 交付与验证：OpenSpec 变更必要性、门禁命令、集成证据与完成定义（仓内协议对接，不依赖官方 seam）。

问题只覆盖当前被质询 artifact；规格未冻结时不追问实现细节。

## 事实与决策分工

- 事实由 Agent 查：AGENTS.md、docs、openspec change、packages 代码、门禁与 CI 现状。
- 决策由用户做：目标用户、场景优先级、范围取舍、体验取向、风险承受、停止条件。
- “不知道、需要真机感受”转有界 proof：用 `docs/cookbook/dsh-plugin-hot-development.md` 的热开发工作流做可丢弃 prototype，拿证据回来继续访谈。
- 默认不写文件、不修改代码、不创建 OpenSpec change、不进入实现。

## 收束

frontier 为空或剩余问题已明确转为调研、prototype 或延期项后，输出决策摘要并等待用户确认：

- 结论：被质询对象的一句话定性与去留判断。
- 关键选择：surface、owner 边界、数据/投影、seam、形态、视觉、生命周期、验证门。
- 非目标、风险、验证缺口、建议下一步。

用户确认后按需 handoff（每项均需单独授权）：起草 OpenSpec change、进入 `dsh-tab-plugin-development` 实施、或先做 prototype。确认摘要不等于创建 change、生成代码或运行构建。
