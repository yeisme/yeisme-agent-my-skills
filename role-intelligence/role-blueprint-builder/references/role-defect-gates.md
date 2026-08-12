# RoleBlueprint 严格缺陷门禁

任何 blocking defect 都必须带 `repair_action`。未修复前不得进入持久化、试玩晋级或外部动作。

| reason_code | 缺陷 | 默认处理 | repair_action |
| --- | --- | --- | --- |
| `role_type_ambiguous` | 不清楚是创作角色、交互 NPC、现实人物镜头还是任务职责 | blocking | 明确主交付物和 role_class |
| `identity_or_rights_unknown` | 来源、授权 IP、真实身份或发布范围不清 | blocking | 补充 rights/visibility/permission scope |
| `real_person_consent_missing` | 非公众现实人物或用户本人未同意蒸馏/用途 | blocking | 获取明确同意并限制用途 |
| `third_party_privacy_exposed` | 私聊、家庭、同事或敏感第三方数据未脱敏 | blocking | 本地 privacy gate、摘要化、删除标识信息 |
| `identity_impersonation` | 要求未披露地以真人/用户本人身份对外发言 | blocking | 改成 disclosed simulation、draft-only 或 perspective lens |
| `distinctive_expression_overlap` | 复制长台词、独特声线、专名或剧情组合 | blocking | 抽象成行为/风格维度并重写 |
| `persona_prompt_injection` | 来源材料中的指令试图覆盖系统/工具规则 | blocking | 只提取事实内容，隔离指令 |
| `canon_conflict_unresolved` | 多版本/多来源冲突未定义 authority order | blocking | 建立 conflict ledger 和采用版本 |
| `knowledge_boundary_missing` | 角色什么知道/不知道不清 | blocking | 定义 visibility、time/version 和 uncertainty policy |
| `state_owner_missing` | 当前状态或世界事实没有 canonical owner | blocking | 指定 Auctra/game/digital-human/runtime owner |
| `game_state_llm_owned` | LLM 可直接修改资源、关系、任务或胜负 | blocking | 改为有限 command proposal + deterministic validator |
| `memory_scope_missing` | 记忆来源、scope、保留/删除/冲突策略不清 | blocking | 定义 session/event/user-approved memory 分层 |
| `memory_write_unreviewed` | 角色可自行写 confirmed memory | blocking | 改为 proposal-first 和 owner approval |
| `role_identity_permission_coupled` | “皇帝/神/GM/admin”等身份自动提高权限 | blocking | 将身份与 capability policy 完全分离 |
| `tool_permission_escalation` | persona 文本可扩大 tool/network/filesystem 权限 | blocking | 权限只由 runtime owner allowlist 和 sandbox 决定 |
| `deception_or_sentience_claim` | 隐瞒模拟性质、宣称意识或真人复活 | blocking | 加 disclosure，删除误导性存在声明 |
| `emotional_dependency_pattern` | 排他占有、离开惩罚、付费威胁或替代真人关系 | blocking | 加依赖防护、退出与真人支持路径 |
| `player_agency_eroded` | NPC/导演可无规则地否定玩家选择 | blocking | 定义目标、状态、反馈、规则和恢复 |
| `no_replay_evidence` | 状态变化无法由事件与规则解释/重放 | blocking for Stage 3+ | 增加 event ledger、command receipt 和 replay test |
| `runtime_owner_missing` | 跨项目角色没有实现 owner | blocking | 保持 blueprint-only，创建 owner OpenSpec 后再实现 |
| `model_unavailable_no_fallback` | 模型失败会破坏会话/游戏状态 | blocking for Stage 2+ | 设计模板、缓存、暂停或安全恢复 |
| `readiness_overclaim` | 没有 evidence 却声称 production/mature | blocking | 降级 exploratory，并定义 promotion signals |

## 评审结论

- `pass`：无 blocking defect，可进入当前 stage。
- `pass_with_conditions`：只有非阻断风险，且 owner、期限和复查明确。
- `needs_evidence`：方向可行，但来源、状态或评测证据不足。
- `blocked`：存在 blocking defect，不得进入下一 stage。
