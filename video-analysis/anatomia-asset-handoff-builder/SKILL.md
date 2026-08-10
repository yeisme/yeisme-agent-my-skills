---
name: anatomia-asset-handoff-builder
description: Use when exporting Anatomia storyboard, original clip, representative frame, transcript, subtitle, asset observation, prompt, manifest, or evidence packages, or when handing an accepted analysis to Scaena, Eikona, Sonora, or MediaHub through provider-neutral refs.
---

# Anatomia Asset Handoff Builder

Build atomic, lineage-preserving packages from an accepted revision. Route each downstream action to the owning Yeisme project.

## Inputs

- Accepted or frozen analysis revision.
- Requested formats and target directory.
- Optional target owner: `scaena`, `eikona`, `sonora`, or `mediahub`.

## Workflow

1. Verify the revision is eligible for the requested readiness level.
2. Select only required clips, frames, transcripts, prompts and reports.
3. Export atomically with manifest, checksums, permission snapshot, lineage and evidence refs.
4. For handoff, create a provider-neutral receipt with target owner and blockers.
5. Use the target owner's stable API/SDK; do not read its private database or invoke its CLI as a production service transport.
6. Report partial success and recovery actions instead of claiming an all-or-nothing transaction.

## Commands

```bash
anatomia export package analysis:demo --revision analysis-revision:demo:v2 --format json,markdown,clips,frames --to ./dist --json
anatomia handoff scaena analysis:demo --revision analysis-revision:demo:v2 --project project:demo --json
anatomia handoff eikona analysis:demo --revision analysis-revision:demo:v2 --assets reference_frames,prompt_pack --json
anatomia handoff sonora analysis:demo --revision analysis-revision:demo:v2 --assets transcript,audio_cues --json
anatomia handoff mediahub analysis:demo --revision analysis-revision:demo:v2 --json
```

## Owner Boundaries

- Scaena owns production review, frozen editing scripts and ProductionGraph/EditTimeline materialization.
- Eikona owns image generation, artifacts, feedback and visual memory. New image generation defaults use `openai/gpt-5.4-image-2`; `gpt-5.4-image-2` and `gpt-image-2` remain accepted short aliases.
- Sonora owns voice, music, SFX generation, rights and audio review.
- MediaHub owns library ingest, Jellyfin organization, browse and review.
- Connectors owns chat delivery and provider identity.

## Safety

- Never include credentials, signed URLs, raw provider payloads, private tool arguments, hidden prompts or full reasoning.
- Do not export host absolute paths as stable refs.
- Do not overwrite a visible package on partial failure.
- Do not claim a prompt can faithfully reproduce protected identity, style or copyrighted content.

## Output

Return package/handoff ref, target owner, revision digest, artifact refs, manifest/checksum refs, status, blockers, recovery action and the next real command.

## Validation

```bash
anatomia export verify <package-ref> --json
anatomia handoff show <handoff-ref> --json
```
