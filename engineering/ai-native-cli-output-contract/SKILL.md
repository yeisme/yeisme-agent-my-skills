---
name: ai-native-cli-output-contract
description: Use when designing, implementing, testing, or reviewing CLI output for Yeisme apps, including default human summaries, --agent key=value output, --json envelopes, --events NDJSON streams, --explain reports, stdout/stderr separation, redaction, schema versioning, and contract tests.
---

# AI Native CLI Output Contract

Use this skill whenever a command-line interface is created or changed. It enforces one shared projection rendered through multiple modes instead of letting each command hand-roll unrelated text, JSON, and agent output.

## Contract

All CLI output must follow "one core, multiple renderers":

- `summary`: default human output; concise Chinese text for operators.
- `--agent`: stable low-token key=value lines for agents and shell glue.
- `--json`: strict machine envelope for scripts, CI, SDKs, and schema validation.
- `--events`: NDJSON event stream for long-running automation.
- `--explain`: Chinese reviewable reasoning summary with conclusion, evidence, confidence, risk, and next action.

Every mode must come from the same command projection. Do not parse localized human text to build JSON, TUI state, tests, or agent output.

Structured project assets must be CLI-authored. For config, profile/policy, run receipt, event log, review decision, sync mapping, export manifest, OpenSpec task evidence, or any machine-readable metadata, design commands or application services that create and update the files. Agents should invoke commands such as `app project set`, `app profile set`, `app run start`, `app event append`, or `openspec new change`; they should not hand-write JSON, YAML, JSONL, or Markdown metadata files. User prose, note bodies, drafts, and ordinary content files are the exception.

For Pi, OMP, Cohors, Auctra, pinax, GitPulse, skillctl, and similar agent tools, user-visible plans, explanations, reviews, handoffs, run summaries, errors, and `--explain` reports default to Chinese. Machine protocol fields, schema keys, enum values, command names, flags, log keys, JSON envelope fields, `--agent` keys, and third-party API fields remain stable English or existing names.

Never output or persist full chain-of-thought, raw prompts, hidden system prompts, unredacted provider payloads, private tool arguments, or model-internal reasoning in stdout, stderr, traces, event logs, run receipts, snapshots, fixtures, golden files, docs, or structured assets. When explanation is needed, provide a redacted Chinese summary: conclusion, key evidence, risk, tradeoff, next step, and evidence references.

When designing a new schema, migration, or test matrix, read `references/contract.md`.

## Required Envelope

`--json` must emit one valid JSON object on stdout with at least:

```json
{
  "spec_version": "1.0",
  "mode": "json",
  "command": "domain.action",
  "status": "success"
}
```

Stable top-level fields are:

- `spec_version`: semantic output contract version.
- `mode`: `summary`, `agent`, `json`, `events`, or `explain`.
- `command`: normalized command name such as `deploy.status`.
- `status`: `success`, `partial`, or `failed`.
- `summary`: one-sentence human result when useful.
- `facts`: small key fact object for automation.
- `actions`: next commands as `{ "name": "...", "command": "..." }`.
- `evidence`: short evidence strings, object IDs, or paths.
- `confidence`: number from 0 to 1 when the command makes a judgment.
- `data`: full machine payload.
- `error`: standardized error object on failure.

Use command-specific schema under `data`; keep the envelope stable.

## Mode Rules

Default output is for humans:

- Prefer `状态`, `重点`, optional `风险`, optional `证据`, and one `推荐下一步`.
- Default output must not be a large JSON dump.
- Keep it short enough to scan; fold detail into `--json`, `--verbose`, or a detail command.
- User-visible text is Chinese unless it is a command, flag, path, schema key, protocol field, model id, provider id, or third-party name.

`--agent` is for low-token parsing:

- Emit one `key=value` fact per line.
- Required lines: `spec_version`, `mode=agent`, `command`, `status`.
- Use stable ASCII keys with dots for hierarchy, such as `fact.state=done`.
- Quote values only when they contain spaces or shell-sensitive characters.
- Put runnable next steps in `action.<name>=...`.
- Do not include ANSI, tables, prose paragraphs, debug dumps, localized section labels, raw prompts, provider payloads, or reasoning chains.

`--json` is for strict machines:

- stdout must contain JSON only. No ANSI, progress text, logs, suggestions, banners, or trailing prose.
- Use the shared envelope and validate command-specific `data`.
- On failure, still emit a valid envelope with `status=failed` and `error`.
- Add optional fields in minor versions; remove or rename fields only in major versions.

`--events` is for streams:

- Emit newline-delimited JSON, one event object per line.
- Start with `{"type":"start",...}` and end with `{"type":"end",...}` or `{"type":"error",...}`.
- Include monotonically increasing `seq` when ordering matters.
- Keep logs and progress decoration out of stdout; write diagnostics to stderr.

`--explain` is for decisions:

- Use Chinese `结论`, `证据`, `置信度`, and optional `风险`, `取舍`, `推荐下一步`.
- Every conclusion must have evidence or be explicitly marked as a hypothesis.
- Do not expose full chain-of-thought, raw prompts, hidden system prompts, secrets, credentials, cookies, tokens, private tool arguments, or unredacted provider payloads.

Privacy controls are part of the contract:

- For commands likely to touch credentials, provide `--no-output`, `--output none`, or an equivalent sidecar-only path when the product surface supports it.
- Sidecar, trace, audit, and test snapshot output must use the same redaction policy as stdout.
- Reasoning summaries may be persisted only through CLI/service-authored structured evidence after redaction; never by direct agent-written metadata files.

## Implementation Workflow

1. Enter the owning subproject before editing CLI code, then use that subproject's `AGENTS.md` and domain skill.
2. Locate the command projection or create one. The projection owns status, facts, actions, evidence, confidence, data, and error.
3. Identify structured assets the command owns: config, profile, policy, receipt, event log, mapping, manifest, review decision, or OpenSpec evidence. Add `init`, `set`, `append`, `validate`, `doctor`, or `repair` commands instead of documenting direct file edits.
4. Implement renderers from the projection: human summary, agent, JSON, events, and explain.
5. Keep compatibility explicit:
   - new optional field: minor version
   - new output mode: minor version
   - renamed or deleted field: major version
   - optional field becoming required: major version
   - docs/examples only: patch version
6. Add tests close to the command:
   - `--json` parses as JSON and matches the envelope.
   - `--agent` has stable key=value lines and required keys.
   - `--events` is valid NDJSON with correct start/end order.
   - default output is not JSON and has one primary next command.
   - ANSI/progress/logs do not leak into machine stdout.
   - structured assets are created or changed through CLI/service commands, not direct agent-written JSON/YAML/JSONL/Markdown metadata files.
   - `--explain` is a Chinese reasoning summary with evidence references, not full chain-of-thought.
   - `--agent` remains stable key=value and does not include localized prose.
   - secrets are redacted in every mode and sidecar.
7. Update help text and docs with real user-runnable commands only. Do not mention local execution wrappers, shell aliases, or agent-only prefixes.

## Validation

Run the owning project's tests first. Then use the bundled validator when sample output is available:

```bash
python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode json < output.json
python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode agent < output.agent
python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode events < output.ndjson
```

For live commands, use real CLI examples:

```bash
app task get T123 --json | python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode json
app task get T123 --agent | python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode agent
app task watch T123 --events | python .skills/yeisme/engineering/ai-native-cli-output-contract/scripts/validate_cli_output.py --mode events
```

Also validate with the project-local parser, for example `jq`, Node, Go, or Python. The bundled validator is a guardrail, not the only test.

## Boundaries

- Do not force every CLI into MCP. MCP is a bridge or integration layer; ordinary CLI output stays flag-driven.
- Do not make direct file editing the primary workflow for structured metadata. If users or agents need to change config, profile, policy, events, receipts, mappings, review decisions, or manifests, add a CLI command such as `app config set`, `app event append`, or `app run start`.
- Do not switch an existing script-facing default from JSON to summary without a compatibility window, explicit flags, and migration notes.
- Do not put full schema descriptions into `--agent`; keep complex data in `--json` or MCP tool schemas.
- Do not rely on color for meaning. `NO_COLOR=1` and `--color never` must remain readable.
- Do not emit secrets, auth headers, provider tokens, raw prompts, hidden system prompts, cookies, full chain-of-thought, private tool arguments, model-internal reasoning, provider payloads, or full unredacted stack traces in any output mode.
