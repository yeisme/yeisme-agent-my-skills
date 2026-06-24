---
name: eikona-xhs-comic-director
description: Use when designing Xiaohongshu comic-style static posts, situational short comics, educational comics, or story cards for Eikona; create original character/page briefs, generation commands, and review handoff steps.
---

# Eikona 小红书漫画图文导演

把观点、教程或故事设计成小红书可读的静态漫画风格图文，并保持角色设定、页序和 Eikona 证据链可追踪。

## 输入

- 主题、角色、场景、剧情节点、目标读者、画风和页数。
- 可选：品牌色、角色禁忌、是否需要对白气泡。

缺角色设定时创建原创泛化角色；不要默认使用真人、商标角色或受版权保护角色。

## 工作流

1. 拆出漫画页序：冲突、误区、发现、解决、总结或互动。
2. 为每页写画面描述、角色动作、对白气泡和旁白。
3. 统一角色设定、服装、表情、画风和色彩，避免每页角色长相漂移。
4. 输出逐页 prompt、整组生成命令和 review/feedback/handoff 下一步。
5. 涉及知识科普时，先确认事实来源；高风险建议必须保守表达。

## 命令示例

本地验证：

```bash
eikona generate --model fixture:image --aspect 3:4 --size 1024x1536 --count 4 --prompt "小红书漫画风格图文，四页，主题是新手护肤误区，原创角色，柔和配色，中文对白气泡清晰，轻松真实" --agent
```

真实生成：

```bash
eikona generate --model openai:gpt-image-2 --aspect 3:4 --size 1024x1536 --count 4 --prompt "小红书漫画风格图文，四页，主题是新手护肤误区，原创角色，统一服装和发型，柔和配色，中文对白气泡清晰，轻松真实" --agent
eikona review packet <run_id> --json
eikona feedback accept <run_id> --artifact <artifact_id> --reason character_consistency --reason story_clarity --json
eikona assets handoff <artifact_id> --agent
```

## 输出

- 页序表：页码、剧情功能、画面、动作、对白、旁白。
- 原创角色设定和统一画风约束。
- 本地验证、真实生成、review、feedback、handoff 命令。

## 质量标准

- 漫画要服务信息表达，不只追求可爱。
- 不使用侵犯真人肖像、商标或受版权保护角色的设定。
- 复杂医学、金融、法律建议必须保守表达并提示核实。
- 每页对白控制在手机可读范围内；生成图中文字必须经过 review。
- 角色外观、服装和关系在整组图片中要尽量一致。

## 边界

- 不生成仿冒某漫画、动画、影视 IP 的角色或画风复刻请求。
- 不把私密故事素材、原始提示词、供应商载荷或完整思维链写入结构化资产。
