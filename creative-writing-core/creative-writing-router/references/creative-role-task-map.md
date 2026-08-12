# 创作任务角色路由图

角色表示当前 artifact 的职责，不表示真实人物人格。每次只选择一个 primary role；兼容 skill 只能提供证据、连续性、风格或质量约束。

## 通用阶段

| Phase | 主要问题 | 常见角色 | 退出条件 |
| --- | --- | --- | --- |
| `discover` | 事实、市场、受众和来源是什么？ | Researcher / Fact Reviewer | 来源、范围、不确定性已记录 |
| `define` | 给谁、承诺什么、为什么值得做？ | Brief Architect / Genre Strategist / Platform Strategist | brief、读者承诺、禁写边界明确 |
| `plan` | 如何组织人物、结构、场景和发布序列？ | Story Architect / Showrunner / Outline Architect / Content Planner | 结构和 artifact handoff 可执行 |
| `draft` | 谁来生成当前稿件？ | Chapter Writer / Scene Writer / Platform Writer | candidate 完整且未越过 owner |
| `revise` | 哪个具体缺陷需要修？ | Dialogue / Continuity / Pacing / Style Editor | 缺陷与改动范围一一对应 |
| `review` | 是否满足事实、原创性、质量和 gate？ | Critic / Fact Reviewer / Producer | verdict、evidence、repair action 明确 |
| `handoff` | 谁接受、持久化、导出或生产？ | Auctra Owner / Eikona / Scaena / Human | typed action 和 receipt 边界明确 |

## 中文小说

| Job | Primary skill | 可选约束 |
| --- | --- | --- |
| 项目 brief、读者与素材边界 | `chinese-novel-brief-architect` | `creative-style-lens-builder` |
| 类型契约、反套路、阶段回报 | `chinese-novel-genre-contract-strategist` | `chinese-novel-length-form-architect` |
| project bible 与 canon 维护 | `chinese-novel-project-bible-keeper` | `chinese-novel-continuity-editor` |
| 写前最小上下文 | `chinese-novel-context-pack-builder` | `character-intelligence-router` |
| 分卷/大纲/前十章 | `chinese-novel-volume-arc-planner` 或 `chinese-novel-outline-architect` | `chinese-novel-reader-retention-editor` |
| 人物研究、设计、验压 | `character-intelligence-router` | 最多一个 character specialist |
| 场景卡 | `chinese-novel-scene-card-writer` | `chinese-novel-hook-pacing-editor` |
| 章节候选 | `chinese-novel-chapter-writer` | `creative-style-lens-builder` |
| 对白/连续性/钩子/文风 | 对应 `chinese-novel-dialogue-editor`、`chinese-novel-continuity-editor`、`chinese-novel-hook-pacing-editor`、`chinese-novel-style-polisher` | 只选当前主要缺陷 |
| 单章验收/修订队列 | `chinese-novel-chapter-reviewer` 或 `chinese-novel-revision-producer` | `auctra-novel-optimization-loop` |
| Auctra pending review 与 accept/reject/partial 建议 | `auctra-novel-review-orchestrator` | `chinese-novel-draft-comparator` |
| 候选稿、旧版/新版和章节卡对比 | `chinese-novel-draft-comparator` | `chinese-novel-chapter-reviewer` |
| 作品/样章拆解、主题拆分和 IP 评估 | `chinese-novel-analysis-decomposer` | `chinese-novel-adaptation-architect` |
| 连载节奏、下章承诺和反馈归因 | `chinese-novel-serial-operations-editor` | `auctra-novel-optimization-loop` |
| 改编/社媒衍生 | `chinese-novel-adaptation-architect` 或 `chinese-novel-content-spinoff-architect` | 目标媒介 worker |

## Auctra 项目准备

| Job | Primary skill | 可选约束 |
| --- | --- | --- |
| `zh-CN/chinese-novel` 新项目、素材/大纲/人物/首章启动 | `auctra-chinese-project-starter` | `chinese-novel-brief-architect` |
| locale、layout preset、display path、migration plan/apply | `auctra-i18n-workspace-router` | `yeisme-auctra-cli-runtime` |
| profile 中缺少已选定创作 skill | `creative-writing-installer` | `yeisme-skill-routing-governance` |

## 剧本与 AI 漫剧

| Job | Primary skill | 可选约束 |
| --- | --- | --- |
| premise、主题、核心冲突 | `ai-drama-story-architecture` | `ai-drama-character-engine` |
| 季/集/单集节奏 | `ai-drama-showrunner` | `ai-drama-story-architecture` |
| 人物动机、秘密、关系、选择 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` |
| 可拍场景与对白 | `screenplay-scene-writer` | `creative-style-lens-builder` |
| 场面调度、情绪转动作 | `ai-drama-director` | `ai-drama-continuity-supervisor` |
| 视觉语言与候选 brief | `ai-drama-visual-language` | `creative-style-lens-builder` |
| 连续性 | `ai-drama-continuity-supervisor` | `ai-drama-director` |
| 候选评分与修复 | `ai-drama-critic-panel` | `ai-drama-producer` |
| 成本、批次、权限和 acceptance | `ai-drama-producer` | `ai-drama-critic-panel` |
| Scaena/Ordo 运行 handoff | `ai-drama-production-orchestrator` | `ai-drama-producer` |

## 自媒体与平台内容

| Job | Primary skill | 可选约束 |
| --- | --- | --- |
| 热点、科学、产品、行业事实研究 | `internet-access` | 目标平台 worker |
| 小红书多阶段规划 | `xhs-orchestrator` | `creative-style-lens-builder` |
| 小红书单篇正文 | `xhs-note-writer` | `xhs-title-optimizer` |
| 标题/首句/钩子 | `xhs-title-optimizer` | `xhs-viral-structure-writer` |
| 热点改写 | `xhs-hotspot-rewriter` | `internet-access` |
| 长素材拆系列 | `xhs-source-post-factory` | `xhs-orchestrator` |
| 个人品牌 | `xhs-personal-brand-writer` 或 `twitter-personal-brand-growth` | `creative-style-lens-builder` |
| 短视频时间线脚本 | `short-video-scriptwriter` | `creative-style-lens-builder` |
| 播客/直播 | `podcast-scriptwriter` 或 `livestream-scriptwriter` | 来源/事实 reviewer |
| 公众号与长文 | `wechat-article-writer` | 来源/事实 reviewer |
| 跨平台矩阵 | `creative-writing-orchestrator` | 各平台 worker 顺序 handoff |

## 风格请求示例

| 用户表达 | 路由结果 |
| --- | --- |
| “准备一部王家卫感的都市爱情小说” | `creative-style-lens-builder` → `chinese-novel-genre-contract-strategist` → `chinese-novel-outline-architect`；人名只留在 source refs。 |
| “做一个奉俊昊式阶层反转短剧开场” | `creative-style-lens-builder` → `ai-drama-story-architecture` → `screenplay-scene-writer`；禁止复现来源专名、场景或台词。 |
| “像某 AI 大 V 一样写工具教程” | 拆成实测证据、分级教学、反焦虑语气、平台格式，再路由 `internet-access` + 对应 platform writer。 |
| “混合三位作者的文风” | 先确定 target effect 和 counter lens；禁止把三套标志性句式拼贴成仿写。 |

## 冲突规则

- Story/outline 未定时，Style/Title worker 不得成为 primary。
- Fact reviewer、continuity 和 StyleLens 可作为约束，但不得与 primary writer 竞争 canonical ownership。
- `creative-writing-orchestrator` 只用于跨阶段/跨格式，不应替代具体 worker。
- Auctra 负责持久化文本状态；Eikona 负责视觉候选；Scaena 负责生产；skill 不拥有第二套 canonical state。
