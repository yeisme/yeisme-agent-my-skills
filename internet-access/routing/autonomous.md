# Autonomous 浏览器路线

## 目的

处理需要浏览器交互、动态内容、认证、重复导航、下载、表单、截图或多步骤网页工作流的任务。优先直接使用已有本地浏览器和 CLI 工具；只有当用户需要可复用产物时才创建自动化脚本。工具细节先参考 `browser_tools.md`。

## 什么时候使用

- 静态搜索或抓取不足以完成任务。
- 用户要求登录、点击、填写表单、筛选、下载、监控或自动化。
- 网站依赖 JavaScript 渲染状态。
- 数据需要跨多个页面并根据页面状态分支收集。

## 本地工具优先级

优先使用本地已配置的自动化工具，因为它们可能已经具备浏览器二进制、profile、凭证和网络访问：

```bash
command -v agent-browser
command -v browser-use
command -v npx
command -v firecrawl
```

工具选择：

- 需要 AI agent 逐步观察、点击、读取页面状态时，优先使用 `agent-browser`。
- 已知、可重复、要进入测试或长期维护的工作流使用项目已有 Playwright 命令或 `npx playwright`。
- 需要视觉探索或 UI 状态不确定时，使用 `agent-browser`；如果本机没有它，再用 `browser-use` 或内置浏览器工具。
- 静态提取降级使用 `firecrawl scrape` 或 `firecrawl crawl`。
- 如果存在结构化数据入口，优先用来源专用 CLI/API，而不是浏览器自动化；例如 GitHub 才用 `gh`。
- 不要为一次性探索编写新的封装脚本。

## 工作流

1. 拆分任务步骤并定义成功标准。
2. 检查本地浏览器/搜索 CLI，并阅读 `browser_tools.md` 的工具选择规则。
3. 先尝试成本最低且可靠的路径：
   - 结构化 CLI（GitHub 时用 `gh`，包 registry 时用包管理器）
   - `firecrawl search` / `firecrawl scrape`
   - 需要交互时使用浏览器自动化
4. 保留证据：最终 URL、必要截图或下载文件、抽取出的记录。
5. 只有遇到凭证、权限、支付或破坏性操作时，才停下来向用户确认。

## 示例模式

已知静态来源：

```bash
firecrawl scrape "https://github.com/trending"
```

GitHub 结构化数据：

```bash
gh search repos "stars:>10000 language:TypeScript" --sort stars --limit 10
```

浏览器工作流：

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
npx playwright --help
npx playwright codegen "https://example.com"
browser-use --help
```

如果仓库已经提供项目专用 Playwright 脚本，优先使用项目已有脚本。

## 输出格式

```markdown
**执行摘要**
- 路线：autonomous
- 使用工具：[本地 CLI / 浏览器工具]
- 已完成：[成功事项]
- 阻塞：[失败事项或需要用户访问的事项]

**结果**
[结构化数据、链接、文件或观察]

**证据**
[截图、URL、日志或产物路径]
```

## 安全

- 未经用户明确确认，不提交购买、不可逆表单、账号变更或破坏性操作。
- 遵守 robots、服务条款、速率限制和认证边界。
- 避免把 secret 写入输出或产物。
