---
name: dsh-plugin-development
description: "Use when building, reviewing, or cleaning up a DeepSeek Harness (DSH) plugin (DSH 插件): choose official client surfaces, register conversation/right-pane tabs and global pages, expose host RPC/media/projections, test a lazy-CJS bundle, and prevent custom tab/pane/window systems."
---

# DSH Plugin Development

用于 DeepSeek Harness（DSH）host/client 插件的设计、实现、清理和评审。先选官方表面，再写内容；不要用自建 Workspace/tab strip/pane 复制 DSH 窗口系统。

## 先判断表面

| 需求 | 官方机制 | 边界 |
|---|---|---|
| 左侧栏全页/项目工作台 | `sidebar.panellist` + `main` keyed slot | global panel；一次一个主页面 |
| 会话内主区域视图 | `conversation.view` | session-scoped view ring；不要和全局页重复 |
| 会话右侧监视器 | `ctx.sidebarRightTabs` + `sidebar.right.pane.tab` + dockkit | tab strip/split/float/fullscreen 都由 DSH 提供 |
| Header 动作 | `conversation.session.header.utilities` | 打开右侧 pane 或轻量动作 |
| Agent 实时状态 | Session Projection + `useProjection` | 只导出脱敏、有界字段 |
| 数据/媒体 | host RPC + opaque media token | 不读 owner 私有状态/凭据 |

**先决定表面模型，再写组件。** 同一职责只给一个主入口；不要让全局页、conversation view、右栏 tabs 三套同时承载项目。

## 两条硬规则

1. **不自建 tab/pane/window 系统。** 不写 dock、tab strip、split、float、fullscreen、theater overlay、icon rail；这些属于 DSH 官方组件。右侧 pane 只用官方 dockkit，打开新 pane 用 `openTab(kind, { preferNewPane: true })`。
2. **页面内 tabs 不是 dockable tabs。** 全局面板没有公开 page-tabs slot 时，页面 tabs 只能是 section navigation：不拖拽、不 pin、不 split、不 detach。需要停靠/并排时回到官方右侧 pane。若 DSH 提供 page-tabs primitive，再迁移。

## 官方 surface 速查

- **Global page**：`ctx.sidebar.panellist.register` + `main` keyed slot；页面占据主区域，右侧栏在 global panel 期间不挂载；页面自己负责 header/tabs/content，但不得自建窗口 chrome。
- **Conversation view**：`ctx.slots.inject('conversation.view', () => ctx.slots.register({ name, id, order, locale, label, inject }, View))`；view 是 session-scoped，可用 `useProjection`。
- **Right pane**：`ctx.sidebarRightTabs.register({ id, kind, title, guide })` + `ctx.slots.register({ name: 'sidebar.right.pane.tab', key: id }, Body)`；body 只做内容，不自带页面标题/页脚/tab bar。
- **Header**：`conversation.session.header.utilities`；按钮打开 Companion，不做第二套导航。
- **Projection**：host 定义 schema/init/fold，client 用 `useProjection`；最多导出工具名/状态/时间/token，不导出参数、结果、prompt、路径、provider payload。

## 设计页面/Tab

写实现前先给用户看：

1. **表面模型**：项目页、Conversation、Companion 各自职责；不重复。
2. **左上角入口**：位置、图标、active、折叠态、首次使用 setup。
3. **页面构图**：header 高度、tab strip 高度、content 宽度策略、detail drawer 是否可接受。
4. **Tab 行为**：列表、默认、计数/错误点、键盘、溢出、持久化；明确不做 drag/pin/split。
5. **状态**：loading/empty/error/partial/no-owner；不伪造数据。
6. **视觉**：片场工作台而不是后台管理；用 DSH token；少卡片、少渐变、真实媒体。
7. **响应式/无障碍**：ARIA tablist、焦点顺序、对比度、reduced motion。
8. **官方映射**：每个能力对应哪个 slot；没有官方 slot 时写清取舍。

设计未确认前只保留 foundation：host/client `apply` 为空，不预埋半成品 UI/RPC/adapter。

## Host/client 合同

- 单包同时提供 host（`lib/index.js`）和 client（`lib/client.js`，`window.__ModuleLoader__.load({id,factory})`）。
- `dsh.bundle.patch` 自引用插入 row；client 基线模块 external，不打包第二份 React。
- Host 用直接 argv（无 shell）调用 owner CLI；认证 RPC 用精确 fetch route；媒体用短时 opaque token + realpath allowlist。
- Client 不接触 service token；付费动作必须 preview → confirm；未知成本/结果不得自动重放。
- 领域状态、凭据、付费门留在 owner；插件只做组合、投影、媒体代理和 handoff。

## 验证

```bash
pnpm typecheck
pnpm test
pnpm build
pnpm pack:plugin
```

- **client apply 单测**：fake ctx 捕获 slot 注册；断言只用允许的 surface，没有 `main`/`sidebar.panellist`（除非设计明确要 global page）、没有自建 tab/pane。
- **bundle 测试**：VM 加载 lazy-CJS factory，断言 exports/apply/inject。
- **安装 smoke**：一次性 `DSH_HOME`/profile；验证 guide、官方 split、native fullscreen；不修改当前 `web` profile。
- **OpenSpec**：`openspec validate <change> --strict --no-interactive`。
- **视觉**：设计稿/线框图先评审；view ring 的视觉验证需要真实历史会话，空白 hero 不显示。
- 不运行 race；不打印 secrets。

## 反模式

- 自建 Workspace/tab strip/icon rail/三栏 pane/theater：已证明会返工。
- 用全局页、conversation view、右栏 tabs 同时放同一项目内容。
- 把服务 readiness 卡塞满首页；服务是数据源，不是工作流。
- 在空白 hero 假设 view ring 可见；在无模型 profile 声称 live Agent 遥测已验证。
- 页面 tabs 做 drag/pin/split；这是 dockable tabs 的能力，不属于 page section nav。
- 为了“看起来快”造 fixture/假 stage/假 asset；无数据就显示 setup。

## Media Studio 参考

- Foundation：`cli/dsh-media-studio/docs/foundation.md`
- 页面/Tab 设计：`cli/dsh-media-studio/docs/design/page-and-tabs.md`
- 线框图：`cli/dsh-media-studio/docs/assets/foundation-page.svg`
- 当前只保留 foundation；设计评审后再创建实现 change。
