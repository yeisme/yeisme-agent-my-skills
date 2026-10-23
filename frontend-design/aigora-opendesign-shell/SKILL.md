---
name: aigora-opendesign-shell
description: Use when implementing or reviewing the Aigora gateway console app shell sourced from OpenDesign project aigora-gateway-control-room, including MCP-first readback, Neutral shell parity, live/demo isolation, incremental module delivery, and redacted browser evidence.
---

# Aigora 网关控制台框架规范（OpenDesign App Shell）

专用于独立网关控制台（`apigateway/aigora-web-console/`）的整体框架（App Shell）开发、模块扩展与界面验收。

## 1. 设计稿读取与核对

- 以 Open Design 项目 `aigora-gateway-control-room` 为唯一设计来源，改动前先核对 `reference/WORKSPACE-EXPERIENCE-SPEC.md`、`reference/SHADCN-COMPONENTS.md`、`src/index.css` 以及原型入口源码。
- 优先通过 OpenDesign MCP 工具读取项目和文件；如果 `entryFile` 或 `list_files` 返回为空，再通过内网 HTTP raw 地址交叉核对，并在文档中说明读取范围。
- 每次同步原型改动时，更新 `reference/opendesign-source-manifest.json` 并说明本地实现与设计稿的差异。读回设计稿只代表拿到设计输入，不能代替本地构建和浏览器测试。

## 2. 界面与架构原则

- **视觉风格**：采用中性灰阶工作台（Neutral）风格——左侧导航栏（展开 240px / 收起 64px）、紧凑顶部栏（48px）、范围栏（44px）、8px 圆角以及 4 / 8 / 12 / 16 / 24px 间距体系。
- **核心布局结构**：`AppShell → ShellSidebar → TopBar → ScopeToolbar → PrimarySurface → SharedInspector`。
- **真实模式与演示模式严格隔离**：
  - 默认进入**真实模式（`live`）**，只展示后端 Operator API 返回的真实数据；未接入接口时明确显示未连接，绝不用演示数据兜底。
  - 只有显式访问 `?mode=demo`（或在设置菜单切换）才进入**演示模式（`demo`）**；演示模式只使用本地模拟数据，不向后端发送业务请求。
- **渐进接入业务模块**：完整保留 13 个功能模块和 60 个子页面的导航结构与深链跳转，各业务页面按计划逐个开发接入，不要从历史归档里直接搬回已退役的旧前端代码。
- **保持技术栈精简**：统一复用现有的 React、Tailwind CSS、shadcn/ui、Radix、Lucide、Bun、Playwright 和 Axe，不额外引入第二套组件库或动画库。

## 3. 质量检查与测试证据

在 `apigateway/aigora-web-console/` 目录下执行验证：

```bash
bun run typecheck
bun test tests
bun run lint
bun run build
CONSOLE_URL=http://127.0.0.1:4212/ bun run test:ui:shell
```

- 浏览器验证需覆盖 1440px、1280px、1024px、390px 等关键视口，检查右侧面板拖拽与键盘缩放、抽屉焦点回退、Escape 关闭、全局搜索、深浅色主题、减弱动效（`prefers-reduced-motion`）、无横向滚动条溢出以及 Axe 无障碍扫描。
- 集成与 UI 测试证据统一输出到 `temp/integration-test-runs/<run-id>/`（含标准六件套与脱敏截图）。
- 不运行 `-race`，不发起真实厂商调用，也不把演示模式页面当成生产环境已就绪的证明。
- 子项目里的 `.agents/skills/` 和 `.claude/skills/` 是自动生成目录；修改本技能源码后，在仓库根目录运行 `bash scripts/skills.sh sync-target apigateway/aigora-web-console` 同步。

## 4. 统一 Inspector 实体矩阵

右侧详情统一复用 `SharedInspector`、`EntityNav` 和 `InspectorOutline`，不要在业务页面新建局部详情栏或局部 Sheet。

| Entity | Inspector 重点 | 允许关联跳转 |
| --- | --- | --- |
| `mcp` / `agent` | safe reference、source、status、diagnostics、action boundary | capability、profile、binding、key、audit |
| `connection` | 接入、凭据安全状态、发现快照、模型选择、health、routes、operations | channel、model、route group、profile |
| `channel` | 精确调度资源、model/capability、health、route membership、revision | connection、model、route、text test |
| `route` / `group` / `profile` / `binding` | 匹配、候选、策略、消费者绑定和 revision | 各自注册的 route/channel/profile/binding |
| monitor detail | snapshot、freshness、coverage、candidate blocker、fallback、`unknown_accept` | connection、channel、route group、operation |

Connection 是业务接入级身份，Channel 是调度器的精确执行资源；发现快照是 presence evidence，不得显示为可调用或可路由资格。监控详情只读，不触发 Provider probe、自动隔离、自动恢复或路由发布。

## 5. 深链、边界与嵌套导航

- URL 只保存 `entity=<type>:<opaque-id>`，不保存凭据、raw provider payload、signed URL 或完整请求内容。
- Inspector 内关联跳转必须保留实体和返回栈；普通侧栏导航清理 entity。
- Live 无安全投影时显示 ID-only `unknown/unavailable`，不得借用 Demo 名称；Demo fixture 必须显式标识并且不发 Operator 请求。
- `ready / partial / unknown / forbidden / unavailable` 由服务端投影决定；缺失 usage、quota、health 或 route evidence 不得补成 0。
- 连接级详情与精确 Channel/Route 详情使用嵌套返回栈，刷新只替换当前投影，不重新提交任何动作。

## 6. 右侧栏专项验收

除基础 App Shell 验收外，MCP/Agent/Channel/Route 详情必须覆盖：

- 1440/1280 Dock、1024 Sheet、390 全宽 Sheet。
- Escape 关闭、焦点返回、Inspector Outline 锚点、Back、跨实体 URL 和普通导航清理 entity。
- zh-CN/en-US 长词条、深色主题、`prefers-reduced-motion`、无横向溢出和 Axe。
- Demo 无 Operator 请求；Live 不出现 Demo 文案；Live `partial/unavailable/forbidden` 保持显式。
- 浏览器证据只证明客户端投影和交互，不证明 Provider、生产权限、账本完整性或外部 Agent 成功。
