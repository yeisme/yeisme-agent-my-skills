# Source And Tool Priority

## Purpose

Replace fixed tool ordering with source-driven decisions. The key to internet information access is not always searching first; it is identifying where the most authoritative source likely lives.

## General Rules

Priority is source-driven:

1. If the user gave an explicit source, use that source's CLI, API, or scrape command directly.
2. If the task clearly happens in a Yeisme/Connectors/OpenWebUI local deployment, apply `local_research_infra.md` first to confirm local Firecrawl, SearXNG, Research Harness, and Gateway policy.
3. If the task targets a platform covered by Agent Reach, apply `agent_reach.md` to choose and diagnose the backend before using the selected upstream tool.
4. For ordinary web discovery, extraction, JavaScript-rendered pages, documentation crawling, and supported interaction, use the matching Firecrawl command first.
5. If search results point to structured sources, switch to the source-specific CLI/API.
6. If Firecrawl is unavailable or insufficient after a reasonable attempt, escalate to an existing project Playwright workflow or `npx playwright`.
7. Use `agent-browser` or `browser-use` for one-off visual inspection when that is more suitable than a maintained Playwright artifact.

## Role Of Agent Reach

Agent Reach is the preferred route selector for platform-specific internet access when the platform has known friction, login requirements, or multiple backend choices.

Use it for:

- Twitter/X, Reddit, YouTube, Bilibili, XiaoHongShu, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou, RSS, and related optional channel setup.
- Installing or updating the local capability layer.
- Running health checks before deciding whether to use `twitter-cli`, OpenCLI, `yt-dlp`, `bili-cli`, `rdt-cli`, `gh`, `feedparser`, or another backend.
- Cookie, proxy, or browser-session configuration guidance.

Common commands:

```bash
command -v agent-reach
agent-reach doctor
agent-reach doctor --json
agent-reach install --env=auto --safe
```

Do not treat Agent Reach as a content wrapper. Once the active backend is clear, use that backend directly and report it in the evidence.

## Is `gh` Redundant?

`gh` is not redundant, but it is not a general search tool. Use it first only for GitHub-related tasks:

- The user gives a GitHub repo, issue, PR, release, organization, or user.
- Search results already point to GitHub and structured fields are needed.
- Stars, update time, releases, issue state, PR state, or repository metadata are needed.
- Browser page parsing for GitHub should be avoided.

Examples:

```bash
gh repo view openai/openai-python --json name,description,stargazerCount,pushedAt,url
gh release list --repo openai/openai-python --limit 10
gh issue list --repo openai/openai-python --state open --limit 20
gh search repos "agent framework language:TypeScript" --limit 10
```

Do not prioritize `gh` when:

- The user asks about general web pages, news, standards, blogs, product docs, or vendor docs.
- The target source is not GitHub.
- The task only needs broad web discovery.
- A GitHub page is only one search result and has not been established as the main source.

## Role Of `firecrawl`

`firecrawl` is the general discovery, rendered extraction, crawling, and supported interaction tool:

```bash
firecrawl search "Model Context Protocol registry" --limit 8
firecrawl scrape "https://docs.firecrawl.dev/"
firecrawl crawl "https://docs.firecrawl.dev/" --limit 20
firecrawl scrape "https://example.com"
firecrawl interact --prompt "Open the documentation menu and extract the visible API sections"
```

Use `firecrawl` first when:

- The user gives only a topic and sources must be found.
- The target is web page text, docs, blogs, or official pages.
- A URL is known and main content must be extracted.
- A documentation site needs to be crawled.
- The page relies on JavaScript rendering; try `firecrawl scrape --wait-for <ms>` before browser automation.
- The task needs a supported click, form, pagination, or navigation flow; try `firecrawl interact` before Playwright.

Do not rely only on `firecrawl` when:

- GitHub, npm, PyPI, Cargo, Go modules, or other sources have structured CLIs/APIs.
- Real visual UI state, unsupported browser behavior, or browser diagnostics are required.
- A reasonable Firecrawl scrape/interact attempt still misses the required content or state.

## Connectors/OpenWebUI Local Search Infrastructure

When the task is explicitly about this repository's Connectors, OpenWebUI, MCP Gateway, or Research Harness internet capability, use `local_research_infra.md`:

- In the host shell, prefer the `firecrawl` CLI, with explicit local Firecrawl API URL when needed.
- Inside OpenWebUI, Web Search uses SearXNG and Web Loader uses Firecrawl.
- Research Harness is for query buckets, traces, source diversity, and quality checks.
- Do not use BigModel/Zai `web-search-prime` as the default internet search backend.

Common commands:

```bash
firecrawl view-config
firecrawl search "Open WebUI Research Harness" --api-url http://localhost:32741 --limit 5 --json
curl -fsS "http://localhost:32742/search?q=openwebui&format=json" | jq '.results[:3][] | {title, url}'
```

If these ports differ on the machine, use `docs/service-ports.md`, the current `.env`, and `firecrawl view-config` as the source of truth.

## Package Manager CLIs

Package versions, release times, repository links, and dependency metadata should come from registry CLIs first:

```bash
npm view @playwright/test version time repository --json
python -m pip index versions requests
cargo search tokio --limit 5
go list -m -versions golang.org/x/tools
```

If the package manager CLI is insufficient, search the official registry page or source repository.

## `curl` + `jq`

Use for known JSON endpoints, official APIs, health checks, or GitHub API fallback:

```bash
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, description, stargazers_count, pushed_at, html_url}'
```

Rules:

- Use only for stable endpoints.
- Do not write tokens or private headers into the final answer.
- If API output conflicts with the web page, explain the difference and cite both.

## Browser Tools

Escalate to Playwright only after Firecrawl is unavailable or insufficient, or when the flow must become reusable automation:

```bash
npx playwright codegen "https://example.com"
npx playwright test --headed
```

Use `agent-browser` or `browser-use` instead when the remaining need is one-off visual inspection rather than maintained automation. Do not use a browser just to read documentation that Firecrawl can extract.
