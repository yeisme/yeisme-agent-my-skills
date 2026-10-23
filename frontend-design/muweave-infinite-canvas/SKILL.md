---
name: muweave-infinite-canvas
description: Use when designing or implementing MuWeave's node-first infinite canvas with safe projections, UI-only view state, story references, keyboard interaction, and responsive workspace behavior.
---

# 幕织无限画布

## 目标

把 Scaena 生产画布（`production_canvas.v0.2`）实现为 MuWeave 的 Canvas feature package。它是故事关系与制作引用工作台（发散、探索），分镜是收敛工作台；画布不是通用白板，也不拥有正文、媒体或生成状态。设计基线是 Open Design 项目 `manju-infinite-canvas`（基于产品原型 `drama-development-center-unified` 的画布）。

## 先读的来源

- `client/muweave-frame-studio/docs/design/infinite-canvas-v2-ui-spec.md`
- `client/muweave-frame-studio/docs/architecture/production-canvas-contract.md`
- `client/muweave-frame-studio/src/contracts/canvas.ts`
- `client/muweave-frame-studio/src/adapters/canvas-fixture.ts`、`canvas-http.ts`、`manju-sample.ts`
- `client/muweave-frame-studio/src/shared/generation/machine.ts`
- Open Design `manju-infinite-canvas` 的 `docs/ui-spec.md` 与 `docs/research.md`

## 不变量

- 只写 `src/features/canvas/`、页面测试和页面文档；共享合同、adapter、Shell、registry、`src/shared/` 交给 L0。
- 页面只消费 `ProjectionEnvelope<CanvasWorkspaceProjectionV2>`；未知节点种类 fail closed 并计数提示，未知状态中性显示原值，不安全引用和悬空边丢弃并降级为 partial。
- 节点按 Scaena 14 种种类映射到四个视觉家族：剧情（集/场/镜）、主体与参考、生产（计划/运行/候选集/抽卡）、关卡（审阅/交付）。
- 本地只保存 `CanvasViewStateV2`：视口、选择、位置、折叠、隐藏和 ≤60 字的 UI 分组标题；禁止 Brief/Prompt、正文、凭据、媒体 blob、provider payload 和私有路径。
- Delete 只从视图隐藏；没有 owner 端点的连线、建节点、采用只显示禁用原因，不伪造成功。
- 生成 = 预检 → 显式确认 → 提交；幂等键首次预检生成、首次提交后锁定；unknown 只能用同一请求回查。
- 撤销/重做只覆盖 UI 布局操作；owner 动作以回执呈现。
- 跨页交接只用 hash 意图（`#/storyboard?focus=…&from=canvas&rev=…`），只带安全引用和 revision。

## 交互与无障碍

- 单击、Shift 多选、框选、⌘A、Esc；Space/中键/手型平移；⌘ 滚轮缩放；F 适应全部、⇧F 适应所选。
- 方向键按网格微移，拖拽吸附与对齐参考线（Alt 关闭）；多选对齐/分布；⌘Z/⇧⌘Z；⌘F 画布搜索；L 溯源高亮。
- 快捷键只在画布区域生效，输入框内不拦截，不抢 Shell 的 ⌘K 与 `?`。
- Sheet、抽屉、对话框有焦点陷阱、Escape 关闭和焦点恢复；`prefers-reduced-motion` 下不依赖动效表达状态。
- 820px 以下节点不可拖、不显示 composer；移动端只读浏览与审批。

## 必须验证

- 9 个 fixture 场景：ready、empty、partial、stale、offline、permission required、contract mismatch、unavailable、large（500 节点，渲染 DOM 节点 <200）。
- 视图状态迁移、数值边界、不安全引用过滤；布局同步冲突。
- 预检 → cost_reconfirm → 选档 → 提交 → 运行节点；unknown 回查只产生一个运行；Brief 不进入任何存储。
- 送往分镜与返回画布的 hash 交接。
- 1440×900、1280×800、1024×768、820px 和 390px；浅色/深色。
- 证据写入 `temp/integration-test-runs/<run-id>/`，不得包含 secrets、Prompt、Provider payload 或完整推理。

真实命令：

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run build && node scripts/assert-production-boundaries.mjs
MUWEAVE_E2E_PORT=4253 node scripts/run-e2e.mjs tests/canvas-workspace.spec.ts
```

本地 live：`SCAENA_DEV_PROXY_TARGET` + `SCAENA_DEV_PROXY_TOKEN` 启动 dev server 后用 `?mode=live&facade=/__dev/scaena&project=…&episode=…#/canvas`，只验证读取、布局与预检。

禁止 race 检测、真实 Provider 调用、真实生成提交、生产部署和跨 feature import。
