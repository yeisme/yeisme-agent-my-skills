# modular-tiered-ci-cd Specification

## Purpose
TBD - created by archiving change skills-modular-tiered-ci-cd-v1. Update Purpose after archive.
## Requirements
### Requirement: 项目必须按场景选择 CI 级别

`Yeisme Skills` MUST 对普通 PR 运行 quick，对默认分支和高风险配置变化运行 full，并在存在 integration runner 时将真实依赖或长链路测试放入独立 integration workflow。

#### Scenario: 普通 PR

- **WHEN** PR 只修改普通源代码
- **THEN** quick 运行项目声明的快速命令
- **AND** 不触发正式发布

#### Scenario: 高风险配置变化

- **WHEN** PR 修改 workflow、dependency/lock、schema/contract、migration 或 release config
- **THEN** full 运行完整项目门禁

### Requirement: 发布必须保持 tag 与 snapshot 分离

项目 MUST 仅允许 SemVer tag 进入正式 publish；manual dispatch MUST 只执行 snapshot 或验证。

#### Scenario: manual dispatch

- **WHEN** 操作者手动触发 release workflow
- **THEN** 只生成 snapshot
- **AND** 不创建正式 Release 或跨仓写入

