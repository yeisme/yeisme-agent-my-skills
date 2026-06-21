# Task Intent Classification

## Purpose

Before choosing tools, identify what kind of internet task the user wants. Tool choice must serve the task intent, not the other way around.

## Intent Types

### `lookup`

Goal: find one clear fact, current version, URL, release date, status, or short definition.

Signals:

- "check"
- "current version"
- "official site / repository address"
- "when was it released"
- "who maintains it"

Default route: `lightweight.md`

Example commands:

```bash
npm view @playwright/test version --json
gh repo view openai/openai-python --json name,url,pushedAt
firecrawl search "Firecrawl GitHub" --limit 5
```

Output: direct answer + source.

### `research`

Goal: multi-source research, comparison, background, or option analysis around a topic.

Signals:

- "research"
- "compare"
- "analyze"
- "what are the options"
- "pros and cons"

Default route: `standard.md`

Example commands:

```bash
firecrawl search "Firecrawl Exa Tavily comparison" --limit 8
firecrawl search "site:docs.firecrawl.dev search scrape crawl" --limit 8
```

Output: summary, findings, sources, limits.

### `local-research-infra`

Goal: choose or debug search, scraping, Research Harness, and browser escalation in a Yeisme/Hermes/OpenWebUI local deployment.

Signals:

- "Hermes/OpenWebUI research"
- "Open WebUI search"
- "Research Harness"
- "SearXNG/Firecrawl local service"
- "MCP Gateway internet search"
- "web-search-prime"

Default route: `local_research_infra.md`, combined with `standard.md`, `deep_research.md`, or `browser_tools.md` when needed.

Example commands:

```bash
firecrawl view-config
firecrawl search "Open WebUI Research Harness" --api-url http://localhost:32741 --limit 5 --json
curl -fsS "http://localhost:32742/search?q=openwebui&format=json" | jq '.results[:3][] | {title, url}'
```

Output: local route decision, services/CLIs used, port/config evidence, trace/budget/coverage limits, and next debugging path.

### `platform`

Goal: read, search, configure, or diagnose a named social, video, community, RSS, podcast, or logged-in platform through Agent Reach's backend routing.

Signals:

- "Agent Reach"
- "Twitter/X", "Reddit", "YouTube", "Bilibili", "小红书", "XiaoHongShu", "LinkedIn", "V2EX", "雪球", "Xueqiu", "小宇宙", "Xiaoyuzhou", "RSS"
- "configure cookies"
- "which backend is active"
- "doctor"

Default route: `agent_reach.md`, combined with `standard.md` for synthesis or `browser_tools.md` when visible UI interaction is still required.

Example commands:

```bash
command -v agent-reach
agent-reach doctor
agent-reach install --env=auto --channels=opencli,twitter,reddit,bilibili
agent-reach configure --from-browser chrome
```

Output: Agent Reach route decision, platform, active backend, completed read/search/configuration, blocked credentials or proxy needs, and evidence.

### `deep-research`

Goal: systematic, large-sample, auditable internet research.

Signals:

- "deep research"
- "broad web research"
- "systematic scan"
- "find 200/300 cases"
- "real search over many examples"
- "market map / competitor map / ecosystem scan"

Default route: `deep_research.md` + `query_strategy.md` + `evidence_ledger.md` + `research_budget.md` + `evidence_policy.md` + `output_contract.md`

Example commands:

```bash
firecrawl search "AI coding agent startup GitHub" --limit 20
firecrawl search "site:github.com AI agent framework TypeScript" --limit 20
gh search repos "agent framework language:TypeScript" --limit 100
npm search agent framework --json
```

Output: research question, query batches, candidate count, deduped count, category statistics, representative samples, evidence matrix, conclusions, and limits.

### `verify`

Goal: check whether a claim is true, stale, exaggerated, or conflicting.

Signals:

- "verify"
- "is this true"
- "is this outdated"
- "what evidence exists"
- "fact check"

Default route: `standard.md` + `evidence_policy.md`

Requirements:

- Prefer primary sources first.
- Use multiple independent sources for high-impact conclusions.
- State conflicts and uncertainty.

### `extract`

Goal: extract fields from a URL, API, GitHub, registry, or documentation site.

Signals:

- "extract"
- "scrape fields"
- "list releases"
- "get version/update time"
- "read from this URL"

Default route: `source_priority.md` + `standard.md`

Example commands:

```bash
firecrawl scrape "https://docs.firecrawl.dev/"
gh release list --repo openai/openai-python --limit 10
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, pushed_at, html_url}'
```

Output: fields, sources, missing items.

### `interact`

Goal: open a web page and perform a one-off operation, inspect real page state, or produce evidence.

Signals:

- "open the page"
- "click"
- "screenshot"
- "download"
- "check after login"
- "what does the page show"

Default route: `autonomous.md` + `browser_tools.md`

Example commands:

```bash
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
```

Output: tool, final URL, operation result, evidence path, blockers.

### `automate`

Goal: turn a browser or internet workflow into a repeatable test, monitor, or automation.

Signals:

- "run repeatedly later"
- "write automation"
- "make a test"
- "monitor"
- "batch download"

Default route: explore with `browser_tools.md`, then consider Playwright or project scripts according to project conventions.

Example commands:

```bash
npx playwright codegen "https://example.com"
npx playwright test --headed
```

Output: execution strategy, whether a project script is needed, risks, and verification command.

## Multi-Intent Tasks

If a task has multiple intents, process them in this order:

```text
local-research-infra -> lookup/extract -> verify -> research -> deep-research -> interact -> automate
```

Example: if the user asks to verify whether a library is still active and open the official site to see if docs are current, first verify activity with `gh`/registry/search, then escalate to browser only if static information is insufficient.
