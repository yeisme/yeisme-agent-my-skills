# portable-skill-manager-adapter Specification

## Purpose
定义公开 Skills 聚合仓库如何通过薄 CLI adapter 管理任意外部项目，同时保持 canonical 管理引擎、profile 和双 runtime 的 owner 边界。
## Requirements
### Requirement: 聚合仓库提供公共管理入口
聚合仓库 SHALL 提供可执行 `scripts/skills.sh`，默认使用当前聚合 checkout 作为 Skill source，并将命令委托给 canonical 管理引擎。

#### Scenario: 管理外部项目
- **WHEN** 用户从聚合仓库运行脚本并指定仓库外项目
- **THEN** adapter 使用聚合 source 对目标项目执行 canonical 命令

### Requirement: 未初始化 submodule 时明确失败
adapter MUST 在 canonical 引擎不存在时以非零状态退出，并显示真实可运行的 submodule 初始化命令。

#### Scenario: agent-workflow submodule 缺失
- **WHEN** 用户运行 adapter 但 `agent-workflow` 未初始化
- **THEN** 输出初始化命令且不修改目标项目

### Requirement: 文档给出 bootstrap 工作流
README SHALL 说明外部项目初始化、添加管理 Skill、同步、Agent 路由和服务器更新流程。

#### Scenario: 新项目首次接入
- **WHEN** 用户按照 README 执行命令
- **THEN** 项目获得 profile、双 runtime 和已激活的管理 Skill
