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

- `export` writes the central value into the target owner's user config and removes the legacy ref after a successful atomic write.
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

