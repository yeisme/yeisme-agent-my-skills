---
name: aigora-operator-guarded
description: Use when a downstream agent must prepare, hand off, or verify guarded Aigora operator mutations under the R0-R4 risk model without self-approving or executing production writes.
---

# Aigora 受控运维变更交接（Operator Guarded）

用于帮管理员准备变更预览（preview）、整理变更影响并生成交接单。对于中高等风险（R2 及以上）的管理操作，Agent 只负责生成预览和交接方案，不能自己审批或直接修改生产配置。

配套技能：能力查询与回执核对请搭配 `$aigora-agent-core`。详细规范见 `docs/protocols/downstream-agent-interaction.md`。

## 风险分级（R0–R4）

| 风险等级 | Agent 允许做的事 | 必须满足的门禁条件 |
| --- | --- | --- |
| **R0（只读）** | 查询已授权范围内的状态和数据 | 服务端校验权限范围、输出脱敏 |
| **R1（低风险准备）** | 在明确授权范围内做低影响准备动作 | 受速率与预算限制、保留回执；按团队策略决定是否需人工确认 |
| **R2（受控变更）** | 仅生成变更预览（preview）和交接方案 | 必须填写原因、核对期望版本号（CAS）、附带依据并由人工确认执行 |
| **R3（高危变更）** | 仅生成交接方案并转交授权管理员 | 必须由另一名独立管理员审批并执行（双人复核），且备好回滚方案 |
| **R4（事故应急）** | 禁止自动化执行 | 按应急手册由人工值班负责人直接处置 |

注：CLI 中的 `--actor` 和 `--approve` 参数只是调用方传入的字符串标识，不能单独作为双人独立审批的证明；真实生产审批以服务端认证过的会话和审批单引用为准。

## 常用预览与核对命令

```bash
aigora mcp preview --action aigora_channel_action_preview --args '{...}' --json
aigora channels disable <channel> --reason <reason> --expected-version <version> --preview-hash <hash> --explain
aigora mcp receipt --job-ref <job_ref> --json
```

生产环境的创建 Key、调整配额、记录健康状态、启停渠道等写操作（如 `aigora_key_create`、`aigora_quota_create`、`aigora_provider_health_record`、`aigora_channel_action`）在 MCP 侧默认禁用，必须走受控的 Operator API 或 CLI 流程。

## 交接单需要包含什么

交给人工管理员的变更方案应写清楚：
1. 变更目标与所属范围（租户/工作区）
2. 风险等级（R0–R4）与变更原因
3. 当前资源的期望版本号（`expected_version`）和预览摘要（`preview_hash`）
4. 相关证据引用（`evidence_ref`）
5. 需要的独立审批人角色与回滚条件

人工管理员执行完成后，Agent 只需通过 `receipt` 接口核对最终状态和审计引用即可。

## 注意事项

- 绝不自审自批（self-approval），也不要试图用第二个会话冒充独立审批人。
- 不要把“预览成功（preview）”当成“变更已生效（committed）”。
- 不要在交接单或日志里写入密钥、原始提示词或未脱敏的请求体。


## 资源命令与版本合同

先读取安装版的 help/结构化发现面，确认 canonical 路径存在。运行 `aigora channels list --agent`，从 `fact.channel.N.id` 取真实 ID，再调用 `aigora channels describe <id> --agent`；`<id>` 是待替换的语法说明，不作为可直接执行的 Next。保持原项目、配置、过滤与权限范围。解析失败报告合同或版本问题，可查 `--json`，不要解析人读表或猜 ID。

详情类旧 show 只作隐藏兼容；正常操作使用 describe，独立 inspect/export/download 等动作保持原义。补全是同一目录的只读视图；需要安装时显式运行 completion install，并用 completion doctor 区分文件存在与 shell 可发现。源码候选通过不代表 PATH 安装版已更新。
