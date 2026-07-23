---
name: orbital-studio-experience
description: Use when designing, implementing, or reviewing Auctra Studio, Scaena production, or Yeisme Workbench creative workspaces that need the Orbital Studio System, bounded Pane layouts, data workspaces, context actions, Agent collaboration, responsive behavior, accessibility, or visual blacklist enforcement without moving canonical domain authority into the client.
---

# Orbital Studio Experience

Apply one shared interaction grammar while preserving three distinct products:

- `Editorial Orbit`: Auctra Studio manuscript, Story World, Scene Matrix, and proposal/review comparison.
- `Production Orbit`: Scaena production ProductionGraph, shot/asset workspaces, preview, review, and delivery gates.
- `Operations Orbit`: Yeisme Workbench owner health, Task, Operation, Receipt, Evidence, and safe deep links.

## Inputs

Read the owning product PRD/OpenSpec, public client contract, capability manifest, projection schemas, action descriptors, state/error matrix, and existing design tokens. Identify the canonical owner before proposing UI or code.

## Boundaries

- Keep canonical screenplay, ProductionGraph, asset/job state, review authority, credentials, private paths, and provider payloads in their owners.
- Consume only versioned projections, safe refs, allowed actions, receipts, evidence refs, and approved deep-link descriptors.
- Never let drag, Agent output, optimistic UI, or client state directly accept canonical content or production state.
- Never choose an Agent/model, dispatch work, widen permissions, or replace the owning implementation workflow.
- Keep missing contracts visible as `needs_contract`, `unavailable`, `permission_required`, `stale`, or another truthful stable state.

## Workflow

1. **Select one variant.** Choose Editorial, Production, or Operations Orbit from the user job and canonical owner. Do not blend all three into one generic dashboard.
2. **State the page question.** Define what the user must decide or repair on each page before choosing layout or components.
3. **Map contracts.** For every chart, board, table, graph, Pane, action, Agent entry, and deep link, name the owner projection/action, version, freshness, permission, expected version, receipt, evidence, and recovery path.
4. **Design the Pane system.** Use a versioned `PaneLayoutV1`, registered Pane kinds, maximum split depth 2, default maximum 3 visible Panes, hard maximum 4, bounded drop zones, and safe object refs. Keep project-shared layouts in the owner `SavedViewV1` service.
5. **Separate drag domains.** Let Pane/Tab drag change layout only. Convert object drag into typed `DragIntentV1`, then re-run owner capability, permission, version, cost, confirmation, and idempotency gates.
6. **Unify context actions.** Make Context Menu, `Shift+F10`, selection toolbar, Inspector, Command Palette, and keyboard move mode resolve the same action descriptor and disabled reason.
7. **Constrain Agent collaboration.** Start Agents from an object, selection, finding, board card, table row, or chart anomaly. Return only assignment, event, finding, question, proposal, or artifact refs. Route adoption through owner review.
8. **Cover recovery states.** Specify loading, empty, offline, stale, permission, cost, partial, conflict, unknown accept, contract mismatch, cursor expiry, and owner outage states. Preserve safe local layout and completed receipts during failures.
9. **Design responsive reductions.** At desktop, allow navigation + Canvas + Inspector. At tablet, move Inspector to a Sheet and reduce simultaneous Panes. On mobile, keep browse, review, approval, and lightweight actions; do not shrink a dense desktop workspace proportionally.
10. **Verify accessibility and performance.** Provide keyboard/menu equivalents for every drag action, focus restoration, accessible drop announcements, reduced motion, semantic tables/boards, bounded virtualization, and dependency canaries for Dockview/dnd-kit coexistence.

## Visual Contract

Use smoked shell surfaces, restrained borders, clear object breadcrumbs, one main Canvas, contextual Inspector, Problems & Evidence, and low-noise status color. Operations Orbit uses flatter dense surfaces; glass is limited to shell, overlays, and focus context.

Reject:

- marketing Hero sections inside workspaces;
- provider or internal service names as primary navigation;
- decorative KPI card grids, fake percentages, unexplained gradients, or Chat-first home pages;
- whole-page card nesting, oversized pills, excessive blur, or motion without state meaning;
- fake realtime, static success toasts, or optimistic canonical acceptance.

## Output

Produce the narrowest artifact requested: UI spec, page/state matrix, Pane Registry, `PaneLayoutV1` proposal, Context Action matrix, Agent interaction contract, responsive plan, accessibility checklist, implementation handoff, or review findings. Human-authored project artifacts default to Chinese; stable schema fields, action IDs, commands, flags, and code stay English.

## Validation

Run the owning subproject's declared contract, component, integration/E2E, accessibility, typecheck, lint, build, and screenshot checks. Require per-run evidence under `temp/integration-test-runs/<run-id>/` for integration or higher layers. Confirm:

- no browser owner credential or private state;
- no direct cross-owner mutation fallback;
- every action has permission/version/idempotency/recovery semantics;
- every drag action has keyboard/menu parity;
- unknown/partial/offline states remain truthful;
- Editorial, Production, and Operations inputs produce visibly different workspaces while preserving the same safety grammar.
