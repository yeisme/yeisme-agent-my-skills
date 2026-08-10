---
name: local-first-backup-sync-policy
description: Use when designing, documenting, reviewing, or operating local-first backup and sync policy for Git-managed project state plus S3-compatible, rclone, cloud-drive, or CLI-authored backup/restore flows, especially when deciding whether real-time sync needs a separate design.
---

# Local First Backup Sync Policy

Use this skill for reusable local-first backup and sync policy. It keeps Git, object storage, rclone/cloud drives, and product CLIs in separate roles.

## Policy

Default to backup sync, not real-time sync:

- Git manages reviewable project state: config, workflows, manifests, prompts, project metadata, policies, and small source-of-truth records.
- Product CLIs create and modify structured assets. Agents must not hand-write schema-bearing JSON, YAML, JSONL, or Markdown metadata files.
- S3-compatible storage, rclone, NAS, and cloud drives provide backup, restore, migration, and disaster recovery mirrors.
- Real-time sync, file watchers, background daemons, automatic merge, and conflict resolution require a separate design with explicit conflict, lock, rollback, evidence, and credential boundaries.

Pinax is a product-specific exception to generic mirror ordering: when Pinax owns the vault and the binary supports it, prefer Pinax-native repository-encrypted S3/COS Capsa Sync. Git carries reviewable Markdown plus encrypted declaration/ciphertext; rclone is only an external fallback. Do not replace a working Pinax-native design with raw directory mirroring.

## Inputs

- Project state directories, for example `.eikona`, `.auctra`, `.scaena`, `.pinax`, `.gitpulse`, `.app`, `.tool`, or another local-first project directory.
- Existing product CLI commands for config, backup, push, pull, restore, doctor, diff, or sync.
- Remote targets such as S3-compatible buckets, rclone remotes, cloud drives, WebDAV, NAS, or offline archive directories.

## Workflow

1. Read the project or repository backup policy first. In Yeisme, read `docs/workflows/local-first-backup-sync.md`.
2. Classify the requested work:
   - cross-project policy or skill docs: repository workflow docs and skill docs;
   - one product's backup behavior: the owning subproject docs, OpenSpec, and CLI implementation;
   - Pinax Capsa Sync/S3/rclone operation: route through `pinax-agent-router`, then `pinax-sync-storage-operator`; prefer repository-encrypted S3/COS, then Git companion/fallback, then rclone external fallback;
   - Eikona storage behavior: use `yeisme-eikona-cli-runtime` after reading Eikona storage docs.
3. Identify Git-managed state directories. For Yeisme defaults:

```bash
git status --short -- .eikona .auctra .scaena .pinax .gitpulse
git diff -- .eikona .auctra .scaena .pinax .gitpulse
```

4. Prefer CLI-authored backup commands where they exist. For Eikona:

```bash
eikona storage backend set s3 --bucket eikona-assets --prefix eikona-sync/ --region us-east-1 --profile work --json
eikona storage push --backend s3 --yes --json
eikona storage restore --backend s3 --revision <revision> --to temp/storage-restore --json
```

5. For generic non-Pinax repository mirrors, use rclone with explicit excludes:

```bash
rclone copy . remote:project-backup --exclude '.git/**' --exclude '**/node_modules/**' --exclude '**/temp/**' --exclude '**/dist/**'
rclone check . remote:project-backup --one-way --exclude '.git/**' --exclude '**/node_modules/**' --exclude '**/temp/**' --exclude '**/dist/**'
```

6. Restore into staging, a temporary branch, or a temporary worktree first. Do not overwrite a live project root directly.
7. If the user asks for real-time sync, stop and produce a design first. Do not silently turn backup sync into a daemon or bidirectional merge system.

## Boundaries

- Do not design real-time sync by default.
- Do not copy one product's daemon or conflict model into another product without a design and migration plan.
- Do not commit or upload plaintext secrets, raw provider payloads, raw prompts containing private data, hidden prompts, private tool arguments, full chain-of-thought, local credential stores, SQLite WAL/SHM, vector indexes, caches, thumbnails, `temp/`, `dist/`, or `node_modules`.
- Do not claim a remote write succeeded unless the owning CLI reports `remote_write=true` or an equivalent success fact.
- Do not recommend shell credential scripts as a persistence layer.
- Prefer product-native encrypted envelopes and CLI-generated backup objects over raw local directory mirroring. For Pinax, repository-encrypted S3/COS is the preferred target workflow.
- In Yeisme docs, use `.eikona` as the correct path spelling; `.eikoan` is a typo.

## Outputs

- A backup policy or doc update that separates Git-managed state from object-store/cloud-drive backup mirrors.
- A project-specific command sequence for backup, verification, and staged restore.
- A clear statement when real-time sync is out of scope and needs a separate design.

## Validation

For docs and skills only:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh list-custom
```

If profiles or runtime copies are changed:

```bash
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
scripts/skills.sh validate-runtime
```

For Eikona storage documentation or behavior:

```bash
cd cli/eikona
openspec validate --all
go test ./internal/storage ./internal/storagesync ./internal/cli -run 'Storage|S3|Backend|Restore|Push|Pull' -count=1
```

For Pinax sync/storage operations, use routed Pinax operator commands and validate with `pinax sync status --agent`, `pinax sync repo doctor --json`, and `pinax sync diff --target capsa --json` when available.
