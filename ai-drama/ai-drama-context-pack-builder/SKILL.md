---
name: ai-drama-context-pack-builder
description: Use when an AI drama story, episode, scene, director, visual, continuity, review, repair, or production task needs a minimal versioned context pack assembled from Auctra canon, Scaena production facts, Inferrum ContextPack results, accepted evidence, character state, continuity, style, and production constraints without loading the whole project.
---

# AI 做剧上下文包构建器

## 目标

在具体创作或生产阶段前，整理“本轮不知道就会写错、导错或生成错”的最小信息。上下文包只做检索压缩、来源标注和交接，不成为新的 RAG 数据库或 canonical state。

## 输入

- `DramaRoutePlan`、目标阶段、目标 artifact 和下游 `target_skill`。
- Auctra 的 accepted story/character/scene refs，Scaena 的 current production/continuity refs。
- 可选 Inferrum `ContextPack`、StyleLens、DirectorProfile、ProductionConstraintProfile、review/evidence refs。
- principal/project/Episode scope、revision/digest、freshness 和 permission 状态。

## 参考资料

- 需要选择上下文包粒度和字段时读取 `references/context-pack-profiles.md`。
- 需要判断来源等级、权限、引用、freshness、stale 和降级行为时读取 `references/source-evidence-policy.md`。

## 工作流

1. 根据 `phase`、`artifact` 和 `target_skill` 选择一个 `context_pack_profile`，不得默认导出全项目百科。
2. 按权威顺序收集事实：current canonical owner facts → accepted project facts → adjudicated evidence → permission-safe retrieved evidence → planned/candidate material。
3. 跨项目检索需要由 Inferrum 现有权限感知 `ContextPack` 合同提供；不要让 Router、Skill 或 Scaena 私自遍历其他 Owner 的文件、数据库或全文。
4. 只保留会影响本轮人物行动、知识边界、冲突、镜头、主体版本、连续性、时长、成本、权利或验收的内容。
5. 为关键信息标记 source ref、revision/version、digest、maturity、freshness 和 confidence；candidate/planned 不得升级为 confirmed。
6. 任一 required source 为 `stale`、`revoked`、`permission_denied`、`contract_mismatch` 或 unknown 时停止晋级，返回缺口与安全降级动作。
7. 生成最小 handoff，并明确哪些信息被忽略、为什么忽略、何时需要重建上下文包。

## 输出

返回 `DramaContextPack`：

- `schema_version`、`pack_profile`、`target_skill`、`phase`、`artifact`；
- `project_ref`、可选 `episode_ref`/`scene_ref`/`shot_refs`；
- `canon_snapshot`、`active_characters`、`knowledge_boundaries`；
- `active_conflicts`、`open_loops`、`continuity_invariants`；
- 可选 `style_lens`、`director_constraints`、`production_constraints`；
- `source_evidence`、`retrieval_summary`、`ignored_context`；
- `missing_inputs`、`blocking_findings`、`pack_digest_basis`、`expires_when`；
- `handoff`、`status`。

`status` 使用 `ready`、`needs_input`、`needs_retrieval`、`blocked`、`stale` 或 `degraded_no_rag`。

## 质量门槛

- 删除任一信息都会明显增加本轮出错概率；否则该信息不应进入最小包。
- 每条硬约束和关键事实都能回到 Owner ref 或 citation。
- 包外事实不得伪装成检索证据；模型记忆和聊天 transcript 不作为事实来源。
- 包必须有明确过期条件，例如 canon revision、SubjectVersion、StyleLens、permission 或 production profile 变化。

## 边界

- 不写剧本、不做导演结论、不评选候选、不修改 canonical state。
- 不复制完整剧本、图片/视频 bytes、raw prompt、provider payload、凭据、私有路径或完整思维链。
- 不把 Inferrum 命中直接当作主体冻结、production acceptance 或人工决定。
- 需要持久化结构化项目状态时，交给 Auctra、Inferrum、Scaena 或对应 Owner 的 CLI/application service。

## 验证

```bash
scripts/skills.sh resolve ai-drama-context-pack-builder
scripts/skills.sh resolve enterprise-multimodal-knowledge-router
scripts/skills.sh validate-custom
```
