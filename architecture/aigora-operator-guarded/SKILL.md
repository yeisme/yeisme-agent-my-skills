---
name: aigora-operator-guarded
description: Use when a downstream agent must prepare, hand off, or verify guarded Aigora operator mutations under the R0-R4 risk model without self-approving or executing production writes.
---

# Aigora Operator Guarded

受控 Operator 交接技能。当前 operator agent catalog 与 `plan/preview` 只读。R2+ 必须由独立人类在已授权 Operator 表面执行。

配对：发现与 receipt 走 `$aigora-agent-core`。不要加载 Operator 前端实现链，除非任务是改 Aigora Operator Console 本身。

文档：`docs/protocols/README.md` → `downstream-agent-interaction.md`。

禁止 auto-install、auto-update、hot-update。禁止 self-approval、充当第二审批人、绕过 CAS，或把 preview 当 execution receipt。

## 风险模型

| 等级 | agent 可以做 | 必需 gate |
| --- | --- | --- |
| R0 | 已授权 read | server-derived scope、redaction |
| R1 | 显式 scope 内低影响准备 | rate/budget、receipt；组织 policy 可要求人工 |
| R2 | 仅 preview/plan/handoff | 人类 approval、reason、CAS/expected version、evidence |
| R3 | 仅交接给授权 Operator | 独立人类审批和执行、rollback plan |
| R4 | 拒绝自动化执行 | 事故 authority 与紧急 runbook |

当前 CLI `--actor` 与 `--approve` 是 caller-supplied strings；不能单独证明独立人类审批。企业必须提供外部 authenticated approval refs 与 approver/executor separation。

## 当前可运行入口

```bash
aigora mcp preview --action aigora_channel_action_preview --args '{...}' --json
aigora channels disable <channel> --reason <reason> --expected-version <version> --preview-hash <hash> --explain
aigora mcp receipt --job-ref <job_ref> --json
```

生产 mutation 走已审计 Scheduling/Operator 命令，不走 MCP compact execute 伪造 approval。`aigora_key_create`、`aigora_quota_create`、`aigora_provider_health_record`、`aigora_channel_action` 在 MCP 上保持 disabled。

## 交接产物

redacted plan 必须包含：目标、server-derived scope、risk、expected version、preview hash、reason、evidence refs、所需独立审批人、rollback condition。人类执行后回传 receipt；agent 只核对 terminal status 与 audit refs。

## 不要做

- 不要 self-approve 或扮演四眼中的第二人。
- 不要调用 catalog 未列出的 mutation。
- 不要把 MCP preview/execute 当 production write 授权。
- 不要记录 secret、raw prompt、provider payload 或私人 tool arguments。
