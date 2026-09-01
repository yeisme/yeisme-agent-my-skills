---
name: pinax-continuity-operator
description: Use when an agent needs to resume, diagnose, checkpoint, review, or give outcome feedback for Pinax project continuity across Codex and Claude Code sessions, including requests like "继续这个项目", "继续上次的工作", "resume this project", "where did we leave off", "保存进度", "save a checkpoint before switching agents", "每周回顾", "weekly review", or "记录这次交接是否可信"; orchestrates the provider-neutral pinax continue contract without owning any canonical state.
---

# Pinax Continuity Operator

Single source operator for the Pinax continuity workflow, shared by Codex and Claude Code. Runtime copies under `.agents/skills/` and `.claude/skills/` are generated from this source through `scripts/skills.sh`; never edit or hand-patch a generated copy. This skill is an interaction orchestrator only: it calls the Pinax CLI in machine mode and renders what Pinax returns. It never reads Pinax SQLite, the binding registry, or vault metadata directly, and it never creates, modifies, or confirms canonical memory.

## Use When

- The user says or implies `继续这个项目`, `继续上次的工作`, `接着昨天做的`, `恢复上下文`, `resume this project`, `continue where we left off`, `catch me up on this repo`, or asks what the project state is.
- The user wants to pause, finish, or switch agents and preserve progress: `保存进度`, `打个检查点`, `我要切到另一个 agent`, `save a checkpoint`, `hand off to Claude Code/Codex`.
- The user asks about binding/status problems: `为什么 continue 找不到项目`, `绑定状态`, `check continuity status`, `fix the binding`.
- The user wants a weekly or relevant review of pending memory items: `每周回顾`, `weekly review`, `哪些提案需要处理`.
- A substantial recorded loop is closing and outcome feedback is due: `trusted`, `corrected`, `wrong_project`, `insufficient`.
- The task is operational continuity use, not Go code changes under `cli/pinax`; for implementation work use `yeisme-pinax-cli-runtime`.

For ordinary note capture, retrieval, or memory recall, use `pinax-agent-router` instead.

## Contract Status

The command contract is owned and implemented by `cli/pinax/openspec/changes/pinax-trusted-continuity-dogfood-v1/` (contract gate passed 2026-08-30; all listed commands are current).

| Surface | Status | Notes |
| --- | --- | --- |
| `pinax continue --vault <v> --scope <s>` | current | Explicit flags, read-only resume projection. |
| `pinax review` | current | Canonical review inbox commands. |
| `pinax continue bind` / `pinax continue status` | current | Binding create/inspect. |
| `pinax continue checkpoint` | current | Bounded closeout checkpoint. |
| `pinax continue feedback` | current | Four-value user outcome. |
| `pinax continue report` | current | Time-window evidence report. |
| `pinax continue --record-run --runtime <r> --task-class <c>` | current | Opt-in recorded run receipt; default continue stays read-only. |

If a command is missing, fails with an unknown-command/contract error (for example, an older pinax binary), or returns a compatibility blocker: report the concrete blocker plus the canonical recovery path (child change name and owner), and stop. Do not fall back to source-less pseudo-memory, do not simulate continuity from chat history.

## Workflow

1. Detect intent: resume, setup/diagnose, checkpoint, review, or feedback. If none applies, answer normally and do not force continuity steps.
2. Diagnose: call the Pinax status/resume contract in machine mode (`--json` or `--agent`) from the current repository root. Never infer vault, scope, or binding from directory names or chat history.
3. Resume: render only Pinax-returned facts as one compact card — objective, current state, key decisions, blockers/conflicts, one recommended next action, and evidence/freshness status. Do not re-summarize source bodies or add facts Pinax did not return.
4. Work: stay out of the way. Do not interrupt with pending inbox items unless Pinax marks one as changing the current next action.
5. Checkpoint: only when the session is substantial (see below) and the user is pausing, finishing, or switching agents. Submit bounded fields through the Pinax checkpoint contract.
6. Outcome: after a recorded substantial loop closes, ask once for one of `trusted | corrected | wrong_project | insufficient`. If the user does not answer, leave feedback missing; never infer outcome from tone, task success, or tool logs.

"Substantial" means observable state change in this session in at least one of implementation/debugging, product/spec/docs, or release/operations, or an explicit pause/switch request. Plain Q&A, read-only lookups, and attempts that fail before setup produce no checkpoint and no feedback prompt.

## Scenario Paths

Each path yields at most one key question or one next action. Never infer facts or outcomes a second time beyond what Pinax returned.

- Ready: render the Resume Card and one recommended next action. Done.
- Missing binding: stop automatic resume. Offer one choice — ask which registered vault/scope to bind, or show the single canonical recovery command (`pinax continue bind ...`) or explicit-flag fallback (`pinax continue --vault <v> --scope <s>`, current). Do not scan all vaults, auto-create a project, or switch projects silently.
- Ambiguous binding (`continuity_binding_ambiguous`): show the bounded candidates and their status, ask the user to pick one or run the disable/fix command. Until resolved, do not read any candidate scope's continuity content.
- Partial evidence: keep the trustworthy sections, surface stale/conflict/missing exactly as Pinax reports them, and recommend the single recovery action Pinax names. Do not discard trustworthy content because part is missing, and do not upgrade partial facts to verified ones.
- No handoff: show the context-only state and the single next action Pinax recommends (for example, create the first checkpoint at closeout). Do not fabricate an objective or last state.
- Checkpoint oversized: trim to the bounded fields (objective, current state, decisions, completed work, blockers, verification, follow-ups, source refs) within the item/character caps Pinax enforces, then retry once. Never push transcript, raw prompts, or chain-of-thought to make it fit.
- Feedback missing: if the user already answered, submit exactly that value. If unanswered, leave it missing and move on; do not re-ask in the same session and never record `trusted` by default.

## Closeout Rules

- Checkpoint payloads contain only bounded, user-reviewable fields with source refs; no chat transcript, raw provider payloads, hidden prompts, or private tool arguments.
- Durable candidates (decisions, preferences, lessons) go through the Pinax proposal/review flow only. Without explicit user review approval, confirmed memory must not change.
- Approve/reject actions use Pinax stable item references, explicit confirmation, and canonical receipts. This skill provides no bulk approval of its own.
- Keep the `wrong_project` outcome available, but treat cross-project routing as unvalidated: this skill operates one explicitly bound repository at a time and must not claim or attempt automatic cross-project routing.

## Boundaries

- No cross-vault behavior: never search all vaults, enumerate projects to guess, or resolve a repository outside its explicit exact binding.
- Canonical state, permissions, source resolution, ranking, and lifecycle stay in Pinax. This skill adds no store, registry, resolver, or review lifecycle.
- Privacy: do not read or write `.pinax/**`, SQLite files, receipts, or registry files by hand; do not print or transmit credentials, raw prompts, or unredacted payloads.
- Runtime differences are limited to ingress wording and rendering hints; Pinax request/response semantics are identical across Codex and Claude Code.
- Rollback: removing this skill from the root and `cli/pinax` profiles and re-running skill sync removes all generated copies; Pinax CLI, vault, binding, handoff, and receipt data are untouched.

## Validation

- A resume answer renders only Pinax-returned facts with at most one next action; missing/ambiguous binding yields one question or one recovery command.
- Planned commands are labeled planned and never offered as current; contract blockers report the child change and stop.
- Checkpoints contain bounded fields only; no transcript or inferred outcome ever reaches Pinax.
- Unanswered feedback stays missing; no silent `trusted` is recorded.
- No cross-vault scan, silent project switch, or direct `.pinax/**`/registry/database access occurs in any path.
