# 正式项目与 MVP 工作流

仅在 `project-development-router` 已选择 `full-project` 时读取。完整流程表示每个阶段都经过判断，不表示每个 Skill 都必须运行。

## 1. Owner 与能力准入

先判断能力是 `fit`、`split-owner` 还是 `reject-now`。确认代码、文档、CLI/API/event、持久化、客户端和发布分别由谁拥有。能由现有 owner 承载时不要新建项目；只有生命周期、依赖、发布或产品边界确实独立时才创建新的维护边界。

## 2. 产品方向

用户、问题、场景或需求真实性不清晰时，使用最窄的产品方向工作流。用户已给出清晰目标、范围和验收结果时跳过，不重复进行长访谈。

市场、竞品、定价或当前采用情况会改变决策时，使用互联网研究并保留来源。普通工程事实优先从仓库和官方文档查证。

## 3. PRD 与验收

把项目压缩为一个最小完整行为：

```text
角色 → 前置条件 → 操作 → 可观察结果 → 失败恢复 → 验证证据
```

明确目标用户、Job-to-be-done、范围、非目标、成功信号、权限和停止条件。Agent 平台能力使用 `agent-platform-prd`；其它项目使用 owner 既有 PRD 或 OpenSpec 入口。

## 4. 可选质询

只有用户明确要求 `$grill-me`，或关键未决决策会改变 owner、范围或架构时才进行高强度访谈。访谈结束前不实施；需求已经清楚时跳过。

## 5. 架构、规格与兼容性

共享 UI/API/数据合同、跨项目 handoff、并行 writer、稳定公开合同或持久化边界存在时，使用 `spec-driven-feature-workflow`、owner OpenSpec 和 `yeisme-evolutionary-change-policy`。单 owner、可逆、本地非生产切片不为形式完整而制造额外层次。

需要工程或设计评审时只运行对应 review；不要默认叠加 CEO、设计和工程全链。

## 6. 新项目基础

新 Yeisme 子项目在写业务代码前建立：

- `AGENTS.md`：技术栈、owner、禁止动作、测试命令和完成标准。
- `CLAUDE.md`：指向本地 `AGENTS.md`。
- `docs/README.md`：本项目文档索引。
- `openspec/`：正式实现计划、证据和归档 owner。
- `.skills/profiles/targets/<subproject>.txt`：由根目录 Skill manager 创建和维护。
- 现有技术栈对应的最小测试、lint、typecheck 和 build 入口。

远程仓库、push、发布、部署和真实外部写入仍需要用户对具体目标的授权。

## 7. 垂直切片实现

使用 `vertical-slice-delivery` 或同等项目流程完成第一条用户可观察行为。实施时使用 Ponytail 的最小完整实现顺序：复用现有代码、标准库、平台能力和已有依赖，最后才新增必要代码。

实现期间只运行 focused tests 和当前切片必要检查。不要在每次编辑后重复全仓 lint、完整 build 或所有 E2E。

## 8. 最终验证

代码、直接测试和必要文档稳定后，才运行 owner 的完整测试、lint、typecheck、build 和集成证据门。按风险选择 `review`、`qa`、`health` 或 `cso`；不是所有项目都需要全部门禁。

`document-release` 只用于已交付代码的文档收尾；`ship` 只在用户明确要求 commit、push、PR、发布或部署时运行。

## 9. 退出与降级

用户说“跳过完整流程”“正常实现”或等价表达时，立即回到 `workflow-off`。用户把正式项目改成可丢弃验证时，切到 `quick-demo`，并标明已有产物不能直接视为生产实现。
