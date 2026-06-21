---
name: backend-system-workflow
description: Use when designing, implementing, reviewing, optimizing, or testing backend services, APIs, workers, queues, state machines, ORM/database access, persistence, concurrency, observability, permissions, artifacts, or Go/Golang runtime code in this repository; enforce backend boundaries, data consistency, idempotency, concurrency control, performance evidence, and operational readiness.
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
- ORM or typed query builder selection and repository boundary
- state machine and transition authority
- idempotency and duplicate delivery
- transactions and concurrency control
- structured errors and retryability
- permissions and auditability
- API contract stability
- service logging contract, observability, and diagnostics
- queue or worker lifecycle
- migrations, indexes, constraints, and rollback notes
- config and secret handling
- artifact lifecycle
- edge-case tests
- performance baseline and profiling evidence when relevant

For Cohors, Agent Team, MCP Gateway, and engineering consoles, the backend should usually be an event-driven task state system, not a thin CRUD app.
> Database migrations and API/RPC contracts evolve incrementally. `DROP COLUMN`/`DROP TABLE`, narrowing a type, adding `NOT NULL` without a default, renaming a populated column, and changing an HTTP method/path or proto field number are generation-breaking changes. Follow `yeisme-evolutionary-change-policy`: gate them behind an OpenSpec change with expand-then-contract migrations, a deprecation window, and a rollback before touching the schema or wire format.

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
   - ORM/query builder choice, repository boundary, and any raw SQL exception
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
   - Repository / External Gateway: ORM/query builder persistence and third-party calls, no hidden business decisions
   - DB / Queue / Third-party API: migrations, constraints, indexes, retries, timeouts
5. Add migrations and constraints with the model change. Do not only update ORM structs or TypeScript types.
6. Add tests for unhappy paths, duplicate requests, illegal transitions, permissions, concurrent claims, retries, timeout, cancellation, transaction rollback, pagination boundaries, and external failures.
7. Add or verify the service logging contract: JSON logs by default, stdout/stderr separation, optional rotating file sink for local/dev services, call correlation fields, redaction, structured metrics, health checks, diagnostics, audit events, and product TraceEvent records.
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
  logs: JSON structured, redacted, stdout/stderr separated, rotating file sink available for local/dev service debugging
  log_fields: [ts, level, service, component, event, request_id, trace_id, run_id, call_id, operation, status, duration_ms]
  metrics: latency, errors, retries, queue_depth
  events: TraceEvent and audit log
  diagnostics: health or diagnostics endpoint updated

storage:
  access_layer: repository + ORM/query builder
  default_orm:
    go: GORM-only
    typescript_node: Drizzle ORM
    python: SQLAlchemy 2.x
  raw_sql_exceptions:
    allowed_only_for: [migration_ddl, database_rpc, listen_notify, queue_claim_database_primitive, maintenance_script, legacy_compatibility]
    requirements: [centralized_boundary, parameter_binding, identifier_allowlist, documented_reason, integration_or_concurrency_test]
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

## ORM And Database Access Rules

Application code must not hardcode SQL strings for direct `SELECT`, `INSERT`, `UPDATE`, `DELETE`, DDL, or table/column-name interpolation.

Defaults:

- Go subprojects use `GORM` as the application ORM for any relational persistence, local index, repository, or database-backed projection.
- Go subprojects must not add `database/sql`, `sqlx`, `ent`, `bun`, or another ORM/query builder as the ordinary business access layer. Drivers such as SQLite/PostgreSQL/MySQL may appear only underneath GORM or in documented migration/fixture boundaries.
- TypeScript/Node projects use `Drizzle ORM` unless the owning subproject already has a documented ORM choice.
- Python backend projects use `SQLAlchemy 2.x` unless the owning subproject already has a documented ORM choice.
- Other languages follow the owning subproject's existing ORM or document the selection in that subproject's `AGENTS.md`.

Required boundaries:

- Handlers and controllers must not call `db.Query`, `db.Exec`, `pool.query`, or equivalent raw database primitives.
- Application services may define transaction and orchestration boundaries, but persistence calls go through repositories.
- Repositories should use ORM/query builder APIs for CRUD, filtering, pagination, joins, upserts, deletes, and state transitions.
- State changes must go through domain/application transition methods, not ad hoc status-field SQL.

Raw SQL exceptions are allowed only for migration/DDL, database RPC/functions, database primitives that an ORM cannot express safely, `LISTEN/NOTIFY`, `FOR UPDATE SKIP LOCKED`, maintenance scripts, test fixtures, or legacy compatibility work. Go exceptions must not become the ordinary business read/write path around GORM. Exceptions must be centralized in a repository, migration, `db/rpc`, or explicit adapter; use parameter binding; source identifiers from an allowlist; document why GORM or the project ORM is insufficient; and include integration, migration, or concurrency validation.

## Test Layering And Default Tools

Name tests by the boundary they exercise:

- `unit`: pure domain rules, pure functions, or one object.
- `integration`: collaboration inside one service, or one service plus one real dependency such as repository + PostgreSQL.
- `component`: one complete service or CLI component with real dependencies and mocked external boundaries, without UI.
- `system`: multiple services started together to verify system-level behavior.
- `e2e`: starts from a user or automation entry and covers the full business chain, such as CLI -> Gateway -> MCP -> Tool -> DB/MQ -> audit/cache/event.

Default tool policy:

- Reuse the owning subproject's existing runner, fixtures, and harness before adding a new framework.
- Go CLI/tool command-level e2e, process e2e, golden stdout/stderr, fixture file trees, and full user flows should use `github.com/rogpeppe/go-internal/testscript` by default.
- Go service, repository, API, and concurrency tests should use standard `testing`, `httptest`, `testing/fstest`, table-driven tests, subtests, race detector, benchmarks, and pprof unless the project already has a stronger harness.
- TypeScript/Node backend projects should use Vitest when no runner exists; HTTP/API integration should use Supertest, Fastify `inject()`, or the framework's existing injection harness.
- Real PostgreSQL, Redis, Kafka, MinIO, and queue dependencies should use Testcontainers or the project's existing docker compose/test harness. Do not substitute SQLite for PostgreSQL/MySQL unless production is SQLite.
- E2E and system tests should cover only critical flows. Do not promote every integration case into a full-stack or browser flow.

Go `testscript` skeleton:

```go
package e2e

import (
	"testing"

	"github.com/rogpeppe/go-internal/testscript"
)

func TestScripts(t *testing.T) {
	testscript.Run(t, testscript.Params{
		Dir: "testdata/script",
	})
}
```

Recommended layout:

```text
tests/e2e/
  cli_script_test.go
testdata/script/
  status.txt
  config-errors.txt
  workflow-happy-path.txt
```

Focused command:

```bash
go test ./tests/e2e -run TestScripts -count=1
```

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

Do not leak secrets, tokens, authorization headers, private request bodies, or internal stack traces into user-facing errors. Backend and deployment surfaces should use their secret manager, platform credentials, or environment injection; local CLI helpers may use user-level config or a user-level secret store, but project/repo config, fixtures, docs, logs, traces, and evidence must not contain real credentials. Do not introduce shell credential scripts as a persistence mechanism.

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

- JSON structured logs for every service mode, including HTTP APIs, workers, daemons, MCP servers, schedulers, and bridges; diagnostics go to stderr in foreground mode and to bounded rotating files for local/dev file logging
- metrics for latency, errors, retries, queue depth, lease expirations, task duration, artifact failures, and external API failures
- audit log for privileged actions
- health check for process liveness and dependency readiness
- diagnostics endpoint or command for operational status
- TraceEvent as product data for agent systems

TraceEvent is not a log line. It is a structured product object that powers UI timeline, debugging, eval, and user trust.

## Backend Service Logging Contract

Every backend service, worker, daemon, MCP server, agent runtime service, and long-running `serve`, `watch`, scheduler, or bridge mode must be debuggable without reading source code or attaching a debugger.

Do not accept services that only print `localhost:<port>`, `server started`, or other free-form status lines. Startup output must identify what is running, where diagnostics go, how calls are correlated, and whether dependencies are ready.

Required logging behavior:

- Default to structured JSON logs for every service and daemon, including HTTP APIs, workers, schedulers, browser bridges, MCP servers, and long-running CLI `serve`/`watch` modes. Text logs are allowed only for explicitly human-only CLI summaries, never for service diagnostics.
- Keep machine/protocol stdout clean. HTTP services must not rely on stdout banners or `fmt.Println` status lines for diagnostics; stdio MCP/protocol services must reserve stdout for protocol frames only.
- Every service runtime must have an explicit diagnostic sink policy: stderr for foreground development, protocol-safe stderr for stdio-compatible services, plus a configured rotating file sink for local/dev debugging unless the owning platform explicitly forbids local files.
- File sinks must be bounded and rotated by size and/or age with retention. Never append forever to one unbounded log file.
- Include correlation fields on every relevant line: `service`, `component`, `event`, `request_id`, `trace_id`, `run_id`, `task_id`, `worker_id`, `call_id`, `operation`, `target`, `status`, `duration_ms`, and `error_code` where applicable.
- Log lifecycle events: config loaded, service starting, bind/listen address, service ready, dependency readiness, shutdown requested, shutdown complete, and fatal startup failure.
- Log call lifecycle around external and internal boundaries: call started, call completed, call failed, retry scheduled, retry exhausted, timeout, cancellation, and circuit/rate-limit decisions.
- For tool, LLM, browser, Firecrawl, database, queue, or subprocess calls, include dependency name, sanitized target/resource id, attempt, timeout, result count/bytes, and duration. Do not log full prompts, scraped page text, provider payloads, tool outputs, tokens, cookies, auth headers, or connection strings.
- Use stable event names such as `service.starting`, `service.ready`, `http.request.completed`, `worker.job.started`, `call.started`, `call.completed`, `call.failed`, `dependency.ready`, and `shutdown.completed`.
- Make log level configurable through the owning project's config convention. `debug` and `trace` may add detail but must still redact secrets and truncate large values.

Recommended minimum JSON fields:

```json
{
  "ts": "2026-06-10T12:00:00Z",
  "level": "info",
  "service": "indagator-fetcher",
  "component": "firecrawl_client",
  "event": "call.completed",
  "request_id": "req_123",
  "trace_id": "trc_456",
  "run_id": "run_789",
  "call_id": "call_firecrawl_001",
  "operation": "fetch_markdown",
  "target": "https://example.com",
  "status": "ok",
  "duration_ms": 418,
  "attempt": 1,
  "result_bytes": 32768
}
```

For Go services, prefer `log/slog` with a JSON handler unless the subproject already owns an equivalent structured logger. Wrap logger construction once at process boundary; pass request-scoped loggers or fields through context deliberately, not via global mutable state.

Logging tests or smoke checks are required when adding or changing service startup, stdio/protocol mode, external calls, workers, or file logging:

- startup emits JSON logs with service name, bind address or stdio/worker mode, version/build where available, and log sink description
- stdio/protocol stdout contains only protocol data; diagnostics go to stderr or the configured rotating file
- call lifecycle logs include a stable `call_id`, status, duration, and sanitized target
- secret fields are redacted in stderr, rotating files, test snapshots, traces, and evidence
- file logging rotates or is explicitly bounded by size and/or age when enabled
- health/diagnostics smoke output points to logs by path or sink, not only to `localhost:<port>`

TraceEvent, audit records, and logs are separate artifacts. Logs diagnose runtime behavior; TraceEvent explains product/user-visible agent progress; audit records prove privileged decisions.

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
- component tests for one complete service or CLI component with real dependencies and mocked external boundaries
- system tests for multi-service behavior when the project starts multiple services together
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
- hardcodes raw SQL in handlers, services, or ordinary business logic instead of using the project ORM/query builder
- adds relational persistence to a Go subproject without GORM
- adds `database/sql`, `sqlx`, `ent`, `bun`, or another Go database access layer for ordinary business persistence
- lacks idempotency for repeated actions
- performs select-then-update task claims
- omits indexes, constraints, or migrations
- returns unstructured errors
- logs secrets or authorization headers
- only prints a bind URL such as `localhost:<port>` instead of structured startup, readiness, and log sink information
- lacks JSON structured service logs for backend, worker, daemon, MCP, or long-running serve/watch mode
- mixes logs, banners, progress, or diagnostics into stdio protocol stdout
- lacks call lifecycle logging with `call_id`, correlation ids, status, duration, and redacted dependency context
- writes unbounded log files without rotation or size/age limits
- makes external calls, worker jobs, database writes, or subprocess execution impossible to correlate across logs
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
