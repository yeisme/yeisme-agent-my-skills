---
name: muweave-frame-studio-shell
description: Use when implementing or reviewing the MuWeave Frame Studio App Shell while preserving owner boundaries, safe projections, desktop workbench layout, responsive states, and accessible recovery behavior.
---

# 幕织 Frame Studio App Shell

## 目标

实现「幕织 / MuWeave · Frame Studio」的桌面创作壳层。客户端只拥有路由、导航、Pane layout、筛选、主题、可访问性和安全 projection 组合；Auctra、Scaena、Eikona、Sonora 继续拥有领域事实。

## 固定基线

- React + TypeScript + Vite + Tailwind v4。
- Phosphor Icons 单一图标族。
- 208/48px 全局导航、232px 上下文目录、348px Inspector、56px 顶栏。
- 浅色为默认；色系低饱和、**不含橙色 / 珊瑚**（和 Claude 撞色，用户明确不要）：行动色是偏灰的暮紫（OKLCH 色相 308，彩度 ≤ 0.08），只用于行动与当前选择，状态色另用鼠尾草绿 / 赭金 / 胭脂红 / 雾蓝。颜色只走 `src/styles.css` 的 token，不在组件里写十六进制；`src/styles.tokens.test.ts` 守对比度与色相。状态不只靠颜色（形状图标、文字），一个概念一个 Phosphor 图标。不使用大 Hero、统计卡墙或 provider 一级 Tab。
- `#/home` 等 hash route 与原型保持兼容。

## 合同边界

- 只消费 `ShellProjectionV1`、`CapabilityState`、`PaneLayoutV1` 和 owner action descriptor。
- 不读取 owner 私有目录、数据库、凭据、Prompt、provider payload 或领域状态机。
- Mock 只能在开发模式且 URL 明确为 `?mode=mock` 时启用；live/empty 不得静默回退。
- 所有未知、stale、partial、offline、permission 和 contract mismatch 必须保留明确状态与恢复动作。

## 验收

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run test:e2e
bun run build
```

Playwright 至少覆盖 1440×900、1280×800、1024×768、键盘导航、Escape 焦点恢复、主题和 reduced motion。测试证据写入 `temp/integration-test-runs/<run-id>/` 并完成敏感内容脱敏。
