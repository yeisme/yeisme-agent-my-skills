# Local Research Infrastructure

## Purpose

Explain how to map general internet information access routes onto already configured local services and CLIs in Yeisme, Hermes, OpenWebUI, MCP Gateway, and similar local deployment contexts. This file only handles local research infrastructure selection; it does not replace `source_priority.md`, `deep_research.md`, or `browser_tools.md`.

## When To Use

Use this route when:

- The user explicitly mentions Hermes, OpenWebUI, Open WebUI, Research Harness, MCP Gateway, SearXNG, Firecrawl backend, or local services.
- The current task is to design, debug, review, or use OpenWebUI Hermes internet research capability inside this repository.
- The agent needs to decide between host-shell CLI search and OpenWebUI/Hermes configured tools.
- Search quality issues are tied to local service configuration, such as too few results, over-broad query generation, or Firecrawl loader not working.

Do not treat this route as a global default. General internet information access still follows source priority: `firecrawl`, `gh`, package managers, `curl`/`jq`, or browser tools.

## Repository Policy

In Yeisme/Hermes/OpenWebUI context:

- Do not use or debug BigModel/Zai `web-search-prime` as the default internet search backend; it is intentionally kept disabled on the MCP Gateway side.
- When host agents perform search, scraping, or large-sample research, prefer the local `firecrawl` CLI connected to the configured `/home/yeshugen/workplace/backend-server-firecrawl` backend.
- OpenWebUI built-in Web Search uses SearXNG; Web Loader uses Firecrawl.
- OpenWebUI Research Harness plans research tasks, builds query buckets, records evidence traces, enforces source diversity gates, and checks answer quality; it is not a replacement for general web search CLI work.
- `gh` remains a GitHub-specific structured-source adapter. Do not promote it to a general search tool just because the task is in Hermes/OpenWebUI.

## Host Shell Route

When the agent runs a research task in the host shell, prefer direct local CLI commands:

```bash
firecrawl view-config
firecrawl search "Open WebUI web_search_queries_generated query prompt" --limit 5 --json
firecrawl search "Open WebUI web_search_queries_generated query prompt" --api-url http://localhost:32741 --limit 5 --json
firecrawl scrape "https://docs.openwebui.com/" --api-url http://localhost:32741
```

Rules:

- Use `firecrawl view-config` first to see whether the CLI already points at the local Firecrawl backend.
- If the current config does not point at the local backend, pass `--api-url` explicitly.
- This repository records default Firecrawl API ports in `docs/service-ports.md`; common host entry is `32741`, and common SearXNG search entry is `32742`.
- For complex research, write results to `.firecrawl/`, then read incrementally with `jq`, `rg`, `head`, and similar tools to avoid flooding context.

Example:

```bash
mkdir -p .firecrawl
firecrawl search "Hermes Agent Open WebUI Research Harness" --limit 10 --json -o .firecrawl/hermes-research.json
jq -r '.data.web[]? | [.title, .url] | @tsv' .firecrawl/hermes-research.json
```

## OpenWebUI/Hermes Route

When the task happens inside OpenWebUI/Hermes, prefer the injected OpenWebUI configuration:

| Capability | Default local component | Role |
| --- | --- | --- |
| Web Search | SearXNG | Returns candidate search results. |
| Web Loader | Firecrawl | Loads page body text. |
| Research Harness | OpenWebUI Tool | Plans research profiles, builds query buckets, records traces, checks quality. |
| Agent CLI Tool | OpenWebUI Tool | Calls allowlisted agent CLIs inside the container. |

OpenWebUI containers usually access host services through `host.docker.internal`:

```text
http://host.docker.internal:32742/search
http://host.docker.internal:32741
```

For direct host access, use `docs/service-ports.md` and the current `.env` as the source of truth. Do not write tokens, API keys, or real secrets into answers.

## Research Harness Selection

OpenWebUI Hermes Research Harness currently fits:

- `daily_news_digest`: daily hot topics, general news, multi-source digest.
- `technical_research`: technical research, error investigation, version behavior; preserves exact terms and prefers primary sources.
- `fact_check`: fact checking, rumor analysis, insufficient single-source claims.

If an agent in OpenWebUI/Hermes context can call Research Harness, prefer it for planning and trace first, then let lower-level search services collect evidence. Key output should include:

- profile.
- query buckets.
- raw/deduped/selected counts.
- dropped reasons.
- coverage limits.
- trace path.
- quality grade.

If the user asks for 100/200/300 samples, Research Harness may only be suitable as a first-round planner. Large-sample dedupe, classification, and full ledger still follow `deep_research.md` and `evidence_ledger.md`. If local tools or OpenWebUI valves limit the budget, report the clamped parameters and the additional batches needed.

## Query Generation Constraints

This repository's OpenWebUI query generation prompt principles also apply to direct agent searches:

- The first query preserves the user's exact target, product names, commands, flags, filenames, error text, URLs, versions, and dates.
- Do not rewrite a precise technical issue into a broad category.
- Do not add a year mechanically unless the user asks for latest/current/news or the topic is time-sensitive.
- Preserve English product names, API names, repository names, and error text even when the user asks in Chinese.
- For follow-up questions, recover the exact topic from nearby context, but keep the query concise.

Technical research examples:

```bash
firecrawl search "Open WebUI web_search_queries_generated query prompt" --limit 8
firecrawl search "Open WebUI web_search_queries_generated query prompt official docs" --limit 8
firecrawl search "\"Open WebUI web_search_queries_generated query prompt\"" --limit 8
```

## Debugging Route

When Hermes/OpenWebUI search quality is poor, debug in this order:

1. Check host Firecrawl CLI availability:

```bash
firecrawl view-config
firecrawl search "openwebui" --limit 3 --json
```

2. Check whether local service ports match docs:

```bash
ss -lntp | rg ':(32741|32742|7457|8000|8642)\b'
```

3. Check OpenWebUI subproject health:

```bash
cd /home/yeshugen/workplace/yeisme-agent/backend-server/openwebui-hermes
task health
task webui-config-status
```

4. Inspect whether Research Harness reports `search_scarcity`, `domain_scarcity`, or budget clamp.
5. For technical problems, confirm that the query preserved the original command, error text, and version instead of becoming generic.

## Reference Locations

This route is derived from repository materials:

- `docs/skills/skill-trigger-guide.md`
- `docs/service-ports.md`
- `.skills/yeisme/mcp/yeisme-mcp-gateway-operator/SKILL.md`
- `.skills/yeisme/mcp/yeisme-mcp-gateway-maintainer/SKILL.md`
- `.skills/yeisme/mcp/yeisme-mcp-registry-onboarding/SKILL.md`
- `backend-server/openwebui-hermes/AGENTS.md`
- `backend-server/openwebui-hermes/README.md`
- `backend-server/openwebui-hermes/scripts/openwebui_hermes/prompts/search_query_generation.md`
- `backend-server/openwebui-hermes/scripts/openwebui_hermes/research_harness.py`
- `backend-server/openwebui-hermes/openspec/specs/research-harness/spec.md`
