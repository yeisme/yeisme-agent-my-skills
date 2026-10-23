---
name: anatomia-video-analysis-router
description: Use when logging in with an Anatomia service access key and analyzing an authorized local video through the Anatomia CLI.
---

# Anatomia Video Analysis Router

先核对当前安装版 `anatomia --help`。当前六资源 CLI 已验证的发现路径是：

```bash
anatomia source list --agent
anatomia source describe --help
anatomia completion doctor zsh --agent
```

从 `fact.source.N.id` 读取真实 source ref，然后使用 `anatomia source get <id> --json` 或 `anatomia source describe <id> --agent`。解析失败报告版本/合同问题，不猜人读表。`source register`、`analysis decompose` 和 `understand` 是独立业务动作；实际分析仍需要用户的素材和调用授权。

当前源码不提供旧 `login` / `analyze file` 路径。远程 CLI 使用既有 `ANATOMIA_API_ENDPOINT`、service-key file 配置，不把配置来源当作登录或分析成功。旧 breakdown、package、handoff、delivery、learning 命令片段是历史合同，当前不可执行；需要这些能力时先核对 owner 的六资源与 export 合同，不反复猜测子命令。

已登记 ref 的证据解释按需交给 navigator/reviewer/export 技能。模型输出是候选观察；不直接改 Scaena canonical，也不把素材分析等同于作者验收。Skills 不安装产品二进制、凭据或服务。

## Authorized development and acceptance

When used to complete a development or acceptance task, continue through implementation, real execution, result readback, content checks, repairs, and verification within the user's authorized scope. Do not stop at a prepared config or a passing mock. Reuse current authorization rather than asking again for each necessary model call.

If the user waives cost limits, missing prices, balance lookup, token-cost estimates, or settlement must not block functional acceptance. Record returned usage when available and leave unknown cost unknown. Do not carry a superseded one-call limit or blanket no-retry/no-model-change rule into later work. Necessary retries and suitable configured model/channel changes may proceed within the authorized data boundary; record the actual target and reason. Repeated identical failures need diagnosis, not an unproductive call loop.

Read back an in-flight or unknown operation before repeating that same work. An unresolved historical operation does not freeze independent development or separate acceptance tasks. If an old runtime cost gate contradicts the current task, route its scoped implementation fix to the owner; never fabricate a price, approval, or success to pass it. This guidance does not authorize unrelated production changes, purchases, publication, or data exposure.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| No login or key | 核对当前 endpoint 与 service-key file 来源；旧 login 不可用 | Skills do not install the binary or any key |
| Registered-ref question, review, or export | Hand off to navigator / reviewer / handoff-builder | Do not invent an MCP analysis path |
| Model output | Treat as a candidate observation | Do not write structured Anatomia state by hand |
