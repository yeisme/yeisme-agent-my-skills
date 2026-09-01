---
name: manga-drama-grill-me
description: Use when the user explicitly wants a direct dependency-aware interview for manga-drama or comic-drama format, story, character, episode, scene, storyboard, visual, audio, production, review, or delivery decisions without first routing through a generic creative-content question.
---

# 漫剧 Grill Me

直接进入漫剧决策 frontier，不再询问内容媒介。运行前加载 `creative-grilling`、其 Frontier/contract/depth references，以及 [references/manga-drama-frontiers.md](references/manga-drama-frontiers.md)。

## 启动

1. 固定 `domain=manga_drama`，识别 `phase`、`target_artifact` 和 `project_mode`。
2. 故事、剧本、人物或 accepted source 位于 Auctra 时读取 Auctra owner facts。
3. 分镜、ProductionGraph、readiness、生产 session 或交付位于 Scaena 时加载 `scaena-production-decision-handoff` 读取事实。
4. 同时涉及两者时设置 `project_mode=cross_owner`，固定 Auctra story/canon → Scaena production 顺序，禁止并行写两个 owner。
5. 多集、跨阶段、rights、视觉/音频生产或付费准入默认 `deep`；单场/单镜 projectless 可 `quick`。
6. 生成 `creative.grill-route.v0.1`，然后按当前漫剧 phase 运行 frontier。

## 漫剧范围

- format、观看场景、时长、集数、类型承诺和 proof slice。
- premise、人物、关系、单集引擎、场景与对白。
- 分镜方向、视觉可读性、主体连续、声音意图和字幕负担。
- 预算、provider capability、批次、retry、人工接管、review 和 delivery。

“是否抓人、画面是否清楚、动作是否成立、声音是否有压迫感”属于 hypothesis，转为核心场景 A/B、6–12 格分镜、关键帧、镜头或声音样片。

## 收束

frontier 为空后输出 `creative.decision-brief.v0.1` 并等待用户确认。确认后：

- Story/Character/Episode/Scene → handoff 给 `ai-drama-router`，canonical text 仍归 Auctra。
- Storyboard/Visual/Audio/Production/Delivery → 生成 `creative.owner-handoff.v0.1`，交给 `scaena-production-decision-handoff`。
- 跨 owner → Auctra accepted source/handoff refs 准备完成后，才进入 Scaena simulation/readiness。

用户确认 brief 不等于接受分镜、应用 skill plan、付费生成、冻结主体、production acceptance 或 export。

