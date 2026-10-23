---
name: anatomia-gateway-service-operator
description: Use when an Anatomia owner must run read-only preflight, issue or revoke service access keys, or diagnose 401/403 login failures on a self-hosted gateway. Do not use for remote-user login, provider credentials, paid canary, or deploy up.
---

# Anatomia Gateway Service Operator

Owner-only. Remote users receive a `0600` key file and use `$anatomia-video-analysis-router`. This skill never prints plaintext keys, DSN, Authorization headers, or provider payloads.

Confirm current authorization before credential mutation or deployment lifecycle actions. Reuse authorization already given for the exact action and target; read-only preflight alone is not authorization. Provider canaries are outside this skill.

Local preflight (no listener probes or egress):

```bash
anatomia config doctor --json
```

Before issuing a key, collect the recipient label, approved endpoint, scope, state-store identity, owner authority and new private output path as described in `references/commands.md`. Once authorized, issue into a new `0600` file (stdout has fingerprint only):

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

Deployment planning and active observation are described separately in the commands reference. Current `deploy plan` is a local projection; `deploy status` can run container and storage probes. Neither grants deployment or paid Provider authority.
