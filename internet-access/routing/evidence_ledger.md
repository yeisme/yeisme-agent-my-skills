# 证据台账

## 目的

为深度研究和大样本论证提供可追溯记录。agent 必须区分候选来源、去重后来源、纳入样本、排除样本和最终引用。

## 台账层级

| 层级 | 含义 |
| --- | --- |
| candidate | 搜索、CLI、API 或浏览器发现的原始候选 |
| deduped | 去重后的候选 |
| included | 符合纳入标准的样本 |
| excluded | 被排除的候选及原因 |
| cited | 最终回答中引用的代表来源 |

## 推荐字段

| 字段 | 说明 |
| --- | --- |
| id | 稳定编号 |
| name | 项目、产品、公司或来源名 |
| canonical_url | 规范 URL |
| source_type | docs / GitHub / registry / API / paper / blog / news / browser |
| discovery_query | 发现它的 query 或命令 |
| tool | firecrawl / gh / npm / curl / agent-browser 等 |
| raw_url | 原始 URL |
| dedupe_key | URL、owner/repo、package name 或 domain |
| included | yes/no |
| exclusion_reason | 排除原因 |
| category | 分类 |
| fields | 抽取到的关键字段 |
| evidence_level | L1-L5 |
| last_updated | 来源更新时间 |
| confidence | high / medium / low |
| notes | 备注 |

## Markdown 台账格式

小样本可以直接在回答中使用表格：

```markdown
| id | name | category | evidence | source |
| --- | --- | --- | --- | --- |
| S001 | Example | open-source | L4 | https://example.com |
```

## JSONL 台账格式

大样本更适合 JSONL。只有用户要求保存完整清单或样本过大无法在回答中展示时，才创建文件：

```jsonl
{"id":"S001","name":"Example","canonical_url":"https://example.com","source_type":"docs","included":true,"category":"platform","evidence_level":"L3"}
```

如果创建文件，应使用用户指定路径；没有指定时先说明建议路径并征得同意，除非任务明确要求生成交付物。

## 去重规则

优先 dedupe key：

1. GitHub `owner/repo`。
2. package name。
3. canonical URL。
4. domain + product name。
5. title + organization。

## 排除原因

常见排除原因：

- duplicate。
- irrelevant。
- inaccessible。
- low_quality_aggregator。
- no_primary_source。
- outside_scope。
- stale_or_inactive。
- insufficient_evidence。

## 汇总指标

深度研究输出至少报告：

- candidates_total
- deduped_total
- included_total
- excluded_total
- cited_total
- batches_total
- duplicate_rate
- inclusion_rate

## 质量要求

- 每个关键发现都应能回到台账中的来源。
- 最终引用不是越多越好，应代表不同类别和证据等级。
- 如果完整台账未输出，必须说明展示的是代表样本还是完整样本。
