---
name: pinax-vault-operator
description: Use when an agent needs to initialize, register, select, inspect, write, create, save, capture, import, export, draft, inbox, journal, or ordinary note lifecycle operations in a Pinax vault through real Pinax commands.
---

# Pinax Vault Operator

Operate the local Pinax Markdown vault safely. Use this for vault setup, default selection, note capture, inbox/journal/draft workflows, import/export, and ordinary note lifecycle operations. Route high-risk maintenance apply, restore, proof-loop, or record-ledger work to `pinax-proof-maintenance-operator`.

## Intake Index Rule

Agent-authored notes must enter the unified intake index before later classification. Unless the user explicitly names a final target directory or an approved `pinax organize plan` selects one, create generated or imported notes under `notes/index/` with `--dir index`. Never create agent-generated notes in the vault root, and never guess a topic folder from the title.

## Use When

- The task asks to add, write, create, save, or import Pinax notes; capture inbox items; create or manage drafts; append journal entries; or export Markdown.
- The user asks for a `Pinax note`, `Pinax 笔记`, `保存到 Pinax`, `写入 vault`, or similar storage-backed note operation.
- The user wants a default/global vault, vault alias, validation, stats, dashboard, or local vault selector.
- The command family is `pinax init`, `pinax vault`, `pinax note`, `pinax inbox`, `pinax journal`, `pinax draft`, `pinax import`, or `pinax export`, excluding high-risk maintenance apply.

## Command Patterns

```bash
pinax vault list --json
pinax config get vault --json
pinax vault register ./my-notes --name work --default
pinax init ./my-notes --title "My Notes" --json
pinax note add "Title" --dir index --body "Content" --json
pinax note add "AI workflow monetization" --dir index --stdin --json
pinax note list --recent --limit 20 --json
pinax note show "Research Log" --view rendered --json
pinax note move "Research Log" archive --json
pinax note archive "Research Log" --json
pinax inbox capture "Temporary idea" --stdin --json
pinax inbox index preview --json
pinax draft create "Draft title" --stdin --json
pinax draft index preview --json
pinax journal daily append --body "Today I learned..." --json
pinax import markdown ./incoming --dir index --json
pinax export markdown --tag research --to ./export --json
pinax vault validate --json
pinax vault stats --json
```

## Workflow

1. Resolve the vault first: `pinax vault list --json`; only use `--vault` when overriding the configured default.
2. If the user asked for a Pinax note but did not explicitly approve a vault write, provide the note body as a draft and show the exact `pinax note add ... --dir index --stdin --json` command.
3. For direct note creation, prefer `pinax note add --dir index` or `pinax inbox capture`; use `--stdin` for long generated bodies and do not write Markdown files directly unless the user explicitly wants prose file editing.
4. For inbox/draft review pages, use `pinax inbox index preview|create|refresh` or `pinax draft index preview|create|refresh`; do not hand-edit managed index pages.
5. For ordinary single-note maintenance, use `pinax note move`, `pinax note archive`, `pinax note rename`, `pinax note tag`, or `pinax note property` instead of editing frontmatter by hand.
6. Stop and route to `pinax-proof-maintenance-operator` before `metadata apply`, `repair apply`, `organize apply`, `version restore`, broad note moves, or destructive operations that need snapshot/approval gates.
7. Use `--json` for automation and parse the `status`, `facts`, `actions`, and `error` fields.

## Safety Boundaries

- Do not hand-edit `.pinax/config.yaml`, `.pinax/events.jsonl`, receipts, indexes, registry files, or SQLite stores.
- Do not create root-level Markdown notes with bare `pinax note add` for agent-generated content.
- Do not place generated notes directly in topic folders unless the target is user-specified or selected by an approved organize plan.
- Do not apply repair or organize plans from this operator; route to `pinax-proof-maintenance-operator`.
- Do not include secrets, provider payloads, raw prompts, hidden prompts, or full chain-of-thought in notes or evidence.
- Treat Markdown body content as user-owned; preserve language and intent.

## Validation

- After setup: `pinax vault validate --json`.
- After capture: `pinax search "<title or keyword>" --json` or `pinax note list --json`, and confirm unclassified generated notes have paths beginning with `notes/index/`.
- After inbox/draft index changes: `pinax inbox index preview --json` or `pinax draft index preview --json`.
