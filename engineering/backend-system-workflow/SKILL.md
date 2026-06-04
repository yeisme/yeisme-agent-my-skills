---
name: backend-system-workflow
description: Use when designing, implementing, reviewing, optimizing, or testing backend services, APIs, workers, queues, state machines, persistence, concurrency, observability, permissions, artifacts, or Go/Golang runtime code in this repository; enforce backend boundaries, data consistency, idempotency, concurrency control, performance evidence, and operational readiness.
---

# Backend System Workflow

Use this skill for backend work where correctness depends on more than writing handlers and models. It applies to Go services, TypeScript/Node services, CLI daemons, MCP servers, agent orchestration runtimes, workers, queues, database-backed APIs, and operations control planes.

Pair it with:

- `yeisme-coding-execution-driver` for sustained implementation.
- `test-driven-development`, `systematic-debugging`, and `verification-before-completion` when present in the subproject.
- `performance-profiler` for measurement, profiling, and optimization.
- External `golang-pro` for Go 1.21+, goroutines, channels, `sync`, interfaces, generics, table-driven tests, race detector, pprof, and benchmarks when available.
- `cso` when permissions, secrets, audit, tool execution, or external access are security-sensitive.
- `golang-cobra-viper-cli-architecture` when a Go backend project also exposes a CLI, command wrapper, config surface, or reusable Go CLI module.
- `golang-github-release-guardrails` when Go work touches CI, release, GitHub, or distribution.

## Core Rule

Do not accept AI-generated backend code because it compiles or returns a happy-path response.

Backend acceptance requires explicit treatment of:

- ownership boundary and layering
- data model and relationships
- state machine and transition authority
- idempotency and duplicate delivery
- transactions and concurrency control
- structured errors and retryability
- permissions and auditability
- API contract stability
- observability and diagnostics
- queue or worker lifecycle
- migrations, indexes, constraints, and rollback notes
- config and secret handling
- artifact lifecycle
- edge-case tests
- performance baseline and profiling evidence when relevant

For Cohors, Agent Team, MCP Gateway, and engineering consoles, the backend should usually be an event-driven task state system, not a thin CRUD app.

## Required Workflow

1. Locate the owning subproject before editing code. Read the nearest `AGENTS.md`, `go.mod` or `package.json`, migrations, API contracts, worker code, storage docs, and existing tests.
2. Identify the backend surface:
   - API or handler
   - application service or use case
   - domain logic or state machine
   - repository or external gateway
   - worker, queue, lease, scheduler, or daemon
   - database migration or schema
   - observability, health, diagnostics, or audit
3. Define or update the backend contract before implementation:
   - entities and relationships
   - allowed states and transitions
   - idempotency keys and dedupe rules
   - permission checks and actor model
   - API request/response and error shape
   - events, logs, metrics, traces, and audit records
   - retry, timeout, cancellation, and lease behavior
4. Implement through clear layers:
   - API / Handler: parsing, auth context, validation dispatch, response mapping
   - Application Service / Use Case: transaction boundary, orchestration, idempotency, permission checks
   - Domain Logic: invariants, state transitions, pure rules where possible
   - Repository / External Gateway: persistence and third-party calls, no hidden business decisions
   - DB / Queue / Third-party API: migrations, constraints, indexes, retries, timeouts
5. Add migrations and constraints with the model change. Do not only update ORM structs or TypeScript types.
6. Add tests for unhappy paths, duplicate requests, illegal transitions, permissions, concurrent claims, retries, timeout, cancellation, transaction rollback, pagination boundaries, and external failures.
7. Add or verify observability: structured logs, request_id, trace_id, run_id where applicable, metrics, health checks, diagnostics, audit events, and product TraceEvent records.
8. For Go backends or concurrent runtimes, evaluate goroutine ownership, cancellation, `context.Context`, `sync`, channels, atomics, locks, race detection, pprof, and benchmark coverage.
9. Run focused functional checks plus race, integration, and performance checks when the change affects workers, state, queues, or shared resources.

## Backend Contract Minimum Shape

Use this shape when no project-specific template exists:

```yaml
backend_surface:
  name: Approval Decision API
  type: api + application-service + state-machine
  owner_subproject: cli/cohors

entities:
  - name: Approval
    required_fields: [id, run_id, status, created_at, updated_at, version, metadata, last_error]
    relationships: [Run, Task, TraceEvent, PolicyDecision]
  - name: TraceEvent
    note: product event object, not plain stdout

states:
  entity: Approval
  allowed:
    pending: [approved, denied, canceled]
    approved: [approved]
    denied: [denied]
    canceled: [canceled]
  transition_authority:
    approve: [approver, admin, system-agent-with-grant]
    deny: [approver, admin]
  idempotent_transitions: [approve, deny, cancel]
  emits_events: [approval.approved, approval.denied, approval.canceled]

idempotency:
  key: approval_id + action + actor_id
  duplicate_policy: return current terminal state without repeating downstream side effects
  storage: unique constraint or idempotency table

concurrency:
  control: optimistic version or row-level atomic update
  worker_claim: update-with-where, not select-then-update
  race_tests: required when multiple workers or goroutines touch this state

api_contract:
  success_shape: { data: {}, meta: { request_id: req_xxx } }
  list_shape: { data: [], page: { cursor: xxx, has_more: true } }
  error_shape:
    code: TOOL_TIMEOUT
    message: Tool call timed out
    retryable: true
    details: {}
    trace_id: trc_xxx

observability:
  logs: structured, redacted
  metrics: latency, errors, retries, queue_depth
  events: TraceEvent and audit log
  diagnostics: health or diagnostics endpoint updated

storage:
  migration: required
  indexes: [run_id, status, created_at, lease_expires_at]
  constraints: [status enum/check, unique idempotency key, foreign key policy]
  rollback_notes: required for risky changes

tests:
  unit: state transition rules
  integration: API + DB transaction + migration
  concurrency: duplicate approve and worker claim race
  e2e: complete run/task/approval/artifact trace
  failure: timeout, retry, cancellation, rollback
```

## Domain Model Rules

For agent orchestration systems, prefer explicit product objects:

- `Run`
- `Task`
- `Agent`
- `Step`
- `Approval`
- `Artifact`
- `TraceEvent`
- `PolicyDecision`
- `ToolCall`
- `CostEvent`

Critical entities should normally include:

- `id`
- `run_id` or clear owner scope
- `status`
- `created_at`
- `updated_at`
- `version`
- `metadata`
- `last_error`

Do not represent important lifecycle state as arbitrary strings without transition rules. Do not let direct DB field updates be the state machine.

## State Machine Rules

For every critical status field, define:

- allowed states
- allowed transitions
- actor or subsystem allowed to trigger each transition
- whether the transition is idempotent
- whether it emits TraceEvent, audit log, metric, or downstream side effect
- retry behavior and failure handling

Block or redesign code that allows:

- canceled tasks to be claimed or completed
- approved approvals to return to pending
- failed tasks to write success artifacts without an explicit retry transition
- UI state to diverge from worker state
- state changes outside the application service or domain transition path

## Idempotency And Concurrency

Assume duplicate requests and concurrent workers exist.

Required checks for backend mutations:

- user double-clicks or retries HTTP after timeout
- queue duplicate delivery
- worker crash and retry
- multiple workers claim the same task
- approval and cancellation race
- timeout reaper and completion race
- repeated tool result submission

Preferred mechanisms:

- `idempotency_key`, `request_id`, or dedupe key
- unique constraints
- upsert with clear conflict behavior
- compare-and-swap version
- row-level lock or atomic update
- lease owner, heartbeat, and `lease_expires_at`
- queue visibility timeout

Never implement task claim as select-then-update. Use an atomic update with status and lease predicates.

## Go Backend Rules

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

## Error Contract

Errors returned to UI, CLI, or agents must be structured enough to drive the next action:

```json
{
  "code": "TOOL_TIMEOUT",
  "message": "Tool call timed out",
  "retryable": true,
  "details": {
    "tool": "github.create_pr",
    "timeout_ms": 30000
  },
  "trace_id": "trc_xxx"
}
```

Differentiate at least:

- invalid input
- permission denied
- business conflict
- not found
- external dependency failure
- timeout
- rate limit
- internal error
- retryable vs non-retryable failure

Do not leak secrets, tokens, authorization headers, private request bodies, or internal stack traces into user-facing errors.

## Permission And Audit Rules

Do not trust frontend-provided `user_id`, workspace, run, project, or role.

Define:

- actor identity
- workspace/project/run scope
- roles such as viewer, operator, approver, admin, and system-agent
- read, write, approve, admin, dangerous action, artifact, log, and secret visibility permissions
- audit event for dangerous or privileged actions

Dangerous actions must include actor, scope, action, target, decision, request_id, trace_id, timestamp, and redacted details.

## Observability Rules

Backend behavior must be diagnosable after deployment:

- structured logs with request_id, trace_id, run_id, task_id, worker_id where applicable
- metrics for latency, errors, retries, queue depth, lease expirations, task duration, artifact failures, and external API failures
- audit log for privileged actions
- health check for process liveness and dependency readiness
- diagnostics endpoint or command for operational status
- TraceEvent as product data for agent systems

TraceEvent is not a log line. It is a structured product object that powers UI timeline, debugging, eval, and user trust.

## Artifact Rules

Do not leave product artifacts as anonymous local files such as `/tmp/result.md`.

Artifact records should include:

- id
- run_id
- task_id when applicable
- type
- path or uri
- mime_type
- size
- checksum
- status
- created_by
- created_at
- evidence_refs

Storage may be local disk, S3, MinIO, database blob, or another backend, but the product layer should use artifact records, not raw paths.

## Testing Standard

Minimum backend tests should go beyond happy path:

- unit tests for domain rules and state transitions
- integration tests for DB, migrations, repository, and API
- contract tests for request/response and error shape
- concurrency tests for worker claim, duplicate mutation, and cancellation races
- permission tests for each role and forbidden action
- retry/timeout tests for external dependencies and queues
- transaction rollback tests
- pagination and cursor boundary tests
- e2e test for full run/task/approval/artifact/trace flow when the surface is agent orchestration

When no test infrastructure exists, add the smallest local test around the changed domain logic or explicitly report the gap.

## Performance And Optimization Gate

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

## AI Backend Blacklist

Reject or rewrite AI-generated backend code that:

- puts complex business logic in handlers
- updates lifecycle state directly without transition rules
- lacks transactions for multi-write mutations
- lacks idempotency for repeated actions
- performs select-then-update task claims
- omits indexes, constraints, or migrations
- returns unstructured errors
- logs secrets or authorization headers
- trusts frontend-supplied identity or role
- runs long work inside HTTP handlers
- treats TraceEvent as stdout
- writes artifacts only to raw paths
- has no tests beyond happy path
- adds concurrency without cancellation and race verification
- claims performance improvement without measurement

## Validation

Run the narrowest relevant checks for the owning project:

- unit tests for changed domain logic
- integration tests for DB/API/queue behavior
- migration apply or validation command
- contract tests for API response and error shape
- race tests for Go concurrency-sensitive code
- benchmark or profiling command for performance-sensitive code
- lint/static checks
- health or diagnostics smoke test when operational behavior changed

If a validation command cannot run, report the exact reason and the strongest evidence used instead.
