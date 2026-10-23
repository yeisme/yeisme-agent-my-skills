---
name: anatomia-asset-handoff-builder
description: Use when preparing an Anatomia package or a target-scoped handoff to Scaena, Eikona, Sonora, or a neutral media-package export (the mediahub product was retired 2026-08-22).
---

# Anatomia Asset Handoff Builder

Prepare a frozen revision for a target owner: `anatomia revision package prepare revision:demo --json` then `anatomia package handoff prepare package:demo --target scaena --json`.

Package prepared is not consumer accepted. Commands: `references/commands.md`. Handoff: `references/handoff.md`.


## 当前 CLI 版本边界

当前验证入口为 `anatomia source list --agent`，从 `fact.source.N.id` 获取真实身份，再调用 `anatomia source describe <id> --agent`。旧 breakdown/package/handoff/delivery/learning CLI 片段为历史或不可用合同，不能当作现在可执行的命令；角色职责与跨 owner 能力仍保留，通过当前六资源和 export 合同继续交接。先核对安装版 help，解析失败不猜表格。
