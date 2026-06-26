---
name: yeisme-frontend-design-router
description: Use when routing frontend design, UI generation, redesign, screenshot-to-code, Open Design, Taste Skill, Impeccable, browser visual QA, component sourcing, or canvas UI tasks to the smallest appropriate frontend design and quality skills without assuming installation state.
---

# Yeisme Frontend Design Router

Use this skill when a user asks for frontend UI design, page generation, redesign, visual QA, screenshot/Figma implementation, Open Design integration, Taste/Impeccable selection, or frontend design skill routing.

This is a routing skill only. It chooses the next skill/tool chain. It does not implement UI, install dependencies, write product specs, or perform visual QA by itself.

## Core Rule

Route to the smallest effective chain:

```text
Open Design -> one aesthetic direction layer -> implementation workflow -> deterministic quality gate -> browser visual loop
```

Assume the user's agent may have every relevant skill or tool. If a named skill or tool is unavailable, do not stop for installation instructions. Tell the active agent to discover the closest equivalent skill/tool and continue with the same role in the chain.

Do not load multiple aesthetic authorities as equals. Taste Skill, Anthropic frontend-design, UI UX Pro Max, local design-system rules, and Impeccable overlap heavily. Choose one aesthetic direction layer, then use quality gates after implementation.

## Inputs

Accept:

- product idea, PRD, route, wireframe, screenshot, Figma frame, reference site, or Open Design handoff
- request type: new UI, redesign, visual QA, screenshot-to-code, component sourcing, dashboard, landing page, canvas editor, browser diagnosis
- existing project stack and local design system when known
- user preference such as "use Open Design first" or "only route, do not implement"

## Outputs

Return only routing guidance unless the user explicitly asks to execute:

```text
Route:
Open Design -> <aesthetic skill> -> <implementation skill> -> <quality gate> -> <browser loop>

Reason:
<one concise sentence>

Do not load:
<conflicting or unsuitable skills/tools>

Fallback:
If unavailable, the active agent should discover the closest equivalent skill/tool and continue.
```

If the next action is obvious and execution is requested, hand off to the first routed skill/tool. Do not write a long comparison unless the user asks for rationale.

## Default Routes

| Scenario | Route |
| --- | --- |
| General frontend page or product UI | Open Design -> `ui-spec-frontend-workflow` -> local implementation skill -> `yeisme-frontend-quality-workflow` |
| Landing page, brand site, portfolio, marketing page | Open Design -> Taste Skill or `design-taste-frontend` -> implementation skill -> Impeccable-style quality gate |
| Dashboard, SaaS admin, operations console, dense table UI | Open Design -> `ui-spec-frontend-workflow` -> local React/product UI skill -> `yeisme-frontend-quality-workflow` |
| Existing page redesign | Open Design current-state capture -> one aesthetic direction skill -> implementation skill -> visual QA |
| Screenshot, Figma, mockup, or reference implementation | Open Design or screenshot-to-code -> `ui-spec-frontend-workflow` -> implementation skill -> Playwright screenshot comparison |
| Design direction, IA, style, or UI Spec only | Open Design -> UI UX Pro Max or frontend-design -> UI Spec output only |
| Frontend quality audit | `yeisme-frontend-quality-workflow` -> Impeccable detect when available -> Playwright/Storybook/Axe/Lighthouse |
| Browser visual diagnosis | Stagewise, Onlook, browser-use, or design-review -> source fix -> deterministic quality gate |
| Component sourcing | 21st.dev Magic, shadcn registry, OpenUI, or existing component library -> local design-system constraints -> implementation skill |
| Agent workflow, Dify/n8n-like graph, DAG editor, routing canvas | Open Design -> `@xyflow/react` route -> `ui-spec-frontend-workflow` -> implementation skill -> interaction tests |
| Whiteboard, moodboard, free-form material board | Open Design -> `tldraw` route -> UI Spec -> implementation skill -> interaction tests |

## Aesthetic Direction Selection

Choose exactly one:

| UI Type | Preferred Direction Layer |
| --- | --- |
| Marketing, brand, portfolio, campaign, creative page | Taste Skill or `design-taste-frontend` |
| Product admin, dashboard, operations console, agent console, form flow | project design system, Anthropic `frontend-design`, or Yeisme SaaS operations console posture |
| Broad design knowledge retrieval across sectors or styles | UI UX Pro Max as a candidate database, then select one direction |
| Existing project with a mature local design system | local design system first |

Do not use Taste as the default authority for dense product UI, dashboards, complex tables, settings, admin consoles, or multi-step product flows.

Do not use Impeccable as the only taste source. Use it primarily after implementation for deterministic detection, audit, hardening, and polish.

## Open Design First-Use Check

When Open Design is available, route through it first for discovery and handoff:

```bash
od status --json
od skills list
od design-systems list
```

Use Open Design for:

- reference collection
- design system discovery
- Studio exploration
- prototype/image/presentation/video handoff
- `DESIGN.md` or design-system context
- routing to coding agents

Open Design output is input, not final acceptance. Final frontend acceptance still belongs to the owning project through implementation tests, screenshots, accessibility checks, and quality gates.

## Quality Gate Selection

After implementation, route to deterministic checks before subjective polish:

```bash
npx impeccable detect src/
npx impeccable detect --json .
npx impeccable detect https://example.com
```

Use Impeccable-style gates when Impeccable itself is not available:

- typecheck, lint, and build
- Storybook or component state stories
- Playwright screenshots and interaction tests
- Axe and keyboard navigation checks
- Lighthouse where relevant
- console error and failed network request capture
- source scan for hardcoded colors, naked CSS selectors, fake controls, overflow, missing states, and admin-console posture violations

Do not require a Node.js upgrade only to run Impeccable. If the current project cannot run it, route to the closest local deterministic checks.

## Browser Loop Selection

Use browser tools as diagnosis and comparison aids:

| Tool Class | Route Purpose |
| --- | --- |
| Open Design Studio | design exploration, prototype preview, artifact handoff |
| Stagewise | browser-in-agent visual inspection and live adjustment |
| Onlook | Next.js/Tailwind visual source editing when applicable |
| browser-use | exploratory smoke flows and dynamic browser checks |
| design-review / qa | structured visual QA and source fixes |

Browser loop success is not final acceptance unless it produces reproducible evidence through Playwright, Storybook, Chromatic, Axe, Lighthouse, or local project tests.

## Canvas UI Routing

Choose the canvas substrate before UI design:

- `@xyflow/react`: workflow canvases, DAG editors, node graphs, Dify/n8n-like builders, agent route editors, inspector-driven node configuration.
- `tldraw`: free-form whiteboards, moodboards, reference boards, annotation, material arrangement, visual thinking.
- X6 or heavier graph libraries: complex enterprise diagramming that React Flow cannot express.

For React Flow routes, keep frontend and backend ownership separate: React Flow owns interaction and visualization; backend services own DAG validation, execution semantics, persistence, audit, scheduling, and permissions.

## Conflict Rules

- If the user asks for a landing page but also says dashboard, route by primary user job. Marketing acquisition goes to Taste; repeated operational work goes to product UI rules.
- If the user asks for all tools, decline to stack them as equal authorities. Pick one aesthetic layer and keep the rest as references or gates.
- If a screenshot conflicts with the project design system, route to `ui-spec-frontend-workflow` to resolve the written UI Spec before implementation.
- If a component generator produces off-system visuals, treat it as source material and restyle through local tokens/components.
- If browser tools find issues but no deterministic test exists, create or request the narrowest reproducible Playwright/Storybook/manual evidence path.

## Fallback Contract

When a routed skill/tool is unavailable, output:

```text
Fallback:
The active agent should discover the nearest equivalent skill or tool for the same role and continue. Preserve the route roles: discovery, aesthetic direction, implementation, quality gate, browser loop.
```

Do not tell the user to install every possible skill. Do not block routing on inventory uncertainty.

## Boundaries

- Do not implement frontend code inside this skill.
- Do not write long product design plans unless routed to a planning skill.
- Do not perform QA directly; route to quality or visual QA skills.
- Do not create or modify Open Design projects directly; route to Open Design or the relevant operator.
- Do not add this skill to root runtime by default unless the user explicitly asks for a long-lived root default. Frontend execution skills should remain on-demand or subproject-scoped.
- Do not expose local execution wrappers, shell aliases, or agent-only prefixes in routing output.

## Validation

For this routing skill, validation means the route is minimal, non-conflicting, and actionable:

- exactly one aesthetic direction layer is selected
- Open Design is first when available and relevant
- implementation and quality gates are separated
- browser loop is used for evidence, not as sole acceptance
- unavailable skills/tools fall back to discovery rather than blocking
- output includes Route, Reason, Do not load, and Fallback
