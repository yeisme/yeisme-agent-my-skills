---
name: yeisme-frontend-quality-workflow
description: Use when adding, changing, testing, or reviewing frontend tooling and UI quality gates in this repository, including Impeccable-style deterministic detection, default SaaS operations console style conformance, Storybook design-system stories, Tailwind CSS in Storybook, Chromatic or Playwright visual regression, @storybook/addon-designs, Lighthouse, Axe accessibility checks, Front-End Checklist rule/MCP lookups, browser-use driven real browser integration tests, and Ordo-style diagnostics summaries.
---

# Yeisme Frontend Quality Workflow

Use this skill for frontend toolchain and UI quality work in Yeisme projects.

## Scope

- Default frontend stack conformance: React 19, TypeScript, Vite, Bun, Tailwind CSS 4 CSS-first `@theme`, shadcn/ui `new-york` neutral components in `components/ui/`, lucide-react, React Router 7, TanStack Query 5, TanStack Table 8, React Hook Form + Zod, sonner, Recharts, Playwright, and MSW.
- Default SaaS operations console style conformance: dense but readable operations UI, fixed sidebar plus top bar shell, neutral surfaces, compact PageHeader, semantic status colors, restrained shadows, 6px to 8px radius, no hero or decorative gradients.
- Component workbench: Storybook. Style stories through the app Tailwind entry; no new page-specific naked CSS.
- Visual review: Chromatic, Storybook published builds, and Playwright screenshots.
- Design-system regression: token stories, component states, page-pattern stories, and density checks.
- Interaction regression: dropdowns, dialogs, popovers, sheets, image previews, table controls, forms, keyboard behavior, and overlay states.
- Design references: `@storybook/addon-designs`.
- Quality gates: Lighthouse, Axe, keyboard navigation, ARIA, color contrast, console errors, network failures.
- External rules corpus: Front-End Checklist for launch, accessibility, SEO, security, performance, image, privacy, i18n, HTML, CSS, JavaScript, and testing rule lookups. Do not vendor the corpus.
- Motion gate: `yeisme-ui-motion-quality`.
- Real integration testing: Playwright plus browser-use for user-like browser workflows.
- TypeScript Web/Node test layering: Vitest, Testing Library, MSW, and limited Playwright browser E2E. Details: `references/story-and-interaction.md`.

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
- Do not make `motion`, AutoAnimate, GSAP, React Spring, or another animation library a default dependency; inspect the owning app first and justify any addition with a product need and budget.
- Do not use npm, pnpm, or yarn commands for new frontend work; use Bun unless the owning project already mandates a different package manager.
- Do not add a second test framework when the owning TypeScript Web/Node project already has a suitable runner and harness.
- Do not accept a page whose controls only look real. Visible interactive controls must open, close, select, filter, preview, dismiss, navigate, submit, or expose an intentional disabled/pending state.
- Do not use browser-use as a replacement for deterministic Playwright assertions; use it for exploratory or high-level real browser flows, then keep stable assertions in Playwright.
- Do not block a narrow backend-only change on Storybook or Lighthouse unless UI behavior changed.

## Deterministic Quality Gate

Use an Impeccable-style gate for AI-generated or AI-modified frontend work: deterministic checks first, browser evidence second, subjective design commentary last. Commands: `references/commands.md`.

The gate should check at least:

- off-token colors, hardcoded hex values, radius drift, shadow drift, and typography drift
- new naked CSS selectors, route-specific CSS, and unapproved global style changes
- text overflow, clipped controls, overlapping overlays, horizontal scroll, and mobile breakage
- missing loading, empty, error, disabled, hover, selected, focus, dense data, and mobile states
- fake controls that look clickable but do not open, select, filter, preview, navigate, submit, or expose an intentional pending/disabled state
- keyboard navigation, focus return, dialog/menu escape behavior, ARIA, contrast, and accessible names
- console errors, failed network requests, hydration/runtime warnings, and broken asset loads
- admin-console posture violations such as marketing heroes, decorative gradients, low-density stat-card filler, and all-centered layouts

Open Design Studio, Stagewise, Onlook, browser-use, and similar browser tools may accelerate exploration. Final acceptance still needs reproducible evidence through Playwright, Storybook, Chromatic, Axe, Lighthouse, the local test runner, or an explicit manual fallback when infrastructure is out of scope.

Taste or brand guidance is useful before implementation, but it is not a substitute for product UI quality gates.

## Workflow

1. Read local frontend package files first: `package.json`, lockfile, `components.json` / `components/ui/`, `.storybook/`, Vite/Next/Tailwind/PostCSS config, and existing Playwright tests.
2. Identify the UI quality scope: component stories, page/route stories, visual regression, accessibility/keyboard, browser workflow smoke, or Lighthouse.
3. For AI-generated or AI-modified UI, require a UI Spec before visual acceptance: page pattern, allowed tokens/components, desktop/mobile viewports, loading/empty/error/dense/selected/hover/focus/disabled states, control inventory, visual blacklist, Tailwind-only styling boundary, admin console checks, and motion contract via `yeisme-ui-motion-quality`.
4. If Storybook is missing, initialize with the project's package manager, for example `bunx storybook@latest init`. Import the app Tailwind entry in `.storybook/preview.ts`; keep tokens identical; fail or warn on new page-specific CSS.
5. Add stories for touched reusable components and product surfaces. Names, page-pattern stories, and interaction coverage: `references/story-and-interaction.md`.
6. Visual evidence: Chromatic project token in CI secrets only; Playwright screenshots at fixed desktop and mobile viewports including overlay open states, dense data, and empty/error. Attach `@storybook/addon-designs` URLs in `parameters.design` when Figma/spec refs exist.
7. Quality gates: Lighthouse, `@axe-core/playwright`, keyboard navigation, overlay Escape/outside-click/focus-return, console errors, and failed network requests. Front-End Checklist is external (`https://frontendchecklist.io/rules`, MCP `https://mcp.frontendchecklist.io`); convert accepted findings into local evidence.
8. Add browser-use only where realistic integration value is higher than deterministic test complexity (onboarding, multi-page completion, exploratory smoke). Keep pass/fail in Playwright. Test layering: `references/story-and-interaction.md`.
9. Keep CI typecheck separate (`tsc --noEmit`). Commands: `references/commands.md`.
10. Report diagnostics, not prose only, then apply `references/review-gate.md` before calling the work complete.

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

Example:

```bash
bun run typecheck
bunx playwright test visual.spec.ts
```

## Completion Standard

Before calling frontend quality work complete: Storybook/tokens in scope; no new page-specific CSS; stories or screenshots for default/loading/empty/error/dense/mobile; interaction open/keyboard/empty/error; Chromatic token-safe when publishing; visual evidence via Chromatic/Playwright or documented fallback; a11y contrast/ARIA/keyboard; no overflow or clipped overlays; Playwright captures console/network; Lighthouse or equivalent for user-facing pages; browser-use is an aid only. Full checklist: `references/review-gate.md`.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Screenshot-only acceptance | Add Storybook/Axe/Playwright diagnostics | Browser-use success is not the gate |
| Fake control / no open state | Interaction coverage table | Cover open, empty, error, keyboard |
| Off-token color or hero on admin | Impeccable-style gate + console posture | Local design system may override, not ignore |
| New test framework | Reuse Vitest/Playwright | Do not add a second runner |
| Chromatic token in git | CI secret only | Document the command, not the token |
