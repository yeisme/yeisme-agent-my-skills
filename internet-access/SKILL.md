---
name: internet-access
description: 使用场景：当用户需要从互联网获取信息、搜索资料、提取网页内容、核验来源、读取在线服务状态或与网站/浏览器交互时使用；指导 agent 按任务目标选择本地 CLI，例如 firecrawl、来源专用 CLI、agent-browser、playwright、browser-use、curl 和 jq，再降级到托管 API 或内置浏览能力。
---

# 互联网信息获取与交互

## 目的

指导 agent 从互联网获取、验证和处理信息，并在必要时与网页或在线服务交互。这个 skill 的核心不是“搜索一下”，而是让 agent 选择合适的信息获取路径：搜索、提取、结构化查询、交叉验证、浏览器交互，或可复用自动化。

这是说明型 skill，不是脚本封装型 skill。agent 应直接调用真实的本地 CLI，并根据当前环境中实际存在的工具调整做法。

## 建议的 Skill 命令

推荐使用 `internet-access` 作为 skill 名称，因为它覆盖：

- 获取信息：搜索资料、找来源、查文档、查 release、查包版本。
- 验证信息：多来源核验、时效性检查、官方来源优先。
- 提取信息：从 URL、文档站点、GitHub、包 registry 或 API 中抽取内容。
- 与互联网交互：必要时打开浏览器、点击、筛选、截图、下载或登录后读取状态。

不建议命名为 `web-search`，因为真实需求不只是搜索；也不建议立即拆成独立 browser skill，因为浏览器是信息获取流程的升级路线，和搜索天然重叠。

## 什么时候使用

以下任务触发这个 skill：

- 互联网信息获取、网页搜索、在线调研和来源收集。
- 事实核验、时效性检查和多来源交叉验证。
- 从 URL 提取可读正文。
- 查找文档、release、issue、仓库或 changelog。
- 查询 GitHub、npm、PyPI、Cargo、Go module、标准文档或厂商文档。
- 浏览器自动化、需要登录的工作流、动态页面处理。

不要把这个 skill 用于本地文件搜索、代码执行、数据库查询或纯离线分析。

## 默认工具策略

不要把工具优先级理解成固定列表。先判断任务目标和目标来源，再选择最合适的本地工具：

1. 目标来源已知时，优先使用来源专用 CLI 或 API：
   - GitHub 目标：`gh`。
   - npm/PyPI/Cargo/Go 包：`npm`、`pip`、`cargo`、`go`。
   - JSON endpoint 或官方 API：`curl` + `jq`。
2. 目标来源未知、需要找资料时，优先用通用发现/提取工具：
   - `firecrawl`：通用网页搜索、抓取、crawl 和内容提取。
3. 页面真实交互或动态状态是答案的一部分时，才用浏览器工具：
   - `agent-browser`、`browser-use`、`npx playwright` 或项目已有浏览器自动化命令。
4. 本地通用降级工具：
   - `curl`、`jq`、`pup`、`htmlq`、`lynx`、`w3m` 等。
5. 当本地 CLI 不存在、被阻塞或不足以完成任务时，再使用内置浏览器/搜索工具。
6. 只有 CLI 不能完成任务且凭证已存在时，才直接调用托管 API。

`gh` 不属于通用搜索工具，也不是所有互联网任务的默认依赖。它只在目标是 GitHub，或搜索结果已经指向 GitHub 仓库、issue、release、discussion 时优先使用。这样可以避免用浏览器解析 GitHub 页面，也能直接拿到结构化字段。

## 来源优先级

按信息类型选择来源，不要把所有任务都当成网页搜索：

| 信息类型 | 优先工具 | 说明 |
| --- | --- | --- |
| 官方文档/网页正文 | `firecrawl search`、`firecrawl scrape` | 先搜索，再抓取权威 URL。 |
| GitHub 仓库、issue、release | `gh` | 结构化字段优先，不用浏览器解析页面。 |
| npm/PyPI/Cargo/Go 包 | 对应包管理器 CLI | 版本、发布时间、repository、依赖信息优先走 registry。 |
| API 返回值 | `curl` + `jq` | 适合官方 API、JSON endpoint 和健康检查。 |
| 动态页面/登录后状态 | `agent-browser` 或 `browser-use` | 需要真实页面状态时才使用。 |
| 可重复浏览器流程 | `npx playwright` 或项目已有 Playwright 命令 | 适合测试、回归和长期自动化。 |

不要默认假设必须导出 API key。本地 CLI 能工作时，优先用本地 CLI。规划前按任务探测工具，不需要每次检查所有工具：

```bash
command -v firecrawl
```

如果任务指向 GitHub：

```bash
command -v gh
```

如果任务需要浏览器交互：

```bash
command -v agent-browser
command -v browser-use
command -v npx
```

如果任务需要 JSON/API：

```bash
command -v curl
command -v jq
```

然后直接使用真实 CLI：

```bash
firecrawl search "GitHub" --limit 5
```

除非用户明确要求可复用自动化，否则不要新增本地封装脚本。这个 skill 的目标是教 agent 判断该用什么工具、如何透明地使用工具，而不是把判断隐藏到容易过期的脚本里。

## 四阶段模型

按任务需要从轻到重推进：

1. **发现**：用搜索或结构化 CLI 找到候选来源。
2. **提取**：从 URL、仓库、registry 或 API 中取出正文和元数据。
3. **验证**：优先官方/一手来源，必要时用独立来源交叉核验。
4. **交互**：只有静态信息不够时，才使用浏览器查看真实 UI 状态、点击、筛选、截图或下载。

典型路径：

```text
firecrawl search → firecrawl scrape → gh/npm/curl 结构化查询 → agent-browser 交互 → Playwright 固化
```

更准确的决策顺序：

```text
目标来源已知 → 来源专用 CLI/API
目标来源未知 → firecrawl search 做发现
已有 URL → firecrawl scrape 或 curl
静态内容不足 → agent-browser/browser-use
需要长期重复 → npx playwright 或项目已有测试命令
```

## 任务意图优先

先判断用户意图，再选择 route 和工具：

| 意图 | 目标 | 常见路线 |
| --- | --- | --- |
| `lookup` | 查一个事实、版本、URL、状态 | `lightweight.md` |
| `research` | 多来源调研、背景、比较 | `standard.md` |
| `deep-research` | 大样本调研、市场扫描、200-300 个实例论证 | `deep_research.md` + `evidence_policy.md` |
| `verify` | 核验一个说法是否真实、过时或有争议 | `standard.md` + `evidence_policy.md` |
| `extract` | 从 URL/API/仓库/registry 抽字段 | `source_priority.md` + `standard.md` |
| `interact` | 打开网页操作、截图、下载、登录后查看 | `autonomous.md` + `browser_tools.md` |
| `automate` | 可重复执行的浏览器流程 | `browser_tools.md`，必要时沉淀项目脚本 |

详细规则见 `routing/task_intent.md`。

## 路由

选择能满足任务的最小路线：

- `routing/task_intent.md`：先判断用户是要 lookup、research、verify、extract、interact 还是 automate。
- `routing/lightweight.md`：快速事实、定义、单来源核验和聚焦查询。
- `routing/standard.md`：多来源调研、比较、分析和交叉验证。
- `routing/deep_research.md`：深度研究、大样本搜索、200-300 个候选实例、证据矩阵和分层抽样。
- `routing/query_strategy.md`：查询扩展、批次设计、搜索覆盖和偏差控制。
- `routing/evidence_ledger.md`：候选来源、纳入样本、字段抽取和证据矩阵的台账结构。
- `routing/research_budget.md`：不同规模研究的时间/样本预算、停止条件和升级规则。
- `routing/autonomous.md`：浏览器交互、登录流程、动态内容、表单和多步骤网页工作流。
- `routing/source_priority.md`：按目标来源选择 `firecrawl`、`gh`、包管理器、`curl`/`jq` 或浏览器工具。
- `routing/browser_tools.md`：选择 `agent-browser`、`playwright`、`browser-use` 或静态抓取的具体规则。
- `routing/evidence_policy.md`：证据等级、来源可信度和引用要求。
- `routing/freshness_policy.md`：什么时候必须查新信息，如何处理日期和时效性。
- `routing/output_contract.md`：不同任务类型的稳定输出格式。

路由不明确时先读 `routing/decision_tree.md`。当结果太薄、互相冲突、过时，或页面需要交互时，升级路线。

## 搜索与浏览器边界

默认先做搜索和静态提取，不要一开始就开浏览器。浏览器是升级路线，适合解决“搜索结果无法直接回答”的问题。

继续使用搜索/抓取的情况：

- 用户需要事实、来源、文档、release、仓库、包版本或比较结论。
- `firecrawl search`、`firecrawl scrape`、`gh` 或包管理器 CLI 已能返回足够信息。
- 页面是静态文档、博客、README、release notes 或 API 文档。

升级到浏览器的情况：

- 需要点击、筛选、登录、填写表单、下载、截图或读取动态状态。
- 静态抓取缺少关键内容，或页面内容依赖 JavaScript 渲染。
- 需要验证页面真实交互、可见文本、弹窗、分页、无限滚动或认证后的状态。
- 用户明确要求“打开网页操作”、“浏览器里看一下”、“截图”、“帮我点/填/下载”。

如果浏览器任务开始变成长期复用能力，例如固定站点登录、定时监控、批量下载或端到端回归测试，再考虑创建专用浏览器 skill 或项目脚本。

## 什么时候拆专用浏览器 Skill

暂时不要拆分；保持在 `internet-access` 内部路由处理。只有满足以下任一条件时，再创建独立浏览器操作 skill：

- 浏览器任务本身成为主要目标，而不是为了获取信息服务。
- 需要长期维护登录态、profile、站点特定流程或下载目录。
- 需要沉淀 Playwright fixtures、selectors、截图基线、回放或回归测试规范。
- 多个项目都会复用同一套浏览器操作策略。

如果只是“为了查信息而打开网页”，继续留在本 skill 的 `autonomous` 路线。

## 工作流

1. 重述信息需求，判断是否需要时效性、引用来源或网页交互。
2. 用 `command -v` 检查当前路线可能需要的本地工具，不要机械检查无关工具。
3. 选择路线：lightweight、standard 或 autonomous。
4. 直接运行真实的本地 CLI 命令。
5. 保留有用证据：URL、标题、日期、执行过的命令和置信度限制。
6. 对重要结论做独立来源交叉验证。
7. 当本地工具缺失、结果过时或需要认证访问时，明确说明限制。

## 常见本地 CLI 模式

### 通用搜索

```bash
firecrawl search "GitHub" --limit 5
firecrawl search "OpenAI Responses API docs" --limit 10
```

### 抓取或提取已知 URL

```bash
firecrawl scrape "https://github.com/"
firecrawl scrape "https://docs.firecrawl.dev/"
```

### Crawl 文档站点

```bash
firecrawl crawl "https://docs.firecrawl.dev/" --limit 20
```

### GitHub 专项调研

```bash
gh search repos "agent framework language:TypeScript" --limit 10
gh repo view openai/openai-python --json name,description,stargazerCount,pushedAt,url
gh release list --repo openai/openai-python --limit 10
gh issue list --repo openai/openai-python --state open --limit 20
```

### GitHub API 降级方案

```bash
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, description, stargazers_count, pushed_at, html_url}'
curl -L "https://api.github.com/repos/openai/openai-python/releases?per_page=5" | jq '.[].tag_name'
```

### 包元数据

```bash
npm view playwright version description repository time --json
python -m pip index versions requests
cargo search tokio --limit 5
go list -m -versions golang.org/x/tools
```

### 浏览器交互证据

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
browser-use state
```

### HTTP 降级方案

```bash
curl -L "https://example.com" | head
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, description, stargazers_count, pushed_at, html_url}'
```

## 输出标准

快速回答：给出答案和来源链接。调研任务：给出简短综合、由来源支持的发现和信息缺口。自动化任务：说明尝试了什么、使用了哪些工具、哪些成功、哪些失败，以及产生了哪些产物。

只要答案依赖外部信息，就包含来源 URL。对可能近期变化的信息，优先使用新的本地搜索结果，不要只依赖记忆。

输出应体现任务类型：

- 获取信息：答案、关键来源、时间敏感性。
- 核验信息：结论、支持来源、冲突来源、置信度。
- 提取内容：来源 URL、抽取字段、缺失字段。
- 浏览器交互：工具、最终 URL、操作结果、截图/下载路径、阻塞点。

正式输出格式见 `routing/output_contract.md`。如果任务涉及最新版本、价格、政策、API、release、法律/规则、负责人或其它高变动事实，必须按 `routing/freshness_policy.md` 处理。

## 深度研究边界

不要默认把普通 research 升级成 deep-research。只有满足以下任一条件时才进入 `routing/deep_research.md`：

- 用户明确要求“深度研究”、“全网调研”、“系统性扫描”、“尽可能全面”。
- 用户要求真实搜索大量实例，例如 50、100、200、300 个候选来源或案例。
- 任务需要市场地图、竞品清单、生态扫描、开源项目普查、供应商长名单、论文/案例系统综述。
- 结论需要建立在样本覆盖率、分类统计或证据矩阵上，而不是少量来源综合。

深度研究必须分阶段执行：先建立查询计划和采样框架，再批量发现候选来源，去重分类，抽取字段，最后综合。不能直接把 200 条搜索结果堆进最终回答。

大样本研究必须遵守：

- `routing/query_strategy.md`：先设计查询矩阵，再批量搜索。
- `routing/evidence_ledger.md`：用统一字段记录候选、去重、纳入和排除原因。
- `routing/research_budget.md`：先确认规模、预算和停止条件，避免无限搜索。

## 护栏

- 技术结论优先使用官方文档、项目仓库、release notes、标准、论文和厂商文档。
- 对重要或不稳定结论使用多个独立来源。
- 把搜索摘要当作线索，而不是最终证据；除非用户只需要快速查询。
- 不在回复中暴露 secret、cookie、token 或私有 profile 路径。
- 未经用户明确确认，不执行购买、账号变更、破坏性操作或不可逆提交。
- 如果本地工具缺失，说明哪个命令不可用，并选择下一条可行路线。
