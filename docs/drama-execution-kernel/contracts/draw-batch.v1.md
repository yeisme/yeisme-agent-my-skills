# C2 — `scaena.draw_batch.v1`（抽卡批量合同）

> 状态：**设计合同，待 `agent/scaena` 实现**。不是新的 provider job；Eikona 仍独占生成与 artifact 真源。

## 目的

把逐条 `scaena asset draw plan → start → record` 的 N 次远程往返，收敛为「一次冻结清单 → 依赖波次调度 → 统一回查」，并保留现有 DrawSession 的全部人工门禁。

## 依赖的现有能力

- `scaena asset draw plan --wave N --requires <frozen-slot-ref>`（wave 依赖、cap、`DrawPath` 唯一取路）；
- `scaena asset draw start / record --digest sha256:<64-hex>`（record 零 provider 调用）；
- `scaena asset draw select --actor <human>` / `freeze --confirm`（human-only）；
- `scaena asset draw status --agent`、`scaena workflow status/resume`；
- `eikona generate --purpose subject_candidate --model openai/gpt-image-2.5-sunburst --agent` + `eikona events tail <run_id> --json`；
- `eikona.asset_handoff.v2` 的 path-free `eikona://artifact/<handle>` 与 `sha256`。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `schema_version` | string | 固定 `scaena.draw_batch.v1` |
| `batch_ref` | string | owner 签发的稳定批次 ref |
| `project_ref` / `production_graph_ref` | string | 绑定项目与 ProductionGraph version |
| `source_digest` | string | 上游 `creative.owner-handoff.v0.1` / canon digest；变化即整批失效 |
| `template_digest` | string | 项目模板固定正文摘要；展开词漂移在发送前拒绝 |
| `slots[]` | array | `{slot_ref, brief_ref, wave, requires[], cap, state}` |
| `image_concurrency` | int | 1–100；只表示本地派发上限，**不承诺服务端等量并行** |
| `budget` | object | `{max_dispatches, max_active_ms}`；调用前计入，失败也消耗 |
| `checkpoint_ref` | string | 先落盘再发送；崩溃后只核对，不重发 |
| `items[]` | array | 每项 `{slot_ref, run_ref, artifact_ref, digest, outcome}`；区分新生成 / 旧图复用 / 已绑定 / 在途 / 失败 / 待决 / 缺图 |
| `outcome` | enum | `PLANNED \| DISPATCHING \| AWAITING_READBACK \| COMPLETED \| PARTIAL \| UNKNOWN` |

## 不变量

1. `wave > 1` 的 slot 必须声明 `requires[]`，且上游全部 `frozen` 才可开抽；同 slot 同一时刻只允许一个 active session。
2. 不同 slot 可并行，同 slot 的生成 / 绑定 / 衍生串行；登记仍串行防重复创建。
3. **先落盘再发送**：整批尝试先持久化 `checkpoint_ref`，崩溃后子状态缺失只核对，不重发。
4. 一批提交后**统一回查**；不预造 imageId、不自动选候选、不自动覆盖主图、不自动冻结。
5. `record` 只登记 `run_ref + sha256`，零 provider 调用；bytes 不进 Scaena。
6. `candidate → selected → frozen` 每次跃迁必须 append-only human decision；自动冻结在状态机上不可达。
7. `COMPLETED` 只表示本批已列节点完成；不等于全剧零遗漏、美术验收或 `production_admitted`。
8. UNKNOWN / 在途只恢复查询；确认失败也不自动付费重试；写入预算与只读回查分账。

## Identity-equal 快路径（A5）

命中「候选已生成完成 + 用户已选定 + 只覆盖既有衍生视图」时，允许跳过设计 / 复核 / 全量回归，直接走 EU-09：

- 沿用同一 `entryId` / slot 与完整衍生生产身份，只把动作改为覆盖；
- 复制当前主体详情为不可变写前证据；
- 逐项校验 `template_digest`、母图、衍生别名、集数、旧图与新图 digest；任一漂移整批停止；
- 执行后回读确认衍生 ID / 别名 / 集数不变、`imageId` 等于选定候选、母图不变；
- 技术覆盖完成不等于新增审美结论；旧图不自动删除。

任一创意字段（模型 / 正文 / 时长 / 造型语义）变化 → 退回完整 EU-02..EU-05 链，并生成新 `idempotency_key`。

## 验收

- 一次 `batch_ref` → 并发 → 一次回查；断线 `scaena workflow resume` 不产生第二个 provider attempt；
- `template_digest` 漂移在发送前拒绝；
- 未 `frozen` 的上游 wave 阻止下游开抽；
- `select` / `freeze` 的 `actor` 恒为 human。
