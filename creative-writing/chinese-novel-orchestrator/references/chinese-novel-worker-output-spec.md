# 中文小说 worker 输出规格

## 通用输出

- `task_brief`：本次任务目标、输入材料、不可改动约束、缺失信息。
- `draft_or_plan`：正文、表格、台账或修订方案，必须能交给下游技能继续使用。
- `continuity_delta`：新增事实、人物状态、时间线变化、道具状态、地点变化、知识边界变化。
- `risk_flags`：硬矛盾、人物越界、伏笔欠账、禁写规则、Auctra review 阻塞项。
- `handoff`：建议交给哪个技能继续处理，以及需要读取的材料。

## Auctra 轻集成

普通创作可直接输出 Markdown。只有用户明确在 Auctra 项目内工作、需要结构化 review/export、或需要保存材料时，才建议使用 `auctra text`、`auctra material`、`auctra review`、`auctra export`。不要把未 review 候选稿说成正典。
