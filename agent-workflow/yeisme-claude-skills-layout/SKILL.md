---
name: yeisme-claude-skills-layout
description: Use when designing, migrating, reviewing, or enforcing Yeisme repository skills management that keeps .claude and .agents as parallel active skill homes managed by skillctl.
---

# Yeisme Dual Agent Skills Layout

Use this skill when a repository should keep local agent skills simple, inspectable, and compatible with both Claude Code and generic agent runtimes while managing skill changes through `skillctl`.

The `yeisme-agent` repository itself uses `.skills/yeisme/` as the source of truth for reusable Yeisme skills and `.skills/imported/` for imported third-party skills. Downstream product or infrastructure repositories should usually avoid copying that publishing model unless they truly publish skills; they can still use the same runtime home shape.

## Target Layout

Use this structure in the downstream repository:

```text
.claude/
  settings.local.json
  skills/
    <active-runtime-skill>/
      SKILL.md
.agents/
  skills/
    <active-runtime-skill>/
      SKILL.md
.skillctl/
  available/
    _agent-workflow/
      <inactive-reviewed-skill>/
        SKILL.md
    _backend/
    _devops/
    _frontend/
    _reference/
    _testing/
```

Directory roles:

| Path | Role |
| --- | --- |
| `.claude/skills/` | Active runtime skills loaded by Claude Code for the current repository. Keep this small. |
| `.agents/skills/` | Active runtime skills loaded by generic/OpenAI-style agents for the current repository. Keep this in sync with `.claude/skills/`. |
| `.skillctl/available/` | Reviewed inactive skill inventory grouped by category. This is managed by `skillctl`, not loaded by default. |
| `AGENTS.md` | Repository-wide active skill list, skill discovery policy, and validation contract for both homes. |
| `CLAUDE.md` | Claude Code entrypoint that points back to `AGENTS.md` and names `.claude/skills` as the Claude runtime. |

## Required Categories

Use category directories with a leading underscore so they sort before skill names:

- `_agent-workflow/`: agent process, OpenSpec, plan execution, repository routing, skill governance, multi-agent coordination.
- `_backend/`: backend, CLI runtime, MCP, API, persistence, and project-specific implementation workflows.
- `_devops/`: release, deployment, CI, dependency, performance, and external runtime operations.
- `_frontend/`: frontend, TUI, design system, UI implementation, and visual QA workflows.
- `_reference/`: output contracts, examples, research, diagrams, command references, and low-frequency knowledge packs.
- `_testing/`: TDD, debugging, QA, review, health, security audit, and completion verification.

Add another `_category/` only when an existing category would become ambiguous.

## Active Runtime Rules

`.claude/skills/` and `.agents/skills/` should contain only skills that are useful at session start or frequently needed in that repository. Typical active skills:

- session bootstrap and skill discovery
- repository-specific OpenSpec or SDD/TDD workflow
- repository-specific documentation governance
- one or two high-frequency implementation guardrails

Do not put every useful skill in active runtime directories. If a skill is useful only for release, security, performance, QA, design review, or rare maintenance, keep it in source or `.skillctl/available/<category>/` and load it intentionally when needed.

## Retired Directories For Downstream Projects

For projects using this layout, do not create or reintroduce:

- `.codex/`
- root `.skills/`
- root `skills/`
- root `my-skills/`
- root `skills.profiles/`
- root `agent-skills/`

These directories cause agents to see duplicate or stale skill sources in downstream repositories. If they exist from an older migration, move their useful contents into `.claude/skills/` plus `.agents/skills/`, source directories, or `.skillctl/available/<category>/`, then delete the old directory. In `yeisme-agent`, keep root `.skills/yeisme/`, `.skills/imported/`, `.skills/profiles/root.txt`, and `.skills/profiles/targets/<subproject>.txt` because `.skills/` is the publishing and sync source of truth.

## Discovery Workflow

When a task may need a non-active skill:

1. Read `AGENTS.md` and the active `.claude/skills/<skill>/SKILL.md` or `.agents/skills/<skill>/SKILL.md` files that match the current task.
2. List inactive reviewed candidates without opening everything:

```bash
skillctl skills available --target root
```

3. Open only the specific candidate `SKILL.md` that matches the task:

```bash
sed -n '1,220p' .skillctl/available/_testing/review/SKILL.md
```

4. Do not bulk-load `.skillctl/available/`.
5. Do not promote an inactive skill into active runtime directories unless `AGENTS.md` is updated to declare it active and both homes are synced.

## Validation Contract

Every repository using this layout should provide a lightweight validation command, usually through `Taskfile.yml` or `scripts/skills.sh`, that checks:

- `AGENTS.md` declares the active skill names in a machine-readable block.
- every declared active skill exists under `.claude/skills/` and `.agents/skills/`.
- active runtime directories contain no undeclared skill directories unless explicitly accepted as local runtime-only skills.
- `.claude/skills` and `.agents/skills` are real directories, not symlinks to another runtime.
- `.skillctl/available/` is managed only by `skillctl` when reviewed inactive inventory is needed.
- retired directories do not exist.

Suggested `AGENTS.md` block:

```markdown
Active root runtime skills:

<!-- runtime-skills:start -->
- `using-superpowers`
- `find-skills`
- `project-openspec-sdd-tdd`
<!-- runtime-skills:end -->
```

Suggested validation commands:

```bash
task skills:validate
task skills:list
```

If a project has no Taskfile, use a small `scripts/skills.sh` with commands equivalent to:

```bash
scripts/skills.sh validate-runtime
scripts/skills.sh list-runtime
skillctl skills available --target root
```

## Migration Checklist

1. Inventory current runtime and source directories:

```bash
find .claude .agents .skillctl .skills agent-skills -maxdepth 3 -type d 2>/dev/null | sort
```

2. Choose the small active runtime set and move it into `.claude/skills/` and `.agents/skills/`.
3. Move inactive reviewed skills into source directories or `.skillctl/available/<category>/`.
4. Delete retired directories after confirming their useful contents were moved.
5. Update `AGENTS.md`, `CLAUDE.md`, docs, and any OpenSpec workflow notes.
6. Add or update `task skills:validate` and `task skills:list`.
7. Run validation and record results in the change notes.

## Output Style

When applying or reviewing this policy, report:

- active runtime skills under `.claude/skills/` and `.agents/skills/`
- reviewed inactive inventory under `.skillctl/available/`
- retired directories removed or still present
- validation commands run and their results
- any skill that should be promoted or demoted, with reason
