# 抽象设计（DEK v1）

> 本文的抽象不是新造能力，而是把现有做剧工具里已经实现的合同**统一命名并固定不变量**。所有「真实承载」都能在当前仓库的 CLI 文档或代码里查到。

## 六个抽象 + 一条调度律

| ID | 抽象名 | 真实承载 | 统一不变量 |
| --- | --- | --- | --- |
| A1 | `FrozenRef`<br>冻结引用 | Scaena `frozen intent ref/digest`、`frozen spec ref/digest`、`validated bundle ref/digest`（`scaena-production-operator/references/workflow.md:140`）；Eikona `artifact.sha256` / `binding_digest`（`eikona.asset_handoff.v2`）；Auctra `canon_digest`（`auctra.production_handoff.v1`）；`creative.owner-handoff.v0.1` 的 `source digest` | 跨 owner 交接只传 `ref + digest`，不传 bytes / 绝对路径 / provider payload；digest 变化 → 依赖它的 proposal、score、recommendation、handoff 标 `stale`（`ai-drama-router/references/canon-boundary.md` 已定义） |
| A2 | `CapabilityInvocation`<br>单一写者 + 单一作用 | Scaena `ProductionGraph` / `workflow run` / `video task`；Eikona `run` / `artifact` / `assets`；Auctra `canonical screenplay`；`GenerationCapability<kind>`（`image\|video\|audio`） | 一个 canonical state 只有一个 owner；一个动作 = 一次 Capability 调用，流程不感知 `cli/mcp/http/sdk` 等 binding；`remote profile` 与 `--no-remote` 都不改变 owner；判断由 `DramaRoutePlan.stage_plans[]` 决定，写入由 owner capability 执行。见 [capability-abstraction.md](capability-abstraction.md) |
| A3 | `Outcome`<br>结果代数 | `unknown_accept`、`submission_ref`、`reconcileVideoProviderTask`（`scaena-production-operator/references/official-routing.md`）；Eikona `queued\|running\|awaiting_review\|completed\|failed\|cancelled`、`replacement_status: not_applied\|staged\|applied`、`permission: handoff_candidate`；控制中心 `complete\|partial\|pending\|unknown\|not_recorded\|forbidden\|unavailable\|expired\|integrity_failed\|needs_contract` | `ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED ≠ PRODUCTION_ADMITTED ≠ EXPORT_READY`；UNKNOWN 只读 reconcile，不换幂等键、不换模型、不创建替代任务 |
| A4 | `IdempotentGrant`<br>幂等授权 | `eikona review decide --expected-version 0 --idempotency-key OPERATION_KEY --confirm --agent`；Scaena 执行前「non-empty idempotency key」；`input.prepare` 单一稳定 key；`--confirm --budget-ok --quota-ok` | 一次 `--confirm` 绑定一个 `(operation_key, expected_version, digest, scope)`；scope / digest 漂移拒绝；动作与确认分离；控制中心 Preview allowlist 不产生 Owner 写入 |
| A5 | `LineageReuse`<br>内容寻址复用 | `eikona://artifact/<handle>`、`lineage_refs`、`evidence_refs`、`eikona events rebuild <run_id> --json`；`eikona assets import-anatomia`（refs-only + package sha256 + lineage ledger + 同 ref 去重）；`scaena asset draw record --digest sha256:<64-hex>` | digest 相同 → 复用 / 去重，不重生成；只失效依赖闭包；`eikona rollback` 是技术回滚，不等于验收通过 |
| A6 | `HumanGate`<br>人工跃迁 | `scaena asset draw select --actor <human-actor-ref>` / `freeze --confirm`；`eikona review decide --confirm` | actor 必须 human；自动 `frozen` / 自动 `accepted` 在状态机上不可达；`selected ≠ frozen ≠ production_admitted` |
| B1 | `WaveBatch`<br>依赖波次批 | `scaena asset draw plan --wave N --requires <frozen-slot-ref>`；`scaena workflow resume / repair plan / repair run`；`eikona events tail <run_id> --json` | 上游未 `frozen` 不开下一波；先落盘再发送；统一回查；写入预算与只读回查分账 |

## 不变量总图

```text
ai-drama.route-plan.v1 (ai-drama-router, 只读语义路由)
   │ stage_plans[] / gates[] / canonical_owner / owner_action
   ▼
FrozenRef (A1) ──绑定──► IdempotentGrant (A4) ──签发──► CapabilityInvocation (A2)
                                                          │ 执行（owner 侧）
                                                          ▼
                                     Outcome (A3) + receipt + event_cursor
                                                          │
                ┌─────────────────────────────────────────┼──────────────────────┐
                ▼                                         ▼                      ▼
        LineageReuse (A5)                          HumanGate (A6)           WaveBatch (B1)
     digest 相同复用 / identity-equal 快路径       人工跃迁不可自动化        波次 / 预算 / 统一回查
```

## 三条硬不变量

1. **判断与写入分离**：`DramaRoutePlan` 与 `creative.owner-handoff.v0.1` 只产出「允许动作 + next command + mutation/confirmation 状态」；任何 owner state 只由该 owner 的受控 CLI 入口写入。skill 不手写 `.scaena` / SQLite / manifest / receipt。
2. **一次动作一个 receipt**：receipt 至少含 `action_id, plan_ref, plan_sha256, scope_digest, outcome, readback_ref, event_cursor`，统一使用 `ai-native-cli-output-contract` 的 envelope（`spec_version / mode / command / status / summary / facts / actions / evidence / confidence / data / error`）；`--agent` 用于常规自动化，`--json --compact` 用于脚本/CI，`--events` 用于长任务。
3. **UNKNOWN 单调**：`unknown_accept` 之后只允许 `reconcile` 读原 `submission_ref`；任何「重试」必须证明 `mutationAttempted=false` 且沿用原幂等键，不允许换 run-dir / state 路径 / 模型重发。

## 词汇映射（消除跨 owner 口径漂移）

| 统一词 | Eikona | Scaena | 控制中心 | Auctra |
| --- | --- | --- | --- | --- |
| `FrozenRef` | `artifact.sha256` / `binding_digest` | `frozen intent/spec/bundle ref+digest` | `revision` / `source` | `canon_digest` / `source_revision` |
| `Outcome.ACCEPTED` | `run` 已创建 / `awaiting_review` | `submission_ref` 已返回 | `pending` | — |
| `Outcome.COMPLETED` | `run.completed` | 视频任务终态成功 | `complete` | — |
| `Outcome.BOUND` | `replacement_status: applied` | `asset subject bind` 回读 | — | — |
| `Outcome.REVIEWED` | `feedback_status` / `review decide` | `production review` | — | `accepted handoff` |
| `Outcome.UNKNOWN` | `awaiting_review` 不等于完成 | `unknown_accept` | `unknown` / `not_recorded` | — |
| `event_cursor` | `eikona events tail <run_id> --json` | `workflow status` / `submission_ref` | 签名 `cursor` / `revision` 去重 | — |

## 与上一轮「糯米包抽象」的关系

上一轮从外部技能包里剥离领域名词后得到的 6 个抽象，在**本设计中全部改用现有工具的真实词汇重新表达**：

| 外部抽象 | 本设计 |
| --- | --- |
| FrozenIntentChain | `FrozenRef` + `IdempotentGrant` + receipt |
| Decider/Executor Split + Lease | `CapabilityInvocation` + `GenerationCapability<kind>` + `DramaRoutePlan.stage_plans[]` |
| Outcome Algebra / UNKNOWN | `Outcome` + `unknown_accept` / `reconcile` |
| ScopeReceipt | `IdempotentGrant` |
| Content-addressed Reuse / Identity-equal Fast Path | `LineageReuse` + `identity_equal` 判定门 |
| HumanGate | `HumanGate`（沿用 `select --actor human`） |
| Dependency-wave Batch | `WaveBatch` |

不引入外部技能包的任何角色名、脚本名、模型白名单或平台 CLI 术语。

## 能力 / 绑定分离（v2 扩展）

A2 从「按入口分流的动作」收敛为「按能力调用的动作」：**只要能生成，就是一个作用** `GenerationCapability<kind>`（`image|video|audio`），CLI / MCP / HTTP / SDK / 本地 / 第三方只是 `GenerationBinding`。流程、门禁、调度、收据、恢复、复用全部不感知 binding。

| 新增对象 | 落点 |
| --- | --- |
| `GenerationIntent` | A1 `FrozenRef` + typed controls + A4 `IdempotentGrant` + `approval_ref` |
| `GenerationCapability<kind>` | A2 `CapabilityInvocation` 的调用目标 |
| `GenerationBinding` | 实现层，`discover()` / `adapt()` / `normalize()` / `reconcile()`；`surface` 只是标签 |
| `GenerationReceipt` | A3 `Outcome` + `binding_ref` / `retry_used` / `approval_ref` / `event_cursor` |

三条新增不变量：

1. **换 Binding 不增加权限**：成本、授权、幂等、回读、脱敏在 Capability 层；
2. **一次审批 = 一个自动化窗口**：窗口内全自动（含 `retry_budget=2` 的自动重试、自动选 binding），越界重新审批；UNKNOWN 只 `reconcile`，不消耗重试预算；
3. **等价准则四条**：同一 Intent / 同一 Receipt 形状 / 同一授权与脱敏 / 可被同一 `reconcile` 恢复，与协议和产品无关。

完整三类合同（`image` / `video` / `audio` 的 operations、typed controls、真实入口、约束源、receipt 锚、特有门禁）、能力发现矩阵、重试规则与 `ApprovalWindow` 见 [capability-abstraction.md](capability-abstraction.md)。A1 / A3 / A4 / A5 / A6 / B1 与 C2 / C3 均不变。
