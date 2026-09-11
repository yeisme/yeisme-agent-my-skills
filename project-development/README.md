# Project Development Skills

项目级开发路由模块。`project-development-router` 先在 `quick-demo`、`full-project` 和 `workflow-off` 三种模式间选择，再判断直接本地实现、规格驱动、API 并行工作或垂直切片交付。完整流程渐进加载，不替代代码 Owner、测试证据或外部动作审批。

`dsh-ordo-agent-ops` 只覆盖 DeepSeek Harness 对 Ordo Agent Operations 的适配：租户上下文、快照/事件游标、runtime/lease 投影、审批、收据和对 Workbench 的交接。

`dsh-plugin-grill-me` 是 DSH 插件开发的显式质询入口：在 OpenSpec change、脚手架或实现之前，沿 DSH 插件专属 frontier（表面、owner 边界、投影、seam、形态、视觉、生命周期、验证）做依赖感知的高强度访谈。与 `grill-me` 协议成对激活，只在用户明确要求质询、挑战、压力测试或逐问时运行。
