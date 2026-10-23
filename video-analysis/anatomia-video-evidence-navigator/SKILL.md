---
name: anatomia-video-evidence-navigator
description: Use when a registered Anatomia source or analysis ref already exists and the user only needs one bounded probe, question, time-range inspect, or compare.
---

# Anatomia Video Evidence Navigator

Ask one bounded question on a registered ref: `anatomia video understand --source source:demo --question "What changes in this shot?" --json`.

This skill does not upload files, start analysis, accept claims, freeze revisions, or prepare handoffs. MCP is not a shipped user surface; stay on the released CLI. Commands: `references/commands.md`. Handoff: `references/handoff.md`.

For an authorized development acceptance task, one bounded question describes each operation, not a one-call limit for the whole project. Continue through result checks, necessary repairs and re-verification. Honor the user's current cost waiver: missing pricing, balance or settlement is not a functional acceptance blocker, and earlier temporary limits do not override newer instructions. Record available usage without inventing charges.

Keep the same operation identity while it is pending or unknown; do not blindly duplicate it. Independent development and separate acceptance may continue while historical operations remain unresolved. Runtime/provider configuration repairs belong to the owning implementation workflow; this skill's narrow command surface is not a reason to stop the broader authorized task. Never treat unavailable or unreviewed output as acceptance.


## 当前 CLI 版本边界

当前验证入口为 `anatomia source list --agent`，从 `fact.source.N.id` 获取真实身份，再调用 `anatomia source describe <id> --agent`。旧 breakdown/package/handoff/delivery/learning CLI 片段为历史或不可用合同，不能当作现在可执行的命令；角色职责与跨 owner 能力仍保留，通过当前六资源和 export 合同继续交接。先核对安装版 help，解析失败不猜表格。
