---
name: eikona-xhs-cover-director
description: Use when designing Xiaohongshu cover images, first-frame visuals, or title-safe 3:4 static assets for Eikona; produce visual briefs, candidate directions, executable generation commands, and review handoff steps.
---

# Eikona 小红书封面导演

为小红书笔记设计静态封面图，并输出可执行、可评审、可交接的 Eikona 创作方案。

## 输入

- 笔记标题、主题、账号调性、主体元素、色彩偏好和禁用元素。
- 可选：参考图、产品图、人物限制、是否需要真实摄影感。

缺少标题或主体时，先从正文提炼；仍无法判断时，只问一个最小澄清问题。

## 工作流

1. 提炼封面任务：一句主标题、视觉主体、背景、风格和构图。
2. 设计 3 个封面方向：真实生活感、信息型、强情绪钩子型；每个方向说明适合的标题位置和风险。
3. 为推荐方向输出 Eikona 提示词，明确中文标题留白、3:4 竖版安全区、主体大小和禁用项。
4. 加载 `eikona-file-prompt-workflow`，将 brief 和候选保存到 `prompts/xhs/cover/<collection>/`；推荐方向使用独立 prompt 文件，多方向使用 runbook。
5. 给出本地验证命令、真实生成命令，以及生成后的 review/feedback/handoff 命令。
6. 如果用户提供参考图，先确认来源和权限；权限未知时不生成自动上传 provider 的命令。

## 命令示例

本地验证：

```bash
eikona generate --model fixture:image --aspect 3:4 --size 1024x1536 --input prompts/xhs/cover/skincare-morning/prompts/01-clean-lifestyle.md --dry-run --json
```

真实生成：

```bash
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --aspect 3:4 --size 1024x1536 --input prompts/xhs/cover/skincare-morning/prompts/01-clean-lifestyle.md --json
eikona review packet <run_id> --json
eikona feedback accept <run_id> --artifact <artifact_id> --reason title_safe --reason composition --json
eikona assets handoff <artifact_id> --agent
```

## 输出

- 3 个候选方向及推荐排序。
- 推荐方向的完整视觉 brief、分类目录、prompt 文件和可选 runbook。
- 本地验证、真实生成、review、feedback、handoff 命令。

## 质量标准

- 封面必须有可放中文标题的位置，不能让主体遮挡标题区。
- 避免廉价模板感、过度滤镜、虚假前后对比和不可验证效果图。
- 手机首屏要能一眼识别主体；不要把核心卖点放进模型容易写错的小字。
- 文字必须作为版式意图处理；最终中文标题是否准确需要 review，不默认信任生成图中文字。

## 边界

- 不承诺医学、美容、金融效果；涉及功效时使用保守视觉表达。
- 不仿冒真实平台截图、聊天记录或第三方品牌官方物料。
