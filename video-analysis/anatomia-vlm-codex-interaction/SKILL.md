---
name: anatomia-vlm-codex-interaction
description: Use when inspecting or reconciling a local Anatomia VLM-Codex interaction session through owner HTTP (session, events, attempt reconcile) without real Provider calls. CLI video dialogue commands are planned and must not be invented.
---

# Anatomia VLM-Codex Interaction

Maintainer skill. Default `anatomia skills list` hides it; `--all` may show it. Do not install this as a user product skill. Do not call a live Provider.

Inspect one session, then reconcile only the original persisted attempt:

```
GET /api/v1/interactions/{session_ref}
GET /api/v1/interactions/{session_ref}/events
POST /api/v1/interactions/{session_ref}/attempts/{attempt_ref}/reconcile
```

Send the original Idempotency-Key on reconcile. Server rejects identity/version drift. Product events are refs-only.

`anatomia video dialogue *` is planned and unpublished. Do not tell the user to run it. Commands: `references/commands.md`. Handoff: `references/handoff.md`.
