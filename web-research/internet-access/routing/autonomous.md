# Autonomous Browser Route

## Purpose

Handle tasks that require browser interaction, dynamic content, authentication, repeated navigation, downloads, forms, screenshots, or multi-step web workflows. Prefer existing local browsers and CLI tools. Create automation scripts only when the user needs a reusable artifact. See `browser_tools.md` for tool details.

## When To Use

- Static search or scraping is insufficient.
- The user asks for login, clicks, form filling, filtering, downloads, monitoring, or automation.
- The site depends on JavaScript-rendered state.
- Data must be collected across multiple pages with state-dependent branches.

## Local Tool Priority

Prefer locally configured automation tools because they may already have browser binaries, profiles, credentials, and network access:

```bash
command -v agent-browser
command -v browser-use
command -v npx
command -v firecrawl
```

Tool choice:

- Use `agent-browser` first when the task needs an AI agent to observe, click, and read page state step by step.
- Use existing project Playwright commands or `npx playwright` for known, repeatable workflows that should become tests or long-term automation.
- Use `agent-browser` for visual exploration or uncertain UI state; if unavailable, use `browser-use` or built-in browser tools.
- Fall back to `firecrawl scrape` or `firecrawl crawl` for static extraction.
- If structured data exists, prefer source-specific CLI/API instead of browser automation; for example, use `gh` only for GitHub.
- Do not write new wrapper scripts for one-off exploration.

## Workflow

1. Split the task into steps and define success criteria.
2. Check local browser/search CLIs and read `browser_tools.md` for tool selection.
3. Try the lowest-cost reliable path first:
   - structured CLI (use `gh` for GitHub; package managers for package registries)
   - `firecrawl search` / `firecrawl scrape`
   - browser automation when interaction is needed
4. Preserve evidence: final URL, screenshots or downloaded files if needed, and extracted records.
5. Pause for user confirmation only when credentials, permissions, payments, or destructive actions are involved.

## Example Patterns

Known static source:

```bash
firecrawl scrape "https://github.com/trending"
```

GitHub structured data:

```bash
gh search repos "stars:>10000 language:TypeScript" --sort stars --limit 10
```

Browser workflow:

```bash
agent-browser skills get core --full
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser screenshot /tmp/example.png
npx playwright --help
npx playwright codegen "https://example.com"
browser-use --help
```

If the repository already has a project-specific Playwright script, use that first.

## Output Format

```markdown
**Execution Summary**
- Route: autonomous
- Tools used: [local CLI / browser tool]
- Completed: [successful work]
- Blocked: [failed work or items needing user access]

**Result**
[structured data, links, files, or observations]

**Evidence**
[screenshots, URL, logs, or artifact paths]
```

## Safety

- Do not submit purchases, irreversible forms, account changes, or destructive operations without explicit user confirmation.
- Respect robots, terms of service, rate limits, and authentication boundaries.
- Avoid writing secrets into output or artifacts.
