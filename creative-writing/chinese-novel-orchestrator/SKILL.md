---
name: chinese-novel-orchestrator
description: Use when planning, drafting, continuing, revising, decomposing, or adapting Chinese narrative fiction across short stories, novellas, long-form serials, series, reader contract, project bible, scene cards, continuity, Auctra review flow, and cross-media handoff.
---

# 中文小说总编排

运行完整中文小说与叙事作品工作流。它负责分派最小合适技能、控制项目状态和交付顺序，覆盖短篇、中篇、长篇、系列文、小说拆解、主题拆分和全媒介改编，不把所有创作决策都塞进一个提示词。

## 输入

- 小说目标、已有材料、Auctra 项目状态、目标篇幅/媒介、读者定位、更新时间和交付格式。
- 用户需要的阶段：立项、篇幅选择、规划、写章、续写、拆解、主题拆分、改编、修订、review、导出或校验。

## 输出

- 端到端工作计划和当前阶段交付物。
- 篇幅形态、拆解目标、改编媒介、应加载的子技能、需要读取的参考、Auctra 命令建议和 handoff。
- 完成报告：产物、验证、阻塞、待确认和下一步。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-length-form-matrix.md`：需要短篇、中篇、长篇、系列文结构选择、压缩、扩写或篇幅转换时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-analysis-decomposition.md`：需要拆解小说主题、结构、人物弧线、场景功能、伏笔或 IP 可改编性时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-adaptation-matrix.md`：需要把小说改编成短剧、长电视剧、电影、广播剧、有声书、漫画/动态漫、游戏剧情或短视频系列时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-content-spinoff.md`：需要把小说章节或项目圣经转成小红书/公众号/短视频选题、角度、剧透边界和平台宣发包时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-theme-breakdown.md`：需要拆分主题命题、反命题、人物承载、场景证明或平台表达角度时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-search-keyword-presets.md`：需要参考知名小说、搜索预设关键词、同类作品结构拆解或反抄袭边界时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-premise-scene-idea-bank.md`：需要批量生成故事前提、场景思路、前 10 章钩子或类型组合变体时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-review-gate.md`：需要验收单章目标、冲突升级、信息增量、人物推进、连续性 delta、章尾钩子和 risk_flags 时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-serial-operations.md`：需要安排连载更新节奏、cliffhanger 排程、读者反馈归因、下一章承诺和社媒衍生节奏时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段、章首/章尾模板或场景家族入口时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查、多轮修订门禁或 blocking/deferred 判定时读取。
- 类型专项参考：悬疑/推理读取 `chinese-novel-genre-suspense-mystery.md`，言情读取 `chinese-novel-genre-romance.md`，玄幻/奇幻读取 `chinese-novel-genre-xuanhuan-fantasy.md`，都市/职场读取 `chinese-novel-genre-urban-career.md`，科幻读取 `chinese-novel-genre-sci-fi.md`，历史/权谋/宫斗读取 `chinese-novel-genre-historical-power.md`，武侠/仙侠读取 `chinese-novel-genre-wuxia-xianxia.md`，灵异/恐怖读取 `chinese-novel-genre-horror-supernatural.md`，冒险/夺宝/无限流/生存读取 `chinese-novel-genre-adventure-survival.md`。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-suspense.md`：需要线索发现、误导、审讯、跟踪、反转或真相推进模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-relationship.md`：需要初遇、试探、误会、告白、背叛或和解模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-escalation.md`：需要升级、战斗、竞赛、谈判、资源争夺或失败代价模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-worldbuilding.md`：需要规则展示、地点进入、组织势力、道具能力或信息解释模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-transition.md`：需要过渡章、日常缓冲、旅途、训练、调查间隙或余波模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-climax-payoff.md`：需要小高潮、卷中/卷末高潮、伏笔回收或情绪结算模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-investigation-procedure.md`：需要取证、讯问、证词矛盾、时间线复核或程序阻力模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-power-politics.md`：需要权谋、宫斗、朝堂、宗门、派系或公开仪式模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-heist-strategy.md`：需要夺宝、潜入、救援、破阵、团队分工或撤离追逐模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-survival-disaster.md`：需要生存、灾变、无限流副本、资源耗尽或逃生倒计时模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-horror-supernatural.md`：需要灵异、恐怖、民俗禁忌、规则怪谈或异常信号模板时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-scene-library-comedy-satire.md`：需要喜剧、讽刺、黑色幽默、身份错位或误会升级模板时读取。

## 工作流

1. 判断任务类型：原创写作、续写修订、篇幅转换、作品拆解、主题拆分、章节验收、连载运营、媒介改编或导出校验。
2. 判断承载形态：微型、短篇、中篇、长篇、系列文、连载、短剧、长剧、电影、音频、漫画、游戏或短视频系列。
3. 按最小范围分派子技能；篇幅先交给 `chinese-novel-length-form-architect`，拆解先交给 `chinese-novel-analysis-decomposer`，章节验收交给 `chinese-novel-chapter-reviewer`，连载运营交给 `chinese-novel-serial-operations-editor`，改编先交给 `chinese-novel-adaptation-architect`，社媒引流交给 `chinese-novel-content-spinoff-architect`。
4. 需要持久化时使用 Auctra 命令，候选稿先进入 review。
5. 原创正文要求冲突、转折、角色差异对白、感官细节、阶段回报和结尾钩子；分析/改编要求事实边界、交接包和下一步 owner。
6. 完成前校验连续性、留存、禁写规则、字数/媒介限制和 handoff。

## 质量门槛

- 除非已运行 Auctra 命令或得到人工审稿，不声称 Auctra 审稿已完成。
- 默认服务中文叙事作品，不自动转成英文小说写作。
- 不把短篇、中篇、长篇、剧本、短剧、电影、漫画、音频和游戏剧情混用同一套结构。
- 输出必须可交给具体 worker 继续执行。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 章节长度可用 `python3 .skills/yeisme/creative-writing/chinese-novel-orchestrator/scripts/check_chinese_chapter_wordcount.py <chapter.md> 3000` 检查。
- 检查是否读取了任务所需 reference，而不是全量加载。
- 确认所有 blocking 风险都有下一步处理者。
