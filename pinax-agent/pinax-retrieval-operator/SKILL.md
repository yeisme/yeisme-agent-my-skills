---
name: pinax-retrieval-operator
description: Use when an agent needs bounded Pinax retrieval through index refresh, search, note links/backlinks/orphans, KB semantic context, saved views, folders, database/dataview/query surfaces, or controlled read-only context commands without editing vault state directly.
---

# Pinax Retrieval Operator

Retrieve bounded context from a Pinax vault for agents. Use deterministic index/search first; use KB semantic context only when fuzzy note-body retrieval is needed.

## Use When

- The task asks to find notes, inspect backlinks, gather context, answer from the vault, or prepare an implementation/research context pack.
- The user mentions `search`, `index`, `kb`, semantic context, links, backlinks, orphans, `view`, `folder`, `database`, `dataview`, `query`, or stale index behavior.
- A downstream agent needs compact evidence rather than full note bodies.

## Command Patterns

```bash
pinax index status --json
pinax index refresh --json
pinax index doctor --json
pinax index lookup diagram --scope all --json
pinax index page preview ideas --json
pinax search "release workflow" --agent
pinax note links "Release Plan" --json
pinax note backlinks "Release Plan" --json
pinax note orphans --json
pinax kb doctor --json
pinax kb context "prepare the next release" --limit 8 --json
pinax kb search "project context" --limit 8 --json
pinax view list --json
pinax folder list --json
pinax folder show notes/research --json
pinax database view list --json
pinax dataview table --from notes --limit 20 --json
pinax query run "SELECT title, path FROM notes LIMIT 10" --json
```

## Workflow

1. Check or refresh deterministic projections with `pinax index refresh --json` when search results may be stale. Use `pinax index doctor --json` for structural exceptions or corrupt projections.
2. Use `pinax search` for keywords, tags, folders, status, links, and ordinary note discovery.
3. Use `pinax note links`, `pinax note backlinks`, and `pinax note orphans` for graph-like note relationship checks before semantic search.
4. Use `pinax view`, `pinax folder list/show`, `pinax database view`, `pinax dataview`, or `pinax query` only through their controlled Pinax surfaces; do not read SQLite files directly.
5. Use `pinax memory context` through `pinax-memory-operator` for durable decisions or facts; do not use KB as a decision ledger.
6. Use `pinax kb context` only when semantic similarity over larger note bodies is required.
7. Prefer `--agent` for low-token facts and `--json` when another tool needs structured records.
8. Keep returned context bounded by `--limit` and cite `path`, `title`, or source facts in the response.
9. Use `pinax index sync` only when a workflow explicitly requires the record/proof-loop sync semantics; for ordinary stale search recovery, prefer `pinax index refresh`.

## Safety Boundaries

- Retrieval commands must not expose raw secrets, provider payloads, hidden prompts, or full private note bodies unless the user explicitly asks to read a specific note.
- Do not hand-edit `.pinax/index.sqlite`, `.pinax/kb/**`, database projection files, saved view metadata, or folder metadata.
- Do not run arbitrary SQL outside `pinax query` surfaces.
- Do not create or refresh managed index pages unless the task is authoring or maintenance; route those writes to `pinax-template-authoring-operator` or `pinax-proof-maintenance-operator` as appropriate.

## Validation

- `pinax index refresh --json` returns `status=success` before relying on fresh deterministic search.
- `pinax kb doctor --json` reports sidecar availability before semantic KB operations.
- Retrieved context includes enough source identifiers for the user or agent to verify later.
