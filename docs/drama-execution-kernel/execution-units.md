# 执行单元设计（DEK v1）

执行单元（Execution Unit, EU）是做剧流程里**一个 owner、一个写者、一个 receipt** 的最小可组合块。本文的 EU 全部由现有真实命令组成；只有标注「待补」的三处合同需要 owner 侧新增能力。

## EU 通用形状

```text
EU := {
  id             : eu.<lane>.<name>
  owner          : Auctra | Scaena | Eikona | Aigora | ControlCenter   # 一个 EU 一个 owner
  lane           : read | decide | mutate | recover
  input_refs[]   : FrozenRef {ref, digest}        # 只来自上游 EU 的 receipt
  gates[]        : IdempotentGrant | HumanGate | budget | rights | preflight
  command        : 真实 CLI 命令（--json / --agent / --events），owner 侧执行
  output         : receipt {action_id, outcome, readback_ref, next_actions, event_cursor}
  recovery       : resume / reconcile 的真实命令；UNKNOWN 不重投
  consumer       : DEK skill / 控制中心投影
}
```

约束：

- EU 之间**只传 `ref + digest`**，不传 bytes / 路径 / provider payload；
- 输出统一 `ai-native-cli-output-contract` envelope；结构化运行资产由 owner CLI 产出，agent 不手写；
- 任何 EU 的 `UNKNOWN` 只允许 `recovery` 只读，不新建 state 路径、不换幂等键；
- `remote profile` 下的 EU 由 `L-Transport` 转发到 owner 侧执行，不在客户端落 owner state。

## 领域 EU 目录（9 个）

| EU | 名称 / owner / lane | 输入 `FrozenRef` | 门禁 | 真实命令 | 输出 receipt | 恢复 |
| --- | --- | --- | --- | --- | --- | --- |
| EU-01 | `CanonIntake`<br>Scaena / mutate | `auctra.production_handoff.v1` + `canon_digest` | `--confirm` | `scaena handoff auctra inspect --project <p> --from <handoff-file> --json`<br>`scaena handoff auctra import --project <p> --from <handoff-file> --confirm --json` | import receipt、`source_project_ref` / `source_revision`、scene/action/dialogue refs | `scaena handoff auctra describe --project <p> <receipt-ref> --json` |
| EU-02 | `DrawBatch`<br>Scaena / decide→batch<br>**（C2 待补）** | `creative.owner-handoff.v0.1` + frozen slots + template digest | wave 上游 `frozen`、写入预算 | 现状逐条 `scaena asset draw plan --project <p> --asset <slot> --brief <brief-ref> --wave 1 --json`；待补一批冻结成 `scaena.draw_batch.v1` 返回 `batch_ref` + 依赖图 | `batch_ref`、`DrawSession: planned`、`wave/requires` | `scaena asset draw status --project <p> --asset <slot> --agent` |
| EU-03 | `GenerationInvoke`<br>Capability / mutate（付费）<br>`kind=image\|video\|audio` | `GenerationIntent`（`FrozenRef` + typed controls）+ `ApprovalWindow` + binding 候选表 | 一次审批窗口、`--dry-run` 预检、resolver 只选 `executable` binding | `GenerationCapability<kind>.invoke()`；image 如 `eikona generate --model openai/gpt-image-2.5-sunburst --quality high --size WxH --agent`；video 如 `scaena video generate`；audio 走 `sonora`；进度 `eikona events tail <run_id> --json` | `GenerationReceipt`（`run_ref` / `submission_ref` / audio 注册项 + path-free `artifact_ref` + `outcome` + `event_cursor` + `binding_ref` + `retry_used`） | `reconcile` 只读原 `action_id`；可重试错误按 `retry_budget=2` 自动重试 |
| EU-04 | `CandidateRecord`<br>Scaena / mutate（零 provider） | `run_ref` + `sha256` digest | digest 必填 fail-closed | `scaena asset draw record --project <p> --asset <slot> --session <draw-session-ref> --eikona-run <run-ref> --digest sha256:<64-hex> --json` | `candidate_ref`、DrawSession → `candidate_review` | `scaena asset draw status ... --agent` |
| EU-05 | `HumanSelectFreeze`<br>Scaena / human gate | `candidate_ref` | `--actor <human>` / `--confirm` | `scaena asset draw select --project <p> --asset <slot> --candidate <ref> --action accept --actor <human> --reason "<reason>" --json`<br>`scaena asset draw freeze --project <p> --asset <slot> --confirm --json` | `selected_candidate_ref`、`frozen_subject_version_ref` | 只读 `status` |
| EU-06 | `ShotBind`<br>Scaena / decide | `frozen_subject_version_ref` + `ProductionGraph ref/version` | `workflow.md:140` 完整校验 + 非空 idempotency key | `scaena production graph describe <graph-ref> --json`<br>`scaena asset subject bind --graph <graph-ref> --character <ref> --filing <id> --permission licensed --json`<br>`scaena visual pack plan --graph <graph-ref> --json` | `frozen intent ref/digest`、`validated bundle ref/digest` | `scaena workflow status <run-ref> --project <p> --agent` |
| EU-07 | `VideoSubmit`<br>Scaena→Aigora / mutate（付费） | EU-06 全部 frozen refs + `capability ref/digest/maturity` | 用户授权 + idempotency key + `duration/ratio/output/audio policy` | `scaena video model list --json` → `scaena video generate ... --json` | `ACCEPTED` receipt + `submission_ref` + `event_cursor` | `unknown_accept` → EU-08 |
| EU-08 | `Reconcile`<br>Scaena / recover（只读） | `submission_ref` | 不得换幂等键 / 模型 / 任务 | `reconcileVideoProviderTask` 查询原任务；`scaena workflow resume <run-ref> --project <p> --json`；`createArtifactAccessGrant` 下载 | 终态 `COMPLETED` / `FAILED`，保持 `pending_review`、`export blocked` | 原 `submission_ref` 只读查询 |
| EU-09 | `BoundedReplace`<br>Eikona（写）+ Scaena（绑定）<br>**（C3 待补）** | `old_ref` / `new_ref` + 三份 `sha256` provenance + `field_plan` / `audio_plan` + `claim_key` | **`identity_equal` 判定门** + `--yes` + 当前文件 hash 校验 | `eikona assets stage <handle> --to <path> --json`<br>`eikona assets handoff <asset_handle> --agent`<br>`eikona replace <artifact_id> --project current --to <path> --yes --json`<br>`eikona rollback <replacement_id> --json` | `replacement_status: applied`、`replacement_id`、`binding_digest` | `eikona rollback <replacement_id> --json` |
| EU-31 | `FailedRepair`<br>Scaena / recover | 终态 `FAILED` + 原 `submission_ref` + 原配置全等 | 只有 FAILED 可重提；共享 `claim_key` | `scaena workflow repair plan --run <run-ref> --json`<br>`scaena workflow repair run --repair <repair-ref> --json` | 新 attempt receipt，保留原 / 后继 ref | `reconcile` 原任务 |

**EU-03 的三类 kind**：`image`（Eikona，`eikona://artifact/<handle>` + `asset_handoff.v2`）、`video`（Scaena/Aigora，`submission_ref` + `pending_review`，须有 `ShotAudioIntent`）、`audio`（Sonora，`audition` 审听 + `final_mix`，`video_native` 缺证据时降级补配）。三类的 operations / typed controls / 约束源 / 特有门禁见 [capability-abstraction.md](capability-abstraction.md#二三类合同)。EU-03 **不按 `cli/mcp` 分流**：resolver 自动选 `executable` binding，选择理由写入 `receipt.binding_ref`；`retry_budget=2` 内自动重试，UNKNOWN 只 `reconcile`。

> 装配与交付沿用现成链，不另设 EU：`scaena quality check` / `continuity check` / `edit plan|timeline|render|select` / `scaena export package ... --confirm --json`。

## 两个横切层（每个 EU 都经过）

| 层 | 解决 | 现状 / 待补 |
| --- | --- | --- |
| **L-Transport `RemoteAction`**（G1） | 远程 CLI 与控制中心只提交 `OwnerAction{plan_ref, plan_sha256, scope_digest, idempotency_key, confirm_receipt}`，owner 侧执行对应 EU 并返回统一 receipt | 现状：`eikona serve --addr ... --api-key-file ...`（`/api/v1`）、`eikona remote connect`、`scaena-api serve --config ...`、`scaena remote connect --endpoint ... --key-file ... --project ...`。**待补**：`agent/scaena/docs/commands/remote.md` 明确 v1 slice 只路由 `remote / upload / mcp / doctor / board`，本地生产写在 remote profile 激活时返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`；需要 `scaena-api` 的 typed action 路由（C1）。**不建跨 owner 网关**：Eikona 与 Scaena 各自执行自己的 EU |
| **L-Projection `ProjectionAlign`**（G2） | receipt 的 `action_id + event_cursor + revision` 成为控制中心唯一事实源，消除三层各读一次 | 现状：`yeisme.work_queue.v1`（签名 cursor、按 `scope/owner/object/source/revision` 去重）、`yeisme.creative_flow.v1` 五阶段 rail、`yeisme.drama_episode.v1`、`yeisme.control_center.launch_context.v1`、45s 缓存与 `cache: hit/miss/refresh_limited`。**待补**：把 Eikona `run_id` / Scaena `submission_ref` / 控制中心 `revision` 映射到同一 `action_id`；控制中心 Preview allowlist 保持「不代表 Owner 已写入」 |

## 编排 DAG

```text
EU-01 CanonIntake
   │ ProductionGraph ref/version + canon_digest
   ▼
EU-02 DrawBatch ──► EU-03 CandidateGenerate ──► EU-04 CandidateRecord ──► EU-05 HumanSelectFreeze
   │ wave/requires, 先落盘再发送      (eikona events tail)     (digest, 零 provider)      (human-only)
   │                                                                                       │
   │ 同 digest 候选 ─────────── A5 LineageReuse 快路径 ────────────────────────────────────┤
   │                                                                                       ▼
   └───────────────────────────────────────────────────────────► EU-06 ShotBind (frozen intent/spec/bundle)
                                                                        │
                                                                        ▼
                                             EU-07 VideoSubmit ──► EU-08 Reconcile ──► export package
                                                (submission_ref)      (unknown_accept 只读)
                                                     │
                                  FAILED 且配置全等 ──► EU-31 FailedRepair（共享 claim）
                                                     │
                          identity_equal 替换 ──► EU-09 BoundedReplace（+ eikona rollback）
                                                     │
                          任一创意字段变化 ──► 退回 EU-06 新创作批（新 idempotency key）
```

## 三个场景的 EU 组合

| 场景 | 组合 | 直接收益 |
| --- | --- | --- |
| 生图抽卡 | `EU-02 + 03 + 04 + 05`，经 `L-Transport` 远程提交；命中已选候选走 `A5` 快路径到 `EU-09` | N 次往返 → 1 次 `batch_ref` + `eikona events tail` 事件流；template digest 漂移发送前拒绝 |
| 资产管理 | `EU-01 + 05 + 06 + 09`，全程 `FrozenRef`，`binding_digest` 管复用 | digest 未变不重生成；`ProductionGraph` 反向查替换影响面；`permission: handoff_candidate` 防止越级 |
| 视频资产替换 | `EU-09`（`identity_equal` 门）+ `EU-08` + `EU-31` + `eikona rollback` | 断线 / `unknown_accept` 不产生第二次付费提交；技术回滚与验收分离 |

## 需要新增的 3 个 owner 侧合同

| ID | 合同 | owner | 依赖的真实基础 |
| --- | --- | --- | --- |
| C1 | `yeisme.owner_action.v1` | root 交接 + 各 owner | root `openspec/specs/remote-media-service-access` 已要求 stable operation ref / status / event cursor / cancel / reconcile / idempotency |
| C2 | `scaena.draw_batch.v1` | `agent/scaena` | `scaena asset draw plan --wave/--requires`、`workflow status/resume` |
| C3 | `yeisme.replacement_bound.v1` | `cli/eikona` + `agent/scaena` | `eikona replace/rollback` 的 hash 校验、`scaena workflow repair` 的幂等、`eikona.asset_handoff.v2` 的 `replacement_status` |

详见 [contracts/](contracts/) 下三份合同定义。

## 明确不做

- 不引入外部技能包的任何角色、脚本、模型白名单或平台 CLI 术语；
- 不建跨 owner 凭据 / 生产网关（root `owner-hosted-remote-profile` 已判 `reject-now`）；
- 不改 `ai-drama-router` 的唯一入口，`DramaRoutePlan v1` 仍是语义路由结果而非 canonical state；
- 不放松 `scaena asset draw select --actor <human>` / `freeze --confirm`；
- 不把 `eikona accepted` 写成 `production_ready`；不把 `--no-remote` 当绕过 owner 的路径；
- 不手写 `.scaena` / SQLite / manifest / receipt；receipt 由 owner CLI 的 `--json` 产出。
