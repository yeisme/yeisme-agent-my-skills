# Handoff

- Remote user login/analyze: `$anatomia-video-analysis-router`. Hand them the `0600` file and approved endpoint only.
- Registered-ref questions: `$anatomia-video-evidence-navigator`.
- VLM-Codex interaction inspect/reconcile: `$anatomia-vlm-codex-interaction`.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| `401 access_key_invalid` | `service key list --json` vs API `--db` / `ANATOMIA_SERVICE_ACCESS_KEY_FILE` | Re-issue to a new `--out` path; never reuse a revoked `key_ref` |
| `403 access_key_scope_insufficient` | Use `analyze` scope or GET-only | Do not widen a `read` key in place |
| Create refused because `--out` exists | Choose a new path | Do not overwrite |
| Revoke bootstrap key | Also delete that line from `ANATOMIA_SERVICE_ACCESS_KEY_FILE` | API will fail-closed on replay if the line remains |
| `--db` vs `--state-store` both set | Use one | Exit 2 `service_key_*_state_store_invalid` |

## Do not

- Print `plaintext_key`, DSN, Authorization, provider payloads, or host secrets.
- Ask chat for a pasted key. Demand a `0600` file.
- Treat deploy plan success as deploy authorization.
- Auto `--force`, auto `deploy up`, or paid Provider canary.
- Copy this package into the public five-skill user install set.
