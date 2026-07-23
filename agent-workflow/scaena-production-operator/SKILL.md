---
name: scaena-production-operator
description: Use when planning, running, resuming, repairing, reviewing, or verifying a Scaena short-drama or comic-drama production from screenplay through subject asset readiness, accepted shot assets, motion preview, timeline, and export package, especially for frozen character/style/location/prop assets, generation preflight, consistency, target-duration coverage, blocking findings, or multi-session handoff.
---

# Scaena Production Operator

Operate Scaena as a staged production system. Do not equate generated files, fixture duration, or successful commands with a production-ready episode.

## Inputs

- Project path and source screenplay or existing `resume_ref`.
- Target duration, platform, aspect ratio, episode scope, quality tier, cost ceiling, and external-side-effect policy.
- Existing ProductionGraph, accepted asset, quality, preview, timeline, export, and evidence refs.

## Output

Return a compact stage receipt:

```text
status
stage
run_ref
target_duration
covered_duration
accepted_refs
failed_refs
blocking_findings
subject_readiness
generation_preflight_ref
next_command
resume_ref
evidence_refs
```

Use `--agent` for routine inspection and handoff. Use `--json` only when exact nested fields are required. Never paste raw provider payloads, full logs, hidden prompts, private tool arguments, or full chain-of-thought into the conversation.

## Workflow

### 1. Inspect Before Mutating

Enter `agent/scaena`, read its `AGENTS.md`, and locate the project. Inspect the narrowest current state:

```bash
scaena doctor --agent
scaena board --project <project-path> --agent
scaena workflow status <workflow-run-ref> --project <project-path> --agent
scaena production graph show <production-graph-ref> --json
```

If a referenced command is unavailable in the installed version, run `scaena help` or the relevant command-group help and use the supported equivalent. Do not invent a replacement command or hand-write `.scaena` state.

### 2. Lock Brief And Timing

Confirm target duration, platform, aspect ratio, episode interpretation, canonical screenplay ref, scene/beat scope, and approval policy before image generation.

Calculate coverage from ProductionGraph shot durations. Treat `sum(shot.duration_seconds) < target_duration` as blocking even when every existing shot has an image. For a 180-second target, 10 five-second shots cover only 50 seconds.

Create or revise the production plan through Scaena commands and record the resulting refs. Do not treat `--episodes 3` as equivalent to a three-minute target.

### 3. Lock Subject Asset Foundation

Before any episode, shot, cover, keyframe, or motion generation, use `$scaena-subject-asset-readiness`.

Require accepted source facts, a frozen project style, frozen primary/secondary subject versions, required wardrobe/location/prop anchors, exact shot bindings, rights, and a current generation preflight. Legal filing/permission binding alone is insufficient.

If the installed Scaena version lacks readiness/freeze/preflight commands, report the capability gap and stop production generation. Do not use a successful `visual pack plan/render`, fixture accepted state, empty `reference_asset_refs`, or `--confirm` as a substitute.

Only `subject_candidate`, `subject_reference`, and `look_development` may proceed before freeze, and their outputs must remain non-production. Route candidate creation or correction to `$eikona-subject-asset-director`.

### 4. Build Asset Budget

Budget reusable and per-shot requirements before generation:

- character identity, costume, expression, pose, and continuity variants;
- locations, establishing views, lighting/time variants, props, and rights;
- per-shot keyframes, motion clips, voice, music, SFX, subtitles, and transitions;
- provider attempts, cost ceiling, review batches, fallback, and reuse refs.

Use average shot duration only as a planning estimate. The hard gate is complete timeline coverage plus accepted requirements. Read [production-gates.md](references/production-gates.md) for the required gate matrix.

### 5. Produce In Batches

Process one episode, scene group, or shot batch per session. Reuse accepted assets and skip completed nodes. Use Eikona through supported Scaena/Eikona API or SDK workflows; do not create provider scripts or service-side CLI fallbacks.

Inspect and bind production assets with commands such as:

```bash
scaena asset center --project <project-path> --agent
scaena character bible show --project <project-path> --character <character-ref> --json
scaena asset subject bind --graph <production-graph-ref> --character <character-ref> --filing <filing-id> --permission licensed --json
scaena visual pack plan --graph <production-graph-ref> --json
scaena shot board --project <project-path> --episode <episode-ref> --agent
```

`asset subject bind` only establishes filing/permission facts; it does not freeze visual identity. Generated Eikona artifacts become production assets only after import, exact frozen-version binding, rights checks, current preflight, and Scaena consistency review acceptance.

### 6. Review And Repair

Run quality and continuity checks before motion preview:

```bash
scaena quality check --graph <production-graph-ref> --json
scaena continuity check --project <project-path> --scope <episode-ref> --json
```

If blocked, load only the finding, affected refs, and repair action. Resume or repair instead of replaying the whole workflow:

```bash
scaena workflow resume <workflow-run-ref> --project <project-path> --json
scaena workflow repair plan --run <workflow-run-ref> --json
scaena workflow repair run --repair <repair-ref> --json
```

Never overwrite a canonical state with a hand-authored report. When report and projection disagree, treat CLI/application state and evidence refs as authoritative and record the drift as a finding.

### 7. Preview Progressively

Run preview gates in order and stop on blockers:

```bash
scaena video motion-preview --graph <production-graph-ref> --mode probe --confirm --json
scaena video motion-preview --graph <production-graph-ref> --mode preview-batch --confirm --json
scaena video motion-preview --graph <production-graph-ref> --mode full-preview --confirm --budget-ok --quota-ok --json
```

Probe actual media duration with `ffprobe`. A fixture cut whose duration matches the target is not sufficient when its review is pending, motion clips are placeholders, timeline coverage is incomplete, or production export is blocked.

### 8. Export Only After Completion Gates

Plan before confirming:

```bash
scaena export package --dry-run --profile <profile> --to <output-path> --json
scaena export package --confirm --profile <profile> --to <output-path> --json
```

Require zero blocking findings, accepted required assets, timeline and audio/subtitle alignment, playable preview, rights, manifest, checksums, and evidence refs. Fail closed when `production_allowed=false` or the command requests repair.

### 9. End The Session With Handoff

Do not carry the full conversation into the next stage. Return only the compact receipt plus the exact next command, expected effect, side-effect class, and stop condition. A new session must resume from refs rather than reread the full repository or provider output.

## Boundaries

- Keep Scaena as the short-drama production truth; do not reimplement ProductionGraph or acceptance in Studio Backend skills.
- Keep Eikona as visual run/artifact truth; do not call provider SDKs directly.
- Keep Auctra source acceptance, Eikona candidate feedback, Scaena subject freeze, and Scaena shot acceptance as separate decisions.
- Do not generate Scaena production visuals without a current passed generation preflight.
- Do not claim completion from file counts, fixture success, or command exit zero alone.
- Do not publish, spend externally, delete, or batch mutate without explicit authority.
- Do not edit `.scaena` structured files, SQLite rows, manifests, receipts, or evidence metadata by hand.

## Validation

- Verify subject readiness/frozen versions/preflight first, then ProductionGraph duration and requirements, quality/continuity findings, preview media duration, review state, and export readiness independently.
- Treat a production request with missing reference/style/preflight facts as a blocking defect even if a command returns success.
- Preserve integration evidence under `temp/integration-test-runs/<run-id>/` with redaction and original exit codes.
- Prefer focused project commands; do not run root-wide scans or read both generated skill mirrors.
