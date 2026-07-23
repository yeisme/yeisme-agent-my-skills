---
name: anatomia-storyboard-reviewer
description: Use when reviewing, validating, revising, accepting, rejecting, freezing, or forking an Anatomia storyboard or analysis revision, especially for timeline coverage, low-confidence observations, identity, rights, domain-specific fields, and production handoff readiness.
---

# Anatomia Storyboard Reviewer

Review immutable revisions. Never edit accepted structured state or exported manifests by hand.

## Review Dimensions

- Timeline order, coverage, gaps, overlaps, source ranges, clip and frame lineage.
- Visual, action, dialogue, subtitle, audio, camera, style, rhythm, character, location and prop observations.
- Field-level confidence, provenance, unsupported assumptions and review blockers.
- Domain-specific gates from the selected profile.
- Identity, rights, sensitive content and production-readiness findings.

## Workflow

1. Inspect the active revision and validation report.
2. Compare every blocking or low-confidence claim with source clip/frame evidence.
3. Create a revision patch through the CLI; do not modify prior revisions.
4. Re-run validation and request changes when uncertainty remains.
5. Accept and freeze only when blockers are resolved or explicitly waived by an authorized actor.
6. Fork a frozen revision for later edits.

## Commands

```bash
anatomia analysis show analysis:demo --revision analysis-revision:demo:v1 --json
anatomia review validate analysis:demo --revision analysis-revision:demo:v1 --json
anatomia review revise analysis:demo --revision analysis-revision:demo:v1 --patch ./revision.patch.json --json
anatomia review request-changes analysis:demo --revision analysis-revision:demo:v2 --reason "identity needs confirmation" --json
anatomia review freeze analysis:demo --revision analysis-revision:demo:v2 --confirm --json
anatomia review fork analysis:demo --revision analysis-revision:demo:v2 --json
```

## Boundaries

- Never promote a model-suggested real-person identity without authorization and human confirmation.
- Never infer training rights from source availability.
- Mark camera, lens, lighting, material and intent fields as estimated when not directly evidenced.
- Frozen revisions are immutable; use fork.
- Keep review notes concise and redacted; do not store raw prompts or provider payloads.

## Output

Return revision/version, decision, blocker changes, unresolved risks, evidence refs, actor authority, and the next real command.

## Validation

```bash
anatomia review validate <analysis-ref> --revision <revision-ref> --json
anatomia analysis show <analysis-ref> --revision <revision-ref> --json
```
