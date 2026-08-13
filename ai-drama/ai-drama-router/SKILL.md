---
name: ai-drama-router
description: Use when a user asks to create, adapt, develop, write, evaluate, reroll, storyboard, style-reference, produce, review, or hand off any AI drama, short-drama, manga-drama, television, film, procedural, anthology, comedy, or audio-drama project and the format matrix, minimal context pack, narrowest task-role Skill, activation decision, originality constraint, canonical owner, or next production stage must be selected.
---

# AI 做剧矩阵路由器

## 目标

作为所有“做剧”请求的唯一入口，把用户意图编译成一个可执行的 `DramaRoutePlan`。先确定剧型、类型、阶段、artifact 和上下文，再选择一个 primary Skill、最多一个 compatible constraint Skill，以及按需加载或启用决策。

Router 不代写完整剧本、不成为新的创作数据库，也不为一次任务批量安装整套 Skills。

## 参考资料

- 需要识别 canonical owner、revision 和 mutation boundary 时读取 `references/canon-boundary.md`。
- 需要按阶段和 artifact 选择工作 Skill 时读取 `references/routing-matrix.md`。
- 需要判断 active、local on-demand、persistent activation、missing 或 external install 时读取 `references/skill-resolution-policy.md`。
- 需要生成稳定输出或映射到宿主运行时计划时读取 `references/drama-route-plan-contract.md`。
- 需要校验美剧、竖屏短剧、漫剧、电影和已有剧本请求时读取 `references/route-examples.md`。

## 路由流程

1. 识别九个轴：`medium`、`format_profile`、`genre_lens`、`phase`、`artifact`、`task_role`、`evidence_state`、`canonical_owner`、`activation_scope`。
2. 剧型、单集时长、季/集形态或类型承诺不明确，且会改变结构判断时，选择 `ai-drama-format-strategist` 作为 primary；不要让 Writer 猜承载形态。
3. 读取已有 CanonSnapshot、revision/digest、当前 artifact、最近 blocker 和权限/成本状态。跨项目知识只消费宿主声明的 Owner refs 或权限感知 ContextPack，不直接遍历私有状态。
4. 根据阶段选择一个 `context_pack_profile`。除纯 intake 外，需要 owner/project 历史的工作先调用 `ai-drama-context-pack-builder` 准备最小上下文。
5. 用户点名导演、作品、流派、情绪或视觉风格时，先使用 `creative-style-lens-builder` 生成原创 `StyleLens`；人名只保留在 source refs，不把 persona identity 传给 writer/provider。
6. 选择一个 primary Skill。只有连续性、风格、生产约束或明确输入依赖需要时，增加一个 compatible constraint Skill。
7. 按 `active → resolved_local_on_demand → needs_profile_promotion → needs_install_decision` 顺序解析 Skill。一次性任务默认停在 local on-demand，不执行持久化 activation。
8. 若项目高频需要该 Skill，生成宿主无关的 `SkillActivationPlan`。宿主声明了启用适配器时可交给该适配器；未声明时只返回 proposal。没有当前用户的明确启用/安装授权时不得执行持久化变更。
9. 生成 Owner handoff、gates 和下一动作。在 provider call、canonical 修改、主体冻结、持久化 activation、production acceptance、export 或 publish 前停在对应 gate。

## 核心路由

| 用户意图 | Primary Skill | 可选约束 |
| --- | --- | --- |
| 选择短剧/漫剧/美剧/电影/音频剧形态、时长、集数和类型契约 | `ai-drama-format-strategist` | `ai-drama-producer` |
| 一句话想法、主题、冲突、beat、结尾钩子 | `ai-drama-story-architecture` | `ai-drama-character-engine` |
| 角色动机、秘密、关系、知识边界和行动模拟 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` |
| 季度、多集、pilot、单元案、A/B/C 线和长期回报 | `ai-drama-showrunner` | `ai-drama-story-architecture` |
| 可拍场景、动作、对白、潜台词和转场 | `screenplay-scene-writer` | `creative-style-lens-builder` |
| 把情绪变成表演、调度、空间、镜头和声音意图 | `ai-drama-director` | `ai-drama-visual-language` |
| Blender/动作/相机参考视频、Seedance `reference_video` 入参 | `ai-drama-video-reference-director` | `ai-drama-continuity-supervisor` |
| 主体、风格、关键帧、分镜和视觉候选 | `ai-drama-visual-language` | `ai-drama-continuity-supervisor` |
| 节奏、剪辑、声音、字幕和 assembly | `ai-drama-edit-and-sound` | `ai-drama-continuity-supervisor` |
| 多候选评分、争议、选优和有限修复 | `ai-drama-critic-panel` | `ai-drama-producer` |
| 成本、权限、预算、批次、retry 和 delivery readiness | `ai-drama-producer` | `ai-drama-critic-panel` |
| 跨故事、评估、视觉、声音和生产 Owner 运行与恢复 | `ai-drama-production-orchestrator` | `ai-drama-producer` |

## 输出

返回 `DramaRoutePlan`，至少包含：

- `goal`、`medium`、`format_profile`、`genre_lens`；
- `phase`、`artifact`、`task_role`、`context_pack_profile`；
- `primary_skill`、可选 `compatible_skill`、可选 `style_lens_skill`；
- `resolution_status`、`skill_sources`、可选 `activation_plan`；
- `input_refs`、`missing_inputs`、`canonical_owner`、可选 `owner_binding`、`gates`；
- `owner_action`、`next_action`、`status`。

复杂跨阶段请求还应输出有序 `stage_plans`；每个 stage 仍只有一个 primary 和最多一个 constraint。

## 严格失败条件

- `needs_format_decision`：承载形态不清且会改变结构。
- `needs_context`：关键 canon、人物、连续性或生产事实缺失。
- `needs_style_lens`：点名人物/作品风格但没有维度化原创约束。
- `writer_conflict`：多个 writer 声称同一 canonical artifact。
- `needs_install_decision`：本地 source 不存在，或需要外部代码/工具。
- `activation_not_authorized`：需要持久化 activation，但用户未明确授权。
- `stale`：revision、digest、permission、StyleLens、SubjectVersion 或 production constraint 已变化。
- `external_side_effect`：付费调用、生产接受、导出、发布或外部 mutation 缺少授权。

## 边界

- 不把自然语言理解编码进 shell、CLI 或宿主适配器；Agent 读取 Skill 描述和 references 后选择，宿主能力只负责确定性查找、预览、持久化、回滚和验证。
- 不同时激活一组相互竞争的 writers；canonical 文本由宿主绑定的 story owner 维护。
- 不复制导演/作品 persona skill 的身份卡、表达 DNA、典型片段、专名、台词、口头禅或独特桥段。
- 不让“继续”“一键”自动等价于外部安装、付费调用、接受资产、冻结主体、导出或发布。
- 不在生产会话中联网发现、安装、更新或热替换 Skill；已开始阶段固定 Skill lineage。

## 验证

从本 Skill 目录运行独立验证；它不依赖任何宿主仓库命令：

```bash
python3 scripts/validate_drama_matrix.py
```
