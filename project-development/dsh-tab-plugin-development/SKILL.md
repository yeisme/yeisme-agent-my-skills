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
- Choose the seam by data scope: session-scoped domain view → `slots.register('conversation.view')` mounted/disposed per session; cross-session process/project data → `applyOfficialPanePlugin` / `createOfficialPaneSurface` (official right Sidebar); an action entry → header action with honest disable, never `shell.overlay` as a pane host. Architecture: `agent/harness-plugins/docs/architecture/dsh-pane-plugin-ecosystem.md`.
- Client `inject` declares required services (`slots`, `locale`, `sessions`, …); every registration (pane, slot, locale, subscription) flows into disposer(s) returned by `apply` — symmetric teardown on HMR, profile switch, plugin disable, session switch.
- Capability probe before query: missing Remote/capability = entry visible but disabled with a readable `disabledReason()`, never hidden silently, never a fake fallback.
- The web row's host half is an empty `apply` — re-inserting the host plugin duplicates its scoped tool catalog and causes client command invalidation loops. Domain host rows belong in the domain agent preset, not the global patch.
- Projections are folds of logged tool calls (deterministic ids, pure replay), not a second state store; bounded window views (e.g. latest 200) must state their boundary honestly and point to the authoritative read path (`*_state`/`*_report` from storage).
- Host boundary passes safe projections only (opaque refs, bounded summaries, versions, freshness, reason codes). No raw prompts, credentials, provider payloads, private tool arguments, or absolute paths to the browser.
- A non-chat `conversation.view` tab is not a transcript: it must clean the conversation-page chrome the core reuses into every tab — the composer via the `conversation.composer` chain takeover, and the core transcript width handles (`data-width-handle` left/right, rendered as siblings of `[data-conversation-scroll]` when the phase is active) via a `:has()` sibling CSS rule. DOM contract and both patterns: §5.1 of the guide.
- A user ruling to DELETE a control means delete the whole chain (component file, props/state keys, CSS attribute hooks, locale entries, prefs fields, screenshot baselines, spec delta). "Converge into one button/menu" is NOT deletion. When the user names a control as main-conversation-page legacy, grep the core `dsh-client-ui-*` packages for the same-shaped DOM hook before touching your own package again.

## Workflow

1. **Classify the surface** (tab vs pane vs overlay) with §1 of the guide; pick package shape A (self-contained bundle, `lib/` prebuilt) or B (host/client/bundle trio with React). Shape B requires the visual-system contract; shape A fits upstream pins and preset/data bundles.
2. **Declare the composition** in `cordis.patch.yml` using the repo-converged `- insert: [id, name]` grammar; full cordis grammar (id-override rows, multiple inserts) is allowed only for vendored bundles carrying `YEISME-VENDORED.md` (declaration-lint then records, not reds).
3. **Build the host face** with the four registration points: `ctx.tools.register(defineTool(...))`, `systemPrompt.section({name, order, text})` for protocol injection, `sessionProjections.register({key, schema, stateVersion})`, `ctx.storageDomain.open(spec)` with explicit dispose effect. Storage stays in `$DSH_HOME/storages/` (sqlite needs Node ≥ 22.5), records are per-session.
4. **Build the client face**: zh/en locale dictionaries via `ctx.effect`; per-session tab = subscribe `sessions.list`, walk `parentId` ancestry with a cycle guard, register/dispose `conversation.view` on preset membership; pane = `createOfficialPaneSurface(ctx)?.registerView({descriptor: {kind, label, componentKey, role, preferredRegion, retention, singleton}})`.
5. **Gate and verify**: `pnpm run typecheck && pnpm run test && pnpm run build && pnpm run check:bundles && pnpm run check:plugins && pnpm run check:surfaces`. Completion is repo protocol conformance — never gated on official DSH seams. Chrome-removal changes additionally need a real-preview check (screenshot fixtures do not include core chrome): restart the workbench preview, open a real session, count the visible `[data-width-handle]` on the chat tab vs your tab. Optional host evidence: `dsh plugin --profile web add`, `--dump-config` row check, `timeout 40 dsh --profile web --port 0` boot smoke (errors=0), recorded sanitized under `temp/integration-test-runs/<run-id>/`.
6. **For vendored upstream bundles**: exclude `.git`/lockfiles/upstream per-package build outputs/process docs; commit the pinned `lib/` (add a `.gitignore` directory negation); pin commit + license + upgrade procedure in `YEISME-VENDORED.md`; upgrade = fresh-clone byte diff + human review + full gate rerun.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Overlay used as a pane host | Official Sidebar pane or `conversation.view` | Never `shell.overlay` for durable panes |
| Missing capability hidden the entry | Show disabled + `disabledReason()` | No silent hide, no fake fallback |
| Host plugin re-inserted on the web row | Empty `apply` on web host half | Duplicate tools cause command invalidation loops |
| Raw prompts/paths in the browser | Safe projection only | Opaque refs, bounded summaries, reason codes |
| Visual tokens skipped | Read unified panel visual system; `check:surfaces` | Vendored faces still need bilingual/focus/disabled honesty |
| User still sees a "main-conversation width" control after deletion | Core `WidthHandle` reused into every conversation tab; hide via the `:has()` sibling CSS rule (§5.1) | Deleting only your own package's controls is not enough; verify in the real preview |
