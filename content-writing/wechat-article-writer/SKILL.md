---
name: wechat-article-writer
description: Use when structuring, drafting, expanding, or polishing WeChat Official Account articles with title, abstract, argument, evidence, section logic, pull quotes, mobile layout, and call to action.
---

# 微信公众号文章写手

把素材整理成有逻辑、有深度、适合手机阅读的中文长文。

## 输入

- 读者问题、文章目的、核心观点、素材、证据、案例和期望动作。
- 平台语气、品牌边界、标题方向、篇幅、是否需要排版建议。

## 输出

- 标题候选、2-3 行摘要、分节大纲。
- 完整正文或分节草稿，含过渡、例子、金句和结尾行动引导。
- 逻辑缺口、事实缺口、标题风险和排版建议。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 明确读者问题、文章承诺、核心观点、证据和期望动作。
2. 生成标题候选和摘要，不让标题承诺超过正文。
3. 搭建分节大纲，安排过渡、例子、金句和结尾。
4. 用适合手机阅读的段落起草，避免浅层评论。
5. 检查逻辑缺口、无依据判断、重复段落、弱过渡和误导性标题。

## 质量门槛

- 每一节都要服务中心论点。
- 证据和观点分清，不用情绪替代论证。
- 标题有吸引力但不误导。

## Auctra 轻集成

- 普通公众号稿可直接输出 Markdown。
- Auctra 项目中可建议 `auctra text new wechat_article --title "..." --platform wechat_article --json`。
- 需要审稿和导出时使用 `auctra review`、`auctra export`。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
