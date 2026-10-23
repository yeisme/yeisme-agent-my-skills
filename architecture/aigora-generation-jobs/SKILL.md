---
name: aigora-generation-jobs
description: Use when a downstream agent must submit, wait, recover, or inspect Aigora generation jobs using capability-specific HTTP async, the same Idempotency-Key, and authorized artifact refs.
---

# Aigora 异步生成任务（Generation Jobs）

用于提交、轮询、恢复和查看 Aigora 的异步生成任务（如视频生成）。真实的生成请求走对应的 HTTP 接口；CLI 里的 `aigora jobs` 命令仅用于查看本地队列记录，不代表上游厂商的真实执行流。

配套技能：
- 调用前先用 `$aigora-agent-core` 确认权限范围与可用模型。
- 涉及渠道或路由变更请交给 `$aigora-operator-guarded`。
- 接口细节见 `docs/protocols/downstream-agent-interaction.md` 和 `docs/protocols/seedance-api-contract.md`。

## 常用命令与接口

```bash
aigora capabilities explain video.generate --explain
aigora mcp preview --action aigora_video_offers_list --args '{}' --json
aigora mcp execute --action aigora_video_offers_list --args '{}' \
  --preview-ref <preview_ref> --approval-ref unused-for-read \
  --expected-revision revision:one --idempotency-key idem:one --json
aigora mcp receipt --job-ref <job_ref> --json
aigora jobs inspect <job> --json
aigora jobs wait <job> --events
```

- 视频生成任务的完整生命周期以 HTTP 接口为准：`/v1/videos/{id}`、`/cancel`、`/poll`、`/reconcile`。
- 如果接口声明支持异步响应，可带上 `Prefer: respond-async` 和固定的 `Idempotency-Key`。
- `/v1/jobs/{job_id}` 系列接口仅作为通用任务状态读取补充，不替代视频专用生命周期接口。

## 超时与异常恢复规则

1. **保持同一个幂等键（Idempotency-Key）**：同一个请求内容必须绑定同一个 `Idempotency-Key`。遇到网络超时、不确定服务端是否受理时，必须保留原 Key 去查询或对账，**绝不能换一个新 Key 重新提交**（否则可能重复扣费或重复生成）。
2. **`409 idempotency_conflict`**：说明同一个幂等键被用在了不同参数的请求上，立即停止并由人工核对。
3. **`unknown_accept` 或流中断**：先调用 `/poll`、`/reconcile` 或查 receipt 核实状态，不要直接重发创建请求。
4. **重连游标保密**：SSE 的 `Last-Event-ID` 仅在进程内存中用于断线重连，不要写进日志、回执或测试证据。
5. **只消费受控产物引用**：任务成功后只读取服务端返回的 `artifact_ref`，不要直接拼接或暴露上游厂商的临时签名 URL。

## 注意事项

- 不要把本地 `aigora jobs ... --events` 输出当成真实厂商已生成成功的证据。
- 不要在日志或证据中记录原始提示词（prompt）、完整返回报文或签名下载链接。
