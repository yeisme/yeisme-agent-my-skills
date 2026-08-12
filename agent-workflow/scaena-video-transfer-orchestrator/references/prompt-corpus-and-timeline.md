# Scaena 视频 Prompt Corpus 与时间轴速查

## 当前可执行入口

```bash
scaena video generate \
  --project /workspaces/yeisme-agent/data/scaena-video-transfer-lab \
  --model doubao-seedance-2-0-260128 \
  --bundle <bundle-ref> \
  --media-profile <storage-profile> \
  --prompt-file prompts/scaena/video-transfer/E001-001/prompts/01-source-locked.md \
  --draw 1 \
  --candidate-only \
  --json
```

```bash
scaena video task prompt \
  --project /workspaces/yeisme-agent/data/scaena-video-transfer-lab \
  --model doubao-seedance-2-0-260128 \
  --task <task-id> \
  --verify-prompt-file prompts/scaena/video-transfer/E001-001/prompts/01-source-locked.md \
  --agent
```

## 文件布局

```text
prompts/scaena/video-transfer/<episode>-<shot-or-chunk>/
  README.md
  prompts/
    01-source-locked.md
    02-action-repair.md
```

- `README.md`：人类目标和来源说明，不提交给 provider。
- `prompts/*.md`：只包含实际 provider prompt；一个文件一个方向。
- 不把 model、task id、signed URL、credential、审批状态、训练授权或私有路径放进 prompt body。

## 时间轴硬规则

```text
HH:MM:SS.mmm --> HH:MM:SS.mmm
这一段可观察的角色、动作、镜头、遮挡、道具和禁止变化。

---

HH:MM:SS.mmm --> HH:MM:SS.mmm
下一段动作。
```

- 使用 provider clip 相对时间；源视频绝对时间留在 Scaena shot/chunk binding。
- 首段从 `00:00:00.000` 开始。
- 时间段有序、连续、无 gap、无 overlap。
- 末段结束时间等于 clip duration。
- `---` 必须独占一行，上下空一行。
- 同一块中不要写另一个时间段；角色不存在时不得上传其 reference image。

## 语料晋级

正文现在可以保存在用户项目文件并直接提交，但 Scaena corpus register/export 尚未实现。未来语料只能按以下顺序晋级：

```text
registered -> linted -> used -> reviewed -> corpus_eligible -> exported
```

`corpus_eligible` 必须同时满足：人工 accepted、rights 允许、`training_use=allowed`、清洗无 blocker、task/bundle/artifact/review lineage 完整。

训练数据采用 source/clean 双摘要：

- source digest：实际提交字节。
- clean digest：确定性清洗后文本。

清洗只允许机械变换和敏感信息替换，不默认用 LLM 改写。导出正文写独立 `.txt`，structured manifest 只保存 refs/digests/labels，不嵌入 prompt body。

## Eikona owner 边界

- Eikona 图片/storyboard/subject prompt 继续由 Eikona prompt memory/file workflow 管理。
- Scaena 只保存 `eikona://` supporting ref/digest，不复制其正文。
- Scaena 视频 timeline prompt 单独保存，绑定 shot/chunk/source video 和 Seedance task。
- planning board、clean video reference、Seedance timeline prompt 必须使用三个独立 prompt 文件。
