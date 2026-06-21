---
name: eikona-xhs-visual-router
description: 使用场景：当用户需要为小红书笔记生成静态视觉资产时使用；路由到封面、图文卡片、信息图或漫画风格图像指挥技能。
---

# Eikona 小红书视觉路由器

先判断小红书静态图需求，再加载最小的 Eikona 视觉指挥技能。

## 工作流

1. 判断视觉类型：封面图、3/6/9 图文卡片、信息图、漫画风格图文。
2. 如果用户只有文案，先要求或提取标题、正文要点、账号调性和禁用视觉元素。
3. 将封面交给 `eikona-xhs-cover-director`，图卡系列交给 `eikona-xhs-card-series-director`，信息图交给 `eikona-xhs-infographic-director`，漫画交给 `eikona-xhs-comic-director`。
4. 所有新图像示例默认使用 `openai:gpt-image-2`。

## 命令示例

```bash
eikona generate --model openai:gpt-image-2 --aspect 3:4 --size 1024x1536 --prompt "小红书封面图，中文标题区域清晰，真实生活感，干净明亮" --dry-run --json
```

## 边界

- 只处理静态图，不处理视频、动效、发布或平台账号操作。
- 不把原始提示词、供应商载荷或完整思维链写入结构化资产。
