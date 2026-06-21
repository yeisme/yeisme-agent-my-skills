---
name: yeisme-feishu-hermes-integration
description: Use when designing, reviewing, documenting, or operating Feishu/Lark collaboration integration for Yeisme projects through Hermes provider-neutral commands, events, approval-style interactions, card-message boundaries, tenant/user mapping, credential safety, and redacted evidence.
---

# Yeisme Feishu/Lark Hermes Integration

Use this skill when work mentions Feishu, Lark, chat delivery, collaboration notifications, approval messages, or agent handoffs that should reach Feishu users.

## Boundary

- Hermes owns Feishu/Lark provider SDKs, app event receivers, webhook parsing, card/message rendering, retries, tenant/user mapping, conversation state, and token handling.
- Ordinary Yeisme domain projects emit provider-neutral commands and events. They must not import Feishu SDKs, parse Feishu payloads, render Feishu cards directly, or persist Feishu credentials.
- Oh My Hermes may select profiles, route provider-neutral events, generate local operator guidance, and declare MCP Gateway bindings. It is not the Feishu bot implementation.

## Workflow

1. Identify the domain event, command, approval request, or artifact handoff that needs Feishu/Lark delivery.
2. Keep the payload provider-neutral: actor, target, intent, summary, action links, evidence references, and redacted metadata.
3. Route through Hermes or an MCP Gateway route that delegates to Hermes.
4. Store credentials only in user-level local config, user-level secret store, or Hermes-owned local secret store.
5. Produce redacted evidence with configured source type, delivery status, tenant/user reference type, and evidence references, never raw provider payloads.

## Validation

- Confirm no domain project imports Feishu/Lark SDKs or embeds provider-specific webhook payloads.
- Confirm logs, run evidence, fixtures, docs, and screenshots do not contain tokens, Authorization headers, raw prompts, hidden prompts, private tool arguments, provider payloads, or full chain-of-thought.
- For OMH profile work, prefer dry-run/diff commands before applying profile changes.

## Command Examples

```bash
omh diff --profile personal --json
omh apply --profile personal --yes --json
omh tools doctor --json
```
