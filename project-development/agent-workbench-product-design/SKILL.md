---
name: agent-workbench-product-design
description: Use when designing, implementing, reviewing, or routing Yeisme Workbench shell, navigation, Agent session, Pane dock, command palette, proposal authority, Owner consumer, or frontend/backend composition changes; enforces the Agent-first single-shell blueprint so parallel shells and browser-authoritative actions cannot silently return.
---

# Agent Workbench Product Design

适用于 `client/yeisme-workbench` 内所有主壳、导航、Agent session、Pane、命令面板、proposal、Owner consumer 与前后端组合的产品/设计/实现/评审工作。先用本 skill 定边界，再按任务性质配合 PRD、UI、backend 或 OpenSpec skill。

## 真源与优先级

冲突时按以下顺序裁决，历史 R0–R5、Studio、Canvas、Orbit 文档不得重新定义并列主壳：

1. `client/yeisme-workbench/docs/product/agent-workbench-blueprint.md`：应用级产品与系统组合真源。
2. `client/yeisme-workbench/docs/ui/agent-first-workbench.md`：视觉、布局、控件与响应式 UI 基线。
3. `client/yeisme-workbench/docs/interfaces/agent-pi-workspace.md`：Browser → BFF → services → Owner 前后端合同。
4. 视觉参考：`client/yeisme-workbench/prompts/product/ui-reference/workbench-agent-pane/deliverables/`，三张 Eikona 图，`02-plugin-pane-workspace.png` 为主基线（布局），`01` 为对话密度，`03` 为评审/证据。图片约束信息架构与密度，不是可照抄的组件规格，也不是真实运行证据。

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

## 实现红线

- Pane 只能来自 versioned registry（capability、permission、version、receipt、recovery 合同齐全）；禁止动态 import、任意 URL、shell 命令、浏览器裁定的 availability。
- `apps/web` 只经 `WorkbenchClient` typed clients 访问数据；浏览器不得直连 owner 或读取 session token。
- `service/internal/proposalauthority` 是 proposal/decision 唯一权威；accept 必须进入 `TaskService`，不得形成第二套执行状态机。
- 不引入第二个 Task/event/Context/action 客户端状态 owner；多 Pane 数据按各自 `pane.document.params` 派生。
- 新文案必须双语写入 `api/locale/source/{zh-CN,en-US}/agent/*.json` 并跑 compose；inline fallback 只是兜底，不是交付。
- integration/component/e2e 必须经 `scripts/test-evidence/run.ts` 写入 `temp/integration-test-runs/<run-id>/` 脱敏证据。

## 工作流程

1. 判定能力准入 `fit | split-owner | reject-now`；用户明确要求的能力进 required-capability ledger，不得静默删除。
2. 改动主壳/导航/Pane/proposal 前，先读三真源与对应 OpenSpec change（`openspec/changes/workbench-agent-pi-workspace-v1/`、`workbench-agent-proposal-authority-v1/`）。
3. 实现遵循子项目 `AGENTS.md` 验证命令：`openspec validate --all --strict`、`bun run typecheck`、`bun run test`、`CGO_ENABLED=0 go test ./service/...`（涉及服务端时）。
4. 完成前核对：无并列主壳回潮、无浏览器直连 owner、无第二套状态机、证据分层齐全。
