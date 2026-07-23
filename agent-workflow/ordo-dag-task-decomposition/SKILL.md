---
name: ordo-dag-task-decomposition
description: Use when designing, reviewing, or implementing Ordo/OpenSpec task decomposition, atomic task contracts, dependency DAGs, owned-path analysis, derived edge provenance, ready/blocked explanations, or agent-executable verification boundaries.
---

# Ordo DAG Task Decomposition

## Inputs

- Approved OpenSpec `proposal.md`, `design.md`, `tasks.md`, and specs.
- Repository ownership boundaries and nearest `AGENTS.md` files.
- Required acceptance commands, evidence paths, permissions, and runtime limits.

## Workflow

1. Treat each source task as a candidate, not an executable task.
2. Require one primary outcome, one writer ownership set or explicit no-write scope, bounded input refs, explicit output refs, exclusions, acceptance, verification, expected result, and failure recheck.
3. Split a candidate when it mixes unrelated outcomes, overlapping writers, contract definition with dependent consumers, implementation with independent final verification, or acceptance that depends on an unfinished sibling candidate.
4. Preserve explicit dependencies. Add only evidence-backed derived edges using `artifact`, `contract`, `verification`, `path_conflict`, or `approval` kinds.
5. Record source, reason, confidence, and stable refs for every derived edge. Route low-confidence relationships to operator review instead of silently changing authority.
6. Verify that each ready task can be executed and accepted without reading another unaccepted candidate.
7. Keep implementer ownership of production code plus related tests; keep independent verifier tasks read-only and downstream of candidate freeze.

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
- Do not optimize for maximum agent count; optimize for independently acceptable work.
- Do not make a derived edge hard when evidence is weak.
- Do not edit durable plan metadata directly when Ordo exposes an application-service command.
- Do not dispatch child agents recursively.

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
