---
name: auctra-ai-drama-panel-handoff
description: Use when an Auctra screenplay scene or novel chapter must be prepared for Ordo PanelRun evaluation, when a typed PanelRun result must be consumed into Auctra review evidence, or when reviewing the CLI/MCP parity and fail-closed boundary of that handoff.
---

# Auctra AI Drama Panel Handoff

## Owner boundary

Auctra owns accepted text, Story World refs, source revisions and review decisions. Ordo owns PanelRun scheduling, evaluator fan-out, correlation clusters, quorum, aggregation, adjudication and reconcile. This skill connects the two owners with typed refs; it never becomes a scheduler or a second consensus engine.

## Workflow

1. Read `cli/auctra/openspec/changes/auctra-ai-drama-story-handoff-v1/` and confirm the source revision is accepted and not stale.
2. Freeze `subject_ref`, `subject_scope`, `context_ref`, `profile_ref`, `rubric_digest`, `hard_gate_refs`, `owner_grant` and a stable `idempotency_key`. Do not place screenplay text, prompt text, provider payloads or private Ordo state in the packet.
3. Compile the packet through the Auctra owner projection:

   ```bash
   auctra story handoff evaluation-packet --packet-ref <ref> --project-ref <ref> --subject-ref <ref> --scope screenplay_scene --context-ref sha256:<digest> --profile screenplay-craft-v1 --rubric-digest sha256:<digest> --hard-gate-ref <ref> --owner-grant <ref> --idempotency-key <key> --json
   ```

4. Pass the returned packet to the Ordo agent tool `ordo.panel.start`. Do not implement evaluator retries, quorum, median/IQR, disagreement adjudication or provider calls in Auctra.
5. When Ordo returns its typed result, bind it to the expected source and rubric digests and validate it through Auctra:

   ```bash
   auctra story handoff panel-result --from - --expected-source-digest sha256:<digest> --expected-rubric-digest sha256:<digest> --evidence-ref <ref> --json
   ```

6. Treat `review_intake.next_action` as a review navigation hint only. A completed PanelRun, high score, recommendation or adjudication never accepts canonical text. Use Auctra review commands and the revision service for explicit accept/revise/reject decisions.

## Profile routing

- `screenplay_scene` → `screenplay-craft-v1`; dimensions are scene-level craft and drama gates.
- `novel_chapter` → `novel-craft-v1`; do not reuse screenplay dimensions or claim full-novel coverage.
- Candidate comparison, disagreement and repair reasoning belongs to `ai-drama-critic-panel`; Auctra only compiles/consumes its typed boundary.
- Cost, permission, capability and retry admission belongs to `ai-drama-producer`.
- Ordo/Scaena pause, resume and production handoff belongs to `ai-drama-production-orchestrator`.

## Fail-closed rules

- Missing context/profile/rubric/hard gate/owner grant/idempotency → `needs_contract`.
- Source revision or digest mismatch → stale/conflict; never score it as current.
- Profile/scope mismatch → reject; never silently coerce.
- Unknown, inconclusive, blocked or conflicting result → preserve refs and require human review.
- `story_handoff.panel_result` creates a review-only intake projection; it does not write review metadata or canonical revision by itself.
- Future MCP mapping is catalog-derived and remains `planned` until the adapter parity gate is complete.

## Verification

```bash
cd /workspaces/yeisme-agent/cli/auctra
go test ./internal/storyhandoff ./internal/operation -count=1
go test -tags=nomsgpack ./internal/cli -run 'TestStoryHandoff|TestOperationCatalog|TestBackendFacing' -count=1
openspec validate auctra-ai-drama-story-handoff-v1 --strict --no-interactive
```
