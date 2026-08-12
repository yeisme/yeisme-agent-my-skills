---
name: ai-drama-router
description: Use when a user asks to create, adapt, evaluate, reroll, storyboard, style-reference, produce, review, or hand off an AI drama or manga-drama project and the narrowest task-role Skill, originality constraint, owner, or next production stage must be selected.
---

# AI Drama Router

## 目标

把“做剧”请求路由到最小、最明确的创作 Skill 和 Owner action。先判断用户意图和当前 artifact 状态，再决定 primary skill、最多一个兼容约束 skill、下一步和阻塞原因。

## 路由流程

1. 读取 `references/canon-boundary.md`，识别目标：新故事、人物、分集、导演设计、视觉候选、评估修复、生产运行、连续性或交付。
2. 读取已有的 `CanonSnapshot`、revision、digest、当前模式和最近 blocker；缺失时只提出最小补充问题。
3. 用户点名导演、作品、流派、情绪或视觉风格时，先调用 `creative-style-lens-builder` 生成原创 `StyleLens`；人名只保留在 source refs，不把 persona identity 传给 writer。
4. 选择一个 primary Skill；只有确有输入依赖时再加一个 compatible constraint Skill。
5. 生成阶段计划：输入 refs、StyleLens、输出 proposal、验收、Owner handoff、下一动作。
6. 在 provider call、主体冻结、canonical 修改或 production acceptance 前停在对应 gate。

## 默认路由

| 用户意图 | Primary Skill | 兼容约束/Owner |
| --- | --- | --- |
| 一句话想法、主题、冲突、故事结构 | `ai-drama-story-architecture` | `ai-drama-character-engine` |
| 角色动机、秘密、关系、行动模拟 | `ai-drama-character-engine` | `ai-drama-continuity-supervisor` |
| 季度/多集/单集规划 | `ai-drama-showrunner` | `ai-drama-story-architecture` |
| 把情绪变成场面、调度、镜头 | `ai-drama-director` | `ai-drama-visual-language` |
| 点名导演/作品/流派风格、混合风格或反风格 | 当前 artifact 对应的 Story/Director/Visual/Writer | `creative-style-lens-builder` |
| Blender/动作/相机参考视频、Seedance `reference_video` 入参 | `ai-drama-video-reference-director` | `ai-drama-continuity-supervisor` |
| Eikona 抽卡、主体、镜头视觉方案 | `ai-drama-visual-language` | `ai-drama-continuity-supervisor` |
| 多候选评分、争议、选优、修复 | `ai-drama-critic-panel` | `ai-drama-producer` |
| 时间线、服装、道具、空间、动作不一致 | `ai-drama-continuity-supervisor` | `ai-drama-director` |
| 节奏、剪辑、声音、字幕和 assembly | `ai-drama-edit-and-sound` | `ai-drama-continuity-supervisor` |
| 成本、权限、预算、批次和异常 | `ai-drama-producer` | `ai-drama-critic-panel` |
| Ordo/Scaena 运行、暂停、恢复、handoff | `ai-drama-production-orchestrator` | `ai-drama-producer` |

## 输出

返回一个简短的 routing plan：`goal`、`phase`、`artifact`、`primary_role`、`primary_skill`、`compatible_skill`、可选 `style_lens`、`input_refs`、`missing_inputs`、`gates`、`owner_action`、`next_action`。不要在 router 内代写完整剧本或绕过 owner。

## 边界

- 不把自然语言理解编码进 shell；由 agent 读取 Skill 描述后选择。
- 不同时激活一组互相竞争的 writer；canonical 文本由 Auctra 维护。
- 不复制导演/作品 persona skill 的身份卡、表达 DNA、典型片段、专名、台词、口头禅或独特桥段；风格参考必须维度化并带原创性约束。
- 不让“继续”自动等价于付费调用、接受资产、冻结主体或导出。
- 没有版本、权限、成本或生产策略时，输出 `needs_input`/`needs_contract`。

## 验证

```bash
cd /workspaces/yeisme-agent
scripts/skills.sh search "AI drama story director critic continuity production"
scripts/skills.sh resolve ai-drama-router
scripts/skills.sh resolve creative-style-lens-builder
scripts/skills.sh validate-custom
```
