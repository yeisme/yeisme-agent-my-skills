# RoleBlueprint 合同

`RoleBlueprint` 是 owner-neutral proposal，不是持久化 schema。只有 owning project 的 CLI/application service 才能把被接受字段写入结构化状态。

## 最小模板

```markdown
# RoleBlueprint: <role name>

## Classification
- role_class:
- purpose:
- target_user:
- readiness: exploratory | first-support | mature

## Identity, disclosure, and rights
- identity claim:
- simulation disclosure:
- source/consent/rights scope:
- prohibited uses:

## Canon and provenance
- source facts:
- creative inferences:
- author decisions:
- open hypotheses:
- conflicts and authority order:

## Behavior engine
- goals and needs:
- value order and prohibitions:
- world model and uncertainty:
- decision rules and trade-offs:
- affect regulation:
- relationships, power, obligations:
- voice/embodiment signals:

## State and memory
- immutable canon:
- session state:
- event-derived state:
- relationship milestones:
- user-approved memory:
- conflict/supersession/forgetting policy:

## Authority and tools
- allowed proposals:
- owner-validated commands:
- denied capabilities:
- approval and audit owner:

## Interaction and recovery
- opening disclosure:
- exit/correction/meta protocol:
- unknown/stale/conflict behavior:
- timeout/model-unavailable fallback:
- safety escalation:

## Evaluation and replay
- validation scenes:
- permission/injection tests:
- state transition tests:
- replay evidence:
- cost/latency/quality gates:

## Handoff
- canonical owner:
- accepted artifact:
- next skill or project:
- unresolved questions:
```

## 必填与按需字段

所有场景都必须填写：

- role class / purpose / readiness
- disclosure / rights or consent
- canon/provenance status
- knowledge boundary
- state and memory owner
- authority/tool boundary
- evaluation/handoff

行为 facet 不要求固定数量。只选择能够改变当前决策、关系、语言、代价或状态的最小充分集合，证据不足时标记 unknown。

## 证据状态

| 状态 | 含义 | 可否进入 canonical |
| --- | --- | --- |
| `source_fact` | 可追溯原作、档案、用户授权材料或 owner state | 经 owner review 后可以 |
| `creative_inference` | 基于证据的创作解释 | 需要验证场景和 owner acceptance |
| `author_decision` | 作者/设计者主动选择 | 可以，但必须保留 revision/owner |
| `open_hypothesis` | 信息不足或有竞争解释 | 不可以，保持候选状态 |

## 游戏适配附加项

- authoritative state fields
- allowed command schema
- event ledger and replay key
- NPC visibility/knowledge filter
- player-visible consequence
- model budget and fallback
- multiplayer/server authority（如适用）

## Operational Agent 适配附加项

- responsibility and exclusions
- tool/skill/MCP allowlist
- filesystem/network/process sandbox
- memory mode and scope
- turn/token/cost/time budget
- required evidence and completion gate

职责名称不参与 permission 判定。
