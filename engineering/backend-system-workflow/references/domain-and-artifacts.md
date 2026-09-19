# Domain model and artifact records

For agent orchestration systems, prefer explicit product objects:

- `Run`
- `Task`
- `Agent`
- `Step`
- `Approval`
- `Artifact`
- `TraceEvent`
- `PolicyDecision`
- `ToolCall`
- `CostEvent`

Critical entities should normally include:

- `id`
- `run_id` or clear owner scope
- `status`
- `created_at`
- `updated_at`
- `version`
- `metadata`
- `last_error`

Do not represent important lifecycle state as arbitrary strings without transition rules. Do not let direct DB field updates be the state machine.

## Artifact records

Do not leave product artifacts as anonymous local files such as `/tmp/result.md`.

Artifact records should include:

- id
- run_id
- task_id when applicable
- type
- path or uri
- mime_type
- size
- checksum
- status
- created_by
- created_at
- evidence_refs

Storage may be local disk, S3, MinIO, database blob, or another backend, but the product layer should use artifact records, not raw paths.
