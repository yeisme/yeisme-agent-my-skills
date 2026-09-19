---
name: ui-spec-frontend-workflow
description: Use when turning product ideas, PRDs, wireframes, screenshots, high-fidelity UI images, or Open Design handoffs into React/web frontend implementation or visual fixes; enforce Open Design first-use discovery, single design direction selection, the default SaaS operations console style, design-system assembly, UI Spec, page patterns, component tree, React animation rules, and screenshot regression before code is accepted.
---

# UI Spec Frontend Workflow

Use this skill when work touches React or web frontend screens and the source of truth includes an idea, PRD, wireframe, screenshot, design mock, GPT Image output, or visual diff.

This is a frontend development skill adapted for React product UIs. It is not a generic design-writing skill and not a terminal UI skill.

## Core Rule

Do not treat an image as the only source of truth, and do not let AI freely invent a visual system.

AI-generated frontend should be assembled inside an explicit design system: product type and style posture, semantic design tokens, approved component library, page pattern, layout dimensions and responsive rules, visual blacklist, component states, interactive control inventory, motion policy, and visual acceptance evidence.

Frontend implementation must be driven by product scenario or PRD, information architecture and user path, design tokens, approved page pattern, component tree, interactive control contracts, layout dimensions and responsive rules, component states, motion tokens and animation policy, and screenshot regression evidence.

If a reference image and UI Spec conflict, follow the UI Spec and call out the conflict.

If Open Design is available, use it as the first discovery and handoff tool before inventing a local visual direction. Open Design does not replace the owning project's implementation checks or acceptance evidence.

## Design Stack Selection

Use one clear design direction layer for non-trivial UI work. Do not stack Taste, Anthropic frontend-design, UI UX Pro Max, Impeccable, and local Yeisme rules as equal authorities.

Default order:

1. Run Open Design discovery when the official CLI is available. First inspect the resolved command so an HTTP compatibility wrapper or GNU coreutils `od` is not mistaken for the native Open Design CLI:

```bash
command -v od
od --help | sed -n '1,40p'
```

If help identifies `Open Design CLI wrapper`, GNU coreutils, or another compatibility launcher, report that the native CLI is unavailable. Use an explicit HTTP/API fallback only for supported read or compatibility operations; do not present it as native CLI execution.

For the official CLI, run:

```bash
od status --json
od skills list
od design-systems list
od projects list
```

Use Open Design for reference collection, design-system selection, Studio exploration, image/prototype generation, and handoff artifacts. Treat its output as design input that must still be translated into the owning app's tokens, components, tests, and evidence.

Use `od mcp` only where the official daemon CLI files are installed or mounted. Require an explicit native executable and arguments for bridges or automation; never default MCP startup to an ambiguous command name.

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

1. Locate the owning subproject. Read the nearest `AGENTS.md`, UI docs, tokens, component library, routes, and screenshot conventions. Identify whether the task is exploration, UI Spec authoring, implementation, visual review, or fix-after-review.
2. If a UI Spec does not exist, draft it from the PRD and reference image before code. Mark uncertain image-derived values. Freeze the design system: product type, style posture, spacing, radius, semantic colors, typography, components, icons, motion, and blacklist. Default posture: `references/saas-console-posture.md`.
3. Select a page pattern from `references/page-patterns.md`. Do not ask for a generic "nice dashboard" when a list/detail, table/inspector, queue, timeline, diagnostics, or settings pattern fits. Wireframe first when layout or hierarchy is unsettled (neutral blocks only).
4. Write a component tree (shell, regions, repeated components, state surfaces, responsive substitutions, controls) and the interaction contract before implementation. Control inventory: `references/interactive-controls.md`. YAML template: `references/ui-spec-template.md`.
5. Implement with the existing frontend stack. Prefer mature systems already in the project (shadcn/ui, Radix, Tailwind, lucide, TanStack Table/Query). Polish only after structure, tokens, and interaction are correct; polish must not change information architecture.
6. Apply the React animation policy in `references/react-animation.md`. Do not add Motion or AutoAnimate by default; CSS/Radix first; UI Spec exception required for a new runtime dependency. Run `yeisme-ui-motion-quality` after implementation.
7. Capture Playwright (or equivalent) screenshots at fixed desktop and mobile viewports, including open states for dropdowns, dialogs, popovers, sheets, and image preview when touched.
8. Compare screenshots against the target or UI Spec. Report executable fixes (layout, spacing, hierarchy, density, color, typography, states, animation, interaction, responsive). Patch and re-run the narrowest checks until issues are resolved or a blocker is explicit.
9. Split non-trivial generation into three named stages: wireframe (grayscale layout only) → design-system pass (approved tokens/components, no new style families) → polish (spacing, states, responsive; do not change layout intent). For high-risk UI, use a separate review pass before polish is accepted.
10. Review with `references/visual-review.md`: a measurable fix list, not taste commentary.

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

## Reference Image Rules

When a screenshot, GPT Image output, Figma frame, Stitch output, or visual mock is provided:

- Pair the image with written token, component, layout, and acceptance rules before implementation.
- Prefer structured design data when available, such as Figma Dev Mode, MCP-provided measurements, design tokens, or existing CSS variables.
- Extract uncertain image values as estimates, not facts.
- Reject visual details from the image if they conflict with the project design system.
- Keep reference images for direction and composition; keep code faithful to tokens, components, and measurable spec.

## Related Skills

Use this skill as the React/frontend workflow constraint. Pair it with:

- `frontend-design` and `web-design-guidelines` when implementing web UI in a subproject that has them in its profile.
- `yeisme-ui-motion-quality` for the focused enter/exit, overlay, list, reduced-motion, and animation-performance review after implementation.
- `vercel-react-best-practices` when React rendering, rerenders, bundle size, long lists, or animation performance have measurable evidence.
- `vercel-composition-patterns` when shared components need compound APIs, context boundaries, or boolean-prop reduction.
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

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Image used as the only spec | Draft a UI Spec first | Image vs spec conflict: follow the UI Spec |
| Multiple taste authorities stacked | One direction layer | Impeccable is a gate after implementation |
| Hero/gradient on an ops console | Default SaaS operations posture | No marketing layout for admin |
| Naked CSS / hex in components | Tailwind utilities + semantic tokens | Global CSS only for tokens/reset |
| Control looks clickable but does nothing | Control inventory + keyboard/open/close | Stories or Playwright for open/empty/error |
| New animation library by default | CSS/Radix first | Motion exception must be in the UI Spec |
