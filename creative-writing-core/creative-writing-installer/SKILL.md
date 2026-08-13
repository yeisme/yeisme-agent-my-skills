---
name: creative-writing-installer
description: Use when a creative-writing, screenplay, or AI-drama route has already selected a required Skill and an agent must coordinate one-time loading, confirmed persistent activation, removal, source-pinned external package review, validation, or rollback through the host's declared capability adapter without bulk-installing a creative inventory.
---

# 创作 Skill 启用协调器

## 目标

消费 Router 已经生成的 `SkillActivationPlan`，通过宿主声明的 capability adapter 协调最小、确定性、可回滚的 Skill 启用或降级。协调器不负责理解自然语言创作任务，也不重新选择 Writer。

它不假设仓库布局、脚本名称、profile 文件、runtime 目录、包管理器或某个产品实现。

## 输入

- 已选定的 `skill_name`、目标任务、`activation_scope` 和当前 resolution status。
- source kind/ref/version/digest、预期使用频率、冲突、工具/权限需求和用户授权状态。
- 宿主声明的 catalog、runtime、activation、package inspection 和 validation capabilities。
- 可选 `DramaRoutePlan`、`CreativeRoutePlan` 或等价 route 结果。

## 决策

1. `active`：不变更，报告当前 source、scope 和 runtime receipt。
2. `resolved_local_on_demand`：通过宿主的一次性加载能力使用可信本地 source；一次性任务默认使用此路径。
3. `needs_profile_promotion`：该 v1 状态表示“需要持久化启用”；只在高频、启动必需或 owner 不变量要求时提出。先 preview，只有当前用户明确授权后 apply。
4. `needs_install_decision`：可信本地 source 缺失时停止。外部 package 需要独立授权、固定版本、完整审查和 project-scoped canary。
5. `remove`：仅在 Skill 罕见、错误 owner、已替代或造成冲突时提出，先 preview 并保留 rollback action。

## 工作流

1. 调用宿主只读 catalog/runtime capabilities，确认 source、版本、digest、当前 scope 和冲突。
2. 选择最窄 scope：`session` 优先；高频项目可选择 `project`；owner 不变量才考虑 `workspace`；除非用户和宿主策略都明确要求，否则不使用 `global`。
3. 宿主没有 `skill_activation.preview` 时只返回 proposal，不猜测命令或配置文件。
4. 先 preview，检查一个 primary/一个 constraint、无同名双版本、无 owner 冲突、工具和权限满足、rollback 可用。
5. 只有 `authorization_state=approved_current_request` 时才调用宿主 `apply` capability。
6. apply 后通过宿主 validation capability 验证 active 状态、source/version/digest 和 scope；未获得 receipt 时不得声称已启用。
7. remove 同样先 preview，再由明确授权的宿主 action 执行；失败时调用声明的 rollback capability。
8. 外部 package 先检查来源完整性、固定版本、完整说明、references/scripts、工具、权限和冲突；未通过时保持 quarantine，不进入 active runtime。

## 输出

返回 `SkillActivationReceipt` 或 proposal：

- `skill_name`、`source_kind`、`source_ref`、`version_or_digest`；
- `activation_scope`、`adapter_id`、`adapter_capabilities`；
- `before_status`、`after_status`、`authorization_state`；
- `preview_result`、`apply_result`、`validation_result`、`rollback_action`；
- `conflicts`、`receipt_ref`、`status`。

兼容旧宿主时 MAY 附带 `target_profile` 或 command 字段，但只能由宿主 adapter 生成。未实际执行时必须标为 proposal，不能声称已安装或启用。

## 质量门槛

- 不为一个请求批量启用整套小说、短剧、漫剧或自媒体 Skills。
- 不把 Agent 语义路由编码成 shell set、关键词评分或固定剧种包。
- 不发明宿主命令、目录、profile 或安装器。
- production run 中不热安装、热更新或热切换 Skill。

## 边界

- 用户授权“一键做剧”不自动等于外部代码安装、持久化 activation、provider 调用或发布授权。
- 结构化项目状态仍通过对应 canonical owner 的 CLI/API/application service 修改。
- 协调器只报告 Skill activation 结果，不声称稿件、资产或成片已经完成。
