---
name: aigora-skill-router
description: Use when starting any Aigora session or when the next skill is unclear; route the task through a decision tree to the smallest non-conflicting skill chain instead of loading a flat skill list.
---

# Aigora Skill Router

This is a routing skill only. It chooses the next skill chain. It does not implement code, write OpenSpec artifacts, or perform QA.

Do not load every Aigora skill. Walk the tree once. Stop at the first matching leaf. Load a second skill only when that leaf names it as a required pair.

## Output

Return routing guidance, then hand off:

```text
Route:
aigora-skill-router -> <leaf> -> <optional pair> -> <verify skill if named>

Reason:
<which tree question matched>

Do not load:
<siblings on other branches>

Docs:
docs/<domain>/README.md -> <one page that domain README names>
```

If the user asks to read all skills, refuse and return this tree.

## Decision Tree

```text
1. Is this thinking / product / architecture with no code request?
   yes -> openspec-explore
         docs/planning/README.md
         STOP. Do not load yeisme-coding-execution-driver.

2. Would this rename, remove, or retype a released contract
   (CLI field, RPC/API, DB column, config key, public Go/TS symbol, skill schema)?
   yes -> yeisme-evolutionary-change-policy
         if no OpenSpec gate with migration + deprecation + rollback: STOP

3. Is this an OpenSpec lifecycle action on a change?
   ├─ no change yet, need proposal+design+tasks
   │    -> openspec-propose  (or openspec-new-change if the user wants stepwise)
   ├─ existing change, next artifact
   │    -> openspec-continue-change
   ├─ implement approved tasks.md
   │    -> openspec-apply-change + yeisme-coding-execution-driver
   ├─ check implementation vs artifacts
   │    -> openspec-verify-change
   ├─ archive completed change(s)
   │    -> openspec-archive-change  (many: openspec-bulk-archive-change)
   └─ copy delta spec into main specs
        -> openspec-sync-specs

4. Is the work Operator Console / frontend / visual?
   yes -> yeisme-frontend-design-router
         then that skill's chain:
           ui-spec-frontend-workflow
           -> aigora-operator-i18n   (user-visible copy only)
           -> implementation
           -> yeisme-ui-motion-quality   (ordinary UI motion)
           -> yeisme-frontend-quality-workflow
         docs/operator/README.md
         STOP this tree; do not also load backend-system-workflow
         unless a shared API contract is the actual leaf.
         Remotion only if the output is a timeline video, not CSS/React motion.

5. Is the work Seedance-specific?
   ├─ three-plane ownership / module gaps
   │    -> aigora-seedance-core-architecture
   │       docs/architecture/README.md
   └─ eligibility-first next router / attempt / callback
        -> aigora-seedance-next-router-design
           docs/routing/README.md
   Do not load both unless the user asked for both reviews.

6. Is the work secrets / credentialctl?
   yes -> credentialctl-usage
         docs/upstreams/README.md  (access-key / session host only if that is the topic)

7. Is the work a security audit / threat model (not feature implementation)?
   yes -> cso
         do not use as an implementation driver

8. Is the work a pre-landing diff review?
   yes -> review
         do not use as an implementation driver

9. Is the work integration evidence directory layout?
   yes -> project-integration-test-evidence
         docs/operations/README.md

10. Is the work CLI output modes / --json / --agent / --events / --explain?
    yes -> ai-native-cli-output-contract
          + yeisme-coding-execution-driver when implementing
          docs/protocols/README.md -> cli.md

11. Is the work backend / API / worker / queue / GORM / state machine?
    yes -> backend-system-workflow + yeisme-coding-execution-driver
          language choice unclear? go-rust-implementation-defaults first
          docs/architecture/README.md
          plus protocols/ routing/ or upstreams/ only if that is the leaf domain

12. Otherwise implementing, debugging, or finishing code
    -> yeisme-coding-execution-driver
       then re-enter this tree only for a named domain pair
```

## Docs Domain Tree

After the skill leaf, open **one** docs domain. Do not walk `docs/` as a list.

```text
Who owns the truth, or which plane / table / stack?
  -> docs/architecture/README.md

Wire protocol, CLI projection, fingerprint, Eikona Operator API?
  -> docs/protocols/README.md

Channel identity, video model binding, coding-plan admission?
  -> docs/routing/README.md

Provider connector, session host, conformance, key migration?
  -> docs/upstreams/README.md

Operator page, shell, i18n, table, ContextDeck?
  -> docs/operator/README.md

Taskfile, runbook, local DB, e2e evidence?
  -> docs/operations/README.md

Request audit, abuse, metrics cardinality?
  -> docs/observability/README.md

Cross-change goal / execution DAG (not a tasks.md replacement)?
  -> docs/planning/README.md
```

Canonical pages live under those directories. `docs/<name>.md` at the docs root is a compatibility stub only.

## Conflict Rules

- One aesthetic authority for frontend: `yeisme-frontend-design-router` picks it. Do not load Taste, Impeccable, and `ui-spec-frontend-workflow` as equals.
- `openspec-explore` never pairs with `yeisme-coding-execution-driver`.
- `cso`, `review`, and `health` are not implementation drivers.
- `remotion-animation-workflow` is not for ordinary UI transitions.
- Do not nest skill folders; loaders resolve `.agents/skills/<name>/SKILL.md`.
- `.claude/skills/<name>` is a loader alias of `.agents/skills/<name>`, not a second source.

## Fallback

If a named skill is missing, keep the same tree role and discover the closest local equivalent. Do not block on installation. Do not implement inside this skill.
