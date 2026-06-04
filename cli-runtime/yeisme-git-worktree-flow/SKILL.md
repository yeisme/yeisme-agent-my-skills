---
name: yeisme-git-worktree-flow
description: Use when developing this repository with Git flow style branching, git worktree isolation, Taskfile automation, and nerdctl compose.yml based service orchestration.
---

# Yeisme Git Worktree Flow

Use this skill when planning, implementing, reviewing, or shipping changes in this repository and the work needs a disciplined branch/worktree/container workflow.

## Defaults

- Use Git flow style branches:
  - `main`: stable integration branch.
  - `develop`: optional shared integration branch when multiple features are active.
  - `feature/<name>`: normal feature work.
  - `fix/<name>`: bug fixes.
  - `hotfix/<name>`: urgent production fixes from `main`.
  - `release/<version>`: release stabilization.
- Prefer `git worktree` for isolated parallel work instead of switching one dirty checkout between tasks.
- Prefer `Taskfile.yml` for project commands.
- Prefer `nerdctl compose` with `compose.yml` for local services and deployment-like orchestration.
- Keep command behavior reproducible and discoverable through tasks instead of ad hoc shell notes.

## Worktree Rules

Before starting substantial work:

1. Check current state:

```bash
git status --short
git branch --show-current
git worktree list
```

2. If the current checkout is dirty or the work is independent, create a worktree:

```bash
git fetch origin
git worktree add ../yeisme-agent-<topic> -b feature/<topic> main
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

## Git Flow Workflow

For a normal feature:

```bash
git fetch origin
git switch -c feature/<topic> origin/main
```

For a fix:

```bash
git fetch origin
git switch -c fix/<topic> origin/main
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
gh pr create --base main --head <branch>
```

Do not use GitHub MCP when `gh` can perform the job with less context and clearer auditability.

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
- Only owned files are staged.
- Repeated commands are captured in Taskfile tasks.
- Container lifecycle uses `nerdctl compose` and `compose.yml` where applicable.
- Runtime data, secrets, generated files, and local caches are not staged.
- Validation commands ran and results are reported.

## When Not To Use

Do not use this skill for tiny read-only questions, one-off shell checks, or repositories that explicitly use a different branching and orchestration model.
