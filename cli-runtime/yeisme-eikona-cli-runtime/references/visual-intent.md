## Visual Intent Evidence

The runtime consumes validated `eikona.visual_intent.v1` evidence through `eikona workflow import intent`. It is the only Skill responsible for provider execution and artifact lifecycle. Evidence files (`visual_intent.json`, `skill_receipt.json`, `intent_compile.json`) are written under each run directory and linked through existing runstore paths.

The runtime distinguishes claimed from verified skill identity; unverified receipts cannot support promoted/core evidence. Default model: `openai/gpt-5.4-image-2`.

Contract reference: `../eikona-visual-router/references/visual-intent-contract.md`.

### Canvas recovery implementation boundary

- Use `--full-body` for versioned framing controls; add `--require-review feet` when visible feet are required. An intact hem does not prove visible feet. Read `eikona review composition RUN_ID --artifact ARTIFACT_ID --json` and inspect the complete original before recording observations.
- Explicit `--recovery-policy` accepts configured candidates and bounded attempts/deadlines. Only adapter-proven pre-generation rejection or local non-submission permits switching. Read `eikona recovery show RECOVERY_REF --json`; `deferred` is a durable unknown outcome, not permission to regenerate. Legacy retry must not bypass this policy.
- Explicit background recovery uses the existing worker. Read child run IDs from `recovery.attempts`; the coordinator owns no copied images. Automatic foreground-to-background handoff, automatic unknown-submit lookup and unconfigured candidate discovery are not implemented. Private digest-only prompt sources currently require foreground execution.
- A gateway tier without a trusted native pixel table remains `unverified`, even when its observed ratio is correct. Never promote measured samples into a guaranteed tier table. Recovery charges must distinguish provider settlement from catalog estimates; historical `actual_usd` fallback values are not independent billing evidence. Proven no-generation rejection does not prove zero cost: without a calculated cost, a frozen provisional reservation, or explicit unknown-cost authority, `needs_policy_change/unknown_settlement_not_authorized` stops switching when settlement remains unknown. Inspect the existing handle instead of resubmitting.
- Preparation now exposes local `recovery_candidates` admission and frozen canvas digests. This is not proof of online availability. `recover_artifact` means the provider generated an image but original materialization is incomplete: use the existing child run's `resume --download-only` only when job evidence exists; never start a new generation to replace an unknown outcome. Recovered original bytes make the handle reviewable while dimension and composition gates remain independent.
- Recovery candidate normalization prioritizes same-model alternatives before allowlisted cross-model candidates, retaining order within each group. Read the prepared candidate order rather than inferring it from the raw input list.
- A recovery handle's availability is checked against current original bytes. Missing originals return `recover_artifact`; a late original recovered from an accepted job can become `review_artifact` without a new submission. Neither transition bypasses dimension/composition review or rewrites historical lineage.
- Follow the returned `next_step`/MCP `next_action` or CLI `action.next`. A saved original provider job permits the existing `resume` path; unknown submission without a job permits only recovery inspection. These recommendations do not grant broader authority or permit a new generation Submit.
- New recovery preparations default `lookup_timeout_seconds` to 120 (0 disables it). On REMOTE_TIMEOUT after acceptance with a saved provider job, the service claims one bounded existing-job lookup under the root deadline. A recovered original is returned with `review_artifact` while timeout history remains; read both run status and recovery before choosing another action. No-job unknown submissions are never automatically regenerated or queried through an invented lookup endpoint.
- For full trailing fabric, use `--complete-drapery` on generate/edit/preparation preview. It freezes full-body framing plus `accessory_extent`; add `--require-review feet` separately when visible feet are needed. Ordinary `--full-body` does not imply the new drapery requirement, and old preparations are not silently upgraded.

### Official pricing and provisional budget

- Discover installed `pricing show/quote/set/unset` before use. Quotes are offline; price changes use the owner host's config CLI, not hand-written metadata. Channel/model overrides take priority over model defaults and verified official cards. A partial override never borrows missing official components.
- New billing receipts keep `calculated_usd`, `reserved_usd`, `budget_usd`, `basis` and price snapshots separate from `actual_usd`. Measured costs and frozen estimates can advance bounded recovery without a verified provider invoice. Unknown submission still forbids resubmission.
- Per-image pricing requires exact operation/quality/resolution and confirmed generated count. Do not equate a native tier with a pixel size, count downloaded files as generated images, or bill image output both by tokens and by image.
- No official price mapping is assumed for `openai/gpt-5.4-image-2`; keep the configured model and resolve a missing price through explicit owner configuration. Never restore a hard-coded gateway discount or borrow another model's official price.
- Without a CLI, discover `pricing.quote` through registered MCP schemas and `eikona://docs/pricing`. Do not send credentials, prompts, or client-supplied price snapshots to the quote action.

### DriveBridge remote CLI interaction

- Development assets saveback select/status/resume/cancel, feedback effort and report effort support optional --endpoint/--key-file/--scope. Reuse the existing typed SDK and upload transport; incomplete explicit remote options must fail instead of silently writing local state.
- Preserve local owner-host defaults when remote options are absent. Source connection configuration stays on the owner host; operator/service-api purpose is distinct from input-only permission.
- All structured modes use structuredOutputEnabled and the shared renderer. blocked/partial transfer results retain original IDs and advisory recovery; do not report them as completed deliveries.
- For client-without-CLI interaction, use advertised MCP schemas and eikona://docs/drivebridge. Computer-local files need a local reader/relay or existing input page, never remote filesystem path interpretation.
- Keep the independently frozen recovery release separate from later DriveBridge interaction changes. Local verification does not publish or deploy a service.
