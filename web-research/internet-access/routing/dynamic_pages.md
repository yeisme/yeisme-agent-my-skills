# JavaScript-Rendered Page Recovery

## Purpose

Recover page-specific content when Firecrawl reaches a valid page but extracts only the application shell because client-side rendering or hydration has not finished. This is distinct from an anti-bot challenge, an authentication wall, and a genuinely empty page.

## Normalize The URL First

Always pass an absolute URL with `https://` or `http://`. Quote the entire URL when it contains `?` or `&`.

Good:

```bash
firecrawl scrape "https://wetoken.ai/model-docs?model=dreamina-seedance-2-5-filter-off"
```

Do not pass `wetoken.ai/...` without a scheme. Firecrawl may still reach the page, but relative links and relative API examples can remain malformed in the extracted Markdown.

## Recognize A Render Shell

Do not equate HTTP success or a Scrape ID with content success. Treat the result as a render shell when one or more of these signals appear:

- The output contains only site-wide branding, navigation, account, top-up, or footer text.
- The expected page-specific heading, entity ID, endpoint, table, article body, or selected query-parameter value is absent.
- `--only-main-content` returns a few generic lines even though the visible page should be substantial.
- Repeating the request without changing render timing returns the same thin content.

For the WeToken model page, `Top UpExpense History` without the model name, endpoint, and `Request Parameters` table is a shell, not a successful extraction.

## Bounded Recovery Ladder

1. Save a fresh baseline so the result can be inspected as a whole:

```bash
firecrawl scrape "https://wetoken.ai/model-docs?model=dreamina-seedance-2-5-filter-off" --only-main-content --max-age 0 --timing -o /tmp/wetoken-model-docs-immediate.md
```

2. If the baseline is a shell, retry once with a 5-second render wait:

```bash
firecrawl scrape "https://wetoken.ai/model-docs?model=dreamina-seedance-2-5-filter-off" --only-main-content --wait-for 5000 --max-age 0 --timing -o /tmp/wetoken-model-docs-waited.md
```

3. Validate page-specific markers and compare the result size:

```bash
wc -c -l /tmp/wetoken-model-docs-immediate.md /tmp/wetoken-model-docs-waited.md
grep -nE 'dreamina-seedance-2-5-filter-off|/api/v3/contents/generations/tasks|Request Parameters' /tmp/wetoken-model-docs-waited.md
```

4. If the expected markers remain absent, make at most one longer bounded retry, such as `--wait-for 8000`, when slow hydration is plausible. Do not keep increasing the delay blindly.
5. If waiting still returns a shell, inspect embedded JSON or the page's XHR endpoint as described in `browser_tools.md`. Use `firecrawl interact` when a supported action is required, then escalate to Playwright or another browser only when browser-only state remains necessary.

## Option Semantics

- `--wait-for` gives client-side rendering time to mount page-specific content.
- `--only-main-content` filters the rendered result; it does not cause the content to render.
- `--max-age 0` is useful while diagnosing because it avoids accepting a cached shell. Omit it after the route is stable when normal caching is desirable.
- `--timing` records whether the extra wait was actually applied and helps distinguish slow rendering from immediate extraction.

## Acceptance Checks

Accept the scrape only when:

- At least one expected page-specific marker is present.
- Query-driven pages reflect the requested query value, not a default or different entity.
- The output contains the required section or fields, not only a larger navigation shell.
- Extracted links are absolute or otherwise usable.

Use `head` or `tail` only for preview. Preserve and inspect the complete result before claiming the page was extracted successfully.
