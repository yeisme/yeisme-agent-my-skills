---
name: xhs-orchestrator
description: Use when planning, briefing, drafting, optimizing, or reviewing Xiaohongshu (XHS) notes and series across选题, title, viral structure, hotspot rewrite, source-post factory, and personal brand — dispatching the narrowest xhs skill without drafting inside the orchestrator.
---

# 小红书内容总编排

运行小红书笔记与系列内容工作流。它负责分派最小合适技能、控制阶段/状态和交付顺序，覆盖选题 → brief → 正文 → 标题/钩子 → 爆款结构 → 审阅，不把所有创作决策都塞进一个提示词。

## 输入

- 小红书任务目标、已有素材、Auctra 项目状态、目标读者、账号定位、发布节奏和交付格式。
- 用户需要的阶段：选题、brief、单篇正文、标题/首句/钩子优化、爆款结构、热点改写、长文/PDF/素材拆系列、个人品牌内容、review、导出或校验。
- 平台约束：字数、图卡页数、话题标签、首图规范、风险词。

## 输出

- 端到端工作计划和当前阶段交付物。
- 任务形态判断、应加载的子技能、需要读取的参考、Auctra 命令建议和 handoff。
- 完成报告：产物、验证、阻塞、待确认和下一步。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../xhs-orchestrator/references/xhs-lifecycle-handoff.md`：任务跨越选题、brief、正文、标题优化、review、Auctra handoff 或多个 xhs worker 时读取，用于统一阶段、handoff 字段和质量门禁。
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要选题、标题公式、正文结构、图卡页序、话题标签或爆款套路模板时读取。
- `../xhs-note-writer/references/xhs-title-card-and-risk-checklist.md`：需要标题卡字段、图卡脚本、风险词检查或导出前门禁时读取。

## 工作流

1. 判断任务类型和生命周期阶段：discovery、topic、brief、draft、optimize、review 或 handoff；多阶段任务先读取 `xhs-lifecycle-handoff.md`。
2. 按最小范围分派子技能，不在总编排内直接起草最终笔记：
   - 单篇笔记正文（选题落点、首段、正文结构、结尾 CTA）→ `xhs-note-writer`
   - 标题/首句/钩子/CTR 优化、A/B 候选标题、点击率复盘 → `xhs-title-optimizer`
   - 爆款结构、高互动模板、情绪节奏、留人模型 → `xhs-viral-structure-writer`
   - 热点/趋势/蹭热点改写、时效选题、平台热搜承接 → `xhs-hotspot-rewriter`
   - 长文/PDF/素材拆成系列笔记、图卡脚本、连载拆条 → `xhs-source-post-factory`
   - 创始人/个人品牌/职业成长/专家人设内容 → `xhs-personal-brand-writer`
   - 多阶段项目、跨平台联动或同时涉及多个 xhs 工作的复合任务 → 留在总编排或交给 `creative-writing-orchestrator`
3. 为下游 worker 输出标准 handoff：`lifecycle_stage`、`target_skill`、`task_brief`、`source_material`、`reader_promise`、`structure_type`、`constraints`、`risk_flags` 和 `next_action`。
4. 需要持久化时使用 Auctra 命令，候选稿先进入 review。
5. 控制阶段顺序：先 brief/落点，再正文，再标题/钩子，再做爆款结构或热点改写，最后审阅；不要在选题未定时就硬写标题。
6. 完成前校验字数、图卡页数、风险词、话题标签、证据真实性、Auctra handoff 和禁写规则。

## 质量门槛

- 总编排只分派和阶段控制，不直接产出最终笔记正文、标题候选或图卡稿。
- 不把选题、标题、正文、爆款结构和热点改写混用同一套结构或塞进一个 prompt。
- 默认服务小红书中文内容，不自动转成英文或跨平台稿。
- 输出必须可交给具体 worker 继续执行，handoff 含阶段、产物、阻塞和下一步。
- 多阶段任务必须标明当前生命周期阶段，不能让下游 worker 猜测是选题、起草还是优化。
- 除非已运行 Auctra 命令或得到人工审稿，不声称 Auctra 审稿已完成。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- Auctra 项目内结构化变更必须走 Auctra 命令，不手写 `.auctra/**` 状态。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 确认分派匹配任务形态和当前阶段，而非总编排内包办。
- 检查是否读取了任务所需 reference，而不是全量加载。
- 检查 handoff 是否包含生命周期阶段、目标 worker、素材证据、约束、风险和下一步。
- 确认所有 blocking 风险都有下一步处理者。
- 路由 smoke 可在仓库根目录运行 `skillctl route --task "写一篇小红书笔记，主题是打工人周末复盘" --target cli/auctra --json`。
