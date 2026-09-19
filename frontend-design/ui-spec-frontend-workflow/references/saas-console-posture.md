# Default SaaS operations console posture

Use this default for Yeisme engineering tools, Agent consoles, MCP Gateway, Ordo, diagnostics, internal systems, and control surfaces unless a local design system overrides it:

- Product type: modern SaaS operations console, engineering tool, Agent console, internal system, or operations workbench.
- Style keywords: restrained, clear, trustworthy, high information density without crowding, low saturation, non-marketing.
- First viewport: show data, filters, tables, status, and actions immediately. Do not build a hero, large illustration, decorative gradient, or landing-page composition for admin surfaces.
- Layout shell: fixed left sidebar, top bar, primary workspace, optional right inspector or detail panel.
- Sidebar: about 240px wide, light neutral background, thin right border, active item uses subtle background plus primary text, not a large color block.
- Top bar: 56px to 64px high with global search, theme toggle, user menu, and sign-out.
- Workspace: `p-4 md:p-6`, common page rhythm `space-y-6`; lists should use available width, forms should limit readable width, editors and previewers use a full-width workbench.
- PageHeader: compact title `text-2xl font-semibold tracking-tight`, optional description `text-sm text-muted-foreground`, primary action on the right.
- Typography: Inter or `system-ui` for UI; mono font for code, IDs, traces, logs, paths, and metrics.
- Spacing: 4, 8, 12, 16, 24, 32 token scale.
- Radius: 6px to 8px for most surfaces and controls. Avoid overly round UI.
- Background and surfaces: page background should be neutral near-white such as `bg-muted/30`; content surfaces use `bg-card` or white with `border-border`. Use light shadow only for dialogs, floating overlays, drag panels, or other elevated UI.
- Color: use semantic tokens only: `background`, `foreground`, `muted`, `muted-foreground`, `card`, `border`, `primary`, `success`, `warning`, `destructive`, `info`, and `chart-1` through `chart-5`.
- Primary color: low-saturation blue-cyan, reserved for primary buttons, active nav, links, and focus rings. It must not dominate the page.
- Status color examples: `bg-success/15 text-success border-success/20`, `bg-warning/15 text-warning border-warning/20`, `bg-info/15 text-info border-info/20`, and `text-destructive`.
- Charts: use Recharts and no more than five semantic chart colors, `chart-1` through `chart-5`.
- Motion: subtle feedback only; animation explains state changes and never becomes decoration.

Preferred React stack for new Yeisme product surfaces when the owning project does not already choose another system:

- React 19 + TypeScript + Vite + Bun
- Tailwind CSS 4 as the styling runtime, CSS-first `@theme` semantic tokens
- shadcn/ui as the primary component source, `new-york` style, neutral base, component source under `components/ui/`
- Radix primitives through shadcn/ui
- lucide-react icons
- React Router 7 for routes
- TanStack Query 5 for server state
- TanStack Table 8 for dense tabular data, with `@tanstack/react-virtual` when row count or viewport size requires it
- React Hook Form + Zod + `@hookform/resolvers` for forms
- sonner for toast
- Recharts for charts
- cmdk for Cmd/Ctrl+K global command palette
- `motion` for micro-interactions
- `react-resizable-panels` for workbench panes
- `react-hotkeys-hook` for shortcuts when needed
- `qrcode.react`, `react-syntax-highlighter`, and `papaparse` when those capabilities are needed
- `next-themes` for theme switching in Vite/React projects unless the local app already has a theme system
- MSW for API mocks
- Playwright / `@playwright/test` for E2E and visual evidence
- Native `fetch` wrapped in a typed API client. Do not introduce axios for new frontend work.
- Bun for frontend commands and dependency changes. Do not use npm, pnpm, or yarn in new frontend work unless the owning project already mandates them.
- Storybook plus Playwright or Chromatic for visual evidence

Styling architecture for React/Vite/Next product surfaces:

- Use utility-first implementation by default: Tailwind CSS 4 utilities in JSX plus semantic tokens.
- Put theme tokens in one global entry only, usually `src/tailwind.css`, using `@theme`, CSS variables, and base reset.
- Build reusable surfaces through component recipes, such as `class-variance-authority` variants and small primitives for Button, Panel, Badge, Field, Tabs, Sheet, Dialog, Tooltip, and Inspector.
- Prefer shadcn/ui and Radix primitives for accessible controls; do not hand-roll focus management, overlay positioning, menu keyboard behavior, or dialog traps.
- Page and component styling must not be written as naked CSS selectors. Do not add `.page-name`, `.feature-card`, `.foo button`, or route-specific selector blocks for new UI.
- Raw CSS is only acceptable for Tailwind entry directives, design tokens, global base reset, unavoidable third-party overrides, or documented browser quirks. If one of those exceptions is used, keep it in the global style boundary and explain why.
- Dark mode, density, accent, and font choices must flow through tokens or component recipes. Do not patch individual components with hardcoded dark colors.
