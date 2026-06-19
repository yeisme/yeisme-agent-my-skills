# TaskBridge Maintenance Lanes

Use this reference after loading `yeisme-taskbridge-cli-runtime` when the task is broader than a single command edit.

## Command Surface And Docs

- Keep Cobra command entrypoints in `cmd/`; move behavior into `internal/` packages.
- Prefer generated command docs under `docs/commands/**`. If docs drift, find and run the project generator or Taskfile command first; update the generator before hand-editing repeated command pages.
- Help text, command names, flags, schema keys, examples, and CLI output remain English. Local implementation notes, OpenSpec artifacts, and non-public project docs may be Chinese by repository policy.
- New or changed flags must follow the long-flag-first rule from `golang-cobra-viper-cli-architecture` and `ai-native-cli-output-contract`.

## Control Plane, Action Files, And Sync

- Read surfaces such as `today`, `next`, `inbox`, `review`, and `sync diff` must stay preview-safe.
- Dangerous writes need `--confirm` or action-file confirmation. Do not silently delete, bulk-complete, reschedule, overwrite remote data, or discard conflicts.
- `--dry-run` must not write local storage or call remote write APIs.
- Agent and MCP adapters must not read or write `~/.taskbridge` files directly; use services/stores through the CLI/runtime boundary.
- Remote Todo writes must go through provider interfaces in `internal/provider/*`; never bypass a provider adapter for convenience.

## Output Contracts

- `agent *` stdout must remain valid `taskbridge.agent-result.v1` JSON.
- JSON mode writes machine JSON only to stdout; diagnostics, logs, prompts, and progress go to stderr.
- Default human output can summarize, but `--json`, `--agent`, and `--events` need stable projection structs and focused contract tests.
- Removing, renaming, or retyping released fields, enum values, agent keys, events, command names, or config keys is a generation-breaking change. Gate it through `yeisme-evolutionary-change-policy` and an OpenSpec change.

## Persistence And Evidence

- Local file persistence should reuse existing store patterns and `internal/persistence/atomicjson.go` for atomic writes.
- Integration/process tests should write redacted evidence under `temp/integration-test-runs/<run-id>/` when the Taskfile path exists.
- Do not commit `dist/`, `temp/`, local stores, provider credentials, or generated run evidence.

## Release And Package Managers

- Release config is covered by `.goreleaser.yaml`, `.github/workflows/release.yml`, `.github/workflows/post-release.yml`, `internal/releasecontract`, and `docs/release-*.md`.
- Homebrew distribution is a cask in `yeisme/homebrew-tap/Casks/taskbridge.rb`; Scoop distribution is `yeisme/scoop-bucket/bucket/taskbridge.json`.
- Release workflows must install any runner tools needed by GoReleaser, including Syft when SBOM cataloging is enabled.
- Post-release Homebrew cask smoke must trust `yeisme/tap` before installing from the tap because Homebrew tap trust is enforced on modern runners.
- Do not reuse a pushed semver tag after a failed public release attempt; fix forward with the next patch tag.

## Verification Matrix

Use the smallest gate that proves the touched surface, then broaden before release:

```bash
cd cli/taskbridge
go test ./cmd ./internal/actionfile ./internal/controlplane ./internal/syncaudit ./internal/projectservice
go build ./...
```

For output, docs, process, or release behavior:

```bash
cd cli/taskbridge
task test
task test:integration
task build
task release:check
task release:local
task check
```

For skill/profile/source changes from repository root:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
go run ./cli/skillctl/cmd/skillctl --root . sync cli/taskbridge --agent-home all --yes
scripts/skills.sh validate-subprojects-runtime
```
