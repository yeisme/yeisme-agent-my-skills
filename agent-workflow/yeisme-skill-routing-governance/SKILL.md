---
name: yeisme-skill-routing-governance
description: Use when selecting, adding, removing, discovering, reviewing, or routing skills for the Yeisme root repository or a subproject, especially when changing .skills/profiles, syncing .agents/.claude runtimes, replacing skillctl commands, or deciding whether a skill should be active or loaded on demand.
---

# Yeisme Skill Routing Governance

Keep semantic routing in the agent and deterministic state changes in repository scripts.

## Boundaries

- Treat `.skills/yeisme/` as the project-owned source and `.skills/imported/` as the reviewed third-party source.
- Treat `.skills/profiles/root.txt` and `.skills/profiles/targets/<owner>.txt` as the only active-skill declarations.
- Treat `.agents/skills/` and `.claude/skills/` as generated runtime copies. Never edit them as source.
- Do not recreate marketplace, route scoring, sets, telemetry, MCP, HTTP, or background services.
- Do not encode natural-language task understanding in shell. The agent reads descriptions and chooses.

## Routing Workflow

1. Read the nearest `AGENTS.md` and identify the code or document owner.
2. Prefer a named or clearly triggered active skill.
3. If no active skill fits, search the source layer:

```bash
scripts/skills.sh search "<task terms>"
scripts/skills.sh resolve <skill-name>
```

4. Read only the matching `SKILL.md`. Do not bulk-load source skills.
5. Use the smallest compatible combination: one primary workflow, at most one compatible domain constraint, and independent audit skills on separate read-only review work.
6. Keep a skill on demand unless it is useful at session start or repeatedly required by that owner.
7. If promotion or demotion is justified, update the profile through the script, then sync and validate.

## Profile Management

```bash
scripts/skills.sh profile show root
scripts/skills.sh profile show cli/cohors
scripts/skills.sh profile add cli/cohors <skill-name> --dry-run
scripts/skills.sh profile add cli/cohors <skill-name>
scripts/skills.sh profile remove cli/cohors <skill-name> --dry-run
scripts/skills.sh profile remove cli/cohors <skill-name>
scripts/skills.sh profile validate
```

Promote a skill only when it is required at session start, protects a high-frequency owner invariant, repeated discovery causes misses, or the nearest `AGENTS.md` declares it active. Demote release-only, audit-only, rare, superseded, or wrong-owner skills.

## Sync And Validation

Skill synchronization is a final-gate operation, not an implementation-loop
command. Assign one root sync owner and wait until all writers affecting
`.skills/yeisme/**`, `.skills/imported/**`, `.skills/profiles/**`,
`.agents/skills/**`, `.claude/skills/**`, or `scripts/skills.sh` have finished.
Freeze those paths before generation.

Before syncing, inspect the current source, profile, and runtime changes:

```bash
git status --short -- .skills/yeisme .skills/imported .skills/profiles .agents/skills .claude/skills scripts/skills.sh
git diff -- .skills/yeisme .skills/imported .skills/profiles scripts/skills.sh
```

Abort synchronization when a runtime-only change cannot be explained by its
source skill and profile, when another writer is active, or when ownership is
ambiguous. Never resolve a sync conflict by hand-editing `.agents/skills/` or
`.claude/skills/`; repair the source/profile state, then regenerate.

Use the narrowest supported sync command. Run `sync-root` for root-only source
or profile changes. Run `sync-target <target>` for one affected subproject.
Run `sync-subprojects` only when multiple subproject assignments or shared
source skills genuinely require it.

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-target <target>
scripts/skills.sh sync-subprojects
scripts/skills.sh validate-runtime
scripts/skills.sh validate-subprojects-runtime
```

Validation must fail on an unknown source, duplicate skill name, missing owner, profile/runtime drift, or different `.agents` and `.claude` contents.

## External Skills

Import only from an explicit Git ref:

```bash
scripts/skills.sh import <repo-url> <ref> <module>
```

Review the Git diff before adding the skill to any profile. Do not write external skills into `.skills/yeisme/` and do not treat discovery as installation approval.

## Output

Report the selected skill, owner, active/on-demand status, profile changes, validation evidence, and unresolved conflicts.
