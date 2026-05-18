# Deep Research Route

## Purpose

Handle systematic, large-sample, auditable internet research. Use this when the user explicitly asks for deep research, broad web research, market/competitor/ecosystem scans, or real search over 50, 100, 200, or 300 candidate examples to support a conclusion.

Deep Research is not "search more". It requires defining the research question and inclusion criteria first, then discovering candidate sources in batches, deduplicating, classifying, extracting fields, building an evidence matrix, and synthesizing conclusions. Query design lives in `query_strategy.md`; evidence tracking lives in `evidence_ledger.md`; scale and stopping conditions live in `research_budget.md`.

## When To Use

Use this route when:

- The user explicitly says "deep research", "broad web research", "systematic scan", or "as comprehensive as possible".
- The user asks for many real examples, such as 50, 100, 200, or 300 cases.
- The task is a market map, competitor longlist, ecosystem scan, open-source project survey, vendor shortlist, or paper/case review.
- The conclusion needs category statistics, trends, coverage, or a sample frame.

Do not use this route when:

- The user only needs a quick fact.
- A normal 5-10 source search can answer the question.
- The user did not request sample coverage or many examples.
- The task is actually opening a web page, operating a browser, or downloading files.

## Research Tiers

Choose research intensity by scale:

| Tier | Candidate sources | Included samples | Best for |
| --- | ---: | ---: | --- |
| quick scan | 20-50 | 10-20 | Initial judgement, light competitor scan |
| standard scan | 50-120 | 20-50 | General deep research, technical comparison |
| large scan | 120-300 | 50-150 | Market maps, ecosystem scans, case synthesis |
| exhaustive attempt | 300+ | 100+ | User explicitly asks for broad coverage and time allows |

Candidate sources are raw results found by search/CLI/API. Included samples are deduplicated, filtered, and confirmed records. Do not treat candidate count as evidence count.

## Workflow

### 1. Define The Research Question

Write down:

- Research question.
- Time range.
- Geography/language scope.
- Source types: official, GitHub, registry, papers, news, communities, company sites.
- Inclusion criteria.
- Exclusion criteria.
- Target sample size.

Example:

```text
Goal: find 200 candidate AI agent development platforms or frameworks.
Include: public website, GitHub repo, docs, or product page; related to agent workflow/runtime/tool use.
Exclude: pure chatbots, no public source, duplicate mirrors, clearly inactive projects without usage evidence.
```

### 2. Design Query Batches

Do not use a single query. Build a query matrix from `query_strategy.md` and split by dimensions:

- Core keywords.
- Synonyms.
- Source filters.
- Technology stack.
- Use case.
- Geography/language.
- Year/freshness.

Example commands:

```bash
firecrawl search "AI agent framework open source" --limit 20
firecrawl search "AI coding agent platform developer tools" --limit 20
firecrawl search "site:github.com agent framework tool use" --limit 20
firecrawl search "site:docs.github.com GitHub Copilot agent mode" --limit 10
gh search repos "agent framework language:TypeScript" --limit 100
gh search repos "AI agent framework language:Python" --limit 100
npm search agent framework --json
```

### 3. Discover Candidates In Batches

For each query batch, record:

- query.
- tool.
- returned count.
- primary source type.
- obvious bias.

Use 10-30 results per batch to keep output manageable. For 200-300 candidates, use many batches that cover different angles.

Each batch result should enter the candidate ledger defined in `evidence_ledger.md`. Do not keep it only in temporary context.

### 4. Deduplicate And Filter

Dedupe key priority:

1. canonical URL.
2. GitHub `owner/repo`.
3. package name.
4. product/company name + domain.

Filter out:

- clearly irrelevant results.
- duplicate mirrors.
- low-quality aggregators.
- inaccessible sources without substitutes.
- items outside the research definition.

### 5. Extract Fields

Extract fields based on the task. Common fields:

| Field | Description |
| --- | --- |
| name | Project/product/organization name |
| url | Authoritative URL |
| source_type | docs / GitHub / registry / paper / blog / company |
| category | Classification |
| evidence_level | L1-L5 |
| last_updated | Update time |
| status | active / inactive / unclear |
| notes | Key notes |

GitHub example:

```bash
gh repo view openai/openai-python --json nameWithOwner,description,stargazerCount,pushedAt,url
```

npm example:

```bash
npm view @playwright/test version time repository --json
```

### 6. Classify And Sample

Large samples cannot be only link lists. They must be classified:

- Type: open source, commercial, research, tool, platform.
- Scenario: developer tools, customer support, data analysis, browser automation, DevOps, enterprise workflows.
- Maturity: active, early, inactive, unclear.
- Evidence level: L2/L3/L4/L5.

If the sample is too large, the final answer should include category statistics and representative samples. Output the full list in batches or write it to a user-specified file. If the user did not ask for a file, do not create one.

### 7. Synthesize Conclusions

Conclusions must be based on:

- sample count.
- deduped count.
- inclusion/exclusion criteria.
- category statistics.
- representative samples.
- evidence levels.

Do not claim "complete coverage" unless the user gave enough time and a clearly bounded search scope. Safer phrasing: "within this query scope".

### 8. Stopping Conditions

Use `research_budget.md` to decide whether to stop, expand, or degrade. Common stopping conditions:

- Target candidate count or included sample count is reached.
- New valid-sample rate drops below the threshold in later query batches.
- Key categories each have representative samples.
- Time or tool budget is exhausted and marginal value is low.
- The requested 200/300 examples cannot be completed reliably with current tools; report covered scope and next steps.

## Output Format

Use the `deep-research` output in `output_contract.md`. Include:

- research question.
- query batches.
- query matrix.
- candidate source count.
- deduped source count.
- included sample count.
- category statistics.
- evidence matrix or representative samples.
- limits and bias.

## Quality Guardrails

- Do not treat search snippets as final evidence.
- Do not treat candidate count as included sample count.
- Do not use GitHub stars as the only quality signal.
- Do not support a "market landscape" conclusion with 3-5 sources.
- Do not claim "the whole web" or "complete coverage".
- If the user asks for 200/300 examples but tools or time are insufficient, first report feasible batches, covered scope, and next steps.
