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

Backend acceptance requires explicit treatment of ownership and layering, data model and relationships, ORM/query-builder selection and repository boundary, state machine and transition authority, idempotency, transactions and concurrency, structured errors, permissions and audit, API contract stability, logging/observability, queue or worker lifecycle, migrations/indexes/constraints/rollback, config and secrets, artifact lifecycle, edge-case tests, and performance evidence when relevant.

For Ordo, Agent Team, MCP Gateway, and engineering consoles, the backend should usually be an event-driven task state system, not a thin CRUD app.

Database migrations and API/RPC contracts evolve incrementally. `DROP COLUMN`/`DROP TABLE`, narrowing a type, adding `NOT NULL` without a default, renaming a populated column, and changing an HTTP method/path or proto field number are generation-breaking changes. Follow `yeisme-evolutionary-change-policy`: gate them behind an OpenSpec change with expand-then-contract migrations, a deprecation window, and a rollback before touching the schema or wire format.

## Backend Workspace And Debugging Defaults

Backend work that runs a hot-reload service, worker, daemon, migration, database, cache, or long-lived diagnostic process defaults to an isolated `feature/<topic>` branch/worktree. Keep ports, runtime/data directories, caches, temporary files, generated outputs, process groups, and logs separate from a client/Web preview running in the current workspace. Use the current workspace only when the backend must consume its uncommitted state or the user/owner explicitly requires it; record the override and keep a single writer.

The agent should debug this lane automatically through a bounded loop: start with the real owner command, wait for a health/readiness signal, reproduce with the smallest focused test or request, inspect structured logs and trace/request IDs, patch only owned backend paths, rerun focused tests, then verify the client-facing contract. Preserve failure evidence and classify it as introduced, pre-existing, concurrent, environmental, or ambiguous before repairing. Never restart a duplicate writer or kill a process outside the recorded lease.

At stable boundaries, report or create narrow checkpoints for contract/schema, backend behavior plus focused tests, and real integration. A child agent returns evidence and a checkpoint manifest; root owns any commit, merge, push, migration apply, or cleanup action under repository authorization.

## Required Workflow

1. Locate the owning subproject before editing code. Read the nearest `AGENTS.md`, `go.mod` or `package.json`, migrations, API contracts, worker code, storage docs, and existing tests.
2. Identify the backend surface: API/handler, application service, domain/state machine, repository/gateway, worker/queue/lease/scheduler/daemon, migration/schema, or observability/health/audit.
3. Define or update the backend contract before implementation: entities, ORM/repository boundary and any raw SQL exception, allowed states/transitions, idempotency keys, permissions, API error shape, events/logs/metrics/traces, retry/timeout/cancellation/lease. Copyable YAML: `references/contract-template.md`.
4. Implement through clear layers: Handler (parse/auth/validate/map) → Application Service (transaction, orchestration, idempotency, permission) → Domain (invariants, transitions) → Repository/Gateway (ORM persistence, no hidden business decisions) → DB/Queue/third-party (migrations, constraints, indexes, retries, timeouts).
5. Add migrations and constraints with the model change. Do not only update ORM structs or TypeScript types.
6. Add tests for unhappy paths, duplicate requests, illegal transitions, permissions, concurrent claims, retries, timeout, cancellation, transaction rollback, pagination boundaries, and external failures. Layering and Go testscript: `references/testing-tools.md`.
7. Add or verify the service logging contract: JSON logs by default, stdout/stderr separation, optional rotating file sink, call correlation, redaction, metrics, health, diagnostics, audit, TraceEvent. Details: `references/logging.md`.
8. For Go backends or concurrent runtimes, evaluate goroutine ownership, cancellation, `context.Context`, `sync`, channels, atomics, locks, race detection, pprof, and benchmarks. Rules: `references/go-and-performance.md`.
9. Run focused functional checks plus race, integration, and performance checks when the change affects workers, state, queues, or shared resources.

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

Domain objects and artifact records: `references/domain-and-artifacts.md`.

## State Machine Rules

For every critical status field, define allowed states, allowed transitions, actor/subsystem authority, whether the transition is idempotent, whether it emits TraceEvent/audit/metric/side effect, and retry/failure handling.

Block or redesign code that allows:

- canceled tasks to be claimed or completed
- approved approvals to return to pending
- failed tasks to write success artifacts without an explicit retry transition
- UI state to diverge from worker state
- state changes outside the application service or domain transition path

## Idempotency And Concurrency

Assume duplicate requests and concurrent workers exist.

Required checks: user double-click or HTTP retry after timeout; queue duplicate delivery; worker crash and retry; multiple workers claiming the same task; approval/cancellation race; timeout reaper vs completion; repeated tool result submission.

Preferred mechanisms: `idempotency_key` / `request_id` / dedupe key; unique constraints; upsert with clear conflict behavior; compare-and-swap version; row-level lock or atomic update; lease owner, heartbeat, and `lease_expires_at`; queue visibility timeout.

Never implement task claim as select-then-update. Use an atomic update with status and lease predicates.

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

Differentiate at least: invalid input, permission denied, business conflict, not found, external dependency failure, timeout, rate limit, internal error, retryable vs non-retryable.

Do not leak secrets, tokens, authorization headers, private request bodies, or internal stack traces into user-facing errors. Backend and deployment surfaces should use their secret manager, platform credentials, or environment injection; local CLI helpers may use user-level config or a user-level secret store, but project/repo config, fixtures, docs, logs, traces, and evidence must not contain real credentials. Do not introduce shell credential scripts as a persistence mechanism.

## Permission And Audit Rules

Do not trust frontend-provided `user_id`, workspace, run, project, or role.

Define actor identity, workspace/project/run scope, roles (viewer, operator, approver, admin, system-agent), and permissions for read, write, approve, admin, dangerous action, artifact, log, and secret visibility.

Dangerous actions must include actor, scope, action, target, decision, request_id, trace_id, timestamp, and redacted details.

## Observability Rules

Backend behavior must be diagnosable after deployment: JSON structured logs for every service mode; metrics for latency, errors, retries, queue depth, lease expirations, task duration, artifact failures, and external API failures; audit log for privileged actions; health check for process liveness and dependency readiness; diagnostics endpoint or command; TraceEvent as product data for agent systems.

TraceEvent is not a log line. It is a structured product object that powers UI timeline, debugging, eval, and user trust.

Service logging JSON contract and tests: `references/logging.md`.

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

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Handler contains business logic or raw SQL | Move to app service + GORM/Drizzle repository | Do not add `database/sql` / `sqlx` / `ent` / `bun` as the business layer |
| Duplicate request or worker retry | Idempotency key + unique constraint | Never select-then-update for claims |
| Illegal state transition | Encode allowed transitions and actor | Do not write status fields from handlers |
| Happy-path-only tests | Add duplicate, permission, timeout, rollback cases | Do not claim done |
| `localhost:<port>` as the only startup proof | Structured JSON logs + health | File sink must rotate |
| Schema DROP/rename | `yeisme-evolutionary-change-policy` OpenSpec | Expand-then-contract only |
| Secrets in logs/errors | Redact; user-level config only | No shell credential scripts |
