# Deep Research 路线

## 目的

处理系统性、大样本、可审计的互联网研究。适用于用户明确要求深度研究、全网调研、市场/竞品/生态扫描，或要求真实搜索 50、100、200、300 个候选实例来支撑结论。

Deep Research 不是“多搜几次”。它要求先定义研究问题和纳入标准，再批量发现候选来源，去重、分类、抽取字段、建立证据矩阵，最后综合结论。查询设计见 `query_strategy.md`，证据记录见 `evidence_ledger.md`，规模和停止条件见 `research_budget.md`。

## 什么时候使用

使用本路线：

- 用户明确要求“深度研究”、“全网调研”、“系统性扫描”、“尽可能全面”。
- 用户要求大量真实搜索实例，例如 50、100、200、300 个案例。
- 任务是市场地图、竞品长名单、生态扫描、开源项目普查、供应商筛选、论文/案例综述。
- 结论需要分类统计、趋势判断、覆盖率或样本框。

不要使用本路线：

- 用户只要快速事实。
- 普通 5-10 个来源就能回答。
- 用户没有要求样本覆盖率或大量实例。
- 任务其实是打开网页操作或下载文件。

## 研究分层

按规模选择研究强度：

| 规模 | 候选来源 | 纳入样本 | 适用场景 |
| --- | ---: | ---: | --- |
| quick scan | 20-50 | 10-20 | 初步判断、轻量竞品扫描 |
| standard scan | 50-120 | 20-50 | 一般深度研究、技术路线比较 |
| large scan | 120-300 | 50-150 | 市场地图、生态扫描、案例归纳 |
| exhaustive attempt | 300+ | 100+ | 用户明确要求尽可能全面，且时间允许 |

候选来源是搜索/CLI/API 找到的原始结果；纳入样本是去重、过滤和确认相关性后的记录。不要把候选数当作证据数。

## 工作流

### 1. 定义研究问题

先写清楚：

- 研究问题。
- 时间范围。
- 地域/语言范围。
- 来源类型：官方、GitHub、registry、论文、新闻、社区、公司官网等。
- 纳入标准。
- 排除标准。
- 目标样本量。

示例：

```text
目标：找 200 个 AI agent 开发平台或框架候选。
纳入：有公开网站、GitHub repo、文档或产品页；与 agent workflow/runtime/tool use 相关。
排除：纯聊天机器人、无公开来源、重复镜像、明显停更且无使用证据。
```

### 2. 设计查询批次

不要只用一个 query。按 `query_strategy.md` 建立查询矩阵，并按维度拆分：

- 核心关键词。
- 同义词。
- 来源限定。
- 技术栈。
- 场景。
- 地域/语言。
- 年份/时效。

示例命令：

```bash
firecrawl search "AI agent framework open source" --limit 20
firecrawl search "AI coding agent platform developer tools" --limit 20
firecrawl search "site:github.com agent framework tool use" --limit 20
firecrawl search "site:docs.github.com GitHub Copilot agent mode" --limit 10
gh search repos "agent framework language:TypeScript" --limit 100
gh search repos "AI agent framework language:Python" --limit 100
npm search agent framework --json
```

### 3. 批量发现候选

每个查询批次记录：

- query。
- 工具。
- 返回数量。
- 主要来源类型。
- 明显偏差。

建议每批 10-30 条，避免单次结果过长。需要 200-300 个候选时，用多个批次覆盖不同角度。

每批结果都应进入 `evidence_ledger.md` 定义的候选台账，不要只保存在临时上下文里。

### 4. 去重与过滤

去重 key 优先级：

1. 规范 URL。
2. GitHub `owner/repo`。
3. package name。
4. 产品/公司名 + domain。

过滤：

- 明显无关。
- 重复镜像。
- 低质量聚合页。
- 无法访问且无替代来源。
- 与研究定义不匹配。

### 5. 字段抽取

根据任务抽取字段。常用字段：

| 字段 | 说明 |
| --- | --- |
| name | 项目/产品/组织名 |
| url | 权威 URL |
| source_type | docs / GitHub / registry / paper / blog / company |
| category | 分类 |
| evidence_level | L1-L5 |
| last_updated | 更新时间 |
| status | active / inactive / unclear |
| notes | 关键说明 |

GitHub 示例：

```bash
gh repo view openai/openai-python --json nameWithOwner,description,stargazerCount,pushedAt,url
```

npm 示例：

```bash
npm view @playwright/test version time repository --json
```

### 6. 分类和抽样

大样本不能只列链接。必须做分类：

- 类型：开源/商业/研究/工具/平台。
- 场景：开发者工具、客服、数据分析、浏览器自动化、DevOps、企业流程。
- 成熟度：活跃、早期、停更、不明确。
- 证据等级：L2/L3/L4/L5。

如果样本太多，最终回答给分类统计和代表样本；完整清单分批输出或写入用户指定文件。没有用户要求时，不要创建新文件。

### 7. 综合结论

结论必须基于：

- 样本数量。
- 去重数量。
- 纳入/排除标准。
- 分类统计。
- 代表样本。
- 证据等级。

禁止声称“全面覆盖”除非用户给了足够时间和明确搜索范围。更稳妥说法是“在本轮查询范围内”。

### 8. 停止条件

按 `research_budget.md` 判断是否停止、扩展或降级。常见停止条件：

- 已达到用户要求的候选数或纳入样本数。
- 新查询批次的新增有效样本率低于阈值。
- 关键类别都已有代表样本。
- 时间或工具预算耗尽，且继续搜索边际收益低。
- 用户要求的 200/300 个实例无法在当前工具条件下可靠完成，需要报告已覆盖范围和下一步。

## 输出格式

使用 `output_contract.md` 的 `deep-research` 输出。必须包含：

- 研究问题。
- 查询批次。
- 查询矩阵。
- 候选来源数。
- 去重后来源数。
- 纳入样本数。
- 分类统计。
- 证据矩阵或代表样本。
- 限制和偏差。

## 质量护栏

- 不把搜索摘要当最终证据。
- 不把候选数量当纳入样本数量。
- 不把 GitHub stars 当唯一质量指标。
- 不用 3-5 个来源支撑“市场全景”结论。
- 不声称“全网完整”。
- 如果用户要求 200/300 个实例，但工具或时间不足，先报告可完成的批次数、已覆盖范围和下一步。
