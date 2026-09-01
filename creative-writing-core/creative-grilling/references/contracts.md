# 创作 Grilling 实验性合同

这些合同是 Skill 的聊天/handoff 输出，schema 均为 experimental `v0.1`。它们不修改现有 `CreativeRoutePlan`、`DramaRoutePlan` 或 owner API。

## `creative.grill-route.v0.1`

```text
schema_version
entry_skill
domain: generic | novel | manga_drama | ai_drama | adaptation
project_mode: projectless | auctra | scaena | cross_owner
depth: quick | standard | deep
phase
target_artifact
domain_skill
owner_adapter?
missing_inputs[]
loaded_skills[]
status: ready | needs_input | missing | blocked
next_action
```

领域明确时不得询问路由问题。只有两个以上 domain 仍同样可信且会改变访谈图时，才允许一个路由澄清问题。

## `creative.decision-brief.v0.1`

```text
schema_version
goal
domain
project_mode
project_ref?
depth
phase
target_artifact
decisions[]: id, title, status, choice, rationale, tradeoff, reopen_condition?
facts[]: source_ref, summary, confidence, freshness
hypotheses[]: test_kind, target_artifact, success_signal, owner
constraints[]
non_goals[]
gates[]
handoff_owner
readiness: ready_for_handoff | needs_evidence | needs_decision | blocked
```

`decisions[].status` 只允许 `decided|provisional|reopened`。未解决节点必须进入 hypotheses、gates 或 readiness，不得被省略。

## `creative.owner-handoff.v0.1`

```text
schema_version
owner: auctra | scaena | creative-writing-router | ai-drama-router
source_digest
project_ref?
allowed_actions[]
next_command?
mutation_required: true | false
confirmation_required: true | false
status: ready | needs_contract | needs_input | blocked
```

当 `mutation_required=true` 时，`confirmation_required` 必须为 `true`。命令必须来自 owner 当前真实 CLI；缺少能力时返回 `needs_contract`，不得编造命令。

