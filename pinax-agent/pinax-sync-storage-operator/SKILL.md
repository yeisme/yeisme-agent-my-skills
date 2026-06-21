---
name: pinax-sync-storage-operator
description: Use when an agent needs to inspect, configure, or safely operate Pinax Cloud Sync, S3-compatible storage, Tencent COS profiles, backend profiles, sync plans, or remote/local storage diagnostics.
---

# Pinax Sync And Storage Operator

Operate Pinax storage, backend profiles, and Cloud Sync without exposing credentials or confusing local storage, Remote API Mode, and sync transports.

## Use When

- The task mentions Cloud Sync, `pinax sync`, server/file/S3/rclone transports, Tencent COS, AWS profile, backend profiles, storage status, push/pull, conflict checks, or device/workspace setup.
- The user wants to configure object storage by profile or secret ref.
- A sync operation may write remote state and needs a plan or diagnostic first.

## Command Patterns

```bash
pinax storage status --json
pinax storage set-s3 --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend list --json
pinax backend add s3 tencent-cos --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend doctor tencent-cos --json
pinax cloud status --json
pinax cloud backend set s3 --bucket pinax-note-1322128555 --region ap-guangzhou --prefix pinax-sync/ --profile tencent-cos-pinax --workspace yeisme-notes --device laptop --json
pinax cloud backend set rclone --remote pinax-remote:notes --prefix pinax-sync/ --workspace yeisme-notes --device laptop --json
pinax sync diff --target cloud --json
pinax sync push --target cloud --dry-run --json
```

## Workflow

1. Inspect current state first: `pinax storage status --json`, `pinax backend list --json`, and `pinax cloud status --json`.
2. Store only profile names, endpoint URLs, bucket names, rclone remote names, prefixes, workspace IDs, device IDs, and secret refs in Pinax config.
3. Do not paste or save raw access keys. Use AWS-compatible profile names such as `tencent-cos-pinax` or secret refs such as `env://PINAX_CLOUD_TOKEN`.
4. Use separate prefixes for local storage backend data and Cloud Sync data when possible, for example `pinax-storage/` and `pinax-sync/`.
5. Before remote writes, run `pinax sync diff --target cloud --json` and use `--dry-run` when available.
6. On conflicts, inspect conflict commands and stop before choosing local or remote resolution without user approval.
7. Keep Cloud Sync transports (`server`, `file`, `s3`, `rclone`) separate from localhost Remote API Mode (`pinax api serve` and `--api-url`).

## Safety Boundaries

- Never echo full access keys, secret keys, Authorization headers, cookies, or provider config contents.
- Do not hand-edit `.pinax/cloud/config.yaml`, `.pinax/sync-state.json`, `.pinax/backends.json`, or backend receipts.
- Do not claim a remote write succeeded unless the Pinax command returns `remote_write=true` or an equivalent success fact.
- Remote API Mode is not Cloud Sync; keep `--api-url` workflows separate from `pinax cloud` and `pinax sync`.
- Do not treat a direct object store list or upload as a successful sync unless the Pinax sync command committed the revision and reported the success fact.

## Validation

- After configuration: `pinax storage doctor --json` and `pinax backend doctor <name> --json`.
- For Cloud Sync: `pinax cloud doctor --json` and `pinax sync diff --target cloud --json`.
- Verify output reports configured profile/secret-ref status without raw secrets.
