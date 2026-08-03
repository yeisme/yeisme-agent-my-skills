---
name: yeisme-claude-skills-layout
description: Use when designing, migrating, reviewing, or enforcing Yeisme repository skills management that keeps .claude and .agents as parallel generated runtime homes sourced from .skills and declarative profiles through scripts/skills.sh.
---

# Yeisme Dual Agent Skills Layout

Keep source, declaration, and runtime responsibilities separate.

## Layout

```text
.skills/
  yeisme/                      project-owned source skills
    <project>/                 optional first-party Git submodule with its own modules
  imported/                    reviewed third-party source skills
  profiles/
    root.txt                   root active declaration
    targets/<owner>.txt        subproject active declaration
.agents/skills/                generated generic-agent runtime
.claude/skills/                generated Claude runtime
```

Subprojects use the same two runtime homes. They do not need their own source inventory unless they independently publish skills.

## Rules

- Keep `.skills/yeisme/` and `.skills/imported/` as the only source layers.
- First-party product collections may be mounted as Git submodules below `.skills/yeisme/<project>/`; they remain part of the Yeisme source layer and must not duplicate Skill names in the parent source.
- Keep `.agents/skills/` and `.claude/skills/` as real generated directories, never symlinks and never maintenance sources.
- Keep active runtime small. Leave release-only, audit-only, design-only, or rare skills in the source layer for on-demand loading.
- Do not create `.skillctl/available/`, root `skills/`, `my-skills/`, `agent-skills/`, or project-owned `.codex/skills/` duplicates.
- Preserve `openspec-*` runtime skills only through the OpenSpec workflow owner; ordinary profile sync must not silently delete or invent them.

## Discovery

When an inactive skill may fit, search source metadata and read only the matching file:

```bash
scripts/skills.sh search "<task terms>"
scripts/skills.sh resolve <skill-name>
sed -n '1,220p' <resolved-path>/SKILL.md
```

Do not copy an inactive skill into runtime merely to use it once. Promote it only through the owner profile when repeated session-start value justifies the context cost.

## Profile And Sync

```bash
scripts/skills.sh profile show root
scripts/skills.sh profile show <owner>
scripts/skills.sh profile add <owner> <skill-name>
scripts/skills.sh profile remove <owner> <skill-name>
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
```

`<owner>` matches the repository path represented under `.skills/profiles/targets/`, for example `cli/cohors`.

## Validation

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh validate-runtime
scripts/skills.sh validate-subprojects-runtime
```

Validation must check:

- every profile entry resolves to one unique source;
- every profile owner directory exists;
- `.agents/skills` and `.claude/skills` contain the same names and bytes;
- runtime contents match the declared profile plus explicitly owned generated skills;
- retired duplicate directories are absent.
- source submodules and their `.gitmodules` metadata are allowed; generated runtimes must still be derived from the same stable Skill names.

## Migration

1. Inventory all source, profile, and runtime directories.
2. Move project-owned skills to `.skills/yeisme/` and third-party skills to `.skills/imported/`.
3. Express each owner active set in its profile.
4. Remove duplicate inactive mirrors and retired runtime sources.
5. Sync both runtime homes and run all validation commands.

## Output

Report source locations, active profiles, generated runtime sets, removed duplicate paths, and validation results.
