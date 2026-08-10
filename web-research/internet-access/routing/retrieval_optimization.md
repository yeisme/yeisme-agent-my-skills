# Agent Retrieval Optimization

## Purpose

Keep web retrieval useful to an agent while minimizing context tokens, repeated fetches, provider credits, and unnecessary browser escalation. This is a routing and response-contract layer around Firecrawl and other source-specific tools; it is not a replacement for those tools.

## Boundary

Apply this overlay whenever the agent searches unknown sources, expands queries, compares multiple pages, performs deep research, or may call the same source again in the same task.

Do not solve these concerns by modifying Firecrawl first:

- Agent context compaction and maximum response size.
- Cross-query, cross-provider, or cross-turn deduplication.
- Source diversity and evidence-role selection.
- Query budgets, stop conditions, and cache policy.

Consider a Firecrawl source change only when the current endpoint has a reproducible provider bug, lacks a required stable field or option, or needs a reviewed security or compatibility update. Keep the upstream source patch separate from this routing policy.

## Progressive Retrieval

Use the smallest useful retrieval stage and escalate only when evidence is insufficient:

| Stage | Route | Default agent-visible output |
| --- | --- | --- |
| Discover | `firecrawl search` | 5-8 compact results with query-relevant highlights; no full-page scrape |
| Select | Local ranking, URL normalization, and deduplication | 1-3 source IDs to open |
| Open | `firecrawl scrape` for selected URLs | Main content or selected passages only |
| Extract | Scrape JSON mode or a source-specific CLI/API | Requested fields plus source URLs |
| Deep fallback | `firecrawl agent` | Structured result, explicit credit cap, and evidence sources |

Preferred routing:

```text
known URL -> scrape or JSON extraction
known domain -> map(search) -> scrape selected URLs
unknown web -> search highlights -> open selected results
multi-hop or unknown locations -> agent with a budgeted fallback
```

Do not enable search-result scraping by default. Search and scrape are separate stages so the model does not receive several full pages before it has selected evidence.

## Deduplication Policy

Deduplicate in this order:

1. Normalize URLs: remove fragments and tracking parameters, normalize host and trailing slashes, follow redirects when available, and preserve functional query parameters.
2. Group exact canonical URLs before fetching.
3. After fetching, hash normalized main content to identify mirrors and repeated pages.
4. Use title, host, and a short normalized content prefix for deterministic near-duplicate grouping.
5. Enforce source diversity during ranking; do not keep every result from one domain.

Deduplication must not erase independent corroboration. Keep the best authoritative source and, when needed, one independent source for the same claim. Do not use an LLM or embedding model for default deduplication; reserve semantic grouping for deep research or high-duplication news/republishing workloads.

Useful result metadata outside the default prose context:

```json
{
  "source_id": "r1",
  "canonical_url": "https://example.com/article",
  "dedupe_group": "g7",
  "domain": "example.com",
  "evidence_role": "primary"
}
```

## Compact Response Contract

Provider payloads should be normalized before being returned to the agent. The default discovery response should look like:

```json
{
  "query": "...",
  "results": [
    {
      "source_id": "r1",
      "url": "https://example.com/article",
      "title": "Page title",
      "highlight": "Short passage relevant to the query",
      "rank": 1,
      "source_type": "web"
    }
  ],
  "next": "open source_id r1"
}
```

The open response should contain only the selected passages, headings, source URL, fetch time, and any extraction fields requested by the agent. Keep raw HTML, full Markdown, provider metadata, screenshots, and duplicate snippets in a cache keyed by `source_id` or canonical URL.

Every compact response should expose enough provenance to cite the source, but should not repeat the same URL, title, metadata block, or page body in later turns.

## Starting Budgets

These are defaults to tune with evidence, not provider limits:

| Profile | Search limit | Open limit | Context target | Escalation |
| --- | ---: | ---: | ---: | --- |
| `fast` | 5 | 1 | <= 2k tokens | no agent by default |
| `balanced` | 6-8 | 2 | <= 4k tokens | agent only when evidence is thin |
| `deep` | 8-12 | 3-5 | <= 8k tokens | agent with explicit `maxCredits` |

Track two budgets separately:

- Agent context tokens: normalized response size sent to the model.
- Provider cost: Firecrawl credits/tokens, scrape pages, browser actions, and other upstream usage.

Stop or ask for escalation when the requested fields are supported by independent evidence, the context budget is full, or two query expansions add mostly duplicate sources. Do not start a full crawl merely because the first search returned fewer results than the requested limit.

## Cache And Freshness

Use separate cache keys for query discovery and page content:

- Query key: normalized query, route profile, locale, freshness profile, include/exclude domains, and source type.
- Page key: canonical URL, extraction options, and content version or hash.

Use `maxAge` and `storeInCache` where the Firecrawl deployment supports them. Suggested starting TTLs are 1-7 days for stable documentation, 5-30 minutes for current news, 1-6 hours for volatile product/status pages, and 7 days for stable research papers. Bypass cache only when the user asks for current state or the freshness policy requires it.

Cache negative results and failed URLs briefly as well, so repeated agent turns do not retry the same dead source without new evidence.

## Quality And Cost Metrics

Record per run:

- raw result count, deduped result count, selected result count;
- duplicate ratio and unique-domain ratio;
- context tokens sent to the agent;
- Firecrawl credits or upstream tokens used;
- pages scraped and cache-hit ratio;
- evidence coverage, source diversity, and unsupported-claim rate;
- latency and escalation count.

Use the metrics to decide whether stronger deduplication is justified. If duplicate content is below roughly 10% of the context, prefer passage selection and caching. If it stays above 15-20%, add near-duplicate grouping or a domain-diversity reranker.

## Firecrawl Change Gate

The current routing layer can use Firecrawl's existing search limit, domain filters, scrape options, cache age, Map, and Agent budget controls. Do not modify `backend-server/firecrawl/src` for the first implementation of this overlay.

Before upgrading or redeploying the Firecrawl backend, review the pinned upstream diff and verify the custom image path. Then use the owning project's real commands:

```bash
cd backend-server/firecrawl
git -C src log --oneline --decorate -20
docker compose --env-file .env -f docker-compose.yml build api
docker compose --env-file .env -f docker-compose.yml up -d
task health
task test-search
task test-scrape
```

Do not run a blind `task update` when the compose file points at a custom local API image; pulling the upstream source does not necessarily rebuild that image. Keep source upgrades and deployment changes behind a separate review and verification gate.
