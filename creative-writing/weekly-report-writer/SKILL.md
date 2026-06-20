---
name: weekly-report-writer
description: Use when writing Chinese weekly reports, work summaries, progress updates, retrospectives, or planning notes with outcomes, evidence, blockers, priorities, and next-week commitments.
---

# 中文周报写手

把原始工作记录整理成对决策有用的中文更新。

## 输入

- 已完成成果、证据、阻塞、决策、指标、下周优先级和受众。
- 原始流水记录、提交摘要、会议纪要、项目目标和口吻要求。

## 输出

- 摘要、已完成工作及证据、风险/阻塞、下周计划。
- 按目标分组的进展，而不是时间流水账。
- 需要上级/协作者决策或支持的事项。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 收集成果、证据、阻塞、决策、指标和下一步优先级。
2. 按目标或项目分组，不按时间流水账排列。
3. 说明影响：改变了什么、为什么重要、还有什么风险。
4. 把阻塞写成可处理请求，标明责任人或依赖。
5. 下周承诺简洁、可验证、不过度承诺。

## 质量门槛

- 每个成果最好有证据或可观察结果。
- 风险不能被包装成“基本完成”。
- 计划要可执行，不写空泛方向。

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
