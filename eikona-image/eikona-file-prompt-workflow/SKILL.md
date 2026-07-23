---
name: eikona-file-prompt-workflow
description: Use when creating, organizing, reviewing, or executing Eikona image prompts stored as Markdown or text files, including categorized prompt libraries, reusable prompt collections, candidate directions, runbooks with prompt_file or prompt_files, and migration away from long inline --prompt commands.
---

# Eikona 文件提示词工作流

把提示词作为可审阅、可分类、可版本化的文档管理，再通过 Eikona CLI 从文件生成。不要把长提示词长期保存在 shell 历史、聊天记录、provider 配置或 run evidence 中。

## 职责

- 本技能负责提示词目录、命名、prompt 文档、集合索引、runbook 和文件驱动执行。
- 视觉内容由匹配的 Eikona director 负责；本技能不替代产品、小红书、主体资产、Auctra 或故事看板导演。
- CLI schema、provider、provenance 和 run evidence 问题交给 `yeisme-eikona-cli-runtime`。

## 先读资料

创建或整理提示词库前读取：

- `references/prompt-library-convention.md`

需要新建集合时，从 `assets/templates/` 复制并替换模板；不要直接运行仍含占位符的文件。

## 工作流

1. 确认 owner 和 asset type；不要按 provider 或模型分类。
2. 建立 `prompts/<owner>/<asset-type>/<collection>/`。
3. 将 brief、来源、权限和交付说明写入 `README.md`，不要写进 provider prompt。
4. 将每个候选方向写入独立的 `prompts/NN-<direction>.md`；正文只放可提交给模型的自然语言提示。
5. 单个候选使用 `generate --input`；多个候选使用同目录 `runbook.yaml` 的 `matrix.prompt_files` 或 `jobs[].prompt_file`。
6. 先用 `fixture:image` 或 `--dry-run` 验证路径和展开结果，再批准真实 provider run。
7. 通过 `review packet`、`feedback` 和 `assets handoff` 完成证据链；不要手改 run-owned snapshot 或 `prompt_sources.json`。

## 单文件生成

```bash
eikona generate \
  --model fixture:image \
  --input prompts/product/landing-hero/local-first-cli/prompts/01-clean-editorial.md \
  --size 1536x1024 \
  --dry-run \
  --json

eikona generate \
  --model openai:gpt-image-2 \
  --input prompts/product/landing-hero/local-first-cli/prompts/01-clean-editorial.md \
  --size 1536x1024 \
  --json
```

`--input` 与 `--prompt` 互斥。文件路径必须指向一个普通文件，不能指向目录或集合 README。

## 集合生成

```bash
eikona run \
  -f prompts/product/landing-hero/local-first-cli/runbook.yaml \
  --dry-run \
  --json

eikona run \
  -f prompts/product/landing-hero/local-first-cli/runbook.yaml \
  --background \
  --json
```

- `defaults.prompt_file`：所有普通 job 共享一个基础 prompt 文件。
- `jobs[].prompt_file`：每个命名 job 使用一个指定文件。
- `matrix.prompt_files`：同一模型、尺寸和策略逐个展开候选文件。
- 同一 source level 的 `prompt`、`prompt_file`、`prompt_ref` 互斥。
- prompt 和 reference image 路径都相对于 runbook 所在目录解析。

## 输出契约

一次文件提示词任务至少输出：

- 分类路径和选择理由。
- `README.md` 集合索引。
- 一个或多个 `prompts/*.md` 文件。
- 多候选时的 `runbook.yaml`。
- dry-run 命令与结果摘要。
- 真实生成、review、feedback、handoff 下一步。

## 边界

- 不在 prompt 文件中放 API key、provider payload、run ID、成本、审批状态、隐藏系统提示或完整思维链。
- 不把未接受的 Auctra canon、未冻结的 Scaena production subject 或权限不明素材写入可执行 prompt。
- 不用模型名、日期或临时人员姓名作为顶层分类；模型和尺寸属于 runbook，日期可写入集合 README。
- 不把多个候选拼进一个超长 prompt 文件；一个文件只表达一个可比较方向。
- 不直接编辑 Eikona 生成的 run evidence、snapshot、queue、manifest 或 batch plan。

## 验证

- prompt 文件不含未替换的 `<...>` 占位符。
- runbook 中引用的文件存在，且路径相对于 runbook 正确。
- `eikona run -f <runbook> --dry-run --json` 成功并展开预期 job 数。
- 真实远程示例和新默认使用 `openai:gpt-image-2`。
