---
name: eikona-mcp-actions
description: "Use when an agent operates the Eikona MCP beyond ordinary image generation: routing an intent to the right eikona.execute action, checking consumer/operator lane entitlement, batching, review and feedback, visual library, assets, workflows, delivery, comparison, dataset, or evidence writeback actions, or recovering from typed Eikona action errors. For plain image generate/edit delivery use eikona-mcp-image first."
---

# Eikona MCP action routing

The Eikona MCP tool surface is intentionally compact: `eikona.search` (read-only
card retrieval) and `eikona.execute` (one allowlisted `action` + `args` per
call). This skill routes an intent to the right action in the fewest calls.
Ordinary image generation and editing
stay in `eikona-mcp-image`; everything else starts here.

## Current map and drift

Use the bundled v0.7.6 action map (77 actions) for ordinary routing. Do not
fetch a full catalog or generate a card at session start. Refresh the map only
after an actual installed-version mismatch or a typed action denial that needs
diagnosis:

1. Local released `eikona` CLI present → run `eikona mcp capabilities --json
   --full` on demand.
2. Service endpoint known → read `GET <service-origin>/api/v1/mcp/actions`
   only to resolve that demonstrated drift.
3. Otherwise, stop on the typed denial; do not enumerate guesses.

Do not depend on a bundled helper script: released Skill bundles intentionally
contain only the installed Skill content.

Never guess or pluralize an action name. `DeniedActionError` is returned
identically for unknown and non-entitled actions (existence-oracle
protection); on denial, stop and reassess the lane, do not probe action names.

## Navigation map (by intent domain)

Lane markers: `op` = operator lane (owner/operator principal only; remote
consumer tokens never see them). Unmarked = consumer lane.

| Intent domain | Actions |
| --- | --- |
| Generation loop | `generate`, `edit`, `run.batch`, `wait`, `status`, `inspect`, `cancel`, `retry`, `repair`, `resume`, `reroll`, `trace.tail`, `report` |
| Review & feedback | `review.packet`, `review.contact_sheet`, `feedback.accept`, `feedback.reject`, `feedback.needs-edit`, `feedback.reference-only`, `analyze` |
| Assets & delivery of accepted work | `assets.handoff`, `assets.stage`, `assets.apply`, `artifact.access` (op), `replace.preview`, `replace.apply`, `rollback`, `export` |
| Visual library & style | `library.search`, `library.list`, `library.show`, `library.save`, `library.tag`, `library.update`, `library.import-url`, `library.import-runs`, `style.build-from-image`, `deck.list`, `deck.show`, `recipes.list`, `recipes.show`, `prompts.list` |
| Workflows | `workflow.plan`, `workflow.validate`, `workflow.run`, `workflow.pack.inspect`, `workflow.submit_scaena_request`, `preview.status` |
| Delivery pipeline | `delivery.create`, `delivery.status`, `delivery.capture`, `delivery.review`, `delivery.resume`, `delivery.cancel`, `delivery.outcome` |
| Comparison loop | `comparison.preflight`, `comparison.start`, `comparison.status`, `comparison.inspect`, `comparison.retry_failed` |
| Model catalog & diagnostics | `models.search`, `models.readiness`, `health` |
| Operator diagnostics & indexing | `config.inspect` (op), `providers.doctor` (op), `projects.list` (op), `index.status` (op), `worker.status` (op), `capsa.status` (op), `sync.status` (op) |
| Evidence writeback & datasets | `lifecycle.inspect` (op), `outcomes.record` (op), `reuse.record` (op), `repairs.record` (op), `dataset.build` (op), `dataset.export` (op), `bindings.confirm` |

Full per-action kind (readonly/generation/mutation) and safety columns live in
[references/action-map.md](references/action-map.md).

## Shortest sequences for common jobs

- **Accept and land an artifact**: `feedback.accept` → `assets.handoff` (for a
  downstream agent) or `assets.stage`/`assets.apply` (to land it). Read-only
  inspection first only when the typed response directs it.
- **Safe replacement**: `replace.preview` → human confirms → `replace.apply`;
  undo via `rollback`.
- **Queued workflows**: `workflow.validate` (cheap, no provider calls) →
  `workflow.run` → `preview.status`/`status` → `review.packet`.
- **Delivery**: `delivery.create` → `delivery.status` → `delivery.capture` →
  `delivery.review` → `delivery.outcome`; resume/cancel only on typed
  non-terminal states.
- **Comparison**: `comparison.preflight` → `comparison.start` →
  `comparison.status` → `comparison.inspect`; failed members via
  `comparison.retry_failed`.
- **Find reusable visuals**: `library.search` (not `eikona.search`) —
  `eikona.search` is the cross-type card index for docs/skills/samples, not
  the library itself.

## Error recovery rules

- Keep the idempotency key as submission evidence. If the transport outcome is
  lost before any `run_id` arrives, report unknown outcome and stop; never
  resubmit or claim the key reconciled the run.
- Consume the MCP `ResourceLink` immediately. On 404/expiry, call
  `artifact.access` once only when it is advertised for the active credentials
  and the caller is an authorized operator; send `confirm: true` and the
  completed run's canonical `artifact_uri`, then retry the new link once. If
  it is absent or denied, report that an operator grant or a compatible MCP
  host is required; do not retry or probe actions.
- Only run `models.search`, `providers.doctor` (op), or resource reads after a
  typed Eikona error says that exact information is needed.
- Mutations report `safety: mutates_local_state_or_requires_dry_run`; when a
  preview variant exists (`replace.preview`, `workflow.validate`,
  `comparison.preflight`), run it before the applying call.

## On-demand drift check

Run `eikona mcp capabilities --json --full` or read the scoped REST action
endpoint only after an actual version mismatch or typed denial. Neither is a
per-session preflight. Re-check after an Eikona upgrade only when the bundled
map no longer matches the installed action set.
