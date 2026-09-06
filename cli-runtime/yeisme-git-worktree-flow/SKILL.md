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

## Hygiene: Temporary Branches And Worktrees

Temporary lanes are disposable by design and must not outlive their wave:

- Name them recognizably: `wt/<topic>`, `tmp/<topic>`, snapshot or `*-wip-*` branches. Delete them at lane closeout.
- `/tmp` and the root `temp/` directory are ephemeral scratch space. Branch refs are the durable layer: commit in-progress work to a branch before leaving a worktree behind. Removing a worktree only destroys unique work when its HEAD is detached and the tree is dirty.
- Every commit in this workspace runs the shared advisory hook `.githooks/post-commit` (installed everywhere by `scripts/install-git-hooks.sh`): it prunes dead worktree registrations and prints a one-line nudge when merged branches or dead worktrees exist. It never deletes anything; disable per command with `YEISME_GIT_HOOKS=0`.
- Deep sweep: `scripts/worktree-doctor.sh` reports extra/dead/detached-dirty worktrees, merged branches, redundant local mirrors, and unmerged branches across the root repository and all submodules. `--prune` performs only safe cleanup (`git worktree prune` plus `git branch -d`, which git refuses for anything unmerged); `--strict` turns warnings into a non-zero exit for gates.

### Staleness Classification Before Removal

1. Is the worktree's base commit an ancestor of the integration branch HEAD? Then the wave landed on top and the worktree's dirty drafts are residue. Confirm by diffing key files against the current checkout.
2. Are the dirty files identical to current HEAD content (typical: cross-repo skills sync residue in `.agents/skills` / `.claude/skills`)? The edits already landed; discard them with the worktree.
3. Is the branch ahead of the correct default branch (resolve `origin/HEAD`; several subprojects default to `develop`, not `main`)?
   - `ahead=0` — merged: remove the worktree, then `git branch -d`.
   - `ahead>0` — unmerged real work: keep the branch (it survives worktree removal), keep its worktree if it holds uncommitted state, and hand the merge-or-discard decision to the owning lane.
   - Detached HEAD plus dirty files is the only state where removal destroys unique work — commit it to a branch first.

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
- Temporary branches (`wt/*`, `tmp/*`, snapshots, `*-wip-*`) were removed at closeout, and `scripts/worktree-doctor.sh` reports no merged branches or dead worktrees for the touched repositories.
- No abandoned worktree holds the only copy of unmerged commits (detached HEAD with a dirty tree); anything worth keeping was committed to a branch first.

## When Not To Use

Do not use this skill for tiny read-only questions, one-off shell checks, or repositories that explicitly use a different branching and orchestration model.
