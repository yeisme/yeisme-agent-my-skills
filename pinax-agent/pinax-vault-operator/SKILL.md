---
name: pinax-vault-operator
description: Use when an agent needs to initialize, register, select, inspect, write, create, save, capture, or import notes into a Pinax vault; append journal or inbox content; snapshot, repair-plan, organize-plan, or safely mutate a Pinax vault through real Pinax commands.
---

# Pinax Vault Operator

Operate the local Pinax Markdown vault safely. Use this for vault setup, default selection, note capture, health checks, snapshots, and plan-first maintenance.

## Intake Index Rule

Agent-authored notes must enter the unified intake index before later classification. Unless the user explicitly names a final target directory or an approved `pinax organize plan` selects one, create generated or imported notes under `notes/index/` with `--dir index`. Never create agent-generated notes in the vault root, and never guess a topic folder from the title.

## Use When

- The task asks to add, write, create, save, or import Pinax notes; capture inbox items; append journal entries; or organize vault content.
- The user asks for a `Pinax note`, `Pinax 笔记`, `保存到 Pinax`, `写入 vault`, or similar storage-backed note operation.
- The user wants a default/global vault, vault alias, validation, stats, doctor, snapshot, repair, or organize workflow.
- A write command touches vault Markdown or `.pinax/**` metadata.

## Command Patterns

```bash
pinax vault list --json
pinax config get vault --json
pinax vault register ./my-notes --name work --default
pinax note add "Title" --dir index --body "Content" --json
pinax note add "AI workflow monetization" --dir index --stdin --json
pinax inbox capture "Temporary idea" --json
pinax inbox capture "AI workflow monetization" --stdin --json
pinax journal daily append --body "Today I learned..." --json
pinax vault doctor --json
pinax repair plan --save --json
pinax organize plan --save --json
pinax version snapshot --message "before maintenance" --json
```

## Workflow

1. Resolve the vault first: `pinax vault list --json`; only use `--vault` when overriding the configured default.
2. If the user asked for a Pinax note but did not explicitly approve a vault write, provide the note body as a draft and show the exact `pinax note add ... --dir index --stdin --json` command.
3. For direct note creation, prefer `pinax note add --dir index` or `pinax inbox capture`; use `--stdin` for long generated bodies and do not write Markdown files directly unless the user explicitly wants prose file editing.
4. For maintenance, run `pinax vault doctor --json`, then plan commands before apply commands.
5. Before apply commands or broad note moves, run `pinax version snapshot --message "before agent changes" --json`.
6. Use `--json` for automation and parse the `status`, `facts`, `actions`, and `error` fields.
7. Stop before destructive commands unless the user explicitly approved the matching `--yes` action.

## Safety Boundaries

- Do not hand-edit `.pinax/config.yaml`, `.pinax/events.jsonl`, receipts, indexes, registry files, or SQLite stores.
- Do not create root-level Markdown notes with bare `pinax note add` for agent-generated content.
- Do not place generated notes directly in topic folders unless the target is user-specified or selected by an approved organize plan.
- Do not apply repair or organize plans without checking the saved plan and approval requirement.
- Do not include secrets, provider payloads, raw prompts, or hidden prompts in notes or evidence.
- Treat Markdown body content as user-owned; preserve language and intent.
- Keep generated prose bodies free of secrets, raw prompts, provider payloads, hidden prompts, and full chain-of-thought before capture.

## Validation

- After setup: `pinax vault validate --json`.
- After capture: `pinax search "<title or keyword>" --json` or `pinax note list --json`, and confirm unclassified generated notes have paths beginning with `notes/index/`.
- After plan generation: confirm the command returned `status=success` and a saved plan path.
