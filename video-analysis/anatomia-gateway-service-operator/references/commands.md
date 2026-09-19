# Commands

Owner-only. `--db` must be the same state store as `anatomia-api`. Do not pass plaintext keys on argv.

## Preflight

```
anatomia config doctor --json
anatomia deploy plan --release-manifest <release-manifest> --stage <stage> --json
curl -sS <endpoint>/healthz
```

These checks do not authorize create, revoke, deploy, or paid provider calls.

## Issue / list / revoke (SQLite)

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

`--out` must be a missing absolute path. With `--out`, stdout has no `plaintext_key`. Omit `--out` only when the operator must see the one-time plaintext in the create response.

## postgres_minio

```
anatomia service key create --state-store postgres --scope analyze --owner-auth-ref <ref> --evidence evidence:<ref> --out /absolute/private/tester.key --endpoint https://anatomia.example.com --json
anatomia service key list --state-store postgres --json
anatomia service key revoke --state-store postgres --key-ref <key-ref> --owner-auth-ref <ref> --evidence evidence:<ref> --json
```

PG DSN never appears on argv or in output. Optional `--runtime-config /absolute/path/runtime.yaml`.

## Do not run

- `anatomia login` as a substitute for create (that is the remote-user path).
- Provider `models list` / live canary from this skill.
- `deploy up` unless a separate owner authorization names the stage.
