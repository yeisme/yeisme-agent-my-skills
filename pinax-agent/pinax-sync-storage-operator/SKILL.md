---
name: pinax-sync-storage-operator
description: Use when an agent needs to inspect, configure, or safely operate Pinax Cloud Sync, sync daemon/logs/conflicts, S3-compatible or rclone transports, storage backend, backend profiles, backend object diagnostics, or remote/local storage checks without exposing credentials.
---

# Pinax Sync And Storage Operator

Operate Pinax storage, backend profiles, Cloud Sync, sync daemon, logs, conflicts, and object diagnostics without exposing credentials or confusing local storage, Remote API Mode, and sync transports.

## Use When

- The task mentions Cloud Sync, `pinax sync`, sync daemon, sync logs, conflicts, server/file/S3/rclone transports, Tencent COS, AWS profile, backend profiles, backend object listings, storage status, push/pull, conflict checks, or device/workspace setup.
- The user wants to configure object storage by profile, rclone remote, or secret ref.
- A sync operation may write remote state and needs a plan or diagnostic first.

## Command Patterns

```bash
pinax storage status --json
pinax storage set s3 --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend list --json
pinax backend add s3 tencent-cos --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend doctor tencent-cos --json
pinax backend object list tencent-cos pinax/ --json
pinax backend object stat tencent-cos pinax/manifest.json --json
pinax cloud status --json
pinax cloud backend set s3 --bucket pinax-note-1322128555 --region ap-guangzhou --prefix pinax-sync/ --profile tencent-cos-pinax --workspace yeisme-notes --device laptop --json
pinax cloud backend set rclone --remote pinax-remote:notes --prefix pinax-sync/ --workspace yeisme-notes --device laptop --json
pinax sync diff --target cloud --json
pinax sync push --target cloud --dry-run --json
pinax sync daemon status --json
pinax sync daemon logs --limit 20 --json
pinax sync conflicts list --json
```

## Workflow

1. Inspect current state first: `pinax storage status --json`, `pinax backend list --json`, `pinax cloud status --json`, and `pinax sync status --target cloud --json` when available.
2. Store only profile names, endpoint URLs, bucket names, rclone remote names, prefixes, workspace IDs, device IDs, and secret refs in Pinax config.
3. Do not paste or save raw access keys. Use AWS-compatible profile names such as `tencent-cos-pinax`, rclone remotes such as `onedrive:PinaxSync`, or secret refs such as `env://PINAX_CLOUD_TOKEN`.
4. Use separate prefixes for local storage backend data and Cloud Sync data when possible, for example `pinax-storage/` and `pinax-sync/`.
5. Before remote writes, run `pinax sync diff --target cloud --json` and use `--dry-run` when available.
6. For local automatic sync, inspect daemon status/logs before start/stop, and only run `pinax sync daemon run --target cloud --yes` or `pinax sync daemon start --target cloud --yes` after the user approves automatic writes.
7. On conflicts, inspect `pinax sync conflicts list`, `show`, or `diff`, then stop before choosing local, remote, or merged resolution without user approval.
8. Keep Cloud Sync transports (`server`, `file`, `s3`, `rclone`) separate from localhost Remote API Mode (`pinax api serve` and `--api-url`).

## Safety Boundaries

- Never echo full access keys, secret keys, Authorization headers, cookies, provider config contents, or token values.
- Do not hand-edit `.pinax/cloud/config.yaml`, `.pinax/sync-state.json`, `.pinax/backends.json`, `.pinax/sync-daemon/**`, conflict receipts, or backend receipts.
- Do not claim a remote write succeeded unless the Pinax command returns `remote_write=true` or an equivalent success fact.
- Remote API Mode is not Cloud Sync; keep `--api-url` workflows separate from `pinax cloud` and `pinax sync`.
- Do not treat a direct object store list or upload as a successful sync unless the Pinax sync command committed the revision and reported the success fact.

## Validation

- After storage/backend configuration: `pinax storage doctor --json` and `pinax backend doctor <name> --json`.
- For Cloud Sync: `pinax cloud doctor --json` and `pinax sync diff --target cloud --json`.
- For daemon work: `pinax sync daemon status --json` and `pinax sync daemon logs --limit 20 --json`.
- Verify output reports configured profile/secret-ref status without raw secrets.
