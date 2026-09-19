# Eikona product contracts

Preserve these contracts when planning, documenting, or changing `cli/eikona`:

- Keep product planning and documentation headless: new roadmap items may improve generation quality, provider coverage, evidence, review/reuse, asset lifecycle, delivery, or consumer-neutral interfaces, but must not add an Eikona-owned Web/frontend backlog.
- `--json` output must remain machine-readable and stable for scripts, Ordo, CI, and shell pipelines: since v0.6.0 bare `--json` is the bounded compact default, `--json --compact` is its explicit equivalent, and `--json --full` is the permanent forensic projection. Routine agents still prefer `--agent`.
- New or changed CLI output must follow `ai-native-cli-output-contract`: human summary by default, strict `--json`, `--agent` for low-token parsing, optional `--events`, and secret-safe stdout/stderr separation.
- Local project docs and OpenSpec artifacts should be Chinese by default; human CLI output, help text, logs, and user-visible errors should be English unless the user explicitly requests another language for that artifact or the content is Chinese-language product content.
- Every successful provider artifact must be written through the run evidence store under `runs/<run_id>/outputs/`.
- Provider requests in tests must use `httptest` or repository test adapters; do not call real remote providers in automated tests.
- User-level local Eikona config or the local auth store may store plaintext provider keys when the user explicitly configures them; secrets must never be written to project YAML, YAML examples with real values, traces, provider jobs, artifact manifests, test snapshots, or README output.
- Eikona must not create, recommend, or read shell credential scripts for provider keys; use direct user config, `eikona auth set <channel> --api-key-stdin`, or process environment for CI and temporary overrides.
- Command examples in docs, help, skills, plans, reviews, and final responses must be real user-runnable commands such as `eikona workflow run ...`; do not expose local wrappers or agent-only prefixes.
- Command docs must cover every visible subcommand and explicitly mark hidden/internal entries such as `models`, `worker`, and disabled `video` when relevant.
- Do not add isolated scenario commands for Xiaohongshu, short-drama, product, game, docs, or graphic-design variants; scenario differences belong in workflow templates, prompt decks, prompt skills, profiles, style packs, assessment criteria, review policy, and recipe influence evidence.
- Prompt skills are provenance-bearing reusable prompt sources; prompt decks are versioned card-pull assets; workflows snapshot prompt refs and deck selections into run evidence. Later edits to prompt skills, decks, style packs, or recipes must not reinterpret old runs.
- Storage sync is backup/restore only by default: local output root remains the source of truth, S3-compatible storage is a mirror, `storage push` must produce encrypted content-addressed objects and receipts, and `pull`/`restore` must stage output instead of overwriting project files.
- Do not add real-time sync, file watchers, automatic bidirectional merge, or multi-device conflict resolution to Eikona without a separate OpenSpec change.
- Visual assessment and recipe reuse must be evidence-backed and explainable: store scores/tags/corrections/recipe influence as structured evidence, never as hidden reasoning or unbounded prose. Machine-only scores must not silently select winners without append-only human feedback.
