---
name: pinax-update
description: Use when the user asks for /pinax-update, to pull latest Pinax notes, validate the vault, refresh indexes, and automatically resolve safe Cloud Sync conflicts using a negotiated strategy.
---

# Pinax Update

Run a safe one-command update for the Yeisme Pinax notes vault. This skill is for requests such as `/pinax-update`, `拉取最新笔记并自动处理冲突`, `同步笔记`, or `自动修复 Pinax sync 冲突`.

## Default Command

```bash
bash .agents/skills/pinax-update/scripts/pinax-update.sh --vault /workspaces/yeisme-agent/data/yeisme-notes --strategy auto
```

Use the runtime copy under `.agents/skills/` when working inside the vault. If the runtime copy is missing, use the source script under `/workspaces/yeisme-agent/.skills/yeisme/pinax-agent/pinax-update/scripts/`.

## Strategy Negotiation

- `auto` is the default for `/pinax-update`: resolve only safe config/runtime conflicts with `--keep-local`; stop for note-body conflicts.
- `keep-local`: use only when the user explicitly says local/GitHub/current workspace wins.
- `keep-remote`: use only when the user explicitly says cloud/remote wins.
- `manual`: inspect and report conflicts without resolving.

Safe auto-resolvable conflicts are limited to root vault docs, `.agents/skills/**`, `.claude/skills/**`, `.gitignore`, and `.pinaxignore`. Conflicts under `notes/`, `daily/`, `inbox/`, `drafts/`, `journal/`, `assets/`, or unknown paths require user confirmation.

## Workflow

1. Run the default command with `--strategy auto` unless the user names another strategy.
2. If the command exits with code `2`, report the unsafe conflicts and ask which strategy to use: keep local, keep remote, or manual merge.
3. If safe conflicts were resolved, validate that `conflicts=0`, `vault.validate` succeeded, and index refresh succeeded.
4. Do not claim remote push success unless a later Pinax command reports `remote_write=true`.

## Boundaries

- Do not edit `.pinax/**` by hand.
- Do not expose credentials, provider payloads, Authorization headers, cookies, or token values.
- Do not resolve note-body conflicts automatically under `auto`.
- Do not use `pinax backend pull/push` as a substitute for Cloud Sync.
