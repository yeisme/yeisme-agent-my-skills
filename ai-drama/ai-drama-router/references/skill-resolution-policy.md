# AI 做剧 Skill 渐进解析与启用政策

## 目标

让用户只调用 `ai-drama-router`，同时保持 active runtime 小。Agent 负责语义选择；宿主只通过已声明的 capability adapter 完成确定性发现、一次性加载、持久化启用、回滚和验证。

Router 不假设任何仓库布局、脚本名称、运行时目录、profile 文件格式或安装工具。

## 宿主能力词汇

宿主可以声明以下能力；名称表达合同，不要求采用特定实现：

- `skill_catalog.lookup`：按名称查找可信本地 Skill source、版本和 digest。
- `skill_runtime.inspect`：判断 Skill 是否 active，以及来自哪个 scope/source。
- `skill_loader.load_once`：在当前任务中按需加载一个已审查的本地 Skill。
- `skill_activation.preview`：预览持久化启用或移除，不改变状态。
- `skill_activation.apply`：在明确授权后执行持久化启用或移除。
- `skill_activation.rollback`：恢复变更前状态。
- `skill_package.inspect`：检查外部 package 的来源、版本、权限、工具和冲突。

宿主未声明某项能力时，Router 返回 proposal 或 fallback，不发明命令、路径或工具。

## 解析顺序

### 1. `active`

宿主运行时已经声明匹配 Skill。记录 source ref、scope、version/digest 和宿主 capability receipt；不要重复启用。

### 2. `resolved_local_on_demand`

Skill 未 active，但宿主可信本地 catalog 能解析，且允许 `load_once`。读取且只读取匹配 `SKILL.md` 与本轮需要的 references，不修改持久化配置。

这是一次性任务的默认结果，不应称为“下载安装”。

### 3. `needs_profile_promotion`

该状态名为 v1 兼容字段，语义是“需要宿主持久化启用”，不要求宿主真的使用 profile 文件。仅在以下情况生成 `SkillActivationPlan`：

- owner 会话启动时必须知道该约束；
- 同一项目或 workspace 高频重复使用；
- 未持久化导致持续漏路由或违反 owner 不变量；
- 宿主策略明确要求该 Skill 启动时 active。

先请求 `skill_activation.preview`。只有当前用户明确授权后，宿主才可以执行 `skill_activation.apply`。

### Activation scope

按最窄范围选择：

- `session`：当前会话临时加载；默认优先。
- `project`：单个创作项目高频使用。
- `workspace`：同一工作区的 owner 不变量。
- `global`：仅当宿主策略和用户明确要求时使用。

项目创作能力不得因为“可能以后使用”自动扩大到 workspace 或 global。

### 4. `needs_install_decision`

active runtime 与可信本地 catalog 均无匹配能力时停止。输出缺失能力、普通 Agent fallback、候选来源要求、固定版本、权限/工具假设、冲突和 canary scope。

外部安装必须独立授权。宿主需要先 `skill_package.inspect`，再由自己的安装能力执行；Router 不联网下载、不选择包管理器，也不生成宿主私有命令。

## `SkillActivationPlan`

计划至少包含：

- `skill_name`、`source_kind`、`source_ref`、`version_or_digest`；
- `current_status`、`desired_status`、`reason`、`expected_frequency`；
- `activation_scope`、`adapter_capabilities`、`authorization_state`；
- `preview_action`、`apply_action`、`rollback_action`、`validation_action`；
- `conflicts`、`security_review`、`status`。

兼容旧宿主时 MAY 附带 `target_profile`、`dry_run_command`、`apply_commands`、`rollback_commands` 或 `validation_commands`，但这些字段只能由宿主 adapter 填充，Router 本身不得生成私有路径或命令。

`authorization_state` 使用 `not_requested`、`requested` 或 `approved_current_request`。不得从“一键做剧”“继续”或启动生产推断持久化启用、外部安装或 provider 调用授权。

## 热切换和漂移

- 活动 production run 固定 Skill name/source/version/digest。
- source 或 activation 变化只使未开始的相关 stage `stale`；运行中或已完成 Owner job 保留原 lineage。
- 不同时加载同名 Skill 的两个版本。
- missing、conflict、quarantine、工具缺失或权限不符时使用普通 Agent fallback，不自动降低安全边界。

## 禁止事项

- 不批量激活“全套短剧 Skills”。
- 不把自然语言分类、剧型判断或固定评分写进 CLI、脚本或 adapter。
- 不猜测宿主目录、配置文件、profile 机制或安装命令。
- 不因 source discovery 自动获得外部安装、更新、执行或生产权限。
