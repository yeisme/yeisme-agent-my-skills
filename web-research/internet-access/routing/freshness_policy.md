# Freshness Policy

## Purpose

Internet information changes often. Agents must decide which content needs current lookup and which can use stable knowledge as support.

## Information That Must Be Refreshed

Use current internet lookup and include source dates or update signals for:

- "latest", "now", "today", "recent", "current".
- versions, releases, changelogs, API changes.
- pricing, plans, quotas, policies, terms.
- laws, rules, standards status, compliance requirements.
- CEOs, maintainers, owners, organization status.
- security vulnerabilities, risks, incidents, news.
- package activity, repository maintenance, issue/release state.
- whether a product feature still exists.

Preferred command examples:

```bash
gh repo view openai/openai-python --json pushedAt,latestRelease,url
npm view @playwright/test version time --json
firecrawl search "OpenAI Responses API latest docs" --limit 8
```

## Information That Can Rely Less On Current Lookup

These topics are usually more stable, but should still have sources:

- basic concept explanations.
- historical background.
- stable protocol and standards concepts.
- long-lived math and computer science fundamentals.

## Date Handling

When useful, include:

- query/access date.
- source publication/update date.
- release time or structured fields such as `pushedAt`.

Example output:

```markdown
**Freshness**: This is high-change information; I used current lookup and prioritized official docs and release data.
```

## Staleness Risk

When source dates are old or update time cannot be confirmed:

- mark as "possibly stale".
- use another source for confirmation.
- lower confidence for key conclusions.

## User Relative Dates

When the user uses relative dates, final answers should use absolute dates when possible. For example:

- "today" -> "2026-05-19"
- "yesterday" -> "2026-05-18"
- "recent" -> state the search range or source dates used.
