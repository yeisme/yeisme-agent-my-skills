---
name: book-review-writer
description: Use when writing Chinese book reviews, reading notes, recommendations, or theme essays that go beyond plot summary and include insight, textual evidence, reader fit, and personal takeaway.
---

# 中文书评写手

写能回答“这本书为什么值得某类读者读”的中文书评，而不是只复述剧情。

## 输入

- 书名、作者、类型、目标读者、素材笔记、是否允许剧透。
- 用户想强调的主题、个人经历、引用、平台和篇幅。

## 输出

- 无剧透版或含剧透版书评。
- 核心洞察、文本证据、个人收获、适合/不适合读者和推荐结论。
- 可选标题、摘要、金句和延伸阅读问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 明确书名、目标读者、评论角度、剧透边界和素材笔记。
2. 区分内容摘要、核心洞察、证据/引用、个人共鸣和推荐结论。
3. 用具体情节、段落或观点支撑判断，不用剧情复述替代分析。
4. 写出这本书对哪类读者有用，对哪类读者可能不适合。
5. 需要时分别提供无剧透版和含剧透版。

## 质量门槛

- 至少有一个清晰判断和两个以上证据点。
- 不把作者观点、角色观点和自己观点混为一谈。
- 没有读过或缺少素材时，不假装知道具体章节。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
