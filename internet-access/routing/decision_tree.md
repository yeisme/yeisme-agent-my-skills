# Internet Access 路由决策树

## 目的

选择能满足互联网信息获取或网页交互任务的最轻量路线，同时优先使用本地已配置的 CLI 工具。这个决策树用于指导 agent 判断，不要求使用辅助脚本。

## 第一步：判断任务意图

先读 `task_intent.md`，把任务归到一个主意图：

| 意图 | 典型请求 | 默认路线 |
| --- | --- | --- |
| `lookup` | “查一下 X 当前版本/URL/发布日期” | lightweight |
| `research` | “调研/比较/分析 X” | standard |
| `deep-research` | “深度研究/全网扫描/找 200 个案例” | deep_research |
| `verify` | “验证这个说法/是不是过时了” | standard |
| `extract` | “从这个 URL/API/repo 取字段” | standard |
| `interact` | “打开网页点一下/截图/下载/登录后看” | autonomous |
| `automate` | “做成以后可重复执行的流程” | autonomous + Playwright |

## 第二步：判断目标和来源

再判断任务来源属于哪一类：

- 已知来源查询：用户已经给出 GitHub 仓库、包名、URL、API endpoint 或具体网站。
- 未知来源发现：用户只给主题，需要找资料和来源。
- 核验/比较：用户需要多来源证据和结论。
- 网页交互：用户需要点击、登录、截图、下载、筛选或读取动态状态。
- 可重复自动化：用户希望以后反复执行或进入测试/监控。

## 第三步：检查证据和时效要求

- 需要最新信息时，按 `freshness_policy.md` 执行。
- 涉及高影响结论时，按 `evidence_policy.md` 提高证据等级。
- 输出前按 `output_contract.md` 选择格式。

## 第四步：检查相关本地工具

只检查当前路线相关工具，不要把所有 CLI 当作必需依赖：

```bash
command -v firecrawl
```

目标是 GitHub 时：

```bash
command -v gh
```

目标是 API/JSON endpoint 时：

```bash
command -v curl
command -v jq
```

需要浏览器交互时：

```bash
command -v agent-browser
command -v browser-use
command -v npx
```

选择最适合信息来源的工具。例如：GitHub 元数据用 `gh`，通用网页搜索或抓取用 `firecrawl`，AI agent 交互式浏览用 `agent-browser`，可重复回归流程用 `npx playwright` 或项目已有 Playwright 命令。

## 路线选择

### 1. Lightweight

当用户需要快速答案、定义、URL 查询、单个聚焦事实或简单在线状态时，使用 `lightweight.md`。

信号：

- “是什么”、“定义”、“谁”、“什么时候”、“快速”
- 单一、明确的问题。
- 不需要深度比较或多来源综合。
- 一到三个来源足够。

示例：

```text
REST API 是什么？
找到 Firecrawl 的 GitHub URL。
Python 最早是什么时候发布的？
查一下 playwright 当前 npm 版本。
```

### 2. Standard

当用户需要调研、比较、分析、核验、来源多样性或结构化信息抽取时，使用 `standard.md`。

信号：

- “调研”、“比较”、“分析”、“验证”、“最新”
- 多个结论需要交叉验证。
- 输出需要引用、置信度或权衡。
- 答案可能影响技术或产品决策。

示例：

```text
比较 Firecrawl 和 Exa 在 agent 互联网信息获取中的适用性。
调研当前 MCP registry 的常见模式。
验证最新的 OpenAI API 模型推荐。
```

### 2.5 Deep Research

当用户要求系统性、大样本、可审计研究时，使用 `deep_research.md`。

信号：

- “深度研究”、“全网调研”、“系统性扫描”
- “找 50/100/200/300 个案例”
- “市场地图”、“竞品地图”、“生态扫描”
- 需要分类统计、覆盖率、样本框或证据矩阵。

示例：

```text
真实搜索 200 个 AI agent 平台案例，按开源/商业/垂直场景分类。
深度研究当前 MCP server 生态，给我一个供应商和项目长名单。
找 300 个使用 Playwright 做可视化回归的公开项目并归类。
```

### 3. Autonomous

当任务需要交互、认证、动态页面、表单、截图、重复导航或多步骤网站工作流时，使用 `autonomous.md`。

信号：

- “登录”、“点击”、“填写”、“下载”、“监控”、“自动化”
- JavaScript 渲染页面或无限滚动。
- 需要跨多个页面带状态地收集数据。
- 用户要的是工作流，而不仅是答案。

示例：

```text
登录并收集最新 dashboard 指标。
打开 GitHub trending，按语言过滤后提取仓库。
监控三个网站的价格。
```

## 升级规则

在以下情况升级路线：

- Lightweight 结果过时、冲突或太薄。
- 来源阻止静态提取。
- 用户要求更深入分析。
- 任务实际需要网页交互。

在以下情况降级路线：

- 本地 CLI 已返回完整结构化数据。
- 用户只需要直接答案。
- 简单搜索后发现不需要自动化。

## 工具选择矩阵

| 需求 | 优先使用 | 降级方案 |
| --- | --- | --- |
| 未知来源发现 | `firecrawl search "query" --limit 5` | 内置搜索或托管 API |
| URL 内容提取 | `firecrawl scrape "URL"` | `curl -L "URL"` 加解析工具 |
| GitHub 仓库/issue/release 数据 | `gh ... --json ...` | GitHub API、`firecrawl search` |
| 包元数据 | 包管理器 CLI | registry 网站/API |
| JSON/API 数据 | `curl` + `jq` | 官方文档或浏览器 |
| 动态 Web UI 探索 | `agent-browser` | `browser-use` 或内置浏览器 |
| 可重复浏览器流程 | `npx playwright` 或项目已有命令 | `agent-browser` 探索后再固化 |
| 登录工作流 | 使用本地浏览器自动化和已有 profile | 向用户确认访问约束 |

## 信息获取与浏览器的重叠处理

先问任务目标是什么：

- 目标是“知道什么”：来源未知时用搜索，来源已知时用来源专用 CLI/API。
- 目标是“拿到结构化字段”：优先来源专用 CLI、registry CLI、`curl` + `jq`。
- 目标是“网页上实际发生什么”：升级浏览器。
- 目标是“以后反复执行”：先浏览器探索，再考虑 Playwright 脚本或项目自动化。

典型升级路径：

```text
来源专用 CLI/API → firecrawl search → firecrawl scrape → agent-browser snapshot/click → Playwright 固化
```

典型不要升级的情况：

- `gh repo view` 已能返回字段。
- `npm view` 已能返回包版本和发布时间。
- 官方文档可被 `firecrawl scrape` 正常提取。

## 默认不写封装脚本

不要为了执行一次搜索而创建脚本。优先在当前工作会话中使用透明命令：

```bash
firecrawl search "GitHub" --limit 5
gh repo view openai/openai-python --json name,description,url,pushedAt
```

只有当用户明确要求可复用自动化、定时调研或可重复抽取产物时，才创建或修改脚本。

## 如何报告路线选择

只有当路线选择会影响预期时才说明，例如：

```text
我使用 standard 路线，因为这个问题需要跨来源验证。
```

简单查询直接回答并附来源。
