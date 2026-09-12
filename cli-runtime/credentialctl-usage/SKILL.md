---
name: credentialctl-usage
description: Use when installing, operating, integrating, diagnosing, or releasing credentialctl for file-first user credentials, inline target copies, bindings, storage migration, repository project secrets, machine output, Homebrew, or Agent Skill setup.
---

# Credentialctl usage

Use this skill for the local single-user `credentialctl` trust boundaries. It never authorizes printing, logging, returning, or committing a secret.

## Choose the flow

- Install the CLI through the verified `yeisme-dist` Homebrew cask or installer.
- Use `setup`, `set`, `rotate`, `status`, `doctor`, `enable`, and `disable` for the central user credential.
- Use `export`, `import`, `sync`, `binding`, `migrate local-tools`, `storage`, `cleanup`, and `purge` for owner-managed inline user-config copies.
- Use `project init`, `project secret`, `project unlock`, `project rekey`, and `project exec` only for encrypted repository project secrets.
- Do not use credentialctl as a remote vault, browser credential broker, OAuth refresh-token manager, or provider revoke API.

## Install and update

```bash
brew tap yeisme/dist https://github.com/yeisme/yeisme-dist
brew install --cask yeisme/dist/credentialctl
credentialctl --version
```

Install this Skill from the public Yeisme collection:

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill credentialctl-usage --yes
```

Update later with:

```bash
brew update
brew upgrade --cask yeisme/dist/credentialctl
npx --yes skills update credentialctl-usage --yes
```

## Central credential workflow

```bash
credentialctl setup openai/personal-default --preset local-ai --json
credentialctl status openai/personal-default --json
credentialctl rotate openai/personal-default --json
credentialctl doctor openai/personal-default --json
```

- Human input should use the hidden TTY prompt. Automation may pipe one value through stdin.
- Normal storage is one user-level `0600` file per ref. Do not hand-edit secret files or `bindings.json`.
- `setup` is create-if-absent. Use `rotate` for an existing ref.
- Add `--probe` to `doctor` only when a provider network request is explicitly intended.

Local single-user default is an inline key in the owner user config (`api_key`, file mode 0600). credentialctl is the shared store and rotation plane; `export` copies into that same slot. Do not tell the user to keep both `api_key` and `api_key_env`. Process environment is CI/temporary override only when the slot is empty. Cross-project contract: `openspec/changes/local-credential-single-slot-v1/`.

## Discover without reading (purpose metadata)

Every credential can carry secret-free metadata — `note` (what the key is for), `tags`, `kind` (`api-key|mcp-server|remote-service|registry-token|other`), and `env_name`. Agents select credentials from this knowledge axis and never need the value:

```bash
credentialctl describe openai/personal-default \
  --note "company OpenAI relay key for chat and embedding" \
  --tag ai,prod --kind api-key --env-name OPENAI_API_KEY --json
credentialctl search "openai" --agent        # matches provider/account/note/tags/env_name
credentialctl search "" --kind mcp-server --json
credentialctl describe openai/personal-default --json   # view without mutating
```

- There is deliberately no `get`/`print` command; if you find yourself wanting the value, you want `export`/`sync` or a consumer resolver instead.
- Secrets are rejected in metadata (`METADATA_INVALID`); describe the purpose, never paste the key.
- `set`/`rotate` keep existing metadata; `--clear-note` removes a note.
- Lifecycle: every value mutation stamps `rotated_at`; set an expiry with `describe <ref> --expires <RFC3339>` (`--clear-expires` removes it) and `doctor` warns `expired`/`expiring` (within 30 days) locally.
- `search` results include `matched_on` plus the metadata, redacted in every output mode.

## Collect scattered keys (discover / import-config)

Keys already living in config files (`~/.env`, `~/.netrc`, `~/.aws/credentials`, gh `hosts.yml`, `.npmrc`, docker `config.json`, `.mcp.json` / `~/.claude.json` / `~/.cursor/mcp.json`) are collected centrally instead of being read raw:

```bash
credentialctl discover --json                       # scan well-known locations (read-only, redacted)
credentialctl discover --path ~/.env --format dotenv --json
credentialctl import-config ~/.env --format dotenv --key OPENAI_API_KEY --json
credentialctl import-config ~/.env --format dotenv --key OPENAI_API_KEY --dry-run --json
```

- Never `cat` a config file to find a key — run `discover` first; output carries only proposed refs, digests and provenance notes.
- `import-config` copies the value file→store in-process; it never prints, never writes temp files, and never modifies the source.
- Imports attach provenance automatically (tags `imported,<format>`, note citing path+key) — annotate further with `describe`.
- Re-import of the same value is `unchanged`; a different value needs `--replace-central --expected-revision <rev> --yes`.
- Sources must be regular non-world-writable files ≤1 MiB (`SOURCE_UNREADABLE`); malformed content fails closed (`SOURCE_FORMAT_INVALID`).

## Use without seeing (exec / render / sink)

Configure tools with a key WITHOUT ever reading its value. The value flows store→process or store→file in-process only:

```bash
credentialctl exec --env OPENAI_API_KEY=openai/main -- ./tool --flag   # env injection, shell-free
credentialctl exec openai/main -- ./tool --flag                       # uses the stored env_name
printf 'OPENAI_API_KEY={{credential:openai/main}}\n' \
  | credentialctl render --output ~/tools/.env --json                 # pipe template → 0600 sink
credentialctl render --output ~/tools/.env --dry-run --json
credentialctl sink list --json && credentialctl sink verify --json
```

- `exec`: argv after a literal `--`, no shell; same-named host env vars are dropped so the injection is authoritative; machine output modes are rejected (child owns stdout); the child's exit code propagates. Loader/shell-startup env names (`LD_PRELOAD`, `BASH_ENV`, …) are refused.
- `render`: single-pass `{{credential:<provider>/<account>}}` substitution; writes ONLY the mandatory `--output` path (0600, atomic); stdout is never a sink. Template caps: ≤256 KiB, ≤64 placeholders, ≤16 refs; malformed placeholders fail closed (`TEMPLATE_INVALID`).
- Sink safety rules refuse (with `SINK_REFUSED`): group/world-writable parents, `/tmp`-style areas, symlink path components, git worktrees (escape: `--allow-repo-sink --yes`, recorded) and execution-adjacent files (`~/.ssh`, shell startup, git config, terminal/editor rc). Every render is recorded in `sinks.json`; `sink verify` reports drift informationally; `sink remove` never deletes the file.
- Never `cat` the rendered sink back into the conversation — `sink verify` reports digests instead.

## Sync MCP server keys (mcp targets)

MCP client configs get keys through the same target machinery, with a builtin JSON writer (no owner CLI needed):

```bash
credentialctl export openai/main --to yeisme-target://mcp/claude-user/context7 \
  --env CONTEXT7_API_KEY --json
credentialctl export gateway/main --to yeisme-target://mcp/claude-project/fetch \
  --env FETCH_API_KEY --allow-repo-sink --yes --json   # repo-local .mcp.json needs the escape hatch
credentialctl import yeisme-target://mcp/cursor-user/brave-search --as mcp/brave --json
credentialctl sync mcp/brave --dry-run --json
```

- Clients: `claude-project` (`./.mcp.json`), `claude-user` (`~/.claude.json`), `cursor-user` (`~/.cursor/mcp.json`); slots: `env.<NAME>` (via `--env` or the stored `env_name`) or `headers.Authorization` (`--authorization`).
- The writer preserves unknown JSON fields, snapshots the previous file, writes 0600 atomically; interpreter-hijack env names (`NODE_OPTIONS`, `PYTHONPATH`, …) are refused.
- `claude-project` targets inside a git worktree need `--allow-repo-sink --yes` per invocation (repo-local secret is opt-in and recorded).
- `import` reads the existing slot in-process (discovery fallback when exactly one secret-looking slot exists) and records `env_name` on created entries.
- credentialctl itself never runs as an MCP server (recorded non-goal).

## Opt-in encrypted store (encrypted-file)

The default store stays plaintext 0600. Users who want at-rest encryption migrate explicitly:

```bash
credentialctl storage migrate openai/main --from file --to encrypted-file --yes --json \
  --unlock-file ~/.config/credentialctl.passphrase        # or --unlock-env / TTY prompt
credentialctl storage rollback openai/main --to file --yes --json
```

- After migration `<base>/envelope.json` exists (Argon2id fixed profile + wrapped DEK; per-ref AEAD bound to ref+revision+envelope digest).
- Unlock precedence: `--unlock-file` > `CREDENTIALCTL_UNLOCK_FILE` > `--unlock-env` > `--unlock keychain` (macOS/Windows Credential Manager item `credentialctl-store`) > TTY prompt (humans only). Machine flows without a source fail closed `UNLOCK_REQUIRED` (exit 4); wrong passphrase or missing keychain item is `UNLOCK_FAILED` (exit 4).
- One unlock/derivation per process; keys wiped at exit. `status`/`doctor` on a locked store still render (unavailable + unlock action); data-touching commands fail closed.
- On macOS the system Keychain is also a real explicit backend: `storage migrate <ref> --from file --to keychain --yes` (file stays the default authority; other platforms fail closed).
- Inline sync, exec, render and backup all work unchanged over an encrypted store (decrypt in-process).

## Inline target workflow

Target URIs have the fixed shape `yeisme-target://<tool>/<kind>/<slot...>`. Supported v1 owners are Eikona, Scaena, Sonora, and Inferrum.

```bash
credentialctl target list --json
credentialctl export openai/personal-default \
  --to yeisme-target://eikona/channel/openai --json
credentialctl sync openai/personal-default --dry-run --json
credentialctl sync openai/personal-default --json
credentialctl binding list --json
```

- `export` writes the central value into the target owner's single user-level `api_key` slot (0600 inline copy) and removes the legacy ref after a successful atomic write. Do not also write `api_key_env`.
- `import` asks the target owner to read its user-level inline or explicit named source and call `localstore.Manager.Import`; the value never crosses stdout, a temporary file, or a socket.
- `export` and `import` create a binding unless `--no-bind` is supplied.
- Target drift returns a conflict. Use `--force-target --yes` only after reviewing the target copy.
- Batch sync requires `--yes`. A sync pins its starting central revision and stops remaining targets if that revision changes.
- `binding remove` removes only the relationship. It does not delete the target copy.

## Migration, rollback, and deletion

```bash
credentialctl migrate local-tools --dry-run --json
credentialctl migrate local-tools --yes --json
credentialctl storage migrate openai/personal-default \
  --from keychain --to file --dry-run --json
credentialctl storage migrate openai/personal-default \
  --from keychain --to file --yes --json
credentialctl binding rollback <binding-id> --yes --json
credentialctl cleanup legacy --yes --json
credentialctl purge openai/personal-default --yes --json
```

- A pre-authority file/Keychain digest mismatch is `storage_conflict`; do not guess which value wins.
- After file authority is established, a retained different Keychain value is `legacy_stale`, not a reason to block file rotation.
- `purge` clears target copies first and deletes the central file only when every target succeeds.
- Local purge cannot revoke a provider key. Revoke or rotate it in the provider console separately.

## Go owner boundary

- Target-owner imports may use `pkg/credentials` and `pkg/localstore.Manager.Import`.
- Non-target Go owners continue to use the runtime resolver APIs.
- Never import `internal/store`, expose a resolver to browser/facade code, or persist `Resolution.Secret`.
- Wipe resolved bytes immediately after the provider operation.

## Machine output

- `--json`: one `spec_version=1.0` envelope with command data under `data`.
- `--agent`: single-line-safe `key=value`; it is not JSON.
- `--events`: ordered NDJSON with `type`, `seq`, `spec_version`, and `command`.
- `--explain`: redacted decision summary, never chain-of-thought.
- Diagnostics may contain refs, target URIs, revisions, states, and redacted digests only.

## Release checks

Before publishing credentialctl, run:

```bash
task ci
task test:race
task security
task release:check
task release:local VERSION=v0.3.0
task release:verify VERSION=v0.3.0
```

Require a clean GitHub Release, checksums, per-archive SPDX SBOMs, public-mirror sync, Homebrew cask generation, and an anonymous install smoke test before declaring the version available.

