---
name: yeisme-frontend-quality-workflow
description: Use when adding, changing, testing, or reviewing frontend tooling and UI quality gates in this repository, including Impeccable-style deterministic detection, default SaaS operations console style conformance, Storybook design-system stories, Tailwind CSS in Storybook, Chromatic or Playwright visual regression, @storybook/addon-designs, Lighthouse, Axe accessibility checks, Front-End Checklist rule/MCP lookups, browser-use driven real browser integration tests, and Cohors-style diagnostics summaries.
---

# Yeisme Frontend Quality Workflow

Use this skill for frontend toolchain and UI quality work in Yeisme projects.

## Scope

- Default frontend stack conformance: React 19, TypeScript, Vite, Bun, Tailwind CSS 4 CSS-first `@theme`, shadcn/ui `new-york` neutral components in `components/ui/`, lucide-react, React Router 7, TanStack Query 5, TanStack Table 8, React Hook Form + Zod, sonner, Recharts, Playwright, and MSW.
- Default SaaS operations console style conformance: dense but readable operations UI, fixed sidebar plus top bar shell, neutral surfaces, compact PageHeader, semantic status colors, restrained shadows, 6px to 8px radius, no hero or decorative gradients.
- Component workbench: Storybook.
- Styling in stories: Tailwind CSS wired through Storybook preview/global CSS.
- Styling boundary: Tailwind CSS 4 utilities, semantic tokens, and component recipes; no new page-specific naked CSS.
- Visual review: Chromatic, Storybook published builds, and Playwright screenshots.
- Design-system regression: token stories, component states, page-pattern stories, and density checks.
- Interaction regression: dropdowns, dialogs, popovers, sheets, image previews, table controls, forms, keyboard behavior, and overlay states.
- Design references: `@storybook/addon-designs`.
- Quality gates: Lighthouse, Axe, keyboard navigation, ARIA, color contrast, console errors, network failures.
- External rules corpus: Front-End Checklist for launch, accessibility, SEO, security, performance, image, privacy, i18n, HTML, CSS, JavaScript, and testing rule lookups.
- Real integration testing: Playwright plus browser-use for browser workflows that should exercise the app like a user.
- TypeScript Web/Node test layering: Vitest, Testing Library, MSW, Supertest or framework injection, Testcontainers or docker compose, and limited Playwright browser E2E.

## Boundaries

- Do not add Storybook, Chromatic, Lighthouse, Axe, or browser-use to a project without checking its package manager and frontend framework first.
- Do not store Chromatic project tokens, browser-use API keys, or service credentials in tracked files.
- Do not rely on screenshots alone for frontend acceptance. Include structured diagnostics.
- Do not vendor the full Front-End Checklist rule corpus into this repository. Link to the upstream rules or use its MCP/skills when a task needs that external coverage.
- Do not treat a Front-End Checklist MCP or website pass as final acceptance unless findings are converted into deterministic local checks, screenshots, Storybook stories, Axe/Lighthouse results, Playwright assertions, or diagnostics evidence.
- Do not accept AI-generated UI only because it renders. It must preserve design-system tokens, page pattern, component states, density, and responsive behavior.
- Do not accept frontend work that ignores the default SaaS operations console style unless a local project design system explicitly overrides it.
- Do not accept new React UI implemented through route/page-specific CSS selectors. Styling must be assembled from Tailwind utilities, tokens, and reusable component recipes; global CSS is reserved for Tailwind entry, tokens, reset, and documented third-party overrides.
- Do not accept hardcoded hex colors in business components; colors must flow through semantic tokens such as `primary`, `success`, `warning`, `destructive`, `info`, and `chart-1` through `chart-5`.
- Do not accept hand-written SVG icons when `lucide-react` has a suitable icon.
- Do not accept axios in new frontend code; HTTP should use native `fetch` through a typed API client.
- Do not accept new untyped JavaScript frontend app files.
- Do not use npm, pnpm, or yarn commands for new frontend work; use Bun unless the owning project already mandates a different package manager.
- Do not add a second test framework when the owning TypeScript Web/Node project already has a suitable runner and harness.
- Do not accept a page whose controls only look real. Visible interactive controls must open, close, select, filter, preview, dismiss, navigate, submit, or expose an intentional disabled/pending state.
- Do not use browser-use as a replacement for deterministic Playwright assertions; use it for exploratory or high-level real browser flows, then keep stable assertions in Playwright.
- Do not block a narrow backend-only change on Storybook or Lighthouse unless UI behavior changed.

## Deterministic Quality Gate

Use an Impeccable-style gate for AI-generated or AI-modified frontend work: deterministic checks first, browser evidence second, subjective design commentary last.

When Impeccable is installed and the local Node.js version supports it, prefer these checks for frontend files or deployed pages:

```bash
npx impeccable detect src/
npx impeccable detect --json .
npx impeccable detect https://example.com
```

Do not casually upgrade a project to Node.js 24 only to run Impeccable. If the tool is unavailable, reproduce the same gate with the project's existing lint, typecheck, Storybook, Playwright, Axe, Lighthouse, and targeted source scans.

The gate should check at least:

- off-token colors, hardcoded hex values, radius drift, shadow drift, and typography drift
- new naked CSS selectors, route-specific CSS, and unapproved global style changes
- text overflow, clipped controls, overlapping overlays, horizontal scroll, and mobile breakage
- missing loading, empty, error, disabled, hover, selected, focus, dense data, and mobile states
- fake controls that look clickable but do not open, select, filter, preview, navigate, submit, or expose an intentional pending/disabled state
- keyboard navigation, focus return, dialog/menu escape behavior, ARIA, contrast, and accessible names
- console errors, failed network requests, hydration/runtime warnings, and broken asset loads
- admin-console posture violations such as marketing heroes, decorative gradients, low-density stat-card filler, and all-centered layouts

Open Design Studio, Stagewise, Onlook, browser-use, and similar browser tools may accelerate exploration and visual diagnosis. Final acceptance still needs reproducible evidence through Playwright, Storybook, Chromatic, Axe, Lighthouse, the local test runner, or an explicit manual fallback when infrastructure is out of scope.

Taste or brand guidance is useful before implementation, but it is not a substitute for product UI quality gates.

## Workflow

1. Read the local frontend package files first:
   - `package.json`
   - `bun.lock` or the package manager lockfile
   - `components.json` and `components/ui/` when shadcn/ui is present
   - Storybook config under `.storybook/`
   - Vite/Next/Tailwind/PostCSS config
   - existing Playwright tests
2. Identify the UI quality scope:
   - component stories only
   - page or route stories
   - visual regression
   - accessibility and keyboard checks
   - browser workflow smoke tests
   - Lighthouse or performance audit
3. For AI-generated or AI-modified UI, require a UI Spec or equivalent design-system contract before visual acceptance:
   - selected page pattern
   - allowed tokens and component libraries
   - desktop and mobile viewports
   - loading, empty, error, dense data, selected, hover, focus, and disabled states
   - interaction control inventory for dropdowns, dialogs, popovers, sheets, image previews, table controls, and forms
   - visual blacklist violations to check
   - styling boundary: Tailwind entry + tokens only in CSS, JSX utilities and recipes for component/page styling
   - admin console checks: no hero, no decorative gradients, fixed sidebar/top bar shell when building a management app, compact PageHeader, semantic statuses, restrained radius and shadows, DataTable density, Cmd/Ctrl+K command palette where global search exists
4. If Storybook is missing, initialize with the package manager used by that frontend, for example:

```bash
bunx storybook@latest init
```

5. For Tailwind CSS in Storybook:
   - import the app's Tailwind CSS entry in `.storybook/preview.ts` or `preview.tsx`
   - keep Storybook and app tokens pointed at the same design system source
   - for Vite projects, avoid extra PostCSS addons unless the project needs them
   - confirm stories render through the same utility-first tokens and component recipes as the app
   - fail or warn when new `.css` files or new page-specific selectors appear outside the approved global style boundary
6. Add stories for touched reusable components and product surfaces. For AI-generated UI, default stories should include:
   - `Default`
   - `Loading`
   - `Empty`
   - `Error`
   - `DenseData`
   - `Selected`
   - `Open`
   - `Disabled`
   - `KeyboardFocused`
   - `Mobile`
   - `DarkMode` when the app supports dark mode
7. For page-level stories, represent the selected pattern explicitly, for example:
   - `DashboardOverview`
   - `ListDetail`
   - `TableInspector`
   - `TimelineEventDetail`
   - `ApprovalQueue`
   - `ArtifactBrowser`
   - `Diagnostics`
   - `SettingsControl`
   - `CostUsage`
   - `EmptyOnboarding`
8. For Chromatic:
   - add the `chromatic` package or use the CLI through the package manager
   - keep the project token in CI secrets, not in source
   - document the publish/check command near the frontend package scripts
   - set stable viewports for desktop and mobile where the project supports it
   - treat visual diffs as review artifacts that must map back to tokens, layout, component states, or intentional product changes
9. For Playwright screenshot regression:
   - capture fixed desktop and mobile viewports for changed routes or stories
   - capture open states for changed dropdowns, dialogs, popovers, sheets, command menus, image previews, and table overflow menus
   - include dense data and empty/error states for operational screens
   - fail on console errors and unexpected failed network requests
   - compare screenshots against the UI Spec or approved baseline, not only against subjective taste
10. For `@storybook/addon-designs`:
   - install and register it in `.storybook/main.ts`
   - attach design URLs in story `parameters.design`
   - prefer specific Figma frame URLs over top-level file URLs
   - when using generated reference images, attach the written UI Spec or design doc alongside the image reference
11. Add quality gates:
   - Lighthouse for accessibility, performance, SEO, best practices, and PWA where relevant
   - `@axe-core/playwright` for repeatable accessibility assertions
   - keyboard navigation checks for dialogs, menus, tabs, forms, tables, command palettes, and route changes
   - interaction checks for overlay open/close, Escape handling, outside click, focus return, disabled actions, loading guards, and image preview behavior
   - console error and failed network request capture in Playwright
12. Use Front-End Checklist when a public launch, broad audit, or rule-specific review needs wider coverage than the local gate:
   - browse https://frontendchecklist.io/rules for manual rule lookup
   - use the public MCP endpoint `https://mcp.frontendchecklist.io` only in MCP-capable clients or subprojects that explicitly configure it
   - use `search_rules` before giving frontend accessibility, SEO, security, image, privacy, i18n, or performance recommendations when MCP is available
   - use `get_workflow`, `get_checklist_rules`, or `get_quick_reference` for launch, accessibility, SEO, security, and performance audits when MCP is available
   - convert every accepted finding into local evidence through Playwright, Storybook, Chromatic, Axe, Lighthouse, typecheck, lint, tests, diagnostics, or a documented manual fallback
13. Add browser-use only where realistic integration value is higher than deterministic test complexity:
   - onboarding flows
   - multi-page task completion
   - exploratory smoke runs after large UI changes
   - flows with dynamic content where strict selectors are brittle
14. For ordinary TypeScript Web/Node testing, keep the test layer explicit:
   - `unit`: Vitest for pure functions, single objects, and complex rules
   - `integration`: Vitest for service/repository, component/store/API mock, or API handler + app harness
   - `component`: one complete frontend page or backend service component with real or controlled dependencies and mocked external boundaries
   - `system`: multiple services started together for system-level behavior
   - `e2e`: user or automation entry through the full business chain; browser paths use Playwright, CLI/API paths do not require a browser
15. Use the default TypeScript Web/Node stack unless the project already has an equivalent:
   - Vitest as the main test runner
   - Testing Library + MSW for frontend component/page integration tests
   - Supertest, Fastify `inject()`, or framework injection for backend HTTP/API integration tests
   - Testcontainers or the project's docker compose/test harness for PostgreSQL, Redis, MQ, MinIO, and other real dependencies
   - Playwright for a small number of critical browser E2E paths
16. Keep CI checks separated: run typecheck such as `tsc --noEmit` separately because Playwright does not type-check the app.
17. Report results as diagnostics, not prose only:

```text
Diagnostics:
  design tokens       ● ok       no off-system colors or radius values
  story coverage      ▲ warning  missing DenseData story for RunsTable
  interactions        × failed   artifact thumbnail opens no preview dialog
  visual regression   ● ok       1440x960 and 390x844 screenshots accepted
  accessibility       ▲ warning  3 contrast issues
  performance         ● ok       score 92
  console errors      × failed   2 runtime errors
  network failures    ▲ warning  1 failed request
  keyboard navigation ● ok       tab order verified
  browser workflow    ● ok       create project flow completed
```

## Suggested Commands

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

## AI Frontend Design Review Gate

Before accepting AI-generated frontend work, verify:

- Design-system assembly: the UI uses approved tokens, component libraries, typography scale, radius, and semantic colors.
- Admin console posture: the first viewport shows operational data, filters, tables, status, and actions directly; no hero, large illustration, decorative gradient, or marketing layout.
- Stack conformance: shadcn/ui `new-york` neutral primitives, lucide-react icons, React Router routes, TanStack Query server state, TanStack Table data grids, React Hook Form + Zod forms, sonner toasts, Recharts charts, MSW mocks, and Playwright E2E are used where those capabilities are needed.
- Styling architecture: React styling is Tailwind CSS 4 utilities plus tokens and component recipes; CSS files contain only Tailwind entry, tokens, base reset, and documented third-party overrides.
- API and package discipline: native `fetch` API client instead of axios; TypeScript app code; Bun commands for new frontend work.
- Theme legibility: dark/night mode, font family, density, accent, hover, selected, disabled, and focus states all inherit from the same token system without hardcoded light-mode leaks.
- Page pattern: the implemented layout matches the selected pattern and is not a generic stat-card dashboard unless that is the approved pattern.
- Visual blacklist: no broad blue-purple gradients, glassmorphism, excessive shadows, random emoji, random colors, decorative hero sections, or meaningless metric cards.
- State completeness: loading, empty, error, dense data, selected, hover, focus, disabled, and mobile states exist where relevant.
- Interaction completeness: every visible control has real behavior or an intentional disabled/pending state; overlays open and close correctly; images and artifacts preview according to spec.
- Product clarity: the page answers a clear operational question and exposes the next recommended action.
- Engineering quality: stories or screenshots are deterministic, accessibility checks run, console errors are captured, and visual changes have traceable evidence.

## Required Interaction Coverage

When these controls are touched, add a Storybook story, Playwright interaction check, or documented manual fallback:

| Control | Required Checks |
| --- | --- |
| Select / Combobox | opens, keyboard selects, empty/loading option, selected value persists |
| Dropdown / Context menu | trigger alignment, disabled item, action fires or is intentionally stubbed, Escape closes |
| Dialog / AlertDialog | focus trap, title/description, Escape or explicit close, destructive confirmation |
| Popover / HoverCard | anchored position, outside click behavior, focus return |
| Sheet / Drawer | mobile behavior, scroll lock, close affordance |
| Image / Artifact preview | thumbnail click, loading, error, aspect ratio, close, optional next/previous |
| Table controls | sort, filter, pagination, row selection, dense data, empty data |
| Forms | labels, validation, submit loading, server error, disabled/save states |
| Toast / Alert | semantic styling, dismiss policy, retry or next action where useful |
| Command palette | open shortcut or trigger, search, no results, keyboard navigation |

## Completion Standard

Before calling frontend quality work complete:

- Storybook starts or builds for the touched frontend when Storybook is in scope.
- Tailwind stories render with the same tokens as the app when Tailwind is in scope.
- Styling boundary checks pass or are explicitly documented: no new CSS files, no new page selectors, and no hardcoded dark-mode exceptions outside approved token/base CSS.
- Touched UI has stories or screenshots for default, loading, empty, error, dense data, and mobile states when those states are relevant.
- Touched interactive controls have open, disabled, focused, keyboard, and failure/empty states covered by stories, Playwright, or explicit fallback evidence.
- Chromatic config is documented and token-safe when visual publishing is in scope.
- Visual regression evidence exists through Chromatic, Playwright screenshots, or an explicit documented fallback.
- Accessibility checks cover color contrast, ARIA, focus order, and keyboard navigation.
- Desktop and mobile viewport checks confirm no text overflow, control overlap, clipped menus, inaccessible icon buttons, or broken sidebar/top-bar responsive behavior.
- Playwright captures console errors and network failures for core flows.
- Lighthouse or an equivalent audit has fresh evidence for user-facing pages.
- Real browser integration tests use browser-use only as an aid; pass/fail remains machine-checkable.
