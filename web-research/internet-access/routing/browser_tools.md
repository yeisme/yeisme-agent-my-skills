# Browser Tool Guide

## Purpose

Explain when an internet information task should escalate from Firecrawl to a browser, and how to choose among existing project Playwright commands, `npx playwright`, `agent-browser`, and `browser-use`. This file is an escalation route inside `internet-access`, not a separate skill.

## Principle

A browser is not the default web access tool. Use source-specific CLIs or Firecrawl first, including for JavaScript-rendered pages and Firecrawl-supported interactions. Use a browser only when Firecrawl is unavailable or insufficient, or when real visual state and reusable UI automation are required.

Priority:

1. `gh` / package manager CLIs / official APIs: structured sources.
2. `firecrawl search` / `scrape` / `map` / `crawl` / `download`: discovery and rendered content extraction.
3. `firecrawl interact`: supported clicks, forms, pagination, and navigation.
4. Existing project Playwright commands or `npx playwright`: fallback for browser-only state and repeatable, testable workflows.
5. `agent-browser` or `browser-use`: one-off visual inspection when that browser surface is more suitable.

## Check Embedded Page Data First

Modern SPA pages usually ship their structured data as inline JSON on `window`; one `page.evaluate` (or `agent-browser` eval, or viewing page source for `<script>` blocks) often replaces the entire UI clicking flow. Before driving clicks, pagination, or infinite scroll, check for:

- `window.__NEXT_DATA__` (Next.js), `window.__NUXT__` (Nuxt), `window.__INITIAL_STATE__`, `window._ROUTER_DATA`, and similar framework globals.
- `<script type="application/json">` or `<script id="__NEXT_DATA__">` blocks in the raw HTML.
- The XHR/fetch requests the page itself makes (browser network panel or Playwright request interception) — calling the site's own JSON endpoint directly is often the cleanest extraction path.

Typical wins: full item lists, IDs (for example every video `vid`), and clean titles without touching the UI. Only drive the visible UI when no embedded data or underlying endpoint exists.

## Browser Tool Failure Fallback

Browser tools fail in predictable ways; do not burn turns rediscovering the fixes:

1. Run the tool's own health check first: `agent-browser doctor` (and `firecrawl doctor` for Firecrawl-side issues) before assuming the target site is at fault.
2. If `agent-browser` fails to start (for example CDP channel errors such as `response channel closed`) and `doctor` does not repair it, switch to `npx playwright` instead of retrying the same launch.
3. If Playwright reports a browser version mismatch (for example it wants `chromium-1234` but only `chromium-1228` is cached), either run `npx playwright install chromium` or point Playwright at the system browser via `executablePath` (for example the installed Chrome/Edge binary) — the system browser path is usually the fastest unblocking move.
4. If no Playwright browser can launch, fall back to `browser-use` with a real Chrome profile/CDP, or to Firecrawl rendered extraction.

Record which fallback worked; later steps in the same session should reuse it directly.

## When To Use Playwright

Use an existing project Playwright command or `npx playwright` when:

- Firecrawl is unavailable or remains incomplete after a reasonable `scrape --wait-for` or `interact` attempt.
- The workflow depends on browser-only state, unsupported widgets, complex authentication, downloads, popups, or multi-tab behavior.
- The flow must run repeatedly as a test, QA check, regression, monitor, or maintained automation.
- Console, network, accessibility, screenshot, or trace evidence is required.

Prefer existing project commands:

```bash
npm test
npm run test:e2e
npx playwright test
```

For exploration or script generation:

```bash
npx playwright --help
npx playwright codegen "https://example.com"
npx playwright test --headed
npx playwright show-report
```

Rules:

- If the repository already has Playwright config, follow existing directories, fixtures, and naming.
- Do not create a Playwright test when Firecrawl already completes a one-off lookup or extraction.
- Preserve the Firecrawl failure or limitation that justified browser escalation.

## When To Use agent-browser

Use `agent-browser` when one-off visual exploration is required and it is more efficient than creating or adapting a Playwright flow:

- The user asks to see what the page visibly displays.
- Accessibility snapshots, clicks, screenshots, console errors, or page state evidence are needed.
- Firecrawl cannot expose the required visible state and a maintained Playwright artifact is unnecessary.

Common commands:

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/page.png
agent-browser close
```

Rules:

- Run `snapshot` before operating by `@ref`; do not guess selectors blindly.
- Ask the user before credentials, payments, account changes, form submission, or destructive operations.
- Do not reveal cookies, tokens, profile paths, or credentials in final output.

## When To Use browser-use

Use `browser-use` when:

- It is already configured locally and is more stable than other browser tools in the environment.
- A real Chrome profile or CDP connection is needed.
- Playwright and `agent-browser` are unavailable but interactive browsing is still required.

Common commands:

```bash
browser-use doctor
browser-use open "https://example.com"
browser-use state
browser-use screenshot /tmp/page.png
browser-use extract "Extract the main prices and product names from this page"
browser-use close
```

## When Not To Use A Browser

Do not escalate to a browser when:

- `firecrawl search` returns sufficient sources.
- `firecrawl scrape`, including a suitable `--wait-for`, extracts the page text.
- `firecrawl map`, `crawl`, or `download` covers the documentation or site.
- `firecrawl interact` completes the required supported interaction.
- `gh`, `npm view`, `pip index`, `cargo search`, or `go list` returns structured answers.
- The user only needs explanation, facts, comparisons, or sources, not page interaction evidence.

## Checkpoint Before Escalating From Firecrawl To Browser

Confirm at least one condition:

- Firecrawl was unavailable or a reasonable scrape/interact attempt still misses key content or state.
- The user cares about the actual visible state of the page, not just extracted content.
- Unsupported filters, widgets, authentication, downloads, popups, or multi-tab behavior must be operated.
- Screenshots, browser traces, console output, or network evidence are needed.
- The flow must become a repeatable browser test or maintained automation.

If none apply, keep using Firecrawl or structured CLIs.

## Browser Evidence Output

Browser-route final answers should include:

- tool used.
- key URL.
- completed operations.
- Firecrawl limitation that required escalation.
- unfinished or permission-blocked operations.
- screenshot, downloaded file, or artifact path if produced.

Example:

```markdown
**Browser Evidence**
- Tool: Playwright
- Final URL: https://example.com/results
- Firecrawl limit: required browser-only authenticated state
- Screenshot: /tmp/page.png
- Limit: login is required for full results
```
