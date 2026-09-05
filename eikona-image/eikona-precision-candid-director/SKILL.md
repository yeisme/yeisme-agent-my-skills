---
name: eikona-precision-candid-director
description: Use when creating precision-parameterized candid lifestyle photos through Eikona — single fully-specified shots with exact camera height/lens/framing percentages, foreground coverage ratios, quantified color palettes, two-source lighting, scene fingerprints, and tag-managed shot spec libraries, as opposed to random matrix batches or fixed poster systems.
---

# Eikona 精调抓拍镜头导演

面向「精调参数化」抓拍写真：每条 shot spec 完整决定一张图——机位高度（cm）、焦段、主体占幅比、前景遮挡比、色块百分比、双光源方向、场景指纹全部量化。与两个姊妹技能的分工：`eikona-candid-photo-director` 做随机矩阵批量采样，`eikona-iconic-landmark-poster-director` 做固定视觉系统系列海报，本技能做单镜头精确复现。落盘规范遵循 `eikona-file-prompt-workflow`，执行交给 `yeisme-eikona-cli-runtime`。

## 输入

- `shot`：镜头 spec id（`assets/shots/<id>.json`，现有 `night-bedroom-lookback`、`night-flash-lean-in`；`--list-shots` 查看）。
- `aspect` / `size`：默认取 spec 内值（9:16，`1024x1536`）。
- 新镜头：复制现有 spec 改内容，不需要改代码。

## 工作流

1. 渲染（确定性，纯 stdlib）：

   ```bash
   python3 .skills/yeisme/eikona-image/eikona-precision-candid-director/scripts/render_shot.py \
     --shot night-bedroom-lookback \
     --out prompts/<owner>/precision-candid/night-bedroom-lookback
   ```

2. 产物：`prompts/01-<shot>.md`（英文提示词，无 frontmatter）、`runbook.yaml`（`eikona.batch.v1`，模型 `openai/gpt-5.4-image-2`）、`manifest.json`（tags + combo + 色板数据，脚本生成，不要手写）。
3. 按 runbook 走 Eikona CLI 执行；审阅后改 spec 重渲，combo 变化即提示词内容变化。

## 提示词槽位顺序（固定）

`规格行 → 主体+姿势+表情 → 服装 → 机位（高度/焦段/占幅/裁切）→ 前景遮挡比 → 双光源 → 色块百分比 → 场景指纹 → 质感氛围 → 负向`。

模板正文的 canonical 归属是模板仓库 `data/yeisme-prompt-templates/solutions/image/precision-candid-shot`（promptrepo 包，contract 声明 21 个输入，规范投递语言为 `main.en.md`）。`render_shot.py` 加载该模板，把 shot spec 的结构化字段组装为子句变量绑定；可选子句绑定为空字符串即整段省略。本技能不内嵌模板正文。

量化语言是本风格的核心：cm、百分比、角度（45 degrees）直接写进提示词，不要改写成模糊形容词。字段说明与 tags 规则见 [references/shot-spec.md](references/shot-spec.md)。

## Tags 管理

`style:precision-candid`、`shot:<id>`、`aspect:*`、`subject:*`、`lens:*`、`light.temperature:*`、`palette.primary:*`、`fingerprint:*`（每个场景指纹一条）、`use:*`、`mood:*` + combo 哈希。完整色板（含百分比）作为数据存 manifest，不进 tag。

## 不要做

- 不要把量化参数改写成文学化描述——精确数字就是这种风格的交付物。
- 不要手写 manifest.json 或 tags。
- 不要在本技能里做批量随机采样（那是 candid-photo-director）或固定视觉系统（那是 landmark-poster-director）。
