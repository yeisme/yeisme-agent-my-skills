# Seedance 模块代码与职责对照

| 模块方向 | 相关代码路径 | 当前实现现状 | 目标设计职责 |
| --- | --- | --- | --- |
| Seedance 请求解析 | `internal/protocol/seedance/video_parser.go` | 已支持解析基础视频参数、备案与业务引用；暂不支持的扩展字段会记录在元数据中 | 由 Service Plane 将外部协议请求统一转换为内部 `CapabilityIR` |
| 视频 HTTP 接口 | `internal/httpapi/v1_videos.go` | 已接入 `gateway.HandleVideo` 并返回任务结果；完整异步生命周期仍需按具体接线核对 | 由 Service Plane 接收请求并返回任务引用（job/result ref） |
| 网关视频服务 | `internal/app/gateway_service.go` | 已调用 Seedance 解析器；审查时需结合具体实现确认是否接通真实厂商 | 由 Scheduling Plane 统一管理系统状态与任务调度 |
| 路由与预算控制 | `internal/scheduling/route/`、`internal/scheduling/budget/` | 已有基础路由和预算模块；Seedance 专属的资格过滤与 Attempt 绑定需逐项核对 | 由 Scheduling Plane 负责资格过滤、候选排序、预算预留和故障熔断 |
| 厂商适配器 | `internal/adapters/` | 已有通用/模拟（mock）/兼容适配器；独立的 Seedance 生产适配器按需扩展 | 提供独立的请求构造、提交、轮询与回调验签适配器 |
| 任务与产物模型 | `internal/persistence/models/operator.go` | 已有基础 `JobRecord` 和 `ArtifactRecord`；细粒度 Attempt 与转存状态按规划演进 | 区分 Job 与 Attempt，记录产物清单（manifest）及对象存储转存状态 |
| 可观测与消费账本 | `internal/observability/`、`docs/architecture/data-model.md` | 已有观测模块与数据表设计；具体字段覆盖需结合调用链路核实 | 维护只追加（append-only）账本、Trace 归档、质量评分卡与控制台查询视图 |

> 注：本表用于快速定位代码位置；做架构评估或任务验收时，请以实际源码、测试用例和对应 OpenSpec 文档为准。
