# Standard 路线

## 目的

使用多个直接的本地 CLI 查询和来源专用工具，产出有来源支撑的调研、比较、核验或分析。

## 什么时候使用

- 用户要求调研、比较、分析、验证或查找最新信息。
- 重要结论需要交叉验证。
- 答案需要引用、权衡、日期或置信度。
- 结果可能指导技术、产品、法律、财务或运营决策。

如果用户明确要求 50/100/200/300 个真实案例、全网调研、生态扫描或证据矩阵，升级到 `deep_research.md`。不要用普通 standard 路线假装完成大样本研究。

## 本地 CLI 工作流

### 1. 规划搜索角度

选择三到七个聚焦角度：

```text
overview
official docs
recent changes
comparison / alternatives
implementation examples
limitations / criticism
community evidence
```

### 2. 先用来源专用工具

如果用户已经给出明确来源，先用对应 CLI/API，不要先搜索：

```bash
gh repo view mendableai/firecrawl --json name,description,stargazerCount,pushedAt,url
gh release list --repo mendableai/firecrawl --limit 10
npm view @playwright/test version time repository --json
curl -L "https://api.github.com/repos/mendableai/firecrawl" | jq '{name, pushed_at, html_url}'
```

`gh` 只负责 GitHub 来源，不是通用发现工具。目标不是 GitHub 时，不需要探测或使用 `gh`。

### 3. 再做本地搜索

来源未知或需要补充背景时，用 `firecrawl search` 做广泛发现：

```bash
firecrawl search "Firecrawl CLI search documentation" --limit 8
firecrawl search "Firecrawl alternatives Exa Tavily comparison 2026" --limit 8
firecrawl search "site:docs.firecrawl.dev CLI search scrape crawl" --limit 8
```

权威 URL 直接抓取：

```bash
firecrawl scrape "https://docs.firecrawl.dev/"
```

不要把这些步骤隐藏到本地辅助脚本里。agent 应保留可见的调研路径，这样最终回答才能解释来源、限制和置信度。

### 4. 使用结构化来源补证

如果搜索发现来源有稳定 CLI 或 JSON API，切回结构化查询补证：

```bash
gh repo view mendableai/firecrawl --json name,description,stargazerCount,pushedAt,url
gh release list --repo mendableai/firecrawl --limit 10
npm view @playwright/test version time repository --json
curl -L "https://api.github.com/repos/mendableai/firecrawl" | jq '{name, pushed_at, html_url}'
```

### 5. 验证和综合

- 优先使用官方文档和一手来源。
- 对重要结论用独立来源交叉验证。
- 记录发布时间和 “last updated” 等时效信号。
- 区分事实、解释和不确定性。
- 为每个实质性结论保留来源 URL。

### 6. 优雅降级

如果 `firecrawl` 不可用：

```bash
command -v firecrawl
curl -L "https://example.com" | head
```

然后根据需要使用内置搜索/浏览器工具。不要只因为首选 CLI 缺失就阻塞任务。

## 输出格式

```markdown
**摘要**
[3-5 句话综合]

**发现**
- [发现]（[来源]）
- [发现]（[来源]）

**证据**
- 工具：[firecrawl / gh / npm / curl / agent-browser]
- 命令类型：[搜索 / 抓取 / 结构化查询 / 浏览器交互]

**注意事项**
- [冲突、过时来源、访问缺失或不确定性]

**来源**
- [标题或域名] - [URL]
```

比较多个选项时使用表格。报告长度应和用户要求的深度匹配。

## 质量标准

- 对高影响结论使用多个来源。
- 优先使用一手来源，而不是二手摘要。
- 对不稳定主题使用新的搜索结果。
- 当本地 CLI 输出不足或不可用时明确说明。
- 如果任务需要交互、认证或动态页面状态，升级到 `autonomous.md`。
