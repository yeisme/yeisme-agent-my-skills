# Internet Access Routing Decision Tree

## Purpose

Choose the lightest route that satisfies an internet information access or web interaction task, while preferring locally configured CLI tools. This decision tree guides agent judgement and does not require helper scripts.

## Step 1: Classify Task Intent

Read `task_intent.md` first and assign one primary intent:

| Intent | Typical request | Default route |
| --- | --- | --- |
| `local-research-infra` | "Use/debug Hermes or OpenWebUI research/search" | local_research_infra |
| `platform` | "Read/search/configure Twitter, Reddit, YouTube, Bilibili, XiaoHongShu, RSS, or Agent Reach" | agent_reach |
| `lookup` | "Check X current version/URL/release date" | lightweight |
| `research` | "Research/compare/analyze X" | standard |
| `deep-research` | "Deep research / broad scan / find 200 examples" | deep_research |
| `verify` | "Verify this claim / is it stale?" | standard |
| `extract` | "Extract fields from this URL/API/repo" | standard |
| `interact` | "Open the page, click, screenshot, download, inspect after login" | autonomous |
| `automate` | "Make this repeatable" | autonomous + Playwright |

## Step 2: Identify Target And Source

Then classify the source shape:

- Local research infrastructure: the task clearly points to Yeisme, Hermes, OpenWebUI, Research Harness, MCP Gateway, SearXNG, or a local Firecrawl backend.
- Agent Reach platform: the task names Agent Reach or a supported platform with known platform routing, login, cookie, proxy, video, social, community, RSS, or podcast needs.
- Known source query: the user gave a GitHub repo, package name, URL, API endpoint, or specific site.
- Unknown source discovery: the user gave only a topic and needs sources found.
- Verification/comparison: the user needs multi-source evidence and conclusions.
- Web interaction: clicking, login, screenshots, downloads, filters, or dynamic state are needed.
- Repeatable automation: the user wants repeated execution, tests, or monitoring.

## Step 3: Check Evidence And Freshness Requirements

- If current information is required, apply `freshness_policy.md`.
- For high-impact conclusions, raise the evidence bar with `evidence_policy.md`.
- Before output, choose the format from `output_contract.md`.

## Step 4: Check Relevant Local Tools

Only check tools relevant to the route. Do not treat every CLI as required:

```bash
command -v firecrawl
```

For GitHub targets:

```bash
command -v gh
```

For Agent Reach platform targets:

```bash
command -v agent-reach
agent-reach doctor
```

For API/JSON endpoints:

```bash
command -v curl
command -v jq
```

For browser interaction:

```bash
command -v agent-browser
command -v browser-use
command -v npx
```

Pick the tool that best matches the information source. GitHub metadata uses `gh`; general web search or scraping uses `firecrawl`; AI interactive browsing uses `agent-browser`; repeatable regression flows use `npx playwright` or existing project commands.

## Route Selection

### 0. Local Research Infra

When the task happens inside this repository's Hermes/OpenWebUI/MCP Gateway search and research capability, use `local_research_infra.md` first.

Signals:

- The user mentions Hermes, OpenWebUI, Open WebUI, Research Harness, SearXNG, Firecrawl backend, or MCP Gateway internet search.
- The task needs a decision between Firecrawl CLI, OpenWebUI Web Search, Research Harness, and browser tools.
- The task involves search quality, search budget, query generation, trace, source diversity, or local port configuration.

Examples:

```text
Optimize OpenWebUI Hermes Research Harness search quality.
Open WebUI returns too few search results; inspect local Firecrawl/SearXNG configuration.
How should Hermes agents call local search tools for deep research?
```

### 0.5 Agent Reach Platform Route

Use `agent_reach.md` when the task targets Agent Reach or a supported social, video, community, RSS, podcast, or logged-in platform.

Signals:

- The user mentions Agent Reach setup, update, doctor, install, optional channels, cookies, or proxy.
- The target is Twitter/X, Reddit, YouTube, Bilibili, XiaoHongShu, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou, or RSS.
- The task needs backend routing rather than ordinary generic web search.

Examples:

```text
帮我安装 Agent Reach 并检查哪些渠道可用。
帮我读这个 B 站视频的内容。
帮我搜推特上大家怎么评价这个产品。
小红书要怎么配置给 agent 用？
```

Do not use this route for normal public docs lookup when `firecrawl` or a structured CLI can answer directly.

### 1. Lightweight

Use `lightweight.md` when the user needs a quick answer, definition, URL lookup, single focused fact, or simple online status.

Signals:

- "what is", "definition", "who", "when", "quick".
- Single clear question.
- No need for deep comparison or multi-source synthesis.
- One to three sources are enough.

Examples:

```text
What is REST API?
Find Firecrawl's GitHub URL.
When was Python first released?
Check the current npm version of playwright.
```

### 2. Standard

Use `standard.md` when the user needs research, comparison, analysis, verification, source diversity, or structured information extraction.

Signals:

- "research", "compare", "analyze", "verify", "latest".
- Multiple conclusions need cross-checking.
- Output needs citations, confidence, or tradeoffs.
- The answer may affect a technical or product decision.

Examples:

```text
Compare Firecrawl and Exa for agent internet information access.
Research common patterns in current MCP registries.
Verify the latest recommended OpenAI API models.
```

### 2.5 Deep Research

Use `deep_research.md` when the user requires systematic, large-sample, auditable research.

Signals:

- "deep research", "broad web research", "systematic scan".
- "find 50/100/200/300 cases".
- "market map", "competitor map", "ecosystem scan".
- Category statistics, coverage, sample frame, or evidence matrix are required.

Examples:

```text
Search for 200 real AI agent platform examples and classify them by open-source, commercial, and vertical scenario.
Deep research the current MCP server ecosystem and give me a vendor/project longlist.
Find 300 public projects using Playwright for visual regression and classify them.
```

### 3. Autonomous

Use `autonomous.md` when interaction, authentication, dynamic pages, forms, screenshots, repeated navigation, or multi-step web workflows are required.

Signals:

- "login", "click", "fill", "download", "monitor", "automate".
- JavaScript-rendered pages or infinite scroll.
- Data must be collected across multiple stateful pages.
- The user wants a workflow, not just an answer.

Examples:

```text
Log in and collect the latest dashboard metrics.
Open GitHub Trending, filter by language, and extract repositories.
Monitor prices across three sites.
```

## Escalation Rules

Escalate when:

- Lightweight results are stale, conflicting, or too thin.
- Static extraction is blocked.
- The user asks for deeper analysis.
- The task actually requires web interaction.

Degrade when:

- Local CLI returns complete structured data.
- The user only needs a direct answer.
- A simple search shows automation is unnecessary.

## Tool Choice Matrix

| Need | Prefer | Fallback |
| --- | --- | --- |
| Hermes/OpenWebUI local research path | `local_research_infra.md` + local `firecrawl`/SearXNG/Research Harness | normal `firecrawl search`, built-in search |
| Social/video/community platform routing | `agent_reach.md` + selected upstream CLI | static extraction, browser tools |
| Unknown source discovery | `firecrawl search "query" --limit 5` | built-in search or hosted API |
| URL content extraction | `firecrawl scrape "URL"` | `curl -L "URL"` plus parser |
| GitHub repo/issue/release data | `gh ... --json ...` | GitHub API, `firecrawl search` |
| Package metadata | package manager CLI | registry site/API |
| JSON/API data | `curl` + `jq` | official docs or browser |
| Dynamic Web UI exploration | `agent-browser` | `browser-use` or built-in browser |
| Repeatable browser flow | `npx playwright` or existing project command | explore with `agent-browser`, then harden |
| Login workflow | local browser automation and existing profile | ask user to confirm access boundaries |

## Handling Search And Browser Overlap

Ask what the task is trying to accomplish:

- Goal is "know something": use search for unknown sources, or source-specific CLI/API for known sources.
- Goal is "get structured fields": prefer source-specific CLI, registry CLI, or `curl` + `jq`.
- Goal is "what actually happens on the page": escalate to browser.
- Goal is "repeat this later": explore with a browser first, then consider Playwright or project automation.

Typical escalation path:

```text
source-specific CLI/API -> firecrawl search -> firecrawl scrape -> agent-browser snapshot/click -> Playwright hardening
```

Typical cases that should not escalate:

- `gh repo view` already returns the needed fields.
- `npm view` already returns package version and release time.
- Official docs scrape cleanly with `firecrawl scrape`.

## Do Not Write Wrapper Scripts By Default

Do not create a script for a one-off search. Prefer transparent commands in the current session:

```bash
firecrawl search "GitHub" --limit 5
gh repo view openai/openai-python --json name,description,url,pushedAt
```

Create or modify scripts only when the user explicitly asks for reusable automation, scheduled research, or repeatable extraction artifacts.

## Reporting Route Choice

Only explain the route when it affects expectations, for example:

```text
I am using the standard route because this question needs cross-source verification.
```

For simple lookups, answer directly and include sources.
