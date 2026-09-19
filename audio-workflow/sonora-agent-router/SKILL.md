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
| Discover installed commands | `sonora commands suggest "<intent>" --agent` |
| Discover product Skills | `sonora skills list --agent` / `sonora skills suggest "<intent>" --agent` |
| Workspace readiness | `sonora doctor --agent` |
| Initialize a project | `sonora init --project . --agent` |
| Adapted providers plus local credential status | `sonora provider list --agent` |
| Full TTS provider capability matrix | `sonora tts providers list --json` |
| Built-in local TTS models | `sonora tts models list --local --agent` |
| Voice models for one provider | `sonora tts models list --provider <provider-id> --agent` |
| Voices for one provider | `sonora tts voices list --provider <provider-id> --agent` |
| Music provider catalog | `sonora music providers list --json` |
| Music fixture lifecycle | `sonora music brief create --purpose <purpose> --instrumental --agent` → `sonora music plan create --brief <ref> --provider fixture --agent` → `sonora music generate --plan <ref> --idempotency-key <key> --agent` |
| Music cover (suno-kie) | `sonora music brief create --mode cover --source-asset <audio-asset-ref> --output-format mp3 --json` → `sonora music plan create --capability cover --provider suno-kie --rights-snapshot <ref> --json` → approval → `sonora music generate ... --confirm-external-call --confirm-unknown-price --json` |
| Music cover HTTP/SDK | `CreateMusicBrief`/`POST /api/v1/music/briefs` (`mode=cover`, `source_asset_refs`) → `CreateMusicPlan` (`provider_capability=cover`, `rights_snapshot_refs`) → `IssueMusicApproval` → `CreateMusicJob` (`confirm_live`, `confirm_unknown_price`) |
| Music job status/list/reconcile | `sonora music job status <job-id> --agent` / `sonora music job list --agent` / `sonora music job reconcile <job-id> --agent` |
| Music approval lane (paid providers) | `sonora music approval issue --plan <ref> --project-id <p> --authorization-epoch <e> --idempotency-key <k> --max-cost-usd <cap> --agent` |
| Music review and handoff | `sonora music review accept <job-id> --agent` → `sonora music handoff get <job-id> --agent` |
| Music cue orchestration | `sonora music cue --help`（plan/candidates/placement/preview-mix/handoff） |
| Local fixture flow | `sonora bridge scaena plan --graph <production-graph-ref> --agent` |
| Compile AI-drama shot audio intent | `sonora bridge scaena episode-audio compile-intent --from <handoff.json> --agent` |
| Import AI-drama shot audio intent | `sonora bridge scaena episode-audio import-intent --from <handoff.json> --idempotency-key <key> --agent` |
| Register video-model native audio for review | `sonora audio native register --video <video-asset-ref> --source <provider> --agent` |
| Compare replacement/final mix routes | `sonora audio strategy compare --plan <language-plan-ref> --agent` |
| Render or review receipt | `sonora render plan --plan <language-plan-ref> --voice-pack fixture --confirm --agent` |
| Detailed strategy comparison | `sonora audio strategy compare --plan <language-plan-ref> --json` |

`provider list` 同时给出代码 catalog 与本地 credential 状态，不访问远程 provider。`credential_missing` 不是未适配。`tts models list --local` 只列内建本地模型生命周期，不代表已部署或可渲染。测试 provider 不进入 `provider list`。

## Credentials

本地默认把 key 写进用户级配置的单一槽，不要再配 `api_key_env`：

```yaml
# ~/.sonora/config.yaml  (0600)
providers:
  suno-kie:
    enabled: true
    base_url: https://api.kie.ai
    upload_base_url: https://kieai.redpandaai.co
    api_key: <inline-key>
```

`api_key` 按内容识别：内联密钥、环境变量名，或 `yeisme-credential://...`。槽为空才读进程环境 `SONORA_<PROVIDER>_API_KEY`。跨工具复用或轮换再用 `credentialctl export --to yeisme-target://sonora/provider/<id>`，写入的仍是同一 `api_key` 槽。Agent 不得把真实 key 写进项目配置、docs、evidence 或 stdout。

## Remote Safety

### Local media upload

For client audio/video files on a connected MCP without a local Sonora CLI, first read `sonora://input/capabilities` and the live execute schemas. If the explicitly bound input lane is enabled, use `input.prepare` with purpose `audio_input` and the execute-level idempotency key; omit file metadata until selected. A capable host streams HTTP with the transient grant, while a pure MCP client uses the one-time page and polls `input.status`. Completion supplies only the managed input reference; renew/cancel/recovery use the original request. Do not persist links or send a long-lived bearer to the transfer interface. If the lane is unconfigured, report that exact limitation.

When a matching local CLI is installed, first discover `sonora upload inspect` and `sonora upload put` through `sonora commands describe`. Use `sonora upload inspect --file <client-file> --mime <media-mime> --agent` to compute size and SHA-256 without exposing the file path in the result. Do not send a client absolute path or file bytes to legacy MCP actions; the dedicated input.upload_base64 exception is described below. Images belong to Eikona/Scaena; use their canonical reference instead of creating a Sonora image store. Sonora's local upload flow needs no S3; do not invent an S3 switch for it or change another owner's existing storage mode.

Read MCP resource `sonora://docs/local-media-upload` before operating the upload session. Use `media.upload.begin` with a stable idempotency key and file metadata, stream bytes using `sonora upload put --endpoint <issuing-owner-origin> --session <session-id> --file <client-file> --grant-stdin --agent`, then call `media.upload.complete`. Pass the transient grant through stdin, never command arguments, logs, notes, persistent scripts or evidence. The server must explicitly bind upload actor/project; client-supplied identity does not authorize a session. Do not follow a transfer redirect or attach a service/MCP bearer to the grant-only PUT.

On interruption, inspect the same session before retrying. Capacity errors allow a later retry on that session; an expired session requires a new key. `media.upload.abort` and `media.upload.cleanup` affect unfinished inputs, not completed assets. Do not manually delete private storage to repair an upload. Configuration and local executable discovery use `sonora config upload set` and `sonora config upload doctor`; doctor does not prove deployment reachability.

Completion returns a `sonora://media-input/` reference, not permission to transcribe, clone a voice or publish. `media.upload.prepare_audio` requires a current approved transcription snapshot for `sonora://audio-asset/upload-<session_id>` and returns a managed audio asset. Submit that asset through the existing CLI/HTTP transcription workflow with its valid permission snapshot; do not invent a transcription MCP action. Keep review and paid-provider authorization separate. If these commands/actions are absent in the installed build, report the version gap and hand off to the Sonora owner; do not silently fall back to a provider call or another storage service.

1. Inspect `sonora provider doctor --provider <provider-id> --agent` before a remote action.
2. Estimate cost with `sonora tts estimate --plan <language-plan-ref> --provider <provider-id> --voice-model <voice-model-ref> --max-cost-usd <limit> --agent`.
3. Require explicit user authorization before a command with `--confirm-external-call`.
4. Voice creation or real-person reference audio also requires `--permission licensed` and redacted permission evidence.

## Music Generation（BGM / cue）

真实付费生成只走 `suno-kie`（kie.ai 聚合渠道，非官方 Suno API；配置见 Credentials 节）或受限 preview 的 `elevenlabs`；`suno-web-bridge` 是用户自部署实验桥，`suno` 官方占位保持 disabled，绝不互相 fallback。标准链：`music brief create`（`--duration-ms` 目标时长、`--instrumental`、`--output-format mp3`）→ `music plan create`（显式 `--provider`/`--model`，未知模型 fail-closed）→ `music approval issue`（绑定 plan/预算/身份/幂等，≤900s 单次消费）→ `music generate`（复用同一 `--idempotency-key`、`--project-id`、`--authorization-epoch`，加 `--confirm-external-call`；`unknown_preview` 渠道再加 `--confirm-unknown-price`）→ `music job reconcile` → `music review accept` → `music handoff get`。

模型选择：`music providers list --json` 的 `supported_models` 带 `duration_support`（effective/ineffective/unverified/unsupported）。时长敏感的 BGM 用 `V6`（实测 30s→30.0s 精确）；`V6_MINI` 忽略 duration（实测 30s→~185s）只用于不在意时长的场景；`V6_WILD` 见最新 notes；`V4`–`V5_5` 已停用不可选。非 instrumental 或 <10s/>360s 的 brief 时长提示不生效。

Cover：`music brief create` 用 `--mode cover` 且恰好一个受管 `--source-asset`（owned snapshot、非商用、无歌词、源 ≤8 分钟）；plan `--capability cover` 并带 `--rights-snapshot`。没有 `sonora music rights` 命令。kie 在 `music generate` 时才把文件上传到 `upload_base_url` 再走 `upload-and-cover-audio`（真实 live 已包含这次上传）。不要假设时长等于源曲（V6 live 20s 源 → ~235s）。extend/mashup 仍不可用。

MCP 客户端：先读内置资源 `sonora://docs/music`（provider 身份、模型矩阵、门控、错误码与恢复、terms、cover 参考输入），动作面 `music.*`（17 个生命周期动作）与 `music.cue.*`（12 个编排动作，零外呼）；`music.generate` 对所有 provider 统一强制幂等键、正预算、`approval_ref`、`confirm_external_call=true`。artifact host 首次被 `artifact_host_forbidden` 拦截时按错误中的宿主补 `providers.suno-kie.artifact_hosts` 再 reconcile，不要重复提交。

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

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Unknown command | `sonora commands suggest "<intent>" --agent` | Do not invent verbs |
| `credential_missing` | User-level `~/.sonora/config.yaml` `api_key` slot | Not an adapter gap; do not write keys to the repo |
| Paid TTS/music without confirm | Estimate then `--confirm-external-call` | `unknown_preview` also needs `--confirm-unknown-price` |
| Cover/generate `artifact_host_forbidden` | Add host from the error, then `music job reconcile` | Do not resubmit |
| Native video audio treated as accepted mix | `sonora audio native register`; keep `pending_review` | Sonora never marks Scaena timeline accepted |
| Dialogue as first-line TTS on Seedance native shots | Leave `video_native`; only `replace_after_generation` is full TTS | Do not rebuild EpisodeAudioPlan by hand |

## Single-file multitransport intake

For a client file, discover `sonora://input/capabilities` and the installed execute schemas. Use `input.prepare` with purpose `audio_input` and one stable idempotency key. Prefer executable `object_storage` through the transient HTTP `POST /input-requests/{id}/transfer` plan, then `http_put`; a user may select/preview a file on the one-time page. Only when explicitly advertised, a client program may encode a file up to the owner's inline limit (default 4 MiB) for `input.upload_base64` with file name, MIME, size, SHA-256 and `data_base64`. The dedicated MCP envelope permits 6 MiB; ordinary/legacy actions retain their original limits. Never ask the model to produce or echo base64.

Call `input.complete` after transfer; repeated completion returns the original receipt. Query `input.status` before retry/switch, wait for active writers, and reuse the request. A failed auth, MIME, digest, permission or capacity check cannot be bypassed by switching transport. Keep temporary plans/grants/signatures and file bytes out of logs and notes. An object-store PUT receives only its required signed headers, never the MCP bearer or owner grant. Upload readiness does not approve generation, transcription, rights or canonical acceptance. Owner configuration is documented in the product's `docs/mcp-input-intake.md`; missing object storage does not disable separately configured HTTP/base64.
