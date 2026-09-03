## Context

本 change 只拥有 `.skills/yeisme` 内的 workflow、质量命令、项目文档和验证，不把其他仓库作为完成门禁。

## Design

```mermaid
flowchart LR
  PR[PR / changed paths] --> Q[quick]
  RISK[workflow/dependency/schema] --> F[full]
  INT[integration paths / manual] --> I[integration]
  TAG[SemVer tag] --> REL[release]
  Q --> G[stable gate]
  F --> G
  I --> G
```

- Profile: `skills/content`.
- quick commands: `python3 scripts/validate_repository.py`
- full commands: `python3 scripts/validate_repository.py`, `python3 scripts/test_network_install.py`
- integration commands: 不适用
- release: No binary CD; publication follows the skills repository owner workflow.
- workflow 顶层默认只读；PR checkout 不持久化 credential。
- 手动 dispatch 不得正式发布，tag publish 必须复跑 mandatory gates。

## Compatibility

已有 workflow/job 名不删除。新增场景先以加法方式上线；如果后续迁移 branch protection，由项目 owner 单独执行。

## Rollback

如果新增 workflow 产生不可接受的重复运行，可先禁用新增 trigger 并保留原 required check；不得删除原门禁或 release history。
