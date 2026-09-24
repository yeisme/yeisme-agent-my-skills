# Project Development Skills

项目级开发路由模块。`project-development-router` 先在 `quick-demo`、`full-project` 和 `workflow-off` 三种模式间选择，再判断直接本地实现、规格驱动、API 并行工作或垂直切片交付。完整流程渐进加载，不替代代码 Owner、测试证据或外部动作审批。

`delivery-phase-contract` 把跨端请求收窄为单一阶段任务：`CONTRACT`、`FRONTEND`、`BACKEND` 或 `INTEGRATION`。每端独立开发、独立验收，合同在单端阶段只读，Mock 由合同派生，本端通过只记 `PHASE_PASS`，未执行的联调记 `INTEGRATION_PENDING`。规则真源为仓库 `docs/workflows/phase-scoped-delivery.md`；流水线角色分工见 `agent-pipeline-development-constraints`。

