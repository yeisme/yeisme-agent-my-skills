---
name: yeisme-claude-skills-layout
description: Use when designing, migrating, reviewing, or enforcing Yeisme repository skills management that keeps .claude and .agents as parallel generated skill homes with active skills plus skills-available libraries.
---

# Yeisme Dual Agent Skills Layout

Use this skill when a repository should keep local agent skills simple, inspectable, and compatible with both Claude Code and generic agent runtimes.

The `yeisme-agent` repository itself uses `my-skills/` as the source of truth for reusable Yeisme skills and `skills/` for imported third-party skills. Downstream product or infrastructure repositories should usually avoid copying that publishing model unless they truly publish skills; they can still use the same runtime home shape.

## Target Layout

Use this structure in the downstream repository:

```text
.claude/
  settings.local.json
  skills/
    <active-runtime-skill>/
      SKILL.md
  skills-available/
    _planning/
      <optional-skill>/
        SKILL.md
    _engineering/
    _quality/
    _security/
    _devops/
    _workflow/
.agents/
  skills/
    <active-runtime-skill>/
      SKILL.md
  skills-available/
    _planning/
      <optional-skill>/
        SKILL.md
    _engineering/
    _quality/
    _security/
    _devops/
    _workflow/
```

Directory roles:

| Path | Role |
| --- | --- |
| `.claude/skills/` | Active runtime skills loaded by Claude Code for the current repository. Keep this small. |
| `.agents/skills/` | Active runtime skills loaded by generic/OpenAI-style agents for the current repository. Keep this in sync with `.claude/skills/`. |
| `.claude/skills-available/` | Optional Claude-discoverable skills grouped by category. This is a discovery library, not a runtime loading directory. |
| `.agents/skills-available/` | Optional generic-agent skills grouped by category. Keep this in sync with `.claude/skills-available/`. |
| `AGENTS.md` | Repository-wide active skill list, skill discovery policy, and validation contract for both homes. |
| `CLAUDE.md` | Claude Code entrypoint that points back to `AGENTS.md` and names `.claude/skills` as the Claude runtime. |

## Required Categories

Use category directories with a leading underscore so they sort before skill names:

- `_planning/`: PRD, architecture, roadmap, plan review, founder/PM review.
- `_engineering/`: coding execution, backend, CLI, docs, project-specific engineering workflows.
- `_quality/`: review, QA, health, debugging, TDD, verification.
- `_security/`: threat modeling, security audit, permission review.
- `_devops/`: release, dependency, deployment, performance, external runtime operations.
- `_workflow/`: shipping, documentation release, repository routing, skill maintenance, general process helpers.

Add another `_category/` only when an existing category would become ambiguous.

## Active Runtime Rules

`.claude/skills/` and `.agents/skills/` should contain only skills that are useful at session start or frequently needed in that repository. Typical active skills:

- session bootstrap and skill discovery
- repository-specific OpenSpec or SDD/TDD workflow
- repository-specific documentation governance
- one or two high-frequency implementation guardrails

Do not put every useful skill in active runtime directories. If a skill is useful only for release, security, performance, QA, design review, or rare maintenance, put it under both `skills-available/<category>/` homes.

## Retired Directories For Downstream Projects

For projects using this layout, do not create or reintroduce:

- `.codex/`
- root `skills/`
- root `my-skills/`
- `skills.profile`
- `skills.profiles/`
- root `agent-skills/`

These directories cause agents to see duplicate or stale skill sources. If they exist from an older migration, move their useful contents into `.claude/skills/` plus `.agents/skills/`, or into both `skills-available/<category>/` libraries, then delete the old directory. In `yeisme-agent`, keep root `my-skills/`, root `skills/`, and legacy profile files because they are the publishing and sync source of truth.

## Discovery Workflow

When a task may need a non-active skill:

1. Read `AGENTS.md` and the active `.claude/skills/<skill>/SKILL.md` or `.agents/skills/<skill>/SKILL.md` files that match the current task.
2. List optional candidates without opening everything:

```bash
find .claude/skills-available .agents/skills-available -mindepth 2 -maxdepth 2 -type d | sort
```

3. Open only the specific candidate `SKILL.md` that matches the task:

```bash
sed -n '1,220p' .claude/skills-available/_quality/review/SKILL.md
```

4. Do not bulk-load `.claude/skills-available/`.
5. Do not bulk-load `.agents/skills-available/`.
6. Do not promote an optional skill into active runtime directories unless `AGENTS.md` is updated to declare it active and both homes are synced.

## Validation Contract

Every repository using this layout should provide a lightweight validation command, usually through `Taskfile.yml` or `scripts/skills.sh`, that checks:

- `AGENTS.md` declares the active skill names in a machine-readable block.
- every declared active skill exists under `.claude/skills/` and `.agents/skills/`.
- active runtime directories contain no undeclared skill directories unless explicitly accepted as local runtime-only skills.
- `.claude/skills` and `.agents/skills` are real directories, not symlinks to another runtime.
- `.claude/skills-available/` and `.agents/skills-available/` exist.
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
scripts/skills.sh list-available
```

## Migration Checklist

1. Inventory current runtime and source directories:

```bash
find .claude .agents skills my-skills skills.profiles agent-skills -maxdepth 3 -type d 2>/dev/null | sort
```

2. Choose the small active runtime set and move it into `.claude/skills/` and `.agents/skills/`.
3. Move optional skills into `.claude/skills-available/<category>/` and `.agents/skills-available/<category>/`.
4. Delete retired directories after confirming their useful contents were moved.
5. Update `AGENTS.md`, `CLAUDE.md`, docs, and any OpenSpec workflow notes.
6. Add or update `task skills:validate` and `task skills:list`.
7. Run validation and record results in the change notes.

## Output Style

When applying or reviewing this policy, report:

- active runtime skills under `.claude/skills/` and `.agents/skills/`
- optional category layout under both `skills-available/` homes
- retired directories removed or still present
- validation commands run and their results
- any skill that should be promoted or demoted, with reason
