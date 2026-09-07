# template-registry-locale-skills Specification

## Purpose
TBD - created by archiving change template-registry-skill-en-locale-v1. Update Purpose after archive.
## Requirements
### Requirement: Agent operator 必须使用英文编译 locale
Operator SHALL 为新会话选择 `locale=en`，并 SHALL 正确处理 review-only 与 missing-English 错误。

#### Scenario: Registry 拒绝中文会话
- **WHEN** 工具返回 `TEMPLATE_LOCALE_REVIEW_ONLY`
- **THEN** Skill SHALL 改用同版本英文模板或报告缺口
- **AND** SHALL NOT 复制中文译文绕过门禁

### Requirement: 系统必须提供新模板 authoring Skill
`template-registry-template-author` SHALL 指导英文正文、中文审阅译文、CLI-authored contract 和 catalog validation。

#### Scenario: 创建新模板
- **WHEN** maintainer 请求新建 promptrepo solution
- **THEN** Skill SHALL 使用 `solution add --locale en` 与 `solution locale describe --locale zh-CN`
- **AND** SHALL NOT 手写结构化 metadata

### Requirement: 领域 Skill 必须引用统一模板 owner
Scaena 与 Eikona Skill SHALL 引用模板仓英文正文，并保留领域执行和 acceptance 边界。

#### Scenario: 领域 Agent 准备执行模板
- **WHEN** Scaena 或 Eikona Skill 选择官方 promptrepo solution
- **THEN** Skill SHALL 使用 exact `locale=en` 引用
- **AND** SHALL NOT 在 Skill 内复制模板正文或接管领域 review

