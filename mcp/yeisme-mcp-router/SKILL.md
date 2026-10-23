---
name: yeisme-mcp-router
description: "Use when an agent is about to operate any Yeisme MCP surface — eikona mcp, gitea-mcp through the Gateway, cloudflare-api backends, or scaena mcp — and must pick the right operating skill, verify tool/action names before first use, or recover from slow multi-round MCP fumbling. Route-only: connection setup, tokens, approvals, and server administration stay in the dedicated skills."
---

# Yeisme MCP 操作路由

先选最窄的 owner 操作入口，再核验实时 tool/action 名称。紧凑工具面背后可能有大量动作；不要靠猜名字、补复数或反复探测权限来调用。

## 意图路由

| 意图 | 入口与边界 |
| --- | --- |
| Eikona 生成/编辑、artifact 交付和下载恢复 | `eikona-mcp-image`；使用 generate/edit 最短路径 |
| Eikona 审阅、反馈、资产、library、workflow、delivery、comparison、dataset、证据与诊断 | `eikona-mcp-actions`；先确认 lane 与动作卡 |
| Gitea 仓库、Issue、PR、分支和 CI | `gitea-mcp-quickstart`；search → 复制 exec_example → exec |
| Gateway 连接、token/OAuth、发现、审批与 peer-origin 错误 | `yeisme-mcp-gateway-consumer` |
| 已部署 Gateway 的 catalog、revision、approval、pack 管理 | `yeisme-mcp-gateway-operator` |
| 自建 MCP 实现 | `yeisme-mcp-builder` |
| backend registry 登记 | `yeisme-mcp-registry-onboarding` |
| Codex 客户端配置 | `codex-agent-runtime`；使用 owner 生成配置 |
| 直接 Eikona 内网 `/mcp` | `eikona-mcp-image` 后按需读 `codex-agent-runtime`；不是 Gateway |
| Scaena 官方 MiniMax H3 / Wan3、上传与任务恢复 | `scaena-production-operator`；tools/list、scaena.search、scaena://video-tasks/guide；官方 binding 的 createVideoProviderTask 不套用 Aigora URL 或 shot preflight |
| 其他 Scaena 操作 | tools/list 与可读 capability resources；本机 CLI 仅作可选辅助 |
| Auctra 文本创作 | auctra.search + auctra.execute；读 auctra://authoring/capabilities，mutations 带 idempotency_key，不写 canonical text |
| OneDrive/S3 文件上传下载、Scaena 文件引用、成品回存 | `drivebridge-operator`；稳定 drivebridge://file/<id>，字节走 owner transport，不输出临时 URL；不是 lark-drive 或 Pinax |

Gateway 源码维护、peer 和发布分别使用 `yeisme-mcp-gateway-maintainer`、`yeisme-mcp-gateway-peer-operator`、`yeisme-mcp-gateway-provider`，按需读取，不常驻加载。个人 MCP 网关能力归 `mcp/gateway`，企业 MCP 网关归 Aigora；个人项目正常维护。

## 首次调用核验

每个会话第一次 execute 前确认一次实时合同；地图只是导航，不是当前能力证明：

- Eikona：操作 Skill 的 card，或 `eikona mcp capabilities --json --full` / `GET /api/v1/mcp/actions`。
- Scaena：tools/list、scaena.search 与可读 owner resources；安装 CLI 时可用 `scaena mcp capabilities --json`。
- Auctra：已安装 CLI 可用 `auctra mcp capabilities --json`，并读 authoring capabilities；planned 动作不可执行。
- Sonora：`sonora mcp capabilities --json`，或 sonora.search 的 `types:["command"]`。
- Anatomia：已安装 CLI 可用 `anatomia mcp doctor --json` 与 `anatomia mcp capabilities --json`。
- DriveBridge：已安装 CLI 可用 `drivebridge doctor`、`drivebridge capabilities --json`，否则读 `drivebridge://capabilities`；未启用服务不会凭文档变成可写，not_probed 不等于失败。
- Gateway backend：一次 tools/list；确有需要再取 `GET /v1/tools/{name}` 完整 schema。
- Gitea：catalog search 本身就是必要发现步骤，不能跳过。

`UNKNOWN_ACTION` 或 `-32602` 类错误应重新发现，不尝试相近名称。未授权动作与不存在动作可能返回相同错误，这是存在性保护；重新检查身份与 lane，不枚举名字。动作卡含 `digest_sha256_16` 和 `generated_utc`，与 typed error 冲突时重新获取。

## 没有本机产品 CLI 的文件输入

先读已连接 owner 的 `://input/capabilities` 与 tools/list inputSchema，使用明确公布的 typed tool/action。不能要求用户安装 CLI 才能发现已有 MCP 合同，也不能把只读、未配置或旧版部署当成支持 planned 写操作。

能读取客户端文件并发 HTTP 时，以稳定幂等键准备原 input request，临时 grant URL 只在内存中消费，将字节流发送给签发 owner。不知道文件时省略 metadata，进入 awaiting_file。纯 MCP 客户端把一次性页面链接交给用户，再轮询同一个 input request；一个请求绑定一个文件，多参考图用多个请求。

grant/page URL 不进入普通日志、笔记、回执或持久化工具请求。不得猜 URL 或使用脱敏占位 URL。出现 `INPUT_LINK_RELAY_UNAVAILABLE` 时从保留临时 ResourceLinks 的客户端恢复原请求。中断后先查询原 ID；必要时用相同 prepare key 找回，再 renew/cancel/retry。输入恢复不授权重发生成。

只把稳定 owner input ref 交回原任务。上传成功不等于批准生成、分析、canonical 采用、覆盖或付款。部署状态与源码能力分别验证。

## 恢复与输出

明确当前 owner、已确认动作、scope、调用结果与恢复入口。拒绝信息保持不透明；不要在 router 内扩展连接管理、admin 或 peer 实现。有限 search 一次后使用最短操作序列，避免重复发现。
