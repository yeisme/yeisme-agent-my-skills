---
name: performance-profiler
description: Use when investigating, measuring, benchmarking, profiling, or optimizing software performance in this repository, including slow builds, slow tests, sluggish CLIs, high CPU or memory use, slow APIs, frontend latency, startup time, throughput, regressions, and before/after performance evidence for targeted optimization.
---

# Performance Profiler

## Purpose

Measure before optimizing. Turn a vague "it feels slow" request into a specific workload, baseline, bottleneck hypothesis, targeted change, and repeatable before/after evidence.

Use this with the domain skill for the owning subproject, such as `yeisme-mcp-gateway-maintainer`, `yeisme-cohors-cli-runtime`, or `yeisme-mcp-builder`.

For backend work, also pair with `backend-system-workflow` so optimization does not bypass state-machine, transaction, idempotency, concurrency, permission, or observability requirements.

## Inputs

- Target path or subproject.
- User-visible performance symptom, target metric, or suspected bottleneck.
- Representative workload: command, endpoint, UI flow, CLI invocation, fixture, dataset, or trace.
- Existing quality gates and functional tests.
- Backend-specific signals when applicable: request latency, DB query count, queue depth, worker throughput, lease expiry rate, retry count, goroutine count, allocation rate, CPU profile, heap profile, lock contention, and race test results.

If the workload is unclear, infer the narrowest realistic scenario from the repo and state the assumption before measuring.

## Outputs

- A short performance brief:
  - target scenario and metric
  - baseline measurements with command or URL
  - bottleneck evidence, not just speculation
  - change made or recommended
  - after measurements using the same method
  - functional verification run after optimization
- Machine-readable probe output when using `scripts/perf_probe.py`.

## Guardrails

- Do not run load tests against production, third-party services, paid APIs, or shared systems without explicit user approval.
- Do not optimize without a baseline unless the task is only to add instrumentation.
- Do not use a microbenchmark as final proof when the user-visible workload is available.
- Do not trade correctness, security, data integrity, or maintainability for a small benchmark win.
- Do not optimize backend state, queues, workers, or concurrency by weakening transactions, idempotency, locks, leases, permissions, or auditability.
- Treat benchmark variance as signal. Repeat runs and compare medians or p95 instead of relying on one fastest run.
- Keep secrets and private request payloads out of logs and reports.

## Workflow

1. Route to the owning subproject for concrete code changes. Stay at the root only for cross-project analysis, skill/tool work, or documentation.
2. Define the performance question:
   - metric: latency, throughput, CPU, memory, allocation, bundle size, startup time, build time, test time, DB query time, or UI responsiveness
   - workload: exact command, endpoint, browser flow, CLI invocation, or benchmark
   - budget: existing SLO, regression threshold, or a pragmatic target
   - backend dimension when applicable: API latency, worker throughput, queue drain time, lease churn, retry rate, DB contention, goroutine count, lock contention, or artifact write throughput
3. Discover available probes:

   ```bash
   python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --cwd <target-path> --discover-only
   ```

4. Establish a baseline with the closest user-visible workload:

   ```bash
   python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --cwd <target-path> --cmd '<command>' --cmd-repeat 3
   python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --url 'http://127.0.0.1:3000/health' --url-repeat 20
   ```

5. Pick the profiler that matches the stack and symptom:
   - Go CPU or allocation issue: `go test -bench ... -benchmem`, `go test -run '^$' -bench ... -cpuprofile cpu.out -memprofile mem.out`, then inspect with `go tool pprof`.
   - Go concurrency issue: run `go test -race ./...`; inspect goroutine ownership, `context.Context` cancellation, channel closure, shared maps, `sync.Mutex`/`sync.RWMutex`, `sync.WaitGroup` or `errgroup`, and `sync/atomic` use.
   - Go worker or queue issue: measure claim latency, queue depth, lease expirations, heartbeat gaps, retry count, worker throughput, task duration, and cancellation latency before changing algorithms.
   - Node or Bun CPU issue: use existing benchmark/test scripts first; if needed run Node with `--cpu-prof` or `--prof` around the representative command.
   - Frontend runtime issue: use Playwright traces, browser performance traces, Lighthouse only when appropriate, and measure the specific interaction.
   - Slow API or CLI: measure end-to-end latency first, then split server, DB, network, serialization, and client-side costs.
   - Build or test slowness: use build tool timings, test runner timing output, cache behavior, and repeated cold/warm runs.
6. Optimize the smallest credible bottleneck. Prefer algorithmic wins, cache correctness, batching, query shape, allocation reduction, and removing repeated work over broad rewrites.
7. Re-run the same baseline commands after the change. Add or update functional tests when behavior changed.
8. Report both the performance evidence and the verification evidence. If the measurement is noisy or inconclusive, say so and recommend the next instrumentation point.

## Backend Performance Checklist

For API, worker, queue, scheduler, daemon, database, or agent runtime optimization, include:

- Baseline workload: exact endpoint, command, benchmark, fixture, or trace.
- Functional invariant: state machine, idempotency, permission, audit, and artifact behavior that must not change.
- Contention hypothesis: DB lock, transaction shape, queue claim, serialization, external API, filesystem, CPU, allocation, goroutine leak, lock contention, or repeated work.
- Observability signal: structured log, metric, TraceEvent, health, diagnostics, pprof, or benchmark output.
- Before/after evidence: same workload and repeat count.
- Regression guard: test, benchmark, race test, or diagnostics check that future AI changes can rerun.

For Go backend code, prefer this escalation order:

1. End-to-end workload timing.
2. `go test -race ./...` for concurrent worker, cache, queue, lease, state machine, or daemon changes.
3. `go test -bench ... -benchmem` for local hot paths.
4. CPU and heap profiles with `go tool pprof` for sustained CPU or memory symptoms.
5. Lock/block/goroutine profiles when symptoms point to contention or leaks and the project exposes runtime profiling.

Useful Go commands:

```bash
go test ./...
go test -race ./...
go test -bench . -benchmem ./...
go test -run '^$' -bench BenchmarkName -benchmem -cpuprofile cpu.out -memprofile mem.out ./...
go tool pprof cpu.out
go test -run TestName -count=100 ./...
```

Do not treat `sync/atomic` as a generic performance fix. Atomics are appropriate for simple counters, flags, and carefully isolated values. Complex lifecycle state should stay behind domain transitions, locks, transactions, or single-owner goroutine confinement.

## Helper Script

`scripts/perf_probe.py` is a dependency-free Python helper for discovery and baseline probes.

Useful modes:

```bash
# Discover manifests, available tools, and likely perf/build/test scripts.
python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --cwd .

# Time commands and capture exit code, wall time, and best-effort max RSS.
python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --cmd 'npm run build' --cmd-repeat 3

# Probe local HTTP latency.
python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --url 'http://127.0.0.1:8787/health' --url-repeat 20

# Save JSON evidence.
python .skills/yeisme/qa-release/performance-profiler/scripts/perf_probe.py --cmd 'go test ./...' --output /tmp/perf-probe.json
```

When documenting benchmark commands or reporting results, show the real command being measured. Local execution wrappers are agent-internal and must not appear in user-facing docs or final replies. Inside `perf_probe.py --cmd`, pass the real command being measured so wrapper behavior does not hide tool behavior.
