---
name: yeisme-mcp-gateway-maintainer
description: Use when changing, debugging, testing, archiving, deploying, releasing, or operating the Go MCP Gateway under mcp/gateway, including CLI/API behavior, upstream routing, credential distribution, audit safety, and gateway lifecycle.
---

# Yeisme MCP Gateway Maintainer

Use this skill for Gateway implementation and operations work. In the Yeisme
workspace the project lives at `mcp/gateway/`; in a standalone checkout, treat
the directory containing `go.mod` and this project's `AGENTS.md` as the root.

## Boundary

- CLI entrypoint lives in `cmd/mcp-gateway/`.
- Gateway HTTP/API implementation lives in `internal/gateway/`.
- Registry loading and validation lives in `internal/registry/`.
- Tests live beside the Go packages they cover.
- The registry schema source of truth is `registry.schema.json`; user runtime
  configuration defaults to `~/.mcp-gateway/registry.yaml`.
- Product, interface, runtime, deployment, observability, security, and
  long-lived implementation docs live in local `docs/**` and `openspec/**`.
  Root project-doc mirrors are not valid owners and must not be required for
  closeout.
- Do not put gateway implementation code in `.skills/imported/`.
- Do not add per-server Taskfiles for remote MCPs; prefer registry entries.
- Do not add Web UI, TUI, mobile, or frontend marketplace code to `mcp/gateway`; this project is CLI/API only.
- BigModel/Zai `web-search-prime` is intentionally disabled for 联网搜索.
  Preserve that policy; use the Firecrawl CLI from its owning backend checkout,
  resolved from the active workspace rather than a maintainer-specific absolute
  path, unless a separate plan explicitly introduces a Firecrawl MCP backend.
- Never commit or print real Gateway tokens, upstream provider keys, signing
  keys, `Authorization` headers, or release-distribution tokens.

## Workflow

1. Read the closest existing files before designing:
   - `AGENTS.md`
   - `README.md`
   - `go.mod`
   - changed files under `cmd/` or `internal/`
   - relevant package tests
2. Preserve the current architecture:
   - registry-driven config
   - one public `/mcp` gateway endpoint
   - Streamable HTTP and supervised stdio backends share namespace, exposure,
     policy, budget, audit, and lifecycle boundaries
   - compact CLI output by default, JSON when requested
   - CLI output changes must also follow `ai-native-cli-output-contract`
3. For deployment or release work, also read `Dockerfile`, `Taskfile.yml`,
   `.goreleaser.yml`, `.github/workflows/release.yml`, and
   `docs/deployment-and-key-distribution.md`.
4. Keep credential roles separate:
   - upstream provider keys stay on the Gateway host in its secret manager or
     referenced environment file; clients never receive them
   - the quickstart operator token is an operator credential, not a consumer
     sharing token
   - use `mcp-gateway grant create` for a bounded human or agent-worker tool
     subset, and `mcp-gateway tokens create` for service accounts that need
     explicit scopes
   - keep generated credentials in `0600` files, transfer them through an
     approved secret channel, and pair every issue path with revoke/rotation
5. Keep failure boundaries isolated. A failed backend must not break unrelated backends.
6. Keep audit output compact and secret-safe. Do not log full tokens, headers, large payloads, complete tool outputs, raw prompts, or full chain-of-thought.
7. Update tests near changed behavior. Update `CHANGELOG.md` and the local docs
   index when a user-facing command, deployment path, or credential contract
   changes.
8. When asked to archive completed Gateway specifications, use
   `openspec archive -y <change-name>` and validate the resulting main spec;
   do not hand-move OpenSpec state files.

## Validation

Run the narrowest useful checks, then broaden if shared behavior changed:

```bash
cd mcp/gateway
task fmt-check
task lint-new
task test
task build
task validate
task status
openspec validate --all --strict
```

For deployment, release, or credential changes:

```bash
./dist/mcp-gateway --help
./dist/mcp-gateway release check --registry ~/.mcp-gateway/registry.yaml --json
goreleaser check
goreleaser release --snapshot --clean
```

For a local credential smoke path, use disposable data and credential
directories; never print or commit the token file contents. If a command cannot
run because services, credentials, GoReleaser, or another optional tool is
missing, report that explicitly and include the next runnable command.
