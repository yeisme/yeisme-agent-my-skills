---
name: solocut-service
description: Use when implementing or reviewing the SoloCut Go product backend in client/solocut/server, including HTTP contracts, GORM/PostgreSQL persistence, owner projections, idempotency, ETag conflicts, and operation recovery.
---

# SoloCut Service

`client/solocut/server` 是 SoloCut 产品后端，不是 Scaena/Auctra/Sonora/Eikona/DriveBridge/Anatomia/Aigora 的领域真源。

## 先读

1. `client/solocut/server/AGENTS.md`
2. `client/solocut/docs/architecture/backend-boundary.md`
3. `client/solocut/docs/protocols/api-contract.md`
4. `client/solocut/docs/protocols/error-and-recovery.md`
5. `client/solocut/openspec/changes/solocut-product-platform-foundation-v1/design.md`

## 分层

`HTTP handler -> application service -> domain -> GORM repository -> PostgreSQL`。

- handler 只解码、认证、调用 service、写 envelope。
- service 负责权限、幂等、ETag、事务和状态转换。
- repository 只用 GORM 做普通业务持久化。
- migration DDL 集中在 `migrations/`。
- owner adapter 只能调用公开 contract。

禁止在 handler、application service 或普通 repository 中硬编码业务 SQL；禁止新增 `database/sql`、`sqlx`、`ent`、`bun` 作为业务访问层。

## 合同

成功使用 `{data,meta}`，失败使用 `{error,meta}`。写操作使用 `Idempotency-Key`；版本写入使用 `If-Match`。unknown 结果只能按原 operation identity reconcile，不能换 key 重提。取消后的迟到结果不能覆盖 cancelled。

身份来自服务端 context；请求体不能自报 user、workspace 或 role。错误不能泄漏 token、Authorization、raw provider payload、prompt 或堆栈。

## 当前 readiness

已完成并可由本地证据核验：

- strict/dev auth 隔离；dev headers 仅在 `SOLOCUT_AUTH_MODE=dev` 下读取，workspace membership 仍由 service/store 校验；
- GORM/PostgreSQL migration apply/replay，`001_init`、`002_operation_identity`、`003_operation_version` ledger 与 schema upgrade 检查；
- project/draft/binding/operation 的 membership 边界、ETag/version conflict 和 idempotency replay；
- operation `accepted/running/succeeded/failed/cancelled/unknown` 状态规则、原 operation identity reconcile、cancel replay、transition identity、CAS 并发和 cancelled late result；
- 脱敏 integration evidence，最新参考目录为 `client/solocut/server/temp/integration-test-runs/20261018-131500/`。

仍未完成、不得提前声称完成：正式 OIDC/session、真实 owner projection、Tauri runtime、跨端真实 INTEGRATION 链路。缺少 live DSN 时标记 `INTEGRATION_PENDING`，缺少正式 auth/owner contract/Tauri 依赖时标记 `BLOCKED`。

## 运行与证据

本地 memory/server smoke：

```bash
cd client/solocut/server
SOLOCUT_AUTH_MODE=dev SOLOCUT_DEV_SEED=1 go run ./cmd/solocut serve
```

基础门禁：

```bash
cd client/solocut/server
go test ./... -count=1
go vet ./...
CGO_ENABLED=0 go build ./cmd/solocut
go run ./cmd/solocut version
go run ./cmd/solocut doctor
```

PostgreSQL live integration：

```bash
cd client/solocut/server
SOLOCUT_TEST_POSTGRES_DSN='<redacted-local-dsn>' \
  go test ./... -run 'Postgres|Migration|Repository' -count=1 -v
```

证据必须写入 `client/solocut/server/temp/integration-test-runs/<run-id>/`，至少包含 command、exit status、stdout/stderr、redacted env、summary 与 artifacts。真实 DSN、密码、token、Authorization、provider payload、raw prompt 和 chain-of-thought 不得写入证据。`go test ./...` 未设置 live DSN 时的 PostgreSQL skip 只能记为 `INTEGRATION_PENDING`；必须用配置 DSN 的独立运行证明 live PostgreSQL。

不运行 race。PostgreSQL integration 使用 disposable PostgreSQL 或 `SOLOCUT_TEST_POSTGRES_DSN`，不能用 SQLite 冒充。
