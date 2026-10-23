---
name: aigora-seedance-next-router-design
description: Use when designing or reviewing Aigora Seedance eligibility-first routing, job and attempt semantics, callback recovery, and evidence boundaries from an Aigora session.
---

# Aigora Seedance 下一代路由设计

用于设计和审查 Seedance 视频生成请求的路由逻辑，核心思路是：**先过滤不合资格的渠道（Eligibility First），再对可用候选渠道打分排序（Ranking）**，并保证重试绑定（sticky attempt）、受理状态未知（`UNKNOWN_ACCEPT`）时的对账恢复、回调验签以及产物与扣费记录一致。

## 参考文件

在 Aigora 根目录下按需查阅：

1. `AGENTS.md`
2. `docs/architecture/runtime-architecture-detail.md`
3. `docs/architecture/data-model.md`
4. `docs/upstreams/upstream-profile-conformance.md`
5. `docs/routing/video-model-routing.md`
6. `openspec/changes/aigora-seedance-video-core/design.md`
7. `internal/scheduling/route/controller.go`
8. `internal/scheduling/budget/controller.go`
9. `internal/protocol/seedance/video_parser.go`
10. `references/router-blueprint.md`

## 设计梳理要点

1. **全链路流转**：从请求解析为统一中间表示（`CapabilityIR`），依次经过资格过滤、候选排序、预算预留、创建任务（Job / Attempt）、调用 Adapter、回调或轮询对账、产物转存（Mirror）到记账归档。
2. **硬性准入条件（一票否决，不能靠打分绕过）**：备案与授权资质、渠道发布阶段（test / gray / default）、输入素材就绪状态、内容安全策略、配额与限流、预算余额以及故障冻结状态。
3. **候选渠道排序**：对通过准入检查的渠道，明确打分维度、同分决胜规则（tie-breaker）以及脱敏的路由决策记录（方便在控制台解释“为什么选了这个渠道、为什么排除了别的渠道”）。
4. **Job 与 Attempt 边界**：同一个幂等键对应唯一的 Job；每次实际调用生成一条固定配置快照的 Attempt；轮询、回调和取消都严格绑定到当前 Attempt。当请求超时、不确定上游是否已受理时，进入 `UNKNOWN_ACCEPT` 状态，必须先对账确认，不能盲目重发。
5. **回调与产物交付**：回调必须先验签、去重并核对关联 Attempt；上游生成成功不等于产物已就绪，只有转存到自有对象存储（MinIO/S3）成功后才算交付完成，转存失败要明确标记为 `mirror_failed`。

## 注意事项

- 区分现有代码和目标设计，不要把还在规划中的路由或状态机说成已经上线。
- 无论质量评分多高，都不能绕过备案授权、预算上限、安全审查或渠道发布门禁。
- 不要在设计文档或日志中暴露原始提示词、厂商返回正文、密钥或回调签名密钥。
