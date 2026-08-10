---
name: eikona-xhs-visual-router
description: Use when routing Xiaohongshu static visual asset requests for Eikona, including covers, card series, infographics, and comic-style posts; keep generation on Eikona workflow, review, feedback, and handoff contracts.
---

# Eikona 小红书视觉路由器

判断小红书静态图需求，选择最小的视觉导演 skill，并保持 Eikona 的证据链：brief -> prompt/run -> review packet -> feedback -> handoff。超宽连续空间故事看板不在本 router 内处理，应交给 `eikona-ultrawide-storyboard-director`。

## 输入

- 笔记标题、正文要点、目标读者、账号调性、禁用元素和期望页数。
- 可选：产品图、人物/场景参考图、品牌色、是否需要真实摄影感或漫画感。

缺标题、正文要点或目标读者时，先提取已有信息；仍不足以决定视觉类型时，问一个最小澄清问题。

## 工作流

1. 判断视觉类型：封面图、3/6/9 图文卡片、信息图、漫画风格图文。
   - 如果用户要的是 3:1 超宽剧情走位、动作调度、短剧预演、战役推演或转视频参考图，停止本路由并交给 `eikona-ultrawide-storyboard-director`。
2. 将封面交给 `eikona-xhs-cover-director`，图文卡片交给 `eikona-xhs-card-series-director`，信息图交给 `eikona-xhs-infographic-director`，漫画图文交给 `eikona-xhs-comic-director`。
3. 同时加载 `eikona-file-prompt-workflow`，要求导演输出：视觉 brief、`prompts/xhs/<asset-type>/<collection>/` 分类目录、2-3 个候选文件、runbook、review/feedback/handoff 下一步。
4. 本地验证优先用 `fixture:image`；真实远程生成默认用 `openai/gpt-5.4-image-2`，短别名仅用于兼容输入。
5. 生成后必须通过 `review packet` 和 `feedback` 记录选择，不让 agent 只凭主观文字宣称“最佳”。

## 命令示例

本地验证：

```bash
eikona generate --model fixture:image --aspect 3:4 --size 1024x1536 --input prompts/xhs/cover/skincare-morning/prompts/01-clean-lifestyle.md --dry-run --json
```

真实生成：

```bash
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --aspect 3:4 --size 1024x1536 --input prompts/xhs/cover/skincare-morning/prompts/01-clean-lifestyle.md --json
eikona review packet <run_id> --json
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --json
eikona assets handoff <artifact_id> --agent
```

已有 promoted workflow 时优先走工作流：

```bash
eikona workflow run -f testdata/workflows/xhs-cover.yaml --background --agent
eikona worker daemon --once --max-active-runs 2 --agent
eikona review packet <run_id> --json
```

## 输出

- 选择的 director skill 和选择理由。
- 视觉 brief：目标、主体、构图、文案安全区、风格、禁用项。
- 分类 prompt 目录、集合 README、候选文件、runbook、Eikona 执行命令和 review/feedback/handoff 下一步。

## 边界

- 只处理静态图，不处理视频、动效、发布或平台账号操作。
- 不上传权限不明的参考图；未知权限只能做本地说明或要求用户确认来源。
- 不把原始提示词、供应商载荷、私密素材或完整思维链写入结构化资产。
