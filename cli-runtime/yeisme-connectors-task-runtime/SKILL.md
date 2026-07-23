---
name: yeisme-connectors-task-runtime
description: Use when changing, testing, reviewing, documenting, releasing, or maintaining the task-control runtime absorbed into backend-server/connectors, including connectors task commands, TaskBridge compatibility binaries and schemas, provider sync, action/audit files, Pinax handoff, evidence, and Go quality gates.
---

# Yeisme Connectors Task Runtime

Use this skill for the task-control product runtime owned by `backend-server/connectors`. The primary operator surface is `connectors task`; `taskbridge` is a compatibility binary built from the same codebase and must not become a second implementation owner.

Read `references/maintenance.md` when the task touches compatibility inventory, provider writes, storage migration, Pinax handoff, package smoke, deprecation, or deletion gates.

## Boundaries

- Enter `backend-server/connectors` and follow its `AGENTS.md` before implementation.
- Keep task application logic under `internal/task*`; `cmd/connectors` and `cmd/taskbridge` are thin entrypoints over the same implementation.
- Preserve released `taskbridge.*.v1` schemas, error semantics, dry-run behavior, and confirmation gates until an explicit versioned migration removes them.
- Provider credentials stay in Connectors credential references; never emit secrets, raw provider payloads, prompts, or private tool arguments.
- Pinax consumes the stable CLI contract and must not import Connectors internals or read its stores.
- The compatibility inventory must fail closed until consumer, package, rollback, deprecation, and repository-deletion gates have evidence.

## Workflow

1. Inspect `internal/taskcompat`, the affected `internal/task*` package, both command entrypoints, and the owning OpenSpec change.
2. Implement behavior once under the shared task runtime; do not fork logic for the compatibility binary.
3. Add focused tests for the formal `connectors task` path and compatibility tests for `taskbridge` where the stable contract requires them.
4. For integration/system/e2e work, write redacted evidence under `temp/integration-test-runs/<run-id>/`.
5. Update compatibility inventory entries only after the named evidence exists.

## Validation

```bash
cd backend-server/connectors
go test ./...
go test -race ./...
go vet ./...
CGO_ENABLED=0 go build ./...
scripts/taskbridge-replacement-smoke.sh
openspec validate connectors-absorb-taskbridge-runtime --strict
```

After source or profile changes, run from the repository root:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-target backend-server/connectors
scripts/skills.sh validate-subprojects-runtime
```
