# Standard Route

## Purpose

Use multiple direct local CLI queries and source-specific tools to produce sourced research, comparison, verification, or analysis.

## When To Use

- The user asks to research, compare, analyze, verify, or find current information.
- Important claims need cross-checking.
- The answer needs citations, tradeoffs, dates, or confidence.
- The result may guide technical, product, legal, financial, or operational decisions.

If the user explicitly asks for 50/100/200/300 real examples, broad web research, an ecosystem scan, or an evidence matrix, escalate to `deep_research.md`. Do not use the standard route to pretend that large-sample research is complete.

## Local CLI Workflow

### 1. Plan Search Angles

Choose three to seven focused angles:

```text
overview
official docs
recent changes
comparison / alternatives
implementation examples
limitations / criticism
community evidence
```

### 2. Start With Source-Specific Tools

If the user gave a specific source, use the matching CLI/API first instead of searching:

```bash
gh repo view mendableai/firecrawl --json name,description,stargazerCount,pushedAt,url
gh release list --repo mendableai/firecrawl --limit 10
npm view @playwright/test version time repository --json
curl -L "https://api.github.com/repos/mendableai/firecrawl" | jq '{name, pushed_at, html_url}'
```

`gh` only handles GitHub sources. It is not a general discovery tool. If the target is not GitHub, there is no need to probe or use `gh`.

### 3. Then Search Locally

When the source is unknown or background is needed, use `firecrawl search` for discovery:

```bash
firecrawl search "Firecrawl CLI search documentation" --limit 8
firecrawl search "Firecrawl alternatives Exa Tavily comparison 2026" --limit 8
firecrawl search "site:docs.firecrawl.dev CLI search scrape crawl" --limit 8
```

Scrape authoritative URLs directly:

```bash
firecrawl scrape "https://docs.firecrawl.dev/"
```

Do not hide these steps inside local helper scripts. The agent should preserve a visible research path so the final answer can explain sources, limits, and confidence.

### 4. Use Structured Sources For Confirmation

If search discovers a stable CLI or JSON API source, switch back to structured queries:

```bash
gh repo view mendableai/firecrawl --json name,description,stargazerCount,pushedAt,url
gh release list --repo mendableai/firecrawl --limit 10
npm view @playwright/test version time repository --json
curl -L "https://api.github.com/repos/mendableai/firecrawl" | jq '{name, pushed_at, html_url}'
```

### 5. Verify And Synthesize

- Prefer official docs and primary sources.
- Cross-check important claims with independent sources.
- Record publication dates and freshness signals such as "last updated".
- Separate facts, interpretation, and uncertainty.
- Keep source URLs for every material claim.

### 6. Degrade Gracefully

If `firecrawl` is unavailable:

```bash
command -v firecrawl
curl -L "https://example.com" | head
```

Then use built-in search/browser tools if needed. Do not block the task just because the preferred CLI is missing.

## Output Format

```markdown
**Summary**
[3-5 sentence synthesis]

**Findings**
- [finding] ([source])
- [finding] ([source])

**Evidence**
- Tools: [firecrawl / gh / npm / curl / agent-browser]
- Command types: [search / scrape / structured query / browser interaction]

**Caveats**
- [conflicts, stale sources, access gaps, or uncertainty]

**Sources**
- [title or domain] - [URL]
```

Use a table when comparing multiple options. Match answer length to the depth the user requested.

## Quality Bar

- Use multiple sources for high-impact claims.
- Prefer primary sources over second-hand summaries.
- Use fresh search results for unstable topics.
- State when local CLI output is insufficient or unavailable.
- Escalate to `autonomous.md` when interaction, authentication, or dynamic page state is required.
