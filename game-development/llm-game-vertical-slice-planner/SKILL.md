---
name: llm-game-vertical-slice-planner
description: Use when turning an LLM-native game concept into a two-to-six-week playable prototype or vertical slice with a bounded player loop, content scope, implementation lanes, model budget, playtest protocol, telemetry, acceptance criteria, failure rechecks, promotion signals, and explicit kill criteria.
---

# LLM 游戏垂直切片规划师

## 目标

用最小可玩闭环验证玩家是否愿意主动使用 LLM 玩法，而不是只验证模型能否生成内容。

## 输入

- 已选方向、玩家幻想、核心循环和主要风险。
- 团队、周期、技术栈、已有资产和可用模型。
- 目标玩家、测试渠道、预算和内容安全边界。

## 输出

- 10–30 分钟可玩闭环与试玩脚本。
- 明确的内容预算、状态预算、调用预算和非目标。
- 按依赖排序的实施任务与验证命令。
- 试玩招募、观察、访谈、遥测和证据包计划。
- 晋级、返工和停止标准。

## 切片约束

默认只保留：

- 1 个地点或封闭场景。
- 3–8 个重要 NPC。
- 1 个核心谜题、冲突或关系目标。
- 1 套权威状态与事件账本。
- 1 条模型降级路径。
- 1 次完整开始、发展、结果和复盘。

删除开放世界、程序化地图、大规模战斗、多人同步、完整经济、UGC 平台、长期赛季和无限内容承诺，除非它们正是待验证的唯一核心假设。

## 工作流

1. 写出单句假设：`如果玩家能够 X，系统通过 Y 产生 Z 后果，玩家会因为 W 再玩一次。`
2. 选择一个最危险假设，只允许切片围绕它展开。
3. 定义核心循环：观察 → 决策/输入 → NPC 或世界响应 → 可见状态变化 → 新问题。
4. 标记每一步由规则、人工内容、LLM 或组合负责。
5. 设定内容预算：角色、场景、线索、结局、对白种子和人工审校数量。
6. 设定模型预算：每分钟调用、每局 token、P50/P95 延迟、失败率和最坏单局成本。
7. 建立三层测试：确定性单元测试、模型契约/回放测试、真人试玩。
8. 设计证据：屏幕录制、事件日志、状态差异、调用成本、失败样本、访谈笔记和复玩选择。
9. 先跑内部 dogfood，再跑 5–10 名目标玩家；不以朋友的礼貌评价替代行为证据。
10. 根据 gate 决定晋级、缩小、换方向或停止。

## 最低成功指标

按产品调整，但至少覆盖：

- `time_to_first_meaningful_choice`：玩家多久做出第一次真正改变状态的选择。
- `consequence_recognition`：玩家是否能说出自己的行为造成了什么后果。
- `goal_comprehension`：玩家是否知道当前目标、风险和可用行动。
- `recovery_rate`：模型失败后能否继续完成流程。
- `session_completion`：是否完成完整闭环。
- `voluntary_replay`：是否主动重玩或尝试另一策略。
- `llm_value`：玩家认为最有价值的变化是否确由 LLM 能力产生。
- `cost_per_completed_session`：每次完整体验的模型与运营成本。

## 默认停止条件

- 玩家主要称赞“AI 很神奇”，但无法描述游戏目标或后果。
- 自由输入大多被忽略、误解，或最终落回固定选项。
- 关键体验依赖主持人手工救场。
- P95 延迟持续破坏节奏，且异步或降级设计无法解决。
- 单局成本超过可接受商业模型，且缩小调用不能保留体验。
- 安全审校量随内容近似线性增长，团队无法承担。
- 移除 LLM 后体验几乎不变。

## 交接

- 方向仍不清晰时返回 `llm-game-direction-strategist`。
- 状态、记忆、调用或安全边界不清晰时交给 `llm-game-systems-architect`。
- 被接受为长期交付、改变稳定契约或需要多人并行实施时，在 owning subproject 创建 OpenSpec change 后再硬化。

## 验证

- 每项任务有 owner、依赖、产物、验证方式、预期结果和失败复查。
- 试玩指标同时覆盖乐趣、可理解性、LLM 价值、可靠性与成本。
- 计划有明确非目标和停止条件，不用“继续优化提示词”无限延长实验。
- 切片结束时能做出方向决策，而不仅是展示 demo。
