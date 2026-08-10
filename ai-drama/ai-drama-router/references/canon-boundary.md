# Canon Boundary Reference

AI Drama Skills 只消费和产生带版本的 refs、proposal 与 evidence，不拥有剧本、资产或生产状态。

## Owner map

| 内容 | Canonical owner | Skill 可做的事 |
| --- | --- | --- |
| story world、beat、character state、screenplay revision | Auctra / Dramaturge | 读取 revision，提出新 proposal 或 handoff |
| PanelRun、JudgeTask、receipt、adjudication | Ordo | 提交有界任务，读取结果和恢复证据 |
| visual artifact、subject/style/reference version | Eikona | 生成 visual brief、candidate proposal、评估请求 |
| ProductionGraph、production acceptance、assembly、delivery | Scaena | 请求状态转换，读取 gate 结果和交付证据 |
| Skill routing、rubric guidance、director principles | Skills source | 维护执行指导，不写业务事实 |

## Boundary rules

- 每个 handoff 必须携带 `owner`、`revision`、`digest`、`scope`、`created_at` 和来源 evidence ref。
- 任一输入 revision、subject/style version、权限、preflight 或生产状态改变后，依赖它的 proposal、score 和 recommendation 必须标记 `stale`，不能继续晋级。
- Skill 不得直接覆写 canonical screenplay、ProductionGraph、asset bytes 或 production acceptance；必须调用所属 Owner 的 typed action。
- 聊天 transcript、模型记忆和未落 receipt 不能作为事实来源或交付依据。

完整字段和状态合同以根级及 Owner OpenSpec 为准：

- `openspec/changes/ai-drama-skills-governance-v1/`
- `agent/ordo/openspec/changes/ordo-ai-drama-panel-run-v1/`
- `cli/auctra/openspec/changes/auctra-ai-drama-story-handoff-v1/`
- `cli/eikona/openspec/changes/eikona-ai-drama-visual-judge-v1/`
- `agent/scaena/openspec/changes/scaena-ai-drama-production-gate-v1/`
