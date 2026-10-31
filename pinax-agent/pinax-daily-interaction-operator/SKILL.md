---
name: pinax-daily-interaction-operator
description: Use when an agent should guide a Pinax daily workflow across capture, retrieval, inbox review, planning, protected apply, continuity resume, or checkpoint without adding a new session or bypassing existing write and recovery gates.
---

# Pinax Daily Interaction Operator

Use Pinax's existing commands as the canonical interaction surface. This Skill
is an orchestrator only: it reads the returned `pinax.daily_interaction.v1`
projection, renders one next action, and never reads `.pinax/**`, SQLite,
vault registries, receipts, or provider state directly.

## Use when

- The user asks to start the day's work, record something, find a note, review
  inbox items, plan the next work, continue a project, or save a handoff.
- A previous Pinax command returned `phase`, `state`, `recommended_next_action`,
  or a recovery action and the user wants to continue.

For a single ordinary note operation, route to the narrower Pinax operator
instead of forcing a whole daily flow.

## Workflow

1. Confirm the vault with `pinax vault list --agent` when the vault is unknown.
2. Run one primary real command in machine mode. Prefer `--agent` for reads and
   `--json` for writes, plans, approvals, and recovery.
3. Render only returned facts: phase, state, read/write boundary, source and
   freshness status, and one recommended action. Keep stale, partial, conflict,
   blocked, approval-required, and unknown states visible.
4. Follow only the returned action. A second read-only command is allowed when
   the first projection explicitly asks for it; do not create an implicit
   workflow session.
5. Before a protected write, keep the existing `--dry-run`, `--yes`, snapshot,
   expected revision, receipt, and operation-reconcile requirements.
6. At substantial pause, finish, or Agent switch, use the bounded checkpoint
   contract. Durable decisions/preferences/lessons remain proposals until the
   user reviews them.

## Canonical transitions

- Capture: `pinax inbox capture "Title" --stdin --json` →
  `pinax inbox review --limit 5 --json`.
- Retrieve: `pinax search "keyword" --agent` → the returned
  `pinax note preview <note-id> --json` action.
- Review: `pinax inbox review --limit 5 --json` → the returned scoped
  `pinax organize plan --note <note-id> --json` action.
- Plan/apply: review `pinax plan daily --dry-run --json` or a saved plan before
  `pinax organize apply --plan <plan-id> --yes --vault ./my-notes --json`.
- Resume/close: `pinax continue --json` and
  `pinax continue checkpoint --json`.

## Safety and recovery

- Missing or ambiguous binding: show the returned bind/status/rebind action;
  never scan all vaults, guess a project, or switch scope silently.
- `partial` or stale evidence: preserve trustworthy sections and show the
  refresh/review action; do not upgrade it to ready.
- `approval_required` or `plan_stale`: stop and show the returned action;
  never add `--yes`, allow stale, or re-plan silently.
- `unknown`, `reconcile_required`, or `unknown_accept`: inspect the original
  operation identity before any retry.
- Never infer `trusted` feedback from task success or user silence.
- Never persist transcript, raw prompts, provider payloads, credentials, or
  full note bodies in the interaction response.

## Boundaries

Pinax owns canonical Markdown, scopes, revisions, proposals, snapshots,
receipts, and recovery. This Skill owns only natural-language routing and
rendering. It does not create a database, durable session, provider bridge,
MCP App, UI, daemon, external task action, sync, publish, or automatic memory
approval.

If the installed binary does not expose the command or interaction projection,
report the version/contract blocker and use the existing owner recovery path;
do not simulate the flow from chat history.
