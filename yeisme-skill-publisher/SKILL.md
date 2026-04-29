---
name: yeisme-skill-publisher
description: Use when creating, updating, validating, syncing, or publishing this repository's self-built skills from my-skills/, including preparing them for GitHub distribution through scripts/skills.sh.
---

# Yeisme Skill Publisher

Use this skill when the user asks to create, change, publish, package, install, or share custom project skills for this repository.

## Source And Targets

- Author source skills in `my-skills/<skill-name>/`.
- Sync runnable copies into `.agents/skills/` and mirror them into `.claude/skills/` with `scripts/skills.sh sync-custom`.
- Use `.agents/skills/` for the project agent runtime and `.claude/skills/` for Claude Code. `.claude/skills/` must contain every skill present in `.agents/skills/`.
- Keep `mcp/` for MCP implementations only.

Do not treat `.agents/skills/`, `.claude/skills/`, or `.codex/skills/` as the publishing source for self-built skills. `my-skills/` is the publishing source, `skills/` is reserved for third-party skills, and `.agents/skills/` plus `.claude/skills/` are generated local install targets.

Do not sync self-built project skills into `.codex/skills/` in this repository. Do not put external skills, symlinks, or local runtime copies into `my-skills/`.

## Duplicate Skill Rule

This repository uses a single local install target for project-owned skills:

```text
my-skills/<skill-name>/     source of truth
.agents/skills/<skill-name>/ local runnable copy
.claude/skills/<skill-name>/ Claude Code runnable copy
```

Never mirror the same project-owned skill to:

```text
.codex/skills/<skill-name>/
```

If a skill appears twice in Codex, check for duplicate copies:

```bash
find .codex/skills -maxdepth 2 -name SKILL.md 2>/dev/null | sort
find my-skills -maxdepth 1 -mindepth 1 -type l -print
```

Fix by deleting only generated duplicates for project-owned skills, keeping `my-skills/<skill-name>/`, then run `scripts/skills.sh sync-custom` to regenerate `.agents/skills/<skill-name>/` and `.claude/skills/<skill-name>/`.

## Required Structure

Every self-built skill must include:

```text
my-skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
```

`SKILL.md` must have YAML frontmatter with:

- `name`: same as the directory name.
- `description`: clear trigger conditions, task object, and scope; prefer `Use when ...`.

The body should stay lean:

- when to use the skill
- inputs and outputs
- boundaries
- workflow
- validation
- references to optional scripts or reference files

`agents/openai.yaml` must include:

- `display_name`: human-readable name.
- `short_description`: UI-facing one-line summary matching `SKILL.md`.
- `default_prompt`: a concrete starting prompt the user can run directly.

Do not add per-skill `README.md`, `CHANGELOG.md`, `QUICK_REFERENCE.md`, or `INSTALLATION_GUIDE.md`. Put human-facing authoring guidance in `docs/skills/` instead.

## Workflow

1. Read `my-skills/README.md` and the target skill's `SKILL.md` if it already exists.
2. Confirm the requested capability is a reusable agent workflow. If it is an MCP implementation, put the implementation under `mcp/` and only create a skill if the workflow needs agent guidance.
3. Create or update the skill in `my-skills/<skill-name>/`.
4. Keep metadata in `agents/openai.yaml` consistent with `SKILL.md`.
5. Run:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh sync-custom
scripts/skills.sh list-custom
```

6. If publishing, ensure the GitHub remote exists, commit the `my-skills/`, `scripts/skills.sh`, and docs changes, then push.

## Validation Rules

- Directory name, `name:` frontmatter, and display metadata must agree.
- `description:` must say when the skill should be used and must not be empty.
- `agents/openai.yaml` must contain `display_name`, `short_description`, and `default_prompt`.
- `scripts/skills.sh sync-custom` must not write project-owned skills into `.codex/skills/`.
- `scripts/skills.sh sync-custom` must write project-owned skills into `.agents/skills/` and mirror `.agents/skills/` into `.claude/skills/`.
- `my-skills/` must contain only self-built skill directories plus `README.md`.
- `skills/` must contain only third-party skill directories plus `README.md`.
- Do not add generated caches, local secrets, runtime data, or vendored dependencies.
- Do not create per-skill README files unless the user explicitly asks for human-facing documentation.

## Publishing Notes

For other users, document either:

```bash
git clone <repo-url>
cd yeisme-agent
scripts/skills.sh sync-custom
```

or:

```bash
scripts/skills.sh install-custom <repo-url> [ref]
```
