---
name: ai-drama-story-architecture
description: Use when designing or revising an AI drama premise, theme, conflict engine, beat sheet, scene purpose, episode arc, hook, escalation, or ending before canonical screenplay writing.
---

# AI Drama Story Architecture

## 目标

把故事想法变成可验证的戏剧结构，而不是直接生成一篇漂亮梗概。核心判断是：人物为什么不得不做这件事，以及每个 beat 如何改变信息、关系、风险或情绪。

## 输入

- `DramaFormatContract`：format profile、类型契约、受众承诺、结构单位和回报节拍；
- `DramaContextPack`：本轮需要的 accepted facts、人物状态、知识边界、连续性和来源；
- `CreativeBrief`：题材、受众、媒介、时长和目标情绪；
- `CanonSnapshot`：世界规则、已有角色、时间线和禁用事实；
- `DirectorProfile` 与 `ProductionConstraintProfile`；
- 可选的 Auctra screenplay/beat revision refs。

## 工作流

1. 提炼一句话 premise、主题命题和观众承诺。
2. 建立 `desire → obstacle → choice → cost → change` 冲突链。
3. 设计 episode/scene beats：每个 beat 标注目标、阻碍、转折、信息和情绪变化。
4. 检查因果、升级、人物主动性、结尾钩子和可视觉化程度。
5. 输出 `StoryProposal`，交给 Auctra/Dramaturge 评审；不要直接覆盖 canonical screenplay。

## 质量门槛

- 删除一个 beat 后，必须能说明观众会失去什么；
- 关键事件必须由人物选择或规则压力造成，而不是作者方便；
- 每集既要完成局部情绪弧，又要留下可兑现的后续问题；
- 结尾钩子不能只是新信息，必须改变目标、关系或代价；
- 视觉化描述必须可转成场面行动，不能只写抽象情绪词。

## 输出

`StoryProposal` 应包含 premise、theme、audience promise、character goals、conflict chain、beat cards、scene purpose、risk、open questions、CanonSnapshot refs 和下一步 owner action。

## 边界与验证

不写入 Auctra 正文、不伪造观众数据、不以“电影感”代替结构。Auctra 集成验证由 owner 运行：

```bash
cd /workspaces/yeisme-agent/cli/auctra
auctra --help
go test ./...
```
