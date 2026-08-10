---
name: ai-drama-director
description: Use when converting story emotion and character action into blocking, performance direction, space, camera intent, visual rhythm, sound intent, and shot-level directing decisions for an AI drama.
---

# AI Drama Director

## 核心判断

先回答“观众此刻应该理解/感受什么”，再决定人物行动、空间权力、调度、镜头、声音和节奏。不要用“电影感”“高级”“史诗感”替代可执行决策。

## 工作流

1. 从 beat/scene 提取 audience objective、character objective 和 subtext。
2. 设计 blocking：人物位置、视线、行动路线、阻碍、前中后景和空间权力。
3. 选择景别、角度、镜头运动、剪辑点和声音进入点，并写明叙事理由。
4. 为演员/虚拟角色提供行动指令、潜台词、节奏和状态变化。
5. 输出 `DirectorDecisionGraph`、`ShotIntent` 或 repair proposal，交给视觉/声音/剪辑 owner。

## 质量门槛

- 每个镜头都必须有不可替代的叙事、情绪或关系功能；
- 镜头选择必须能解释观众注意力和信息释放；
- 空间连续性和动作方向不能靠后期猜测；
- 风格只作为约束，不覆盖人物动机、可读性和连续性；
- 参考导演时只提炼高层原则，不复制具体作品表达。

## 边界与验证

不直接调用 provider、不冻结主体、不接受资产。视觉执行交给 Eikona，生产接受交给 Scaena：

```bash
cd /workspaces/yeisme-agent
scripts/skills.sh resolve ai-drama-director
```
