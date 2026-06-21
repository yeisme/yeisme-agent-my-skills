---
name: yeisme-telegram-hermes-integration
description: Use when designing, reviewing, documenting, or operating Telegram integration for Yeisme projects through Hermes provider-neutral commands, events, Bot API boundaries, chat/thread identity, credential safety, and redacted evidence.
---

# Yeisme Telegram Hermes Integration

Use this skill when work mentions Telegram, Telegram Bot API, chat delivery, command routing, approval messages, artifact handoffs, or run notifications that should reach Telegram users.

## Boundary

- Hermes owns Telegram Bot API calls, webhook or polling receivers, update parsing, message rendering, retries, chat/thread identity mapping, conversation state, and bot token handling.
- Ordinary Yeisme domain projects emit provider-neutral commands and events. They must not import Telegram SDKs, parse Telegram updates, render Telegram messages directly, or persist Telegram credentials.
- Oh My Hermes may select profiles, route provider-neutral events, generate local operator guidance, and declare MCP Gateway bindings. It is not the Telegram bot implementation.

## Workflow

1. Identify the domain event or command that needs Telegram delivery.
2. Keep the payload provider-neutral: actor, target, intent, summary, action links, evidence references, correlation ID, and redacted metadata.
3. Route through Hermes or an MCP Gateway route that delegates to Hermes.
4. Store bot tokens only in user-level local config, user-level secret store, Hermes-owned local secret store, or deployment secret manager.
5. Produce redacted evidence with configured source type, delivery status, chat/thread reference type, and evidence references, never raw Telegram updates or message payloads.

## Validation

- Confirm no domain project imports Telegram SDKs or embeds Telegram webhook/polling payloads.
- Confirm logs, run evidence, fixtures, docs, and screenshots do not contain bot tokens, Authorization headers, raw prompts, hidden prompts, private tool arguments, provider payloads, or full chain-of-thought.
- For OMH profile work, prefer dry-run/diff commands before applying profile changes.

## Command Examples

```bash
omh diff --profile personal --json
omh apply --profile personal --yes --json
omh tools guide --json
```
