---
name: aigora-seedance-core-architecture
description: Use when reviewing or designing Aigora Seedance core architecture, three-plane ownership, lifecycle boundaries, and implementation gaps from an Aigora session.
---

# Aigora Seedance 视频核心架构审查

用于审查或设计 Seedance 视频生成能力在 Aigora 中的三平面划分、生命周期边界和当前实现差距。本技能仅做只读分析与设计梳理，不直接修改代码或运行状态。

## 参考文件

在 Aigora 根目录下按需查阅：

1. `AGENTS.md`
2. `docs/architecture/architecture.md`
3. `docs/architecture/data-model.md`
4. `docs/architecture/runtime-architecture-detail.md`
5. `docs/protocols/seedance-api-contract.md`
6. `openspec/changes/aigora-seedance-video-core/proposal.md`
7. `openspec/changes/aigora-seedance-video-core/design.md`
8. `openspec/changes/aigora-seedance-video-core/tasks.md`
9. `internal/protocol/seedance/video_parser.go`
10. `internal/httpapi/v1_videos.go`
11. `internal/persistence/models/operator.go`
12. `references/module-map.md`

## 梳理步骤

1. **明确三平面职责**：厘清 Service Plane（协议解析与响应）、Scheduling Plane（路由、预算、任务与重试）和 Observability Plane（账本、Trace、评分与回放）各自负责什么数据。
2. **区分“已实现”和“规划中”**：对照现有源码与 `data-model.md`，只有代码和迁移里真正落地的才算“已实现”，其余明确标为“待实现”。
3. **核对准入条件**：逐项检查备案/资质（filing）、站点账号、密钥、输入素材、预算控制与安全策略的就绪状态。
4. **梳理全链路状态**：检查任务（Job）、单次执行尝试（Attempt）、回调（Callback）、轮询（Poll）、对象存储转存（Mirror）、计费与控制台展示之间的衔接与缺口。

## 与上游创作端（Scaena）的协作边界

当 Scaena 调用 Aigora 生成分镜视频时，Scaena 负责剧本与分镜审美验收，Aigora 负责底层视频生成调度：

```text
Scaena 分镜规格（ShotIntent / ShotGenerationSpec）
  -> 绑定执行凭据与外部引用
  -> Aigora 创建任务（Job / Attempt）并返回回执
  -> Scaena 按原任务引用轮询或对账（Reconcile）
  -> 导入待审阅产物（pending_review）
```

核对要点：
- Scaena 只传引用 ID、摘要、能力标识、权限范围和幂等键，不传 Scaena 内部数据库私有状态。
- 首次提交如果遇到网络超时、不确定是否受理，Scaena 必须保留原任务引用去做对账回查（reconcile），不能换幂等键重复提交。
- 任务终态只认 `succeeded`、`failed` 或 `cancelled`，遇到未知状态一律按未完成处理（fail closed）。
- Aigora 不替 Scaena 做画面内容审核，Scaena 也不直接持有底层视频厂商的密钥。

## 注意事项

- 不要把本地模拟（mock）的视频流程说成已经接通真实 Seedance 厂商。
- 不要在分析报告中输出原始提示词、厂商报文、签名下载链接、密钥或备案隐私材料。
