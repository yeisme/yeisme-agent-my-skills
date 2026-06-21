---
name: yeisme-pinax-cli-runtime
description: Use when changing, testing, reviewing, documenting, or operating Pinax under cli/pinax, including local knowledge indexing, profile management, publish/sync workflows, backend client behavior, and Go CLI validation.
---

# Yeisme Pinax CLI Runtime

Use this skill for `cli/pinax`, the local-first knowledge/vault CLI, agent-safe proof loop, local index projection, and Cloud Sync client.

## Boundary

- Pinax owns local vault/index workflows, profile management, publish/sync behavior, backend client integration, and run evidence.
- Credentials must live in user-level config or secret stores, never repository files, fixtures, docs, logs, or evidence.
- Structured project assets must be mutated through Pinax commands or app services, not hand-written by agents.
- Human development docs default to Chinese, while CLI help, CLI output, logs, errors, automation examples, schema fields, flags, and protocol keys remain English or existing stable names.

## Workflow

1. Enter `cli/pinax` before concrete implementation.
2. Read local `AGENTS.md` and use Pinax OpenSpec changes for behavior changes.
3. Preserve Go CLI output contracts and redaction across default human output, `--agent`, `--json`, `--events`, `--explain`, and automation surfaces.
4. Keep backend API, Cloud Sync, provider, storage, and vault writes behind Pinax app service/client boundaries.
5. Treat `.agents/skills/` and `.claude/skills/` under `cli/pinax` as generated runtime copies. Update `.skills/yeisme/` source and profile files, then sync.

## Validation

```bash
cd cli/pinax
task check
```

If `task` is unavailable, run the equivalent local gate:

```bash
golangci-lint fmt --diff
golangci-lint run
go test ./...
go build -trimpath -ldflags="-s -w" -o dist/pinax ./cmd/pinax
openspec validate --all
```
