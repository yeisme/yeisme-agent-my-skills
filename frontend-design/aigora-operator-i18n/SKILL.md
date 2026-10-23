---
name: aigora-operator-i18n
description: Use when adding, changing, testing, or reviewing user-visible copy, locale behavior, accessibility labels, tables, forms, filters, commands, status text, or responsive layout in the Aigora Operator Console, where zh-CN/en-US parity and protocol-safe translation boundaries must be preserved.
---

# Aigora 控制台多语言与文案规范（i18n）

用于维护独立网关控制台（`apigateway/aigora-web-console/`）的中英文界面文案、状态标签与无障碍名称。

## 核心规则

- **中英词条严格对齐**：默认语言为简体中文（`zh-CN`），同时提供完整的英文（`en-US`）翻译。`src/locales/zh-CN.ts` 与 `src/locales/en-US.ts` 的键名必须完全一致（由 TypeScript 类型 `Record<keyof typeof zhCN, string>` 强制约束）。
- **只译界面文字，不译协议字段**：API/CLI/JSON 字段名、路由路径、operation ID、厂商与模型名称、能力标识（capability ID）、原因码（reason code）、资源 ID、权限标识和审计字段一律保持原样，不翻译。
- **无感切换语言**：切换语言时直接更新页面文案、URL 参数和 `<html lang>`，不刷新整页，也不清空当前打开的右侧详情面板、搜索筛选条件或表单输入。
- **统一通过 `useI18n()` 读取文案**：所有组件统一使用 `src/app/i18n.tsx` 提供的 `I18nProvider` 和 `useI18n().t()` 获取文案，导航配置通过 `src/app/navigation.ts` 中的 `labelKey` / `descKey` 关联词条，不要在业务组件里硬编码散落的中英文字符串或单独维护语言状态。
- **文案说人话**：导航标题、模块说明、按钮、表头、空状态和报错提示要自然直白，一眼看懂“当前是什么状态、下一步能做什么”，杜绝“合成数据·非后端事实”“演示壳层已加载”“供给受损”“关联洞察”这类生硬的 AI 翻译腔。
- **业务逻辑不依赖翻译文本**：权限校验、状态样式映射和筛选逻辑一律使用底层枚举值或 ID（如 `ok` / `warn` / `degraded`），不要用翻译后的中文或英文文本做判断。

## 修改流程

1. 梳理受影响页面的标题、模块说明、表头、筛选项、表单标签、空状态/加载/报错提示、弹窗文案以及按钮 `aria-label`。
2. 在 `src/locales/zh-CN.ts` 和 `src/locales/en-US.ts` 中同步新增或修改中英文词条。
3. 检查单元测试（`tests/shell-model.test.ts`）和浏览器测试脚本（`scripts/browser-app-shell.mjs`）是否有针对特定按钮名称、`aria-label` 或状态提示的文本断言，如有修改需同步更新测试脚本。
4. 检查英文长词条在窄屏（如 390px）和 240px 侧边栏下是否会溢出或挤压布局，必要时加上合理的截断（`truncate`）或换行样式。

## 验证命令

在 `apigateway/aigora-web-console/` 目录下运行检查：

```bash
bun run typecheck
bun test tests
bun run lint
bun run build
```

如果修改了关键按钮名称、导航文案或无障碍标签，启动本地服务后可运行 UI 自动化验证：

```bash
CONSOLE_URL=http://127.0.0.1:4212/ bun run test:ui:shell
```

## Inspector 与监控文案

- Inspector 分段标签使用稳定语义：`Overview`、`Identity`、`Health`、`Models`、`Routes`、`Strategy`、`Activity`、`Diagnostics`、`Technical`；领域新增分段前先检查 `InspectorOutline` 注册表。
- MCP、Agent、Connection、Channel、Route、Group、Profile、Binding 和监控详情的状态文案必须来自底层枚举映射；不能用翻译后的文字参与筛选或状态判断。
- `reason_code`、`operation_ref`、`revision`、`snapshot_ref`、`capability ID`、资源 ID、API 路径和协议枚举保持原样；解释性文案通过双语词条提供。
- 关联跳转按钮、禁用 action 的原因、Live unavailable、partial、ID-only 和 unknown 都需要中英文完整词条，并提供可读 `aria-label`。
- 390px 下长状态、英文表头、operation/snapshot 引用必须使用换行、截断或可滚动容器，不能造成页面级横向溢出。
- “已发现”“已配置”“可调用”“可路由”“已验证”“仅本地观测”必须分别表达，不将发现或本地 observation 翻译成成功状态。
