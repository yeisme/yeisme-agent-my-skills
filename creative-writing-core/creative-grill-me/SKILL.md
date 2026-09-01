---
name: creative-grill-me
description: Use when the user explicitly requests a stateless aggregate high-intensity interview for a creative idea and the system must route to novel, manga-drama, other AI drama, adaptation, or generic content creation before any planning, drafting, prototyping, or production.
---

# 创作 Grill Me 聚合入口

这是显式、无状态的优化入口。它先生成 `creative.grill-route.v0.1`，再把会话交给最窄的领域入口和 `creative-grilling` 共享协议。它不代替 `creative-writing-router`、`chinese-novel-orchestrator` 或 `ai-drama-router`。

## 路由顺序

1. 识别 `domain`：`novel`、`manga_drama`、`ai_drama`、`adaptation` 或 `generic`。
2. 识别 `project_mode`：
   - 没有项目事实：`projectless`。
   - Auctra 项目或 canonical 文本工作：`auctra`。
   - Scaena 分镜/生产项目：`scaena`。
   - 同时包含已接受故事与生产阶段：`cross_owner`，固定 Auctra → Scaena 顺序。
3. 使用 `creative-grilling/references/depth-routing.md` 选择 `quick|standard|deep`；用户显式覆盖优先。
4. 生成 route，包含 `loaded_skills[]`。领域 Skill 或 `creative-grilling` 未实际加载时返回 `missing`，不得声称已运行完整访谈。
5. 领域明确时零路由追问：
   - `novel` → `novel-grill-me`。
   - `manga_drama` → `manga-drama-grill-me`。
   - 其他 AI 做剧 → `creative-grilling`，访谈后交给 `ai-drama-router`。
   - 通用内容 → `creative-grilling`，访谈后交给 `creative-writing-router`。
6. 只有两个以上 domain 同样可信且会改变决策图时，提出最多一个路由澄清问题。

## 输出与交接

- route 使用 `creative.grill-route.v0.1`。
- 访谈使用 `creative-grilling`，最终产生 `creative.decision-brief.v0.1`。
- projectless 保持 chat-only。
- 用户确认共同理解后，才允许生成 `creative.owner-handoff.v0.1`；写入仍需后续 owner Skill 和独立授权。

## 边界

- 不在聚合入口中展开全部小说和漫剧问题。
- 不把改编同时拆成两个完整访谈；先处理 source contract，再处理 target medium。
- 不开始写作、出图、出视频、合成音频、修改项目、accept、导出或付费生产。
- 用户要求停止或收束时，保留未决项并结束当前 frontier。

