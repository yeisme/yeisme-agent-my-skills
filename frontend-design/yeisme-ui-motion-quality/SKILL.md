---
name: yeisme-ui-motion-quality
description: Use when designing, implementing, reviewing, or debugging Web/React UI motion, including enter/exit, overlays, navigation, list reordering/filtering, hover/focus, scroll-linked effects, or reduced-motion behavior; keep motion purposeful, spatially coherent, accessible, and performant without adding a new animation library by default.
---

# Yeisme UI Motion Quality

把 Web UI 动效当作交互契约和质量门禁，而不是装饰层。这个 skill 负责审查动效是否表达了状态变化、空间关系和反馈优先级，并把问题收敛成带 `file:line` 证据的最小修复清单。

## 路由位置

普通 React/Web UI 使用以下顺序：

```text
yeisme-frontend-design-router
-> ui-spec-frontend-workflow
-> yeisme-ui-motion-quality
-> implementation
-> yeisme-frontend-quality-workflow
```

`ui-spec-frontend-workflow` 仍拥有产品视觉方向、tokens、组件状态和页面验收契约；本 skill 只拥有动效判断与动效证据。Remotion 只处理时间线视频、still 或可复用 composition，不处理普通按钮、Sheet、菜单、路由和列表过渡。

## 先确认依赖与边界

先读取 owning frontend 的 `package.json`、tokens/theme、代表性组件和已有测试。用项目实际包管理器检查已有动效能力，例如：

```bash
cat package.json
grep -RIn --exclude-dir=node_modules --exclude-dir=dist -E "motion|framer|gsap|auto-animate|transition|prefers-reduced-motion" src
```

不要因为需要动效审查就新增 `motion`、AutoAnimate、GSAP 或其它运行时依赖。优先使用现有 CSS transitions、Web Animations、Radix `data-state` 或项目已经采用的动效库；只有明确的产品需求、包体预算和回滚方案都成立时，才进入依赖评估。

## 动效决策表

| 交互 seam | 首选策略 | 必须检查 |
| --- | --- | --- |
| 内容进入/退出 | `opacity` + 小幅 `transform`，或 CSS `@starting-style` | 默认内容不能因等待动画而不可见；进入和退出要可中断 |
| Dialog、Popover、Menu、Sheet | 由触发点决定 `transform-origin`，使用原生 primitive 状态 | Escape、outside click、focus return、滚动锁定和关闭路径一致 |
| Accordion、折叠区 | height/size + opacity，优先项目 primitive 的 state 属性 | 内容可读、键盘可用、关闭后焦点不落入隐藏区域 |
| 列表新增、删除、筛选、排序 | CSS transition 或成熟的布局过渡 | key 稳定、快速连续操作可 retarget、不能造成错误的空间暗示 |
| Hover、focus、active | 颜色、阴影、opacity 或极小 transform | 键盘 focus 必须同等可见；不能只依赖 hover；不让密集表格跳动 |
| 拖拽、滑动、边界回弹 | 项目已有 gesture/spring 能力 | velocity/dismiss、边界、触摸目标、reduced motion 和取消路径 |
| Scroll-linked / parallax | 仅在信息价值明确时使用 | 主线程成本、滚动容器、低性能设备、prefers-reduced-motion |
| 循环、闪烁、自动播放 | 默认拒绝 | 只有状态监测或明确氛围价值才允许，且可暂停或静止 |

## 审查流程

1. **建立频率图。** 区分高频操作（导航、筛选、表格、命令面板）和低频时刻（首次进入、成功、空状态）。运维控制台和数据密集界面默认短、轻、可打断；不要把营销页的 stagger 或 bounce 复制进高频工作流。
2. **找出空间断点。** 搜索条件渲染、`display: none`、列表 `.map(`、Dialog/Popover/Sheet 状态、拖拽处理和 route transition。每个出现、消失、换位或从触发点展开的 seam 都要有明确的空间解释，或记录为“无动效且合理”。
3. **检查属性与预算。** 默认动画 `transform`、`opacity`、颜色和必要的 shadow；避免持续动画布局尺寸、`top/left`、大范围 blur/backdrop-filter、无界 glow 和会引起 CLS 的首屏位移。对长列表、SVG、图表和 scroll handler 重点检查重复渲染、布局测量和事件监听。
4. **检查可访问性。** 每种动效都要有 `@media (prefers-reduced-motion: reduce)` 或等效项目级策略；reduced motion 应取消位移、缩短或瞬时完成，但不能删除状态变化、焦点反馈、错误提示和内容层级。不要只在 class 添加后才让内容出现，以免 tab、SSR 或 headless 渲染得到空白内容。
5. **检查交互一致性。** 进入和退出路径应大体对称，浮层应从触发点展开，关闭后焦点回到触发点；hover、focus、active、disabled、loading、error、empty 和 mobile 状态不能互相打架。动画不能阻塞提交、筛选、导航或恢复操作。
6. **输出最小修复集。** 每条发现写出 `file:line`、用户风险、最小修复、验证命令；没有证据的问题标为假设，不把个人审美偏好写成阻断项。遇到“生硬、跳动、偶发旧内容、焦点丢失”等症状时读取 [references/motion-failure-atlas.md](references/motion-failure-atlas.md)；需要字段规则时读取 [references/motion-contract.md](references/motion-contract.md)。

## 质量规则

- 不使用 bounce、elastic、无限 shimmer 或连续装饰动画作为默认反馈。
- 不用 `scale(0)` 隐藏内容；进入/退出应保持可读的终态和可预测的 transform。
- 不用动画掩盖加载、错误、权限或数据更新语义。
- 不让动画制造布局跳动、滚动位置漂移、焦点丢失或点击目标改变。
- 不把 `will-change` 当作通用性能开关；只在可测量的短时高成本交互中使用，并在结束后清理。
- 不将 Web UI 微交互路由到 `remotion-animation-workflow`。
- 不让外部审计 skill 取代本地 tokens、组件状态、API 合同和项目测试。

## 外部 skill 的兼容用法

它们是按需审计或重构参考，不是第二套设计权威：

- `web-design-guidelines`：补充可访问性、交互状态和 Web Interface Guidelines 审计；输出应保留 `file:line` 证据。
- `vercel-react-best-practices`：只在 React/Next 性能、重复渲染、bundle、列表或动画卡顿有证据时读取相关规则。
- `vercel-composition-patterns`：只在共享组件出现 boolean props、平行组件或 Context/compound API 重构时读取；不决定颜色、节奏或动效风格。
- `find-animation-opportunities` 等动画候选 skill：可以帮助发现机会，但必须经过本地动效预算、reduced-motion 和项目质量门禁。

## 验证

先运行确定性策略扫描，再按 owning frontend 的现有命令运行最窄的检查：

```bash
bash .agents/skills/yeisme-ui-motion-quality/scripts/check_motion_policy.sh src
```

如果 owning frontend 的源码目录不是 `src`，传入实际目录。然后按项目已定义的脚本运行，例如：

```bash
bun run check
bun run test
bun run test:e2e
```

动效相关的最小证据应覆盖：

- 默认 motion 与 `prefers-reduced-motion: reduce` 各一份截图或 Playwright 状态；
- overlay、列表新增/删除/筛选、hover/focus、导航或拖拽中与任务相关的路径；
- console error、failed request、焦点回收、无障碍检查和移动端 viewport；
- 若有性能问题，记录 before/after 的渲染或交互指标，不以“感觉更顺”作为结论。

策略扫描只负责发现高置信违规，不替代 Storybook、Playwright、Axe、Lighthouse 或 owning project 的性能证据。

报告格式：

```text
file:line — finding
Risk: user-visible impact or accessibility/performance risk
Fix: smallest source change
Verify: exact project command or reproducible browser state
```
