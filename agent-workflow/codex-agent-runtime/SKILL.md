---
name: codex-agent-runtime
description: Use when configuring, operating, or instructing Codex in Yeisme projects, including skill loading, tool-name mapping from Claude Code style skills, MCP Gateway client setup, multi-agent usage, profile sync, and safe command examples.
---

# Codex Agent Runtime

Use this skill when a task is being handled by Codex or when documentation must explain how Codex should use Yeisme skills, MCP Gateway, and local tools.

## Workflow

1. Load applicable skills from the current session metadata or generated runtime homes. Project-owned source skills live under `.skills/yeisme/`; do not create duplicate project skills under `.codex/skills`.
2. When a skill mentions Claude Code tools, map them to Codex equivalents:
   - `TodoWrite` -> `update_plan`
   - `Bash` -> shell command tool
   - `Read` / `Edit` / `Write` -> native file tools, with `apply_patch` for manual edits
   - `Task` -> multi-agent dispatch when available; otherwise continue inline
   - `Skill` -> follow the loaded skill instructions directly
3. Prefer CLI contracts before prose parsing: use `--json`, `--agent`, or `--events` when a Yeisme CLI exposes them.
4. Configure MCP access through Gateway-rendered client config rather than hand-writing endpoint blocks.

## Fast Local Iteration Default

Treat an ordinary request to build, extend, fix, refactor, or test a feature as
authorization to implement it in the local, non-production workspace. A new
module, internal/local API, migration source file, mock, test, or codebase
expansion is not an approval gate.

Proceed directly with scoped source, test, fixture, documentation, local
configuration, and disposable test-data changes; use the existing project
pattern, choose a minimal reversible implementation, and run the narrowest
relevant verification. Do not ask the user to approve routine implementation
details or turn a feature request into a design-review sequence. For an
external integration, implement and verify the adapter with a mock, sandbox, or
test endpoint before enabling a live path.

Pause only for a real high-impact side effect: deleting or irreversibly
migrating non-disposable data; credentials; production or live access-control
changes; deploy/publish/push actions; charges; real outbound communication; or
bulk/destructive external writes. A current request that names the exact target
and side effect supplies the required authority, subject to platform safety
requirements. Preserve unrelated dirty worktree changes.

See `docs/workflows/rapid-local-iteration.md` for the full decision matrix.

## Context-Isolated Feature Delivery

Use this workflow only after the current user explicitly requests a `subagent`,
`子 agent`, `子agent`, or delegated/parallel work. Test volume, long logs,
repeated implementation loops, task complexity, and this skill itself never
authorize a child agent. Without that request, keep the same work in the root
thread.

After authorization, a feature with frequent integration/component/system/e2e
tests, noisy logs, or repeated implementation loops may use one shallow Codex
DAG instead of developing inline through a long-lived goal:

```text
root acceptance packet
  -> implementer(single child turn, one complete bounded feature)
  -> test-engineer(independent verification and evidence)
  -> root acceptance or compact failure handoff
  -> same implementer(repair) -> test-engineer(rerun)
```

Rules:

- After user authorization, use the `balanced` model-and-effort route unless
  the user pins a cap: Luna / low for exploration and repetitive checks, Luna /
  medium for high-volume verification, Terra / medium for routine implementation
  and research, and Terra / high only for bounded multi-module implementation.
  Use Sol / medium for spec, task decomposition, acceptance criteria, and TDD
  design; Sol / high for deep debugging, security, high-risk review,
  concurrency, and integration; Sol / max only for core architecture, durable
  contracts or migrations, critical trust boundaries, and costly-to-reverse
  cross-project design. A capability mismatch may trigger one evidence-backed
  tier or effort upgrade per failure loop. Every Sol / max dispatch must state
  why it is core design; `ultra` requires an explicit user request.
- A root goal records only the user objective, accepted scope, current stage,
  and final status. It must not retain full implementation narration or test
  output.
- The implementer is the only tracked-file writer for the feature. It owns the
  production change plus related test, fixture, and required documentation
  edits, and should finish the bounded feature in one child turn when possible.
- The test engineer does not edit tracked source, tests, fixtures, snapshots,
  or config. It runs the real commands and writes only diagnostic/build/test
  artifacts and redacted integration-test evidence.
- The root reads compact worker envelopes and evidence summaries first. On
  failure, return only the command, exit code, failure signature, evidence path,
  and smallest useful log excerpt to the same implementer.
- A timeout is not permission to start another writer. Confirm liveness or close
  the original worker before rerouting.

Use `route-agents` with `context_isolated_delivery: true`; add
`integration_test_heavy: true` when verification is slow or verbose.

## Optional Child Thread Goal

`child_goal_policy` is an additive dispatch field with `schema_version: "1.0"`.
It defaults to `disabled`; only an explicitly authorized current user may set
`create_if_available`. When enabled, a child may inspect and manage at most one
thread-local goal if the runtime offers a goal tool. The goal objective must be
a strict subset of the dispatch scope ceiling; `descendants` remains `false`.
Do not set a token budget unless
the user explicitly requested one, overwrite an incompatible active goal, or
require a goal tool in another runtime.

Report `created`, `reused`, `unavailable`, or `collision` through optional
`goal_report`; use `active`, `waiting_root`, `complete`, `blocked`, or
`liveness_unknown` for state. `complete` is a candidate handoff to root, not
final acceptance. Mark `blocked` only after the same blocker occurs in three
consecutive goal turns. A timeout or interrupt neither cancels the goal nor
releases a writer lease, and the goal never resets repair, model-upgrade, or
circuit-breaker budgets. Root retains all scope/permission changes, user
decisions, external actions, descendants, role or model upgrades, and final
acceptance.

## Staged Verification

Keep implementation feedback separate from final acceptance:

1. `implementing`: the implementer runs only focused tests and necessary local
   checks for the owned slice. Do not repeatedly run repository-wide lint,
   full builds, complete e2e, or strict global validation.
2. `slice-ready`: the implementer returns changed paths, focused verification,
   skipped final gates, and known risks.
3. `verification`: an independent test engineer runs the acceptance-specific
   integration/component/system/e2e commands on a stable diff and records
   evidence without editing tracked files.
4. `final-gate`: after code, direct tests, and required docs are stable, run the
   owning subproject's full lint, build, typecheck, critical e2e, and OpenSpec
   validation before submission or release.

Before repairing a final-gate failure, classify it as `introduced`,
`pre_existing`, `concurrent`, `environment`, or `ambiguous`. Only
`introduced` failures directly authorize the same implementer to patch the
owned scope. Never change unrelated business logic merely to clear a global
lint warning.

See `docs/workflows/codex-subagent-feature-delivery.md` for writer leases,
progress fields, failure attribution, and repair routing.

## Commands

```bash
codex
mcp-gateway client doctor --client codex --registry ../registry.json
mcp-gateway client config codex --registry ../registry.json --instructions
mcp-gateway client config codex --registry ../registry.json --policy --json
scripts/skills.sh list-runtime
scripts/skills.sh profile show <owner>
```

## Boundaries

- Do not expose local execution wrappers, aliases, hidden prompts, private tool arguments, raw provider payloads, or full chain-of-thought.
- Do not sync project-owned Yeisme skills into `.codex/skills`; use `.agents/skills` and `.claude/skills` runtime homes generated from profiles by `scripts/skills.sh`.
- Do not bypass MCP route policy with direct shell calls when Gateway declares an MCP-first route.
- Do not use a long-lived root goal as the implementation worker, test runner,
  or log archive for a feature that can be handed to bounded child agents.
