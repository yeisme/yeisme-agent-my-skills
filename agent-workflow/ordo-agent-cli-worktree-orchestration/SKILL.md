---
name: ordo-agent-cli-worktree-orchestration
description: Use when designing, implementing, debugging, or reviewing Ordo Goal target dispatch, Git workspace admission, task branches, writer leases, process or runtime session identity, heartbeat, timeout reconciliation, candidate retention, integration, or safe cleanup.
---

# Ordo Agent CLI Worktree Orchestration

## Inputs

- Approved Ordo task contract and owned paths.
- Goal target revision, task binding, workspace mode, and source-drift state when the task belongs to an OpenSpec Goal.
- Lane intent (`client_preview`, `backend_hot_reload`, `contract`, or `read_only`) and the runtime resources that must remain isolated.
- Repository root, base commit, current branch, dirty-state and submodule facts.
- Runtime adapter capability, launcher version, timeout, budget, permissions, and evidence contract.

## Workflow

1. Inspect repository root, base commit, branch, tracked and untracked changes, submodule state, existing worktrees, active leases, and target path availability.
2. Resolve workspace intent before writer admission. Default `client_preview` to the current repository root/current branch; default `backend_hot_reload` to an isolated task branch/worktree. An explicit operator, user, or target policy may select the other mode when the base is reproducible, ownership is disjoint, and the reason is recorded.
3. If the task depends on current uncommitted user changes, use current-worktree single-writer mode or request an operator checkpoint. Never stash, reset, clean, move, or delete those changes automatically.
4. Treat `read_only` and `verifier` tasks as no-worktree/no-writer-lease work. They may inspect the current branch, candidate, and evidence but cannot become writers because progress is being computed.
5. Acquire and persist the writer lease before launch. Bind repository identity, target revision, base, branch, absolute worktree path, owned paths, task, attempt, runtime, and candidate policy.
6. Launch the Agent CLI with argv arrays and a bounded environment allowlist. Persist runtime/version, launcher identity, argv digest, cwd, process identity, session/thread ref when available, heartbeat source, and start time before marking the attempt running.
7. On timeout, disconnect, early exit, missing completion envelope, source drift, or ambiguous liveness, retain the lease and reconcile Git, process, target, and runtime session identities.
8. Freeze the candidate before independent verification. Preserve the same worktree for one evidence-backed same-writer repair.
9. Permit cleanup only after accepted integration is proven, or after explicit operator abandonment records recovery and artifact refs. Refuse paths outside the recorded lease.

## Workspace Policy

| task mode | default workspace | lease | rule |
| --- | --- | --- | --- |
| `write` + `client_preview` | current repository root/current branch | one writer lease | preserve the live preview/rendering process and serialize current-branch writes |
| `write` + `backend_hot_reload` | `.agents/worktrees/<safe-target>/<safe-task>` | one isolated lease | isolate branch, ports, data/cache directories, generated outputs, logs, and process group |
| `write` + explicit `current` | current repository root/current branch | one writer lease | allowed for shared uncommitted state or an explicit user/owner override; record the reason |
| `write` + explicit `isolated` | `.agents/worktrees/<safe-target>/<safe-task>` | one isolated lease | create only through the Ordo application service after containment checks |
| `read_only` / `verifier` | none | none | inspect current branch, candidate, or evidence without writer admission |

An isolated path must realpath below the repository root's `.agents/worktrees/` directory. Reject absolute paths, `..`, symlink escape, repository-external sibling directories, and handwritten worktree roots. The project ignores `/.agents/worktrees/`; lease and Goal metadata stay in the canonical application store.

Before a write action, inspect the current Goal projection with `ordo goal target status <change-id> --json` or `ordo goal next <change-id> --json`. These read commands are advisory only — they report target revision, source drift, verified ratio, and blockers without creating a lease, dispatching a runtime, or changing task state. After timeout or unknown liveness, use the existing `ordo goal reconcile <goal-id> --json`. Source drift is reported by `ordo goal target refresh <change-id> --json`; adopting the current source requires the approval-gated `ordo goal target rebase <change-id> --approve --json`. This skill never issues a lease, overrides a guard deny, changes enforcement mode, or closes a Goal — those are operator-driven mutating actions owned by the Ordo application service.

## Automated Debugging And Checkpoints

For `backend_hot_reload`, the lease must include the real start command, health/readiness signal, port, runtime/data directory, log path, and process identity. The bounded debug loop is: start → wait for readiness → reproduce with the smallest focused test/request → inspect structured logs and trace/request IDs → patch owned paths → rerun focused checks → verify the client-facing contract. A worktree does not permit killing an unrelated process or sharing mutable runtime state with the client preview lane.

At `contract_ready`, `preview_ready`, `backend_slice_ready`, and `integration_passed`, freeze the candidate and return a narrow checkpoint manifest. Child agents do not commit, push, merge, or clean worktrees; root performs any authorized checkpoint commit or integration after verifying the candidate.

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
- Target drift, current-branch writer occupancy, workspace/path mismatch, or an unowned dirty current branch must fail closed for new writer admission.
- A read-only or verifier task must never acquire a writer lease as a progress shortcut.
- Port, data-directory, log, process-group, or health-signal collision must fail closed for a backend hot-reload writer.

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
