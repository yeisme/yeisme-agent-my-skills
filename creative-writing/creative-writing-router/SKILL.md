---
name: creative-writing-router
description: Use when routing Chinese creative-writing or Auctra content tasks to the narrowest suitable writing, editing, script, platform-content, review, export, or installer skill without drafting inside the router.
---

# 中文创作路由器

先路由请求，再加载能完成目标稿件的最小工作技能。路由器不直接包办成稿。

## 输入

- 用户请求、目标读者、语言、内容类型、已有 Auctra 项目上下文。
- 可选的 `skillctl route` 结果、已启用技能列表、目标子项目。

## 输出

- 推荐技能、推荐理由、是否需要安装/启用、下一步动作。
- 当候选冲突时，给出 1-3 个澄清问题或默认分派。
- Auctra 项目边界和需要运行的真实命令。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 识别内容家族：中文小说、小红书、公众号、短视频、剧本、产品评测、直播、播客、书评、旅行攻略、教程、周报。
2. 中文小说内继续识别任务形态：短篇/中篇/长篇/系列文、类型契约、搜索关键词预设、场景思路、场景卡、章节写作、作品拆解、主题拆分、全媒介改编或修订。
3. 优先选择具体工作技能；只有跨格式、跨阶段或 Auctra 项目任务才使用总编排。
4. 若技能未启用，交给安装器通过 `skillctl` 启用。
5. Auctra 项目内结构化变更必须走 Auctra 命令，不手写 `.auctra/**` 状态。
6. 默认保留用户语言；创作输出默认中文。

## 质量门槛

- 推荐必须匹配稿件类型和当前阶段。
- 除非没有合适工作技能，路由器不直接产出最终稿。
- 展示给用户的命令必须是真实可运行命令。

## Auctra 轻集成

- 路由 smoke 可在仓库根目录运行 `skillctl route --task "写一篇中文书评，不能只复述剧情" --target cli/auctra --json`。
- 需要安装集合时交给 `creative-writing-installer`。
- 小说短篇/中篇/系列篇幅选择优先交给 `chinese-novel-length-form-architect`。
- 小说类型契约、读者承诺、知名小说结构参考和搜索关键词预设优先交给 `chinese-novel-genre-contract-strategist`；已有作品/样章拆解时交给 `chinese-novel-analysis-decomposer`。
- 小说权谋、调查、夺宝、生存、灵异、喜剧等具体章节场景拆分优先交给 `chinese-novel-scene-card-writer`。
- 小说前 10 章、分阶段章节表和类型组合大纲优先交给 `chinese-novel-outline-architect`。
- 小说拆解、主题拆分、结构复盘或 IP 评估优先交给 `chinese-novel-analysis-decomposer`。
- 小说转短剧、长电视剧、电影、音频、漫画、游戏剧情或短视频系列优先交给 `chinese-novel-adaptation-architect`。
- 小说社媒引流（小红书/公众号/短视频选题、角度、剧透边界和宣发包）优先交给 `chinese-novel-content-spinoff-architect`。
- 小红书选题/brief/标题/爆款结构/热点改写/素材拆系列/个人品牌/多阶段笔记任务优先交给 `xhs-orchestrator`。
- 跨格式改写或多阶段项目交给 `creative-writing-orchestrator`。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 确认路由表覆盖用户内容家族。
- 检查是否错误推荐了总编排或安装器。
- 如果 `skillctl route` 结果和人工判断冲突，说明原因并给出最小下一步。
