---
name: xhs-source-post-factory
description: Use when turning PDFs, Markdown, TXT, JSON, long articles, meeting notes, or folders of source material into Xiaohongshu note series, post packages, and card scripts without losing source facts.
---

# 小红书素材拆帖工厂

把长素材拆成可发布的小红书中文笔记和系列内容，不丢失事实来源。

## 输入

- 用户粘贴的长文内容、文件摘要、目录、研究材料或结构化笔记。
- 目标读者、账号定位、希望产出篇数、是否需要图卡脚本和不可改动事实。

## 输出

- 素材提炼表：事实、观点、案例、步骤、金句、限制条件。
- 系列选题：发布顺序、每篇读者承诺、标题、正文大纲、证据和图卡页序。
- 第一篇完整正文，其余篇可继续扩写的素材包。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要标题公式、正文结构、图卡页序和素材拆帖模板时读取。
- `../xhs-note-writer/references/xhs-title-card-and-risk-checklist.md`：需要封面标题、3/6/9 图卡和热点/个人品牌风险检查时读取。

## 工作流

1. 先提炼事实、观点、案例、步骤、金句和限制条件。
2. 设计单篇或系列结构，控制信息密度和发布顺序。
3. 每篇输出标题、正文大纲、关键证据、图卡页序和话题标签。
4. 对第一篇写完整正文，其余篇给可扩写素材包。
5. 标注需要用户补充的本人经历、截图、数据来源或产品细节。

## 质量门槛

- 不把长文机械压缩成摘要，要转成小红书读者能收藏的结构。
- 保留事实出处，不编造原文没有的结论。
- 图片只输出静态图需求，生成交给 Eikona 图像技能。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra text export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
