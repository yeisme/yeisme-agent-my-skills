# AI 做剧阶段与 Artifact 路由矩阵

复杂任务由 `ai-drama-production-orchestrator` 编排；Router 自身不并发写作。每个阶段恰好一个 primary Skill，最多一个 constraint Skill。

## 阶段矩阵

| `phase` | 当前 artifact / 用户工作 | Primary Skill | 可选 constraint | `context_pack_profile` | Canonical owner |
| --- | --- | --- | --- | --- | --- |
| `intake` | 媒介、剧型、时长、集数、受众、类型承诺 | `ai-drama-format-strategist` | `ai-drama-producer` | `series-development` 或无 | `story_canon_owner` proposal |
| `define` | premise、主题、核心冲突、故事引擎 | `ai-drama-story-architecture` | `ai-drama-character-engine` | `series-development` | `story_canon_owner` |
| `character` | 欲望、恐惧、秘密、关系、知识边界 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` | `series-development` 或 `episode-planning` | `story_canon_owner` |
| `series_plan` | series bible、季度、pilot、分集、单元结构 | `ai-drama-showrunner` | `ai-drama-story-architecture` | `series-development` / `episode-planning` | `story_canon_owner` |
| `episode_plan` | 本集功能、beat、开场与集尾钩子 | `ai-drama-story-architecture` | `ai-drama-showrunner` | `episode-planning` | `story_canon_owner` |
| `scene_draft` | 场景动作、对白、潜台词和转场 | `screenplay-scene-writer` | `creative-style-lens-builder` | `scene-drafting` | `story_canon_owner` |
| `director_plan` | 表演、调度、空间、镜头和声音意图 | `ai-drama-director` | `ai-drama-visual-language` | `director-planning` | story proposal / `production_owner` intent |
| `visual_plan` | 主体、风格、关键帧、分镜、候选 brief | `ai-drama-visual-language` | `ai-drama-continuity-supervisor` | `visual-production` | `visual_asset_owner` proposal |
| `reference_video` | 参考视频动作、相机、构图、姿态约束 | `ai-drama-video-reference-director` | `ai-drama-continuity-supervisor` | `visual-production` | `production_owner` proposal |
| `evaluation` | 候选盲评、分歧、裁决、修复队列 | `ai-drama-critic-panel` | `ai-drama-producer` | `review-repair` | `evaluation_owner` evidence / artifact owner review |
| `generation` | 成本、权限、能力、批次和 retry admission | `ai-drama-producer` | `ai-drama-continuity-supervisor` | `visual-production` | `production_owner` |
| `assembly` | 剪辑、声音、字幕、节奏和时间线 | `ai-drama-edit-and-sound` | `ai-drama-continuity-supervisor` | `assembly-delivery` | `production_owner` / `audio_owner` refs |
| `delivery_review` | 连续性、rights、cost、readiness 和交付 | `ai-drama-continuity-supervisor` | `ai-drama-producer` | `assembly-delivery` | `production_owner` |
| `cross_owner_run` | 完整阶段、pause/resume、typed handoff | `ai-drama-production-orchestrator` | `ai-drama-producer` | 各 stage 独立选择 | production facade + domain owners |

## 格式修饰规则

`format_profile` 改变 Skill 的工作约束，不创建新的 canonical owner：

- `vertical-short-drama`：每集开场压力、快速状态变化、集尾钩子和可复用场景优先。
- `manga-drama`：视觉可读性、主体连续、动作段、声音与话尾钩子优先。
- `us-hour-drama`：pilot 承诺、A/B/C 线、季度问题和人物长期变化优先。
- `us-half-hour-comedy`：角色缺陷、情境升级、回扣和可重复喜剧引擎优先。
- `procedural-series`：单元程序真实性、每集闭环和角色长线并行。
- `anthology-series`：共享主题/形式约束，不强制共享人物 canon。
- `feature-film`：集中主选择、有限支线、高潮和结尾回收。
- `audio-drama`：声音线索、角色声线、空间声场和可听动作优先。

详细结构由 `ai-drama-format-strategist/references/format-profiles.md` 提供，Router 只引用结果。

## 冲突规则

- format 未定且会改变结构时，`ai-drama-format-strategist` 优先于 Story/Writer。
- Story/episode plan 未接受时，Scene Writer、Director、Visual 不得拥有上游 canonical 决策。
- StyleLens、Continuity、Producer 可以作为约束，但不得与 primary writer 竞争 artifact ownership。
- 跨阶段不等于同时运行所有 Skill；先输出有序 stage plan，再逐阶段解析。
- production/cost/rights blocker 不能被创作质量分或用户一句“继续”覆盖。

## 交互模式

- `guided_conversation`：提案、解释、结构化草稿和确认。
- `assisted_batch`：用户确认阶段后，运行有界候选、评估、导入和异常恢复。
- `unattended_batch`：只有明确授权、预算、质量、权限和异常策略冻结后才允许；Skill 激活仍不得在活动 run 中热切换。
