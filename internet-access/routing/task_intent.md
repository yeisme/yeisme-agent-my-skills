# 任务意图分类

## 目的

在选择工具前，先判断用户到底想完成哪类互联网任务。工具选择必须服务任务意图，而不是反过来由工具驱动。

## 意图类型

### `lookup`

目标：查一个明确事实、当前版本、URL、发布日期、状态或简短定义。

信号：

- “查一下”
- “当前版本”
- “官网/仓库地址”
- “什么时候发布”
- “是谁维护”

默认路线：`lightweight.md`

示例命令：

```bash
npm view @playwright/test version --json
gh repo view openai/openai-python --json name,url,pushedAt
firecrawl search "Firecrawl GitHub" --limit 5
```

输出：直接答案 + 来源。

### `research`

目标：围绕主题做多来源调研、比较、背景梳理或方案判断。

信号：

- “调研”
- “比较”
- “分析”
- “有什么方案”
- “优缺点”

默认路线：`standard.md`

示例命令：

```bash
firecrawl search "Firecrawl Exa Tavily comparison" --limit 8
firecrawl search "site:docs.firecrawl.dev search scrape crawl" --limit 8
```

输出：摘要、发现、来源、限制。

### `deep-research`

目标：对一个主题做系统性、大样本、可审计的互联网研究。

信号：

- “深度研究”
- “全网调研”
- “系统性扫描”
- “找 200/300 个案例”
- “真实搜索大量实例”
- “市场地图/竞品地图/生态扫描”

默认路线：`deep_research.md` + `query_strategy.md` + `evidence_ledger.md` + `research_budget.md` + `evidence_policy.md` + `output_contract.md`

示例命令：

```bash
firecrawl search "AI coding agent startup GitHub" --limit 20
firecrawl search "site:github.com AI agent framework TypeScript" --limit 20
gh search repos "agent framework language:TypeScript" --limit 100
npm search agent framework --json
```

输出：研究问题、查询批次、候选数量、去重数量、分类统计、代表样本、证据矩阵、结论和限制。

### `verify`

目标：核验一个说法是否真实、过时、夸大或存在冲突。

信号：

- “验证”
- “是否真实”
- “是不是过时”
- “有没有依据”
- “查证”

默认路线：`standard.md` + `evidence_policy.md`

要求：

- 至少优先找一手来源。
- 对高影响结论使用多个独立来源。
- 明确冲突和不确定性。

### `extract`

目标：从 URL、API、GitHub、registry 或文档站点抽取字段。

信号：

- “提取”
- “抓取字段”
- “列出 release”
- “拿到版本/更新时间”
- “从这个 URL 读取”

默认路线：`source_priority.md` + `standard.md`

示例命令：

```bash
firecrawl scrape "https://docs.firecrawl.dev/"
gh release list --repo openai/openai-python --limit 10
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, pushed_at, html_url}'
```

输出：字段、来源、缺失项。

### `interact`

目标：打开网页并执行一次性操作，查看真实页面状态或生成证据。

信号：

- “打开网页”
- “点一下”
- “截图”
- “下载”
- “登录后查看”
- “页面上显示什么”

默认路线：`autonomous.md` + `browser_tools.md`

示例命令：

```bash
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
```

输出：工具、最终 URL、操作结果、证据路径、阻塞点。

### `automate`

目标：把浏览器或联网流程做成可重复执行的测试、监控或自动化。

信号：

- “以后反复执行”
- “写自动化”
- “做测试”
- “监控”
- “批量下载”

默认路线：先 `browser_tools.md` 探索，再按项目规范考虑 Playwright 或项目脚本。

示例命令：

```bash
npx playwright codegen "https://example.com"
npx playwright test --headed
```

输出：执行策略、是否需要项目脚本、风险和验证命令。

## 多意图任务

如果一个任务同时包含多个意图，按以下顺序处理：

```text
lookup/extract → verify → research → deep-research → interact → automate
```

示例：用户要求“验证这个库是否还活跃，并打开官网看看是否有最新文档”。先用 `gh`/registry/搜索核验活跃度，再在静态信息不足时升级浏览器。
