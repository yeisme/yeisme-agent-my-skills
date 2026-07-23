---
name: scaena-production-ui-workflow
description: Use when designing, implementing, or reviewing Scaena production browser UI, including the production cockpit, canonical stage workspaces, subject readiness, shot and media inspection, review, editorial assembly, export, agent surfaces, responsive behavior, and UI evidence.
---

# Scaena production UI Workflow

Treat this skill as the Scaena domain constraint for frontend work. Pair it with one design-direction layer selected by `yeisme-frontend-design-router`, use `ui-spec-frontend-workflow` for implementation planning, and finish with `yeisme-frontend-quality-workflow`.

## Read The Local Contract

Before changing UI, read:

- `agent/scaena/AGENTS.md` and `agent/scaena/app/AGENTS.md`.
- `agent/scaena/docs/design/client-ui-spec.md` for shell, components, interactions, tokens, responsive rules, and approved visual direction.
- `agent/scaena/docs/design/frontend-architecture-contract-v1.md` for state ownership and dependency boundaries.
- The task-specific document selected from `references/studio-surface-map.md`.

Do not reconstruct these contracts from screenshots or fixtures when the source document exists.

## Workflow

1. Classify the surface and identify its canonical production stage, user decision, primary object, and recovery path.
2. Separate server projections, local view state, editable drafts, and command receipts before choosing components.
3. Define loading, empty, partial, blocked, running, review, ready, stale, offline, forbidden, and error behavior relevant to the surface.
4. Design the information hierarchy before styling: context, work table or canvas, selection, inspector, next action, blockers, and evidence.
5. Reuse shadcn/ui primitives and existing Studio components; keep Feature → Studio → Base dependency direction.
6. Implement keyboard, focus, resize, deep-link, URL persistence, and responsive behavior together with the default state.
7. Add deterministic component and browser evidence for open, loading, empty, error, blocked, mobile, keyboard, and reduced-motion states.

## Domain Invariants

- Preserve the canonical stages: `prepare`, `text`, `subjects`, `shots`, `visual`, `review`, `export`.
- Keep `subjects` as a hard gate. Never expose an executable production-generation CTA before source, candidate comparison, human freeze, exact binding, and preflight readiness pass.
- Access production capabilities only through the Studio Backend public API and SSE projection. Never call owner CLIs, owner databases, Eikona, or provider SDKs from the browser.
- Keep TanStack Query responsible for server state, Zustand responsible for view state, and feature-local models responsible for drafts.
- Route mutations through typed commands with permission, idempotency, expected version, confirmation when required, and visible receipts.
- Treat evidence, provenance, permission, rights, budget, continuity, and repair guidance as first-class UI data.
- Keep generated or imported media pending until the relevant human review gate accepts it.

## Visual Posture

Use the local design system as the authority. Prefer a neutral modern production workstation: dense but legible, cinematic without decorative film clichés, low-saturation accents, explicit status semantics, compact metadata, and stable spatial relationships between list, preview, inspector, and action areas.

Avoid generic card dashboards, oversized marketing typography, neon cyberpunk styling, gratuitous gradients, excessive glass effects, detached floating controls, and status conveyed by color alone.

Do not pixel-copy generated reference images. Reuse their information hierarchy, density, state expression, and interaction zoning while preserving accessibility and architecture contracts.

## Required Output

For design work, return:

- surface and user decision
- information hierarchy and component tree
- state and permission matrix
- desktop, tablet, and mobile behavior
- keyboard and accessibility behavior
- command, receipt, evidence, and repair flow
- component, browser, and visual verification plan

For implementation work, include the changed paths and run the project commands that match the scope:

```bash
cd agent/scaena/app
bun run typecheck
bun run lint
bun run test
bun run build
bun run test:e2e
```

Use `bun run quality:local` for the local deterministic gate. Browser and integration runs must preserve redacted evidence under `agent/scaena/temp/integration-test-runs/<run-id>/`.

## Boundaries

- Do not freeze page composition into backend domain contracts.
- Do not duplicate ProductionGraph, authorization, lifecycle transitions, review acceptance, or idempotency logic in React.
- Do not introduce a new component library, state library, styling system, test runner, or canvas engine without an owning OpenSpec design.
- Do not use Taste-style marketing direction as the default authority for dense production workspaces.
- Do not claim a real production loop when the UI is fixture-only or backend gates are incomplete.
