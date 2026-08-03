---
name: yeisme-skill-publisher
description: Use when creating, updating, validating, syncing, or publishing this repository's self-built skills from .skills/yeisme/, including preparing them for GitHub distribution through scripts/skills.sh.
---

# Yeisme Skill Publisher

Use this skill when the user asks to create, change, publish, package, install, or share custom project skills for this repository.

## Source And Targets

- Author source skills in `.skills/yeisme/<module>/<skill-name>/`, or in a first-party public submodule mounted at `.skills/yeisme/<project>/<module>/<skill-name>/`.
- Assign runnable copies through `.skills/profiles/root.txt` and `.skills/profiles/targets/<subproject>.txt`, then materialize them with `scripts/skills.sh`.
- Use `.agents/skills/` and `.claude/skills/` as generated active runtime copies. Keep inactive reviewed skills in the source layer.
- Keep `mcp/` for MCP implementations only.

Do not treat `.agents/skills/`, `.claude/skills/`, or `.codex/skills/` as the publishing source for self-built skills. `.skills/yeisme/` is the publishing source, `.skills/imported/` is reserved for third-party/imported skills, profile files define scope, and `.agents` plus `.claude` are generated runtime homes.

Do not sync self-built project skills into `.codex/skills/` in this repository. Do not put external skills, symlinks, or local runtime copies into `.skills/yeisme/`.

## Duplicate Skill Rule

This repository uses a single local install target for project-owned skills:

```text
.skills/yeisme/<module>/<skill-name>/     source of truth
.skills/yeisme/<project>/<module>/<skill-name>/ public project source of truth
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
find .skills/yeisme -maxdepth 2 -mindepth 2 -type l -print
```

Fix by deleting only generated duplicates for project-owned skills, keeping `.skills/yeisme/<module>/<skill-name>/`, then run `scripts/skills.sh sync-root` and the relevant subproject sync to regenerate runtime copies from profiles.

## Required Structure

Every self-built skill must include:

```text
.skills/yeisme/<module>/<skill-name>/
  SKILL.md
  agents/openai.yaml
```

`SKILL.md` must have YAML frontmatter with:

- `name`: same as the directory name.
- `description`: clear trigger conditions, task object, and scope; prefer `Use when ...`.

For a product-owning skill, name the product or domain before its current implementation surface. Enumerate every approved surface that should trigger the skill—such as CLI/TUI, API/service/MCP/event, Web/desktop/client, and operational workflows—and identify the stable control-plane contract. Use CLI-only wording only when the nearest `AGENTS.md` or an accepted OpenSpec change explicitly limits the product scope.

The body should stay lean:

- when to use the skill
- inputs and outputs
- boundaries
- workflow
- validation
- references to optional scripts or reference files
- command examples must show the real command a user can run, without local execution wrappers, shell aliases, or agent-only prefixes

`agents/openai.yaml` must include:

- `display_name`: human-readable name.
- `short_description`: UI-facing one-line summary matching `SKILL.md`.
- `default_prompt`: a concrete starting prompt the user can run directly.

Do not add per-skill `README.md`, `CHANGELOG.md`, `QUICK_REFERENCE.md`, or `INSTALLATION_GUIDE.md`. Put human-facing authoring guidance in `docs/skills/` instead.

Do not write local execution wrappers, shell aliases, or agent-only command prefixes into user-facing docs, skill examples, plans, reviews, or final replies. Keep those details inside the execution layer only.
> Renaming or removing a published skill directory, renaming `SKILL.md` frontmatter keys, or changing `agents/openai.yaml` required keys is a generation-breaking change: profiles and consumers reference skills by name. Follow `yeisme-evolutionary-change-policy`: keep the old name as an alias for one release, update every profile that references it, then remove the old name later.

## Workflow

1. Read `.skills/yeisme/README.md` and the target skill's `SKILL.md` if it already exists.
2. Confirm the requested capability is a reusable agent workflow. If it is an MCP implementation, put the implementation under `mcp/` and only create a skill if the workflow needs agent guidance.
3. Create or update the skill in `.skills/yeisme/<module>/<skill-name>/`.
4. Keep metadata in `agents/openai.yaml` consistent with `SKILL.md`.
5. If the skill should be available in a root or subproject session, add it with `scripts/skills.sh profile add <target> <skill-name>`.
6. Run:

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
scripts/skills.sh list-custom
```

7. If publishing, ensure the GitHub remote exists, commit the `.skills/yeisme/`, profile, `scripts/skills.sh`, and docs changes, then push.

## Validation Rules

- Directory name, `name:` frontmatter, and display metadata must agree.
- `description:` must say when the skill should be used and must not be empty.
- `agents/openai.yaml` must contain `display_name`, `short_description`, and `default_prompt`.
- `scripts/skills.sh sync-root` and `sync-subprojects` must not write project-owned skills into `.codex/skills/`.
- `scripts/skills.sh sync-root` must write only root-profile skills into root `.agents/skills/` and `.claude/skills/`.
- `scripts/skills.sh sync-subprojects` must write only each subproject profile into that subproject's generated `.agents/skills/` and `.claude/skills/`.
- Profile files must not reference `.agents/skills` as a source.
- `.skills/yeisme/` must contain only module directories, first-party project submodules, plus `README.md` and optional `.gitmodules`; module directories contain self-built skill directories.
- `.skills/imported/` must contain only module directories plus `README.md`; module directories contain third-party/imported skill directories.
- Do not add generated caches, local secrets, runtime data, or vendored dependencies.
- Do not create per-skill README files unless the user explicitly asks for human-facing documentation.

## Publishing Notes

For other users, document:

```bash
git clone <repo-url>
cd yeisme-agent
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
```

For reviewed third-party skills, require an explicit ref:

```bash
scripts/skills.sh import <repo-url> <ref> <module>
```
