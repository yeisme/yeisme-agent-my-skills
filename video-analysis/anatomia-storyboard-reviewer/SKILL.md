---
name: anatomia-storyboard-reviewer
description: Use when validating, reviewing, freezing, or forking an Anatomia storyboard revision.
---

# Anatomia Storyboard Reviewer

Validate then freeze a reviewed revision: `anatomia revision validate revision:demo --json` then `anatomia revision freeze revision:demo --expected-version 3 --reviewer reviewer:owner --evidence review-receipt:demo --json`.

Never edit accepted structured state by hand. Frozen revisions are immutable; later edits use fork. Commands: `references/commands.md`. Handoff: `references/handoff.md`.


## 当前 CLI 版本边界

当前验证入口为 `anatomia source list --agent`，从 `fact.source.N.id` 获取真实身份，再调用 `anatomia source describe <id> --agent`。旧 breakdown/package/handoff/delivery/learning CLI 片段为历史或不可用合同，不能当作现在可执行的命令；角色职责与跨 owner 能力仍保留，通过当前六资源和 export 合同继续交接。先核对安装版 help，解析失败不猜表格。
