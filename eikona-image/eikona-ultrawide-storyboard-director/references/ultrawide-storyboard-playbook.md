# 超宽连续空间故事看板 Playbook

## 核心方法

超宽故事看板不是普通分镜格，而是在一个连续背景空间里呈现多个时间点的角色位置、动作变化和冲突升级。它适合让导演、编剧、剪辑或视频生成流程快速看懂：角色从哪里来、往哪里走、冲突在哪里升级、最终落点在哪里。

## 适用类型

- 动作冲突：追逐、拦截、近身缠斗、撞翻桌椅、借环境反击、逃进巷口。
- 短剧调度：酒店长廊伏击、地铁站逃离、街头追逐对战、夜市场景冲突。
- 历史推演：战场地形、阵型、进攻路线、关键转折、战局结果。
- 线索规划：人物移动路线、线索触发点、观察视线、事件时间线。

动作冲突类更适合转视频；线索、调查、历史推演类更适合剧情规划和连续性检查。

## 输出结构

| 字段 | 要求 |
| --- | --- |
| aspect | 默认 `3:1`，也可用更宽比例；视频参考图另出 `16:9`。 |
| space | 一个连续背景空间，不能拆成漫画格。 |
| beats | 4-6 个时间点，按空间路径或从左到右阅读。 |
| roles | 同一角色可用 ghosted/time-slice composition 表达不同时间点。 |
| markers | 规划看板可用箭头、编号、圈线、时间线；视频参考图必须去除。 |
| review | 重点检查空间连续性、路径可读性、冲突升级、标记是否污染视频参考图。 |

## Planning Board Prompt 模板

```text
3:1 ultrawide continuous-space storyboard for [scene], one uninterrupted [location] background, [N] sequential frozen moments showing [character/team] moving from [entry] to [exit], beat 1 [action], beat 2 [action], beat 3 [action], beat 4 [action], beat 5 [action], beat 6 [action], arrows and numbered beat markers, circled hotspots for key collisions or clues, clear character blocking, readable planning board, cinematic lighting, no comic panel borders
```

## Clean Video-Reference Prompt 模板

```text
clean cinematic wide shot based on the [scene] storyboard, preserve the same [location] layout, character blocking, entry and exit, key props and conflict center, no arrows, no labels, no circles, no timeline marks, no planning annotations, natural camera framing, cinematic lighting, believable motion staging
```

## Review Checklist

- 是否是一个连续空间，而不是拼贴或普通分镜格。
- 入口、路径、冲突中心、关键道具和出口是否清楚。
- 每个 beat 是否能对应剧情动作，且不会互相遮挡。
- planning board 的文字/箭头/圈线是否只服务调度。
- clean video-reference 是否明确去掉所有标记。
- 历史/现实题材是否保留事实边界，不伪造来源。
