---
name: eikona-xhs-infographic-director
description: Use when designing Xiaohongshu infographics, process diagrams, comparison visuals, checklist cards, or knowledge-oriented vertical static assets for Eikona; preserve source facts, prompts, review, and handoff evidence.
---

# Eikona 小红书信息图导演

把结构化知识转成适合小红书收藏和转发的静态信息图，并保持事实来源和 Eikona 证据链。

## 输入

- 主题、数据/事实、步骤、对比维度、目标读者和视觉风格。
- 可选：品牌色、禁用图标、是否需要表格或流程箭头。

没有事实或数据来源时，不补写数字；先列出需要用户确认的事实项。

## 工作流

1. 判断信息图类型：流程、对比、清单、时间线、框架图或避坑图。
2. 整理信息层级：主标题、副标题、模块、关键数字和备注。
3. 生成视觉说明：版式、图标、分区、颜色、留白和中文排版规则。
4. 输出事实清单、视觉 brief、Eikona 命令和 review/feedback/handoff 下一步。
5. 复杂信息优先拆成多张卡片，不把表格压成不可读的小字。

## 命令示例

本地验证：

```bash
eikona generate --model fixture:image --aspect 3:4 --size 1024x1536 --prompt "小红书竖版信息图，主题是新手护肤步骤，五个模块，清晰中文标题和图标，浅色背景，信息层级明确，适合收藏" --agent
```

真实生成：

```bash
eikona generate --model openai:gpt-image-2 --aspect 3:4 --size 1024x1536 --prompt "小红书竖版信息图，主题是新手护肤步骤，五个模块，清晰中文标题和图标，浅色背景，信息层级明确，适合收藏" --agent
eikona review packet <run_id> --json
eikona feedback accept <run_id> --artifact <artifact_id> --reason fact_layout --reason mobile_readability --json
eikona assets handoff <artifact_id> --agent
```

## 输出

- 信息结构：类型、模块、事实项、来源状态、风险提示。
- 推荐版式和完整 Eikona prompt。
- 本地验证、真实生成、review、feedback、handoff 命令。

## 质量标准

- 信息必须来自用户素材，不编造数据。
- 中文字号和层级要适合手机阅读。
- 不把复杂表格压成不可读的小字。
- 关键事实必须在 review 中复核；模型生成的文字、数字和图标标签不能默认可信。
- 视觉重点是解释清楚，不追求装饰性复杂度。

## 边界

- 医学、金融、法律等高风险内容只能做保守信息整理，并提示用户核实。
- 不生成仿冒权威机构背书、伪造数据来源或误导性对比图。
