# Handoff

## Troubleshooting

- Exit 2 with `video_transform_usage_invalid`: fix the flags (ordered `--start/--end`, required `--source`/`--source-ref`, known `--purpose`) and rerun; nothing ran and no artifact was written.
- `grayscale_request_invalid`: the window is outside 3-10 seconds, the source exceeds 30fps, the long edge exceeds 1280, or chunk frames exceed 4096. Re-encode or narrow the window; do not retry unchanged.
- `shot_list_invalid`: the probe lacked a usable rational time base or the shot list asset is malformed. Re-run detect with the same `--source-ref`; never hand-edit the asset.
- `ffmpeg` missing or probe failure: install ffmpeg/ffprobe on PATH; these transforms never call a provider, so a provider error means the wrong command was used.
- Duplicate retries are safe: identical normalized inputs return the same digests without duplicate materialization (HTTP jobs replay the stored job).

## Boundaries

- Grayscale utility output is `evidence_binding=none`; it never enters a SpatialEvidenceBundle except through standard candidate admission.
- Shot lists and extracted clips/frames are segmentation evidence. `video shots` has no storyboard/review/freeze verbs; canonical production storyboard semantics belong to Scaena.
- Placeholder output discloses `feature_gaps=face_presence,text_region_score` and `selection_method` per purpose; a fallback selection is never a full-feature selection.
- Model analysis on a registered ref: `$anatomia-video-evidence-navigator`. Package handoff: `$anatomia-asset-handoff-builder`. Do not include credentials, raw provider payloads, or host absolute paths in handoffs.
