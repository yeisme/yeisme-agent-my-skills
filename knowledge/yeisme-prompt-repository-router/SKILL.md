---
name: yeisme-prompt-repository-router
description: Use when authoring, changing, reviewing, or integrating Yeisme prompt solution content, promptrepo public contracts, Template Registry storage/distribution, template addresses, safe inspect/render/preview, or domain-owner prompt consumption, and the canonical owner or handoff must be selected.
---

# Yeisme Prompt Repository Router

Route prompt-template work to the narrowest canonical owner. This skill does not execute prompts, call providers, or create a second prompt catalog.

## Owner Map

| Work | Canonical owner |
| --- | --- |
| English Agent template text, Chinese review translations, examples, taxonomy, tags, locale display text, rights, maturity | `data/yeisme-prompt-templates` |
| Public Go contracts, exact `promptrepo://` refs, template address, inspect/validate/render/preview DTOs, embedded engine, source adapters, conformance fixtures | `shared/promptrepo` |
| Team Registry service, immutable releases, CAS/object copies, Git mirror, install/audit state, backup and recovery | `backend-server/template-registry` |
| Approved generic agent consumption: local sessions, source import/analysis adapters, confirmation, prompt-package compilation/export, CLI and embedded stdio MCP | `backend-server/template-registry` |
| Domain compatibility, stage/accept/promote, provider execution, cost, evidence, and asset lifecycle | The consuming owner such as Sonora, Eikona, Scaena, Auctra, or Pinax |

## Routing Workflow

1. Classify the requested change as `content`, `public-contract`, `distribution-control-plane`, or `domain-consumption`.
2. Preserve one canonical writer. Cross-owner work uses refs, digests, snapshots, receipts, and typed handoffs rather than copying private state.
3. Keep inspect, validate, render, preview, plan, and dry-run provider-free. Prompt bodies must not enter ordinary structured output, events, logs, traces, or test evidence.
4. Keep `en` as the only locale registered for new Agent-compilable templates and contracts. Put the Chinese human review translation in `docs/template-zh-CN.md`; it does not compile. Machine IDs, schema fields, tags, capabilities, rights, maturity, and URI syntax remain stable English.
5. Build structured catalog and release metadata through Template Registry commands. Human-authored prompt prose and guides may be edited in the content owner.
6. Route actual execution and acceptance to the consuming domain owner; shared repository layers never infer provider permissions, cost approval, or production acceptance.
7. For the approved Registry consumption workflow, use `template-registry-agent-operator` when installed. Compilation remains provider-free; only explicit source analysis may call a configured analysis backend. Private session content uses explicit resources/exports, never ordinary output or evidence.
8. For new solution authoring, use `template-registry-template-author` when installed. It creates the English template and Chinese review document, then generates all structured metadata through Template Registry CLI.

## Required Handoff

Report the selected owner, artifact, input refs, expected digest/revision, provider-call policy, persistence boundary, validation command, and next owner. When a stable ref or schema changes, apply `yeisme-evolutionary-change-policy`.

## References

- Root owner map: `docs/architecture/prompt-repository-federation.md`.
- Content rules: `data/yeisme-prompt-templates/AGENTS.md`.
- Public SDK rules: `shared/promptrepo/AGENTS.md`.
- Registry service rules: `backend-server/template-registry/AGENTS.md`.

## Validation

Run only the commands for the affected owner:

```bash
(cd backend-server/template-registry && go run ./cmd/template-registry catalog build --repository ../../data/yeisme-prompt-templates --json)
(cd backend-server/template-registry && go run ./cmd/template-registry catalog validate --repository ../../data/yeisme-prompt-templates --json)
(cd shared/promptrepo && go test ./...)
(cd backend-server/template-registry && task test:integration)
(cd data/yeisme-prompt-templates && openspec validate --all --strict --no-interactive)
```
