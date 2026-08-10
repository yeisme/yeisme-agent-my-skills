---
name: pinax-sync-storage-operator
description: Use when an agent needs to inspect, configure, migrate, restore, or safely operate Pinax Capsa Sync, repository-encrypted S3/COS bootstrap, sync logs/conflicts, background sync, S3/rclone transports, backend diagnostics, or remote/local storage checks without exposing credentials.
---

# Pinax Sync And Storage Operator

Operate Pinax Capsa Sync, repository-encrypted S3/COS bootstrap, storage profiles, background sync, logs, conflicts, and object diagnostics without exposing credentials or confusing repository state, device runtime state, Remote API Mode, and sync transports.

## Recommendation Order

For a Pinax vault, recommend these options in this order:

1. **Preferred target: Pinax-native repository-encrypted S3/COS.** Use `.pinax/pinax-sync.yaml` plus `.pinax/project-secrets.yaml`, `pinax sync repo migrate device-profile`, and clone-time `pinax sync repo bootstrap --pull`. Git distributes the declaration and ciphertext; Capsa direct S3 stores encrypted content blobs, manifests, and revisions.
2. **Git fallback/companion.** Use Git for Markdown history, review, rollback, and distribution of the encrypted repository declaration. Do not present Git as a substitute for Capsa attachment/blob/revision backup when Pinax-native S3 is available.
3. **rclone fallback.** Use rclone only for generic archive/mirror recovery when the current Pinax binary or provider cannot complete the native workflow. Prefer rclone crypt or another encrypted destination, restore into staging, and label it external backup rather than Pinax Sync.

The repository-encrypted S3 path remains experimental until the active binary supports the required capabilities, remote-aware `diff|push`, durable commit read-back, and real macOS round-trip evidence. Prefer the design, but do not claim it is stable or complete merely because migration/bootstrap commands exist.

## Non-Negotiable Sync Boundaries

- `pinax sync ... --target capsa` is the primary distributed sync workflow. `cloud` and `pinax-cloud` may be legacy aliases; do not recommend them in new commands when `capsa` is available.
- `pinax backend ...` manages provider-style storage backends such as backup/export mirrors under backend prefixes. It can be diagnosed, but a successful backend pull/push event is not evidence that Cloud Sync completed.
- If the user asks for multi-device restore or S3 backup, inspect `pinax sync status --agent`, `pinax sync repo doctor --json`, and `pinax sync diff --target capsa --json` before considering Git-only or rclone mirroring.
- If a projection says `real remote writes are not wired yet`, `status=partial`, `remote_checked=false`, `remote_write=false` without `up_to_date=true`, or lacks an explicit durable commit/read-back fact, stop and report that native S3 backup did not complete. Do not switch to adjacent backend commands to manufacture success-looking output.
- A successful backup with changes requires `remote_write=true`, a non-empty committed revision, and remote head/manifest read-back. An unchanged backup requires explicit `up_to_date=true` plus `remote_checked=true`.
- Do not ask for endpoint, workspace, device, profile, or secret values when status/doctor already reports a configured backend and repository envelope. Reuse the existing declaration and secret identity.

## Use When

- The task mentions Capsa Sync, `pinax sync`, passphrase S3 bootstrap, repository-encrypted credentials, macOS Keychain, background sync, conflicts, server/file/S3/rclone transports, Tencent COS, AWS profile migration, backend diagnostics, push/pull, or device/workspace setup.
- The user wants to configure object storage by profile, rclone remote, or secret ref.
- A sync operation may write remote state and needs a plan or diagnostic first.

## Command Patterns

```bash
pinax storage status --agent
pinax storage set s3 --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend list --agent
pinax backend add s3 tencent-cos --bucket pinax-note-1322128555 --region ap-guangzhou --endpoint https://cos.ap-guangzhou.myqcloud.com --prefix pinax-storage/ --profile tencent-cos-pinax --json
pinax backend doctor tencent-cos --json
pinax backend object list tencent-cos pinax/ --json
pinax backend object stat tencent-cos pinax/manifest.json --json
pinax sync status --agent
pinax sync repo doctor --json
pinax sync repo migrate device-profile --unlock prompt --remember-keychain --yes --json
pinax sync repo plan --json
pinax sync repo bootstrap --device macbook --unlock prompt --remember-keychain --pull --yes --json
pinax vault ignore status --json
pinax vault ignore apply --yes --json
pinax sync diff --target capsa --json
pinax sync push --target capsa --dry-run --json
pinax sync pull --target capsa --unlock keychain --yes --json
pinax sync logs list --json
pinax sync conflicts list --json
```

## Preferred Repository-Encrypted S3/COS Workflow

On an existing device that already has a working `s3-direct` runtime and AWS shared profile:

```bash
pinax sync repo migrate device-profile \
  --vault . \
  --unlock prompt \
  --remember-keychain \
  --yes \
  --json

pinax sync repo plan --vault . --json
pinax sync repo doctor --vault . --json
git add .pinax/pinax-sync.yaml .pinax/project-secrets.yaml
git commit -m "chore(sync): enable repository-encrypted S3 bootstrap"
git push
```

On a new Mac after cloning the private vault:

```bash
pinax sync repo bootstrap \
  --vault . \
  --device "$(scutil --get LocalHostName 2>/dev/null || hostname)" \
  --unlock prompt \
  --remember-keychain \
  --pull \
  --yes \
  --json

pinax sync repo doctor --vault . --json
pinax vault validate --vault . --json
```

The initial bootstrap must remain pull-only with `remote_write=false`. Do not approve a subsequent push until the active Pinax build exposes repository unlock for remote-aware diff/push and the dry-run reads the real remote head.

## Device-Profile Compatibility Fallback

The AWS shared profile path remains supported for compatibility, recovery, and migration into the preferred repository-encrypted workflow. Pinax only needs an AWS-compatible profile that the S3 SDK can read. Do not require AWS CLI solely to run `aws configure`; if necessary, show direct profile creation with placeholders only:

```bash
mkdir -p ~/.aws
chmod 700 ~/.aws

cat >> ~/.aws/credentials <<'EOF'
[tencent-cos-pinax]
aws_access_key_id = <Tencent COS SecretId>
aws_secret_access_key = <Tencent COS SecretKey>
EOF

cat >> ~/.aws/config <<'EOF'
[profile tencent-cos-pinax]
region = ap-guangzhou
EOF

chmod 600 ~/.aws/credentials ~/.aws/config
```

Then configure the Pinax Capsa direct S3 backend:

```bash
pinax capsa backend set s3 \
  --bucket pinax-note-1322128555 \
  --region ap-guangzhou \
  --endpoint https://cos.ap-guangzhou.myqcloud.com \
  --prefix pinax-sync/ \
  --profile tencent-cos-pinax \
  --workspace yeisme-notes \
  --device <device-name> \
  --vault ./yeisme-notes \
  --json
```

Keep `~/.aws/credentials` and `~/.aws/config` outside the repository. If a user placed AWS files inside a vault or project by mistake, stop and ask them to move the files to `~/.aws/`; do not add real credentials to `.gitignore` as a substitute for moving them out of the repo.

## Durable Backup Workflow

Call the native workflow a backup mirror only when Pinax Capsa Sync writes encrypted objects through the selected direct transport. Direct S3/COS is preferred for Pinax; rclone direct is a provider compatibility option, not the default recommendation. Neither becomes Capsa server-side storage or provides server auth, audit, lifecycle policy, tenant policy, or automatic conflict resolution.

Use this order:

```bash
pinax vault ignore status --json
pinax vault ignore plan --json
pinax vault ignore apply --yes --json
pinax sync status --agent
pinax sync repo doctor --json
pinax sync diff --target capsa --json
pinax sync push --target capsa --dry-run --json
pinax sync push --target capsa --yes --json
```

For restore or second-device verification, initialize/select the second vault, configure the same backend with a different `--device`, then pull:

```bash
git clone https://github.com/yeisme/yeisme-notes.git yeisme-notes
cd yeisme-notes
pinax sync repo bootstrap --device <second-device-name> --unlock prompt --remember-keychain --pull --yes --json
pinax vault validate --json
```

Treat `remote_write=true` plus committed revision read-back as the success signal for a changed backup. Treat `up_to_date=true` plus `remote_checked=true` as the only successful no-change result. Backend setup, Git push, object list, dry-run, blob upload, or local receipt alone is not native S3 backup completion.

When diagnosing an existing vault, read `pinax sync status --agent` and `pinax sync repo doctor --json` before asking for configuration values. If they already report `configured=true`, `backend_kind=s3-direct`, a workspace, a device and a repository credential identity/profile, do not re-run setup or request secrets. Continue with a Capsa diff and the narrowest applicable verification.

## Ignore Handling

Use Pinax commands for vault ignore policy instead of editing metadata by hand:

```bash
pinax vault ignore status --json
pinax vault ignore plan --json
pinax vault ignore apply --yes --json
```

`.pinaxignore` controls which vault content enters the Pinax Cloud Sync manifest. `.gitignore` only controls Git. New or existing vaults should have the Pinax-managed metadata-only `.gitignore` block so Git does not track runtime `.pinax` state, receipts, local sync state, daemon logs, indexes, or caches. Do not hand-edit `.pinax/**`, `.pinaxignore`, or the managed `.gitignore` block unless the Pinax command is unavailable and the user explicitly approves a manual recovery.

## Workflow

1. Inspect `pinax sync status --agent`, `pinax sync repo doctor --json`, vault ignore status, conflicts, and current command help before recommending a transport.
2. Prefer repository-encrypted S3/COS when the active binary supports its required capabilities. Use Git to distribute the declaration/ciphertext, not as a reason to skip native S3 validation.
3. Store only ciphertext, logical credential identities, endpoint URLs, bucket names, prefixes, workspace IDs, device IDs, profiles, and secret refs in Pinax assets. Never store raw credentials.
4. Use AWS shared profiles only for compatibility, rollback, or the one-time migration source. Use rclone only when Pinax-native S3 is unavailable or the target provider requires it.
5. Before backup or sync writes, check `pinax vault ignore status --json` and run `pinax vault ignore apply --yes --json` when the Pinax-managed ignore files are missing.
6. Use separate prefixes for local storage backend data and Cloud Sync data when possible, for example `pinax-storage/` and `pinax-sync/`.
7. Before remote writes, require a remote-aware `pinax sync diff --target capsa --json` and push dry-run.
   If the diff output plans operations but also reports that real remote writes are not wired, treat the result as a blocked/partial implementation state rather than a user configuration problem.
8. For automatic sync, use `pinax sync daemon` only when current help lists it and repository credentials resolve non-interactively from Keychain/file/secret manager. Never let a daemon prompt.
9. On conflicts, inspect `pinax sync conflicts list`, `show`, or `diff`, then stop before choosing local, remote, or merged resolution without user approval.
10. Keep Cloud Sync transports (`server`, `file`, `s3`, `rclone`) separate from localhost Remote API Mode (`pinax api serve` and `--api-url`).

## Safety Boundaries

- Never echo full access keys, secret keys, Authorization headers, cookies, provider config contents, or token values.
- Do not hand-edit `.pinax/cloud/config.yaml`, `.pinax/sync-state.json`, `.pinax/backends.json`, `.pinax/sync-daemon/**`, conflict receipts, or backend receipts.
- Do not commit or copy `~/.aws/credentials`, `~/.aws/config`, `.env`, `.pinax/sync-state.json`, `.pinax/sync-daemon/**`, generated indexes, caches, receipts, or local vault runtime state into the repository.
- Do not claim a remote write succeeded unless the Pinax command returns `remote_write=true` or an equivalent success fact.
- Remote API Mode is not Capsa Sync; keep `--api-url` workflows separate from `pinax sync --target capsa` and sync repository configuration.
- Do not treat a direct object store list or upload as a successful sync unless the Pinax sync command committed the revision and reported the success fact.

## Validation

- After storage/backend configuration: `pinax storage doctor --json` and `pinax backend doctor <name> --json`.
- For native repository-encrypted S3: `pinax sync repo doctor --json`, `pinax sync status --agent`, and `pinax sync diff --target capsa --json`.
- For backup mirror: `pinax vault ignore status --json`, a remote-aware push dry-run, then a confirmed `pinax sync push --target capsa --yes --json` with durable commit/read-back evidence.
- For background sync work: verify the OS scheduler separately, and inspect Pinax state with `pinax sync status --agent` and `pinax sync logs list --json`.
- Verify output reports configured profile/secret-ref status without raw secrets.
