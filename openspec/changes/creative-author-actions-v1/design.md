# 设计：五个作者动作与内容类型路由

## Context

`.skills/yeisme/creative-writing-core/creative-writing-router` 已提供 `CreativeRoutePlan`、canonical owner、candidate/review gate 与按需加载原则，但作者可见的任务角色仍然过细，且既有引用包含已退役的工作区路由与中文 starter。批准计划要求 Skills 源只描述可移植的创作判断；Auctra CLI、profile 管理器和生成 runtime 分别由对应 owner 实现。

## Decisions

### 1. 五个显示动作，保留稳定机器字段

动作标签固定为：

| 作者说法 | 语义 | 主要 phase 示例 |
| --- | --- | --- |
| 写作 | 产出新的候选正文或结构草案 | `draft` / `scene_write` |
| 规划 | 形成 brief、结构、人物或课程顺序 | `brief` / `outline` |
| 审稿 | 阅读候选、差异、事实和连续性问题 | `review` |
| 修订 | 基于已选反馈形成 successor candidate | `revise` |
| 整理 | 归档、重排、引用核对和交接准备 | `organize` / `handoff` |

Router 输出继续携带 `phase`、`artifact`、`primary_skill`、`canonical_owner`、`gates` 与 `next_action`。一次请求只能有一个 primary；兼容约束只在输入或验收确实需要时加载。`整理` 不等于接受或保存，`审稿` 不等于采纳。

### 2. 六类内容使用实际方法

- 小说默认 `chinese-novel-chapter-writer`；大纲、人物、文风和前文只按需读取。验收覆盖连贯章节、人物知识、位置/时间/资源和伏笔后果，不强制每章反转。
- 剧本经 `ai-drama-router` 进入已有编剧方法或 `screenplay-scene-writer`；验收覆盖可表演动作对白、分集分场、整集原文和场景区间，不另造第二份场景正文。
- 小红书单篇默认 `xhs-note-writer`，多篇才用 `xhs-orchestrator`；验收覆盖选题、正文、标题、配图说明、事实/广告风险和真实经历检查，不自动发布。
- 课件使用 `tutorial-writer`；产物包含课程目标、学习顺序、例子、讲义、练习和答案，不硬套故事冲突。
- PPT 讲稿使用同一 `tutorial-writer` 的教学/演讲参考；每页标题与要点须对应口头讲稿、衔接与预计时长，不增加渲染引擎。
- 长期讲课视频使用同一 `tutorial-writer` 的课程系列参考；产物包含课程/课次、先修知识、口播、演示步骤、时长、复习和练习，不复用短视频强钩子模板。

教学参考只新增普通文件 `content-writing/tutorial-writer/references/teaching-and-presentation.md`，不新增内容类型、CLI 或存储模型。`natural-writing-editor` 仅在修订或终稿需要时调用。

### 3. 本地和远程运行指导边界

源 Skill 只描述 capability-neutral 路由：

- 本地：使用宿主已安装的 Auctra CLI，先发现当前 work/unit，再创建或绑定稿件，候选进入 review；生成、accept、apply、saved version 和 export 分开。
- 远程：使用 MCP `tools/list`、search 的 `input_schema`、capabilities/resource 和 HTTP invoke/input/download；客户端不安装 CLI，不提交服务端路径，不把结果未知当作成功。
- 生成不等于采纳，accept 不等于 apply，working file 不等于 saved version；作者未明确决定时不能调用 reviewer 动作。
- 服务不可用时保留普通本地待审稿，并标为未登记；禁止伪造回执或自动创建同名作品。

真实 action、scope、长任务和下载合同由 Auctra change 提供；本 change 仅提供作者侧可移植说明与 handoff 依赖。

### 4. 自然词和退役引用

作者文件、标题、帮助、错误解释和默认下一步使用世界观/作品说明、文风、读者、时间线/前后衔接、地图/人物参考图/场景参考图等自然词。机器 schema、operation、ref、历史归档和剧情对白不全局替换。实现阶段以精确引用扫描迁移退役 `auctra-i18n-workspace-router`、`auctra-chinese-project-starter`，并把 `chinese-novel-project-bible-keeper` 迁移为 `chinese-novel-setting-editor`；本 change 不直接删除文件或 profile。

### 5. 交接与验证

本 change 的实现任务按共享路由、内容方法、引用迁移和验证交接分组。任务必须标注 `CONTRACT`、owner、owned/shared/forbidden paths、依赖、验收、focused verification、evidence target 和 stop condition。实现阶段禁止修改产品代码与运行副本；稳定后由 owner 运行源仓验证和本 change strict 校验。
