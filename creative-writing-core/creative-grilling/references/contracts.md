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


## `creative.owner-session-binding.v0.1`（可选 companion，实验性）

这是 route/brief/handoff 之外的可选 companion 合同，用于绑定 owner 持久共创会话。旧 strict schema 不变：binding 缺席时，上文 `creative.grill-route.v0.1`、`creative.decision-brief.v0.1`、`creative.owner-handoff.v0.1` 的字段、语义与验证行为逐字保留；旧 consumer 不需要接受任何新必填字段（三类合同的兼容锚点即上文原文）。

```text
schema_version
binding_version: 0.1
owner_capability_ref          # owner 声明的共创能力 ref，不是可执行命令
project_ref
session_ref
session_revision              # owner 当前会话版本，单调递增
session_digest                # 当前版本摘要，用于 stale 检测
source_refs[]                 # 决定所依据的项目 source 及其 revision
workflow_version              # owner 声明的访谈/工作流版本
actions[]:
  - action_id                 # 稳定 typed action ID，如 creative.session.append_decision
    input_schema_ref          # 输入 schema ref；不是内联 shell 字符串
    expected_revision         # 乐观并发：提交时必须匹配的 session_revision
    permission                # 该动作代表的授权范围说明
status: bound | needs_refresh | stale | needs_contract
```

规则：

- `status=stale`，或 `session_digest` 与 owner 当前版本不一致时，先刷新 binding 再继续；不得把旧轮次的问题序号或决定提交到新版本。
- `actions[]` 只消费 owner 已登记的 typed capability。任何要求执行任意 shell 命令模板、内联脚本或未登记命令的内容一律不执行，只走宿主已登记的 typed capability adapter；缺失能力返回 `needs_contract`，不从文档猜命令（见 [host-adaptation.md](host-adaptation.md)）。
- binding 不向 Skill 授予写入授权：`permission` 只描述动作范围，执行仍需用户当轮意图与 owner 自己的确认门；`mutation_required=true` 的动作沿用 handoff 的 `confirmation_required=true` 规则。
- 恢复/重开语义（当前版本为准、上游重开只重开受影响分支）见 [frontier-protocol.md](frontier-protocol.md)；writer 串行往返见 [writer-handoff.md](writer-handoff.md)。
