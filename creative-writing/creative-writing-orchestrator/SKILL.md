---
name: creative-writing-orchestrator
description: Use when coordinating multi-stage Chinese creative-writing tasks across planning, drafting, editing, review, cross-format transformation, Auctra project work, export, and handoff.
---

# 中文创作总编排

协调端到端中文创作，不把所有创作决策都塞进一个提示词。适合跨格式、跨阶段、Auctra 项目或需要 review/export 的任务。

## 输入

- 用户目标、内容类型、目标读者、素材、截止时间、发布平台和期望输出格式。
- 已有 Auctra 项目、普通稿件文件、route 结果或多个技能输出。

## 输出

- 阶段化执行计划：创作简报、结构、初稿、润色、校验、审稿、导出/交付。
- 每阶段推荐技能、输入、输出、验收和 handoff。
- 最终完成报告：产物、路径、未解决问题和建议下一步。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-adaptation-matrix.md`：需要小说转短剧、长电视剧、电影、音频、漫画、游戏剧情或短视频系列的改编交接包时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-analysis-decomposition.md`：需要先拆解小说主题、结构、人物、场景功能或 IP 价值时读取。

## 工作流

1. 将请求拆成阶段：创作简报、结构、初稿、润色、校验和导出。
2. 任务类型不明确或涉及多个候选技能时，先运行或引用 `skillctl route`，再决定 owner skill。
3. 每个阶段交给范围最窄的工作技能。
4. Auctra 工作优先使用 `auctra material`、`auctra text`、`auctra review` 和 `auctra export`。
5. 跨格式改写时保留原始意图，例如小说章节转小红书笔记、公众号文章或改编交接包。
6. 小说改编先产出改编诊断、媒介结构和交接包，再交给 `screenplay-scene-writer`、`short-video-scriptwriter`、`podcast-scriptwriter` 等具体写手。
7. 返回简洁完成报告，包含输出路径、未解决问题和下一步。

## 质量门槛

- 每份稿件都要有明确读者、承诺、结构、素材依据和修订目标。
- 中文小说保留人物一致性、冲突、钩子和连续性；改编任务还要保留不可牺牲承诺、删改边界和媒介结构。
- 平台内容贴合平台机制，不复用泛泛文案。
- 默认产出中文稿件。

## Auctra 轻集成

- 普通单篇写稿不强制进入 Auctra。
- Auctra 项目内的材料、正文、review、export 必须使用对应 CLI，不手写结构化状态。
- 不自动 accept review，不自动覆盖正文，不自动发布。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 确认每个阶段都有 owner skill、输入、输出和验收。
- 检查跨格式改写是否保留事实边界和原始意图。
- 未运行 Auctra 命令时，不声称 review/export 已完成。
