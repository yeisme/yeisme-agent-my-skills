---
name: yeisme-local-backup-sync-policy
description: Use when designing, documenting, reviewing, or operating Yeisme local-first backup and sync policy across project state directories such as .eikona, .auctra, .indagator, .scaena, .pinax, and .gitpulse, especially Git-managed state plus S3-compatible, rclone, or cloud-drive backup flows, and when deciding whether real-time sync needs a separate design.
---

# Yeisme Local Backup Sync Policy

Use this skill for cross-project local-first backup and sync policy. It keeps Git, S3-compatible storage, rclone, cloud drives, and project CLIs in separate roles.

## Policy

Default to backup sync, not real-time sync:

- Git manages reviewable project state under directories such as `.eikona`, `.auctra`, `.indagator`, `.scaena`, `.pinax`, and `.gitpulse`.
- S3-compatible storage, rclone, and cloud drives provide backup, restore, migration, and disaster recovery mirrors.
- Project CLIs create and modify structured assets. Agents must not hand-write schema-bearing JSON, YAML, JSONL, or Markdown metadata files.
- Real-time sync, file watchers, background daemons, automatic merge, and conflict resolution require a separate OpenSpec change.

## Workflow

1. Read `docs/workflows/local-first-backup-sync.md` before changing docs, skills, or implementation plans.
2. Classify the requested work:
   - repository policy or cross-project docs: root `docs/workflows/` or `docs/skills/`;
   - Eikona storage behavior: `cli/eikona/docs/**`, `cli/eikona/openspec/**`, or `cli/eikona/internal/**`;
   - Pinax Cloud Sync/S3/rclone operation: route through `pinax-agent-router`, then `pinax-sync-storage-operator`;
   - other subproject storage implementation: enter the owning subproject and follow its `AGENTS.md`.
3. Keep Git scope explicit. Before suggesting a commit, inspect only the relevant state directories:

```bash
git status --short -- .eikona .auctra .indagator .scaena .pinax .gitpulse
git diff -- .eikona .auctra .indagator .scaena .pinax .gitpulse
```

4. Prefer CLI-authored backup commands where they exist. For Eikona:

```bash
eikona storage backend set s3 --bucket eikona-assets --prefix eikona-sync/ --region us-east-1 --profile work --json
eikona storage push --backend s3 --yes --json
eikona storage restore --backend s3 --revision <revision> --to temp/storage-restore --json
```

5. For generic backup mirrors, use rclone with explicit excludes:

```bash
rclone copy . remote:yeisme-agent-backup --exclude '.git/**' --exclude '**/node_modules/**' --exclude '**/temp/**' --exclude '**/dist/**'
rclone check . remote:yeisme-agent-backup --one-way --exclude '.git/**' --exclude '**/node_modules/**' --exclude '**/temp/**' --exclude '**/dist/**'
```

6. Restore into staging or a branch first. Do not overwrite a live project root directly.

## Boundaries

- Do not design real-time sync by default.
- Do not copy Pinax Cloud Sync daemon assumptions into Eikona, Auctra, Indagator, Scaena, or GitPulse without an OpenSpec design.
- Do not commit secrets, raw provider payloads, raw prompts containing private data, hidden prompts, private tool arguments, full chain-of-thought, local credential stores, SQLite WAL/SHM, vector indexes, caches, thumbnails, `temp/`, `dist/`, or `node_modules`.
- Do not claim `remote_write=true` unless the owning CLI reports it or an equivalent success fact.
- Do not recommend shell credential scripts as a persistence layer.
- Use `.eikona` as the correct path spelling; `.eikoan` is treated as a typo.

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

For Pinax sync/storage operations, use the routed Pinax operator commands and validate with `pinax storage status --json`, `pinax cloud status --json`, and `pinax sync diff --target cloud --json` when available.
