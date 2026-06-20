# 中文小说章节验收门禁

## 使用时机

当章节候选稿需要在进入修订、Auctra review、导出或发布前做单章验收时读取本文件。它关注“这一章是否完成可交付目标”，不替代整书结构修订，也不直接重写正文。

## 验收总表

| 维度 | pass | needs_revision | blocking |
| --- | --- | --- | --- |
| 章节目标 | 本章目标在正文中被行动或发现兑现 | 目标兑现但弱，读者感知不清 | 本章目标缺失或与大纲相反 |
| 冲突升级 | 冲突压力、代价或选择比章首更强 | 有冲突但无明显升级 | 全章空转，状态未改变 |
| 信息增量 | 新事实、线索、规则或误导清晰可追踪 | 信息存在但埋得过散或无引用 | 没有新增信息，或与台账冲突 |
| 人物推进 | 人物选择、关系、信念或资源状态变化 | 人物变化弱，需要强化动作后果 | 人物行为违背已确认设定 |
| 连续性 delta | 新增事实、伏笔、知识边界可入台账 | delta 不完整，需要补字段 | 出现时间线、知识边界或伏笔矛盾 |
| 章尾钩子 | 钩子可被下一章偿还，承诺明确 | 钩子有但承诺模糊 | 钩子虚假、不可偿还或剧透越界 |
| 类型回报 | 符合主类型读者承诺，有阶段爽点或情绪回报 | 回报不足，需要补场景或转折 | 章节背离类型契约，读者预期被破坏 |

## 验收报告模板

```markdown
## 章节验收

- chapter_id:
- chapter_goal:
- verdict: pass | needs_revision | blocking | deferred
- confidence: high | medium | low

### 分项判定

| 维度 | 判定 | 证据 | 问题 | 最小修复动作 | owner_skill |
| --- | --- | --- | --- | --- | --- |
| 章节目标 |  |  |  |  |  |
| 冲突升级 |  |  |  |  |  |
| 信息增量 |  |  |  |  |  |
| 人物推进 |  |  |  |  |  |
| 连续性 delta |  |  |  |  |  |
| 章尾钩子 |  |  |  |  |  |
| 类型回报 |  |  |  |  |  |

### continuity_delta

- facts_added:
- character_state_changes:
- relationship_changes:
- foreshadowing_seeded:
- foreshadowing_paid:
- knowledge_boundary_changes:
- unresolved_questions:

### risk_flags

- target_missing
- conflict_flat
- information_empty
- character_static
- continuity_conflict
- hook_unpayable
- spoiler_boundary_crossed
- style_or_dialogue_issue

### handoff

- next_owner:
- required_reference:
- smallest_next_action:
```

## 分级规则

- `blocking`：章节目标缺失、连续性冲突、人物违背设定、钩子不可偿还、重大剧透越界。这类问题未修前不能称为可发布稿。
- `needs_revision`：目标可见但力度不足、信息释放不清、人物推进弱、章尾钩子模糊、类型回报不足。可进入修订，不应导出。
- `deferred`：问题存在但不影响本章交付，且有明确后续章节偿还点，例如支线伏笔暂不解释。
- `pass`：核心目标完成，无 blocking，needs_revision 项不影响当前交付。

## Owner skill 映射

- 结构和多轮修订：`chinese-novel-revision-producer`
- 时间线、知识边界、伏笔冲突：`chinese-novel-continuity-editor`
- 留存、章尾钩子、冲突升级：`chinese-novel-hook-pacing-editor`
- 人物行为或关系推进：`chinese-novel-character-architect`
- 对白功能和潜台词：`chinese-novel-dialogue-editor`
- 文风、节奏句式、AI 味：`chinese-novel-style-polisher`

## 验收检查

- 每个判定必须有章节证据，不能只写抽象评价。
- 每个 blocking 必须有最小修复动作和 owner skill。
- 连续性 delta 必须能被项目圣经或台账吸收。
- 章尾钩子必须写明下一章如何偿还。
- 如果缺少大纲、项目圣经或上一章上下文，结论降为 medium/low confidence，并列待补问题。
