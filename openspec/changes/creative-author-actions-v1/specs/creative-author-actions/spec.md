# creative-author-actions Specification

## Purpose

把作者可见创作入口收敛为五个自然动作，并为六类内容提供最小、真实且可审阅的方法选择；本规格只约束 Skills 源合同，不代表宿主 runtime 已实现。

## ADDED Requirements

### Requirement: 作者请求必须映射到五个显示动作

Router MUST 将作者请求映射为且仅映射一个主要显示动作：写作、规划、审稿、修订或整理。输出 MUST 保留稳定的 `phase`、`operation`、`artifact`、`canonical_owner` 和 gate 字段；一次任务 MUST 只选择一个 primary skill，兼容约束仅在必要时加入。

#### Scenario: 作者请求写一章

- **WHEN** 用户要求写小说章节
- **THEN** 显示动作 SHALL be `写作`
- **AND** primary SHALL be `chinese-novel-chapter-writer`
- **AND** candidate MUST remain pending review until explicit author decision

#### Scenario: 作者要求整理资料

- **WHEN** 用户要求归档、重排或核对引用
- **THEN** 显示动作 SHALL be `整理`
- **AND** the route MUST NOT imply accept, apply, save-version, or publish

### Requirement: 六类内容必须使用内容匹配的方法

Router MUST distinguish 小说、剧本、小红书单篇、课件、PPT 讲稿和长期讲课视频。每类 MUST declare a primary method, expected artifact/checks, and an explicit boundary against unsuitable templates.

#### Scenario: 教学内容请求

- **WHEN** 用户请求课件、PPT 讲稿或课程系列视频文案
- **THEN** route SHALL use `tutorial-writer` and the shared teaching/presentation reference
- **AND** output SHALL cover learning goals, sequence, examples, steps, timing, practice and answers as applicable
- **AND** MUST NOT apply a short-video hook or forced story-conflict template by default

### Requirement: 本地与远程创作必须保持同一审稿边界

Author guidance MUST distinguish local CLI from remote MCP/HTTP discovery and invocation. Remote guidance MUST NOT require a client-side Auctra CLI or server filesystem path. Generation, accept, apply, saved version, and export/download MUST remain distinct states.

#### Scenario: 远程生成返回待审稿

- **WHEN** remote generation returns a queued or pending candidate
- **THEN** guidance SHALL use the returned ref and status/resource lookup
- **AND** SHALL wait for explicit author review before reviewer actions
- **AND** MUST NOT fabricate a receipt or create a same-named work when the service is unavailable

### Requirement: 退役入口和自然词必须可迁移

Implementation MUST provide a source-level migration plan for retired `auctra-i18n-workspace-router` and `auctra-chinese-project-starter`, and for the rename to `chinese-novel-setting-editor`. Author-facing explanations SHOULD use natural terms such as 作品说明、文风、读者、时间线/前后衔接 and actual reference-image meaning; machine schema/operation/ref and historical archive wording MUST remain stable.

#### Scenario: 精确引用扫描

- **WHEN** source implementation completes
- **THEN** owned router/reference callers MUST contain no retired skill names
- **AND** cross-owner paths MUST be handed to their owning change rather than edited here
