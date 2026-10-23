# Go backend, concurrency, and performance

## Race 检测执行限制

Agent 在任何阶段都不得主动运行 race 检测，也不得通过子 Agent、Skill、CI、验收、发布、聚合任务或脚本间接触发。只有当前人类用户明确、强烈要求执行 race 时，才允许在指定范围内运行一次；失败、超时、中断均不得自动重试，后续运行必须取得新的同等明确要求。一般的“测试、验收、修复、发布、跑全部检查”不构成授权。

Race 不属于默认验收或完成门禁；未运行不得阻塞交付，也不得声称已经通过。执行聚合命令前检查其依赖，移除或跳过 race 阶段，继续普通测试、静态检查和构建。本规则取代本文件及 Skills、OpenSpec、历史计划、文档中的自动或强制 race 要求；它们不能作为执行授权。


When modifying Go backend/runtime code, review concurrency and performance explicitly:

- Use `context.Context` for cancellation, deadlines, and request-scoped values. Do not store contexts in structs unless the project has a clear lifecycle reason.
- Own every goroutine: define start, stop, cancellation, error propagation, and leak prevention.
- Use `sync.Mutex`, `sync.RWMutex`, `sync.Cond`, `sync.Once`, `sync.WaitGroup`, `errgroup`, channels, or `sync/atomic` intentionally. Do not rely on "probably single-threaded" assumptions in workers or daemons.
- Prefer `errgroup.WithContext` for coordinated concurrent tasks where cancellation should propagate.
- Use atomics only for simple counters, flags, or lock-free values with clear memory-order expectations. Do not use atomics to hide complex state transitions.
- Protect shared maps and mutable state with locks or confinement to a single goroutine.
- Use ordinary concurrency tests; race execution requires a strong, explicit human request for one run.
- For performance-sensitive code, add `go test -bench ... -benchmem` or a representative integration benchmark and inspect CPU/allocation profiles with `go tool pprof` when useful.
- Avoid long-running work inside HTTP handlers. Handlers should enqueue or create work, then workers process with lease, heartbeat, trace events, artifacts, and cancellation.

## Performance and optimization gate

Optimization work must start with a baseline and end with comparable evidence.

For backend changes that affect latency, throughput, memory, workers, queue depth, concurrency, database access, or startup:

- define target workload and metric
- capture baseline using local command, benchmark, endpoint probe, or integration flow
- identify bottleneck evidence
- make the smallest optimization that preserves correctness
- re-run the same measurement
- run functional tests after optimization

For Go:

- use `go test -bench ... -benchmem` for local algorithmic or allocation questions
- use pprof CPU/heap profiles for sustained CPU or memory symptoms
- use ordinary concurrency tests; never initiate race detection autonomously
- consider `go test -run TestName -count=100` for suspected flakes or races that are hard to trigger
