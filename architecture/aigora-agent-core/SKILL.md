---
name: aigora-agent-core
description: Use when a downstream vendor or enterprise agent must discover Aigora capabilities, establish server-derived scope, classify errors, and keep redacted receipts. Orchestrates current CLI/HTTP/MCP surfaces only.
---

# Aigora Agent Core

下游 agent 的发现与核对技能。只编排当前可运行表面，不新增协议，不持久化 credential，不把 MCP 当 primary fact。

配对：异步生成/恢复走 `$aigora-generation-jobs`；R2+ Operator mutation 走 `$aigora-operator-guarded`。不要同时加载 Operator 前端或 mcp-gateway-sidecar Operator API skills。

文档：`docs/protocols/README.md` → `downstream-agent-interaction.md`。

禁止 auto-install、auto-update、hot-update。默认无 network、无 credential access、无 production write。认证材料只由企业 secret manager 或已批准 helper 在进程内提供。

## 当前可运行入口

```bash
aigora capabilities list --json
aigora capabilities explain video.generate --explain
aigora models list --capability video.generate --json
aigora mcp doctor --json
aigora mcp tools --catalog compact --json
aigora mcp search --query models --json
aigora mcp invoke aigora.search --args '{"query":"models"}' --json
```

本地 owner 需要全量 Operator catalog 时才用 `aigora mcp tools --json`（默认 full）或 `--catalog full`。远程默认 compact，不要把本地全量目录当成远程发现。

HTTP 浅层 discovery（部署 base URL 由企业配置；不要把 credential 写入命令、文档或 evidence）：

```bash
curl --fail-with-body --silent --show-error \
  -H 'Accept: application/json' \
  'https://aigora.example.invalid/v1/capabilities'
```

远程 Operator MCP 默认 compact catalog。全量目录仅在本地 owner 或显式 `--catalog full` / `profile=legacy`。

## 循环

1. 冻结 capability、操作意图与企业 tenant/workspace/principal 上下文。scope 不明即停止。
2. 用 CLI 或 `GET /v1/capabilities`、`GET /v1/models` 发现；记录 `spec_version` 与 opaque refs，不记录 prompt/payload。
3. 认证结果只处理“已建立/未建立”。scope 必须由服务端从会话/token/policy 推导；不得把 `X-Tenant-ID` 等 caller header 当授权事实。
4. 读取走 CLI/HTTP/MCP observer 投影。MCP 是可选 bridge；receipt 以 HTTP/CLI 为准。
5. 证据只保留 request/trace/receipt refs、capability/model、redacted status。禁止 Authorization、cookie、raw prompt、provider payload、signed URL、完整 base64、opaque cursor 值。

## 错误

| 类别 | 行为 |
| --- | --- |
| 400/422 | 修正已授权 intent 后重新 discovery |
| 401/403 | 停止并交给企业 identity owner |
| 404 | 核对 scope/ref，不跨租户寻找 |
| 429 | 等待 retry-after；不绕过 limit |
| 5xx/unknown | 保留 refs，先 inspect/reconcile |

## 不要做

- 不要依赖 `/.well-known/aigora-agent.json`、`aigora agent discover` 或 `/agent/v1`。
- 不要发明通用 agent HTTP body；按具体 OpenAPI endpoint 构造。
- 不要把 `aigora mcp serve --stdio` 的本地全量 catalog 当成远程默认。
- 不要执行 R2+ production mutation；交给 `aigora-operator-guarded`。
