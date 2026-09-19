---
name: anatomia-gateway-service-operator
description: Use when an Anatomia owner must run read-only preflight, issue or revoke service access keys, or diagnose 401/403 login failures on a self-hosted gateway. Do not use for remote-user login, provider credentials, paid canary, or deploy up.
---

# Anatomia Gateway Service Operator

Owner-only. Remote users receive a `0600` key file and use `$anatomia-video-analysis-router`. This skill never prints plaintext keys, DSN, Authorization headers, or provider payloads.

🔴 CHECKPOINT · 🛑 STOP before `service key create`, `service key revoke`, `deploy up`, or any Provider canary. Read-only preflight is not authorization.

Preflight (no writes):

```bash
anatomia config doctor --json
anatomia deploy plan --release-manifest <release-manifest> --stage <stage> --json
```

Issue a key into a new `0600` file (stdout has fingerprint only):

```bash
anatomia service key create \
  --db /absolute/path/to/anatomia-state.sqlite \
  --scope analyze \
  --owner-auth-ref <authenticated-owner-ref> \
  --evidence evidence:<ref> \
  --out /absolute/private/tester.key \
  --endpoint https://anatomia.example.com \
  --json
```

Public `postgres_minio` deployments use `--state-store postgres` instead of `--db`. `--db` and `--state-store` are mutually exclusive. Commands: `references/commands.md`. Handoff: `references/handoff.md`.
