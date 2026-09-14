---
name: dsh-3d-director-gltf-workbench
description: Use when designing, implementing, or reviewing the DSH 3D Director workbench — Shot-anchored scene orchestration, Khronos glTF/GLB capability contracts, canvas/viewport selection synchronization, auditable generation change sets, and revision-safe conflict handling.
---

# DSH 3D Director glTF/GLB Workbench

Use this skill for the `dsh-3d-director-gltf-workbench-v1` change.

- Read `docs/design/dsh-unified-panel-visual-system.md` before any UI work.
- Treat Shot as the workflow anchor and reuse project-canvas bindings.
- Keep scene graph edits in versioned workbench state; Ordo and domain owners remain authoritative for tasks, approvals, assets, and delivery.
- Support glTF 2.0 core and GLB first. Report every official extension with explicit readable/editable/exportable/opaque-preserved capability.
- Preserve unsupported extension payloads or block export with a capability gap; never silently drop data.
- Represent generation as auditable change sets with safe references, preview, digest, status, and rollback.
- Freeze writes on revision mismatch; require owner reconcile; never auto-overwrite or retry unknown/stale operations.
- Never expose credentials, raw prompts, provider payloads, arbitrary fetch targets, or absolute paths in projections, fixtures, logs, or evidence.
- Validation evidence must be redacted and written under `temp/integration-test-runs/<run-id>/`.
