---
name: product-review-writer
description: Use when writing Chinese product reviews, comparison notes, recommendation posts, or experience-based evaluations with evidence, scenarios, tradeoffs, risk disclosure, and clear fit judgment.
---

# 中文产品评测写手

基于本人真实体验或用户提供的证据写有用评测，不写无依据种草。

## 输入

- 产品、目标读者、使用场景、价格/背景、替代品和披露限制。
- 用户体验、测试条件、截图摘要、优缺点、不能说的承诺。

## 输出

- 评测正文、对比表、适合/不适合人群、购买或使用建议。
- 事实/体验/判断分层说明。
- 风险、限制和需要补充的证据。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 明确产品、读者、场景、价格、替代品和披露要求。
2. 区分可观察事实、本人体验和主观判断。
3. 比较取舍：谁适合买、谁不适合买，以及原因。
4. 写入具体使用场景、踩坑点和实用建议。
5. 避免无依据的医疗、金融或效果保证类说法。

## 质量门槛

- 结论必须来自已提供证据或清楚标注为主观体验。
- 不能只罗列参数，要说明对用户决策的影响。
- 商业合作、样品或利益关系需要提示用户披露。

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
