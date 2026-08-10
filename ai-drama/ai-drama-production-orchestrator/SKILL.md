---
name: ai-drama-production-orchestrator
description: Use when coordinating AI drama stages across Dramaturge, Auctra, Ordo, Eikona, and Scaena with typed handoffs, bounded parallelism, approvals, retries, receipts, evidence, and guided-to-unattended maturity.
---

# AI Drama Production Orchestrator

## 目标

编排“做剧”闭环，而不是成为新的领域数据库。所有阶段使用 typed refs、版本、digest、owner receipt 和显式下一动作。

## 三种运行模式

- `guided_conversation`：提案和确认优先；
- `assisted_batch`：阶段性确认后运行有界批次；
- `unattended_batch`：只有成本、权限、质量、异常策略和 kill switch 冻结后才可启用。

## 工作流

1. 读取 `ai-drama-router/references/canon-boundary.md` 与 `ai-drama-producer/references/production-constraints.md`，编译 CreativeBrief、CanonSnapshot、DirectorProfile 和 ProductionConstraintProfile。
2. 调度 Story/Character/Showrunner/Director/Visual/Critic/Continuity/Producer Skills。
3. 在 Ordo 中执行并行候选和评委任务，保存 attempt/receipt/evidence。
4. 把 Auctra screenplay、Eikona artifact 和评估推荐交给对应 Owner；不跨边界写入。
5. 处理 review、repair、pause、resume、partial failure、unknown accept 和 stale invalidation。
6. 读取 `ai-drama-continuity-supervisor/references/continuity-evidence.md`；只在 Scaena 明确选择、连续性检查、production acceptance 和 delivery review 后结束。

## 状态不变量

```text
generated → assessed → recommended → human_review → selected
→ consistency_review → production_accepted → assembled
```

禁止 `assessed → selected`、`recommended → production_accepted` 和“provider succeeded 即交付”。

## 验证

```bash
cd /workspaces/yeisme-agent/agent/ordo
bun run test
cd /workspaces/yeisme-agent/agent/scaena
task test:architecture
task test:integration
```
