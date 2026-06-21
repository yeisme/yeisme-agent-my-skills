---
name: pinax-memory-operator
description: Use when an agent needs to capture, list, recall, or provide bounded context from Pinax non-vector memory records such as facts, decisions, events, and tasks.
---

# Pinax Memory Operator

Use Pinax memory as a deterministic, cited agent memory ledger. It is for durable facts, decisions, events, and tasks, not fuzzy semantic note search.

## Use When

- The user asks for agent memory, prior decisions, durable project facts, release facts, follow-up tasks, or source-cited recall.
- A session discovers a reusable fact that future agents should remember.
- The task needs explainable recall reasons and lifecycle state instead of vector similarity.

## Command Patterns

```bash
pinax memory context "prepare next release" --entity pinax --limit 12 --agent
pinax memory recall "release workflow" --entity pinax --json
pinax memory capture --type fact --subject pinax --predicate release_workflow --object "tag push triggers GitHub Actions" --source docs/operations/release-packaging.md --json
pinax memory capture --type decision --subject pinax --object "Use structured memory before vector recall" --source openspec/changes/pinax-agent-memory-ledger/design.md --json
pinax memory list --entity pinax --json
pinax memory stats --json
```

## Workflow

1. Recall first with `pinax memory context "<task>" --agent` before adding duplicate memory.
2. Capture only source-cited, stable information. Prefer concise `subject`, `predicate`, and `object` fields.
3. Use `fact` for stable facts, `decision` for chosen direction, `event` for releases/incidents, and `task` for future commitments.
4. Include `--source` whenever possible. Use vault-relative paths, OpenSpec paths, or redacted evidence references.
5. Use `--dry-run` before bulk or uncertain capture.
6. Do not use `memory link` or `memory prune` until those commands are implemented beyond the reserved entry points.

## Safety Boundaries

- Do not store secrets, tokens, provider payloads, raw prompts, hidden prompts, private tool arguments, or full chain-of-thought in memory.
- Do not hand-edit `.pinax/memory/ledger.sqlite`.
- Do not capture unverified LLM guesses as `confirmed`; use a source or leave the candidate out.
- Cloud Sync treats memory as a local rebuildable projection, not a remote source of truth.

## Validation

- After capture: `pinax memory recall "<keyword>" --entity <entity> --json`.
- For agent handoff: `pinax memory context "<task>" --entity <entity> --limit 12 --agent`.
- Confirm the output contains stable facts and does not include private note bodies or credentials.
