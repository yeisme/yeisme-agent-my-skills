# 来源与工具优先级

## 目的

把“用哪个工具”从固定列表改成来源驱动决策。互联网信息获取的关键不是永远先搜索，而是先判断信息最可能在哪个一手来源里。

## 总规则

优先级按来源确定：

1. 用户给了明确来源：直接使用该来源的专用 CLI、API 或抓取命令。
2. 用户只给主题：先用 `firecrawl search` 找候选来源。
3. 搜索结果指向结构化来源：切换到来源专用 CLI/API。
4. 静态内容无法回答：升级到浏览器工具。
5. 需要反复执行：再考虑 Playwright 或项目自动化。

## `gh` 是否多余

`gh` 不多余，但它不是通用搜索工具。它只在 GitHub 相关任务中优先：

- 用户给出 GitHub repo、issue、PR、release、organization 或 user。
- 搜索结果已经指向 GitHub，且需要结构化字段。
- 需要查 stars、更新时间、release、issue 状态、PR 状态、repository metadata。
- 需要避免用浏览器解析 GitHub 页面。

示例：

```bash
gh repo view openai/openai-python --json name,description,stargazerCount,pushedAt,url
gh release list --repo openai/openai-python --limit 10
gh issue list --repo openai/openai-python --state open --limit 20
gh search repos "agent framework language:TypeScript" --limit 10
```

不要在这些场景优先用 `gh`：

- 用户问的是普通网页、新闻、标准、博客、产品文档或厂商文档。
- 目标来源不是 GitHub。
- 只需要 broad web discovery。
- GitHub 页面只是搜索结果之一，还没有确定它是主要来源。

## `firecrawl` 的位置

`firecrawl` 是通用发现和静态提取工具：

```bash
firecrawl search "Model Context Protocol registry" --limit 8
firecrawl scrape "https://docs.firecrawl.dev/"
firecrawl crawl "https://docs.firecrawl.dev/" --limit 20
```

优先使用 `firecrawl` 的场景：

- 用户只给主题，需要找来源。
- 目标是网页正文、文档、博客、官方页面。
- 已有 URL，需要提取主要内容。
- 需要 crawl 文档站点。

不要在这些场景只依赖 `firecrawl`：

- GitHub、npm、PyPI、Cargo、Go module 等有结构化 CLI/API。
- 需要网页真实 UI 状态。
- 静态抓取缺少关键动态内容。

## 包管理器 CLI

包版本、发布时间、repository、依赖元数据优先使用 registry CLI：

```bash
npm view @playwright/test version time repository --json
python -m pip index versions requests
cargo search tokio --limit 5
go list -m -versions golang.org/x/tools
```

如果包管理器 CLI 不足，再搜索官方 registry 页面或源码仓库。

## `curl` + `jq`

适合已知 JSON endpoint、官方 API、健康检查或 GitHub API 降级：

```bash
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, description, stargazers_count, pushed_at, html_url}'
```

使用规则：

- 只对稳定 endpoint 使用。
- 不把 token 或私有 headers 写入最终回答。
- API 返回和网页显示冲突时，说明差异并给出来源。

## 浏览器工具

只有当页面真实状态本身重要时才升级浏览器：

```bash
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
```

如果只是为了读取静态文档，不要用浏览器。
