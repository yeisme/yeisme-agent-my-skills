# 接入与验证（DEK v1）

> 总览见 [HANDOFF.md](HANDOFF.md)；C1/C2/C3 的后续实现规格、并行 lane 与验收命令见 [implementation-roadmap.md](implementation-roadmap.md)。

## 独立仓库关系

| 仓库 | 角色 |
| --- | --- |
| `yeisme/yeisme-agent-my-skills` | **本模块所在仓库**，全部自建 skills 的源层；在主仓以 submodule `.skills/yeisme` 挂在 `develop` 分支 |
| `yeisme/ai-drama-skills` | 做剧 skills 的便携发布入口（`npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes`） |
| `yeisme/yeisme-agent` | 主仓，持有 `.skills/profiles/**`、runtime 副本生成与各 owner 子项目 |

**不得在两个发布仓库维护同一 skill 的不同正文**。源层修改只发生在 `.skills/yeisme/`，`ai-drama-skills` 作为发布镜像由发布流程同步；重命名或改 frontmatter 必须遵循 `yeisme-evolutionary-change-policy`（至少一个 release 的兼容入口）。

## Skill 分层与 profile 分配

按 `yeisme-skill-publisher` 规范：源在 `.skills/yeisme/<module>/<skill>/`，每个 skill 含 `SKILL.md` + `agents/openai.yaml`；`.agents/skills/` 与 `.claude/skills/` 是生成副本，不手改；`root.txt` 不新增条目。

| target profile | 新增条目 |
| --- | --- |
| `.skills/profiles/targets/agent/scaena.txt` | `scaena-asset-draw-batch`、`scaena-bounded-replacement`、`ai-drama-action-receipt` |
| `.skills/profiles/targets/cli/eikona.txt` | `ai-drama-action-receipt`、`ai-drama-remote-operations` |
| `.skills/profiles/targets/client/yeisme-control-center.txt` | `ai-drama-remote-operations` |

`ai-drama-router` 已在 root runtime，不重复分配。所有新 skill **按需加载**，由 Router 的 `execution_lane` 轴选中，不进 root runtime、不批量激活。

`ai-drama-bootstrap` 是 Router 之前的环境准备层（安装 skills / CLI、配置连接、交接 Router），由用户复制引导提示词触发，**按需、不加入任何 target profile**。提示词源在 `yeisme/ai-drama-skills` 的 `ai-drama-bootstrap/references/`：

| 版本 | 文件 |
| --- | --- |
| 完整版 | `bootstrap-prompt.md` |
| 简短版 | `bootstrap-prompt-short.md` |
| 渐进式 | `bootstrap-prompt-progressive.md` |
| 选择指南 | `prompt-variants.md` |
| binding 参考（已降级） | `surface-choice.md` |
| 命令全表 | `install-and-connect.md` |

三版共同的机制：**不再询问 `cli|mcp|both`**，流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding；凡 agent 发起的非只读动作都要审批，但用一次 `ApprovalWindow`（`capability_kinds[]` / `intent_digest` / `binding_allowlist` / `count` / `cost_ceiling` / `retry_budget=2`）实现窗口内全自动，含可重试错误自动重试最多 2 次。UNKNOWN 只 `reconcile` 且不消耗预算；越界或耗尽交 `needs_decision`。`surface-choice.md` 已降级为 binding 参考。完整设计见 [capability-abstraction.md](capability-abstraction.md)，自动化流程见 [automation-core.md](automation-core.md)。

## 完善清单（向后兼容，只加引用段落，不改 frontmatter）

| Skill | 追加内容 |
| --- | --- |
| `ai-drama-router` | `execution_lane` 轴 + 4 个新 skill 的路由条目；写明「Router 只选一个 primary，执行链交 DEK」 |
| `ai-drama-production-orchestrator` | 把散落的 receipts / bounded retries / honest capability checks 统一引用 `ai-drama-action-receipt` 词汇 |
| `scaena-production-operator` | 补 `identity_equal` 门、失败受控修复、共享 claim、UNKNOWN 只读恢复；`defect-routed refinement` 分岔到 `scaena-bounded-replacement` |
| `scaena-subject-asset-readiness` | 补 batch 入口、`template_digest` 保护、快覆盖转交条件；保留 human-only `select/freeze` |
| `eikona-asset-lifecycle` | 补 `replacements replace/rollback` 的「技术回滚 ≠ 验收」、scope grant 与 accepted delivery 分离 |
| `scaena-production-decision-handoff` | 作为 `FrozenRef` 链形状的落点（已有 zero-call simulation + `creative.owner-handoff.v0.1`） |

## 验证命令

```bash
scripts/skills.sh validate-custom
scripts/skills.sh list-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
scripts/skills.sh validate-runtime
```

按影响范围选择命令，普通修改不要求每次跑全套；跨多个真实消费方时才用 `sync-subprojects`。profile 变更必须用 `scripts/skills.sh profile add`，不手写 targets 文件。

## owner 侧实现归属

| 合同 / 能力 | owner | 位置 |
| --- | --- | --- |
| C1 `yeisme.owner_action.v1` + typed action 路由 | Scaena / Eikona | `agent/scaena`、`cli/eikona` 各自的 OpenSpec change |
| C2 `scaena.draw_batch.v1` | Scaena | `agent/scaena` |
| C3 `yeisme.replacement_bound.v1` | Eikona + Scaena | `cli/eikona`、`agent/scaena` |
| `action_id` → `revision` 去重 | 控制中心 | `client/yeisme-control-center` |
| 合同形状与交接记录 | 主仓 | root `openspec/` 交接记录 |

主仓不保留本模块的设计文档副本；本目录是唯一真源。

## 落地顺序

| 阶段 | 内容 | 验收 |
| --- | --- | --- |
| D0 | 本目录设计文档 + 4 个新 skill 源 + 6 处完善 + profile 分配 | 上面 6 条 `scripts/skills.sh` 全绿 |
| D1 | C1：`scaena-api` typed action 路由 + Eikona `/api/v1` 对齐 receipt envelope | `scaena remote doctor --json`；远程提交一个 EU-02 后返回 `action_id` + `event_cursor`，且不产生客户端 owner state |
| D2 | C2 + EU-02/03/04 垂直切片 | 一次 `batch_ref` → 并发 → 一次回查；断线 `workflow resume` 无第二个 provider attempt |
| D3 | C3 + EU-09/31 | 非 FAILED 或配置漂移拒绝重提；并发两入口最多一个提交；回滚不冒充验收 |
| D4 | L-Projection 控制中心 `action_id/revision` 去重 | `bun run test:preview:real`；缓存由 `event_cursor` 驱动而非三层轮询 |

## 禁止事项

- 不从 runtime 副本发布源码；不向 `.codex/skills/` 重复安装同一 skill；
- 不把本模块变成第二个做剧 router 或跨 owner 网关；
- 不改付费 / 发布 / 凭据 / 线上配置；真实 provider canary 单独授权；
- 不把凭据、provider payload、raw prompt、全链路推理写进 receipt / evidence / stdout。
