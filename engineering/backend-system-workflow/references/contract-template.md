## Backend Contract Minimum Shape

Use this shape when no project-specific template exists:

```yaml
backend_surface:
  name: Approval Decision API
  type: api + application-service + state-machine
  owner_subproject: agent/ordo

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

