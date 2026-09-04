---
name: agent-workbench-product-design
description: Use when designing, implementing, reviewing, or routing Yeisme Workbench shell, navigation, Agent session, Pane/document dock, Text Development/Working Copy, candidate review, command palette, proposal authority, Team control, Owner consumer, or frontend/backend composition changes; enforces the Agent-first single-shell blueprint, shared UI governance, and owner-safe actions.
---

# Agent Workbench Product Design

适用于 `client/yeisme-workbench` 内所有主壳、导航、Agent session、Pane/document、Text Development、Working Copy、candidate review、Team control、命令面板、proposal、Owner consumer 与前后端组合的产品/设计/实现/评审工作。先用本 skill 定边界，再按任务性质配合 PRD、UI、backend 或 OpenSpec skill。

## 真源与优先级

冲突时按以下顺序裁决，历史 R0–R5、Studio、Canvas、Orbit 文档不得重新定义并列主壳：

1. `client/yeisme-workbench/docs/product/agent-workbench-blueprint.md`：应用级产品与系统组合真源。
2. `client/yeisme-workbench/docs/ui/agent-first-workbench.md`：视觉、布局、控件与响应式 UI 基线。
3. `client/yeisme-workbench/docs/interfaces/agent-pi-workspace.md`：Browser → BFF → services → Owner 前后端合同。
4. `client/yeisme-workbench/docs/design/workbench-ui-governance.md`：唯一视觉权威、Surface 分类、组件准入、状态/action 与迁移门禁。
5. 领域 UI 文档：例如 `docs/ui/text-development-workbench.md`、`docs/ui/auctra-screenplay-room.md`，只扩展内容区，不重定义主壳。
6. 视觉参考：`client/yeisme-workbench/prompts/product/ui-reference/workbench-agent-pane/deliverables/`，三张 Eikona 图，`02-plugin-pane-workspace.png` 为主基线（布局），`01` 为对话密度，`03` 为评审/证据。图片约束信息架构与密度，不是可照抄的组件规格，也不是真实运行证据。

## 不可协商的产品约束

- `/agent` 是默认入口；Agent timeline 与 composer 是不可关闭的布局锚点。
- 功能通过有界热插拔 Pane 提供：桌面默认 1–3 个可见 Pane，硬上限 4，split depth ≤ 2；重复打开只 focus 已有 Pane；超限是显式 `limit_reached`，用户关闭或显式替换，绝不静默替换。
- 平板/手机一次一个带标签 Sheet；Sheet 有 focus trap、Escape、scroll lock 与焦点恢复；桌面互补 Pane 不 trap 焦点。
- Server-authored truth：状态、权限、成本、版本、availability、unread 与 receipt 全部由服务端投影；浏览器 query、Vite var、localStorage、route state 永远不授予 capability。
- Truthful unavailable：合同不足显示 `needs_contract / permission_required / offline / stale`，禁用 mock fallback 冒充可用。
- 单一 mutation 链：所有副作用经过 用户确认 → 服务端重验 → TaskService → Owner receipt/reconcile；Review 走独立 Proposal Authority，禁止浏览器拼装 basisRefs 直接创建 Task。
- `unknown_accept` 是真实状态，只允许 reconcile，不自动重试、不伪造成功或失败。
- Owner remains owner：Workbench 只做组合体验与 typed projection / approved action / safe summary / receipt，不复制 Eikona、Scaena、Anatomia 等 canonical state，不加载 owner 私有页面。
- 旧 Studio、Orbit、Gateway 等降级为注册 Pane、advanced route 或 Owner deep link；稳定深链不得破坏。
- 状态色只用于 `ready/running/warning/blocked/stale/unknown_accept` 等语义，不使用装饰性渐变或假实时发光。
- 新 UI 必须先分类为 `core-shell|registered-pane|domain-lens|advanced-compatible|owner-deep-link|internal-evidence`，并填写视觉优先级、共享组件、主滚动 owner、状态矩阵、响应式、a11y 和例外。
- Context、Review、Version、Team 等复杂内容应进入少量稳定 deck；禁止把所有子能力铺成一排平级 tabs、卡片首页或第二业务侧栏。

## 实现红线

- Pane 只能来自 versioned registry（capability、permission、version、receipt、recovery 合同齐全）；禁止动态 import、任意 URL、shell 命令、浏览器裁定的 availability。
- `apps/web` 只经 `WorkbenchClient` typed clients 访问数据；浏览器不得直连 owner 或读取 session token。
- `service/internal/proposalauthority` 是 proposal/decision 唯一权威；accept 必须进入 `TaskService`，不得形成第二套执行状态机。
- 不引入第二个 Task/event/Context/action 客户端状态 owner；多 Pane 数据按各自 `pane.document.params` 派生。
- 新文案必须双语写入 `api/locale/source/{zh-CN,en-US}/agent/*.json` 并跑 compose；inline fallback 只是兜底，不是交付。
- integration/component/e2e 必须经 `scripts/test-evidence/run.ts` 写入 `temp/integration-test-runs/<run-id>/` 脱敏证据。
- 业务 UI 不得直接导入新的 Radix/Lucide、创建私有 token/font/modal/focus trap；先复用 design-system。只有至少两个真实消费者共享同一状态与交互语义时，feature-local composition 才能晋级全局 composite。
- 不继续扩大 `AgentConversationWorkspace` 等超大组合文件；新增 domain document、editor、candidate 或 Team surface 使用独立模块，并复用现有 session/layout/query owners。

## Text Development 边界

- Text Development 是 `agent.text-development.v1alpha1` domain-lens document，不是 `/studio` 或新的 docking shell。
- Auctra 拥有正文、Working Copy、Checkpoint、ReviewItem 与 Canon；浏览器只暂存 active editor buffer/undo/selection，saved 只来自 owner receipt。
- Conversation Runtime 拥有 Pi session、Profile/Grant、project-full retrieval、web search、visible Blocks 与 egress receipt；Working Set 是 must-use context，不是全文权限的替代品。
- Ordo 拥有 Team Profile、Plan、DAG、writer lease、run 与 evidence；Workbench 只能 preview/simulate/start/status/reconcile typed action，不能编辑 owner DAG 或创建第二 scheduler。
- Agent/Team 只产生 candidate。接受 candidate 只更新 Working Copy，不自动 Checkpoint、submit Review 或接受 Canon。
- `Create`/`Collaborate` 是同一 layout posture；四个领域 deck 为 `Structure|Review|Versions|Team`，窄屏转 labelled Sheet，action identity 不变。

## UI 组件准入

1. 先查 `design-system/primitives` 与 `design-system/composites`；已有能力直接复用。
2. 单领域结构留在 feature 目录，不把业务状态放进 design-system。
3. 至少两个真实 surface 共享同一 normalized projection、状态和键盘行为后，才晋级 composite。
4. Shared composite 只呈现，不拥有 Task、Proposal、Working Copy、candidate、Team 或 receipt authority。
5. 每个 surface 默认一个视觉 primary action；disabled 保留原因；unknown 只显示 original-operation reconcile。

## 工作流程

1. 判定能力准入 `fit | split-owner | reject-now`；用户明确要求的能力进 required-capability ledger，不得静默删除。
2. 读取 Blueprint、Agent-first UI、接口合同、UI governance 与实际 owning OpenSpec；归档 change 只作历史证据，不重新打开。
3. 清点现有组件、token、icon、motion、overlay、滚动与稳定 aria/data selector；先写 UI Contract、低保真 wireframe、component tree 和 interactive-control inventory。
4. 把 change 与当前 active specs 对齐，明确复用与 blocked owner gate。Text Development 还需对照根 `text-development-workbench-program-v1`、Auctra `auctra-text-working-copy-v1` 与 Ordo `ordo-workbench-team-control-v1`。
5. 实现遵循子项目 `AGENTS.md` 验证命令：`openspec validate --all --strict --no-interactive`、`bun run typecheck`、`bun run web:test`、`bun run test:contract`、`bun run test:integration`、`bun run web:e2e`；涉及服务端时再运行 `CGO_ENABLED=0 go test ./service/...`。
6. 完成前核对：无并列主壳回潮、无浏览器直连 owner、无第二套状态机、无新 off-system 组件、状态/响应式/a11y/locale/视觉证据分层齐全。
