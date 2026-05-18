# Browser Tool Guide

## Purpose

Explain when an internet information task should escalate to a browser, and how to choose among `agent-browser`, existing project Playwright commands, `npx playwright`, `browser-use`, and static extraction. This file is an escalation route inside `internet-access`, not a separate skill.

## Principle

A browser is not the default search tool. Use search, scraping, or structured CLIs first. Use a browser only when real page state, interaction, or dynamic rendering is part of the answer.

Priority:

1. `firecrawl search` / `firecrawl scrape`: search and static content.
2. `gh` / package manager CLIs: structured sources.
3. `agent-browser`: interactive AI browsing, accessibility snapshots, clicks, screenshots, debugging.
4. Existing project Playwright commands or `npx playwright`: repeatable, testable browser workflows that can be committed to a project.
5. `browser-use`: an alternative interactive browser tool when locally configured and more suitable for the environment.

## When To Use agent-browser

Use `agent-browser` when:

- The page must be opened to inspect real UI state.
- The task needs clicks, fills, pagination, or content reading via accessibility tree `@ref`s.
- Screenshots, PDFs, console errors, network requests, or page state evidence are needed.
- The task is one-off exploration and not worth a Playwright script.
- The user asks to open a page, click something, take a screenshot, or report what the page displays.

Common commands:

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser click "@e2"
agent-browser fill "@e3" "search text"
agent-browser press Enter
agent-browser screenshot /tmp/page.png
agent-browser get url
agent-browser get title
agent-browser console
agent-browser errors
agent-browser close
```

If this is the first use or command details are uncertain, read the locally installed core skill:

```bash
agent-browser skills get core --full
```

Rules:

- Run `snapshot` first, then operate by `@ref`; do not guess CSS selectors blindly.
- For user-visible evidence, prefer screenshots or final URL records.
- Ask the user before login, paid actions, account changes, form submission, or destructive operations.
- Do not reveal cookies, tokens, profile paths, or credentials in final output.

## When To Use Playwright

Use an existing project Playwright command or `npx playwright` when:

- The browser flow must run repeatedly.
- The result belongs in project tests, QA, regression, or monitoring.
- The page flow is stable and selectors are maintainable.
- The user explicitly asks for automation scripts, tests, or repeatable execution.

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
- Do not create a Playwright test for a one-off web lookup.
- Explore uncertain pages with `agent-browser` first, then harden stable flows into Playwright.

## When To Use browser-use

Use `browser-use` when:

- It is already configured locally and is more stable than other browser tools in the environment.
- A real Chrome profile or CDP connection is needed.
- `agent-browser` is unavailable but interactive browsing is still required.

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
- `firecrawl scrape` extracts the page text.
- `gh`, `npm view`, `pip index`, `cargo search`, or `go list` returns structured answers.
- The user only needs explanation, facts, comparisons, or sources, not page interaction evidence.

## Checkpoint Before Escalating From Search To Browser

Confirm at least one condition:

- Search found the page, but scraping misses key content.
- The user cares about the actual visible state of the page, not just docs text.
- Filters, pagination, menus, login state, or download buttons must be operated.
- Screenshots/PDFs are needed as evidence.

If none apply, keep using search, scraping, or structured CLIs.

## Browser Evidence Output

Browser-route final answers should include:

- tool used.
- key URL.
- completed operations.
- unfinished or permission-blocked operations.
- screenshot, downloaded file, or artifact path if produced.

Example:

```markdown
**Browser Evidence**
- Tool: agent-browser
- Final URL: https://example.com/results
- Screenshot: /tmp/page.png
- Limit: login is required for full results
```
