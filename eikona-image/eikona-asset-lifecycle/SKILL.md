---
name: eikona-asset-lifecycle
description: Use when capturing temporary or externally generated PNG/JPEG/WebP images into Eikona, deciding project versus global asset scope, repairing provenance, explicitly promoting selected run artifacts into Visual Library, issuing path-free download grants, or integrating project, artifact-import, library, and OpenAPI service endpoints. Trigger for Codex/imagegen temporary files, durable asset management, DAM-like reuse, artifact persistence, asset API design, and long-term Eikona asset curation.
---

# Eikona Asset Lifecycle

Own the transition from temporary image bytes to durable evidence, curated reuse, and safe delivery. Keep generation evidence and long-term library membership separate.

## Decision Tree

1. If the image was generated through Eikona, start from its existing run artifact. Do not import it again.
2. If Codex, imagegen, a designer, or another tool produced a local PNG/JPEG/WebP, capture it with `eikona artifacts import` before the temporary file is lost.
3. Choose `project` scope for one registered project and `global` only for assets authorized for cross-project reuse.
4. Keep every captured image in `library_state=not_imported` until a human or owning workflow explicitly saves it.
5. Use a download grant for network delivery. Never return or copy an absolute runstore path.

## Capture External Images

Preserve prompt, model, and source tool whenever available:

```bash
eikona artifacts import ./icon.png \
  --scope project \
  --prompt "small product icon" \
  --model openai:gpt-image-2 \
  --source-tool codex-imagegen \
  --json
```

Use `--scope global` only when the asset may be reused outside the current project. Missing prompt, model, or source-tool metadata must remain `provenance_state=incomplete`; do not infer it.

Capture accepts valid PNG, JPEG, or WebP images up to 32 MiB. It creates a succeeded synthetic import run, copies bytes under `runs/<run_id>/outputs/`, and writes normal artifact, event, trace, result, and import evidence.

## Curate Long-Term Assets

Inspect the path-free handle and promote only selected artifacts:

```bash
eikona assets handoff <artifact_handle> --audience agent --agent
eikona library save eikona://artifact/<artifact_handle> \
  --collection generated \
  --permission owned \
  --json
```

Treat permission and provenance as separate gates. Owned assets with incomplete provenance may be viewed and repaired, but must not enter automatic workflow selection.

Do not use `library save` as a substitute for capture: the run artifact is the immutable source evidence; the Visual Library item is the curated reuse projection.

## Use the Service API

- Discover the canonical contract from authenticated `GET /api/v1/openapi.yaml`.
- Upload bytes with admin/operator `POST /api/v1/artifact-imports` using `multipart/form-data`.
- Use JSON `source_path` only as admin and only under a configured `--allow-import-root`.
- Send `Idempotency-Key` on every REST capture. Exact retries return the original run; changed content returns `IDEMPOTENCY_CONFLICT`.
- Read path-free instance and project projections from `/api/v1/instance` and `/api/v1/projects`.
- Restrict project registration and root repair with `--allow-project-root`.
- Create a short-lived grant at `POST /api/v1/artifacts/{handle}/download-grants`; download through the returned `/api/v1/downloads/{grant}` URL.

Read [references/asset-lifecycle-contract.md](references/asset-lifecycle-contract.md) when implementing or reviewing CLI/API behavior.

## Routing

- Use `eikona-product-asset-director` for page context, creative direction, candidate review, and repository apply.
- Use `eikona-file-prompt-workflow` for prompt libraries and runbooks.
- Use `yeisme-eikona-cli-runtime` for Go implementation, CLI output contracts, provider behavior, runstore, or tests.
- Use `eikona-gateway-bootstrap` when provider credentials or model routing are not ready.

## Boundaries

- Never write provider output directly into Visual Library or project files.
- Never bypass runstore, hand-edit evidence, or invent provenance.
- Never expose absolute paths, credentials, raw provider payloads, or signed URLs as durable identifiers.
- Never auto-promote, auto-accept, or widen project assets to global scope.
- Keep the recommended model spelling `openai:gpt-image-2`.

## Verification

For skill and documentation changes:

```bash
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" .agents/skills/eikona-asset-lifecycle
openspec validate --all
```

For runtime or API implementation changes, also run focused tests followed by `go test ./... -timeout 180s`, `task lint`, and `task fmt-check`.
