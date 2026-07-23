---
name: anatomia-video-analysis-router
description: Use when registering, starting, resuming, inspecting, cancelling, or routing an Anatomia video decomposition job across live-action, anime, CG, short-video, commercial, tutorial, music-video, or documentary profiles through the Anatomia CLI or API.
---

# Anatomia Video Analysis Router

Use Anatomia as the video-analysis owner. Do not replace it with Scaena, Eikona, Sonora, MediaHub, or a generic model caption.

## Inputs

- Authorized local source or approved source ref.
- Goal: `study`, `recreate`, `production`, or `dataset`.
- Optional domain/profile, budget, review policy, and target owner.

## Workflow

1. Confirm source permission and avoid unsupported arbitrary-site downloads.
2. Use `domain=auto` unless the user explicitly chooses a domain.
3. Choose the narrowest profile that preserves the requested outputs.
4. Start the analysis and capture `analysis_ref`, `job_ref`, status, blockers, and event URL.
5. Resume retryable partial work; never restart a duplicate job with the same fingerprint.
6. Route review work to `$anatomia-storyboard-reviewer` and export/handoff work to `$anatomia-asset-handoff-builder`.

## Commands

```bash
anatomia source add ./video.mp4 --permission owned --json
anatomia analyze start source-video:demo --domain auto --mode production --profile balanced --json
anatomia analyze watch analysis:demo --events
anatomia analysis show analysis:demo --json
anatomia analyze cancel analysis:demo --json
```

## Boundaries

- Treat model results as candidate observations, not accepted facts.
- Keep uncertain identity, rights, lens, lighting, material, and intent fields reviewable.
- Do not write `.anatomia/**` structured state by hand.
- Do not expose credentials, raw provider payloads, private tool arguments, full reasoning, or host absolute paths.
- Do not invoke Eikona or Sonora generation unless the user requests a downstream handoff and required approval gates pass.

## Output

Return the selected domain/mode/profile, analysis/job refs, status, blockers, available actions, artifact/evidence refs, and the next real command.

## Validation

```bash
anatomia analysis show <analysis-ref> --json
anatomia doctor --json
```
