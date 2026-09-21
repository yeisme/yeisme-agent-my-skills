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

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Tool denial or unknown action | Re-read tools/list and capabilities | Do not guess aliases or install extra tools |
| `network_readiness=not_probed` | Treat as discovery, not a live connection | Probe on the owning host; do not invent success |
| Relay/handoff missing from the installed service | Explain the gap; use an existing upload/input route | Do not auto-expand permissions |
| Import/saveback review failed | Fix through Eikona review | Do not switch to candidate/paid retry |
| Cancelled or expired operation | Inspect retained evidence; new intent only if the user asks | Do not resume as a different actor |
| Credential or transient URL in output | Redact and rerun | Stable file/grant IDs are not credentials |

## Intranet CAS and mounts (design-stage)

Server blob reuse and local WebDAV/FUSE mounts are specified, not shipped. Until capabilities advertise `cas_reuse=available` (not merely the key existing) or `mount.adapter=webdav` with a live `mount_status`, keep using ordinary upload/download and original operations.

- File identity stays `drivebridge://<instance>/file/<id>/version/<vid>` (remote) or `drivebridge://file/<hash>` (local). A SHA-256 blob is not a capability token and is not a public URI. Do not call `GET /api/v1/blobs/{sha256}` as a substitute for `stat`.
- A matching digest does not authorize a read. If create_upload/download reports `blob_reused` or zero transferred bytes, still `stat` the returned version before consuming. `blob_unavailable` means re-upload the original file with a new idempotency key; never treat an empty body as a hit.
- Do not start mounts through MCP. There is no Server `POST /api/v1/mounts`. `drivebridge mount webdav` is a user-terminal command; default binaries return `unsupported` for `mount fuse`. Unlink in a mount is trash, not purge.
- Do not treat a local `.drivebridge-cas` path as a stable reference or send it to a remote tool.

## Pinax object-storage vault

Plaintext notes on S3/MinIO/COS are a **path mount**, not a Pinax remote adapter. Contract: `openspec/changes/pinax-drivebridge-mounted-vault-v1/`. Check `drivebridge capabilities --json` for `mount.path_preset=pinax-vault` and `mount.path_adapters` including `s3`. Agents must not start the mount. Until `mount status` shows `preset=pinax-vault`, `vault_root` set, `alive=true`, tell the user to run the terminal recipe.

```bash
drivebridge storage add --kind s3 --space pinax-vault \
  --remote minio --remote-path '<bucket>/<prefix>' --local-root /abs/workspace --json
drivebridge preset pinax-vault --space pinax-vault --vault-root /abs/Pinax/cloud --json
drivebridge mount status --json
```

S3 uses the host `rclone` CLI (`rclone mount`, `--vfs-cache-mode writes`) plus FUSE/macFUSE/WinFsp. `kind=local` alias spaces overlay without FUSE. Missing rclone/FUSE returns `mount_path_adapter_missing`; do not treat a WebDAV port as `vault_root`.

Then Pinax uses only local commands on that `vault_root` (`pinax init`, `pinax storage set local`, `pinax note add`). Do not point Pinax at `.drivebridge-cas`. Do not use the same prefix as Capsa ciphertext. `.pinax/**` stays on local disk.
