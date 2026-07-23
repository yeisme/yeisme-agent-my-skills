# Scaena Production Gates

Load this reference when creating an asset budget, deciding whether a stage may advance, or reviewing a claimed completed production.

## Gate Matrix

| Gate | Required facts | Blocking examples | Exit evidence |
| --- | --- | --- | --- |
| Brief Lock | target duration, episode scope, platform, aspect ratio, canonical screenplay | ambiguous “3 episodes” vs “3 minutes”, missing screenplay ref | brief ref, target facts |
| Timing Lock | scenes/beats/shots cover target duration | timeline gap, unbounded dialogue, shot total below target | ProductionGraph ref, covered duration |
| Asset Plan | reusable and per-shot requirements budgeted | missing character/location/prop/audio/subtitle requirement | AssetBudget or plan refs |
| Subject Candidate | accepted source/brief and reviewable identity/style/location/prop candidates exist | no character sheet, incomplete views, Eikona artifact not handed off | candidate set refs, owner evidence |
| Subject Freeze | required primary/secondary/style/wardrobe/location/prop versions human-reviewed and frozen | legal binding only, fixture accepted, Eikona feedback treated as freeze | frozen version refs/digests, freeze receipts |
| Shot Binding | each production shot pins exact frozen versions and continuity variants | missing rival/hero/location binding, stale wardrobe, unknown rights | binding refs/versions, rights refs |
| Generation Admission | current preflight passes immediately before owner submission | missing/stale preflight, empty references, unsupported reference model | preflight ref/digest, zero-call blocked evidence |
| Asset Lock | every required asset imported, reviewed, accepted, blob-backed | draft-only Eikona artifact, missing accepted still, placeholder clip | accepted asset refs, manifest revision |
| Motion Ready | quality and continuity blockers zero | `missing_subject_binding`, `missing_accepted_asset`, continuity conflict | quality report, continuity report |
| Preview Lock | probe, batch, and full preview are playable and representative | one-second placeholder, fixture-only output, duration mismatch | media refs, `ffprobe` duration, review refs |
| Edit Lock | timeline, voice, music, SFX, subtitles and transitions align | subtitle overflow, audio gap, unresolved edit finding | timeline/cut refs, scorecard |
| Delivery Lock | export allowed, review accepted, rights valid, manifest/checksum present | `production_allowed=false`, pending review, missing checksum | package ref, manifest, evidence refs |

## Asset Budget Fields

Record at least:

```text
target_duration
shot_duration_policy
estimated_shot_count
character_variants
location_variants
props
per_shot_requirements
audio_requirements
subtitle_requirements
reusable_refs
generation_attempt_cap
cost_ceiling
review_batches
fallback_strategy
```

For planning only, `estimated_shot_count = target_duration / average_shot_duration`. Do not hard-code the estimate as completion criteria. Completion uses actual shot durations and timeline coverage.

## Completion Audit

Use targeted queries instead of broad directory dumps:

```bash
jq '.data.production_graph | {shots:(.shots|length), duration_seconds:(.shots|map(.duration_seconds)|add)}' <production-graph.json>
find <project-path> -type f -name '*.mp4' -print
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <video-path>
```

Inspect quality, preview, cut, and export projections separately. Report contradictions between human-authored reports and current canonical projections.

## Compact Handoff

Use this exact shape between sessions:

```text
status=<ready|blocked|partial|complete>
stage=<brief|timing|assets|produce|review|assemble|verify>
run_ref=<ref>
target_duration=<seconds>
covered_duration=<seconds>
accepted_refs=<comma-separated refs>
failed_refs=<comma-separated refs>
blocking_findings=<codes/refs>
next_command=<real command>
resume_ref=<ref>
evidence_refs=<comma-separated refs>
```

`stage=assets` must distinguish `candidate_only`, `freeze_required`, `binding_required`, `preflight_required`, and `production_ready`. Do not collapse them into one accepted boolean.
