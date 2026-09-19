---
name: radar-operator
description: "Use when an agent needs to read or operate short-drama opportunity intelligence through the short-drama-radar CLI: Morning Edition, market brief, watches, reader state, Chinese reading list, canary, schedule, feedback, decision packs, or Auctra/Scaena assignment handoff; or when the user mentions radar, 短剧雷达, or Morning Edition."
---

# Radar operator

short-drama-radar (`radar`) is a local CLI product for personal short-drama opportunity intelligence. Operate it CLI-first: run `radar` commands, parse the stdout envelope, and read user-level run receipts. Never connect to its SQLite database, load internal modules, keep a second Profile/Edition copy, or reach for a service surface.

## Reach the CLI first

```bash
command -v radar
radar doctor --json
```

If no global `radar` exists, use the project entry:

```bash
cd cli/short-drama-radar && bun run src/cli.ts doctor --json
```

`doctor`'s `actions[].command` is the only source of suggested next-step commands. Do not guess recovery commands. External logins and account configuration belong to the user: never install credentials, export cookies, or start a browser login.

## Read flow (zero writes)

Default read-only sequence, `--json` first:

```bash
radar doctor --json
radar runs --json
radar edition show latest --json
radar market brief show --json
radar market reading list --json
radar market watch list --json
```

Envelope facts (spec_version=1.0): rely only on the stable fields `spec_version, mode, command, status, summary, facts, actions, evidence, confidence, data, error`. Relay `status`, `error.code`, and `facts` verbatim; do not judge success from the human summary, do not invent nested fields, and do not treat stdout error text as JSON data. On a nonzero exit, keep the minimal error summary and stop auto-retrying. `--agent` prints compact stable key=value lines; `--explain` is a redacted review summary, not full reasoning.

When there is no edition or no data yet, relay `status`/`error.code`/`facts`/`actions` as-is and suggest the real commands from the receipts (for example `radar profile create --name main`, then `radar run --json`). Do not lower thresholds on your own, do not treat `degraded` as `ready`, and do not pass an old run off as today's data.

## Write guardrails

- Reads above are zero-write. Any state-changing command runs only after the user confirms the exact command line.
- Confirmed-write family: `feedback add`, `opportunity review`, `market watch add/pause/resume/remove`, `market reader mark/unread`, `market translation add`, `profile create/set/activate`, `edition build`, `run`, `market config set`, `market source set`, `schedule install`. Quote the full command, get confirmation, then execute once.
- Repeated writes reuse the same business ref and idempotency key. On `state_conflict`, re-read the current revision (`profile show`, `signal show`) and redo; never force an overwrite.
- Empty or thin output is `do_not_shoot`: report the limitations verbatim and let the user decide. Never lower `--minimum-fit`/`--minimum-confidence` or pad the board to fake coverage.
- Live observation needs explicit consent: `radar market observe --source hongguo|reelshort-ja|reelshort-ko --mode verify-sample|production --confirm-live`. Use `--fixture` for offline path tests. Never bypass risk control, captchas, or platform checks, and never automate login.
- The Profile source of truth is the radar CLI only. Never hand-edit radar config files, databases, run receipts, profile revisions, or structured exports.
- `radar schedule session-plan` output is read-only prompts: they must not run `radar collect`, `radar run`, or `market observe --confirm-live`.

## Boundaries

- Do not read radar SQLite, audit, or internal state files; consume CLI output and CLI-generated exports only.
- Hermes and DSH panes are consumers of CLI projections: read-only display plus user-confirmed feedback commands.
- Radar has no MCP surface (removed 2026-09-15). Never suggest connecting to a radar MCP server, HTTP API, or resident service; the CLI is the only agent interface.
- Show source status, confidence, degraded flags, evidence refs, and the next command so the user can tell "nothing changed" from "nothing collected". A blocked or unavailable channel is reported with its recovery command, never silently swapped for an undeclared backend.

## Command reference

Verified read commands:

```bash
radar health [window-days] --json
radar canary report [window-days] --json
radar market reader show --json
radar market source list --json
radar market source gaps --json
radar market signal show --signal <ref> --json
radar market analyze --json
radar schedule show --backend auto --json
radar schedule session-plan --runtime grok|claude|both --json
radar assignment show latest --json
radar decision list --json
```

Confirmed-write commands:

```bash
radar run --json
radar edition build [date] --limit <1-50>
radar feedback add --opportunity <ref> --kind saved|used|dismissed|not_relevant|too_risky|already_seen [--idempotency-key <key>]
radar opportunity review --opportunity <ref> --decision accept|reject|needs_evidence
radar market watch add --kind topic|work|platform|market --target <ref>
radar market watch pause|resume|remove --watch <ref>
radar market reader mark|unread --signal <ref> --signal-revision <n>
radar profile create --name <name>
radar profile set --minimum-fit <n>|--minimum-confidence <n>|--risk-tolerance <n>|--genre <tag:weight>|--blocked-topic <topic>
radar assignment create --edition <ref> [--opportunity <ref>] [--key <key>]
radar market observe --source hongguo|reelshort-ja|reelshort-ko --mode verify-sample|production --confirm-live
```

`decision` write subcommands (`create`, `evidence add`, `candidate add`, `experiment lock`, and friends) follow the same confirm-then-execute rule; read `radar decision` help output for their full flags before proposing one.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| `command -v radar` empty | Use `cd cli/short-drama-radar && bun run src/cli.ts <command> --json` | Ask the user; do not install or log in yourself |
| `doctor` reports problems | Run its `actions[0].command` | Do not guess recovery commands |
| Edition `empty`/`absent` | Relay limitations; suggest the receipt's command (`radar run`, profile create) | Do not lower thresholds or pad entries |
| `degraded` sources | Present results with the degraded flag and "lower bound" caveat | Do not label degraded as ready |
| `state_conflict` on a write | Re-read the current revision, retry with the same business ref | Do not force an overwrite |
| Unknown command or flag | Recheck this surface and the CLI's own help | Do not invent flags or backends |
| Channel `blocked`/`unavailable` | Show status plus recovery command verbatim | Do not claim coverage or switch backends |

## Validation

- Every command proposed to the user is a real `radar` command shown above or taken from a receipt's `actions[].command`.
- Read answers relay `status`, `error.code`, and `facts` verbatim from the `--json` envelope.
- Every write was quoted to the user, confirmed, and executed once with stable refs and idempotency keys.
- No radar SQLite, audit file, MCP connection, credential, or cookie was touched.
