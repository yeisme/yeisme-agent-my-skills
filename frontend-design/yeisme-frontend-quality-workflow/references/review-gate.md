# AI frontend design review gate

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

Completion standard before calling frontend quality work complete:

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
