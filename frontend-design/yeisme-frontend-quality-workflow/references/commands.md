# Frontend quality commands

Use Bun for new frontend work unless the owning project already mandates another package manager. Examples:

```bash
bun run typecheck
bun test
bun run storybook
bun run build-storybook
bunx chromatic --project-token "$CHROMATIC_PROJECT_TOKEN"
bunx lighthouse http://localhost:3000 --view
bunx playwright test accessibility.spec.ts
bunx playwright test visual.spec.ts
bunx playwright test interactions.spec.ts
npx skills add frontendchecklist/skills
npx skills add frontendchecklist/skills --skill https
```

For MCP-capable clients that explicitly opt in, use the public Front-End Checklist endpoint:

```text
https://mcp.frontendchecklist.io
```

Useful prompts:

```text
Use the Front-End Checklist MCP to review this React component and report the highest-confidence findings first.
Use the Front-End Checklist MCP to audit https://example.com for accessibility, performance, and SEO issues.
Use the Front-End Checklist MCP to give me a performance checklist in markdown format.
```

For Playwright + Axe:

```bash
bun add -d @axe-core/playwright
```

For browser-use, follow the local language runtime selected by the project. Keep credentials in local env or CI secrets and wrap any AI-assisted browser run with deterministic Playwright assertions for the final gate.

For Front-End Checklist, use the website, MCP, or optional skills as external guidance. Do not copy the upstream rule corpus into this repository; record links and local verification evidence instead.

If the external `browser-use` skill is available, use it only as an exploratory or smoke-test aid. Do not treat browser-use success as final acceptance unless the result is converted into deterministic Playwright assertions, Storybook stories, Chromatic baselines, or diagnostics evidence.

When Impeccable is installed and the local Node.js version supports it:

```bash
npx impeccable detect src/
npx impeccable detect --json .
npx impeccable detect https://example.com
```

Do not casually upgrade a project to Node.js 24 only to run Impeccable. If the tool is unavailable, reproduce the same gate with the project's existing lint, typecheck, Storybook, Playwright, Axe, Lighthouse, and targeted source scans.
