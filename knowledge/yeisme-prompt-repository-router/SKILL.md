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
9. For requests to integrate templates with Skills, multimodal operations, reusable recipes, persistence, installation, or upstream/downstream owners, use `template-registry-integration-designer` when installed before entering the author or operator workflow.

## Required Handoff

Report the selected owner, artifact, input refs, expected digest/revision, provider-call policy, persistence boundary, validation command, and next owner. When a stable ref or schema changes, apply `yeisme-evolutionary-change-policy`.

## References

- Root owner map: `docs/architecture/prompt-repository-federation.md`.
- Content rules: `data/yeisme-prompt-templates/AGENTS.md`.
- Public SDK rules: `shared/promptrepo/AGENTS.md`.
- Registry service rules: `backend-server/template-registry/AGENTS.md`.

## Validation

For Auctra template consumption, prefer the explicit dry-run and binding health
checks before any review-gated mutation:

```bash
auctra prompt-context catalog bind '<template-address>' --target <unit-id> --input-ref name=target.title --dry-run --json
auctra prompt-context catalog binding check --id '<binding-id>' --json
```

Never infer that `preview`, `bind`, or `check` executes a provider. `bind`
without `--dry-run` creates only a refs-only draft; acceptance and text
generation remain separate owner-gated steps.

Run only the commands for the affected owner:

```bash
(cd backend-server/template-registry && go run ./cmd/template-registry catalog build --repository ../../data/yeisme-prompt-templates --json)
(cd backend-server/template-registry && go run ./cmd/template-registry catalog validate --repository ../../data/yeisme-prompt-templates --json)
(cd shared/promptrepo && go test ./...)
(cd backend-server/template-registry && task test:integration)
(cd data/yeisme-prompt-templates && openspec validate --all --strict --no-interactive)
```

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Prompt body in logs/events/evidence | Inspect/render stay provider-free | Bodies never enter ordinary structured output |
| Two owners writing the same template | One canonical writer; others consume refs/digests | Do not copy private state |
| `bind` treated as generation | `--dry-run` then refs-only draft | Acceptance stays with the consuming owner |
| Chinese file compiled as Agent template | `docs/template-zh-CN.md` is review-only | `en` is the only compilable locale |
| Registry metadata hand-written | Template Registry CLI | Content owner may edit prose, not catalog JSON |

## 完整指南的归属

指南正文和逐角色用例归内容仓 docs/README.md；可选 GuideReader、固定来源路径与一致性校验归公共 SDK；prompt guide、MCP guide/resource 和显式文件导出归 Registry。既有 Client 不增加必实现方法。指南不属于可执行 Prompt，不改变 catalog/template digest 或编译资格。

先发现安装版能力，再读取指南与 inspect。MCP 客户端不要求安装 CLI；本地 stdio 和已配置的 Streamable HTTP 复用同一应用合同。

教程 case authoring 与固定验证流程归 Registry/内容 owner；领域 schema 与接受仍归消费者。section 为 GuideReader 的增量读取选择，不改变原全文 digest。独立 Operator 升级由 Registry 宿主 CLI 管理单一内置 Skill；profile 管理项目保持原 manager，不扩展成第二个通用 Skill manager。
