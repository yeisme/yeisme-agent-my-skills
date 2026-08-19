---
name: pinax-agent-router
description: Use when an agent needs to operate Pinax for local-first notes, including requests to write, complete, draft, create, save, capture, import, search, organize, maintain, sync, publish, run proof loops, manage project workspaces, templates, assets, prompts, API/profile/token, plugin, or MCP workflows; route to the narrowest Pinax operator skill before running commands.
---

# Pinax Agent Router

Route Pinax user-agent work to the smallest suitable Pinax operator skill. Root sessions normally keep only this router active; load the specific Pinax operator only after classifying the task. For knowledge-note requests, do not satisfy the user by only printing a complete note in chat; route to Pinax capture unless the request is clearly a non-Pinax publishing draft.

## Intake Index Rule

Agent-authored Pinax notes are captured through the vault's unified intake index first. For newly generated, imported, or saved notes whose final taxonomy has not already been approved, the destination must be `notes/index/` via commands such as `pinax note add "Title" --dir index --stdin --json`. Do not use bare `pinax note add` for agent-generated notes, because it can create root-level notes. Do not place notes directly into topic folders such as `notes/tools/**`, `notes/research/**`, or `notes/media/**` unless the user explicitly named that target path or an approved organize plan selected it.

## Agent I/O Preference

Prefer form-style intake before writing to a vault. Convert loose user input into explicit fields such as `title`, `kind`, `source`, `summary`, `body`, `tags`, `privacy`, and `next_action`, then route to the narrowest Pinax command. For agent-facing reads, searches, status checks, and context gathering, prefer `--agent` for compact output. Use `--json` for writes, validation, sync results, plan/apply results, and structured error handling.

## Use When

- A user or agent wants to add, write, complete, draft, save, capture, import, search, organize, recall, sync, publish, diagnose, maintain, or integrate Pinax knowledge.
- The request says or implies `note`, `笔记`, `知识笔记`, `学习笔记`, `技术笔记`, `Pinax note`, `Pinax 笔记`, `保存到 Pinax`, `收进 vault`, `写入 vault`, or `capture this in Pinax`.
- The user asks in Chinese to complete, write, organize, polish, or turn material into a note, such as `帮我完成一篇笔记`, `写一篇笔记`, `整理成一篇笔记`, or `把这些内容做成笔记`, and no explicit non-Pinax publishing channel is named.
- The task is operational use of `pinax`, not Go code changes under `cli/pinax`.
- The request mentions any Pinax top-level command: `init`, `vault`, `record`, `project`, `journal`, `inbox`, `draft`, `note`, `import`, `export`, `template`, `view`, `folder`, `search`, `memory`, `query`, `dataview`, `database`, `metadata`, `repair`, `organize`, `proof`, `briefing`, `cloud`, `sync`, `plan`, `prompt`, `collection`, `publish`, `plugin`, `backend`, `mcp`, `api`, `token`, `profile`, `config`, `version`, `asset`, `storage`, `index`, or `graph`.

For Pinax code implementation, use `yeisme-pinax-cli-runtime` plus the normal coding skills instead.

## Route Table

| User goal or command family | Skill to load | First commands |
| --- | --- | --- |
| Set up/select a vault, write/complete/capture notes, inbox, journal, draft, import/export, ordinary note lifecycle | `pinax-vault-operator` | `pinax vault list --agent`, `pinax note add ... --dir index --stdin --json`, `pinax inbox capture ... --stdin --json` |
| Search notes, refresh indexes, links/backlinks/orphans, query/dataview/database/view/folder inspection | `pinax-retrieval-operator` | `pinax index refresh --json`, `pinax search "..." --agent`, `pinax note links "..." --agent` |
| Capture or recall durable facts, decisions, events, and tasks | `pinax-memory-operator` | `pinax memory context "..." --agent`, `pinax memory recall "..." --agent` |
| Capsa Sync, repository-encrypted S3/COS bootstrap, sync logs/conflicts, storage backend, S3/rclone fallback, backend object diagnostics | `pinax-sync-storage-operator` | `pinax sync status --agent`, `pinax sync repo doctor --json`, `pinax sync diff --target capsa --json` |
| Proof loop, doctor/stats, metadata/repair/organize apply, snapshot/restore, record ledger, high-risk maintenance | `pinax-proof-maintenance-operator` | `pinax proof loop run --json`, `pinax vault doctor --json`, `pinax version snapshot --message "before maintenance" --json` |
| Project workspace, learning packs, project board/items, personal daily/weekly/monthly plans, local planning action drafts | `pinax-project-workspace-operator` | `pinax project list --agent`, `pinax project board show <project> --agent`, `pinax plan daily --dry-run --json` |
| Templates, template-backed `note add`, index pages, inbox/draft review indexes, journal template workflows | `pinax-template-authoring-operator` | `pinax template recommend --intent "..." --agent`, `pinax template preview <name> --agent`, `pinax index page preview <name> --agent` |
| Assets, note attachments, prompt assets, content collections, prompt graph rebuild/query | `pinax-asset-prompt-operator` | `pinax asset list --agent`, `pinax prompt search "..." --agent`, `pinax graph query --kind technique --match "..." --agent` |
| Publish, plugin, local API, API token, backend profile aliases, MCP, briefing | `pinax-integration-publish-operator` | `pinax publish plan --agent`, `pinax plugin list --agent`, `pinax api routes --agent` |

## Workflow

1. Classify the word `note`: plain knowledge notes, learning notes, technical notes, meeting notes, reading notes, and prompts like `帮我完成一篇笔记` default to Pinax capture. If the user explicitly asks for an article, blog post, newsletter, Xiaohongshu note, social post, public publishing draft, or another named writing surface without Pinax/vault storage intent, route to the matching writing skill or answer normally.
2. Confirm the active vault without writing: `pinax vault list --agent` and, if needed, `pinax config get vault --json`.
3. Pick one operator skill from the route table; if more than one applies, start with the operator that owns the first write or remote effect.
4. Load only the chosen operator skill from the runtime profile or `.skills/yeisme/pinax-agent/<skill>/SKILL.md`; do not bulk-load all Pinax skills.
5. Prefer `--agent` for low-token read/search/status context; use `--json` for writes, validation, sync results, and structured error handling.
6. For note writes, draft or revise the body only as much as needed to create the vault entry, then use `pinax note add "<title>" --dir index --stdin --json` for agent-authored notes that need later classification, or `pinax inbox capture "<title>" --stdin --json` for raw temporary capture, instead of hand-writing Markdown files. Do not stop after printing `下面是一版整理后的完整笔记` when the user asked to complete a note.
7. For writes, use `--dry-run`, `preview`, `plan`, or read-only diagnostic commands first when available.
8. Before high-risk local changes, create a snapshot with `pinax version snapshot --message "before agent changes" --json`.
9. Never edit `.pinax/**`, SQLite files, receipts, sync state, backend registries, API tokens, or cloud config by hand.

## Boundaries

- Pinax vault Markdown notes are user content. Preserve the user's language and do not rewrite unrelated notes.
- Structured assets are CLI-authored. Use Pinax commands for `.pinax/**` changes.
- Do not print, save, or infer raw credentials. Refer to credential profiles, token files, env var names, or secret refs only.
- Cloud Sync and Remote API Mode are different workflows; do not mix them unless the user explicitly asks.
- Publish, plugin, API, token, profile, and MCP workflows expose integration surfaces; start read-only and require explicit approval before writes or network-facing services.

## Validation

- A routed answer names the selected operator skill and why.
- Commands shown to the user are real `pinax` commands.
- Newly generated notes without an explicit approved destination are created under `notes/index/`, not the vault root or a guessed topic folder.
- The router does not directly perform broad content edits when a narrower operator skill applies.
