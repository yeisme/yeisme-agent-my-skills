---
name: eikona-candid-photo-director
description: Use when generating batches of candid lifestyle photography portraits (真实生活摄影抓拍写真) through Eikona, including randomized scene/wardrobe/moment/shot/lens/camera/composition/foreground/light/palette combinations, batch dedup by tags, parameterized subject descriptions, and prompt-file collections with runbooks for review and generation.
---

# Eikona 抓拍写真导演

把「真实生活摄影抓拍写真」的多维随机矩阵变成确定性、可复现、可审阅、可去重的候选批次。本技能只负责采样组合、提示词文件和 tags 清单；落盘规范交给 `eikona-file-prompt-workflow`，CLI 执行与 run evidence 交给 `yeisme-eikona-cli-runtime`。

## 输入

- `batch`：集合名（必填），即 prompt library 的 collection 层。
- `n`：批次数量，默认 10。
- `seed`：任意整数，默认 42；同 seed + 同参数必出同批次，用于复现与重审。
- `lock dim=value`：锁定维度（可重复），如 `scene=盛夏荷塘`。
- `exclude dim=value`：禁用取值（可重复），如 `palette=深蓝夜色+冷白灯光`。
- `subject` / `subject-text`：主体参数化，见下文。
- `aspect` / `size`：默认 9:16（`1024x1536`，按 provider 能力调整）。

## 主体参数化

主体不进采样矩阵，作为独立参数：

- 默认主体 `kr-ins-default`：「一个极具镜头感的韩国 INS 网红，皮肤白皙，身材夸张」。
- 换主体：`--subject <id>`（在 `scripts/matrix.json` 的 `subjects` 中新增条目），或一次性 `--subject-text "<描述>"`。
- 同一批次内主体固定；要对比不同主体，用不同 batch 名重跑同 seed。

## 工作流

1. 确认 batch 名、n、seed 和可选 lock/exclude；缺省直接用默认值，不要追问。
2. 采样（确定性，纯 stdlib）：

   ```bash
   python3 .skills/yeisme/eikona-image/eikona-candid-photo-director/scripts/sample_matrix.py \
     --batch <batch> --seed 42 --n 10 \
     --out prompts/<owner>/candid-portrait/<batch>
   ```

   先加 `--dry-run` 看组合表，满意后去掉再落盘。
3. 产物遵循 `eikona-file-prompt-workflow` 约定：
   - `prompts/NN-<combo>.md`：只含提交给模型的自然语言提示，无 frontmatter。
   - `runbook.yaml`：`schema_version: eikona.batch.v1`，`matrix.prompt_files`，模型固定 `openai/gpt-5.4-image-2`。
   - `manifest.json`：采样器生成的 tags 清单，不要手写。
   - 集合 README.md 由 agent/人补充 brief、权限与审阅状态，不进 provider prompt。
4. 执行与审阅：按 runbook 走 Eikona CLI；按 tags 筛选淘汰方向后，用同 seed + 新 exclude 重采，或换新 seed。

## 采样规则

- 12 个采样维度：`expression / wardrobe / scene / moment / shot / lens / camera / composition / foreground / light / palette / state`，取值池见 [references/matrix.md](references/matrix.md)。
- **兼容约束**：机位、构图、前景、瞬间、光线与场景类别有硬约束（荷叶机位只配荷塘类场景、车厢机位只配车内场景等），采样器自动校验，违规组合直接重采。规则表见 [references/compatibility.md](references/compatibility.md)。
- **批内去重**：组合哈希（combo，sha1 前 8 位）全局唯一；`scene / camera / composition / foreground` 四维在批内强制不重复——这四维最决定画面观感。
- **tags**：每张图输出 `dim:value` 标签集与 combo 哈希，写入 manifest.json，用于审阅筛选、批间去重和淘汰方向回放。

## 提示词结构

每张候选 = 固定主体段 + 12 维采样段 + 全局约束段，模板见 [references/prompt-template.md](references/prompt-template.md)。硬规则写进每张提示词：前景必须自然侵入画面形成明显遮挡；主色块 ≤ 3—4 个；以及全部负向约束（无影楼感、无棚拍、无直视镜头、无居中人像、无过度磨皮等）。

## 不要做

- 不要手编组合或手写 manifest.json/tags——一律由 `sample_matrix.py` 生成，保证可复现。
- 不要把 seed、模型名、CLI 参数写进 prompt 文件正文。
- 不要在本技能里执行真实生成或写 run evidence；那是 cli-runtime 的职责。
- 不要把同一 seed 的批次改名重跑当新批次——combo 相同，应换 seed 或加 exclude。
