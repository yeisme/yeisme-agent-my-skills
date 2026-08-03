---
name: xhs-note-writer
description: Use when creating, revising, or rewriting Xiaohongshu note packages with title hooks, body copy, cover/card requirements, first-person evidence, takeaways, hashtags, and manual publishing handoff.
---

# 小红书笔记素材包写手

基于素材和本人真实细节写小红书笔记素材包，不写泛泛建议，不替用户伪造经历。

## 输入

- 主题、目标读者、发布目的、本人经历、产品/服务/观点素材。
- 参考笔记、图片素材、禁用词、账号定位、期望语气和是否需要图卡。

## 输出

- 5-8 个标题候选，标注情绪钩子、利益点、反差点或搜索关键词。
- 一篇可继续润色发布的中文正文。
- 封面标题、首图说明、3/6/9 图卡页序和每页文案。
- 话题标签组合、去 AI 味检查、需要用户补充的真实细节问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要标题公式、正文结构、图卡页序和素材拆帖模板时读取。
- `../xhs-note-writer/references/xhs-title-card-and-risk-checklist.md`：需要封面标题、3/6/9 图卡和热点/个人品牌风险检查时读取。

## 工作流

1. 明确读者、使用场景、本人体验证据和期望动作。
2. 先产出标题/钩子候选，再写正文；标题优化可交给 `xhs-title-optimizer`。
3. 正文使用短段落、具体细节、个人观察、收获点和评论/收藏触发点。
4. 需要图卡时输出封面和 3/6/9 图顺序；静态图生成交给 Eikona 小红书图像技能。
5. 最后检查泛泛而谈、虚假经历、过度承诺和 AI 味句式。

## 质量门槛

- 每篇笔记必须有为什么点开、为什么读完、为什么收藏或评论。
- 真实经历缺失时提问，不替用户编造。
- 不承诺涨粉、转化、治疗、收益或平台推荐。

## Auctra 轻集成

- 普通小红书草稿可直接输出 Markdown 素材包。
- Auctra 项目中可建议 `auctra text new xhs_note --title "..." --platform xiaohongshu --json`。
- 需要 review 或导出时使用 `auctra review` 和 `auctra export`，不手写项目状态。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
