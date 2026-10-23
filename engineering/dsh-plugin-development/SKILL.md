---
name: dsh-plugin-development
description: "Use when building, reviewing, or cleaning up a DeepSeek Harness (DSH 0.2.x) plugin (DSH 插件): choose official client surfaces, register global pages / right-pane tabs, serve data through exact fetch routes, test a lazy-CJS bundle in a throwaway host, and prevent custom tab/pane/window systems. Carries the host facts verified for dsh 0.2.1-rc.2."
---

# DSH Plugin Development

用于 DeepSeek Harness（DSH）host/client 插件的设计、实现、清理和评审。先选官方表面，再写内容；不要用自建 Workspace/tab strip/pane 复制 DSH 窗口系统。下面的“已验证宿主事实”来自 `dsh@0.2.1-rc.2` 的源码与一次性宿主实测（证据与重跑脚本见 `cli/dsh-media-studio/docs/design/native-extension/`：`01-evidence-ledger.md`、`tools/verify-ledger.mjs`、`tools/spike-host-surfaces.mjs`）。宿主升级后先重跑它们。

## 先判断表面

| 需求 | 官方机制 | 边界 |
|---|---|---|
| 左侧栏全页/项目工作台 | `sidebar.panellist`（list，id）+ `main`（keyed，key = 同一 id） | 一次一个主页面；入口图标组件只收 `{ size, active }`；选中态与 hover 同一填充，插件**不能**加强调标记 |
| 会话右侧监视器 | `ctx.sidebarRightTabs` + `sidebar.right.pane.tab` + dockkit | tab strip/split/float/fullscreen 都由 DSH 提供；**右栏只在选中 Conversation 时存在**，全局页期间不挂载 |
| Header 动作 | `conversation.session.header.utilities` | 空白会话（新建对话）不显示；Companion 入口在那里只能是右栏 Start tile |
| 会话内主区域视图 | `conversation.view` | session-scoped；不要和全局页重复承载同一项目 |
| Agent 实时状态 | Session Projection + `useProjection` | 只在会话作用域槽可用；`main` 页读不到 |
| 数据 | 精确 Fetch 路由（见下） | 不读 owner 私有状态/凭据 |

**先决定表面模型，再写组件。** 同一职责只给一个主入口。

## 两条硬规则

1. **不自建 tab/pane/window 系统。** 不写 dock、tab strip、split、float、fullscreen、theater overlay、icon rail；右侧 pane 只用官方 dockkit。
2. **页面内 tabs 不是 dockable tabs。** 全局面板没有公开 page-tabs slot：页面 tabs 只能是 ARIA tablist 的 section navigation，不拖拽、不 pin、不 split、不 detach。

## 已验证宿主事实（dsh 0.2.1-rc.2）

**启用与生命周期**

- 启用：`dsh plugin --profile <p> add <目录>` 以 `link:` 安装；包自带的 `cordis.patch.yml` 即启用，无需再改 profile（SP-01）。`engines.dsh` 必须等于运行时版本。
- 全局页：`ctx.slots.inject('main', () => ctx.slots.register({ name:'main', key: ID, locale: NS }, Page))` + `ctx.slots.inject('sidebar.panellist', () => ctx.slots.register({ name:'sidebar.panellist', id: ID, order, label: () => t('panel'), locale: NS }, Icon))`。`label` 用函数，随语言即时更新（SP-16）。
- **无 URL 路由，激活面板只在内存**：重载后一律回原生首页；插件**不要**在启动时调用 `selectPanel`；`ctx.layout.selectPanel(null)` 回首页且不抛错（SP-10、SP-12）；热重载后已打开的插件页回到首页，`<style>`/入口不重复（SP-19–22）。
- 副作用一律走 `ctx.effect(() => disposer, '标签')`；`<style>` 在 effect 里创建/移除。`ctx.scope` 不可直接访问（会抛 `cannot get property "scope" without inject`）。
- locale：`ctx.locale.register(ns, { zh, en })` 要求两种语言齐备；读取 `ctx.locale.getLocale().active`；切换触发 `ctx.on('locale/change')`（SP-14、SP-15）。

**数据通道**

- **`ctx.connection.rpc.handle` 对第三方插件不可用**：注册即抛 `cannot get property "webServer" without inject`（即使声明 `inject: ['webServer']`，SP-03/04）。**不要用，也不要留回退分支。**
- 用精确 Fetch 路由：`ctx.connection.fetch.register({ path: '/api/<插件>/rpc', methods: ['POST'], requestBody: 'buffered', fetch })`（路径必须在 `/api` 下）。仅 owner 可达（无 Cookie → 401，SP-06）；客户端取消在毫秒级到达 `request.signal`（SP-05）；50 MB 缓冲体可通过（上限 300 MiB，SP-08）；**处理器抛异常会变成无正文 HTTP 400（SP-07）——必须自己 try/catch 并返回 `{ ok:false, error }` JSON**。客户端用 `fetch(new URL('api/<插件>/rpc', document.baseURI), { method:'POST', credentials:'same-origin', signal })`。
- 宿主**没有**媒体令牌；`/api/file?path=` 暴露绝对路径、整文件读入、无 Range。媒体要自建短 TTL token + realpath 白名单 + Range（见 07 §6）。
- 宿主没有面向插件的数据目录 API：偏好写 `<DSH_HOME>/plugin-data/<插件>/` 下的原子文件（临时文件 + rename，0600）；**不用 web 存储**。

**视觉与组件**

- 字号设置（10–22）**只影响会话内容**，壳与全局页恒 16px：插件用 `rem`，不随设置缩放。全局页是居中 960px 列，页边距 `0 48px 48px`，区块 gap 32px。
- 只用语义 token（`--dsw-alias-*`、`--dsw-font-family`、`--ds-font-family-code`）；不要使用值为空的 alias（`bg-l1`、`bg-layer-4`、`fill-l1`、`fill-l2`、`fill-tertiary`、`fill-tsp-secondary`、`label-quaternary`、`separator-primary`、`--dsw-focus-ring-color`）；无 spacing/density token；浅色下 `label-tertiary` 3.71:1、`label-caption` 2.13:1 不达标，次要文字用 `label-secondary`；状态色（warn/success）单独不承载含义，用形状 + 文字。
- primitives（288 个导出）无类型无文档，宿主指南禁止 `require`；种子模块只有：`react`、`react/jsx-runtime`、`react-dom`、`react-dom/client`、`@deepseek-ai/cordis`、`zod`、`@tanstack/react-virtual`、`@deepseek-ai/dsh-client-store`、`-ui-slots`、`-ui-primitives`、`-ui-dockkit`。client bundle 把它们标 external，不打包第二份 React。
- 宿主用容器查询（900/560px）；`main` 页没有宽度 hook，需要时自己用根节点 `ResizeObserver`。Chrome 145 支持 `popover` 与容器查询（SP-17/18），桌面端 Chromium 版本未验证。

**owner CLI（Media Studio 的数据源）**

- 只经 owner CLI 的 `--json`，argv 直接 `execFile`，无 shell；客户端不能提交 argv/路径。
- **“读”命令并非零写入**：Scaena/Auctra/Sonora 会建 SQLite 辅助文件，Sonora 在未初始化目录隐式建 `.sonora/`，Eikona 首次读取登记项目。调用前必须做标记文件预检（无标记不调用）并披露；文档与验收不得写“零写入”。仅 Scaena 有 `--no-remote`；其余只能标“本机调用”。Anatomia 的 `doctor`/`config` 忽略 `--help` 直接执行，不能用 `--help` 探测。

## 设计页面 / Tab

写实现前先看 `cli/dsh-media-studio/docs/design/native-extension/00-index.md`（表面模型、范围、逐页设计、状态词表、组件与 token 映射、概念图）。旧稿 `docs/design/page-and-tabs.md` 已被取代，不要当依据。要点：

1. 表面模型：项目页、Conversation、Companion 各自职责，不重复。
2. 状态：loading / empty / error / partial / stale / unknown / forbidden / needs_contract / 未初始化；“空”只在信封能证明时显示；不伪造数据。
3. 选中 = 低对比填充 + 字重 500 + `aria-selected`；展开 = 箭头 + 浅填充；不画强调色条。
4. 状态 = 图标形状 + 文字；文字动作是真按钮；辅助小字 ≥ 12px。
5. 中英文案整句 key，不拼接。

## 验证

```bash
pnpm typecheck
pnpm test
pnpm build
pnpm pack:plugin
pnpm test:integration   # 真实宿主 + 真实 owner 验收，写 temp/integration-test-runs/<run-id>/
```

- **client apply 单测**：fake ctx 捕获 slot 注册，断言注册面恰为允许的 slot（首切片：`main` + `sidebar.panellist`），没有 `conversation.view`、hero、自建 tab/pane，启动不调用 `selectPanel`。
- **bundle 测试**：在 VM 里加载 lazy-CJS factory，断言 `require` 只请求种子模块、无第二份 React。
- **真实宿主**：`DSH_HOME=<临时目录> dsh --profile P --from-default-profile web --help`（建 profile）→ `dsh plugin --profile P add <目录> --offline` → `dsh --profile P --no-open --port 0`；放在 `unshare -rn` 里断网；Playwright + 系统 Chrome。`--from-default-profile` 只拷随包模板、按 `$DSH_HOME` 解析，不读用户的 `web`。工具：`docs/design/native-extension/tools/host-harness.mjs`。
- **`web` profile**：永不修改。用户自己在跑的 `dsh --profile web` 会改写 `~/.dsh/profiles/web/cordis.patch.yml`，所以指纹要“每次运行前后各取一次”，不要跨小时对比。
- 不运行 race；不打印 secrets；`openspec validate <change> --strict --no-interactive`。

## 反模式

- 自建 Workspace/tab strip/icon rail/三栏 pane/theater；全局页、conversation view、右栏 tabs 同时放同一项目内容。
- 用 `rpc.handle` 做第三方插件通道；处理器不 catch 异常（宿主会吞成无正文 400）。
- 把服务 readiness 卡塞满首页；在空白 hero 假设 view ring 或 header 按钮可见。
- 为了“看起来快”造 fixture/假 stage/假 asset；fixture 只能由环境变量开启并带不可关闭横幅，且不得作为 owner 行为证据。
- 声称“读取零写入”“本地读取”（对没有 `--no-remote` 的 owner）；用 `--help` 探测 Anatomia。
- 对状态只用颜色；文字动作做成无边线裸文字；行选中画强调色条。
- 对“宿主盖戳 generation”的作用域做乐观更新，或在客户端自增 generation：读请求在宿主**收到时**盖戳、写入落盘后才递增，较早发出的读答复可能在写答复之后到达并把旧状态放回去。改为：等宿主答复再应用；只采纳宿主的戳；较新代数胜出，同代内后发请求胜出；只有发出时间晚于已应用答复的请求答出更低代数才当作宿主重启。
- 让焦点停在会被 re-render 卸载的按钮上而不处理（焦点掉到 `<body>`）：在页面容器上做焦点救援（被卸载的焦点元素 → 最近仍存在的有意义祖先），并让表单 / 确认条关闭时显式回到触发它的按钮；live region 每次播报换一个新节点，否则连续两次相同文案不会再读。

## Media Studio 参考

- 设计入口：`cli/dsh-media-studio/docs/design/native-extension/00-index.md`
- 首切片 change：`cli/dsh-media-studio/openspec/changes/dsh-media-studio-settings-overview-v1/`
- Foundation 说明：`cli/dsh-media-studio/docs/foundation.md`
