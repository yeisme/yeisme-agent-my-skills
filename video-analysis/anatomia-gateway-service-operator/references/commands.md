# Commands

Owner-only. `--db` must be the same state store as `anatomia-api`. Do not pass plaintext keys on argv.

## Local preflight

```
anatomia config doctor --json
```

This local config check does not probe a listener or use egress. It does not authorize create, revoke, deploy, or paid provider calls. An HTTP health request is network observation and is not part of this local preflight.

## Ask before issuing a key

Resolve these inputs before `credential-mutation`: Recipient label, approved endpoint, scope, exact API state store, authenticated owner ref, evidence ref, and a missing absolute private output path. Use answers and authorization already supplied in the current session; ask only for missing inputs or new authority. A recipient label is handoff context, not an invented CLI flag.

For an existing local gateway, confirm its actual configured endpoint, for example `http://127.0.0.1:27877`. Do not substitute a placeholder public endpoint. Handoff must not include plaintext keys in chat, logs, screenshots, evidence, or command arguments. Deliver only the approved endpoint and protected key file via the authorized handoff. Receiver verification uses `task accept-intranet-access-key` with the script's required inputs; it performs authenticated service checks and needs its own in-scope endpoint authorization.

### Issue / list / revoke (SQLite)

Use the owner-approved store already initialized by the application. Key-store commands may open or initialize schema; listing is not a substitute for a no-write live database inspection.

```
anatomia service key create \
  --db /absolute/path/to/anatomia-state.sqlite \
  --scope analyze \
  --owner-auth-ref <authenticated-owner-ref> \
  --evidence evidence:<ref> \
  --out /absolute/private/tester.key \
  --endpoint https://anatomia.example.com \
  --json
anatomia service key list --db /absolute/path/to/anatomia-state.sqlite --json
anatomia service key revoke \
  --db /absolute/path/to/anatomia-state.sqlite \
  --key-ref <key-ref> \
  --owner-auth-ref <authenticated-owner-ref> \
  --evidence evidence:<ref> \
  --json
```

`--out` must be a missing absolute path. With `--out`, stdout has no `plaintext_key`. Keep `--out` in agent-operated commands; do not request plaintext output.

### postgres_minio

```
anatomia service key create --state-store postgres --scope analyze --owner-auth-ref <ref> --evidence evidence:<ref> --out /absolute/private/tester.key --endpoint https://anatomia.example.com --json
anatomia service key list --state-store postgres --json
anatomia service key revoke --state-store postgres --key-ref <key-ref> --owner-auth-ref <ref> --evidence evidence:<ref> --json
```

PG DSN never appears on argv or in output. Optional `--runtime-config /absolute/path/runtime.yaml`.

## Gated deployment actions

Keep deployment review separate from local credential preflight. Current `anatomia deploy plan --json` reads the release manifest and local host/config facts, including the configured listener. It does not bind or dial that listener and performs no DNS/TCP probe. Its output is a proposed plan, not owner acceptance or proof of runtime reachability.

```bash
anatomia deploy plan --json --release-manifest <release-manifest> --stage <stage>
```

Active observation requires existing authorization covering the exact deployment and `deployment-lifecycle-mutation` effects. `anatomia deploy status --json` (and `deploy doctor`) can query container state and HTTP endpoints, start a temporary container, and execute a MinIO write/read/delete canary. These probes are never automatic during local preflight, login diagnosis, or a price lookup. DNS/TCP and HTTP access are subject to the configured endpoint boundary.

```bash
anatomia deploy status --json --state-dir /absolute/private/deployment-state
```

`deploy init`, `up`, `first-run`, `down`, and `restart` require authorization for their own effects. A successful plan/status result does not authorize them or any Provider inference. Do not mutate an existing deployment as part of an isolated acceptance test.

## Do not run

- `anatomia login` as a substitute for create (that is the remote-user path).
- Provider `models list` / live canary from this skill.
- `deploy up` unless a separate owner authorization names the stage.
