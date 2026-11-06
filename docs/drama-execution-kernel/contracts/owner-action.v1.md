# C1 — `yeisme.owner_action.v1`（跨 owner 动作收据）

> 状态：**设计合同，待 owner 侧实现**。不得由 agent 手写 receipt 文件；receipt 由 owner CLI 的 `--json` / `--agent` 输出产出。

## 目的

把远程 CLI、MCP、控制中心三种入口统一成「提交一个已冻结动作」，而不是「转发任意命令」。解决 `agent/scaena/docs/commands/remote.md` 里 `REMOTE_PROFILE_UNSUPPORTED_COMMAND` 造成的远程生产写入口缺口，以及 Eikona / Scaena / 控制中心三套状态口径不一致。

## 依赖的现有合同

- root `openspec/specs/remote-media-service-access`：stable run/operation ref、status、`event cursor`、cancel / reconcile、idempotency、path-free artifact grant；
- root `openspec/specs/owner-hosted-remote-profile`：secret-free remote profile sidecar，每个 owner 各自 `remote connect`，**拒绝统一跨 domain 网关**；
- `docs/workflows/ai-native-cli-output-contract.md`：统一 envelope 与 `--agent` / `--json` / `--events`；
- `eikona.asset_handoff.v2`：path-free refs、`permission: handoff_candidate`、lineage / evidence refs。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `schema_version` | string | 固定 `yeisme.owner_action.v1` |
| `action_id` | string | owner 签发的稳定 id；跨 Eikona `run_id` / Scaena `submission_ref` / 控制中心 `revision` 唯一映射键 |
| `owner` | enum | `auctra \| scaena \| eikona \| aigora` |
| `eu_id` | string | 对应 [execution-units.md](../execution-units.md) 的 EU id |
| `plan_ref` | string | 冻结计划 ref（path-free） |
| `plan_sha256` | string | 冻结计划内容摘要；漂移即拒绝 |
| `scope_digest` | string | 绑定 project / ProductionGraph version / shot / model / 数量 / 原文摘要与用户授权原文 |
| `idempotency_key` | string | 非空；沿用原 key，UNKNOWN 不换 |
| `confirm_receipt` | object | `{actor, mode, granted_at, raw_authorization_ref}`；`actor` 必须 human 时才允许 A6 跃迁 |
| `mutation_attempted` | boolean | 供 UNKNOWN 恢复判断；只有 `false` 且有原账本证据才允许 `--continue-not-sent` 语义 |
| `outcome` | enum | `ACCEPTED \| COMPLETED \| BOUND \| REVIEWED \| TERMINAL_REJECTED \| UNKNOWN \| PARTIAL` |
| `readback_ref` | string | 权威回读 ref；`COMPLETED` 必须有 |
| `event_cursor` | string | owner 事件流位置（Eikona `eikona events tail` 的 NDJSON 位置 / Scaena `workflow status` 位置） |
| `next_actions` | array | owner 给出的下一步命令提示，不替代调用方判断 |
| `error` | object? | 统一 envelope 的 `{code, message, suggestion}` |
| `capability_id` | string | `image_generation.v1` / `video_generation.v1` / `audio_generation.v1`；一个动作只属一个 `GenerationCapability<kind>` |
| `kind` | enum | `image \| video \| audio` |
| `binding_ref` | string | 实际选用的 `GenerationBinding` + 选择理由（可用性 / 成本 / 延迟 / 审计）；`surface` 只是标签，不是流程分支 |
| `retry_used` | int | 已用重试次数；上限来自 `ApprovalWindow.retry_budget`（默认 2）；只读 `reconcile` / `discover` 不消耗 |
| `approval_ref` | string | 本次 `ApprovalWindow` 的 `FrozenRef`；越界必须重新审批 |

见 [capability-abstraction.md](../capability-abstraction.md)：`GenerationIntent` / `GenerationCapability<kind>` / `GenerationBinding` / `GenerationReceipt` 四个对象、三类合同、有界重试与审批窗口。

## 不变量

1. 一次 `--confirm` 只覆盖一个 `(action_id, plan_sha256, scope_digest, idempotency_key)`；任一漂移拒绝。
2. `ACCEPTED` 只代表返回了稳定 ref；`COMPLETED` 必须有 `readback_ref`；`UNKNOWN` 不得写 `COMPLETED`。
3. `UNKNOWN` 之后只允许 `reconcile` 读原 `action_id`；不换 key、不换模型、不新建 state 路径、不换 owner。
4. artifact 交付使用 path-free `eikona://` URI 与短期 capability URL，不暴露 host filesystem path 或 runstore path。
5. 响应统一 `ai-native-cli-output-contract` envelope；命令特有数据放 `data`，不新增顶层字段。
6. 不返回 provider key、Authorization header、raw provider payload、private prompt 或全链路推理。
7. 换 `GenerationBinding` 不得增加权限：`cost_gate` / `IdempotentGrant` / 幂等 / 回读 / 脱敏在 Capability 层；`planned|readonly|unavailable` 一律 fail-closed。
8. 一次 `ApprovalWindow` 绑定 `(capability_kinds[], intent_digest, binding_allowlist, count, cost_ceiling, retry_budget)`；窗口内全自动，越界重新审批。
9. 可重试错误在 `retry_budget`（默认 2）内自动重试，且每次保持同一 `action_id` / `idempotency_key` / `intent_digest` / `approval_ref`；UNKNOWN 写、已 `ACCEPTED`、业务/权限/语义拒绝、创意输入变化禁止重试；`reconcile` 只读不消耗预算；耗尽交 `needs_decision`。

## 恢复决策表

| 观测 | 恢复动作 |
| --- | --- |
| `COMPLETED` + `readback_ref` 一致 | 无动作，进入下游 EU |
| `TERMINAL_REJECTED` | 交回判断职责，不自动重试 |
| `UNKNOWN` / 超时 / 断线 | `reconcile` 只读原 `action_id`；无稳定 id 时报告缺证据 |
| `mutation_attempted=false` 且原账本完整 | 沿用原 `idempotency_key` 的未发送续行语义；不生成新 action |
| `PARTIAL` | 由新的冻结计划续做，不重发已完成动作 |

## 落点

- Eikona：`eikona serve` 的 `/api/v1`，复用 service key / scope / readiness 十维；
- Scaena：`scaena-api serve` 的 typed action 路由（当前 v1 slice 未覆盖生产写，需新增）；
- 控制中心：`yeisme.work_queue.v1` 的 `revision` 去重与 `yeisme.control_center.launch_context.v1` 只消费 `action_id`；Preview 仍不产生 Owner 写入。
