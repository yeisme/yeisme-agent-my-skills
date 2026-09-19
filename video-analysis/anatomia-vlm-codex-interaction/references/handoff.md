# Handoff

- Login and analyze a local file: `$anatomia-video-analysis-router`.
- Bounded question on a registered ref: `$anatomia-video-evidence-navigator`.
- Owner key issue/revoke: `$anatomia-gateway-service-operator`.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Version/identity drift on reconcile | Re-GET the session; reuse the original Idempotency-Key | Do not mint a new key or rewrite the attempt ref |
| `ErrInteractionOwnerAuthority` | Confirm owner-only credential | Remote user keys cannot reconcile |
| `ErrInteractionBudgetOrPolicy` | Stop | Do not start a live Provider attempt from this skill |
| Missing CLI `video dialogue` | Use HTTP/SDK | Do not document unpublished commands as released |

## Do not

- Parse provider payloads, raw prompts, or full chain-of-thought from events.
- Retry a cancelled session as a new writer.
- Put this skill in the public five-skill user install set.
- Treat inspect success as production promotion.
