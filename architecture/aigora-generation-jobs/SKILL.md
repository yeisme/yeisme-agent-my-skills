---
name: aigora-generation-jobs
description: Use when a downstream agent must submit, wait, recover, or inspect Aigora generation jobs using capability-specific HTTP async, the same Idempotency-Key, and authorized artifact refs.
---

# Aigora Generation Jobs

异步生成与恢复技能。实际 generation 使用 capability-specific 已注册 HTTP endpoint。CLI `jobs` 只是 queued JobRecord / local synthetic projection，不是 provider stream 或 production evidence。

配对：先用 `$aigora-agent-core` 冻结 scope 与 discovery。R2+ 渠道/路由变更交给 `$aigora-operator-guarded`。

文档：`docs/protocols/README.md` → `downstream-agent-interaction.md`。视频 lifecycle 细节见同域 `seedance-api-contract.md`。

禁止 auto-install、auto-update、hot-update。默认无 credential persistence。输入媒体只接受当前受控 `artifact_ref` 或 trusted/protected input ref。

## 当前可运行入口

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

Video lifecycle 以已注册 HTTP 为准：`/v1/videos/{id}`、`/cancel`、`/poll`、`/reconcile`。`Prefer: respond-async` 仅在该 OpenAPI endpoint 声明支持时使用，并配同一个 scoped `Idempotency-Key`。

`/v1/jobs/{job_id}` read/cancel/events 是 recognition-only additive projection，不替代 video lifecycle。

## 恢复

1. 同一 scoped `Idempotency-Key` 必须对应相同 canonical request。超时未确认接受时保留同一 key，不得换 key 重提。
2. `409 idempotency_conflict` 停止；人工决定新 intent。
3. `unknown_accept` 或部分 stream：查询已注册 lifecycle/receipt，不静默 resubmit。
4. SSE/`Last-Event-ID` 是 opaque reconnect token。具体 cursor 值只可放在 TTL-bound protected runtime state，不得写入日志、receipt、evidence 或普通输出。
5. 终态成功只消费 authorized artifact ref 或 bounded projection。禁止任意 URL、data URL、裸 object key、provider-signed URL。

## 不要做

- 不要把 `aigora jobs ... --events` 当成 provider submission 或 production evidence。
- 不要把 CLI jobs 或 generic `/events` 当成 job-scoped video stream。
- 不要在 evidence 中写入 raw prompt、完整响应或 signed URL。
- R2+ 变更交给 `aigora-operator-guarded`，本 skill 不执行 production mutation。
