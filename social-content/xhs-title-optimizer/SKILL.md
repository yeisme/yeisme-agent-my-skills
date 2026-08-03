---
name: xhs-title-optimizer
description: Use when optimizing Xiaohongshu titles, cover titles, first-line hooks, search keywords, risk-aware high-click variants, and A/B title groups.
---

# 小红书标题优化师

把普通标题改成更容易被点开、收藏和搜索命中的中文标题组。

## 输入

- 主题、目标读者、正文要点、账号定位、禁用词和发布场景。
- 已有标题、封面图方向、想要的情绪强度和关键词。

## 输出

- 12-20 个标题候选，按痛点型、结果型、反差型、清单型、故事型、搜索型分组。
- 每个标题对应封面短句、适合正文角度和风险提示。
- 3 个优先测试标题及点击理由。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要标题公式、正文结构、图卡页序和素材拆帖模板时读取。
- `../xhs-note-writer/references/xhs-title-card-and-risk-checklist.md`：需要封面标题、3/6/9 图卡和热点/个人品牌风险检查时读取。

## 工作流

1. 提炼读者痛点、结果承诺、反差点、身份标签和搜索关键词。
2. 生成多类型标题，不让所有标题只换词。
3. 标注标题和封面短句的信息分工。
4. 剔除虚假经历、绝对化效果、医疗金融承诺和过度标题党。
5. 给出优先测试顺序和为什么。

## 质量门槛

- 标题必须符合中文小红书语感，避免英文标题腔。
- 关键词自然嵌入，不堆砌标签。
- 不能牺牲真实度换点击。

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
