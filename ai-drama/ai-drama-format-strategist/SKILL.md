---
name: ai-drama-format-strategist
description: Use when an AI drama, short-drama, manga-drama, television, film, procedural, anthology, comedy, or audio-drama project needs its medium, format profile, episode or season shape, genre contract, audience promise, recurring story engine, pacing cadence, or production-density boundary selected before story planning or adaptation.
---

# AI 做剧形态与类型策略

## 目标

先决定故事由什么形态承载、向观众持续兑现什么，再进入故事架构、分集、场景或生产。不要把美式长剧、竖屏短剧、漫剧、电影和音频剧套进同一结构。

## 输入

- 用户目标、受众、媒介、平台、预计时长/集数、已有 IP 或素材。
- 想要的观看体验、主类型/副类型、制作能力、预算和交付目标。
- 可选 `StyleLens`、已有 Auctra project refs、生产约束和用户明确排除的套路。

## 参考资料

- 需要选择作品承载形态时读取 `references/format-profiles.md`。
- 需要冻结主类型、副类型、观众问题、必备回报和反套路边界时读取 `references/genre-lens-map.md`。

## 工作流

1. 区分媒介与形态：视频、动态漫画、音频只是媒介；`vertical-short-drama`、`us-hour-drama`、`procedural-series` 等才是结构合同。
2. 选择一个 `format_profile`。只有两种形态会实质改变结构、成本或用户承诺时，才列出备选并要求决定。
3. 选择一个 `primary_genre_lens`，最多增加一个 `secondary_genre_lens`；副类型只能改变压力和回报，不能建立第二条互相竞争的主故事引擎。
4. 冻结结构单位、单集/全片时长、集数/季度形态、开场承诺、回报节拍、结尾策略、可重复故事引擎和制作密度。
5. 检查素材复杂度是否适合所选形态。需要删并角色、压缩设定、外化内心或降低昂贵场景时，明确写入 adaptation actions。
6. 选择下一阶段：故事前提交给 `ai-drama-story-architecture`；多集长线交给 `ai-drama-showrunner`；已有场景交给 `screenplay-scene-writer`；已有剧本进入导演设计时交给 `ai-drama-director`。
7. 返回类型与形态合同，不在本 Skill 内写完整剧本或触发生产调用。

## 输出

返回 `DramaFormatContract`：

- `medium`、`format_profile`、`primary_genre_lens`、可选 `secondary_genre_lens`；
- `target_audience`、`audience_promise`、`core_audience_question`；
- `story_unit`、`target_runtime`、`episode_or_season_shape`；
- `opening_contract`、`reward_cadence`、`ending_strategy`、`repeatable_story_engine`；
- `production_density`、`adaptation_actions`、`anti_patterns`、`missing_inputs`；
- `canonical_owner`、`next_primary_skill`、`status`。

`status` 使用 `ready`、`needs_format_decision`、`needs_audience`、`genre_conflict` 或 `production_mismatch`。

## 质量门槛

- 形态合同必须能改变具体结构判断，不能只写“电影感”“美剧感”或“短剧节奏”。
- 类型承诺必须落到人物选择、阻力、代价、信息释放和阶段回报。
- 常见时长/集数只能作为起点，不得伪装成平台硬规则或商业保证。
- 形态与制作能力冲突时先降复杂度或请求决策，不得把成本问题推迟到生成阶段。

## 边界

- 不根据剧型自动安装整套 Skills；把 `next_primary_skill` 交回 `ai-drama-router` 解析。
- 不把 genre 标签当作模仿具体作品的授权；点名风格先使用 `creative-style-lens-builder`。
- 不修改 Auctra canonical screenplay、Scaena ProductionGraph 或任何 Owner structured state。

## 验证

```bash
scripts/skills.sh resolve ai-drama-format-strategist
scripts/skills.sh resolve ai-drama-router
scripts/skills.sh validate-custom
```
