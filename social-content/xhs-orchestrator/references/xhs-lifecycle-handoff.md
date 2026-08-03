# 小红书生命周期交付规范

## 使用时机

当任务不是单篇直接起草，而是涉及选题、brief、系列拆帖、标题/首句优化、爆款结构、热点承接、个人品牌定位、review 或 Auctra 项目状态交接时读取本文件。本文件定义小红书内容从想法到可审稿素材包的阶段、字段和门禁，避免总编排直接写成品，也避免下游 worker 缺字段接不住。

## 生命周期阶段

| 阶段 | 目标 | 首选技能 | 关键输出 | 不应做的事 |
| --- | --- | --- | --- | --- |
| discovery | 明确目标读者、账号定位、素材可信度和发布目的 | `xhs-orchestrator` | task_brief、reader、account_position、material_gaps | 不在素材不足时编造个人经历 |
| topic | 选题和角度判断 | `xhs-hotspot-rewriter` / `xhs-personal-brand-writer` / `xhs-source-post-factory` | topic_angle、reader_promise、evidence_refs、risk_flags | 不把热点硬套到不相关账号 |
| brief | 形成可起草 brief | `xhs-orchestrator` | note_brief、structure_type、card_need、draft_constraints | 不直接输出最终正文 |
| draft | 写正文、图卡脚本和标签 | `xhs-note-writer` / `xhs-source-post-factory` | title_candidates、body、card_plan、hashtags、missing_details | 不伪造截图、数据和发布效果 |
| optimize | 优化标题、首句、结构和留存 | `xhs-title-optimizer` / `xhs-viral-structure-writer` | ab_titles、hook_options、retention_changes、anti_ai_polish | 不承诺涨粉或绕平台机制 |
| review | 发布前检查 | `xhs-orchestrator` + 具体 worker | risk_flags、evidence_check、manual_review_notes | 未运行 review 时不声称已通过 |
| handoff | 交给 Auctra 或人工发布 | `creative-writing-orchestrator` / Auctra CLI | next_action、owner、paths_or_commands | 不执行登录、发布或私信 |

## 路由矩阵

- 用户只要一篇完整笔记：直接交给 `xhs-note-writer`。
- 用户要标题、封面标题、首句或点击率复盘：交给 `xhs-title-optimizer`。
- 用户已有草稿但结构松、AI 味重、缺收藏点：交给 `xhs-viral-structure-writer`。
- 用户要蹭热点、趋势改写、热点风险：交给 `xhs-hotspot-rewriter`。
- 用户有 PDF、长文、会议记录、文件夹素材，要拆系列：交给 `xhs-source-post-factory`。
- 用户要创始人 IP、专家人设、职业成长表达：交给 `xhs-personal-brand-writer`。
- 用户要从小说章节引流到小红书：先交给 `chinese-novel-content-spinoff-architect`，再由其 handoff 到小红书 worker。
- 用户同时要选题、正文、标题、审稿、导出或跨平台改写：保留在 `xhs-orchestrator`，分阶段派发。

## 标准 handoff 字段

```markdown
- source_skill: xhs-orchestrator
- target_skill: xhs-note-writer | xhs-title-optimizer | xhs-viral-structure-writer | xhs-hotspot-rewriter | xhs-source-post-factory | xhs-personal-brand-writer
- lifecycle_stage: discovery | topic | brief | draft | optimize | review | handoff
- task_brief: 本轮目标、目标读者、账号定位、发布目的
- source_material: 原始素材摘要、引用范围、不可改动事实、缺失证据
- reader_promise: 读者点开后能得到什么
- structure_type: 经历复盘 | 清单 | 避坑 | 教程 | 观点 | 故事 | 种草 | 拆解
- deliverables: 标题组、正文、图卡页序、标签、评论引导、review notes
- constraints: 字数、图卡页数、禁用词、不得编造的边界、是否允许导流
- risk_flags: 事实缺口 / 虚假经历风险 / 过度承诺 / 医疗金融等高风险 / 平台禁区
- next_action: 需要哪个 worker 继续、是否进入 Auctra material/text/review/export
```

## 输出模板

### 阶段计划

```markdown
## 小红书工作流计划

- 当前阶段：
- 推荐技能：
- 任务判断：
- 必读 reference：
- 交付物：
- 阻塞：
- 下一步：
```

### 交付检查表

```markdown
## 发布前检查

- 点开理由：已明确 / 待补
- 读完理由：已明确 / 待补
- 收藏或评论理由：已明确 / 待补
- 真实素材依据：已标注 / 待补
- 图卡页序：不需要 / 3 页 / 6 页 / 9 页 / 待定
- 标题风险：低 / 中 / 高，说明：
- 平台禁区：无 / 有，说明：
- 待人工确认：
```

## Auctra handoff

- 只需要一次性草稿时，直接返回 Markdown 素材包即可。
- 需要保存素材时，建议先用 `auctra material` 记录 source material。
- 需要生成正文资产时，建议用 `auctra text` 创建或更新文本项。
- 需要审稿时，建议用 `auctra review` 产生 review 结果。
- 需要导出时，建议用 `auctra export` 生成交付物。
- 不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 质量门禁

- 每个输出都必须说明目标读者、读者承诺和素材依据。
- 缺真实经历、截图、数据、采访或平台反馈时，以待补问题列出，不编造。
- 标题可以强钩子，但不得制造虚假结果、虚假身份或虚假平台背书。
- 需要图片时只描述图卡脚本或视觉需求；实际图片生成交给 Eikona 小红书图像技能。
- 未实际运行 Auctra 命令时，不声称项目状态、review 或 export 已完成。
