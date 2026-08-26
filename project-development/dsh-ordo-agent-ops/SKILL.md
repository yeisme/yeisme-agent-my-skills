---
name: dsh-ordo-agent-ops
description: Use when designing, implementing, testing, or reviewing the DeepSeek Harness adapter for Ordo Agent Operations, including tenant context, snapshot/event cursors, runtime and lease projections, approvals, receipts, reconciliation, and Workbench handoff.
---

# DSH Ordo Agent Ops

This skill is guidance for the DSH adapter. It is not a second scheduler, a generic remote-shell workflow, or a substitute for the Ordo owner contract.

## Scope

Use this skill for the DSH host plugin, Web client module, profile bundle, `/ordo` command, ToolView, typed client service, event subscription, safe action dispatch, and their tests and documentation. Use `agent/harness-plugins/openspec/changes/ordo-dsh-plugin-visualization-v1/` as the DSH-facing design source. Ordo remains the owner of run, task, attempt, session, runtime, lease, worktree, approval, verification, evidence, and closeout facts.

## Non-negotiable boundaries

- One DSH runtime generation binds one tenant, workspace, and runtime subject. A browser parameter cannot switch the tenant of a live process.
- The host plugin owns authenticated transport, context binding, snapshot loading, event cursors, backoff, cache lifetime, and disposal. The browser module receives typed safe projections only.
- DSH uses Cordis plugin, `dsh.client`, profile/bundle, command, tool, and ToolView seams. Do not fork DSH core or import private React state.
- The adapter does not create a DAG, task ledger, writer lease, approval ledger, capacity reservation, or terminal result. It reads Ordo facts and owner receipts.
- `unknown`, `partial`, `cancel_unknown`, stale cursors, expired approvals, and contract drift disable mutation and require owner-authored reconciliation. They never trigger an automatic retry or replacement writer.
- Safe projections contain opaque refs, bounded summaries, reason codes, versions, freshness, evidence refs, and allowed actions. They do not contain raw prompts, provider payloads, credentials, generic bearer tokens, private tool arguments, absolute host paths, PIDs, or hidden reasoning.

## Workflow

1. **Route ownership.** Identify the Ordo fact, DSH seam, and external owner receipt before adding a type or service. If the behavior needs a new canonical fact, stop and create an Ordo owner handoff instead of adding DSH state.
2. **Freeze context.** Bind every request and projection to tenant, workspace, principal, context revision, membership revision, installation, plugin digest, policy revision, and runtime generation where applicable. Clear subscriptions, cursors, cache, selections, and pending dialogs before a context switch.
3. **Design the read path.** Load an authoritative snapshot first. Apply events only for the expected stream and next sequence. Ignore duplicates; on a gap, expired cursor, digest drift, or generation change, stop applying deltas and reload the snapshot.
4. **Design the action path.** Render only server-authored action descriptors. Recheck permission, approval, target version, policy, installation config, idempotency, and preview digest at dispatch. Show owner receipt or an explicit unknown/reconcile state after dispatch.
5. **Choose the presentation seam.** Use a reviewed native client module for the persistent Agent Ops panel, ToolView for one action or tool result, and a typed host command/service for transport. Use a Workbench deep link for full DAG, cross-run, or multi-tenant workflows.
6. **Close every lifecycle.** Dispose event streams, timers, pending requests, callbacks, and UI subscriptions on plugin unload, HMR, runtime switch, tenant switch, and connection generation change. The replacement generation starts from a new snapshot.
7. **Prove negative paths.** Test cross-tenant access, stale context, event gaps, duplicate events, late results, unknown liveness, expired approval, revoked installation, contract mismatch, unsafe summaries, and browser token absence through the real package or Web entry path.
8. **Update the local contract.** Change the local OpenSpec, package README or cookbook, and the DSH Agent Note when the owner boundary, wire fields, lifecycle, or security behavior changes.

## Required evidence

For a code change, run the narrow DSH package tests and repository documentation gates selected by the diff from `agent/harness-plugins`:

```bash
pnpm run typecheck
pnpm run test
pnpm run build
pnpm run check:bundles
pnpm run doc-sync
openspec validate ordo-dsh-plugin-visualization-v1 --strict --no-interactive
git diff --check
```

Record the snapshot ref/version, stream/cursor, context revision, action/approval/receipt lineage, and redacted failure evidence. Do not record raw provider payloads, secrets, prompts, tool arguments, or full reasoning. A test that mounts a plugin by hand does not replace a profile or Web composition test.
