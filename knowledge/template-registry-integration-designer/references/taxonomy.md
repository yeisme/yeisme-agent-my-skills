# Tags 与能力

Tags 用于发现和筛选，capabilities 用于兼容性，document required capabilities 用于具体 role 准入。三者不要混用。

## Solution tags

优先使用稳定英文 namespace：

- `job:`：`generate`、`summarize`、`analyze`、`transform`、`review`、`plan`、`edit`。
- `artifact:`：`cover_image`、`storyboard`、`shot_video`、`edit_plan`、`research_brief`、`prompt_package`。
- `modality:`：`text`、`image`、`video`、`audio`、`document`、`code`、`multimodal`。
- `scenario:`：稳定使用场景，如 `product_marketing`、`ai_drama`、`meeting`。
- `stage:`：`briefing`、`prompt_generation`、`asset_generation`、`review`、`delivery`。
- `constraint:`：`source_grounded`、`character_consistency`、`text_legibility`、`rights_review`。
- 可选：`platform:`、`audience:`、`use:`、`workflow:`。

不要用 `eikona`、`scaena` 等项目名作为唯一 job/tag；同一模板应能由 capability 和 artifact 被其它消费者发现。

```bash
template-registry solution tag set --repository ./prompt-templates --package image --id product-campaign --tag job:generate --tag artifact:cover_image --tag modality:image --tag scenario:product_marketing --tag constraint:text_legibility --json
```

## Solution capabilities

使用 provider-neutral、lower snake case 名称，表达粗粒度可消费能力，例如 `image`、`generation`、`visual`、`structured_output`、`source_mapping`、`storyboard`、`audio`、`editing_plan`。

```bash
template-registry solution capability set --repository ./prompt-templates --package image --id product-campaign --capability image --capability generation --capability visual --json
```

## Role required capabilities

多角色方案在 document descriptor 上声明该 role 真正需要的能力，不把所有角色要求合并到 solution：

```bash
template-registry document capability set --repository ./prompt-templates --package video --id campaign-production --role shot-prompt --locale en --capability image_generation --capability asset_reference_binding --json
```

Replace-all 命令要求给出完整列表。确实需要清空时使用 `--clear`。metadata 改动后运行 catalog build/validate，并检查目标消费者 fail-closed 准入。
