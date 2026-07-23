---
name: aigora-seedance-next-router-design
description: Use when designing or reviewing Aigora Seedance eligibility-first routing, job and attempt semantics, callback recovery, and evidence boundaries from an Aigora session.
---

# Aigora Seedance 下一代路由设计

## 用途

在不修改任何文件或运行状态的前提下，为 Seedance 视频请求提出可审计的路由设计。重点是 eligibility-before-ranking、sticky attempt、`UNKNOWN_ACCEPT` reconciliation、callback 安全和 artifact/billing 事实链。

## 必读路径

从 Aigora session 根目录读取：

1. `AGENTS.md`
2. `docs/seedance-core-modules-and-next-router.md`
3. `docs/runtime-architecture-detail.md`
4. `docs/data-model.md`
5. `docs/upstream-profile-conformance.md`
6. `docs/implementation-plan.md`
7. `openspec/changes/aigora-seedance-video-core/design.md`
8. `internal/scheduling/route/controller.go`
9. `internal/scheduling/budget/controller.go`
10. `internal/protocol/seedance/video_parser.go`
11. `references/router-blueprint.md`

## 只读工作流

1. 描述 request 到 `CapabilityIR`、eligibility、ranking、reservation、job/attempt、adapter、callback/poll、mirror、ledger/trace 的事实流。
2. 先列出不可排序覆盖的拒绝条件：filing/authorization、channel stage、asset readiness、安全、quota/rate、预算和 incident。
3. 为 eligible candidates 定义排序输入、稳定 tie-breaker 和可解释的 redacted decision record。
4. 定义 job 与 attempt 的不变量：幂等 job、每次执行的 snapshot、sticky attempt、限制重试与 `UNKNOWN_ACCEPT` 对账。
5. 定义 callback 验签、去重、轮询恢复、镜像失败、账本 reconciliation 和 operator read-only workbench 的边界。
6. 给出仅 test channel 的验证矩阵；明确哪些命令是现有可运行命令，哪些仍是目标接口。

## 约束

- 不声称 router、attempt、callback 或 `UNKNOWN_ACCEPT` 已经实现。
- 不以 ranking 分数绕过备案、授权、预算、安全或 promotion gate。
- 不输出原始 prompt、provider payload、凭据、签名 URL 或 callback secret。
- 不执行网络、live smoke、route promotion、账单对账、callback 重放或任何写操作。

## 输出格式

输出：输入与边界、eligibility matrix、ranking policy、状态机与不变量、失败/恢复规则、证据与验证计划、未决风险。使用“建议/目标”描述未实现能力。
