---
name: muweave-page-lane-delivery
description: Use when designing or implementing parallel MuWeave Frame Studio page lanes with isolated feature ownership, shared contract freezes, safe projection boundaries, and integration evidence.
---

# 幕织页面 Lane 交付

## 核心规则

- 页面实现位于 `src/features/<page-id>/`，不得把业务 UI 继续堆进 `src/app-shell/Shell.tsx`。
- 页面之间禁止互相 import；跨页面行为走 `route-intents` 或 owner action descriptor。
- 共享合同、路由、Shell、shared UI 和全局 tokens 由 L0 集成 owner 单独维护。
- Mock 只用于显式开发模式；live/empty 不得静默回退。

## 页面包

每个页面至少包含 `index.ts`、`page.tsx`、`contract.ts`、`projection.ts`、局部 `state.ts`、私有 `components/` 和 `__tests__/`。页面导出 `PageModule`，由 registry 或自动发现接入。

当前默认使用显式 `src/pages/registry.tsx`；自动发现必须另立变更。`library` 是 L8 的 development-only feature，不进入正式导航。页面首轮必须提供可浏览的 empty/unavailable skeleton、projection blocker 和 disabled owner action，不接入真实 owner API。

## 并行边界

L1 Home/Projects、L2 Analysis、L3 Script、L4 Canvas、L5 Storyboard/Director、L6 Audio/Assets、L7 Tasks/Reviews、L8 Settings 可以并行；它们只能修改自己的 feature 目录和测试。不得同时修改 `Shell.tsx`、`routes.tsx`、`registry.tsx`、`contracts/` 或共享 `styles.css`。

## 验收命令

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run test:e2e
bun run build
```

页面 lane 的集成证据必须写入独立的 `temp/integration-test-runs/<run-id>/`，并保持 secrets、Prompt、Provider payload 和完整推理脱敏。

首轮页面验证使用单 worker smoke：

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
MUWEAVE_TEST_EVIDENCE_DIR=temp/integration-test-runs/page-lane-smoke \
bunx playwright test tests/page-lanes.spec.ts --project=desktop-1440 --workers=1
```
