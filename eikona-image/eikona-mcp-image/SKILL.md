---
name: eikona-mcp-image
description: "Use when explicit Eikona or eikona-lan MCP image generation, editing, artifact delivery, or download recovery is requested. Prefer this direct Eikona flow over generic imagegen when Eikona is named or configured."
---

# Eikona MCP image fast path

Use the configured Eikona MCP as the primary path when the user explicitly
mentions Eikona or `eikona-lan`. Do not switch to a generic image-generation
skill unless the user explicitly asks for that fallback or Eikona returns a
typed blocker that requires it.

## Precision editing when advertised

Check installed capabilities before using `edit.prepare`, `edit.plan.show`, or `precision_edit`; development examples do not prove installed support. Provide a clean original first, plus exactly one annotation copy, mask, or typed regions. Keep annotation and mask out of ordinary reference images. If the agent already understands the marks, submit regions directly and skip model analysis.

Preserve the user or agent's explicit model/channel choice. GPT Image 2.5 Sunburst and Flare are optional choices, not forced defaults. Use strict PNG protection for new precision controls unless natural mode is explicitly requested. Clear requests submit one edit for all regions; ambiguous arrows, missing instructions or overlaps require preview and correction, not one generation per region or automatic visual retries.

Use `edit.prepare` with `analyze=true` only when analysis is intended and cost policy permits it; `dry_run=true` makes no model call. Reuse `edit_plan_ref` and inspect `analysis_run_id` after interruption. Correct regions through a child plan. The image run's cost is not the total analysis-plus-image cost. If capability is unavailable, report the installed limitation rather than inventing an action or installing updates automatically.

When advertised by the installed action contract, `inspect` accepts `refresh_cost: true` to recompute local workflow costs. Preserve unknown totals even when an orchestration component is priced. To recover a completed edit, pass its original `run_id` and `edit_plan_ref` to `edit`; verify the returned run and artifact references. Recovery errors require inspection, not automatic resubmission or claim-file removal. Project selection determines the output owner; source images require separate current authorization, including after a plan was prepared.

## Ordinary generation and editing

Call `eikona.execute` directly. Do not begin an ordinary request with
`eikona.search`, model-catalog scans, provider doctor, or `resources/read`.
Use `action: "generate"` for a new image and `action: "edit"` for a supplied
image, with a stable `idempotency_key` and the user intent. Preserve an
explicit supported Eikona model selection, including Grok or Midjourney. When
the user does not specify a model, default to `openai/gpt-5.4-image-2`. Do not
select test-only model identifiers.

For remote Eikona LAN MCP (`https://<host>:<port>/mcp`; non-loopback
endpoints require HTTPS), `edit`
`reference_image` must be a server-reachable `eikona://artifact/<handle>` or
run artifact URI, or a verified `eikona://asset/<id>` input reference. Do not pass the Codex/Mac host path (`/var/folders/...`,
`/Users/...`, Windows drive letters, clipboard temp files). Those files are
not on the Eikona server. For a client file, first read `eikona://input/capabilities` and use the advertised input action schemas. Do not generate an image as an upload/connectivity probe. Same-host CLI `--input` is unchanged.

When input intake is enabled for the current `media-input-v1` identity, create `input.prepare` with `args.purpose: "reference"`, the authorized scope and a stable input idempotency key. Omit file when metadata is unknown. A file-capable host consumes the transient grant link and streams HTTP without the product CLI; a pure MCP host offers the one-time page and polls `input.status`. Only the completed asset reference enters `edit`. Missing links require original-request recovery and explicit renewal through a compatible client, never a replacement generation. Keep links out of saved evidence. If the capability is absent, report the actual installed upload limitation and do not invent an action.

Keep the idempotency key as submission evidence. After a response returns a
`run_id`, use `eikona.execute` with `action: "wait"` (or `status`/`inspect`
when the typed response directs it) against that same run. Remote `wait` is a
bounded snapshot, not a block-until-image call. If the run is `queued`, poll
the same id. If it is `failed`, stop; do not resubmit that idempotency key
and do not treat queued-without-artifacts as a dead MCP. If the submit
transport outcome is lost before any `run_id` is received, report an
unknown outcome and stop: do not resubmit or claim that the idempotency key
reconciled the run. Only inspect readiness, a model, or a resource after a
typed Eikona error says that exact information is needed.
`AUTH_ACTION_DENIED` on `providers.doctor` from a generation-loop key is
purpose isolation, not proof the server is down.

## Artifact delivery and download recovery

### Canvas and bounded generation recovery

When the installed generation schema exposes `composition_requirements`, pass explicit full-body/margin/visibility requirements independently from `size` and `aspect`. A native 4k label is not automatically 4096 pixels. Inspect the complete original: cropped hems, occluded feet and preview-only crops are different observations. Use advertised `composition_observations` with current original refs and measured bounds; legacy pass strings do not satisfy new composition evidence.

When `recovery_policy` and a recovery projection are advertised, use its owner-computed disposition and bounded next action instead of the legacy stop-on-failed rule above. A proven no-generation failure may switch within an approved candidate set without repeated approval. An unknown submit must not be resent; a generated image must be downloaded/reviewed, even if its composition fails. Keep hard dimensions/ratio semantics and all references/masks when changing channels. Do not infer equivalent 2k/4k canvases across models.

The additive local implementation exposes recovery inspection through `inspect` with the returned `egr_...` reference in `run_id`; use this only when installed discovery documents it. It does not require the CLI. If background takeover or automatic provider lookup is unavailable, report that concrete limitation and use bounded foreground/snapshot behavior rather than claiming a worker is still running. Unknown costs remain unknown; an existing bounded user authorization to continue covers the same workload without another confirmation.

On success, consume the native `ResourceLink` attached to the MCP result
immediately. It is the original artifact delivery path; an optional preview is
only for quick visual inspection. Do not look for original image bytes in
structured content, and do not add image bytes or capability links to business
JSON, evidence, prompts, logs, or saved notes.

If the `ResourceLink` returns 404 or has expired, use `artifact.access` only
when that action is advertised for the active credentials and the caller is an
authorized operator. Then call `eikona.execute` once:

```json
{
  "action": "artifact.access",
  "args": {
    "artifact_uri": "<canonical artifact URI from the completed run>",
    "confirm": true
  }
}
```

Consume the newly attached `ResourceLink` and retry that download once. Do not
reuse an expired link, create a replacement run, or copy the capability URL
into a persistent result. If `artifact.access` is absent or denied, report that
an operator grant or compatible MCP host is required; do not retry, probe
actions, or create a replacement run.

If the MCP host omitted or discarded the `ResourceLink`, use the structured
`artifact_handle` fallback only when a released Eikona CLI and an already
available absolute, mode-0600 access-key file are local to the client. The key
may be the scoped generation-loop operator key; it is not unrestricted REST
authority:

```bash
eikona artifacts download eikona://artifact/<artifact_handle> \
  --endpoint <service-origin-without-/mcp> \
  --key-file <absolute-0600-key-file> \
  --to <local-path>
```

This client-side downloader issues its own grant and verifies length and SHA.
Do not read, print, copy, or request the key file. If the CLI or protected key
file is unavailable, report MCP-host download incompatibility; do not claim
that the image was downloaded.

## Local Skill assistance

The MCP remains usable even when this local Skill is absent. First inspect the
installed release with the no-write preview:

```bash
eikona setup --agent
```

Apply setup only when the installed release has its paired Skill bundle
available and the user grants local-write authority:

```bash
eikona setup --yes --agent
```

This installs the exact Skill bundle paired with the installed Eikona release.
Do not clone a repository, fetch arbitrary Skill code, or silently install
anything before that approval.
