---
name: eikona-xhs-card-series-director
description: Use when designing Xiaohongshu 3/6/9-page static card series, knowledge cards, or long-post visual breakdowns for Eikona; produce page plans, prompts, generation commands, and review handoff steps.
---

# Eikona 小红书图文卡片导演

把小红书正文拆成一组静态 3:4 图文卡片，并输出可执行、可评审、可交接的 Eikona 创作方案。

## 输入

- 笔记正文、标题、目标页数、账号风格、色彩偏好和每页信息密度。
- 可选：是否需要封面页、金句页、步骤页、总结页。

缺目标页数时默认 3 页；正文过长时先做信息分层，不把原文硬塞进图片。

## 工作流

1. 将正文拆成页序：封面、问题、步骤/清单、案例、总结和互动页。
2. 为每页写短标题和 1-3 条卡片文案，避免单页文字过密。
3. 统一视觉系统：字体风格、背景、图标、留白、颜色、安全边距和页码规则。
4. 加载 `eikona-file-prompt-workflow`，按 `prompts/xhs/card-series/<collection>/prompts/NN-<page-role>.md` 保存逐页提示词，并用 runbook 保持统一模型、尺寸和限制。
5. 输出集合 README、逐页提示词、runbook 和页码命名建议。
6. 生成后用 review packet 对比整组一致性，再用 feedback 记录被接受的页面或整组候选。

## 命令示例

输出模式：例行自动化用 `--agent`；非终态 run 用 `eikona watch <run_id> --events` 观察；脚本/CI 用 `--json --compact`（共存期内裸 `--json` 仍是 legacy full）；取证用 `--json --full`。

本地验证：

```bash
eikona run -f prompts/xhs/card-series/skincare-basics/runbook.yaml --dry-run --agent
```

真实生成：

```bash
eikona run -f prompts/xhs/card-series/skincare-basics/runbook.yaml --background --agent
eikona review packet <run_id> --agent
eikona feedback accept <run_id> --artifact <artifact_id> --reason series_consistency --reason mobile_readability --agent
eikona assets handoff <artifact_id> --agent
```

已有 promoted workflow 或多候选工作流时优先使用 workflow：

```bash
eikona workflow run -f testdata/workflows/social-card-series.yaml --background --agent
eikona worker daemon --once --max-active-runs 2 --agent
eikona review packet <run_id> --agent
```

## 输出

- 页序表：页码、标题、1-3 条正文、画面主体、版式备注。
- 统一视觉系统说明、分类目录、集合 README、逐页 prompt 文件和 runbook。
- 本地验证、真实生成、review、feedback、handoff 命令。

## 质量标准

- 每页只承载一个核心信息，不把长文塞进图片。
- 中文排版要有安全区、层级和留白。
- 不生成误导性截图、虚假聊天记录或平台界面仿冒图。
- 系列页必须在色彩、标题层级、图标风格和页码位置上保持一致。
- 模型生成的中文小字必须进入 review；不把 OCR 不可读的图当作合格产物。

## 边界

- 不编造事实、数据、步骤或案例；素材不足时输出待补信息清单。
- 不把私密正文、原始提示词、供应商载荷或完整思维链写入结构化资产。
