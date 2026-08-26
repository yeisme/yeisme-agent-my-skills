# 角色场景路由图

角色不是单一 persona prompt。每个场景都要区分 `identity/canon`、`state/memory`、`authority/tools` 和 `presentation` 四个 owner 面。

## 场景矩阵

| 用户请求 | primary | canonical owner | 必须先阻断 |
| --- | --- | --- | --- |
| “给小说设计一个复杂反派” | `character-intelligence-router` | Auctra | 证据/推断边界、正典 owner |
| “用某导演感做短剧人物” | `creative-style-lens-builder` → 人物/剧本 worker | Auctra | 精确模仿、独特表达重合、来源权限 |
| “做一个会记仇、能成长的 RPG NPC” | `role-blueprint-builder` | future game owner | 事件账本、状态 owner、可回放、LLM 不直接改状态 |
| “做一款皇帝管理朝廷派系的游戏” | `llm-game-direction-strategist` → `role-blueprint-builder` → `llm-game-systems-architect` | future game owner | 皇权不等于系统权限、玩家 agency、派系规则、成本 |
| “让秦始皇给我战略建议” | `role-blueprint-builder` 或 `creative-style-lens-builder` | 当前 host；若保存则进入对应 owner review | 历史来源、推断标记、非本人声明、无外部代理权 |
| “做一个长期陪伴数字人” | `role-blueprint-builder` | `agent/digital-human`；记忆提案交 Pinax | 模拟披露、情感依赖、隐私、记忆审批、紧急场景降级 |
| “把我蒸馏成决策分身” | `role-blueprint-builder` | 用户；可移植记忆交 Pinax | 本人同意、第三方隐私、不冒充、不代替承诺/发送 |
| “给 Ordo 配一个皇帝总管角色” | `agent-platform-prd` / Ordo owner | `agent/ordo` | 职责与人格分离、tool allowlist、预算、审批、审计 |
| “让女娲批量生成几十个 NPC” | 先 `role-blueprint-builder` 生成一个原型并验收 | future game owner | 先单角色 canary；禁止批量复制缺陷和受保护设定 |
| “角色要有固定形象和声音” | accepted blueprint → Anatomia/Eikona/Sonora | 各资产 owner | rights、identity freeze、asset refs、review receipt |

## Owner 分工

- **Auctra**：作者接受的人物事实、关系、弧线、场景文本、review、version 和 export。
- **Game owner**：规则内核、世界状态、NPC state、命令校验、事件账本、存档、回放、玩法遥测。
- **digital-human**：实时会话/呈现控制面；不得偷偷成为人物正典或长期记忆真源。
- **Pinax**：有来源、scope、permission 和 lifecycle 的记忆/上下文；Agent 默认只能 propose。
- **Ordo / runtime owner**：工作角色、工具 allowlist、sandbox、预算、任务和证据；称号不授予权限。
- **Anatomia/Eikona/Sonora/Scaena**：外形、图像、声音和生产资产；不得重写角色认知或正典。

## 渐进式调用链

```text
intent classification
-> RoleRoute
-> RoleBlueprint proposal
-> one owner-specific adapter
-> bounded session simulation
-> deterministic vertical slice
-> evidence-backed promotion
```

不要从“角色卡”直接跳到长期自治、多角色社会或生产发布。
