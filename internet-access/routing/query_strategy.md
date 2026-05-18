# 查询策略

## 目的

把“多搜几次”变成可审计的查询计划。特别适用于 deep-research、竞品扫描、生态普查和 200/300 个候选实例收集。

## 查询矩阵

为每个深度研究任务建立查询矩阵：

| 维度 | 示例 |
| --- | --- |
| 核心概念 | `AI agent framework`、`browser automation testing` |
| 同义词 | `agent platform`、`workflow agent`、`tool use agent` |
| 来源限定 | `site:github.com`、`site:docs.*`、`site:arxiv.org` |
| 技术栈 | `TypeScript`、`Python`、`Go`、`Rust` |
| 场景 | `developer tools`、`customer support`、`DevOps` |
| 证据类型 | docs、repo、release、paper、case study、company |
| 时间 | `2025`、`2026`、`latest`、`last 12 months` |

## 查询批次设计

每个批次应有明确目的：

1. broad discovery：找候选来源。
2. official sources：找官方文档和产品页。
3. structured sources：找 GitHub、registry、API 数据。
4. negative/critical sources：找问题、限制、停更、争议。
5. long-tail sources：找小众、地区、垂直场景。

示例命令：

```bash
firecrawl search "AI agent framework open source" --limit 20
firecrawl search "AI agent platform developer tools 2026" --limit 20
firecrawl search "site:github.com AI agent framework" --limit 20
gh search repos "AI agent framework language:Python" --limit 100
gh search repos "agent framework language:TypeScript" --limit 100
npm search agent framework --json
```

## 批次记录

每个批次记录：

- batch_id
- query
- tool
- limit
- returned_count
- new_candidates
- useful_candidates
- observed_bias

如果一个批次返回大量重复或低质量来源，下一批应调整 query，而不是继续堆同类结果。

## 覆盖率策略

为了避免样本偏差，至少覆盖：

- 官方来源。
- 开源来源。
- 商业来源。
- 社区/用户来源。
- 反向证据或负面评价。

技术主题至少覆盖：

- 官方文档。
- GitHub/release。
- 包 registry。
- 近期博客或案例。
- issue/discussion 中的实际使用信号。

## 扩展查询规则

当有效样本不足时：

- 换同义词。
- 换来源限定。
- 换语言/地区。
- 查代表样本的 alternatives、competitors、integrations。
- 从已纳入样本的 README/docs 链接继续扩展。

当重复率过高时：

- 收窄场景。
- 改用来源专用 CLI/API。
- 排除聚合站。
- 改查垂直关键词。

## 禁止事项

- 不用一个 query 支撑 “全网调研”。
- 不把搜索返回数量当有效样本数。
- 不只搜英文来源，除非用户明确限定。
- 不只搜 GitHub，除非研究对象就是开源项目。
- 不只看第一页或单一工具来源。
