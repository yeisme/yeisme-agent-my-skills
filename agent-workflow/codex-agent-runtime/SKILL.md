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

## Context-Isolated Feature Delivery

When a feature requires frequent integration/component/system/e2e tests, or
when test logs and repeated implementation loops would quickly fill the root
task context, use one shallow Codex DAG instead of developing inline through a
long-lived goal:

```text
root acceptance packet
  -> implementer(single child turn, one complete bounded feature)
  -> test-engineer(independent verification and evidence)
  -> root acceptance or compact failure handoff
  -> same implementer(repair) -> test-engineer(rerun)
```

Rules:

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
