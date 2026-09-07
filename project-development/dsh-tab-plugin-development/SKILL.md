---
name: dsh-tab-plugin-development
description: Use when designing, implementing, reviewing, or evolving a DeepSeek Harness (DSH) web tab, pane, or overlay plugin — per-session conversation.view tabs, workspace panes, shell overlay fallbacks, session projections, storage domains, preset-root registration, or vendored upstream dsh bundles in agent/harness-plugins.
---

# DSH Tab Plugin Development

Guidance for building DSH Web 界面插件（会话内 tab / workspace pane / overlay 兜底）in `agent/harness-plugins`. It extracts the verified patterns from two reference implementations: the vendored `packages/bundle/dsh-pentest/` (per-session pentest view tab + graph visualization) and the repo-native `packages/bundle/dsh-token-usage/` (process-scoped ledger pane). The full extracted guide is `agent/harness-plugins/docs/plugin-tab-development.md` — read it before writing code; this skill routes and enforces.

## Scope

Use for any new DSH Web surface: conversation view tabs, pane workbench views, header-action entries, shell overlays, session projection units, storage domains, agent presets that carry domain host rows, and vendoring/upgrading upstream DSH bundles. Do not use for pure host-side CLI plugins with no Web face, or for non-DSH UIs.

## Non-negotiable boundaries

- Read `agent/harness-plugins/docs/design/dsh-unified-panel-visual-system.md` before any React/Web UI; repo-native faces consume `ui-surface`/`ui-visual-kit` tokens and pass `check:surfaces` + `test:visual`. Vendored upstream faces are visually exempt but follow the same interaction-quality bar (bilingual, focus return, honest disabled reasons).
- Choose the seam by data scope: session-scoped domain view → `slots.register('conversation.view')` mounted/disposed per session; cross-session process/project data → `paneWorkbench.registerView` (keep-alive singleton); an action entry → header action + `shell.overlay` fallback. Never leave a dead tab on a session that lost the domain preset.
- Client `inject` declares required services (`slots`, `locale`, `sessions`, …); every registration (pane, slot, locale, subscription) flows into disposer(s) returned by `apply` — symmetric teardown on HMR, profile switch, plugin disable, session switch.
- Capability probe before query: missing Remote/capability = entry visible but disabled with a readable `disabledReason()`, never hidden silently, never a fake fallback.
- The web row's host half is an empty `apply` — re-inserting the host plugin duplicates its scoped tool catalog and causes client command invalidation loops. Domain host rows belong in the domain agent preset, not the global patch.
- Projections are folds of logged tool calls (deterministic ids, pure replay), not a second state store; bounded window views (e.g. latest 200) must state their boundary honestly and point to the authoritative read path (`*_state`/`*_report` from storage).
- Host boundary passes safe projections only (opaque refs, bounded summaries, versions, freshness, reason codes). No raw prompts, credentials, provider payloads, private tool arguments, or absolute paths to the browser.

## Workflow

1. **Classify the surface** (tab vs pane vs overlay) with §1 of the guide; pick package shape A (self-contained bundle, `lib/` prebuilt) or B (host/client/bundle trio with React). Shape B requires the visual-system contract; shape A fits upstream pins and preset/data bundles.
2. **Declare the composition** in `cordis.patch.yml` using the repo-converged `- insert: [id, name]` grammar; full cordis grammar (id-override rows, multiple inserts) is allowed only for vendored bundles carrying `YEISME-VENDORED.md` (declaration-lint then records, not reds).
3. **Build the host face** with the four registration points: `ctx.tools.register(defineTool(...))`, `systemPrompt.section({name, order, text})` for protocol injection, `sessionProjections.register({key, schema, stateVersion})`, `ctx.storageDomain.open(spec)` with explicit dispose effect. Storage stays in `$DSH_HOME/storages/` (sqlite needs Node ≥ 22.5), records are per-session.
4. **Build the client face**: zh/en locale dictionaries via `ctx.effect`; per-session tab = subscribe `sessions.list`, walk `parentId` ancestry with a cycle guard, register/dispose `conversation.view` on preset membership; pane = `registerView({descriptor: {kind, label, componentKey, role, preferredRegion, retention, singleton}})`.
5. **Gate and verify**: `pnpm run typecheck && pnpm run test && pnpm run build && pnpm run check:bundles && pnpm run check:plugins && pnpm run check:surfaces`. Completion is repo protocol conformance — never gated on official DSH seams. Optional host evidence: `dsh plugin --profile web add`, `--dump-config` row check, `timeout 40 dsh --profile web --port 0` boot smoke (errors=0), recorded sanitized under `temp/integration-test-runs/<run-id>/`.
6. **For vendored upstream bundles**: exclude `.git`/lockfiles/upstream per-package build outputs/process docs; commit the pinned `lib/` (add a `.gitignore` directory negation); pin commit + license + upgrade procedure in `YEISME-VENDORED.md`; upgrade = fresh-clone byte diff + human review + full gate rerun.
