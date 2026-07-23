# Visual Intent Contract (eikona.visual_intent.v1)

Shared reference for all Eikona Visual Operators. One level deep from SKILL.md.

## Purpose

Routers, readiness gates, directors, and the Eikona runtime compiler exchange a versioned provider-neutral intent envelope instead of prose or provider-specific commands. The intent separates creative decisions from provider execution.

## Schema (required fields)

| Field | Description |
| --- | --- |
| `schema_version` | `eikona.visual_intent.v1` |
| `intent_id` | Unique id, `vi_` prefix, lowercase/digits/`-`/`_` |
| `purpose` | `fresh_generation` \| `reference_edit` \| `asset_reuse` |
| `skill_chain` | Bounded chain: 1 router + 1 primary_director + optional gates |
| `readiness` | Monotonic status: `ready` > `candidate_only` > `blocked` > `stale` |
| `review_rubric` | Closed-set identifiers (see below) |

## Optional fields

- `scenario`, `source_refs`, `references`, `reference_mode`, `canvas`, `content_constraints`, `execution_policy`, `handoff`

## Authority order (highest wins)

```
user_decision > readiness_gate > project_rights_policy > accepted_brief > primary_director > domain_router > runtime_default
```

Lower authority may narrow optional choices but cannot weaken safety/readiness/rights/policy restrictions. Readiness is monotonic: once stricter, always stricter within one compile.

## Forbidden in any field

- Secrets (API keys, tokens, bearer strings)
- Image bytes (data URLs, base64)
- Absolute private paths (`/home/...`, `/Users/...`, `C:\Users\...`)
- Shell/exec instructions (`curl`, `bash`, `subprocess`)
- Full prompt text (use resource URIs instead)

## Resource URI schemes

- `eikona://artifact/<id>`, `eikona://brief/<id>`, `eikona://prompt/<id>`
- `auctra://brief/<id>`, `scaena://subject/<id>`
- `fixture:<name>`
- `runs/<run_id>/<evidence_path>`

## Workflow compilation

```bash
eikona workflow import intent -f visual-intent.yaml --out workflow.yaml --json
eikona workflow validate -f workflow.yaml --json
eikona workflow plan -f workflow.yaml --json
```

Blocked or stale readiness fails compilation. Model defaults to `openai:gpt-image-2`; provider/credential resolution remains runtime responsibility.

## Evidence files (per run)

- `visual_intent.json`: normalized intent + digest
- `skill_receipt.json`: claimed/verified skill identity
- `intent_compile.json`: field sources, overrides, warnings, workflow ref

## Review rubric identifiers

`native_resolution`, `title_legibility`, `no_pseudo_cjk`, `title_safe`, `subject_identity`, `style_consistency`, `palette_alignment`, `text_density`, `composition_focus`, `claim_safety`

## Lifecycle states

`candidate` → `incubator` → `promoted` → `core`. Promotion is explicit and evidence-backed; reports never auto-promote.
