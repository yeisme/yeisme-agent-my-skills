---
name: yeisme-evolutionary-change-policy
description: Use when adding, renaming, removing, retyping, or repurposing any stable contract surface in this repository — CLI output fields, --agent keys, --events types, RPC/protobuf/Connect/API methods or fields, database schema, migrations, config/profile/registry keys, public Go/TS exported APIs, package paths, or skill frontmatter — to block generation-breaking (断代) updates and force incremental, backward-compatible evolution with an OpenSpec gate.
---

# Yeisme Evolutionary Change Policy

Use this skill any time a change touches a stable, externally observed contract. The rule is simple: **projects evolve incrementally, they do not do generation-breaking updates** (断代更新). A change that forces every caller, consumer, or migration to break at once is a generation break and is blocked unless an OpenSpec change explicitly approves it with a migration, deprecation window, and rollback.

This skill is the single source of truth for "what counts as breaking" across the six contract surfaces. Narrower skills (`ai-native-cli-output-contract`, `backend-system-workflow`, `go-rust-implementation-defaults`, `yeisme-coding-execution-driver`, `yeisme-skill-publisher`) reference it; they do not redefine the policy.

## Trigger Conditions

Use this skill automatically when the work involves any of these surfaces:

- CLI output: changing `--json` envelope fields, `--agent` keys, `--events` event `type` values, `spec_version`, command names, or default output mode.
- RPC / protobuf / Connect / HTTP API: adding/removing/renaming messages, fields (especially required fields), enum values, service methods, or field numbers; changing HTTP method/path/status semantics.
- Database schema / migrations: `DROP TABLE`, `DROP COLUMN`, narrowing a type, adding `NOT NULL` without a default, renaming a column/table, changing a unique/foreign-key constraint in a way that rejects existing rows.
- Config / profile / registry: renaming or removing keys in `registry.json`, `Taskfile.yml` inputs, `.skills/profiles/**`, `mcp.env`, OpenSpec frontmatter, or any YAML/TOML/JSON the project reads.
- Public Go / TypeScript API: renaming or removing an exported function, type, method, interface, struct field, package import path, or Go module path; changing a function signature in a way that breaks existing callers; changing the concrete type returned by an interface.
- Skill schema: renaming or removing `SKILL.md` frontmatter keys, `agents/openai.yaml` keys, profile entry formats, or the `.skills/yeisme/<module>/<skill>` directory shape.

Do not use this skill for:

- Pure internal refactors where no exported symbol, stored schema, or wire format changes.
- Brand-new, never-released surfaces (no consumers exist yet). Mark them clearly as pre-1.0 in the change and you may iterate freely — but record the "released / stable from" point.
- Documentation-only changes.
- Bug fixes that make wrong output match the documented contract.

## Hard Rule

If a change is breaking on any surface above and is NOT covered by an approved OpenSpec change that contains migration + deprecation + rollback, **stop coding**. Create or update the owning OpenSpec change first, then resume.

The only exceptions are:

1. Pre-1.0 surfaces explicitly labeled unstable in the change description and in code (`// unstable:` / `// EXPERIMENTAL:` / `spec_version: 0.x` / `alpha` / `beta`).
2. A documented security fix that cannot be made backward-compatibly. Still requires an OpenSpec change, but the deprecation window may be collapsed.

When in doubt, treat the surface as stable and gate it.

## Backward-Compatible By Default

For each surface, these changes are safe and do not require a gate:

- CLI output: adding an optional `data` field; adding a new `--events` event `type` that old consumers can ignore; adding a new optional `--agent` key; bumping `spec_version` minor.
- RPC / API: adding an optional field with a new field number; adding a new enum value that old clients treat as unknown; adding a new service method; widening an HTTP response with new optional keys.
- Database: adding a nullable column or a column with a default; adding an index; adding a new table; adding a constraint that existing rows already satisfy.
- Config / profile / registry: adding a new key with a safe default; adding a new optional field.
- Public API: adding a new exported symbol; adding a variadic options pattern; adding a new method to an interface when the project uses a consumer-implemented interface and you also provide a default implementation.
- Skill schema: adding a new optional frontmatter key; adding a new module directory.

Anything that removes, renames, narrows, repurposes, or changes the required-ness of an existing surface is breaking.

## Breaking Change Lifecycle

When a breaking change is genuinely necessary, it must follow this lifecycle:

1. **OpenSpec change first.** Create or update the owning change. Root `openspec/changes/<design-id>/` is for cross-project contract policy; `<subproject>/openspec/changes/<change-id>/` is for a concrete implementation that changes that subproject's surface. The change must name every affected surface and every consumer.
2. **Migration step.** For DB: expand-then-contract (add new, backfill, dual-write/read, then remove old in a later release). For code: add the new surface alongside the old, route internal callers to the new one, keep the old surface as a thin shim. For CLI: add the new field/key and emit both old and new during the transition.
3. **Deprecation window.** The old surface emits a deprecation warning (log line, CLI note, `--explain` risk, linter rule) for at least one release before removal. Document the window length and the removal release.
4. **Rollback plan.** The OpenSpec change must state: if this ships and breaks, what is the exact rollback (revert commit, feature flag flip, reverse migration, re-publish the old version), and how long rollback stays viable.
5. **Consumer updates.** Update every in-repo consumer in the same change, or list out-of-repo consumers and how they will be notified.
6. **Removal release.** Only after the deprecation window, remove the old surface in a release that the OpenSpec change names.

## Surface-Specific Rules

### CLI Output

- `--json` envelope top-level fields (`spec_version`, `mode`, `command`, `status`, `summary`, `facts`, `actions`, `evidence`, `confidence`, `data`, `error`) are stable. Removing or renaming any of them is a major version break.
- `status` enum values (`success`, `partial`, `failed`) are stable. Removing a value or changing its meaning is breaking.
- `--agent` keys are a wire contract. Renaming or removing a key is breaking; adding a key is safe.
- `--events` event `type` strings are stable. Renaming a type or changing its required fields is breaking.
- See `ai-native-cli-output-contract` for the field-by-field versioning rules. This skill is the stop-condition that forces a gate when those rules are violated.

### RPC / Protobuf / Connect / HTTP API

- Never reuse a protobuf field number. Reserved numbers stay reserved.
- Never remove a field that any client may still send. Mark `deprecated` in proto first, remove in a later release.
- Never change a field from optional to required, or change its type, on an existing field number.
- Never change an HTTP method, path, or success status for an existing endpoint. Version the path (`/v2/...`) instead.
- Enum value numbers are immutable once released. Adding a new value is safe; renumbering is breaking.

### Database Schema / Migrations

- Never `DROP COLUMN` or `DROP TABLE` in the same migration that introduces the replacement. Use expand-then-contract across releases.
- Never add `NOT NULL` to an existing column without a backfill and a default.
- Never narrow a type (e.g. `TEXT` → `INT`) on a populated column in one step.
- Never change a unique/foreign-key constraint so that existing rows would be rejected, unless the migration also fixes the data.
- Never rename a column or table and rewrite every query in one migration. Add the new name, dual-write, then remove the old name later.
- Every risky migration carries a documented rollback. See `backend-system-workflow` storage rules.

### Config / Profile / Registry

- `mcp/registry.json`, `.skills/profiles/**`, `Taskfile.yml`, `mcp.env`, OpenSpec frontmatter, and per-subproject config files are versioned contracts.
- Renaming or removing a key requires: keep the old key as a deprecated alias for one release, log a warning when the old key is read, document the new key, then remove.
- Changing the meaning of an existing key value (e.g. `lane: slow` silently becoming `deep`) is breaking even if the key name is unchanged. Keep aliases stable (`slow` still maps to `deep`).

### Public Go / TypeScript API

- Exported symbols in `internal/` are internal; this rule applies to `pkg/`, root packages, and any path imported by another module or subproject.
- Removing or renaming an exported symbol is breaking. Add the new name, keep the old as a deprecated alias, remove later.
- Changing a function signature (parameter order, types, return type) is breaking. Use options structs or variadic args for additive change.
- Changing the concrete type behind an interface return is breaking if callers type-assert.
- Changing a Go module path or a TS package name/export path is breaking.
- See `go-rust-implementation-defaults` for language-level escalation; this skill only governs the compatibility posture.

### Skill Schema

- `SKILL.md` frontmatter keys (`name`, `description`) and `agents/openai.yaml` keys (`display_name`, `short_description`, `default_prompt`) are stable.
- The `.skills/yeisme/<module>/<skill>/` directory shape and the `.skills/profiles/*.txt` line format are stable.
- Renaming a published skill directory is breaking: consumers reference it by name in profiles. Provide a redirect period.
- See `yeisme-skill-publisher` for skill authoring; this skill governs when a skill schema change must gate.

## Enforcement Model

Enforcement is layered, strongest first:

1. **Implementation time (hard stop).** When `yeisme-coding-execution-driver` or any domain skill detects a breaking change without an approved OpenSpec change, stop. Create the change, then resume. This is the default.
2. **Review time (hard block).** `plan-eng-review`, `plan-ceo-review`, and `review` must reject any diff or plan that introduces a breaking change without the migration/deprecation/rollback record. The block names the surface and the missing artifact.
3. **Soft flag (advisory).** When a change is borderline (e.g. an unstable pre-1.0 surface, or an internal symbol that happens to be exported), flag it in the final response with the surface, the risk, and the suggested gate, but continue if the surface is genuinely pre-release.

Default to the hard stop. Only downgrade to advisory when you can show the surface has no consumers and is labeled unstable.

### Review-Time Checklist

When running `plan-eng-review`, `plan-ceo-review`, `review`, or any deputy-architect review pass, apply this checklist before approving. Imported review skills (gstack `plan-eng-review`, `plan-ceo-review`, `review`) do not carry this Yeisme-specific gate by default; this skill supplies it.

- For every changed file, identify whether it touches one of the six surfaces (CLI output, RPC/API, DB migration, config/registry, public Go/TS API, skill schema).
- For each touched surface, classify the change as additive or breaking.
- If any surface is breaking, require an OpenSpec change that contains: the affected surface list, the migration step, the deprecation window length and removal release, the rollback step, and the consumer update list. If any element is missing, the review is blocked.
- Reject diffs that silence a breaking change by deleting or widening a contract test, relaxing a schema validator, or removing a deprecation warning.
- Record the verdict in the review output: `breaking_surfaces: [...]`, `openspec_change: <id|none>`, `deprecation_window: <length>`, `rollback: <step>`. A review that touches a stable surface but records none of these is incomplete.

## Workflow

1. Before editing, identify every contract surface the change touches. List them.
2. For each surface, classify the change: additive (safe), breaking (gate required), or unclear (probe).
3. If any surface is breaking and no OpenSpec change covers it, stop and create/update the owning OpenSpec change with migration, deprecation, and rollback sections before writing implementation code.
4. Implement using the expand-then-contract pattern: add the new surface, keep the old surface working, route internal callers to the new one.
5. Add the deprecation signal (log, warning, linter, note) on the old surface.
6. Update every in-repo consumer.
7. Run the owning project's contract tests plus any cross-project consumer tests. If a contract test does not exist for the surface, add one that pins the old shape.
8. In the final response, name each affected surface, the change class (additive/breaking), the OpenSpec change id, the deprecation window, and the rollback step.

## Inputs

- The change request, plan, or diff.
- Owning subproject `AGENTS.md`, API/RPC definitions, migration files, config files, exported package surfaces, and skill frontmatter.
- Existing OpenSpec changes that already cover (or should cover) the surface.

## Outputs

- A surface-by-surface compatibility classification in the final response or review.
- A created or updated OpenSpec change when a breaking change is required.
- Expand-then-contract implementation, deprecation signal, consumer updates, and rollback notes.
- A clear statement when a change is safe (additive) and needs no gate.

## Boundaries

- Do not treat "it compiles" or "tests pass" as evidence of compatibility. Compatibility is about consumers and stored data, not the build.
- Do not silence a breaking change by widening a test, deleting a contract test, or relaxing a schema validator. If the contract changed, gate it.
- Do not collapse the deprecation window silently. The window length is a user-visible decision; record it.
- Do not batch unrelated breaking changes into one OpenSpec change to save effort. Each affected surface family gets its own migration section.
- Do not use this skill to block pure additions or internal work. The goal is to stop generation breaks, not to freeze the codebase.

## Validation

- Run the owning project's contract tests (CLI output envelope tests, proto/API conformance tests, migration up/down tests, API signature tests).
- For CLI surfaces, run the `ai-native-cli-output-contract` validator against sample output.
- For DB changes, run migration apply and reverse in a test database.
- For Go/TS API changes, run the package's existing tests and any consumer tests in depending subprojects.
- For skill schema changes, run `scripts/skills.sh validate-custom`, `validate-profiles`, and `validate-runtime`.

If a compatibility test does not exist for the surface you changed, add one before claiming the change is safe.
