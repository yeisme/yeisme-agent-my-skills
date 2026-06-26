---
name: pinax-project-workspace-operator
description: Use when an agent needs to manage Pinax project workspaces, learning packs, subprojects, local boards, project work items, personal daily/weekly/monthly plans, TaskBridge action drafts, or plan snapshots.
---

# Pinax Project Workspace Operator

Operate Pinax local project workspaces and planning surfaces. Project Workspace is local-first Markdown plus CLI-authored `.pinax` project metadata; it is not a remote issue tracker.

## Use When

- The request mentions `pinax project`, project workspace, learning pack, subproject, board, work item, planning, daily/weekly/monthly plan, TaskBridge action drafts, or plan snapshots.
- The user wants to organize research, learning, client, content, or tool-candidate work inside one vault.
- The command family is `pinax project` or `pinax plan`.

## Command Patterns

```bash
pinax project create research --name "Research" --notes-prefix notes/research --vault ./my-notes --json
pinax project list --vault ./my-notes --json
pinax project learning init investing stock-learning --title "学习炒股的全部笔记" --project-name "学习炒股" --preset stock-learning --vault ./my-notes --json
pinax project subproject create research stock-learning --title "Stock Learning" --template scenario --vault ./my-notes --json
pinax project subproject show research stock-learning --vault ./my-notes --json
pinax project board configure research --columns inbox,next,doing,blocked,review,done --vault ./my-notes --json
pinax project board show research --subproject stock-learning --vault ./my-notes --agent
pinax project item add research "Read annual report" --subproject stock-learning --column next --vault ./my-notes --json
pinax project item move item_abc123 doing --vault ./my-notes --json
pinax plan daily --dry-run --vault ./my-notes --json
pinax plan weekly --save --yes --vault ./my-notes --json
pinax plan monthly --dry-run --vault ./my-notes --json
pinax plan actions --from daily --taskbridge --save --vault ./my-notes --json
pinax plan snapshot --vault ./my-notes --json
```

## Workflow

1. Resolve vault and active project state with `pinax vault list --json`, `pinax project list --json`, or `pinax project board show <project> --json`.
2. For new workspace setup, create or show the project first, then create subprojects or learning packs.
3. For learning packs, choose an explicit preset such as `learning` or `stock-learning`; keep educational notes separate from recommendations or investment decisions.
4. For boards, use `project board show` before changing columns or moving items.
5. For work items, only mutate managed project items returned by Pinax. Do not edit Markdown task lines or board metadata by hand.
6. Before archive or broad project cleanup, create `pinax version snapshot --message "before project workspace changes" --json` and require explicit approval.
7. For plan commands, start with `--dry-run`; only use `--save` or `--yes` when the user approved writing plan outputs.

## Safety Boundaries

- Do not sync project items to GitHub, Gitea, TaskBridge, or providers unless a separate approved integration does that through its owner.
- Do not hand-edit `.pinax/projects/**`, `.pinax/project-workspaces/**`, board config, or planning snapshots.
- Do not create financial, medical, or legal advice claims from learning packs; keep them as study notes and source tracking.
- Do not execute TaskBridge action drafts from Pinax; Pinax only generates drafts.

## Validation

- After project setup: `pinax project subproject show <project> <slug> --json`.
- After board changes: `pinax project board show <project> --json`.
- After plan writes: `pinax plan snapshot --json` or the relevant `pinax plan <period> --dry-run --json` shows expected state.
