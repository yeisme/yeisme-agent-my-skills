---
name: yeisme-hermes-communication-routing
description: Use when designing, reviewing, documenting, or operating Yeisme communication delivery through Hermes provider-neutral events, commands, approval requests, artifact handoffs, and redacted evidence across Telegram, Feishu/Lark, Slack, Discord, email, or future chat providers.
---

# Yeisme Hermes Communication Routing

Use this skill when a Yeisme project needs chat or collaboration delivery and the request is not limited to one provider, or when the provider is Slack, Discord, email, or another future channel without a dedicated skill.

## Boundary

- Hermes owns provider SDKs, webhook or polling receivers, payload parsing, rendering, identity mapping, conversation state, retries, notification policy, and token handling.
- Ordinary domain projects emit provider-neutral commands and events. They must not import chat provider SDKs, parse provider payloads, render provider-specific cards/messages, or persist provider credentials.
- Oh My Hermes may select profiles, route provider-neutral events, generate operator guidance, and declare MCP Gateway bindings. It is not a chat bot implementation.

## Workflow

1. Classify the communication intent: notification, command, approval, artifact handoff, run status, or human escalation.
2. Express the payload as provider-neutral data: actor, target, intent, summary, correlation ID, action links, evidence references, and redacted metadata.
3. Route through Hermes directly, or through an MCP Gateway route that delegates to Hermes.
4. Keep credentials in user-level local config, a user-level secret store, Hermes-owned local secret store, or deployment secret manager.
5. Record only redacted evidence: source type, delivery request ID, status, correlation ID, and evidence references.

## Validation

- Confirm no domain project embeds Telegram, Feishu/Lark, Slack, Discord, email, or other provider SDK behavior.
- Confirm logs, run evidence, fixtures, docs, screenshots, and generated assets do not contain tokens, Authorization headers, raw prompts, hidden prompts, private tool arguments, provider payloads, or full chain-of-thought.
- Confirm OMH profile work uses dry-run/diff before approved apply or skill sync.

## Command Examples

```bash
omh diff --profile personal --json
omh apply --profile personal --dry-run --json
omh tools guide --json
```
