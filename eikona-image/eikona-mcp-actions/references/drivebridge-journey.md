# Eikona / DriveBridge interaction

Discover the installed tools and input schemas before selecting a connection. The development guide is not proof of a released capability. Read eikona://input/capabilities and eikona://docs/drivebridge when available.

1. A Server file version uses input.drivebridge.import with the existing Eikona connection_id, pinned source_ref, SHA-256 and stable idempotency key.
2. A computer-only DriveBridge file uses that computer's relay_targets, then stat, relay_start and operation_get. An unavailable local adapter is a capability gap: use the existing upload page instead of sending a computer path to remote MCP.
3. Explicitly selected outputs use assets.saveback.select. Requires operator/service-api purpose, matching project and explicit rights; an input-only key cannot save selected outputs or record effort.
4. Existing failed imports or savebacks use their own status/resume/cancel actions. Local DriveBridge operation_id, Eikona import_id/input_request_id/saveback_id and Server grant_id are not interchangeable.

blocked/partial returns an advisory recovery instruction. awaiting_transfer means continue the bound local relay. Missing connection/credential means ask the owner to repair that binding. review_required means finish review and canvas checks; never turn on candidate mode as a workaround. Expired/cancelled inputs do not resume. Preserve original keys and file versions; recovery never calls generation.

Server handoff_status/renew/cancel are exposed as input.handoff_status, input.handoff_renew and input.handoff_cancel only when advertised. The Eikona adapter ordinarily owns grant renewal. Check the original target input before any manual renewal; expiry and cancellation are not overridden.

CLI users can perform saveback and effort against a remote Eikona with --endpoint, --key-file and --scope. If connection options are incomplete, do not fall back to local storage. A connected MCP client needs no local Eikona CLI.

feedback.effort phases are preparation, review, repair, transfer and recovery; minutes are explicit, nonnegative and at most 100000. Shared effort is recorded once. report.effort uses independent consumer usage, not accepted feedback or successful file copies, and does not estimate unrecorded work.
