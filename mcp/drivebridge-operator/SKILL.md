---
name: drivebridge-operator
description: "Use when operating personal files through DriveBridge CLI or MCP, choosing local relay versus Server handoff, or recovering uploads and selected Eikona saveback. DriveBridge owns file transfer; image generation and review remain with Eikona."
---

# DriveBridge operator

Choose the file owner before transferring bytes. DriveBridge owns files, versions, scoped access and transfer recovery. Eikona owns image input, review, selected delivery and consumer adoption. Existing Scaena reference/output operations retain their original scope.

## Start from the installed client

A connected MCP client does not need the product CLI. Read tools/list and the advertised inputSchema, then its capabilities resource. A known tool name is not proof that its backend or binding is configured. Never try guessed action names after a denial.

On a machine that already has the local CLI, optional discovery is:

```bash
drivebridge capabilities --json
drivebridge relay targets --json
```

Do not print credentials, owner endpoint/key-file config, transient download URLs or input grants. A stable file or grant ID is not a credential. Configuration commands execute on the owning host, not through arbitrary remote tool parameters.

## Select the path

| Source / job | Control path | Bytes and recovery |
| --- | --- | --- |
| Existing Server file version for Eikona | Eikona input.capabilities, then input.drivebridge.import with a configured connection | Eikona adapter uses authenticated Server HTTP; inspect the original import |
| File available through a computer's local DriveBridge | relay_targets, stat, relay_start | Local adapter sends to the configured original Eikona input; operation_get before resume |
| Computer file without local DriveBridge access | Existing Eikona upload page or authorized HTTP upload | A remote MCP cannot interpret client filesystem paths |
| Selected Eikona output | assets.saveback.select through Eikona | Explicit rights and review; per-item copies and provenance manifest, then original saveback status |
| Ordinary cloud file task | Installed list/search/stat/upload/download tools | Stay inside configured spaces; reuse original transfer operation |

New relay and handoff actions are development capabilities until the installed service advertises them. If absent, explain the missing capability and use an existing supported input route; do not automatically install tools or expand permissions.

## Local relay

relay_targets returns safe target IDs, source spaces, projects and disabled state. network_readiness=not_probed is configuration discovery, not a successful connection test. Choose an enabled target for the intended project, verify the file with stat, then call relay_start with file_ref, target_id and one stable idempotency_key.

Poll operation_get. The returned input_ref belongs to Eikona; it is not a DriveBridge file_ref. An imported image remains unreviewed. For CLI users:

```bash
drivebridge relay start 'drivebridge://file/FILE_REF' --target images --idempotency-key input-one --json
drivebridge operation OPERATION_ID --json
drivebridge resume OPERATION_ID --json
drivebridge relay cancel OPERATION_ID --json
```

Use the actual returned identifiers. Local stable refs pin observed identity/version rather than guaranteeing archived historical bytes; a changed source must fail instead of silently replacing the original transfer. Resuming may retransmit the same file; do not promise universal byte-level resume for rclone backends.

## Server handoff controls

These are Server MCP actions, not local DriveBridge tool aliases:

- input.bind_reference retains ref, consumer, project_ref, purpose, expected_sha256 and idempotency_key. New bound handoffs additionally use an existing binding_id plus consumer_request_ref and RFC3339 request_expires_at.
- input.handoff_status inspects the original grant_id.
- input.handoff_renew is explicit and only for the original bound receiver, within the original input expiry. Check that the target input is still active first.
- input.handoff_cancel closes the grant and retains existing imported copies.

The Eikona adapter normally manages these controls. Do not manually renew a completed/cancelled Eikona input. Bytes stay on authenticated HTTP in the adapter; never return a signed URL or file bytes in normal MCP text. Agents cannot create receiver bindings through these actions.

Owner-host diagnostic CLI:

```bash
drivebridge-server handoff status GRANT_ID --url https://files.example.com --token-file /absolute/private/receiver.key --json
```

## Recover without changing intent

connection_id is Eikona configuration, target_id is local relay configuration, binding_id is Server authorization, grant_id is a Server handoff, import_id is an Eikona import, and saveback_id is an Eikona selected copy. Query each identifier at its owner.

Use the returned recovery instruction with the same identity/project and original operation. Restore a binding or permission through its owner; do not change actors to evade a denial. Fix review failures through Eikona review, not automatic candidate mode. Stop cancelled/expired work and inspect retained evidence before explicitly creating a new intent.

A partial saveback must retain completed file receipts and resume missing work. Complete requires the provenance manifest too. Transfer recovery never authorizes generation, paid retries, permission expansion or deletion. Saving a file is not consumer adoption.
