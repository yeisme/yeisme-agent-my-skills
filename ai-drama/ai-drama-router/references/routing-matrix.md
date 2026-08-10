# AI Drama Routing Matrix

路由器只选择一个 primary skill 和最多一个兼容约束。复杂任务由 `ai-drama-production-orchestrator` 编排，不由 router 直接并发写作。

## 交互模式

- `guided_conversation`：提案、解释、结构化草稿和 C0–C3 确认。
- `assisted_batch`：用户确认阶段后，运行有界候选、评估、导入和异常恢复。
- `unattended_batch`：只有明确授权、预算、质量和异常策略都冻结后才允许异常驱动运行。

## 需要立即阻塞的信号

- 没有 CanonSnapshot 或输入 revision；
- 需要改 canonical screenplay、ProductionGraph 或 asset acceptance；
- provider/cost/rights/credential capability 未知；
- subject/style/reference 未冻结或 preflight 已过期；
- 请求要求复制具体作品的台词、场景或镜头序列。
