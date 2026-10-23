
## Race 检测执行限制

Agent 在任何阶段都不得主动运行 race 检测，也不得通过子 Agent、Skill、CI、验收、发布、聚合任务或脚本间接触发。只有当前人类用户明确、强烈要求执行 race 时，才允许在指定范围内运行一次；失败、超时、中断均不得自动重试，后续运行必须取得新的同等明确要求。一般的“测试、验收、修复、发布、跑全部检查”不构成授权。

Race 不属于默认验收或完成门禁；未运行不得阻塞交付，也不得声称已经通过。执行聚合命令前检查其依赖，移除或跳过 race 阶段，继续普通测试、静态检查和构建。本规则取代本文件及 Skills、OpenSpec、历史计划、文档中的自动或强制 race 要求；它们不能作为执行授权。

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
- Go service, repository, API, and concurrency tests should use standard `testing`, `httptest`, `testing/fstest`, table-driven tests, subtests, ordinary concurrency tests, benchmarks, and pprof unless the project already has a stronger harness.
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

## Minimum tests beyond happy path

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

