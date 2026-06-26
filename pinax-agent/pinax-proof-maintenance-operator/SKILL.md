---
name: pinax-proof-maintenance-operator
description: Use when an agent needs to run Pinax proof loops, vault doctor/stats, metadata/repair/organize plans or applies, version snapshot/restore, record ledger maintenance, or other high-risk local maintenance with snapshot and approval gates.
---

# Pinax Proof Maintenance Operator

Run Pinax proof-loop and high-risk maintenance workflows with explicit diagnostics, saved plans, snapshots, and approval gates. This skill owns maintenance that can modify many notes, `.pinax/**` state, version evidence, or recovery state.

## Use When

- The request mentions `pinax proof`, proof loop, doctor/stats, maintenance, metadata completion, repair, organize, version snapshot, restore, rollback, record ledger, or broad cleanup.
- The user wants to apply a saved repair/organize/metadata plan.
- A command may rewrite frontmatter, move many notes, repair indexes/metadata, restore vault state, or mutate record/version evidence.

## Command Patterns

```bash
pinax proof loop run --vault ./my-notes --json
pinax proof loop run --vault ./my-notes --apply --yes --json
pinax vault doctor --vault ./my-notes --json
pinax vault stats --vault ./my-notes --json
pinax metadata plan --vault ./my-notes --json
pinax metadata apply --vault ./my-notes --yes --json
pinax repair plan --vault ./my-notes --save --json
pinax repair apply --vault ./my-notes --plan repair-abc123 --yes --snapshot-message "pre-repair snapshot" --json
pinax organize plan --vault ./my-notes --save --json
pinax organize list --vault ./my-notes --json
pinax organize apply --vault ./my-notes --plan organize-abc123 --yes --snapshot-message "pre-organization snapshot" --json
pinax version snapshot --vault ./my-notes --message "before maintenance" --json
pinax version restore notes/a.md --revision snap_123 --plan --vault ./my-notes --json
pinax version restore apply --vault ./my-notes --plan restore-abc123 --yes --json
pinax record status --vault ./my-notes --json
pinax record adopt --vault ./my-notes --plan --json
```

## Workflow

1. Inspect first with `pinax vault doctor --json`, `pinax vault stats --json`, or `pinax proof loop run --json`.
2. Prefer a read-only proof loop before manual sequencing. `pinax proof loop run --json` covers capture/retrieve/diagnose/plan/snapshot/apply readiness in one bounded projection.
3. Generate and inspect plans before any apply: `pinax metadata plan`, `pinax repair plan --save`, or `pinax organize plan --save`.
4. Before `metadata apply`, `repair apply`, `organize apply`, `version restore`, broad record adoption, or any high-risk write, create a fresh snapshot with `pinax version snapshot --message "before maintenance" --json`.
5. Require explicit user approval before commands with `--yes`, `--apply`, restore, destructive cleanup, or bulk moves.
6. After an apply, run the matching diagnostic again, such as `pinax vault doctor --json`, `pinax proof loop run --json`, or `pinax record status --json`.
7. If an operation reports partial success, conflict, snapshot required, or approval required, stop and surface the exact next safe command.

## Safety Boundaries

- Do not hand-edit `.pinax/**`, SQLite stores, repair/organize plan JSON, record ledgers, or version metadata.
- Do not run `--yes`, `--apply`, or restore commands without a snapshot and explicit approval.
- Do not treat `proof loop run --apply --yes` as a default command; use the read-only proof loop first.
- Do not hide warnings about untracked files, missing snapshots, conflicts, or unsupported restore backends.

## Validation

- Before apply: saved plan path exists in command output and a fresh snapshot command succeeded.
- After apply: `pinax proof loop run --json` or `pinax vault doctor --json` reports expected status.
- For restore: run a read-only status/doctor command and report restored snapshot id, not raw file diffs.
