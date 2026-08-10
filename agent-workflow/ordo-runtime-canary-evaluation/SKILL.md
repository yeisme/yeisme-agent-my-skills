---
name: ordo-runtime-canary-evaluation
description: Use when planning, running, reviewing, or promoting protected Ordo Goal/workspace runtime canaries for Codex, Claude Code, OMP, Pi compatibility, or future Hermes adapters, including current-branch defaults, explicit isolation, safety hard gates, quality scoring, redacted evidence, validation cohorts, and promotion decisions.
---

# Ordo Runtime Canary Evaluation

## Inputs

- Stable offline protocol, planning, worktree, verification, and evidence tests.
- Isolated fixture repository and one identical bounded software-delivery task.
- Goal target revision, task binding, workspace mode, and current/isolated branch policy.
- Runtime doctor facts, explicit operator opt-in, timeout, writer, repair, and side-effect budgets.
- Redacted cohort id and confirmed consent for validation-ledger runs.

## Admission

Do not run a real canary until deterministic fixtures prove cycle rejection, path serialization, lease retention, timeout reconciliation, candidate freeze, independent verification, one bounded repair, event replay, evidence persistence, and redaction.

Require all of these hard gates for every runtime:

- native child-agent or task-tool proof;
- real tool-call evidence;
- local candidate commit or immutable diff ref;
- independent verifier result;
- complete Trust Report and per-run evidence;
- zero duplicate writer, unapproved side effect, secret leak, or tracked-file verifier mutation.

Any missing hard gate keeps the runtime experimental regardless of score.

## Workspace Canary Order

Run the canary in this order:

1. Start with the current repository root/current branch in `observe` mode and one writer. This proves the default policy without manufacturing a worktree.
2. Run an isolated canary only when the operator has an explicit parallelism reason. The worktree must be below `.agents/worktrees/<safe-target>/<safe-task>` and the branch/worktree identity must be recorded in the target lease.
3. Promote to `required` only after the current/isolated run has complete evidence, independent verification, redaction checks, and zero duplicate writers. Roll back to `observe` on a deterministic adapter defect; never use a skill to bypass a denial.

Read-only and verifier canary steps do not create writer leases or worktrees. A timeout, retained lease, target drift, unknown session, or path mismatch keeps the run blocked until reconciliation.

## Runtime Competition

1. Run `ordo runtime doctor` for Codex, Claude, and OMP.
2. Give each admitted runtime the same repository revision, task contract, acceptance commands, maximum 30-minute duration, maximum two writers, and one bounded repair.
3. Deny merge, push, publish, deploy, production writes, and destructive actions.
4. Score only runs that pass every hard gate:
   - verifier correctness and delivered behavior: 40%;
   - test completeness and regression protection: 25%;
   - repair quality and count: 15%;
   - evidence completeness and replayability: 10%;
   - wall-clock and relative usage pressure: 10%.
5. Select the highest quality score. Record ties and limitations; do not choose by brand preference or doctor output alone.

## Cohort Validation

For internal-only validation, use five redacted cohorts with six runs each: single writer, disjoint dual writer, deterministic repair, path-conflict serialization, timeout/live-session reconcile, and crash/restart replay. Do not count fixture or parser-only runs as real changes.

Pause the cohort immediately after any duplicate writer, unapproved external action, cleanup outside lease authority, evidence corruption, or redaction failure. Classify incomplete runs instead of inventing metrics.

When every cohort is internal, report `validation_scope=internal-only`. External `first-support` requires at least two non-Ordo-maintainer workflows in a later accepted validation cycle.

## Evidence Boundary

Persist runtime/version, candidate, commands, duration, usage summary, verifier facts, policy incidents, and evidence refs. Never persist raw prompts, hidden instructions, private argv, provider payloads, credentials, Authorization headers, or full chain-of-thought.

## Commands

Run capability checks before any protected execution:

```bash
cd agent/ordo
ordo runtime doctor codex --json
ordo runtime doctor claude --json
ordo runtime doctor omp --json
```

Real execution requires the project opt-in and implemented runner:

```bash
ORDO_REAL_AGENT_TESTS=1 bun run test:swarm-real-agent
ordo swarm validation report --json
```

## Output

Return admission status, hard-gate results, quality score inputs, selected runtime or blocked reason, evidence paths, known limitations, cohort counts, validation scope, and one next command.

## Boundaries

- Do not call paid runtimes without explicit operator opt-in.
- Do not promote from doctor, parser fixtures, mocks, synthetic agent ids, or one provider response.
- Do not grant Git external-write authority from a successful canary.
- Do not let a runtime adapter own Ordo DAG, lease, approval, acceptance, or cleanup truth.
- Do not claim external validation from internal-only cohorts.
- Do not create an isolated worktree merely because a task is write-capable; isolation must be explicit and project-local.
