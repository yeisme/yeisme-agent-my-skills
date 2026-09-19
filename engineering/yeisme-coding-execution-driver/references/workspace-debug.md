## Workspace And Checkpoint Defaults

Choose the workspace before the first write:

- Keep a client/Web lane in the current checkout/current branch when it needs live preview, rendering, browser inspection, or screenshot iteration.
- Put a backend API/service/worker/daemon lane in an isolated `feature/<topic>` branch/worktree when it needs hot reload, long-running processes, migrations, database/cache state, separate ports, or verbose diagnostics.
- Treat API contracts, schemas, generated clients, mocks, fixtures, and shared configuration as single-owner paths. Freeze the contract before splitting lanes.
- Record `workspace_mode`, `owned_paths`, `shared_read_paths`, `forbidden_paths`, startup commands, ports, runtime/data directories, and focused verification in the checklist.

At stable boundaries, use narrow checkpoints in this order: contract ready, previewable client slice, backend slice plus focused tests, and real integration/visual verification. Before a root-owned checkpoint commit, run `git status --short`, `git diff --check`, and the owner-provided focused command; stage only owned paths. A child agent returns the checkpoint manifest and does not commit, push, merge, or delete worktrees.

## Automated Backend Debugging Loop

When the backend lane fails or hot reload becomes unstable, keep the loop bounded and evidence-driven:

1. Start the service with the owning project's real `Taskfile.yml`, package script, or documented command; record the command, process identity, port, health endpoint, log path, and isolated data directory.
2. Wait for readiness, then reproduce with the smallest focused test or request. Do not infer readiness from process existence alone.
3. Inspect structured logs, health output, trace/request IDs, and the smallest relevant diff. Redact credentials, tokens, provider payloads, and private prompts.
4. Patch only the backend lane's owned paths, rerun the focused check, and then rerun the readiness/integration check that crosses the client boundary.
5. Return a compact debug envelope: failure signature, reproduction command, evidence path, patch scope, verification result, and whether the failure is introduced, pre-existing, concurrent, environmental, or ambiguous.

If the same deterministic failure repeats without new evidence, stop the loop at the owning skill's stop condition instead of restarting another backend process or creating a duplicate writer. A worktree does not authorize destructive cleanup or killing an unrelated process.

