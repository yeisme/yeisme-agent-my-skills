# Scaena production Surface Map

Use this map to load only the task-specific source documents.

| Surface or task | Required source | Primary acceptance focus |
| --- | --- | --- |
| Shell, portfolio, navigation, project switcher, cockpit | `agent/scaena/docs/design/client-ui-spec.md` | Deep links, project isolation, density, responsive sidebars, recovery |
| State ownership, routing, API client, realtime | `agent/scaena/docs/design/frontend-architecture-contract-v1.md` | Query/view/draft separation, dependency direction, event reconciliation |
| Canonical production stages and recovery | `agent/scaena/docs/design/production-workflow-v1.md` | Stage semantics, blocking gates, human and agent actions |
| Subject candidates, freeze, binding, preflight | `agent/scaena/docs/protocols/subject-asset-workflow.md` | No generation before readiness, visible blockers and repair |
| Editorial assembly, media compare, rough cut, export | `agent/scaena/docs/design/editor-experience-expansion.md` | Non-destructive edits, versioning, partial failure, NLE handoff boundary |
| Agent dock, plan, approval, tool timeline | `agent/scaena/docs/design/agentic-client-experience.md` | Context refs, authority, approval, receipts, injection resistance |
| Visual and interaction validation | `agent/scaena/docs/qa/quality-and-evidence-strategy-v1.md` | State matrix, keyboard, Axe, Playwright, redacted evidence |
| Release or readiness decision | `agent/scaena/docs/qa/validation-plan.md` | Critical paths, maturity labels, verification commands |

## Surface Questions

Answer these before implementation:

1. What production decision does the user make here?
2. Which object is selected, and where is its inspector?
3. What blocks the next action, and how can the user repair it?
4. Which state is canonical server data, local view state, or an editable draft?
5. Which actions require confirmation, expected version, permission, budget, or human review?
6. How does the surface recover after stale state, disconnect, partial failure, or rejected review?
7. What evidence proves keyboard, responsive, interaction, and visual behavior?

## Minimum State Coverage

Select all relevant states rather than forcing every surface to render every state:

```text
loading empty partial blocked running review ready
stale offline forbidden error cancelled superseded
```

For media and editor surfaces, also cover missing source, unsupported preview, compare sync failure, dirty draft, autosave failure, version conflict, partial export, and retry.
