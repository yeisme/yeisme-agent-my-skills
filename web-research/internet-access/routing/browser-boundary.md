# Search And Browser Boundary

Firecrawl discovery, rendered extraction, crawling, and supported interaction are the default for ordinary websites. Do not open a browser first. Playwright and other browser tools are escalation paths for cases where Firecrawl is unavailable or insufficient.

Continue with search/extraction when:

- The user needs facts, sources, docs, releases, repositories, package versions, or comparison conclusions.
- `firecrawl search`, `firecrawl scrape`, `gh`, or package manager CLIs return enough information.
- The page is documentation, a blog, README, release notes, or API docs, including JavaScript-rendered content that passes the marker checks in `routing/dynamic_pages.md` after `firecrawl scrape --wait-for`.
- Firecrawl can complete the required interaction with `firecrawl interact`.

Escalate to browser tools when:

- A reasonable Firecrawl scrape/interact attempt still misses required browser-only state.
- Extraction returns an anti-bot challenge page (Cloudflare-style interstitial, captcha) or obfuscated text; read `routing/anti_bot.md` for the recognition signals and bypass order before retrying.
- Unsupported widgets, complex authentication, downloads, popups, multi-tab behavior, screenshots, or browser diagnostics are needed.
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
