---
name: internet-access
description: Use when the user needs to get information from the internet, search the web, extract web content, verify sources, inspect online service state, or interact with websites/browsers; guides agents to choose local CLI tools first, such as firecrawl, source-specific CLIs, agent-browser, playwright, browser-use, curl, and jq, before falling back to hosted APIs or built-in browsing.
---

# Internet Information Access And Interaction

## Purpose

Guide agents to gather, verify, and process information from the internet, and to interact with websites or online services when needed. The core of this skill is not "search the web"; it is choosing the right information path: discovery, extraction, structured queries, cross-checking, browser interaction, or reusable automation.

This is an instruction skill, not a script wrapper. Agents should call real local CLI tools directly and adapt to the tools that actually exist in the current environment.

## Recommended Skill Command

Use `internet-access` as the skill name because it covers:

- Information gathering: search, source discovery, docs, releases, package versions.
- Verification: multi-source checks, freshness checks, official-source priority.
- Extraction: pulling content from URLs, documentation sites, GitHub, package registries, or APIs.
- Internet interaction: opening browsers, clicking, filtering, screenshots, downloads, or reading logged-in state.

Do not name this skill `web-search`; the real need is broader than search. Do not split a separate browser skill yet; browser work is an escalation path inside information access and overlaps naturally with search.

## When To Use

Use this skill for:

- Internet information gathering, web search, online research, and source collection.
- Fact checking, freshness checks, and multi-source validation.
- Extracting readable content from URLs.
- Finding docs, releases, issues, repositories, or changelogs.
- Querying GitHub, npm, PyPI, Cargo, Go modules, standards docs, or vendor docs.
- Browser automation, logged-in workflows, and dynamic page handling.

Do not use this skill for local file search, code execution, database queries, or purely offline analysis.

## Default Tool Strategy

Do not treat tool priority as a fixed list. First identify the task goal and likely source, then choose the best local tool:

1. If the target source is known, prefer the source-specific CLI or API:
   - GitHub target: `gh`.
   - npm/PyPI/Cargo/Go package target: `npm`, `pip`, `cargo`, `go`.
   - JSON endpoint or official API: `curl` + `jq`.
2. If the target source is unknown and discovery is needed, prefer generic discovery/extraction tools:
   - `firecrawl`: general web search, scrape, crawl, and content extraction.
3. If the task is in a Yeisme/Hermes/OpenWebUI local deployment context, first read `routing/local_research_infra.md` and reuse the local Firecrawl, SearXNG, and Research Harness constraints.
4. Use browser tools only when real page interaction or dynamic state is part of the answer:
   - `agent-browser`, `browser-use`, `npx playwright`, or an existing project browser automation command.
5. Local generic fallback tools:
   - `curl`, `jq`, `pup`, `htmlq`, `lynx`, `w3m`.
6. If local CLIs are missing, blocked, or insufficient, then use built-in browsing/search tools.
7. Call hosted APIs directly only when CLI options cannot complete the task and credentials already exist.

`gh` is not a general web search tool and is not a default dependency for every internet task. Use it only when the target is GitHub, or when search results already point to a GitHub repository, issue, release, or discussion and structured fields are needed. This avoids parsing GitHub pages in a browser and gives structured data directly.

## Source Priority

Choose sources by information type instead of treating every task as web search:

| Information type | Preferred tool | Notes |
| --- | --- | --- |
| Official docs / web page text | `firecrawl search`, `firecrawl scrape` | Search first, then scrape authoritative URLs. |
| GitHub repos, issues, releases | `gh` | Prefer structured fields; avoid browser page parsing. |
| npm/PyPI/Cargo/Go packages | Package manager CLI | Versions, release time, repository, and dependency data should come from the registry. |
| API values | `curl` + `jq` | Good for official APIs, JSON endpoints, and health checks. |
| Dynamic pages / logged-in state | `agent-browser` or `browser-use` | Use only when real page state matters. |
| Repeatable browser flows | `npx playwright` or existing project Playwright commands | Best for tests, regressions, and long-term automation. |

Do not assume an API key must be exported. If a local CLI works, use it first. Before planning, probe only the tools relevant to the route:

```bash
command -v firecrawl
```

For GitHub targets:

```bash
command -v gh
```

For browser interaction:

```bash
command -v agent-browser
command -v browser-use
command -v npx
```

For JSON/API work:

```bash
command -v curl
command -v jq
```

Then run real CLI commands directly:

```bash
firecrawl search "GitHub" --limit 5
```

Do not create local wrapper scripts unless the user explicitly asks for reusable automation. This skill teaches agents how to choose and transparently use tools; it should not hide decisions inside brittle scripts.

## Four-Stage Model

Move from light to heavy as the task requires:

1. **Discover**: use search or structured CLIs to find candidate sources.
2. **Extract**: pull text and metadata from URLs, repositories, registries, or APIs.
3. **Verify**: prioritize official/primary sources and cross-check with independent sources when needed.
4. **Interact**: use a browser only when static information is insufficient and real UI state, clicks, filters, screenshots, or downloads are needed.

Typical path:

```text
firecrawl search -> firecrawl scrape -> gh/npm/curl structured query -> agent-browser interaction -> Playwright hardening
```

More precise decision order:

```text
Known target source -> source-specific CLI/API
Unknown source -> firecrawl search for discovery
Known URL -> firecrawl scrape or curl
Static content insufficient -> agent-browser/browser-use
Needs long-term repetition -> npx playwright or project command
```

## Task Intent First

Classify the user's intent before choosing a route and tool:

| Intent | Goal | Common route |
| --- | --- | --- |
| `local-research-infra` | Use or debug Yeisme/Hermes/OpenWebUI local research infrastructure | `local_research_infra.md` |
| `lookup` | Find one fact, version, URL, or status | `lightweight.md` |
| `research` | Multi-source research, background, comparison | `standard.md` |
| `deep-research` | Large-sample research, market scan, 200-300 evidence examples | `deep_research.md` + `evidence_policy.md` |
| `verify` | Check whether a claim is true, stale, or disputed | `standard.md` + `evidence_policy.md` |
| `extract` | Extract fields from a URL/API/repo/registry | `source_priority.md` + `standard.md` |
| `interact` | Operate a web page, screenshot, download, inspect logged-in state | `autonomous.md` + `browser_tools.md` |
| `automate` | Build a repeatable browser flow | `browser_tools.md`, then project automation if needed |

See `routing/task_intent.md` for detailed rules.

## Routes

Choose the smallest route that satisfies the task:

- `routing/task_intent.md`: classify lookup, research, verify, extract, interact, or automate.
- `routing/lightweight.md`: quick facts, definitions, single-source checks, focused queries.
- `routing/standard.md`: multi-source research, comparison, analysis, and cross-checking.
- `routing/deep_research.md`: deep research, large-sample search, 200-300 candidate examples, evidence matrices, and stratified sampling.
- `routing/query_strategy.md`: query expansion, batch design, search coverage, and bias control.
- `routing/evidence_ledger.md`: candidate sources, included samples, field extraction, and evidence ledger shape.
- `routing/research_budget.md`: research scale, time/sample budgets, stopping conditions, and escalation rules.
- `routing/autonomous.md`: browser interaction, login flows, dynamic content, forms, and multi-step web workflows.
- `routing/source_priority.md`: choose `firecrawl`, `gh`, package managers, `curl`/`jq`, or browser tools by source.
- `routing/local_research_infra.md`: Yeisme/Hermes/OpenWebUI local search infrastructure, Firecrawl, SearXNG, Research Harness, and Gateway search policy.
- `routing/browser_tools.md`: choose `agent-browser`, Playwright, `browser-use`, or static extraction.
- `routing/evidence_policy.md`: evidence levels, source credibility, and citation rules.
- `routing/freshness_policy.md`: when to fetch current information and how to handle dates.
- `routing/output_contract.md`: stable output formats for each task type.

If the route is unclear, read `routing/decision_tree.md`. Escalate when results are thin, conflicting, stale, or require page interaction.

## Search And Browser Boundary

Search and static extraction are the default. Do not open a browser first. Browser tools are escalation paths for cases where search results cannot answer the question directly.

Continue with search/extraction when:

- The user needs facts, sources, docs, releases, repositories, package versions, or comparison conclusions.
- `firecrawl search`, `firecrawl scrape`, `gh`, or package manager CLIs return enough information.
- The page is static documentation, a blog, README, release notes, or API docs.

Escalate to browser tools when:

- Clicking, filtering, login, form filling, downloads, screenshots, or dynamic state are needed.
- Static extraction misses key content or the page depends on JavaScript rendering.
- The task requires validating visible text, dialogs, pagination, infinite scroll, or authenticated state.
- The user explicitly asks to open a page, inspect it in a browser, take a screenshot, click, fill, or download.

If browser tasks become long-term reusable work, such as fixed-site login, scheduled monitoring, batch downloads, or end-to-end regression tests, consider a dedicated browser skill or project script.

## When To Split A Dedicated Browser Skill

Do not split yet; keep browser routing inside `internet-access`. Create a separate browser-operation skill only if one of these becomes true:

- Browser operation itself becomes the main goal, not a support path for information access.
- Long-lived login state, profiles, site-specific flows, or download directories must be maintained.
- Playwright fixtures, selectors, screenshot baselines, replays, or regression-test rules need to be preserved.
- Multiple projects reuse the same browser operation strategy.

If the browser is only used to get information, keep using the `autonomous` route inside this skill.

## Workflow

1. Restate the information need and decide whether freshness, citations, or web interaction are required.
2. Check whether the task is in a Yeisme/Hermes/OpenWebUI local research infrastructure context; if so, apply `local_research_infra.md`.
3. Use `command -v` only for tools relevant to the current route.
4. Choose a route: lightweight, standard, deep-research, or autonomous.
5. Run real local CLI commands directly.
6. Preserve useful evidence: URL, title, date, command type, and confidence limits.
7. Cross-check important conclusions with independent sources.
8. State limitations when tools are missing, results are stale, or authentication is required.

## Common Local CLI Patterns

### General Search

```bash
firecrawl search "GitHub" --limit 5
firecrawl search "OpenAI Responses API docs" --limit 10
firecrawl view-config
firecrawl search "Open WebUI Research Harness" --api-url http://localhost:32741 --limit 5 --json
```

### Scrape Or Extract A Known URL

```bash
firecrawl scrape "https://github.com/"
firecrawl scrape "https://docs.firecrawl.dev/"
```

### Crawl A Documentation Site

```bash
firecrawl crawl "https://docs.firecrawl.dev/" --limit 20
```

### GitHub-Specific Research

```bash
gh search repos "agent framework language:TypeScript" --limit 10
gh repo view openai/openai-python --json name,description,stargazerCount,pushedAt,url
gh release list --repo openai/openai-python --limit 10
gh issue list --repo openai/openai-python --state open --limit 20
```

### GitHub API Fallback

```bash
curl -L "https://api.github.com/repos/openai/openai-python" | jq '{name, description, stargazers_count, pushed_at, html_url}'
curl -L "https://api.github.com/repos/openai/openai-python/releases?per_page=5" | jq '.[].tag_name'
```

### Package Metadata

```bash
npm view playwright version description repository time --json
python -m pip index versions requests
cargo search tokio --limit 5
go list -m -versions golang.org/x/tools
```

### Browser Interaction Evidence

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
browser-use state
npx playwright codegen "https://example.com"
```

## Validation

For simple lookups, validate by citing the source. For research and verification, validate by cross-checking important claims. For deep research, validate counts, dedupe rules, included samples, categories, and evidence levels. For browser tasks, validate final URL, visible state, screenshots, downloaded files, or structured observations.
