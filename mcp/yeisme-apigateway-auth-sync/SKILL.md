---
name: yeisme-apigateway-auth-sync
description: Use when changing, debugging, testing, or reviewing apigateway authentication sync sidecars for Codex or Gemini CLI channels, including Taskfile tasks, compose wiring, env defaults, model lists, and new-api channel behavior.
---

# Yeisme Apigateway Auth Sync

Use this skill for the `apigateway/` auth synchronization sidecars and related gateway channel behavior.

OpenCode Zen / Go is now handled as direct `new-api` channel types, not by an auth sync sidecar.

## Boundary

- Sync scripts live in `apigateway/scripts/*_auth_sync.py`.
- Sidecar Dockerfiles live in `apigateway/Dockerfile.*-auth-sync`.
- Runtime wiring lives in `apigateway/api-gateway.compose.yml` and `apigateway/Taskfile.yml`.
- Channel defaults live in `apigateway/new-api.env`.
- Source credential directories are `apigateway/codex-auth/` and `apigateway/gemini-auth/`.
- Do not commit new real credentials. Keep examples templated or documented.

## Workflow

1. Identify the provider: Codex or Gemini CLI.
2. Read the provider README section in `apigateway/README.md` and the matching script before editing.
3. Preserve managed-channel safety:
   - update channels owned by the matching managed tag
   - do not overwrite manually detached channels
   - avoid changing names, groups, tags, remarks, proxy, or test model outside the managed contract
4. Keep file normalization deterministic:
   - Codex: `auth.json.<email>`
   - Gemini CLI: `oauth_creds.json.<email>`
5. If script, Dockerfile, requirements, compose, or env inputs change, ensure the Taskfile hash/rebuild logic still includes the changed input.
6. Keep user-facing logs and docs in English unless the user explicitly requests another language for that artifact.

## Validation

Run provider-specific tests first:

```bash
cd apigateway
python3 -m pytest scripts/test_codex_auth_sync.py
python3 -m pytest scripts/test_gemini_auth_sync.py
```

Then run provider smoke commands as applicable:

```bash
task new-api:config
task new-api:codex-sync
task new-api:gemini-sync
task new-api:health
```

If Docker, `nerdctl`, credentials, or the private gateway are unavailable, report the blocked command and the reason.
