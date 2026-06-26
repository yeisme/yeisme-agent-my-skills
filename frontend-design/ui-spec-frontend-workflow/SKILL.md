---
name: ui-spec-frontend-workflow
description: Use when turning product ideas, PRDs, wireframes, screenshots, high-fidelity UI images, or Open Design handoffs into React/web frontend implementation or visual fixes; enforce Open Design first-use discovery, single design direction selection, the default SaaS operations console style, design-system assembly, UI Spec, page patterns, component tree, React animation rules, and screenshot regression before code is accepted.
---

# UI Spec Frontend Workflow

Use this skill when work touches React or web frontend screens and the source of truth includes an idea, PRD, wireframe, screenshot, design mock, GPT Image output, or visual diff.

This is a frontend development skill adapted for React product UIs. It is not a generic design-writing skill and not a terminal UI skill.

## Core Rule

Do not treat an image as the only source of truth, and do not let AI freely invent a visual system.

AI-generated frontend should be assembled inside an explicit design system:

- product type and style posture
- semantic design tokens
- approved component library
- page pattern
- layout dimensions and responsive rules
- visual blacklist
- component states
- interactive control inventory
- motion policy
- visual acceptance evidence

Frontend implementation must be driven by:

- product scenario or PRD
- information architecture and user path
- design tokens
- approved page pattern
- component tree
- interactive control contracts
- layout dimensions and responsive rules
- component states
- motion tokens and animation policy
- screenshot regression evidence

If a reference image and UI Spec conflict, follow the UI Spec and call out the conflict.

If Open Design is available, use it as the first discovery and handoff tool before inventing a local visual direction. Open Design does not replace the owning project's implementation checks or acceptance evidence.

## Design Stack Selection

Use one clear design direction layer for non-trivial UI work. Do not stack Taste, Anthropic frontend-design, UI UX Pro Max, Impeccable, and local Yeisme rules as equal authorities.

Default order:

1. Run Open Design discovery when the CLI is available:

```bash
od status --json
od skills list
od design-systems list
```

Use Open Design for reference collection, design-system selection, Studio exploration, image/prototype generation, and handoff artifacts. Treat its output as design input that must still be translated into the owning app's tokens, components, tests, and evidence.

2. Choose exactly one aesthetic direction layer:

- Taste Skill or `design-taste-frontend`: use for landing pages, brand sites, portfolios, marketing pages, creative redesigns, and one-off campaign pages. Do not make it the default authority for dashboards, dense tables, settings, admin consoles, or multi-step product flows.
- Anthropic `frontend-design`, the local project design system, or this Yeisme SaaS operations console posture: use for product UI, dashboards, internal tools, agent consoles, MCP/admin surfaces, and form-heavy workflows.
- UI UX Pro Max or other design knowledge retrieval: use as a candidate database for style, layout, and component options; do not auto-accept the first industry-template recommendation.

3. Use Impeccable-style checks after implementation as a quality gate, not as the only taste source. Prefer deterministic findings, browser evidence, and project-specific exceptions over vague taste commentary.

4. Treat component supply and screenshot-to-code tools as sources, not direction setters. 21st.dev Magic, shadcn registry components, OpenUI, and screenshot-to-code can speed up local components or reference reconstruction, but the UI Spec still owns product posture, tokens, states, and acceptance.

For canvas-like product UI, choose the interaction substrate before designing screens:

- Use `@xyflow/react` for Dify/n8n/agent workflow canvases, node graphs, execution DAG editors, routing diagrams, and inspector-driven node configuration. React Flow owns the frontend interaction layer only; backend services own DAG validation, execution semantics, persistence, audit, and scheduling.
- Use `tldraw` for free-form whiteboards, reference boards, moodboards, loose annotation, visual thinking, and material arrangement.
- Use X6 or another heavier graph library only for complex enterprise diagramming needs that React Flow cannot express.

## Inputs

Accept any subset of:

- product idea, PRD, user path, acceptance criteria
- reference image, screenshot, wireframe, or visual target
- existing design system files, tokens, component rules, or examples
- existing app route, component library, screenshots, or failing visual review

If only an image is provided, first extract a draft UI Spec and mark uncertain measurements. Do not jump directly to code from the image alone.

## Outputs

For new or changed UI work, produce or update:

- a UI Spec: product posture, tokens, layout regions, page pattern, responsive behavior, component states, and data/content assumptions
- a low-fidelity wireframe when the information architecture is new or uncertain
- a component tree before implementation
- an interactive control inventory for every clickable, selectable, expandable, dismissible, filterable, draggable, or previewable element
- React/web frontend code using the existing project stack and component library
- Playwright or equivalent screenshots at fixed viewports
- a visual review or diff report with actionable fixes

When the task is small, these can be concise and inline. When the task is a reusable screen or product surface, put the spec in the project-owned UI docs path if one exists, such as `docs/ui/` or the app's existing design docs.

## Required Workflow

1. Locate the owning subproject before editing code. Read the nearest `AGENTS.md`, existing UI docs, design tokens, component library, routes, and screenshot test conventions.
2. Identify whether the task is visual exploration, UI Spec authoring, implementation, visual review, or fix-after-review.
3. If a UI Spec does not exist, create a draft from the PRD and reference image before implementation. Mark uncertain image-derived values.
4. Freeze the design system before generating the page: product type, style posture, spacing scale, radius scale, semantic colors, typography, components, icons, motion, and blacklist.
5. Select a page pattern from the approved pattern library. Do not ask for a generic "nice dashboard" when a list/detail, table/inspector, queue, timeline, diagnostics, or settings pattern fits.
6. Generate or sketch a low-fidelity wireframe first when layout or hierarchy is not already settled. Use neutral blocks and labels only; no color, gradients, decorative shadows, or polish.
7. Apply the design system to the wireframe. Use existing components and tokens; do not introduce unknown visual primitives.
8. Write a component tree that names the shell, regions, repeated components, state surfaces, responsive substitutions, and interactive controls.
9. Write the interaction contract before implementation. Every control must name its primitive, states, keyboard behavior, data source, loading/error/empty behavior, and acceptance checks.
10. Implement using the existing frontend stack. Prefer mature component systems already in the project, such as shadcn/ui, Radix, Tailwind, lucide icons, TanStack Table, TanStack Query, and Motion when present.
11. Polish only after structure, token usage, and interaction behavior are correct. Polish may adjust spacing, hierarchy, empty states, hover/selected/focus states, density, and responsive behavior. It must not change information architecture.
12. Apply the React animation policy. Default to Motion, AutoAnimate, and Radix data-state CSS animation; do not introduce GSAP, React Spring, Lottie, or React Transition Group unless the UI Spec requires that category.
13. Capture screenshots with Playwright or the project's equivalent visual test command at fixed desktop and mobile viewports. Include open states for dropdowns, dialogs, popovers, sheets, and image preview when touched.
14. Compare current screenshots against the target or UI Spec. Report differences as executable fixes: layout, spacing, hierarchy, density, color, typography, states, animation behavior, interaction behavior, and responsive behavior.
15. Patch the implementation and re-run the narrowest relevant visual and interaction checks until the main issues are resolved or a blocker is explicit.

## Default Design-System Posture

Use this default SaaS operations console posture for Yeisme engineering tools, Agent consoles, MCP Gateway, Cohors, diagnostics, internal systems, and control surfaces unless a local design system overrides it:

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
- Motion for micro-interactions
- Storybook plus Playwright or Chromatic for visual evidence

Styling architecture for React/Vite/Next product surfaces:

- Use utility-first implementation by default: Tailwind CSS 4 utilities in JSX plus semantic tokens.
- Put theme tokens in one global entry only, usually `src/tailwind.css`, using `@theme`, CSS variables, and base reset.
- Build reusable surfaces through component recipes, such as `class-variance-authority` variants and small primitives for Button, Panel, Badge, Field, Tabs, Sheet, Dialog, Tooltip, and Inspector.
- Prefer shadcn/ui and Radix primitives for accessible controls; do not hand-roll focus management, overlay positioning, menu keyboard behavior, or dialog traps.
- Page and component styling must not be written as naked CSS selectors. Do not add `.page-name`, `.feature-card`, `.foo button`, or route-specific selector blocks for new UI.
- Raw CSS is only acceptable for Tailwind entry directives, design tokens, global base reset, unavoidable third-party overrides, or documented browser quirks. If one of those exceptions is used, keep it in the global style boundary and explain why.
- Dark mode, density, accent, and font choices must flow through tokens or component recipes. Do not patch individual components with hardcoded dark colors.

## Page Pattern Library

Choose one pattern before implementation and encode it in the UI Spec:

| Pattern | Use When | Default Structure |
| --- | --- | --- |
| Dashboard overview | User needs current system posture and next action | status strip, key queues, recent events, recommended action |
| List + detail | User browses resources and inspects one item | list or cards on left, detail panel on right |
| Table + inspector | User compares dense entities | 70% table, 30% inspector, sticky header, selectable rows |
| Timeline + event detail | User investigates traces, logs, or audits | timeline/list, filters, selected event detail |
| Approval queue | User reviews pending decisions | priority queue, risk signals, approve/deny controls, history |
| Artifact browser | User navigates files, outputs, or generated assets | tree/list, preview, metadata inspector |
| Diagnostics page | User finds and fixes system issues | health matrix, failing checks, trace links, remediation |
| Settings/control page | User configures system behavior | grouped settings, validation, danger zone, save state |
| Cost/usage analysis | User tracks spend, tokens, compute, or quota | trend, breakdown table, budget warnings, export |
| Empty onboarding page | User has no data yet | compact explanation, one recommended action, import/create path |

## Three-Stage Generation

When AI is generating or changing a non-trivial UI, split the work:

1. Wireframe: grayscale layout only. Focus on information hierarchy, regions, density, and user path. No color, gradients, shadows, decorative icons, or final copy polish.
2. Design-system pass: apply approved components, semantic tokens, spacing, typography, radius, icon rules, and states. No new component style families.
3. Polish pass: refine spacing, alignment, visual hierarchy, empty/loading/error states, hover/selected/focus behavior, and responsive behavior. Do not change layout intent.

The same agent may implement all stages, but the output must make it clear which stage is being changed. For high-risk UI, use a separate review agent or review pass before polish is accepted.

## UI Spec Minimum Shape

Use this shape when no project-specific template exists:

```yaml
page:
  name: Example Page
  route: /example
  viewports:
    desktop: 1440x960
    mobile: 390x844

design_tokens:
  product_posture:
    type: engineering-tool
    keywords: [high-density, calm, professional, low-saturation, non-marketing]
  typography:
    family: Inter or existing project font
    mono_family: existing mono font
    base_size: 14
  spacing:
    scale: [4, 8, 12, 16, 24, 32]
  radius:
    default: 8
    card: 8
    button: 8
  color:
    allowed_semantic_tokens: [background, foreground, muted, muted-foreground, card, border, primary, success, warning, destructive, info, chart-1, chart-2, chart-3, chart-4, chart-5]
    source: CSS variables or existing theme tokens
  motion:
    duration_fast: 120ms
    duration_normal: 180ms
    duration_slow: 240ms
    easing_standard: ease-out
    easing_emphasized: cubic-bezier(0.16, 1, 0.3, 1)

layout:
  shell: app shell or page frame
  page_pattern: table-inspector
  regions:
    - id: sidebar
      width: 240
      responsive: collapses below tablet
    - id: statusbar
      height: 56
      responsive: remains visible, condenses secondary metadata
    - id: main
      width: fluid
      grid: 12 columns on desktop when useful
    - id: inspector
      width: 360
      responsive: drawer on mobile

components:
  approved_libraries: [existing project components, shadcn/ui new-york, Radix, Tailwind CSS 4, lucide-react, React Router 7, TanStack Query 5, TanStack Table 8, React Hook Form, Zod, sonner, Recharts, cmdk, motion, Playwright, MSW]
  repeated:
    - name: TaskCard
      source: existing component or new component
      states: [default, hover, selected, active, disabled, loading, error, empty]
      props: [title, status, progress]

interactive_controls:
  - id: run-filter-select
    primitive: Select or Combobox from approved component library
    purpose: filter runs by status
    states: [closed, open, hover, focus, selected, disabled, loading, empty]
    keyboard: [Tab focuses trigger, Enter or Space opens, Arrow keys move, Enter selects, Escape closes]
    data: status options from API or local enum
    acceptance: open menu is aligned, scrollable if long, selected value persists, no off-token styling
  - id: artifact-preview
    primitive: Dialog or Sheet with image viewer
    purpose: preview clicked image artifact
    states: [closed, open, loading, loaded, error]
    keyboard: [Enter opens from thumbnail, Escape closes, Tab traps focus, Arrow keys navigate when gallery exists]
    acceptance: image preserves aspect ratio, supports zoom or open-original action when useful, background scroll is locked

blacklist:
  - broad blue-purple gradients
  - glassmorphism cards
  - excessive shadows
  - random emoji as icons
  - card-heavy layouts without real data density
  - icon on every module without semantic need
  - oversized hero sections for product tools
  - landing-page style composition for dashboards
  - meaningless metric cards
  - all-centered layouts for operational tools
  - more than five competing semantic colors

acceptance:
  - Screenshot matches target structure, density, and spacing at fixed viewports.
  - No text overlap or layout shift during loading, empty, or error states.
  - Motion is subtle, supports reduced motion, and never changes the intended layout structure.
  - Implementation uses only approved tokens and component families.
  - Page follows the selected pattern and exposes a clear recommended next action.
  - Every visible interactive control is implemented, keyboard reachable, styled through the same component system, and covered by a story or Playwright interaction check when practical.
```

## Implementation Rules

- Reuse the project's existing component library and design tokens before adding new primitives.
- For React UI, default to Tailwind CSS 4 utilities, semantic tokens, and component recipes. Do not add page-specific naked CSS selectors for new work.
- Do not invent new colors, spacing scales, radius values, or typography unless the UI Spec requires it.
- Do not start by generating a polished full page when the layout or information architecture is unsettled; start with a wireframe.
- Do not replace the visual style with a different product aesthetic.
- Do not create marketing-style hero sections, decorative split layouts, or oversized cards for internal tools and agent consoles.
- Do not hardcode hex colors in business components; add or reuse semantic tokens instead.
- Do not add untyped JavaScript for frontend app code; use TypeScript.
- Do not introduce axios; use the project's typed `fetch` API client.
- Do not use hand-written SVG icons when lucide-react has an appropriate icon.
- Do not use broad gradients, glassmorphism, random shadows, random colors, emoji icons, or decorative illustrations unless the UI Spec explicitly allows them.
- Do not use complex absolute positioning for normal layout unless the UI Spec explicitly requires it.
- Do not hand-roll dropdowns, modals, tables, or focus management when the project already has a reliable component or library.
- Use icons for tool/action buttons when a known icon exists; add tooltips for icon-only controls.
- Keep cards for repeated items, modals, and genuinely framed tools. Do not nest cards inside cards.
- Prefer table, list, inspector, queue, timeline, and diagnostics layouts for engineering tools instead of generic stat-card dashboards.
- Ensure loading, empty, error, disabled, hover, focus, selected, and active states are specified and implemented where relevant.
- Ensure text fits inside controls and panels across target viewports.
- Do not leave static-looking controls without behavior. A dropdown must open, a button must perform or expose its pending behavior, a clickable image must preview or navigate as specified, and a menu item must have a defined action or disabled state.

## Interactive Control System

Before implementing or accepting a page, create a control inventory. Include every:

- button, icon button, segmented control, toggle, checkbox, radio, switch
- select, combobox, dropdown menu, context menu, command menu
- dialog, alert dialog, sheet/drawer, popover, hover card, tooltip
- tabs, accordion, disclosure, collapsible panel
- table filter, sort header, pagination, row action, bulk action
- image thumbnail, gallery, lightbox, preview modal, file attachment
- toast, banner, inline alert, confirmation, destructive action
- date/time picker, numeric input, search input, autocomplete

Default primitive choices for React product UIs:

| Control | Default Primitive | Required Behavior |
| --- | --- | --- |
| Simple option select | shadcn/ui or Radix Select | open/close, keyboard selection, disabled/loading/empty |
| Searchable select | Combobox with Popover + Command | typeahead, no results, async loading if remote |
| Action menu | DropdownMenu | trigger, aligned menu, keyboard navigation, disabled dangerous actions |
| Contextual detail | Popover or HoverCard | anchored positioning, outside click close, focus behavior |
| Blocking decision | AlertDialog | focus trap, Escape behavior, destructive action styling |
| Rich modal task | Dialog | title/description, focus trap, scroll body, footer actions |
| Mobile inspector | Sheet or Drawer | responsive substitution, scroll lock, close affordance |
| Image preview | Dialog/Sheet lightbox | aspect ratio, loading/error, keyboard close, optional zoom/open original |
| Feedback | Toast or inline Alert | semantic status, dismiss policy, no secret leakage |
| Data table controls | TanStack Table + design-system controls | sorting, filtering, pagination, row selection, dense data state |
| Global search | Command dialog with `cmdk` | Cmd/Ctrl+K shortcut, search, grouped results, no results, keyboard navigation |
| Charts | Recharts + semantic chart tokens | accessible labels, responsive container, stable colors, empty/error states |

Unified interaction rules:

- All overlays must use the same radius, border, shadow, background, foreground, z-index scale, and animation timing.
- All overlays must define outside click, Escape, focus trap or focus return, scroll lock, portal/container strategy, and mobile behavior.
- Icon-only controls need accessible labels and tooltip when the action is not obvious.
- Disabled controls need a reason through tooltip, inline helper, or adjacent status when the reason is not obvious.
- Loading controls must prevent duplicate destructive actions and communicate progress.
- Destructive controls require confirmation when the action is irreversible, costly, or security-sensitive.
- Image and artifact previews must avoid layout shift, preserve aspect ratio, handle load failure, and avoid exposing raw filesystem paths unless the product intentionally shows them.
- Tables must keep header, filters, row hover, selected row, empty state, and pagination visually consistent.
- Forms must use consistent label, description, error, required, disabled, dirty, saving, and saved states.
- Responsive behavior must specify whether inspectors become sheets, tables become card lists, and menus collapse into command or overflow actions.

Interaction implementation is incomplete until the main happy path and at least one failure/empty/disabled path are represented in code or tests.

## Reference Image Rules

When a screenshot, GPT Image output, Figma frame, Stitch output, or visual mock is provided:

- Pair the image with written token, component, layout, and acceptance rules before implementation.
- Prefer structured design data when available, such as Figma Dev Mode, MCP-provided measurements, design tokens, or existing CSS variables.
- Extract uncertain image values as estimates, not facts.
- Reject visual details from the image if they conflict with the project design system.
- Keep reference images for direction and composition; keep code faithful to tokens, components, and measurable spec.

## React Animation Policy

Default React animation stack:

```bash
bun add motion @formkit/auto-animate
```

Add Radix primitives only when the owning app needs them and they are not already installed:

```bash
bun add @radix-ui/react-dialog @radix-ui/react-popover
```

Use this selection rule:

| Scenario | Default choice |
| --- | --- |
| Page transitions, cards, tabs, drawers, modal panels, hover/tap micro-interactions | `motion` with `motion/react` |
| List, table row, task card, grid item add/remove/filter/reorder | `@formkit/auto-animate` |
| shadcn/ui or Radix Dialog, Popover, Dropdown, Tooltip, Accordion, Tabs | Radix `data-state` plus Tailwind/CSS animation |
| Complex marketing scroll animation, SVG timeline, hero animation | GSAP only when explicitly required |
| Physics, elastic gestures, 3D or react-three-fiber motion | React Spring only when explicitly required |
| Empty-state illustration, loading illustration, success/failure animation asset | Lottie only when an actual animation asset exists |
| Legacy CSS enter/exit lifecycle | React Transition Group only for existing projects already using it |

Animation rules:

- Default duration range is 120ms to 240ms.
- Use `ease-out` for standard UI motion and `cubic-bezier(0.16, 1, 0.3, 1)` for emphasized but still calm transitions.
- Do not use large movement, strong bounce, rotation, particles, glow effects, or decorative animation in dashboards, admin screens, engineering tools, or terminal-like web UIs.
- Do not change layout structure to create animation.
- Do not use complex absolute positioning for normal UI motion.
- Animation should explain state change: enter, exit, expand, collapse, reorder, select, hover, loading, success, or failure.
- If the UI Spec does not define animation, add only light fade or slide where it clarifies state change.
- Always support `prefers-reduced-motion`. With Motion, use reduced-motion APIs or disable nonessential transforms. With CSS, use media queries or project utilities.
- Verify animation does not create layout shift, text overlap, scroll jumps, or screenshot instability.

## React Dependency Rules

- Inspect the owning app's `package.json` before adding dependencies.
- Do not install duplicate animation libraries that overlap with an existing project standard.
- Prefer `motion` over older Framer Motion package usage for new React code when the project has no existing standard.
- Prefer CSS/Radix `data-state` animation for primitive open/close behavior over wrapping every primitive in Motion.
- Add GSAP, React Spring, Lottie, or React Transition Group only when the UI Spec names the scenario and the existing project does not already solve it.

## Visual Review Rules

Reviewer output should be a fix list, not taste commentary.

Each issue should include:

- location or component
- observed current behavior
- expected behavior from the target or UI Spec
- likely code area to change
- severity: blocker, high, medium, low

Review dimensions:

- Layout: main/secondary hierarchy, density, alignment, scan path, key action visibility.
- Visual system: token use, semantic color count, typography scale, radius, borders, shadows, icons.
- Product: page question answered, recommended next action, empty/error/loading states, recovery path.
- Engineering: component reuse, magic numbers, responsive rules, testability, accessibility hooks.

Prefer measurable observations:

- sidebar is about 40px too narrow
- header appears 16px taller than spec
- table row height is 52px but spec says 44px
- card radius is 6px but token says 8px
- dialog animation moves 36px but spec only allows subtle 8px entry

## Related Skills

Use this skill as the React/frontend workflow constraint. Pair it with:

- `frontend-design` and `web-design-guidelines` when implementing web UI in a subproject that has them in its profile.
- External `baseline-ui` for AI UI slop baseline checks when available.
- External `extract-design-system` when the task is to extract starter tokens from a public website.
- External `tailwind-design-system` when the owning app uses Tailwind CSS v4 or is explicitly creating a v4 token system.
- `plan-design-review` before implementation when the UI plan or product design needs critique.
- `design-review`, `qa`, or `qa-only` after implementation when the user wants visual QA or screenshot-based bug finding.
- `performance-profiler` if animation, rendering, large tables, or route transitions become slow.
- `tui-design-standards` instead of this skill for terminal UI.

## Validation

Run the narrowest available checks for the owning project:

- type check or build
- relevant unit/component tests
- Playwright screenshot or visual test command
- Storybook story coverage for touched reusable components or pages when Storybook exists
- animation smoke test for open/close, reorder/filter, hover/focus, and reduced-motion behavior when relevant
- manual smoke path for the changed route

If Playwright or visual tests do not exist, create the smallest useful screenshot path when the project already has Playwright. If adding test infrastructure would exceed the task scope, report the exact manual screenshot command or limitation.

## Boundaries

- Do not use this skill for terminal UI; use `tui-design-standards`.
- Do not use it for pure backend/API work with no user-facing screen.
- Do not create a large standalone design system unless the user asks for it or the project already has that direction.
- Do not put implementation code, app UI components, or screenshots inside this skill directory.
- Do not treat GSAP, React Spring, Lottie, or React Transition Group as default React dependencies.
