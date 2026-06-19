---
name: yeisme-taskbridge-cli-runtime
description: Use when changing, testing, reviewing, documenting, releasing, or maintaining TaskBridge under cli/taskbridge, including task control-plane commands, project planning, sync diff/audit, action files, command docs, Agent JSON contracts, provider sync, Homebrew/Scoop release checks, and Go CLI quality gates.
---

# Yeisme TaskBridge CLI Runtime

Use this skill for `cli/taskbridge`, the Go CLI that bridges local task control-plane workflows with multiple Todo providers and Agent-safe automation.

For detailed maintenance lanes, read `references/taskbridge-maintenance.md` when the task touches generated command docs, OpenSpec/spec reconciliation, sync/action-file execution, provider writes, release packaging, Homebrew/Scoop distribution, or post-release smoke failures.

## Boundary

- CLI entrypoint: `cli/taskbridge/main.go`.
- Commands live in `cli/taskbridge/cmd/`.
- Core task model and storage live in `cli/taskbridge/internal/model` and `cli/taskbridge/internal/storage`.
- Control-plane behavior lives in `internal/controlplane`, `internal/actionfile`, `internal/syncaudit`, `internal/projectservice`, and `internal/agentcontract`.
- Provider adapters live in `internal/provider/*`; never bypass provider interfaces for remote writes.
- Generated command docs live under `docs/commands/**`; regenerate them through the project command or Taskfile if available, and do not hand-edit generated command reference drift unless the generator is missing.
- Release behavior is owned by `.goreleaser.yaml`, `.github/workflows/**`, `internal/releasecontract`, and `docs/release-*.md`; package-manager distribution must stay consistent with `golang-goreleaser-distribution`.

## Workflow

1. Start inside `cli/taskbridge` and read `AGENTS.md`, the command file, and the owning `internal/` package before editing.
2. Preserve TaskBridge product semantics:
   - `today`, `next`, `inbox`, `review`, and `sync diff` are safe read/preview surfaces.
   - `agent *` stdout must remain valid `taskbridge.agent-result.v1` JSON.
   - new general CLI output surfaces must follow `ai-native-cli-output-contract`: concise human summaries by default, strict machine JSON, stable agent mode, NDJSON events for streams, and no logs mixed into machine stdout.
   - dangerous actions require `--confirm` or an action-file confirmation gate.
   - `--dry-run` must not mutate local storage or call remote write APIs.
   - sync/audit output must describe what was compared or written, not just that a command ran.
3. Keep local project docs and OpenSpec artifacts in Chinese by default. Keep CLI help, text output, and user-facing errors in English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
4. Treat generated artifacts as contracts:
   - command docs must match the current Cobra command surface;
   - JSON, `--agent`, and `--events` shapes must be tested at the renderer or command boundary;
   - release distribution changes need `internal/releasecontract` coverage before workflow edits.
5. Add tests close to the behavior:
   - command wiring and envelope behavior in `cmd/`
   - control-plane classification in `internal/controlplane`
   - action-file execution in `internal/actionfile`
   - sync diff/audit semantics in `internal/syncaudit`
   - project lifecycle behavior in `internal/projectservice`
6. For integration checks, build a temporary binary and run it against a temporary `--storage-path`; parse JSON outputs with `node` or Go rather than relying on text matching.

## Release And Distribution

- Use `golang-github-release-guardrails` for CI/tag/release gates and `golang-goreleaser-distribution` for Homebrew cask, Scoop, nFPM, SBOM, publisher-token, and post-release install smoke policy.
- Do not reuse a public semver tag after a failed release. Publish a forward patch tag instead.
- If GitHub Actions fails after local `task release:local` passes, inspect the failed step logs before editing; common remote-only gaps include missing runner tools, package-manager trust policy, and publisher-token scope.

## Validation

Run the focused gate after code changes:

```bash
cd cli/taskbridge
go test ./cmd ./internal/actionfile ./internal/controlplane ./internal/syncaudit ./internal/projectservice
go build ./...
```

Run a smoke integration sequence when command behavior changes:

```bash
cd cli/taskbridge
tmp=$(mktemp -d)
go build -o "$tmp/taskbridge" .
"$tmp/taskbridge" --storage-path "$tmp/storage" doctor --format json
"$tmp/taskbridge" --storage-path "$tmp/storage" demo today --format json
"$tmp/taskbridge" --storage-path "$tmp/storage" agent plan "学习 OpenClaw" --dry-run=false
```

`go test ./...` is desirable before release, but if it hangs in unrelated provider/loader paths, record the package and keep the focused gate plus smoke evidence.

For release or distribution changes, also run:

```bash
cd cli/taskbridge
task test:integration
task release:check
task release:local
```

After changing skills, profiles, or generated runtime copies from the repository root, validate the source and the affected target:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
go run ./cli/skillctl/cmd/skillctl --root . sync cli/taskbridge --agent-home all --yes
scripts/skills.sh validate-subprojects-runtime
```
