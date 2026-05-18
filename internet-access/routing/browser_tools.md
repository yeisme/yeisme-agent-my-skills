# 浏览器工具指南

## 目的

说明互联网信息获取任务何时升级到浏览器，以及在 `agent-browser`、项目已有 Playwright 命令、`npx playwright`、`browser-use` 和静态抓取之间如何选择。这个文件属于 `internet-access` 的升级路线，不是独立 skill。

## 总原则

浏览器不是默认搜索工具。先用搜索、抓取或结构化 CLI；只有当网页真实状态、交互或动态渲染本身是答案的一部分时，才进入浏览器。

优先级：

1. `firecrawl search` / `firecrawl scrape`：搜索和静态内容。
2. `gh` / 包管理器 CLI：结构化来源。
3. `agent-browser`：AI agent 交互式浏览、读取 accessibility snapshot、点击、截图、调试。
4. 项目已有 Playwright 命令或 `npx playwright`：可重复、可测试、可提交到项目的浏览器流程。
5. `browser-use`：当本地已配置且更适合当前环境时，用作交互式浏览替代方案。

## 什么时候用 agent-browser

使用 `agent-browser` 的信号：

- 需要打开页面观察真实 UI 状态。
- 需要根据 accessibility tree 的 `@ref` 点击、填写、翻页或读取内容。
- 需要截图、PDF、console errors、network requests 或页面状态证据。
- 任务是一次性探索，不值得写 Playwright 脚本。
- 用户要求“你打开看看”、“点一下”、“截个图”、“页面上显示什么”。

常用命令：

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser click "@e2"
agent-browser fill "@e3" "search text"
agent-browser press Enter
agent-browser screenshot /tmp/page.png
agent-browser get url
agent-browser get title
agent-browser console
agent-browser errors
agent-browser close
```

如果第一次使用或不确定命令细节，先读取本机随 CLI 安装的 core skill：

```bash
agent-browser skills get core --full
```

使用规则：

- 先 `snapshot`，再用 `@ref` 操作，不要盲猜 CSS selector。
- 对用户可见证据，优先截图或记录最终 URL。
- 涉及登录、付费、修改账号、提交表单和破坏性操作时先向用户确认。
- 不在最终回答中泄露 cookie、token、profile 路径或凭证。

## 什么时候用 Playwright

使用项目已有 Playwright 命令或 `npx playwright` 的信号：

- 浏览器流程需要反复运行。
- 结果需要纳入项目测试、QA、回归或监控。
- 页面流程稳定，selector 可维护。
- 用户明确要求“写自动化脚本”、“做测试”、“以后能重复执行”。

优先使用项目已有命令：

```bash
npm test
npm run test:e2e
npx playwright test
```

探索或生成脚本时使用：

```bash
npx playwright --help
npx playwright codegen "https://example.com"
npx playwright test --headed
npx playwright show-report
```

使用规则：

- 如果仓库已经有 Playwright 配置，遵循项目现有目录、fixtures 和命名。
- 不为一次性网页查询创建 Playwright 测试。
- 先用 `agent-browser` 探索不确定页面，再把稳定流程固化成 Playwright。

## 什么时候用 browser-use

使用 `browser-use` 的信号：

- 本机已经配置好 `browser-use`，并且它比当前环境的其它浏览器工具更稳定。
- 需要复用真实 Chrome profile 或连接 CDP。
- `agent-browser` 不可用，但仍需要交互式浏览。

常用命令：

```bash
browser-use doctor
browser-use open "https://example.com"
browser-use state
browser-use screenshot /tmp/page.png
browser-use extract "提取页面中的主要价格和商品名"
browser-use close
```

## 什么时候不要用浏览器

不要升级浏览器的情况：

- `firecrawl search` 已返回足够来源。
- `firecrawl scrape` 能提取正文。
- `gh`、`npm view`、`pip index`、`cargo search` 或 `go list` 能返回结构化答案。
- 用户只要解释、事实、比较或来源，不需要页面交互证据。

## 从搜索升级到浏览器的检查点

升级前先确认至少满足一项：

- 搜索结果指向页面，但抓取正文缺少关键内容。
- 用户关心页面上的实际可见状态，而不是文档文字。
- 需要操作筛选器、分页、菜单、登录态或下载按钮。
- 需要截图/PDF 作为证据。

如果这些条件都不满足，继续使用搜索、抓取或结构化 CLI。

## 输出证据

浏览器路线的最终回答应包含：

- 使用了哪个工具。
- 关键 URL。
- 成功完成的操作。
- 未完成或被权限阻塞的操作。
- 截图、下载文件或产物路径（如果产生）。

示例：

```markdown
**浏览器证据**
- 工具：agent-browser
- 最终 URL：https://example.com/results
- 截图：/tmp/page.png
- 限制：需要登录后才能查看完整结果
```
