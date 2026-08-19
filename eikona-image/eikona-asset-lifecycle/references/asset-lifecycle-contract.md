# Asset Lifecycle Contract

## Lifecycle states

| Stage | Durable owner | Stable identity | Automatic reuse |
| --- | --- | --- | --- |
| Temporary external file | External tool or local filesystem | None | No |
| Captured run artifact | Eikona runstore | `eikona://artifact/<handle>` | No |
| Curated library item | Visual Library projection | Library entry plus source artifact | Only after permission and provenance gates |
| Delivered artifact | Short-lived download grant or explicit project apply | Stable artifact URI plus expiring grant | Not applicable |

## Operation contract

| Intent | CLI or REST entry | Required evidence |
| --- | --- | --- |
| Capture | `eikona artifacts import <path> --agent` | `run_id`, path-free artifact, scope, provenance, `not_imported` |
| Inspect | `eikona assets handoff <handle> --agent` | Stable handle, digest, MIME, dimensions, permission |
| Curate | `eikona library save eikona://artifact/<handle> ... --agent` | Explicit collection, permission, source artifact |
| Apply | `eikona assets apply <handle> --project ... --to ... --yes --agent` | Registered project, bounded destination, decision receipt |
| Deliver | `POST /api/v1/artifacts/{handle}/download-grants` | Actor, project scope, expiry, path-free URL |

`--agent` remains key-value and low token. `--json --compact` is the bounded script/CI envelope and `--json --full` the forensic envelope; during coexistence bare `--json` still means legacy full. Human output must explain that capture is not library promotion.

## REST authorization

| Operation | Minimum role | Path rule |
| --- | --- | --- |
| Multipart capture | operator | No server-side input path |
| `source_path` capture | admin | Must resolve below an allowed import root |
| Project reads | reader | Responses remain path-free |
| Project register/repair/archive | admin | Root must resolve below an allowed project root where applicable |
| Download grant | reader with matching project scope | Response contains only stable refs and expiring URL |

REST capture requires `Idempotency-Key`. Local CLI capture may omit it because the command is a single local operation.

## Canonical references

- Product guide: `docs/product/external-asset-capture.md`
- CLI guide: `docs/commands/artifacts.md`
- OpenAPI: `docs/interfaces/api/openapi.yaml`
- Main specs: `openspec/specs/external-artifact-capture/spec.md`, `openspec/specs/asset-library-catalog/spec.md`, and `openspec/specs/project-service-management/spec.md`
