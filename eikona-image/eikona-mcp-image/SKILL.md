---
name: eikona-mcp-image
description: "Use when explicit Eikona or eikona-lan MCP image generation, editing, artifact delivery, or download recovery is requested. Prefer this direct Eikona flow over generic imagegen when Eikona is named or configured."
---

# Eikona MCP image fast path

Use the configured Eikona MCP as the primary path when the user explicitly
mentions Eikona or `eikona-lan`. Do not switch to a generic image-generation
skill unless the user explicitly asks for that fallback or Eikona returns a
typed blocker that requires it.

## Ordinary generation and editing

Call `eikona.execute` directly. Do not begin an ordinary request with
`eikona.search`, model-catalog scans, provider doctor, or `resources/read`.
Use `action: "generate"` for a new image and `action: "edit"` for a supplied
image, with a stable `idempotency_key` and the user intent. Preserve an
explicit supported Eikona model selection, including Grok or Midjourney. When
the user does not specify a model, default to `openai/gpt-5.4-image-2`. Do not
select test-only model identifiers.

Keep the idempotency key as submission evidence. After a response returns a
`run_id`, use `eikona.execute` with `action: "wait"` (or `status`/`inspect`
when the typed response directs it) against that same run until terminal. If
the submit transport outcome is lost before any `run_id` is received, report an
unknown outcome and stop: do not resubmit or claim that the idempotency key
reconciled the run. Only inspect readiness, a model, or a resource after a
typed Eikona error says that exact information is needed.

## Artifact delivery and download recovery

On success, consume the native `ResourceLink` attached to the MCP result
immediately. It is the original artifact delivery path; an optional preview is
only for quick visual inspection. Do not look for original image bytes in
structured content, and do not add image bytes or capability links to business
JSON, evidence, prompts, logs, or saved notes.

If the `ResourceLink` returns 404 or has expired, call `eikona.execute` once:

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
into a persistent result.

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

The MCP remains usable even when this local Skill is absent. Source, profile,
and release-bundle wiring are implemented, but current public releases do not
contain this new Skill until an external release bundle is published. Do not
claim that setup can install it before that release exists. A user may inspect
their installed release with the no-write preview:

```bash
eikona setup --agent
```

After a release that includes this Skill is published, run the following only
after the user grants local-write authority:

```bash
eikona setup --yes --agent
```

This installs the exact Skill bundle paired with the installed Eikona release.
Do not clone a repository, fetch arbitrary Skill code, or silently install
anything before that approval.
