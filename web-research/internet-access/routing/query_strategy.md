# Query Strategy

## Purpose

Turn "search a few more times" into an auditable query plan. This is especially useful for deep research, competitor scans, ecosystem surveys, and collecting 200/300 candidate examples.

## Query Matrix

Build a query matrix for every deep research task:

| Dimension | Examples |
| --- | --- |
| Core concept | `AI agent framework`, `browser automation testing` |
| Synonyms | `agent platform`, `workflow agent`, `tool use agent` |
| Source filters | `site:github.com`, `site:docs.*`, `site:arxiv.org` |
| Technology stack | `TypeScript`, `Python`, `Go`, `Rust` |
| Use case | `developer tools`, `customer support`, `DevOps` |
| Evidence type | docs, repo, release, paper, case study, company |
| Time | `2025`, `2026`, `latest`, `last 12 months` |

## Query Batch Design

Each batch should have a clear purpose:

1. broad discovery: find candidate sources.
2. official sources: find official docs and product pages.
3. structured sources: find GitHub, registry, and API data.
4. negative/critical sources: find issues, limits, inactivity, disputes.
5. long-tail sources: find niche, regional, or vertical examples.

Example commands:

```bash
firecrawl search "AI agent framework open source" --limit 20
firecrawl search "AI agent platform developer tools 2026" --limit 20
firecrawl search "site:github.com AI agent framework" --limit 20
gh search repos "AI agent framework language:Python" --limit 100
gh search repos "agent framework language:TypeScript" --limit 100
npm search agent framework --json
```

## Batch Record

Record each batch with:

- batch_id
- query
- tool
- limit
- returned_count
- new_candidates
- useful_candidates
- observed_bias

If a batch returns many duplicates or low-quality sources, adjust the next query instead of repeating the same pattern.

## Coverage Strategy

To avoid sample bias, cover at least:

- official sources.
- open-source sources.
- commercial sources.
- community/user sources.
- counterevidence or negative reviews.

For technical topics, cover at least:

- official docs.
- GitHub/release data.
- package registry data.
- recent blog or case study material.
- issue/discussion usage signals.

## Query Expansion Rules

When valid samples are insufficient:

- switch synonyms.
- change source filters.
- change language/region.
- search alternatives, competitors, and integrations for representative samples.
- expand from links in included samples' README/docs.

When duplicates are too frequent:

- narrow the use case.
- switch to source-specific CLI/API.
- exclude aggregator sites.
- search vertical keywords.

## Do Not

- Do not use one query to support "broad web research".
- Do not treat returned result count as valid sample count.
- Do not search only English sources unless the user explicitly scopes that way.
- Do not search only GitHub unless the research object is open-source projects.
- Do not rely only on the first page or one tool source.
