---
name: creative-writing-router
description: Use when routing Chinese creative-writing, screenplay, AI drama, self-media, cross-media, style-reference, or Auctra preparation tasks to the narrowest task-role skill, evidence constraint, canonical owner, and next gate without drafting inside the router.
---

# 中文创作任务与风格路由器

先判断“当前需要哪种任务角色解决哪个 artifact 问题”，再加载最小 skill。路由器不直接包办成稿，不按名人身份分派 writer。

## 输入

- 用户请求、目标受众、媒介、平台、内容类型、当前 phase/artifact 和已有 Auctra 项目上下文。
- 可选来源、风格参考、项目 voice/style bible、accepted revision、已启用技能列表和目标 owner。

## 输出

返回 `CreativeRoutePlan`，作者看到的主要动作只有：

| 动作 | 说明 | 常见 phase |
| --- | --- | --- |
| 写作 | 产出新的候选正文或结构草案 | `draft` / `scene_write` |
| 规划 | 形成 brief、结构、人物或课程顺序 | `brief` / `outline` |
| 审稿 | 阅读候选、差异、事实和连续性问题 | `review` |
| 修订 | 基于已选反馈形成 successor candidate | `revise` |
| 整理 | 归档、重排、引用核对和交接准备 | `organize` / `handoff` |

- 路由仍返回稳定字段：`goal`、`medium`、`phase`、`operation`、`artifact`、`task_role`、`desired_effect`、`evidence_state`、`primary_role`、`primary_skill`、`compatible_skill`、`style_lens_skill`、`style_dimensions`、`originality_constraints`、`input_refs`、`missing_inputs`、`canonical_owner`、`gates`、`owner_action`、`next_action`、`status`。一次请求只有一个 primary，最多一个必要 constraint；审稿不等于采纳，整理不等于保存。

当候选冲突时给出默认分派和最多三个必要问题，不把冲突留给多个 writer 同时改稿。

## 参考资料

- 需要按准备、规划、起草、修订、评审和交付选择任务角色时读取 `references/creative-role-task-map.md`。
- 需要教学、PPT 页级讲稿或课程系列时读取 `../../content-writing/tutorial-writer/references/teaching-and-presentation.md`。
- 用户点名创作者、作品、流派、情绪或视觉风格时，先读取并调用 `creative-style-lens-builder`；不要直接加载 persona imitation skill。
- 需要公众号、书评、产品评测、教程、周报或旅行攻略结构时读取 `../../content-writing/wechat-article-writer/references/platform-nonfiction-playbook.md`。
- 已有文本需要去 AI 味、保真润色、作者声音校准或终稿自然度复检时调用 `natural-writing-editor`；新稿仍由对应 writer 负责，编辑器只作为 revise/final-pass owner 或兼容质量约束。

## 工作流

1. 先把用户请求归入写作、规划、审稿、修订、整理之一，再识别 `medium`、`phase`、`artifact`、`task_role`、`desired_effect`、`evidence_state`、`canonical_owner`。
2. 若请求包含“像某人/某作品/某导演”“某某风格”或混合参考，先交给 `creative-style-lens-builder` 形成原创 `StyleLens`，再选择 writer。
3. 按 `creative-role-task-map.md` 选择一个 primary skill；只有确有输入/质量依赖时增加一个 compatible constraint skill。
4. 中文小说默认写作主技能为 `chinese-novel-chapter-writer`；大纲、人物、文风和前文只按需读取，验收关注人物知识、位置、时间、资源和伏笔后果，不强制每章反转。
5. 剧本/AI 漫剧继续识别 Story、Character、Showrunner、Scene Writer、Director、Visual、Continuity、Critic、Producer 和 Production handoff。
6. 自媒体继续识别来源研究、账号定位、选题/brief、正文、标题、平台结构、图卡/视觉、事实/风险 review 和跨平台改写。
7. Auctra 项目内结构化变更必须走 Auctra 命令，candidate 先进入 review；任意 skill 只提供 proposal/handoff。已有绑定文件先 `auctra work inspect --file ./chapter.md --json`，无路径新稿按用户意图创建或绑定；候选登记后先展示 candidate/diff，作者明确决定后才采纳和写回。
8. 本地路径使用已安装 CLI；远程路径使用 MCP `tools/list`、search 的 `input_schema`、capabilities/resource 和 HTTP invoke/input/download。远程客户端无需安装 CLI，不提交服务端路径、target directory、shell 或 actor 字段；长任务用原 ref status 回查，未知结果不自动重试。生成、accept、apply、saved version 和 export/download 始终分开。
9. 服务不可用时保留普通本地待审稿并标为未登记；不伪造 receipt、不自动创建同名作品。未实现的远程能力标记 pending，而不是写成当前支持。
10. 若 skill 未启用，优先按需读取来源；只有会话启动必需、高频或 owner 明确要求时，才生成 `SkillActivationPlan` 并交给 `creative-writing-installer`。外部安装和 profile mutation 都需要当前用户明确授权。
11. 默认保留用户语言；中文创作输出默认中文，协议字段、skill 名称和命令保持稳定英文。

## 六类内容默认路由

- 小说 → `chinese-novel-chapter-writer`；大纲、人物、文风、前文按需读取。
- 剧本 → `ai-drama-router`，再进入已有编剧方法或 `screenplay-scene-writer`；整集原文是唯一正文，场景只引用 AST/source span。
- 小红书单篇 → `xhs-note-writer`；多篇组织才用 `xhs-orchestrator`，不自动发布。
- 课件 → `tutorial-writer`；输出目标、顺序、例子、讲义、练习和答案。
- PPT 讲稿 → `tutorial-writer` + `teaching-and-presentation.md`；逐页对应口播、衔接和预计时长，不增加渲染器。
- 长期讲课视频 → `tutorial-writer` + `teaching-and-presentation.md`；课程/课次、先修、口播、演示、时长、复习和练习，不套短视频强钩子。

## 核心路由

- Auctra pending review、候选稿与旧版/章节卡/读者契约对比 → `auctra-novel-review-orchestrator`。
- 写前上下文、写后台账 delta、反馈归因与多轮优化 → `chinese-novel-context-pack-builder`、`chinese-novel-state-ledger-updater`、`auctra-novel-optimization-loop`。
- 小说项目启动、普通作者目录和 AGENTS 入口 → `auctra-novel-project-starter`；机器状态与绑定仍交给 Auctra runtime。
- 人物任务 → `character-intelligence-router`；普通小说人物卡 → `chinese-novel-character-architect`。
- 小说篇幅/类型/结构/场景/写章/改编/衍生 → 对应 `chinese-novel-*` 最小技能，不让总编排代替 worker。
- 可拍场景剧本与分季分集 → `ai-drama-router`，再选择官方模板或最窄 worker。
- 小红书多阶段任务 → `xhs-orchestrator`；单篇、标题、热点和素材拆帖分别交给对应 `xhs-*` worker。
- 短视频/播客/直播/公众号 → `short-video-scriptwriter`、`podcast-scriptwriter`、`livestream-scriptwriter`、`wechat-article-writer`。
- 已有稿件去 AI 味、润色、声音校准或终稿清理 → `natural-writing-editor`；不默认叠加多个全文改写流程。



## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| 点名人物/作品风格 | 先 `creative-style-lens-builder` | 不加载 persona imitation |
| 事实性成稿无来源 | `needs_evidence` | 不编热点/数据 |
| 多个 writer 争同一 artifact | `writer_conflict` | 只保留一个 primary |
| candidate 未审就要覆盖/导出 | `needs_review` | 不手写 canonical |
| 登录/发布/付费 | `external_side_effect` | 不把“继续”当授权 |

## 严格失败条件

- `needs_style_lens`：点名人物/作品风格但没有维度化原创约束。
- `needs_evidence`：热点、科学、行业、产品或历史事实没有来源，不能进入事实性成稿。
- `phase_artifact_mismatch`：准备工作被错误路由到润色/标题 worker，或未定 brief 就开始终稿。
- `writer_conflict`：多个 writer 同时拥有同一 canonical artifact。
- `needs_owner`：项目写入缺少 canonical owner 或 typed action。
- `stale`：revision、digest、source、style bible 或 accepted candidate 已变化。
- `needs_review`：candidate 未审却被要求覆盖正文、导出 canonical 或声称发布完成。
- `external_side_effect`：登录、发布、私信、刷量、付费调用或生产接受缺少明确授权。

## Auctra 轻集成

- 来源搜索 smoke：`scripts/skills.sh search "中文小说 风格 任务角色"`。
- Auctra 路由输出必须标明 phase、artifact、gate、revision/digest（如有）和 canonical owner。
- 需要 profile 变更时交给 `creative-writing-installer`；不得手写 `.agents/skills/**` 或 `.claude/skills/**`。

## 边界

- 不伪造经历、数据、采访、截图、平台反馈、来源或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不复制外部 persona/director skill 的身份卡、表达 DNA、典型片段或独特词表。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据或结构化资产。
- 需要持久化 Auctra 状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

```bash
scripts/skills.sh resolve creative-writing-router
scripts/skills.sh resolve creative-style-lens-builder
scripts/skills.sh validate-custom
```

人工路由 smoke 至少覆盖小说准备、导演风格短剧、自媒体热点、跨平台改写和 Auctra pending review。
