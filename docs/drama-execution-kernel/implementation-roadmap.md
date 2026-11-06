# 后续实现路线（DEK v1 交接规格）

> **边界**：本文是主仓的**跨项目交接规格**，不是实现计划。C1/C2/C3 的具体代码、CLI 命令面、schema 与测试分别归 `agent/scaena`、`cli/eikona`、`client/yeisme-control-center` 各自的 OpenSpec change；主仓只保留合同形状、依赖顺序与验收口径。本文不授权付费生成、发布、凭据变更或线上配置修改。

## 前置不变式（所有阶段）

- `ai-drama-router` 仍是唯一语义入口；三类生成统一走 `GenerationCapability<kind>`，入口差异只在 `GenerationBinding`；不询问 `cli|mcp|both`。
- 一次 `ApprovalWindow` 覆盖窗口内全自动；`retry_budget=2`；UNKNOWN 只 `reconcile` 且不消耗预算；越界或耗尽交 `needs_decision`。
- 结构化资产（receipt / batch / bound / profile / evidence）**必须由 owner CLI 产出**，agent 不手写。
- 输出统一 `ai-native-cli-output-contract` envelope（`--json` / `--agent` / `--events`）；不返回 provider key / raw payload / 全链路推理。
- 不执行 race、不自动安装外部 Skills、不生产访问、不发布、不推送；真实 provider canary 单独授权。

## 阶段总览

```text
D0 交接（本仓）        → 合同形状 + 依赖 + 验收口径
   ├─ D1 C1 typed action（Scaena + Eikona 并行）
   ├─ D2 C2 抽卡批（Scaena，依赖 D1）
   ├─ D3 C3 有界替换（Eikona + Scaena，依赖 D1；可与 D2 并行）
   └─ D4 控制中心投影（依赖 D1）
D5 收口（本仓）        → Skills/profile 同步 + 总结
```

| 阶段 | owner | 可并行 lane | 依赖 | 交接状态 |
| --- | --- | --- | --- | --- |
| D0 | 主仓 | — | — | ✅ 已完成：`openspec/changes/drama-execution-kernel-handoff-v1/`（proposal/design/tasks/spec，`openspec validate` 通过） |
| D1 | `agent/scaena` + `cli/eikona` | 2 条（各自 owner 内） | D0 | ⏳ 已交接 → `scaena-dek-typed-action-v1` / `eikona-dek-action-receipt-v1` |
| D2 | `agent/scaena` | 1 条 | D1 | ⏳ 已交接 → `scaena-dek-draw-batch-v1` |
| D3 | `cli/eikona` + `agent/scaena` | 2 条 | D1 | ⏳ 已交接 → `eikona-dek-action-receipt-v1` / `scaena-dek-bounded-replacement-v1` |
| D4 | `client/yeisme-control-center` | 1 条 | D1 | ⏳ 已交接 → `control-center-dek-action-projection-v1` |
| D5 | 主仓 + 三个独立 skills 仓 | 1 条 | D1–D4 稳定 | ✅ Skills 源层已收口：5 个 Skills 对齐、三版提示词、索引整合、三仓校验全绿；代码 owner 侧收口待 D1–D4 |

根 change 已把 D1–D4 的实现任务**全部转入对应 owner OpenSpec 路径**，不在根 `tasks.md` 维护实现进度。本轮**未在三个代码 owner 的工作树写入任何文件**，避免污染其 git 状态；各 owner 的 change 由各自会话建立。

## D1 — C1 `yeisme.owner_action.v1` typed action 路由

**问题**：`agent/scaena/docs/commands/remote.md` 明确 v1 slice 只路由 `remote / upload / mcp / doctor / board`；本地生产写在 remote profile 激活时返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`，远程用户做抽卡/资产管理走不通。

| 项 | 内容 |
| --- | --- |
| owner A | `agent/scaena`：`scaena-api` 增加 typed action 路由，接收 `CapabilityInvocation`（`plan_ref` / `plan_sha256` / `scope_digest` / `idempotency_key` / `approval_ref` / `capability_id` / `kind`），执行对应 EU，返回 `GenerationReceipt` |
| owner B | `cli/eikona`：`eikona serve` 的 `/api/v1` 对齐同一 envelope；复用 `serviceauth` 的 scope / access key / readiness 十维，不新建网关 |
| 不做 | 不放开任意本地命令；不建跨 owner 凭据/生产网关（`owner-hosted-remote-profile` 已判 `reject-now`）；不用 `--no-remote` 绕过 |
| 验收 | 远程提交一个 EU-02 后返回 `action_id` + `event_cursor` + `binding_ref`；客户端不产生 owner state；`scaena remote doctor --json` / `eikona remote doctor --agent` 通过；断线重试不产生第二个 provider attempt |
| 失败重查 | 若返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND` → 路由未注册，回到 owner A；若 `AUTH_SCOPE_DENIED` → 检查 key 的 scope 而非放宽；若 `needs_contract` → 保留已完成阶段，不猜测 |

## D2 — C2 `scaena.draw_batch.v1` 抽卡批量

| 项 | 内容 |
| --- | --- |
| owner | `agent/scaena` |
| 新增面 | 一批冻结 `slots[]` + `template_digest` + `wave/requires` + `image_concurrency` + `budget{max_dispatches,max_active_ms}` → `batch_ref`；先落盘再发送、统一回查 |
| 复用 | `scaena asset draw plan/start/record/status`、`scaena workflow status/resume`、`eikona generate` + `eikona events tail <run_id> --json`、`eikona.asset_handoff.v2` |
| 依赖 | D1（远程提交通道）、`GenerationCapability<image>` binding 发现 |
| 验收 | 一次 `batch_ref` → 并发 → 一次回查；`template_digest` 漂移发送前拒绝；上游 wave 未 `frozen` 阻止下游；`scaena asset draw status --project <p> --asset <slot> --agent` 合格；断线 `scaena workflow resume` 无第二个 provider attempt；`select --actor human` / `freeze --confirm` 不放松 |
| 失败重查 | `QUOTA_EXCEEDED` → 清理未完成会话或交 owner，不自动扩大预算；`UNKNOWN` → 只读回查，不重发；`OWNER_UNAVAILABLE` → 保留 checkpoint，恢复后按原 `batch_ref` 继续 |

## D3 — C3 `yeisme.replacement_bound.v1` 有界替换

| 项 | 内容 |
| --- | --- |
| owner A | `cli/eikona`：`eikona replace` / `rollback` 已有 hash 校验与 replacement record，补 `identity_equal` 判定门的输入绑定与 `GenerationReceipt` 输出 |
| owner B | `agent/scaena`：`workflow repair plan/run` 已有幂等，补终态 FAILED 校验、共享 `claim_key`、三类 kind（image/video/audio）的绑定任务 |
| 复用 | `eikona.asset_handoff.v2` 的 `replacement_status` / `binding_digest`、`scaena production graph describe` 反向影响面、Sonora `audition` / `replace_after_generation` |
| 依赖 | D1；可与 D2 并行（不同 owner 路径） |
| 验收 | 非 `FAILED` 或配置漂移拒绝重提；并发两入口对同一 `claim_key` 最多一个提交；`identity_equal:false` 生成新 `idempotency_key` + 新 `ApprovalWindow`；`eikona rollback <replacement_id> --json` 后 owner 状态仍为 `handoff_candidate` / `pending_review`，不出现 `production_ready` |
| 失败重查 | `ARTIFACT_DIGEST_MISMATCH` → 重新冻结 provenance，不改旧包；`REPLACEMENT_CONFLICT` → 查共享 claim 持有者，不删锁；模型拒绝内容按原错误判断，不归因于备案 |

## D4 — 控制中心 `action_id` 投影对齐

| 项 | 内容 |
| --- | --- |
| owner | `client/yeisme-control-center` |
| 新增面 | 把 Eikona `run_id` / Scaena `submission_ref` / 控制中心 `revision` 映射到同一 `action_id`；`yeisme.work_queue.v1` 按 `action_id + event_cursor` 去重；`yeisme.creative_flow.v1` 五阶段 rail 分开显示 `ACCEPTED / COMPLETED / BOUND / REVIEWED` |
| 复用 | 已有签名 cursor、45s 缓存、`cache: hit/miss/refresh_limited`、`yeisme.control_center.launch_context.v1`、Preview allowlist |
| 依赖 | D1 |
| 验收 | `bun run test:preview:real`；三层不再各查一次；缓存由 `event_cursor` 驱动；Preview 仍「不代表 Owner 已写入」；只读请求失败不重试生成 |
| 失败重查 | `stale` 投影 → 只标新鲜度，不替代 owner 事实；`needs_contract` → 显示缺口而非演示数据 |

## D5 — Skills / profile / 总结收口

| 项 | 内容 |
| --- | --- |
| owner | 主仓 + 三个独立 skills 仓 |
| 动作 | 按 `scripts/skills.sh profile add` 分配新增 skill（当前 `ai-drama-bootstrap` 按需、不进 target）；`HANDOFF.md` 更新合同状态为 implemented；各独立仓指针同步 |
| 验收 | `scripts/skills.sh validate-custom` / `validate-profiles` / `sync-root` / `sync-subprojects` / `validate-runtime` 全绿；`python3 scripts/validate_repository.py`、两个子仓 `validate_skills.py`、`ai-drama-router/scripts/validate_drama_matrix.py` 全绿 |
| 边界 | 存在 runtime 独有修改时先保留并协调，不用同步覆盖；不自动安装外部 Skills、不发布、不推送 |

## 实施顺序建议

1. **先 D1**（否则 D2/D3/D4 的远程链路仍被 `REMOTE_PROFILE_UNSUPPORTED_COMMAND` 阻塞）；
2. D1 稳定后 **D2 与 D3 并行**（不同 owner 路径，一个写者一条 lane）；
3. D4 可与 D2/D3 并行但只消费 D1 的 receipt；
4. **D5 最后**：代码、直接测试与文档稳定后才跑全仓校验与同步；不在实现中途反复跑全量 gate。

## 交接纪律

- 每个 owner 在自己的 OpenSpec change 里写 `proposal.md` / `design.md`（含 Mermaid）/ `tasks.md`（原子任务、owner、依赖、并行 lane、验收命令、失败重查）；中文正文，CLI/字段/命令保持英文。
- 主仓 `openspec/` 只留**一份跨项目交接记录**；不回填子项目文档镜像，不保留 `docs/<project>/**` 副本。
- 一个路径一个写入者；写入者不自审；失败归类为引入/既有/并发/环境/不明后回到原 writer。
- 真实 provider / 付费 canary、凭据、发布与远端部署**分别单独授权**，本地 fixture 与结构检查不代表生产就绪。
- 远程发布仍按「干净分支 + cherry-pick + PR」；`ai-drama-skills` 当前在 feature 分支、聚合仓在 `develop`，不直接 push 当前分支夹带历史未推送提交。
