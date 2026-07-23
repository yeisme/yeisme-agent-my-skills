# Seedance 模块映射

| 关注域 | 已确认路径 | 当前可确认状态 | 目标责任 |
| --- | --- | --- | --- |
| Seedance 入站解析 | `internal/protocol/seedance/video_parser.go` | 解析基础视频字段与 filing/business refs；未知字段标记为 mock parser 不支持 | Service Plane 将协议请求投影为 `CapabilityIR` |
| 视频 HTTP 入口 | `internal/httpapi/v1_videos.go` | 调用 `gateway.HandleVideo` 并投影结果；未证明异步 job 生命周期 | Service Plane 接受请求和投影 job/result ref |
| 网关视频路径 | `internal/app/gateway_service.go` | 存在 Seedance parser 调用；需逐次审查实现，不能假定真实 provider 调用 | 由 Scheduling 决定执行和状态真相 |
| 路由与预算 | `internal/scheduling/route/`、`internal/scheduling/budget/` | 已有 route/budget 包；未证明 Seedance eligibility-first 或 attempt binding | Scheduling Plane 路由、预算与 incident guard |
| provider adapter | `internal/adapters/` | 有 core/mock/compat adapter；未发现 `internal/adapters/seedance/` | 独立 Seedance render/submit/poll/callback adapter |
| job 与 artifact 模型 | `internal/persistence/models/operator.go` | 有简化 `JobRecord`/`ArtifactRecord`；未发现 attempt 模型 | job/attempt 分离、artifact manifest 与 mirror 状态 |
| 观测与账本 | `internal/observability/`、`docs/data-model.md` | 已有 observability 包与目标数据设计；需按具体调用确认覆盖 | append-only ledger、trace vault、scorecard、workbench read model |

该表是导航而非实现清单；每次设计结论须回到具体源码、测试和 OpenSpec 核实。
