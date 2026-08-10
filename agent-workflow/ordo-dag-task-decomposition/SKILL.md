---
name: ordo-dag-task-decomposition
description: Use when designing, reviewing, or implementing Ordo/OpenSpec Goal task decomposition, target bindings, atomic task contracts, dependency DAGs, owned-path analysis, derived edge provenance, ready/blocked explanations, or agent-executable verification boundaries.
---

# Ordo DAG Task Decomposition

## Inputs

- Approved OpenSpec `proposal.md`, `design.md`, `tasks.md`, and specs.
- Repository ownership boundaries and nearest `AGENTS.md` files.
- Required acceptance commands, evidence paths, permissions, and runtime limits.

## Workflow

1. Treat each source task as a candidate, not an executable task.
2. Require one primary outcome, one writer ownership set or explicit no-write scope, a declared `workspace_mode` (`current|isolated|none`), bounded input refs, explicit output refs, exclusions, acceptance, verification, expected result, and failure recheck.
3. Split a candidate when it mixes unrelated outcomes, overlapping writers, contract definition with dependent consumers, implementation with independent final verification, or acceptance that depends on an unfinished sibling candidate.
4. Preserve explicit dependencies. Add only evidence-backed derived edges using `artifact`, `contract`, `verification`, `path_conflict`, or `approval` kinds.
5. Record source, reason, confidence, and stable refs for every derived edge. Route low-confidence relationships to operator review instead of silently changing authority.
6. Verify that each ready task can be executed and accepted without reading another unaccepted candidate.
7. Keep implementer ownership of production code plus related tests; keep independent verifier tasks read-only and downstream of candidate freeze. A task is not ready until its target revision, branch/worktree, session, lease, and owned-path facts are compatible with the workspace mode.

## Goal Target and Workspace Admission

For a Goal-backed OpenSpec task, normalize these facts before dispatch:

- `target_revision` and `source_digest` from the imported OpenSpec snapshot.
- `task_ref` and explicit `spec_ref` mapping; do not infer acceptance from prose.
- `workspace_mode=current|isolated|none` and `branch_policy=current|new`.
- `owned_paths`, `cwd`, branch, worktree path, attempt/session identity, and lease fence.

Default `write` tasks use the current repository root/current branch and serialize on one writer. Explicit `isolated` tasks use only `.agents/worktrees/<safe-target>/<safe-task>` after realpath containment checks. `read_only` and `verifier` tasks use `none` and never obtain a writer lease.

When `ordo goal status <goal-id> --json` reports drift, blocked, retained, or unknown, recommend the existing `ordo goal reconcile <goal-id> --json` or operator review. Planned target refresh/rebase names belong to the OpenSpec contract until the CLI exposes them; a skill must not pretend to execute them.

## Atomicity Gate

Reject or rewrite a task when any answer is unclear:

- What single observable outcome does it produce?
- Which exact paths may it write?
- Can another active writer touch those paths?
- Which accepted artifacts are its inputs?
- Which artifact or candidate ref does it output?
- Can its verification command run independently?
- Does failure block only declared descendants?

Return `task_not_atomic`, `ownership_ambiguous`, `verification_not_independent`, or `edge_review_required` rather than inventing missing authority.

## Output

Produce normalized tasks, typed edges, parallel lanes, ready/blocked reasons, conflict decisions, verification commands, expected results, and failure rechecks. Human-authored OpenSpec updates default to Chinese; schema fields, commands, flags, paths, and event types remain English.

## Boundaries

- Do not let an LLM silently assign owned paths, approvals, credentials, external actions, or acceptance criteria.
- Do not let an LLM silently choose current versus isolated workspace, invent a worktree path, or convert a verifier task into a writer.
- Do not optimize for maximum agent count; optimize for independently acceptable work.
- Do not make a derived edge hard when evidence is weak.
- Do not edit durable plan metadata directly when Ordo exposes an application-service command.
- Do not dispatch child agents recursively.
- Skills are advisory: they cannot issue leases, change enforcement mode, override a guard denial, or accept a candidate.

## Validation

Use the owning Ordo checks:

```bash
cd agent/ordo
openspec validate ordo-agent-swarm-control-plane --strict
bun test test/swarm/decomposition test/swarm/planning
```

For planned CLI behavior, validate projections with:

```bash
ordo swarm plan inspect <plan-id> --json
ordo swarm plan graph <plan-id> --format mermaid
```
