---
name: eikona-pixel-sprite-director
description: Use when converting a character into a 4x4 transparent pixel-art battle sprite sheet through Eikona, and when turning an existing sprite sheet PNG into a looping transparent battle GIF through actual code (Pillow) rather than image generation, including frame splitting, alpha cleanup, duration timing, transparent GIF encoding, and automated validation.
---

# Eikona 像素战斗精灵导演

两步流水线：**生成精灵图（图像模型）→ 代码转 GIF（Pillow，不是生图）**。第一步的提示词模板在模板仓库 `data/yeisme-prompt-templates/solutions/image/pixel-battle-sprite`（en 编译，zh 见包内 `docs/template-zh-CN.md`）；第二步由本技能的 `scripts/sprite_to_gif.py` 实际执行。

## 第一步：生成 4×4 透明精灵图

1. 准备角色参考图（可选）与角色一句话描述。
2. 绑定模板 `promptrepo://official/image/pixel-battle-sprite@1.0.0?locale=en` 的变量：`character`（必填）、`reference_binding`（参考图附加说明）、`combat_style`（有默认值）。
3. 经 Eikona 出图（参考图用编辑/参考输入通道；模型默认 `openai/gpt-5.4-image-2`，用户指定更新的图像模型时从其指定）。
4. 验收对照模板自检清单：4×4、16 帧、真透明、无文字网格、帧间一致、可循环。

## 第二步：代码转 GIF

```bash
python3 .skills/yeisme/eikona-image/eikona-pixel-sprite-director/scripts/sprite_to_gif.py \
  <sprite.png> -o <battle.gif> --json
```

- 读取 RGBA → 稳定整数边界切 16 帧（从左到右、从上到下）→ 低 Alpha 脏像素清理（默认阈值 10）→ 透明画布统一帧尺寸（不缩放、不居中、不改注册点）→ 非固定帧时长（默认总长约 1.84s，超范围自动归一到 1.5–2s）→ 索引色透明 GIF（预留透明色索引 255，`disposal=2`，`loop=0`，`optimize=False`）。
- 保存后自动重读校验：16 帧、无限循环、尺寸一致、时长范围、透明索引、disposal；失败自动修正一次再校验，仍失败则退出非零。
- 源图若含完全重复的帧（distinct < 16），fail-closed 退出并说明原因：GIF 编码无法在不改动内容的前提下保留完全相同的帧——先修精灵图，不要试图绕过。
- 禁止：缩放、插帧、补帧、重绘、给透明区填背景色。

## 交付

GIF 文件 + 验证报告（文件名、尺寸、帧数、总循环时长、是否无限循环、是否透明）。

## 不要做

- 不要把第二步当生图任务；不要调用图像模型重画精灵内容。
- 不要在技能内复制模板仓库的提示词正文；模板改动走仓库并 `contract refresh`。
