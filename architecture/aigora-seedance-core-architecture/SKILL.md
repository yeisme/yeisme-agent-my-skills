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

## 约束

- 不把现有 mock video flow 表述为真实 Seedance provider 集成。
- 不把 `docs/data-model.md` 的目标实体表述为已落库模型。
- 不访问网络、密钥、生产 channel 或 callback endpoint。
- 不执行 route promotion、预算、账单、artifact、配置或 OpenSpec 写操作。

## 输出格式

输出：范围、source-confirmed facts、reference lessons、implementation gaps、target recommendations、验证建议与风险。所有“目标”必须带有待实现语义。
