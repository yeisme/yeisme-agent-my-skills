## Why

公开聚合仓库已经是 Yeisme Skills 的发现入口，但缺少可直接管理外部项目的命令。需要提供一个薄 `scripts/skills.sh` adapter，将聚合 source checkout 与 canonical 管理引擎连接起来。

## What Changes

- 新增公共 `scripts/skills.sh`，委托 `agent-workflow/yeisme-skill-routing-governance/scripts/skills.sh`。
- 在 README 与 OpenSpec 中明确技术栈、owner 和验证命令，同时保持 `.skills/yeisme` 顶层 source 契约不新增特殊文件。
- README 增加外部项目初始化、Agent bootstrap、更新与验证说明。
- validator 检查 adapter 与 canonical 引擎均存在且可执行。

## Capabilities

### New Capabilities

- `portable-skill-manager-adapter`: 从公开聚合 checkout 管理任意外部项目的薄入口。

### Modified Capabilities

无。

## Impact

- `scripts/skills.sh`
- `scripts/validate_repository.py`
- `README.md`

不改变任何已有 Skill 目录或名称，也不扩展 `.skills/yeisme` 顶层允许文件集合。
