---
name: yeisme-git-worktree-flow
description: Use when developing this repository with Git flow style branching, adaptive current-workspace or git-worktree isolation, staged checkpoints, Taskfile automation, and nerdctl compose.yml based service orchestration.
---

# Yeisme Git Worktree Flow

Use this skill when planning, implementing, reviewing, or shipping changes in this repository and the work needs a disciplined branch/worktree/container workflow. Choose the workspace from the work's runtime behavior instead of isolating every task mechanically.

## Defaults

- Use Git flow style branches:
  - `main`: stable integration branch.
  - `develop`: default shared integration branch for every Yeisme subproject; start normal feature/fix work from here and keep `.gitmodules` tracking `develop`.
  - `feature/<name>`: normal feature work.
  - `fix/<name>`: bug fixes.
  - `hotfix/<name>`: urgent production fixes from `main`.
  - `release/<version>`: release stabilization.
- Prefer GitPulse for repository status, branch/worktree inspection, commit review, and PR-oriented flows before falling back to raw `git`/`gh`.
- Prefer `git worktree` for isolated parallel work instead of switching one dirty checkout between tasks.
- Prefer `Taskfile.yml` for project commands.
- Prefer `nerdctl compose` with `compose.yml` for local services and deployment-like orchestration.
- Keep command behavior reproducible and discoverable through tasks instead of ad hoc shell notes.

## Workspace Placement Defaults

Resolve the workspace mode before editing. The following defaults apply unless the user or the owning subproject explicitly requires another mode:

| lane | default workspace | reason | minimum guardrail |
| --- | --- | --- | --- |
| client/web UI that needs live preview, rendering, browser inspection, or screenshot iteration | current checkout and current branch | the preview process, browser session, and uncommitted visual work remain immediately inspectable | one writer, preserve the existing dev server, and do not switch branches underneath it |
| backend API, service, worker, daemon, migration, or long-running hot-reload process | isolated `feature/<topic>` branch and worktree | backend reloads, ports, databases, generated files, and logs must not disturb the UI preview lane | separate ports, runtime/data directories, process group, and logs; no writes to the UI worktree |
| API contract, schema, typed client, mock, or shared fixture | the owner-selected contract workspace | these files are shared boundaries and must have one canonical writer | freeze the contract before implementation lanes; generated outputs come from the contract |
| review, investigation, or verification only | no writer worktree | read-only work should not acquire a write lease | do not modify tracked files, tests, fixtures, snapshots, or config |

The backend default is about runtime isolation as well as Git isolation. A second worktree is not sufficient if both processes still share a port, database, cache, temp directory, or generated-output directory.

Use the current workspace for backend work when it must consume current uncommitted changes, the project cannot run from a second checkout, or the user explicitly requests it. Use an isolated worktree for client work when the preview has a reproducible independent runtime, the current checkout is owned by another writer, or the user explicitly requests isolation. Record the reason for every override.

## Parallel Lane Protocol

For a frontend/client plus backend task:

1. Inspect the repository and identify the contract owner, preview command, backend command, ports, runtime/data directories, and test entrypoints.
2. Freeze or identify the API/schema contract before the implementation lanes diverge.
3. Keep the client lane in the current workspace when it needs live preview/rendering. Use mock/service-layer responses until the real backend is ready.
4. Put the backend lane in an isolated worktree when it owns a hot-reload process, service state, migrations, or long-running diagnostics. Start it from the same contract-ready base.
5. Integrate in a small vertical slice, then rerun the client preview and backend focused checks together. Never make the frontend depend on an untracked backend-only file.

## Staged Checkpoint Commits

Long-running development should create narrow local checkpoints at these boundaries when repository policy and user authorization allow commits:

1. contract or interface ready;
2. previewable client slice ready;
3. backend behavior and focused tests ready;
4. real integration and visual verification ready.

Before each checkpoint, run `git status --short`, `git diff --check`, and the owner-provided focused command; stage only owned paths and use one intent per commit. Do not push, open a PR, merge, or delete a worktree as part of checkpointing. A child agent returns a checkpoint manifest to root; root owns the actual commit under the repository's authorization rules.

## Worktree Rules

Before starting substantial work:

1. Check current state:

```bash
git status --short
git branch --show-current
git worktree list
```

2. Apply `Workspace Placement Defaults`. If the selected mode is isolated, create a worktree:

```bash
git fetch origin
git worktree add ../yeisme-agent-<topic> -b feature/<topic> develop
cd ../yeisme-agent-<topic>
```

3. Keep each worktree focused on one branch and one outcome.
4. Do not delete or overwrite another user's worktree.
5. Remove a completed worktree only after the branch is merged or no longer needed:

```bash
git worktree remove ../yeisme-agent-<topic>
git branch -d feature/<topic>
```

If a worktree has uncommitted changes, stop and inspect before cleanup.

For a backend hot-reload lane, verify the isolation before starting the process:

```bash
git worktree list
lsof -i :<backend-port>
```

Use the project's real task or start command after this check. Do not kill an unrelated process or reuse a data directory merely to make a local check pass.

## Git Flow Workflow

For a normal feature:

```bash
git fetch origin
git switch -c feature/<topic> origin/develop
```

For a fix:

```bash
git fetch origin
git switch -c fix/<topic> origin/develop
```

For a hotfix:

```bash
git fetch origin
git switch -c hotfix/<topic> origin/main
```

Commit narrowly:

```bash
git status --short
git add <owned-files>
git commit -m "feat(scope): summary"
```

Push and open review:

```bash
git push -u origin <branch>
```

Use CLI plus skills for GitHub work by default:

```bash
gh pr create --base develop --head <branch>
```

Do not use GitHub MCP when GitPulse or `gh` can perform the job with less context and clearer auditability. For stable releases, open a separate `develop` → `main` PR after validation.

## Taskfile Policy

Prefer adding or using tasks for repeated operations:

```text
Taskfile.yml
Taskfile.<domain>.yml
```

Task names should be short and stable:

- `up`
- `down`
- `ps`
- `logs`
- `health`
- `config`
- `test`
- `lint`
- `build`
- `cleanup`

Use task dependencies for orchestration instead of long copied command sequences. Keep environment variables explicit and document required `.env.example` values near the service that uses them.

## nerdctl Compose Policy

Prefer `nerdctl compose` and `compose.yml` for service lifecycle when the project needs containers.

Expected files:

```text
<service-or-domain>/
  Taskfile.yml
  compose.yml
  .env.example
```

Taskfile commands should wrap compose operations:

```bash
task up
task down
task ps
task logs
task health
```

Compose rules:

- Name services clearly by role.
- Keep persistent data under explicit runtime/data directories that are ignored by Git.
- Keep secrets out of compose files; use environment files or documented variables.
- Add health checks when a service is depended on by another service.
- Prefer small compose files per domain over one opaque root compose file.
- Use `nerdctl compose` unless the local project explicitly requires Docker Compose.

## File Placement

- Worktree and Git workflow guidance belongs in skills or docs.
- Project command entry points belong in `Taskfile.yml`, `cli/`, or domain-specific task files.
- Container orchestration belongs beside the owned service or domain.
- MCP service code belongs in `mcp/<name>/`.
- If an MCP owns a tightly coupled CLI, place it under `mcp/<name>/cli/`.

## Review Checklist

Before finalizing:

- Branch name matches Git flow intent.
- Work happened in the right worktree or the current checkout was clean enough.
- Workspace mode matches the lane: current checkout for preview-critical client work, isolated worktree for backend hot-reload work unless an override is recorded.
- Backend ports, runtime/data directories, process ownership, and logs are isolated from the client lane.
- Only owned files are staged.
- Checkpoint commits are narrow, ordered, and do not include unrelated user changes.
- Repeated commands are captured in Taskfile tasks.
- Container lifecycle uses `nerdctl compose` and `compose.yml` where applicable.
- Runtime data, secrets, generated files, and local caches are not staged.
- Validation commands ran and results are reported.

## When Not To Use

Do not use this skill for tiny read-only questions, one-off shell checks, or repositories that explicitly use a different branching and orchestration model.
