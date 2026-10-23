---
name: pinax-vault-operator
description: Use when an agent needs to initialize, register, select, inspect, write, create, save, capture, import, export, draft, inbox, journal, or ordinary note lifecycle operations in a Pinax vault through real Pinax commands.
---

# Pinax Vault Operator

Operate the local Pinax Markdown vault safely. Use this for vault setup, default selection, note capture, inbox/journal/draft workflows, import/export, and ordinary note lifecycle operations. Route high-risk maintenance apply, restore, proof-loop, or record-ledger work to `pinax-proof-maintenance-operator`.

## Intake Index Rule

Agent-authored notes must enter the unified intake index before later classification. Unless the user explicitly names a final target directory or an approved `pinax organize plan` selects one, create generated or imported notes under `notes/index/` with `--dir index`. Never create agent-generated notes in the vault root, and never guess a topic folder from the title.

## Low-Friction Capture

Normalize the user's request internally; do not turn capture into a questionnaire. When the vault, content and intent to save are clear, infer a short title, preserve the original body and supplied source links, and execute the authorized capture. Tags, taxonomy, template selection and summaries are optional. Ask only about a missing or ambiguous vault/content boundary. Raw fragments enter `pinax inbox capture`; finished generated notes enter `pinax note add --dir index`. Never guess a topic folder or invent a source/date.

## Use When

- The task asks to add, write, create, save, or import Pinax notes; capture inbox items; create or manage drafts; append journal entries; or export Markdown.
- The user asks for a `Pinax note`, `Pinax 笔记`, `保存到 Pinax`, `写入 vault`, or similar storage-backed note operation.
- The user wants a default/global vault, vault alias, validation, stats, dashboard, or local vault selector.
- The command family is `pinax init`, `pinax vault`, `pinax note`, `pinax inbox`, `pinax journal`, `pinax draft`, `pinax import`, or `pinax export`, excluding high-risk maintenance apply.

## Command Patterns

```bash
pinax vault list --agent
pinax config get vault --json
pinax vault register ./my-notes --name work --default
pinax init ./my-notes --title "My Notes" --json
pinax note add "Title" --dir index --body "Content" --json
pinax note add "AI workflow monetization" --dir index --stdin --json
pinax note list --recent --limit 20 --agent
pinax note describe "Research Log" --view rendered --json
pinax note move "Research Log" archive --json
pinax note archive "Research Log" --json
pinax inbox capture "Temporary idea" --stdin --json
pinax inbox review --limit 5 --json
pinax inbox index preview --json
pinax draft create "Draft title" --stdin --json
pinax draft index preview --json
pinax journal daily append --body "Today I learned..." --json
pinax import markdown ./incoming --dir index --json
pinax export markdown --tag research --to ./export --json
pinax vault validate --json
pinax vault stats --agent
```

## Workflow

Experimental note proposal branch: inspect `pinax agent note proposal list --status approval_required --limit 5 --agent` and `show <id> --json` first. Follow returned vault-bound actions; `--kind`, `--status`, `--limit` and `--cursor` must remain consistent across pages. Refresh the first page after mutations or `proposal_cursor_stale`; do not assume the latest 50 contain every pending proposal. MCP callers use the same tool's discovered fields and `tool_actions` without needing a local CLI; approval/refresh remains owner-local. `pinax agent note propose --kind note_draft --title <title> --stdin --json` creates an approved lifecycle draft through the proof gate; ordinary generated knowledge still defaults to the unified index. Only `inbox_capture`, `journal_append`, and `note_draft` auto-apply. For `note_edit`, use the stable object ID and current revision from `pinax note ref <id> --json`. Never approve an Agent's own proposal without the user's explicit instruction. `approve|reject` without `--yes` previews; confirmed outcomes leave redacted receipts. Query the original proposal after errors; `proposal refresh <id> --yes` rebuilds only metadata and never retries the body write.

1. Resolve the vault first: `pinax vault list --agent`; only use `--vault` when overriding the configured default.
2. A request to save, capture or write into the selected Pinax vault authorizes that local creation; do not request duplicate confirmation. For draft-only or review-before-save requests, keep the draft in conversation until the requested decision.
3. For direct note creation, prefer `pinax note add --dir index` or `pinax inbox capture`; use `--stdin` for long generated bodies and do not write Markdown files directly unless the user explicitly wants prose file editing.
4. For daily organization, start with `pinax inbox review --limit 5 --json`: it combines inbox and unclassified index notes, without writing. Present at most five items with suggested destination, reason and exact proposed changes, drawing on the returned related notes and existing folders. Shared tags are clues, not approved destinations. Accept the user's corrections or skip; skipping creates no state. Use the returned next action for read-only pagination; after mutations refresh without `--after`. Separate classification from body rewriting, merging and discarding. Never auto-merge or delete. Index-page authoring remains `inbox index preview|create|refresh` or `draft index preview|create|refresh`.
5. For ordinary single-note maintenance, use `pinax note move`, `pinax note archive`, `pinax note rename`, `pinax note tag`, or `pinax note property` instead of editing frontmatter by hand.
6. Stop and route to `pinax-proof-maintenance-operator` before `metadata apply`, `repair apply`, `organize apply`, `version restore`, broad note moves, or destructive operations that need snapshot/approval gates.
7. Use `--agent` for read/list/status commands; use `--json` for writes and parse the `status`, `facts`, `actions`, and `error` fields.
8. Confirm a successful save briefly with its stable reference and open action. Check `readback_status`; older binaries without it require `note show <returned-note-id> --display body --json` for readback. Keep source bodies out of evidence logs. If the result is failed/partial/unknown, inspect the original returned ID/path before any retry; a saved note with failed indexing is not permission to create a duplicate.
9. For substantial organization, route to the proof maintenance operator for `organize plan --note <id>` repeated for exactly the selected objects (maximum 20), followed by a saved plan and snapshot. `inbox review`'s `organize_preview` is readonly, not approval. Scoped plans reject stale overrides and never retry consumed/interrupted execution. Never apply unrelated operations from a broad plan to process five selected notes. Recheck stale plans; report completed, pending and failed items separately. A pause leaves unprocessed notes intact; recovery must preserve later edits.

## Existing Editor Reading

Use `pinax note preview <note-id>` for direct local reading, or `pinax note open <note-id>` with the user's existing `EDITOR`. This opens on the machine running Pinax, not on the user's remote desktop. From a remote Agent, provide the local command and registered local vault reference; never pretend to open the user's editor or reuse a remote absolute path as a client path. If an editor is unavailable, offer the source/preview command. Human-requested full reading is distinct from bounded Agent context.

Compatibility: check `pinax inbox capture --help` and `pinax inbox review --help` once when the installed binary is unknown. A missing stdin/review flag is a version blocker, not an invitation to pass long bodies in shell arguments or hand-edit metadata. Existing `note add --dir index --stdin` can save a finished note; explain its different intake semantics before substituting for a raw inbox capture.

## Safety Boundaries

- Do not hand-edit `.pinax/config.yaml`, `.pinax/events.jsonl`, receipts, indexes, registry files, or SQLite stores.
- Do not create root-level Markdown notes with bare `pinax note add` for agent-generated content.
- Do not place generated notes directly in topic folders unless the target is user-specified or selected by an approved organize plan.
- Do not apply repair or organize plans from this operator; route to `pinax-proof-maintenance-operator`.
- Do not include secrets, provider payloads, raw prompts, hidden prompts, or full chain-of-thought in notes or evidence.
- Treat Markdown body content as user-owned; preserve language and intent.
- If the user wants the vault on object storage, do not make Pinax talk to S3. The specified path is DriveBridge `preset pinax-vault` (user terminal) then this operator on the local `--vault-root`. Do not start that mount. Do not treat `pinax storage set s3` as a live vault filesystem.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| User requested a draft only | Keep the draft in conversation | Do not infer save permission |
| Vault is ambiguous | `pinax vault list --agent` | Do not guess a vault from the cwd |
| Request is repair/organize/restore | Route to `pinax-proof-maintenance-operator` | Do not `--yes` from this operator |
| Generated note would land in vault root or a guessed topic folder | Force `--dir index` | Do not invent a destination |
| Object-storage vault / 笔记在桶里 | Show DriveBridge `preset pinax-vault` as user-terminal setup; then `pinax storage set local` on `vault_root` | Do not add a Pinax S3 vault adapter or `hydrate` as the main path |
| `content_unmounted` / notes dir not writable | Ask the user to run `drivebridge mount vault --preset pinax ...` | Do not call S3 from Pinax |

## Validation

- After setup: `pinax vault validate --json`.
- After capture: verify returned identity/readback, then use `pinax search "<title or keyword>" --lazy-index off --limit 5 --agent` as needed. Confirm finished unclassified notes are under `notes/index/`; raw fragments retain the existing inbox lifecycle.
- After inbox/draft index changes: `pinax inbox index preview --json` or `pinax draft index preview --json`.
