---
name: ordo-agent-cli-worktree-orchestration
description: Use when designing, implementing, debugging, or reviewing Ordo Agent CLI dispatch, Git worktree admission, task branches, writer leases, process or runtime session identity, heartbeat, timeout reconciliation, candidate retention, integration, or safe workspace cleanup.
---

# Ordo Agent CLI Worktree Orchestration

## Inputs

- Approved Ordo task contract and owned paths.
- Repository root, base commit, current branch, dirty-state and submodule facts.
- Runtime adapter capability, launcher version, timeout, budget, permissions, and evidence contract.

## Workflow

1. Inspect repository root, base commit, branch, tracked and untracked changes, submodule state, existing worktrees, active leases, and target path availability.
2. Use an isolated task branch and worktree only when the base is reproducible, ownership is disjoint, and required state is present.
3. If the task depends on current uncommitted user changes, use current-worktree single-writer mode or request an operator checkpoint. Never stash, reset, clean, move, or delete those changes automatically.
4. Acquire and persist the writer lease before launch. Bind repository identity, base, branch, absolute worktree path, owned paths, task, attempt, runtime, and candidate policy.
5. Launch the Agent CLI with argv arrays and a bounded environment allowlist. Persist runtime/version, launcher identity, argv digest, cwd, process identity, session/thread ref when available, heartbeat source, and start time before marking the attempt running.
6. On timeout, disconnect, early exit, missing completion envelope, or ambiguous liveness, retain the lease and reconcile Git, process, and runtime session identities.
7. Freeze the candidate before independent verification. Preserve the same worktree for one evidence-backed same-writer repair.
8. Permit cleanup only after accepted integration is proven, or after explicit operator abandonment records recovery and artifact refs. Refuse paths outside the recorded lease.

## Runtime Boundary

Codex, Claude Code, OMP, Pi compatibility, and future Hermes adapters are execution adapters. They do not own DAG, lease, approval, acceptance, cleanup authority, or downstream release decisions. Runtime-native child agents do not gain Ordo ownership.

Persist digests and redacted facts, not raw prompts, private argv, provider payloads, credentials, hidden instructions, or full chain-of-thought.

## Failure Rules

- Timeout is not proof that a writer stopped.
- PID absence alone is insufficient when a runtime session may remain live.
- Exit code zero without a valid completion envelope is not acceptance.
- Verification failure retains the candidate and worktree.
- Cleanup mismatch, live identity, unaccepted candidate, or unknown integration state must fail closed.
- Never start a duplicate writer while the original lease remains unresolved.

## Validation

Use the owning Ordo checks:

```bash
cd agent/ordo
openspec validate ordo-agent-swarm-control-plane --strict
bun test test/swarm/lease test/swarm/worktree test/swarm/reconcile test/swarm/attempt test/plugins
```

For planned operator projections, use:

```bash
ordo swarm worktree list <run-id> --json
ordo swarm worktree inspect <run-id> <task-id> --json
ordo swarm worktree reconcile <run-id> <task-id> --json
```

Do not run cleanup as a diagnostic command. Cleanup is an explicit mutation after acceptance or abandonment.
