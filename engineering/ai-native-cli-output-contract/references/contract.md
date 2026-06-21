# AI Native CLI Output Contract Reference

Load this reference when designing a new CLI output schema, writing migration notes, or reviewing compatibility.

## Public Modes

| Mode | Audience | Transport | Primary constraint |
| --- | --- | --- | --- |
| `summary` | human operator | default stdout | short, scannable, one main next command |
| `agent` | LLM/shell glue | `--agent` stdout | low-token stable key=value |
| `json` | scripts/CI/SDK | `--json` stdout | one valid envelope object |
| `events` | long-running automation | `--events` NDJSON stdout | ordered parseable events |
| `explain` | human decision review | `--explain` stdout | conclusion, evidence, confidence |

Existing flags such as `--format ai` can remain as aliases, but new docs should prefer explicit `--agent`.

## Envelope Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AI CLI Output Envelope",
  "type": "object",
  "required": ["spec_version", "mode", "command", "status"],
  "properties": {
    "spec_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+(\\.[0-9]+)?$"
    },
    "mode": {
      "enum": ["summary", "agent", "json", "events", "explain"]
    },
    "command": {
      "type": "string",
      "minLength": 1,
      "pattern": "^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)+$"
    },
    "status": {
      "enum": ["success", "partial", "failed"]
    },
    "summary": {
      "type": "string"
    },
    "facts": {
      "type": "object",
      "additionalProperties": true
    },
    "actions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "command"],
        "properties": {
          "name": { "type": "string", "minLength": 1 },
          "command": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      }
    },
    "evidence": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "data": {
      "type": "object",
      "additionalProperties": true
    },
    "error": {
      "type": "object",
      "required": ["code", "message"],
      "properties": {
        "code": { "type": "string", "minLength": 1 },
        "message": { "type": "string", "minLength": 1 },
        "path": { "type": "string" },
        "suggestion": { "type": "string" },
        "retryable": { "type": "boolean" },
        "details": { "type": "object", "additionalProperties": true }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

Command-specific schemas should validate `data`. Do not add command-specific fields at the top level unless they are promoted to the shared envelope.

## Agent Key Naming

Required:

```text
spec_version=1.0
mode=agent
command=task.get
status=success
```

Recommended prefixes:

- `fact.<name>` for key facts.
- `action.<name>` for runnable next commands.
- `evidence.<name>` for paths, IDs, or metrics.
- `error.<field>` for failed commands.
- `metric.<name>` for numeric operational values.

Rules:

- Keys use `[a-zA-Z0-9_.-]+`.
- Values should be single line.
- Use stable enum values, IDs, and paths rather than localized prose.
- Keep nested or large payloads out of agent mode.

## Event Types

Minimum event sequence:

```json
{"type":"start","spec_version":"1.0","command":"task.get","seq":1}
{"type":"fact","key":"state","value":"done","seq":2}
{"type":"end","status":"success","seq":3}
```

Common event types:

- `start`
- `progress`
- `fact`
- `finding`
- `action`
- `evidence`
- `warning`
- `error`
- `end`

For long-running tasks, include `run_id` or `operation_id` when available. If failure happens after the stream starts, emit an `error` event as the final line and return a non-zero exit code.

## Compatibility Matrix

| Change | Version |
| --- | --- |
| Add optional field | minor |
| Add output mode | minor |
| Add command-specific `data` property | minor |
| Rename field | major |
| Delete field | major |
| Change enum semantics | major |
| Optional field becomes required | major |
| Documentation or examples only | patch |

Parser rule: accept unknown optional fields in command-specific `data`; reject unknown shared-envelope top-level fields unless the schema explicitly allows an extension namespace.

Publisher rule: support at least two minor versions before removing old behavior.

## Security And Redaction

Never print:

- API keys, bearer tokens, cookies, session IDs, private keys, passwords, or authorization headers.
- Raw prompts that may include user secrets.
- Full provider requests or responses before redaction.
- `.env` values, user-level config secret values, secret-store contents, or local credential file contents.

Allowed:

- Last 4 characters of an ID when useful.
- Hashes or stable redacted handles.
- Relative evidence paths after checking they do not include secrets.
- Credential source metadata such as env var names, configured status, keychain refs, or redacted digests.

Machine output is not exempt from redaction. Sidecar files, traces, test snapshots, and audit logs must follow the same rule.

Local CLI auth/config commands may write real credentials to user-level local config or a user-level secret store, but they must not document shell credential scripts as the persistence path and must not write real credentials to repository project assets.

For sensitive commands, prefer one of:

- `--no-output`
- `--output none`
- `--sidecar-only <path>`

Use whichever naming pattern matches the owning CLI. The important invariant is that sensitive values are not forced through stdout just because automation requested structured output.

## Migration Template

Use this sequence when changing an established CLI:

1. Freeze current machine fields and add golden tests.
2. Introduce `--json` v1 envelope while preserving legacy output.
3. Add `--agent`, `--events`, and `--explain`.
4. Dual-write sidecar/evidence if the command has a run store.
5. Announce compatibility window and script migration command examples.
6. Switch default to human `summary` only after explicit JSON paths are stable.
7. Keep `--legacy-output` or an environment fallback for the agreed window.

Rollback should restore the old default without breaking explicit `--json` and `--agent`.

## Examples

Default:

```text
状态：任务 T123 已完成

重点：
- state: done
- duration: 42s

推荐下一步：
app task logs T123
```

Agent:

```text
spec_version=1.0
mode=agent
command=task.get
status=success
fact.id=T123
fact.state=done
action.logs="app task logs T123"
```

JSON:

```json
{
  "spec_version": "1.0",
  "mode": "json",
  "command": "task.get",
  "status": "success",
  "summary": "任务 T123 已完成",
  "facts": {
    "id": "T123",
    "state": "done"
  },
  "actions": [
    {
      "name": "logs",
      "command": "app task logs T123"
    }
  ]
}
```

Events:

```json
{"type":"start","spec_version":"1.0","command":"task.get","seq":1}
{"type":"fact","key":"state","value":"done","seq":2}
{"type":"end","status":"success","seq":3}
```

Explain:

```text
结论：允许执行
证据：error_rate=0.2% < 1%
置信度：0.93
推荐下一步：
app deploy apply svc-a
```
