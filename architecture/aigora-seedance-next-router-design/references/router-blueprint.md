# 下一代 Seedance 路由蓝图

## 决策顺序

```text
request -> CapabilityIR
        -> filing/authorization/asset/safety/quota/budget/incident eligibility
        -> ranking eligible channels only
        -> reserve budget + create idempotent job
        -> create sticky attempt snapshot
        -> adapter submit
        -> accepted | UNKNOWN_ACCEPT | typed failure
        -> callback/poll reconciliation
        -> artifact mirror
        -> ledger/trace/scorecard facts
```

## Eligibility matrix

| 类别 | 必须检查 | 拒绝后的记录 |
| --- | --- | --- |
| Channel | capability、model family、site/region、stage、health | redacted eligibility reason 与 channel ref |
| 合规 | filing/business profile、授权主体、callback domain、content policy | reason code、profile ref、audit ref |
| 资产 | 输入 ref、mirror/下载、MIME、size、duration、hash、retention | asset readiness reason 与 artifact ref |
| 控制 | quota、rate limit、预算 reservation、并发、incident freeze | policy reason、route/incident ref |
| 安全 | input labels、blocked reason、manual review gate | redacted safety result 与 review ref |

## Job 与 attempt 不变量

- 一个 idempotency key 对应一个 gateway job；不因网络不确定性创建重复 job。
- 一个 attempt 固定 channel、profile、route version、credential/site-account ref snapshot 和 provider task correlation。
- callback、poll、cancel、mirror 只操作匹配的 sticky attempt。
- provider 接受状态不明时进入目标状态 `UNKNOWN_ACCEPT`，先对账后重投。
- retry 需要 typed retryable error、cost guard、attempt/elapsed limit 与 fallback policy；adapter 不能自行切 route。

## Callback 与产物

- callback 先验证 attempt 关联、签名、时间窗、nonce/source 与幂等 key，再写入审计事实。
- provider success 与 artifact availability 分开：必需 mirror 失败必须可见为 `mirror_failed` 或受控失败，不能伪造可用 artifact。
- ledger 按 estimate/reservation/commit-intent/observed/reconciled 追加；trace/workbench 只消费 redacted refs 与摘要。

## 验证边界

当前可运行的基础检查是 `task smoke`、`task test`、`task test:cgo0`、`task openspec` 和 `task diff-check`。`aigora conformance run --profile seedance.b2b.video.v1 --channel ch_seedance_test --events` 是现有文档定义的目标 conformance 接口，实施与受控配置完成前不得视作可执行 live 测试。
