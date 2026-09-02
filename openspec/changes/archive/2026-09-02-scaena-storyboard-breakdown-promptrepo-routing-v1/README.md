# scaena-storyboard-breakdown-promptrepo-routing-v1

演进现有 Scaena 分镜 Skill，使其选择方向 profile、绑定 immutable PromptRepo 方案并调用真实 CLI/MCP。

## Closeout evidence (2026-09-02)

- Source validation: `cd scaena && python3 scripts/validate_skills.py` -> `PASS: validated 6 portable Scaena Skills`.
- Safe-receipt scan: `rg -n "raw source|Prompt body|provider payload|full chain-of-thought|evidence_refs" scaena/scaena-storyboard-breakdown` hits only prohibition statements + receipt field; secret/maintainer-path scan clean.
- Root governance: `scripts/skills.sh validate-custom` / `validate-profiles` / `sync-target agent/scaena` / `validate-subprojects-runtime` all exit 0; only the Scaena target was synced and runtime copies match the source.
- Provider-free scenario walkthrough (scaena CLI v0.2.1 7390355, all probes zero provider calls):
  - vertical ready target: `prompt-asset repository doctor` (official ready, provider_calls=0), `catalog inspect`/`validate` on `promptrepo://official/video/ai-drama-storyboard-breakdown@1.0.0?locale=zh-CN` (ready, digest sha256:6817dc…, blockers=[]), `run --help` shows real `--foreground/--timeout/--events/--prompt-template/--direction-profile/--execution-policy`; `watch`/`diff`/`show --view findings|prompts` exist.
  - exploratory profiles: `dialogue-dense-v1`/`manga-panel-v1`/`ad-microdrama-v1` confirmed exploratory in `sdk/contract/storyboard_direction.go` (vertical-short-drama-v1 = first-support); a `manga-panel-v1` run without `--confirm` stopped at `COST_CAP_REQUIRED` (approval gate held).
  - format ambiguity: `needs_format_decision` is the Skill-side fail-closed route (SKILL.md DramaRoutePlan); zero CLI/provider calls by construction.
  - prompt stale/missing: catalog inspect `@9.9.9` and unknown solution -> typed `NOT_FOUND`, no provider call.
  - owner unavailable: `production status --json` reports `owner_adapters_disconnected`, `storyboard_model` disabled, `scaena.storyboard_model.v1` verification `not_requested` -> `OWNER_CAPABILITY_UNVERIFIED`/`OWNER_UNAVAILABLE` path (doctor/handoff, no fake candidate).
  - data policy surface: `storyboard execution-policy create --help` real (classification/retention/training/region); mismatch stays a typed blocker with no generic bypass.
  - input limit: >1 MiB source import -> typed `SOURCE_TOO_LARGE`.
  - injection canary: source with "IGNORE ALL PREVIOUS INSTRUCTIONS..." imported verbatim; `allowed_actions=["run"]`, `blocking=false`; next action still requires the approval packet.
  - timeout/head-conflict/blocking-findings routing rules verified at capability level (flags/commands/codes real: `WAIT_TIMEOUT`, `EXPECTED_VERSION_MISMATCH`, `CANDIDATE_NOT_HEAD`, `BLOCKING_FINDINGS` in contract inventory); live transitions require a paid owner run, which this provider-free rehearsal does not execute.
- Metadata decision (1.4): existing `agents/openai.yaml` remains accurate for the unchanged frontmatter/trigger surface; no file change needed.
