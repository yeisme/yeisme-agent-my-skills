---
name: sonora-agent-router
description: Use when an agent needs to inspect, plan, render, review, or route Sonora voice and audio-asset workflows with the smallest safe CLI command and low-token output.
---

# Sonora Agent Router

## Default Output

Use `--agent` for readiness checks, provider status, reference discovery, planning receipts, render receipts, review decisions, and ordinary local writes. Consume `action.*`, `fact.*`, `data.*`, and `evidence.*`; never parse human cards or `.sonora` private state.

Use `--json` only when the task needs full nested capabilities, strategy comparisons, schema validation, or detailed structured failure data. Return to `--agent` for follow-up reads when scalar output is enough.

## Routing

| Intent | Command |
| --- | --- |
| Workspace readiness | `sonora doctor --agent` |
| Initialize a project | `sonora init --project . --agent` |
| Provider status | `sonora provider list --agent` |
| Full provider capability matrix | `sonora tts providers list --json` |
| Voice models for one provider | `sonora tts voices list --provider <provider-id> --agent` |
| Local fixture flow | `sonora bridge scaena plan --graph <production-graph-ref> --agent` |
| Render or review receipt | `sonora render plan --plan <language-plan-ref> --voice-pack fixture --confirm --agent` |
| Detailed strategy comparison | `sonora audio strategy compare --plan <language-plan-ref> --json` |

## Remote Safety

1. Inspect `sonora provider doctor --provider <provider-id> --agent` before a remote action.
2. Estimate cost with `sonora tts estimate --plan <language-plan-ref> --provider <provider-id> --voice-model <voice-model-ref> --max-cost-usd <limit> --agent`.
3. Require explicit user authorization before a command with `--confirm-external-call`.
4. Voice creation or real-person reference audio also requires `--permission licensed` and redacted permission evidence.

## Tab Completion

Ask the user to install a matching shell script with `sonora completion <shell>`. The CLI supplies local candidates for provider IDs, catalog voice-model refs and project-local workflow refs; completion never performs a provider network call.

## Validation

Use `sonora <command> --agent` for low-token output checks and `sonora <command> --json` when validating complete payloads. Do not expose credentials, audio bytes, raw provider payloads, private tool arguments, or hidden reasoning.
