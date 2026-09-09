# Eikona MCP development action map

Navigation reference for 89 executable development `eikona.execute`
actions. This includes unreleased precision-edit and upload lifecycle actions;
an installed older release must not be assumed to expose them. It is verified
against `ActionDescriptors`; use it directly instead
of catalog discovery at session start. Refresh with `eikona mcp capabilities
--json --full` or the scoped REST action endpoint only after an actual
installed-version mismatch or typed denial requires diagnosis.

Columns: `kind` = readonly / generation / mutation (server-side dispatch
classification); `lane` = consumer / operator (remote consumer principals see
consumer actions only; unknown and non-entitled actions return the identical
`DeniedActionError`).

## Generation loop

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `generate` | generation | consumer | Submit a new image run (stable idempotency key) |
| `edit` | generation | consumer | Submit an edit run with a supplied reference image |
| `edit.prepare` | generation | consumer | Prepare an immutable region or mask edit; unparsed annotations return needs_analysis |
| `edit.plan.show` | readonly | consumer | Read an authorized edit plan summary and preview |
| `asset.upload.begin` | mutation | consumer | Create an authorized upload session for an input image |
| `asset.upload.complete` | mutation | consumer | Validate uploaded image bytes and return a durable asset URI |
| `asset.upload.status` | readonly | consumer | Inspect an existing upload session |
| `asset.upload.abort` | mutation | consumer | Abort an authorized upload session |
| `asset.upload.cleanup` | mutation | consumer | Clean up upload sessions through the upload lifecycle service |
| `run.batch` | generation | consumer | Submit a batch of runs in one call |
| `wait` | generation | consumer | Wait on a run until terminal |
| `status` | readonly | consumer | Read back run status |
| `inspect` | readonly | consumer | Inspect run evidence |
| `cancel` | generation | consumer | Cancel an active run |
| `retry` | generation | consumer | Retry a failed run |
| `repair` | generation | consumer | Repair a stuck run |
| `resume` | generation | consumer | Resume an interrupted run |
| `reroll` | generation | consumer | Request more candidates for a run |
| `trace.tail` | readonly | consumer | Tail run trace events |
| `report` | readonly | consumer | Run report projection |

## Review & feedback

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `review.packet` | readonly | consumer | Bounded review packet: candidates, warnings, actions |
| `review.contact_sheet` | mutation | consumer | Build a contact sheet for human review |
| `feedback.accept` | mutation | consumer | Record human acceptance of an artifact |
| `feedback.reject` | mutation | consumer | Record human rejection of an artifact |
| `feedback.needs-edit` | mutation | consumer | Record a needs-edit decision |
| `feedback.reference-only` | mutation | consumer | Record reference-only decision |
| `analyze` | readonly | consumer | Analysis readback for an image/asset |

## Assets & delivery of accepted work

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `assets.handoff` | readonly | consumer | Path-free handoff descriptor for downstream consumers |
| `assets.stage` | mutation | consumer | Stage an accepted asset to a local path |
| `assets.apply` | mutation | consumer | Apply an accepted asset into a project (confirmation-gated) |
| `assets.qualification.create` | mutation | operator | Record one unconfirmed asset-reuse qualification (confirm: true) |
| `assets.qualification.show` | readonly | operator | Read the qualification projection with acceptance and usability |
| `assets.qualification.validate` | readonly | operator | Re-derive qualification coverage from durable state |
| `assets.qualification.accept` | mutation | operator | Record the one human acceptance decision for a qualification |
| `assets.qualification.supersede` | mutation | operator | Mark one qualification superseded by naming its successor |
| `artifact.access` | mutation | operator | Reissue an artifact grant for 404/expired ResourceLink (`confirm: true`); requires advertised operator entitlement |
| `replace.preview` | mutation | consumer | Preview a safe asset replacement |
| `replace.apply` | mutation | consumer | Apply the previewed replacement |
| `rollback` | mutation | consumer | Roll back an applied replacement |
| `export` | mutation | consumer | Export a run/asset package |

## Visual library & style

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `library.search` | readonly | consumer | Search the visual library |
| `library.list` | readonly | consumer | List library entries |
| `library.show` | readonly | consumer | Show one library entry |
| `library.save` | mutation | consumer | Save an artifact into the library |
| `library.tag` | mutation | consumer | Tag a library entry |
| `library.update` | mutation | consumer | Update library entry metadata |
| `library.import-url` | mutation | consumer | Import an external image by URL |
| `library.import-runs` | mutation | consumer | Import run artifacts into the library |
| `style.build-from-image` | mutation | consumer | Build a style pack from an image |
| `deck.list` | readonly | consumer | List prompt decks |
| `deck.show` | readonly | consumer | Show one prompt deck |
| `recipes.list` | readonly | consumer | List recipes |
| `recipes.show` | readonly | consumer | Show one recipe |
| `prompts.list` | readonly | consumer | List prompt assets |

## Workflows

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `workflow.plan` | readonly | consumer | Plan a workflow run without executing |
| `workflow.validate` | readonly | consumer | Validate a workflow definition |
| `workflow.run` | generation | consumer | Run a workflow |
| `workflow.pack.inspect` | readonly | consumer | Inspect a workflow pack |
| `workflow.submit_scaena_request` | generation | consumer | Submit a Scaena production request from a workflow |
| `preview.status` | readonly | consumer | Preview job status |

## Delivery pipeline

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `delivery.create` | mutation | consumer | Create a delivery |
| `delivery.status` | readonly | consumer | Delivery status readback |
| `delivery.capture` | mutation | consumer | Capture delivery content |
| `delivery.review` | mutation | consumer | Record delivery review |
| `delivery.resume` | mutation | consumer | Resume a paused delivery |
| `delivery.cancel` | mutation | consumer | Cancel a delivery |
| `delivery.outcome` | mutation | consumer | Record the delivery outcome |

## Comparison loop

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `comparison.preflight` | mutation | consumer | Preflight a comparison (no provider calls) |
| `comparison.start` | generation | consumer | Start a comparison |
| `comparison.status` | readonly | consumer | Comparison status readback |
| `comparison.inspect` | readonly | consumer | Inspect comparison results |
| `comparison.retry_failed` | generation | consumer | Retry failed comparison members |

## Model catalog & diagnostics

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `models.search` | readonly | consumer | Search the model catalog |
| `models.readiness` | readonly | consumer | Model readiness readback |
| `health` | readonly | consumer | Service health readback |

## Operator diagnostics & indexing

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `config.inspect` | readonly | operator | Inspect effective configuration |
| `providers.doctor` | readonly | operator | Provider connectivity diagnostics |
| `projects.list` | readonly | operator | List projects |
| `index.status` | readonly | operator | Search index status |
| `worker.status` | readonly | operator | Worker status readback |
| `capsa.status` | readonly | operator | Capsa sync status readback |
| `sync.status` | readonly | operator | Sync status readback |

## Evidence writeback & datasets

| Action | Kind | Lane | Purpose |
| --- | --- | --- | --- |
| `lifecycle.inspect` | readonly | operator | Inspect asset lifecycle state |
| `outcomes.record` | mutation | operator | Record an outcome evidence entry |
| `reuse.record` | mutation | operator | Record a reuse evidence entry |
| `repairs.record` | mutation | operator | Record a repair evidence entry |
| `dataset.build` | mutation | operator | Assemble a dataset |
| `dataset.export` | mutation | operator | Export a dataset |
| `bindings.confirm` | mutation | consumer | Confirm a binding proposal |
