---
name: aigora-agent-core
description: Use when a downstream vendor or enterprise agent must discover Aigora capabilities, establish server-derived scope, classify errors, and keep redacted receipts. Orchestrates current CLI/HTTP/MCP surfaces only.
---

# Aigora 下游 Agent 基础交互（Agent Core）

供接入 Aigora 的下游 Agent 使用：负责查询可用能力与模型、核对服务端权限范围、处理常见报错，并保存脱敏调用回执。

配套技能：
- 提交和恢复异步生成任务（如视频生成）请搭配 `$aigora-generation-jobs`。
- 涉及高风险（R2 及以上）的配置变更预览与人工交接请搭配 `$aigora-operator-guarded`。
- 详细接口约定见 `docs/protocols/downstream-agent-interaction.md`。

安全原则：不自动安装或热更新技能；不在命令、日志或证据里保存密钥；权限范围一律以服务端返回为准。

## 常用查询命令

```bash
aigora capabilities list --json
aigora capabilities explain video.generate --explain
aigora models list --capability video.generate --json
aigora mcp doctor --json
aigora mcp tools --catalog compact --json
aigora mcp search --query models --json
aigora mcp invoke aigora.search --args '{"query":"models"}' --json
```

注：远程调用 MCP 时默认返回精简工具目录（`--catalog compact`）；只有本地管理员排查全部工具时才显式使用 `--catalog full`。

也可以直接调 HTTP 接口查询能力列表（实际域名以部署配置为准，不要把密钥写进命令行参数或文档）：

```bash
curl --fail-with-body --silent --show-error \
  -H 'Accept: application/json' \
  'https://aigora.example.invalid/v1/capabilities'
```

## 标准调用步骤

1. **确认权限范围**：先确定本次要调用的能力（capability）以及所属租户、工作区和调用身份；如果范围不明确就先停下来核实。
2. **查询可用能力与模型**：用 CLI 或 `GET /v1/capabilities`、`GET /v1/models` 查看支持的参数，只记录 `spec_version` 和资源引用 ID，不记录完整提示词或请求正文。
3. **以服务端鉴权为准**：租户和工作区范围必须由服务端根据会话或 Token 推导，不能轻信请求头里自填的 `X-Tenant-ID`。
4. **保存脱敏回执**：证据里只保留 `request_id`、`trace_id`、`receipt_ref`、调用的能力/模型名称和状态码；不要保存 `Authorization`、Cookie、原始提示词、签名下载链接、完整 Base64 或游标（cursor）明文。

## 常见错误处理

| 状态码 | 处理方式 |
| --- | --- |
| `400` / `422` | 检查并修正请求参数，重新查询能力支持范围后再调 |
| `401` / `403` | 停止重试，交由管理员检查账号或 Key 权限 |
| `404` | 核对当前工作区范围和资源 ID，不要跨租户盲猜 |
| `429` | 按 `Retry-After` 等待后再试，不要强行绕过限流 |
| `5xx` / 网络超时 | 保留原请求引用和幂等键，先查状态或对账，不要盲目重发 |

## 注意事项

- 不要依赖尚未实现的 `/.well-known/aigora-agent.json`、`aigora agent discover` 或 `/agent/v1`。
- 请求体格式严格按对应 OpenAPI 接口定义构造。
- 不要直接执行 R2 及以上的生产配置写操作，这类变更一律走 `aigora-operator-guarded` 生成预览并交由人工审批。
