## 命令骨架

普通 Eikona 文件生成（现有 GPT Image 网关，2.5 高质量）：

```bash
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --size 2048x1152 --aspect 16:9 --quality high --input prompts/story/storyboard/scene/prompts/01-planning-board.md --dry-run --agent
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --size 2048x1152 --aspect 16:9 --quality high --input prompts/story/storyboard/scene/prompts/01-planning-board.md --agent
eikona review packet <run_id> --agent
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --agent
eikona assets handoff <artifact_id> --agent
```

直接从提示词文件出图：

```bash
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --input prompts/product/landing-hero/launch/prompts/01-clean-editorial.md --size 2048x2048 --aspect 1:1 --quality high --dry-run --agent
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --input prompts/product/landing-hero/launch/prompts/01-clean-editorial.md --size 2048x2048 --aspect 1:1 --quality high --agent
```

从提示词集合批量出图。runbook 中使用 `defaults.prompt_file`、`jobs[].prompt_file` 或 `matrix.prompt_files` 引用 `prompts/*.md`；先验证计划，再执行：

```bash
eikona run -f prompts/product/landing-hero/launch/runbook.yaml --dry-run --agent
eikona run -f prompts/product/landing-hero/launch/runbook.yaml --background --agent
eikona watch <run_id> --events
```

网关首次接入：

```bash
eikona init --user --agent
eikona auth check gateway --agent
eikona projects register . --agent
```

Auctra 来源必须先走 brief/export/import：

```bash
auctra visual brief <unit-id> --profile short_video_storyboard --json
auctra review accept <review_item_id> --json
auctra visual export-brief <brief-id> --for eikona --to .auctra/exports/<brief-id>.json --json
eikona workflow import auctra -f .auctra/exports/<brief-id>.json --out .eikona/workflows/<brief-id>.workflow.yaml --agent
```

