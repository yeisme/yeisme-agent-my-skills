---
name: eikona-auctra-visual-router
description: Use when turning Auctra content, accepted drafts, novel/context material, or creator-brand notes into Eikona image workflows; route through Auctra visual briefs, Eikona workflow import/run/review, and Auctra handoff import without making Auctra own provider execution.
---

# Eikona x Auctra 图文创作路由器

把 Auctra 的文字、素材、小说设定或创作者笔记转成 Eikona 可执行的视觉工作流，并把产物交回 Auctra 的 visual candidate/review 链路。

## 输入

- Auctra content unit ID、标题、正文版本、素材引用、目标平台和视觉用途。
- 可选：期望 profile、页数、参考图、禁用元素、是否只做本地 fixture 验证。

如果没有 content unit ID，先从当前 Auctra 项目列出或提取候选；仍无法确定时只问一个最小澄清问题。

## Profile 路由

- 小红书图文卡片：`xhs_card_series`，可交给 `eikona-xhs-card-series-director` 做页序和视觉质量建议。
- 微信封面：`wechat_cover`。
- 产品测评信息图：`product_review_infographic`，可交给 `eikona-xhs-infographic-director` 调整事实层级。
- 教程信息图：`tutorial_infographic`。
- 小说角色设定图：`novel_character_sheet`。
- 短视频分镜：`short_video_storyboard`。

## 工作流

1. 确认 Auctra 内容已有 accepted content version；没有时先让用户完成内容 review，不直接生成图。
2. 创建 visual brief，并让用户或 agent 明确 review：

```bash
auctra visual brief <unit-id> --profile <profile> --json
auctra review accept <review_item_id> --json
```

3. 导出给 Eikona：

```bash
auctra visual export-brief <brief-id> --for eikona --to .auctra/exports/<brief-id>.json --json
```

4. 在 Eikona 导入、验证和运行。默认真实远程模型是 `openai:gpt-image-2`；本地验证可用 fixture workflow 或 dry run。

```bash
eikona workflow import auctra -f .auctra/exports/<brief-id>.json --out .eikona/workflows/<brief-id>.workflow.yaml --json
eikona workflow validate -f .eikona/workflows/<brief-id>.workflow.yaml --json
eikona workflow run -f .eikona/workflows/<brief-id>.workflow.yaml --background --json
eikona worker daemon --once --max-active-runs 2 --json
eikona review packet <run_id> --json
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --json
```

5. 产物交回 Auctra：

```bash
auctra visual import-handoff --brief <brief-id> --from <eikona-handoff.json> --json
auctra visual accept <asset-id> <candidate-id> --json
```

## 输出

- 选择的 profile 和理由。
- Auctra brief/review/export 命令。
- Eikona import/validate/run/review/feedback 命令。
- Auctra import-handoff/accept 下一步。

## 质量标准

- Auctra 只负责内容上下文、brief、review 和 candidate 接收；Eikona 负责 provider workflow、run evidence、review packet、feedback 和 artifact handoff。
- 所有 agent 消费都使用 `--json` 或 `--agent`，不解析 human output。
- 不把原始提示词、供应商载荷、私密素材或完整思维链写入结构化资产。
- 不新增 Eikona 默认图像模型；真实远程示例使用 `openai:gpt-image-2`。

## 边界

- 不直接调用 provider SDK。
- 不跳过 Auctra review gate 导出 brief。
- 不把 Eikona run 目录路径硬写进 Auctra 内容正文；通过 handoff JSON 导入候选。
