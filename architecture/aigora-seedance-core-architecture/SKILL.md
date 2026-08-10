---
name: aigora-seedance-core-architecture
description: Use when reviewing or designing Aigora Seedance core architecture, three-plane ownership, lifecycle boundaries, and implementation gaps from an Aigora session.
---

# Aigora Seedance 核心架构

## 用途

在设计、审查或准备实现 Seedance B 端视频能力时，建立“已确认事实 / 参考经验 / 目标建议 / 当前缺口”的清晰边界。此技能只读，不修改代码、测试、配置、OpenSpec 或运行时状态。

## 必读路径

从 Aigora session 根目录读取：

1. `AGENTS.md`
2. `docs/seedance-core-modules-and-next-router.md`
3. `docs/architecture.md`
4. `docs/data-model.md`
5. `docs/runtime-architecture-detail.md`
6. `openspec/changes/aigora-seedance-video-core/proposal.md`
7. `openspec/changes/aigora-seedance-video-core/design.md`
8. `openspec/changes/aigora-seedance-video-core/tasks.md`
9. `internal/protocol/seedance/video_parser.go`
10. `internal/httpapi/v1_videos.go`
11. `internal/persistence/models/operator.go`
12. `references/module-map.md`

## 只读工作流

1. 先列出 Service、Scheduling、Observability 三平面各自的 state truth、命令和只读投影。
2. 将现有代码与目标数据模型逐项比对；只把实际路径能够证明的能力写为“已实现”。
3. 对 filing、authorization、site account、credential、asset、budget 与安全策略分别给出 readiness 结论。
4. 对 job、attempt、callback、poll、mirror、billing、trace 与 workbench 标明现状、缺口、依赖与验证证据。
5. 输出简短的风险清单，明确不能泄露原始 prompt、provider payload、签名 URL、凭据或备案材料。

## Scaena 单镜头 Federation 消费边界

审查 Scaena → Aigora 时，把 Scaena 视为 caller/creative production owner，把 Aigora 视为视频 execution owner：

```text
Scaena frozen ShotIntent/ShotGenerationSpec/bundle
  -> execution binding + external ref + grant
  -> Aigora job/attempt/receipt
  -> Scaena reconcile
  -> pending-review artifact projection/import receipt
```

必须核对：

- caller 只提交 refs/digests、capability、scope、purpose、idempotency 和 correlation，不提交 Scaena 私有数据库状态；
- Aigora `binding_id`、request digest、caller run、scope 与返回 receipt 一致；
- 首次 accepted/timeout 后若状态未知，Scaena 保存原 `aigora_job_ref`，后续只 reconcile，不重复 submit；
- terminal receipt 状态只能是 `succeeded`、`failed` 或 `cancelled`，未知状态 fail closed；
- Phase 0 只接纳安全 artifact refs 并创建 Scaena `pending_review` 投影；真实下载、内容摘要校验、CAS 落盘与 signed URL 隔离属于后续 `aigora-real-video-artifact-delivery-v1`；
- Aigora 不替 Scaena 做 creative acceptance，Scaena 不持有底层视频 provider credential。

## 约束

- 不把现有 mock video flow 表述为真实 Seedance provider 集成。
- 不把 `docs/data-model.md` 的目标实体表述为已落库模型。
- 不访问网络、密钥、生产 channel 或 callback endpoint。
- 不执行 route promotion、预算、账单、artifact、配置或 OpenSpec 写操作。
- 不把 `httptest` federation canary 或安全 ref adoption 描述成真实 provider/CAS 交付。

## 输出格式

输出：范围、source-confirmed facts、reference lessons、implementation gaps、target recommendations、验证建议与风险。所有“目标”必须带有待实现语义。
