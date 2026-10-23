---
name: pinax-agent-router
description: Use when an agent needs to operate Pinax for local-first notes, including requests to write, complete, draft, create, save, capture, import, search, organize, maintain, sync, publish, run proof loops, manage project workspaces, templates, assets, prompts, API/profile/token, plugin, or MCP workflows; route to the narrowest Pinax operator skill before running commands.
---

# Pinax Agent Router

Route Pinax user-agent work to the smallest suitable Pinax operator skill. Root sessions normally keep only this router active; load the specific Pinax operator only after classifying the task. For knowledge-note requests, do not satisfy the user by only printing a complete note in chat; route to Pinax capture unless the request is clearly a non-Pinax publishing draft.

## Research Brief Exception

When a user asks to use old notes for a decision or research brief, load `pinax-retrieval-operator` and its Decision Research Brief branch first. This takes precedence over default note capture and index refresh: draft in conversation, disclose source limits, then save only after explicit acceptance and authorization under the agreed workflow. A usefulness rating alone is not save permission.

## Intake Index Rule

Agent-authored Pinax notes are captured through the vault's unified intake index first. For newly generated, imported, or saved notes whose final taxonomy has not already been approved, the destination must be `notes/index/` via commands such as `pinax note add "Title" --dir index --stdin --json`. Do not use bare `pinax note add --help` for agent-generated notes, because it can create root-level notes. Do not place notes directly into topic folders such as `notes/tools/**`, `notes/research/**`, or `notes/media/**` unless the user explicitly named that target path or an approved organize plan selected it.

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
| Experimental rendered tree, exact-version reference, floating drift, clipboard reference | `pinax-retrieval-operator` | `pinax note preview <id> --view rendered --agent`, `pinax note ref <id> --json` |
| Experimental note proposal, pending edit review, original-outcome recovery | `pinax-vault-operator` | `pinax agent note proposal list --status approval_required --limit 5 --agent`, `pinax agent note proposal describe <id> --json` |
| Capture or recall durable facts, decisions, events, and tasks | `pinax-memory-operator` | `pinax memory context "..." --agent`, `pinax memory recall "..." --agent` |
| Capsa Sync, repository-encrypted S3/COS bootstrap, sync logs/conflicts, storage backend, S3/rclone fallback, backend object diagnostics | `pinax-sync-storage-operator` | `pinax sync status --agent`, `pinax sync repo doctor --json`, `pinax sync diff --target capsa --json` |
| Plaintext object-storage vault (S3/MinIO/COS as notes disk) | `drivebridge-operator` then `pinax-vault-operator` | User terminal `drivebridge preset pinax-vault ...`; then `pinax storage set local --root <vault-root>`. Do not make Pinax talk to S3. |
| Proof loop, doctor/stats, metadata/repair/organize apply, snapshot/restore, record ledger, high-risk maintenance | `pinax-proof-maintenance-operator` | `pinax proof loop run --json`, `pinax vault doctor --json`, `pinax version snapshot --message "before maintenance" --json` |
| Project workspace, learning packs, project board/items, personal daily/weekly/monthly plans, local planning action drafts | `pinax-project-workspace-operator` | `pinax project list --agent`, `pinax project board describe <project> --agent`, `pinax plan daily --dry-run --json` |
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

- For a selected review batch, route `organize plan --note <id>` to the proof maintenance operator; never omit selectors to bypass an unsupported scoped workflow. Proposal pagination uses returned cursors and the same filters/vault, refreshing after writes. MCP-only clients use `tool_actions`; owner-local approval is not a client filesystem action.
- Experimental note proposals and rendered references are admitted by `pinax-agent-note-proposal-v1` and `pinax-rendered-view-v1`. Propose tools are owner-enabled, off by default. Low-risk kinds can auto-apply through the proof gate; edits need explicit user approval. Do not use an owner approve command merely because an Agent proposed a change.
- `note preview --view rendered` is additive; legacy preview remains available. Default rendered depth is card. For floating drift, the caller retains and returns the first `resolved_revision`; no persistent reference memory is implied. On timeout, inspect the original proposal ID; metadata refresh never authorizes reapply.

- Pinax vault Markdown notes are user content. Preserve the user's language and do not rewrite unrelated notes.
- Structured assets are CLI-authored. Use Pinax commands for `.pinax/**` changes.
- Do not print, save, or infer raw credentials. Refer to credential profiles, token files, env var names, or secret refs only.
- Cloud Sync, Remote API Mode, DriveBridge attach/hydrate, and DriveBridge pinax-vault path mounts are different workflows; do not mix them unless the user explicitly asks.
- A plaintext object-storage vault is a DriveBridge path mount plus local Pinax. Do not route it to a Pinax S3 vault adapter.
- Publish, plugin, API, token, profile, and MCP workflows expose integration surfaces; start read-only and require explicit approval before writes or network-facing services.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| No vault / wrong vault | `pinax vault list --agent` | Ask the user to `pinax vault register --help` / select; do not guess a path |
| Operator skill not in this session runtime | Read `.skills/yeisme/pinax-agent/<operator>/SKILL.md` | Do not bulk-load all eight operators |
| Write without snapshot on high-risk maintenance | `pinax version snapshot --message "before agent changes" --json` | Stop; do not hand-edit `.pinax/**` |
| User asked to complete a note but only chat text was produced | Route to `pinax-vault-operator` and `pinax note add "Title" --dir index --stdin --json` | Do not claim the note is saved |
| Gateway/MCP admin mixed into Pinax | Hand off to `yeisme-mcp-router` | Pinax operators do not own Gateway policy |
| User wants vault on object storage | Route to `drivebridge-operator` for `preset pinax-vault`, then local Pinax | Do not `pinax storage set s3` as live vault FS; do not start the mount from the agent |

## Validation

- A routed answer names the selected operator skill and why.
- Commands shown to the user are real `pinax` commands.
- Newly generated notes without an explicit approved destination are created under `notes/index/`, not the vault root or a guessed topic folder.
- The router does not directly perform broad content edits when a narrower operator skill applies.


## 资源命令与版本合同

先读取安装版的 help/结构化发现面，确认 canonical 路径存在。运行 `pinax project list --agent`，从 `fact.project.N.id` 取真实 ID，再调用 `pinax project describe <id> --agent`；`<id>` 是待替换的语法说明，不作为可直接执行的 Next。保持原项目、配置、过滤与权限范围。解析失败报告合同或版本问题，可查 `--json`，不要解析人读表或猜 ID。

详情类旧 show 只作隐藏兼容；正常操作使用 describe，独立 inspect/export/download 等动作保持原义。补全是同一目录的只读视图；需要安装时显式运行 completion install，并用 completion doctor 区分文件存在与 shell 可发现。源码候选通过不代表 PATH 安装版已更新。
