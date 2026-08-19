---
name: sonora-agent-router
description: Use when an agent needs to inspect, plan, render, review, or route Sonora voice and audio-asset workflows with the smallest safe CLI command and low-token output.
---

# Sonora Agent Router

## 职责边界（AI 做剧）

Seedance 2.0 已验证线路的对话镜默认由视频模型原生生成对白（`video_native`，台词进生成 prompt），Sonora 不再是逐句对白的第一生产者。Sonora 的默认职责：配乐、SFX/ambience、最终混音、原生音轨登记与审听证据、失败句补配（原生 review 失败的单句用 TTS 补配并进混音替换）。只有 `replace_after_generation` 镜头才由 Sonora 承担全部对白生产。

## Default Output

Use `--agent` for readiness checks, provider status, reference discovery, planning receipts, render receipts, review decisions, and ordinary local writes. Consume `action.*`, `fact.*`, `data.*`, and `evidence.*`; never parse human cards or `.sonora` private state.

Use `--json` only when the task needs full nested capabilities, strategy comparisons, schema validation, or detailed structured failure data. Return to `--agent` for follow-up reads when scalar output is enough.

## Routing

| Intent | Command |
| --- | --- |
| Workspace readiness | `sonora doctor --agent` |
| Initialize a project | `sonora init --project . --agent` |
| Provider status | `sonora provider list --agent` |
| Full provider capability matrix | `sonora tts providers list --json` |
| Voice models for one provider | `sonora tts voices list --provider <provider-id> --agent` |
| Local fixture flow | `sonora bridge scaena plan --graph <production-graph-ref> --agent` |
| Compile AI-drama shot audio intent | `sonora bridge scaena episode-audio compile-intent --from <handoff.json> --agent` |
| Import AI-drama shot audio intent | `sonora bridge scaena episode-audio import-intent --from <handoff.json> --idempotency-key <key> --agent` |
| Register video-model native audio for review | `sonora audio native register --video <video-asset-ref> --source <provider> --agent` |
| Compare replacement/final mix routes | `sonora audio strategy compare --plan <language-plan-ref> --agent` |
| Render or review receipt | `sonora render plan --plan <language-plan-ref> --voice-pack fixture --confirm --agent` |
| Detailed strategy comparison | `sonora audio strategy compare --plan <language-plan-ref> --json` |

## Remote Safety

1. Inspect `sonora provider doctor --provider <provider-id> --agent` before a remote action.
2. Estimate cost with `sonora tts estimate --plan <language-plan-ref> --provider <provider-id> --voice-model <voice-model-ref> --max-cost-usd <limit> --agent`.
3. Require explicit user authorization before a command with `--confirm-external-call`.
4. Voice creation or real-person reference audio also requires `--permission licensed` and redacted permission evidence.

## AI Drama ShotAudioIntent Handoff

When the caller comes from an AI drama director or Scaena production stage, first load `$ai-drama-router`'s `references/shot-audio-intent-contract.md` and require its versioned `ShotAudioIntent` contract.

- Consume shot/duration/dialogue/cue refs, provider audio policy, plan digest and final-mix owner binding; do not accept an unversioned prose-only “sound” column as the complete plan.
- Prefer one episode-level `sonora.drama-audio-intent.v1` projection generated from the Director's canonical ShotAudioIntent source. Do not ask the demo or Scaena to construct a second `EpisodeAudioPlan` by hand.
- Compile `ambience|foley|motif` to SFX cues, bind `music` to existing MusicCuePlan refs, bind `dialogue` to LanguagePlan/dialogue spans, and keep `silence` as a Sonora mix constraint rather than an audio asset.
- Use `compile-intent` for zero-write validation and `import-intent` for local structured persistence. These operator commands are not Scaena production service transport; production consumers use the stable API/SDK once the additive intent DTO is available.
- If the video has native audio, register it with `sonora audio native register`; the default result is `video_native_audio`, `pending_review`, `rights_risk=unknown`, `editability=replace_only`.
- For `replace_after_generation`, return replacement voice/SFX/music/mix refs and keep the native track as review evidence only.
- Return refs, revision/digest, duration/sync findings, rights/review state and repair command to Scaena. Never mark the Scaena timeline or production asset accepted from Sonora.
- A changed shot duration, dialogue span, cue timing, provider policy or parent video ref makes the old audio plan/mix stale.

## Tab Completion

Ask the user to install a matching shell script with `sonora completion <shell>`. The CLI supplies local candidates for provider IDs, catalog voice-model refs and project-local workflow refs; completion never performs a provider network call.

## Validation

Use `sonora <command> --agent` for low-token output checks and `sonora <command> --json` when validating complete payloads. Do not expose credentials, audio bytes, raw provider payloads, private tool arguments, or hidden reasoning.
