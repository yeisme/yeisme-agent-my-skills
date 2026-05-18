# Lightweight Route

## Purpose

Answer simple web questions quickly with one focused local CLI query. Prefer direct commands and do not use local helper scripts.

## When To Use

- The user asks for a definition, URL, release date, maintainer, version, short explanation, or single fact.
- One to three sources are enough.
- Speed matters more than depth.
- No interaction or login is required.

## Local CLI Workflow

1. Decide whether the target source is known.
2. If the source is unknown, reduce the query to core keywords and use `firecrawl search`:

```bash
firecrawl search "GitHub" --limit 5
firecrawl search "REST API definition" --limit 3
```

3. If the source is known, prefer the source-specific CLI:

```bash
gh repo view firecrawl/firecrawl --json name,description,stargazerCount,url
npm view firecrawl-mcp version description repository --json
python -m pip index versions requests
```

Use `gh` only when the target is GitHub. Do not call `gh` first for general web search.

4. If the answer is on a known URL, scrape it directly:

```bash
firecrawl scrape "https://github.com/firecrawl/firecrawl"
```

5. If the local CLI is missing, fall back to built-in search/browser tools or `curl`.
6. If the user only needs a current version, status, or URL, do not escalate to a browser.

Unless the first result set is unclear or the topic is highly unstable, do not run multi-angle research for a simple fact lookup.

## Output Format

```markdown
**Answer**: [direct answer in 1-2 sentences]

**Source**: [URL or structured source]
```

Add at most three bullets only when they materially improve clarity.

## Quality Bar

- Cite the source URL.
- Avoid generic summaries when the user asks for a fact.
- Use current search for information that can change.
- Escalate to `standard.md` when results conflict or source quality is weak.
