---
name: pinax-integration-publish-operator
description: Use when an agent needs to operate Pinax publish, plugin, local API, API token, backend profile alias, MCP, or briefing workflows with read-only defaults, credential safety, and explicit approval for integration writes.
---

# Pinax Integration Publish Operator

Operate Pinax integration surfaces: static publish, plugins, local REST/RPC API, API tokens, backend connection profiles, MCP, and briefing. Start read-only, keep credential values out of output, and require approval before exposing services or writing integration state.

## Use When

- The request mentions `pinax publish`, GitHub Pages/Wiki output, `pinax plugin`, `pinax api`, `pinax token`, `pinax profile`, `pinax mcp`, or `pinax briefing`.
- The user wants a local API server, MCP surface, plugin validation/install/run, static publish preview/deploy, daily briefing, API token, or backend profile alias.
- The task involves integration boundaries rather than ordinary note capture, retrieval, or sync.

## Command Patterns

```bash
pinax publish plan --vault ./my-notes --json
pinax publish profile init public --target github-pages --renderer hugo --vault ./my-notes --json
pinax publish build --profile public --vault ./my-notes --json
pinax publish doctor --profile public --vault ./my-notes --json
pinax publish serve public --vault ./my-notes
pinax plugin validate ./plugins/project-dashboard --vault ./my-notes --json
pinax plugin doctor --vault ./my-notes --json
pinax plugin list --vault ./my-notes --json
pinax plugin install ./plugins/project-dashboard --vault ./my-notes --json
pinax plugin permissions grant project-dashboard projection.read --capability render_dashboard --vault ./my-notes --yes --json
pinax plugin run project-dashboard render_dashboard --vault ./my-notes --dry-run --json
pinax api routes --vault ./my-notes --json
pinax api schema export --format openapi --vault ./my-notes --json
pinax api serve --vault ./my-notes --readonly --port 8787
pinax token create --label local-agent --scope read --expires 30d --vault ./my-notes --json
pinax token list --vault ./my-notes --json
pinax token revoke tok_123 --vault ./my-notes --json
pinax profile add local --endpoint http://127.0.0.1:8787 --workspace default --device laptop --secret-ref env://PINAX_API_TOKEN --vault ./my-notes --json
pinax profile list --vault ./my-notes --json
pinax mcp serve --vault ./my-notes
pinax briefing run --dry-run --vault ./my-notes --json
```

## Workflow

1. Start with read-only checks: `pinax publish plan`, `pinax plugin validate|doctor|list`, `pinax api routes`, `pinax api schema export`, `pinax token list`, `pinax profile list`, or `pinax briefing` preview/status commands.
2. For publish, run `publish plan` and `publish doctor` before `build`, `serve`, or `deploy`. Static publish outputs are delivery artifacts, not the vault source of truth.
3. For plugins, validate and inspect before install; install disabled first when supported; grant permissions explicitly; run only enabled capabilities with approved permissions.
4. For API, prefer `pinax api serve --readonly` on loopback. Use `--allow-write` only after the user understands the remote mutation boundary.
5. For tokens, show only token ids, labels, scopes, expiry, and redacted digests. If a command prints a one-time token secret, do not store it in repo files, docs, logs, or notes.
6. For profiles, store endpoint, workspace, device, scope, and secret refs only. Do not store raw token values.
7. For MCP, keep the surface read-only unless the Pinax command and user approval explicitly enable controlled writes.

## Safety Boundaries

- Do not expose raw API tokens, plugin secrets, webhook URLs, Authorization headers, cookies, provider payloads, hidden prompts, or full chain-of-thought.
- Do not hand-edit publish profiles, plugin registries, permission grants, token stores, profile metadata, briefing receipts, or MCP state.
- Do not bind API/MCP servers beyond loopback unless the user explicitly requests and approves it.
- Do not confuse Remote API Mode (`pinax api serve`, `--api-url`, profiles/tokens) with Cloud Sync (`pinax cloud`, `pinax sync`).
- Do not deploy publish output or enable plugin writes without explicit approval.

## Validation

- Publish: `pinax publish doctor <profile> --json` after profile or build changes.
- Plugin: `pinax plugin doctor --json` and `pinax plugin inspect <id> --json` after install/permission changes.
- API: `pinax api routes --json` and `pinax api schema export --format openapi --json` before exposing clients.
- Token/profile: `pinax token list --json` or `pinax profile show <name> --json` must not reveal raw secrets.
