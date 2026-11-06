# C3 — `yeisme.replacement_bound.v1`（有界替换合同）

> 状态：**设计合同，待 `cli/eikona` + `agent/scaena` 实现**。用于视频 / 音频 / 衍生图资产替换，防止断线后的第二次付费提交与越权创意修改。

## 目的

把「改音频、改正文、补复核」三个互不绑定的步骤，收敛为**一个绑定替换任务**：先证明语义身份未变，再执行固定替换，最后权威回读。

## 依赖的现有能力

- `eikona replace <artifact_id> --project current --to <path> --yes --json` / `eikona rollback <replacement_id> --json`（`rollback` 校验当前文件 hash，不覆盖后续用户编辑）；
- `eikona assets stage / handoff / apply` 与 `eikona.asset_handoff.v2` 的 `replacement_status: not_applied|staged|applied`、`binding_digest`；
- `scaena workflow repair plan --run <run-ref> --json` / `workflow repair run --repair <repair-ref> --json`；
- `submission_ref` / `reconcileVideoProviderTask` / `unknown_accept`（`scaena-production-operator/references/official-routing.md`）；
- `workflow.md:140` 的执行前逐项校验列表。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `schema_version` | string | 固定 `yeisme.replacement_bound.v1` |
| `bound_ref` | string | owner 签发的稳定替换任务 ref |
| `old_ref` / `new_ref` | string | 冻结的旧包 / 新包，均为 path-free FrozenRef |
| `provenance_sha256[3]` | array | 旧媒体、新媒体、原始音源三份实际字节摘要；只证明技术同源，不决定说话人 / 音色 / 对白 |
| `identity_equal_verdict` | object | `{equal: boolean, checked_fields[], mismatches[]}` |
| `field_plan` / `audio_plan` | string | 冻结的字段计划与音频计划 ref |
| `claim_key` | string | 共享 claim 身份：`(project, episode, shot, 原失败 videoId)`；跨入口去重 |
| `outcome` | enum | `PREPARED \| REPLACED \| READBACK_OK \| TERMINAL_REJECTED \| UNKNOWN` |
| `replacement_id` | string | `eikona replace` 返回的回滚句柄 |
| `recovery_ref` | string | 原 state / 原 `submission_ref` 引用 |

## `identity_equal` 判定门

判定输入**直接复用 `workflow.md:140` 的执行前校验列表**，不新增规则：

```
project, ProductionGraph ref/version, shot ref,
frozen intent ref/digest, frozen spec ref/digest, validated bundle ref/digest,
capability ref/digest/maturity, task policy,
duration / ratio / output / audio policy,
exact subject / style / reference versions and ordinals,
non-empty idempotency key
```

补充三类字段：`speaker` / `character subject` / `voice timbre` / `original audio source` / `dialogue text` / `mention` / `model` / `channel`。

| 判定结果 | 路径 |
| --- | --- |
| 全部相等 → `equal: true` | **技术替换**：EU-09，允许跳过创意复核与全量回归 |
| 任一创意字段变化 → `equal: false` | **新创作批**：退回 EU-06，新的 `idempotency_key` 与新的用户授权；禁止借「原样重提」授权 |
| 字段缺失 / provenance 不全 | `TERMINAL_REJECTED`，报具体缺口，不猜默认值 |

## 不变量

1. 一个 `bound_ref` 绑定旧包 / 新包 / provenance / field_plan / audio_plan / claim_key；不得拆成互不绑定的独立步骤。
2. 先验证 `identity_equal`，再替换，再权威回读；字段结果为 `UNKNOWN` 时停止且不重投。
3. 技术替换完成后才刷新技术证据；技术证据刷新不制造新的语义复核结论。
4. 中断后用原 `recovery_ref` 恢复，不创建新任务绕过旧状态。
5. **失败视频受控修复**：只有「返回 ID 全部终态 `FAILED` + 实时回读仍 `FAILED` + 原配置逐字段全等」才允许原样重提；`claim_key` 防并发重投；`--continue-not-sent` 语义只补「已预留未发送」，不产生新派发；新失败必须以其新返回 ID 建立下一轮证据。
6. `unknown_accept` 不换幂等键、不换模型、不创建替代任务；已受理后只 `reconcile` 原任务。
7. `eikona rollback <replacement_id>` 是技术回滚；**不等于验收通过 / 备案完成 / 生产接受**，状态词汇不越级。
8. 不删除历史候选或其 digest；不覆盖后续用户编辑。

## 验收

- 非 `FAILED` 或配置漂移一律拒绝重提；
- 并发两个入口（远程 CLI / 控制中心）对同一 `claim_key` 最多一个进入提交；
- `identity_equal: false` 时生成新 `idempotency_key` 且要求新授权；
- `rollback` 后 owner 状态仍为 `handoff_candidate` / `pending_review`，不出现 `production_ready`。
