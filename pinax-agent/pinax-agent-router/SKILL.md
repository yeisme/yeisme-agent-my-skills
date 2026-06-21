---
name: pinax-agent-router
description: Use when an agent needs to operate Pinax for local-first notes, including requests to write, create, save, capture, or import a Pinax note; retrieve or recall vault knowledge; maintain a vault; sync, store, or publish Pinax content; and route to the narrowest Pinax operator skill before running commands.
---

# Pinax Agent Router

Route Pinax user-agent work to the smallest suitable Pinax operator skill. Root sessions normally keep only this router active; load the specific Pinax operator only after classifying the task.

## Use When

- A user or agent wants to add, write, save, capture, search, organize, recall, sync, publish, or diagnose Pinax knowledge.
- The request says or implies `Pinax note`, `Pinax 笔记`, `保存到 Pinax`, `收进 vault`, `写入 vault`, or `capture this in Pinax`.
- The task is operational use of `pinax`, not Go code changes under `cli/pinax`.
- The request mentions default vaults, notes, inbox, journal, search, KB, memory, Cloud Sync, S3/COS, backend profiles, snapshots, repair, or organize.

For Pinax code implementation, use `yeisme-pinax-cli-runtime` plus the normal coding skills instead.

## Route Table

| User goal | Skill to load | First commands |
| --- | --- | --- |
| Set up or select a vault, write/capture Pinax notes, inspect health, snapshot before writes | `pinax-vault-operator` | `pinax vault list --json`, `pinax note add ... --stdin --json`, `pinax vault doctor --json` |
| Search notes, refresh indexes, use KB context, query structured note data | `pinax-retrieval-operator` | `pinax index refresh --json`, `pinax search "..." --agent`, `pinax kb context "..." --json` |
| Store or recall durable facts, decisions, events, and tasks for agents | `pinax-memory-operator` | `pinax memory context "..." --agent`, `pinax memory capture ... --json` |
| Configure Cloud Sync, S3/COS, storage, backend profiles, or sync runs | `pinax-sync-storage-operator` | `pinax cloud status --json`, `pinax storage status --json`, `pinax sync diff --target cloud --json` |
| Publish docs, GitHub Pages, GitHub Wiki, or prompt assets | Start with `pinax-vault-operator`; if code or release behavior changes, switch to `yeisme-pinax-cli-runtime` | `pinax publish plan --json`, `pinax prompt list --json` |

## Workflow

1. Classify the word `note`: if the user only asks for an article, social post, or prose note without Pinax/vault language, write content normally; if they mention Pinax or vault storage, route here.
2. Confirm the active vault without writing: `pinax vault list --json` and, if needed, `pinax config get vault --json`.
3. Pick one operator skill from the route table.
4. Load only the chosen operator skill from the runtime profile or `.skills/yeisme/pinax-agent/<skill>/SKILL.md`; do not bulk-load all Pinax skills.
5. Prefer `--json` for structured automation and `--agent` for low-token context.
6. For note writes, draft the body first when useful, then use `pinax note add "<title>" --stdin --json` or `pinax inbox capture "<title>" --stdin --json` instead of hand-writing Markdown files.
7. For writes, use `--dry-run` or plan commands first when available.
8. Before high-risk local changes, create a snapshot with `pinax version snapshot --message "before agent changes" --json`.
9. Never edit `.pinax/**`, SQLite files, receipts, sync state, backend registries, or cloud config by hand.

## Boundaries

- Pinax vault Markdown notes are user content. Preserve the user's language and do not rewrite unrelated notes.
- Structured assets are CLI-authored. Use Pinax commands for `.pinax/**` changes.
- Do not print, save, or infer raw credentials. Refer to credential profiles or secret refs only.
- Cloud Sync and Remote API Mode are different workflows; do not mix them unless the user explicitly asks.

## Validation

- A routed answer names the selected operator skill and why.
- Commands shown to the user are real `pinax` commands.
- The router does not directly perform broad content edits when a narrower operator skill applies.
