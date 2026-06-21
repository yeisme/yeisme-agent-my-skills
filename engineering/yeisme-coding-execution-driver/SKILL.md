---
name: yeisme-coding-execution-driver
description: Use when implementing, modifying, debugging, refactoring, or verifying code in this repository from a user request, PRD, design, bug report, failing command, or implementation plan; enforce trigger discipline, a prioritized recursive checklist, dependency-ordered execution, verification checkpoints, and strict stop conditions so the agent keeps coding until the task is genuinely handled.
---

# Yeisme Coding Execution Driver

## Purpose

Drive coding sessions end to end. Turn a request, approved plan, PRD, bug report, or failing command into a prioritized recursive checklist, execute the highest-priority unblocked leaf, verify each completed slice, and continue until the task is handled or a real stop condition is reached.

Use this together with narrower skills when they apply, such as `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `yeisme-repo-routing`, `yeisme-cohors-cli-runtime`, `yeisme-mcp-builder`, or `yeisme-mcp-gateway-maintainer`.

## Trigger Conditions

Use this skill automatically when the user asks Codex to do any of these in the repository:

- implement, add, change, wire, migrate, refactor, debug, fix, test, verify, polish, or finish code
- execute a PRD, design doc, architecture plan, implementation plan, TODO list, or acceptance checklist
- continue work that stalled, resume a partially completed feature, or make agent coding more persistent
- convert a high-level task into concrete development steps and carry them through
- run checks and repair issues found during coding

Also use it when another domain skill gives engineering guidance but does not define a sustained execution loop.

Do not use this skill for:

- pure strategy, product, CEO, architecture, or design review with no implementation request
- report-only reviews where the user explicitly says not to edit files
- one-off terminal lookups that do not change or verify code
- shipping, publishing, or PR creation workflows after implementation is already complete; use the shipping/release skills instead

## Inputs

- User request, plan file, PRD, bug report, failing command, or desired code change.
- Repository instructions such as `AGENTS.md`, domain `SKILL.md` files, and existing code patterns.
- Current worktree state from `git status --short`.
- Available verification commands inferred from package manifests, Taskfiles, Makefiles, CI config, or existing docs.

## Outputs

- A live recursive checklist with priorities, dependencies, and one active leaf item.
- Scoped code, test, documentation, or config edits that preserve unrelated user changes.
- Focused verification output after each meaningful slice.
- A final status with changed files, checks run, unresolved blockers, and residual risk.

User-facing command examples in docs, plans, reviews, and final replies must show the real command a human can run. Do not expose local execution wrappers, shell aliases, or agent-only command prefixes outside tool execution.

## Checklist Model

Represent work as a tree. Parent nodes organize intent; only leaf nodes are executed.

```text
P0 Goal: <user-visible outcome>
  P0 Phase: <required capability or blocking concern>
    P0 Task: <small coherent code/test/doc slice>
      P0 Step: <2-15 minute executable action> [deps: none] [verify: exact command or inspection]
```

Allowed levels:

- `Goal`: the full user request.
- `Phase`: a major capability, subsystem, or risk area.
- `Task`: a coherent change that can be reviewed independently.
- `Step`: a leaf action the agent can execute now.
- `Probe`: a short discovery leaf used only when implementation order depends on unknown local facts.

Statuses:

- `pending`: not started.
- `in_progress`: exactly one active leaf.
- `blocked`: cannot proceed without a stop-condition decision or artifact.
- `done`: completed and locally verified.
- `cut`: intentionally removed as unnecessary; include the reason.

## Priority Rules

Assign every node a priority:

- `P0`: mandatory for correctness, safety, data integrity, build/test viability, or the user's explicit ask.
- `P1`: required for a complete user-facing workflow, integration, or acceptance criterion.
- `P2`: useful hardening, edge-case coverage, docs, cleanup, or maintainability improvement that supports the change.
- `P3`: optional polish or opportunistic refactor; do only after P0-P2 are complete and the user did not constrain scope.

Priority propagates downward: a child cannot be lower effort than the parent if it is required to satisfy that parent. Raise priority when a lower item becomes a blocker for a higher item.

## Ordering Rules

Choose the next leaf by this order:

1. Unblock P0 correctness, failing tests, broken build, or missing acceptance criteria.
2. Respect explicit dependencies before dependents.
3. Prefer test/proof before implementation when changing behavior.
4. Finish the smallest coherent vertical slice before starting a parallel slice.
5. Prefer high-risk shared contracts before low-risk UI/docs polish.
6. Among equal-priority leaves, choose the one with the least uncertainty and shortest verification loop.

Do not start a P2/P3 leaf while any unblocked P0/P1 leaf remains.

## Recursive Decomposition

Decompose a node when it is too large or ambiguous to execute directly. A leaf is ready only when all of these are true:

- exact files or discovery target are known
- action can be completed in roughly 2-15 minutes
- expected result is clear
- verification or inspection signal is named
- dependencies are known or explicitly absent

If a leaf fails any readiness rule, split it into smaller children before coding. Use `Probe` leaves for local discovery, then replace or refine downstream tasks using evidence from the probe.

When verification fails, recurse under the failing leaf:

```text
P0 Step: Run focused test [blocked by failure]
  P0 Probe: Read failure and identify failing contract
  P0 Step: Patch smallest cause
  P0 Step: Re-run focused test
```

Keep parent nodes open until every required child is `done` or intentionally `cut`.

## Live Checklist Format

Use the plan/update tool when available. If writing the checklist in text, use this compact format:

```markdown
- [ ] P0 Goal: Implement <outcome>
- [ ] P0 Phase: <capability> (depends: none)
- [ ] P0 Task: <slice> (depends: probe-api, verify: npm test path)
- [ ] P0 Step: <leaf action> (depends: none, verify: command)
- [~] P0 Step: <active leaf>
- [x] P1 Step: <verified leaf> (evidence: command passed)
- [!] P0 Step: <blocked leaf> (needs: credential/user decision)
- [-] P3 Step: <cut leaf> (reason: out of scope)
```

Legend:

- `[ ]` pending
- `[~]` in progress
- `[x]` done
- `[!]` blocked
- `[-]` cut

## Start Of Session

1. Announce this skill and any domain skills being used.
2. Read only the instructions and files needed to understand the task.
3. Check `git status --short` before editing and treat existing changes as user-owned unless proven otherwise.
4. Build the first checklist from the request. Start with 3-7 top-level nodes, then recursively expand only the first execution frontier.
5. Pick the first leaf using the priority and ordering rules.

The execution frontier is the set of unblocked leaf nodes whose dependencies are done. Keep the frontier small enough to stay readable.

## Execution Loop

For each active leaf:

1. Mark exactly one leaf `in_progress`.
2. Gather the smallest additional context needed, preferring `rg`, `rg --files`, `sed`, `git show`, and targeted test commands.
3. State the files or area about to be edited before editing.
4. Make the smallest coherent change that advances the leaf.
5. Run the leaf verification.
6. If verification passes, mark the leaf `done`, update parent status, and choose the next frontier leaf.
7. If verification fails, add recursive child leaves for diagnosis and repair, then continue.

Use reasonable assumptions when local context makes the path clear. Do not ask the user to choose between routine implementation details.

## Progress Updates

During longer sessions, report progress in checklist terms:

- active leaf and why it is next
- completed leaves since last update
- verification evidence or current failure
- newly discovered dependencies or priority changes

Do not replace the checklist with a vague status paragraph. The checklist is the source of truth.

## Stop Conditions

Stop and ask only when continuing would risk one of these:

- destructive or irreversible changes, data loss, secrets exposure, external side effects, or production-impacting operations
- a requirement conflict where plausible implementations produce materially different user-visible behavior
- a missing credential, service, dependency, or artifact that cannot be worked around locally
- repeated verification failure after evidence-driven recursive debugging has isolated a blocker that requires user input
- the next required leaf is outside the user's requested scope or permission boundary
- a generation-breaking change (per `yeisme-evolutionary-change-policy`: removing/renaming/retyping a released CLI field, RPC/API method or field, database column, config key, public Go/TS symbol, package path, or skill schema) that has no approved OpenSpec change with migration + deprecation + rollback; stop and create the owning change before continuing

When blocked, report:

- current checklist state
- active blocked leaf and priority
- exact command, diff, or evidence
- root cause or strongest hypothesis
- the smallest user decision or artifact needed to proceed

## Verification

Always run a verification command before claiming completion. Prefer, in order:

1. The focused test for the changed behavior.
2. The package or module test suite covering the changed files.
3. Static checks such as typecheck, lint, validation scripts, or build.
4. A manual inspection with exact files and rationale when no executable check exists.

If a check cannot run, say why and name the next best evidence used.

For formal delivery plan/checklist/work-item workflows, also apply the OpenSpec lifecycle in `docs/workflows/execution-slice-lifecycle.md` before claiming completion. Bounded exploratory MVPs, prototypes, spikes, UI/UX extensions, local refactors, and focused bug investigations may finish with local verification and a concise outcome summary, as long as they remain reversible and do not touch stable contracts, persistence schemas, cross-project boundaries, production behavior, credentials, or external side effects:

- choose the owner first: root `openspec/` is for repository-level design and handoff only; code implementation, test fixes, behavior changes, verification evidence, and closeout belong in the owning `<subproject>/openspec/changes/<change-id>/`
- if formal tracked work was created under `docs/**/checklists`, `docs/**/plans/active`, `work-items/active`, root `openspec/` for code work, or another ad hoc directory, migrate it to the correct owner OpenSpec change before continuing
- update `proposal.md`, `design.md`, `tasks.md`, and `specs/**/spec.md` as needed
- record verification evidence in `tasks.md` or the verification section of `design.md`
- sync any owning readiness, roadmap, README, document-map, or `openspec/specs/` paths
- move completed ordinary changes to the owner archive path, such as `<subproject>/openspec/changes/archive/YYYY-MM-DD-<change-id>/`
- fix stale references that still point to the old task-management paths

## Final Response

Keep the final response short and concrete:

- summarize what changed
- list verification commands and results
- call out unverified areas or residual risk
- mention follow-up only when it directly extends the completed task
