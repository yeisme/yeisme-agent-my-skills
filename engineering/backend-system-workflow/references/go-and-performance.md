# Go backend, concurrency, and performance

When modifying Go backend/runtime code, review concurrency and performance explicitly:

- Use `context.Context` for cancellation, deadlines, and request-scoped values. Do not store contexts in structs unless the project has a clear lifecycle reason.
- Own every goroutine: define start, stop, cancellation, error propagation, and leak prevention.
- Use `sync.Mutex`, `sync.RWMutex`, `sync.Cond`, `sync.Once`, `sync.WaitGroup`, `errgroup`, channels, or `sync/atomic` intentionally. Do not rely on "probably single-threaded" assumptions in workers or daemons.
- Prefer `errgroup.WithContext` for coordinated concurrent tasks where cancellation should propagate.
- Use atomics only for simple counters, flags, or lock-free values with clear memory-order expectations. Do not use atomics to hide complex state transitions.
- Protect shared maps and mutable state with locks or confinement to a single goroutine.
- Add `go test -race ./...` when code contains goroutines, shared mutable state, workers, queues, leases, caches, or cancellation logic.
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
- use `go test -race ./...` for concurrency-sensitive code
- consider `go test -run TestName -count=100` for suspected flakes or races that are hard to trigger
