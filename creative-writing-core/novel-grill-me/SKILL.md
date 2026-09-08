---
name: novel-grill-me
description: Use when the user explicitly wants a direct dependency-aware interview for a novel, web novel, short story, long-form series, chapter, revision, serialization, or novel adaptation without first routing through a generic creative-content question.
---

# 小说 Grill Me

直接进入小说决策 frontier，不再询问内容媒介。运行前加载 `creative-grilling`、其 Frontier/contract/depth references，以及 [references/novel-frontiers.md](references/novel-frontiers.md)。

## 启动

1. 固定 `domain=novel`，识别当前 `phase` 和 `target_artifact`。
2. 如果用户给出 Auctra 项目、项目路径、unit/chapter ref，或当前目录可发现 Auctra workspace，设置 `project_mode=auctra`，加载 `auctra-creative-decision-handoff` 读取事实。
3. 否则设置 `project_mode=projectless`，保持 chat-only。
4. 按共享 depth 规则选择 `quick|standard|deep`。长篇、连载、改编、跨卷或 canonical 变更默认 `deep`。
5. 生成 `creative.grill-route.v0.1`，然后按当前小说 phase 运行 frontier。
6. 按 [references/novel-frontiers.md](references/novel-frontiers.md) 的阶段进入条件加载最窄阶段问法（想法、人物、结构、章节、场景、成稿、修订）；上游未定时不预问下游。
7. 用户提供 `creative.owner-session-binding.v0.1` 时按 `frontier-protocol.md` 的恢复/刷新/重开规则执行；中途进入或接手已有项目时先读取 owner 当前版本的 accepted 决定，只访谈未决与被重开节点。

## 小说范围

- 立项、读者契约、类型承诺和完成标准。
- premise、主题、世界规则、人物与关系。
- 短篇/中篇/长篇/系列/连载、分卷和大纲。
- 章节、场景、视角、叙述距离、声音和对白。
- 修订、连续性、留存、反馈归因和改编边界。

问题只覆盖当前 artifact。篇幅和读者承诺未定时，不追问精细章纲；canon 和 source revision 未核实时，不询问用户当前实现事实。“不知道、哪个更好看”转有界 proof（试写/proof slice/读者小样），不替用户决定；阶段理解确认后才可按 `creative-grilling/references/writer-handoff.md` 串行交接最窄 writer，候选返回后恢复访谈。

## 收束

frontier 为空后输出 `creative.decision-brief.v0.1` 并等待用户确认。确认后：

- projectless → handoff 给 `chinese-novel-orchestrator` 或最窄 `chinese-novel-*` Skill；仍不写文件。
- Auctra → 生成 `creative.owner-handoff.v0.1`，交给 `auctra-creative-decision-handoff`。
- 改编 → 先完成小说 source contract，再把 accepted refs 交给目标媒介 router。

用户确认 brief 不等于创建 scratch、promote review、capture memory 或 accept canonical。

