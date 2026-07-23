# Eikona Prompt Library Convention

## 分类维度

固定使用四层语义：

```text
prompts/<owner>/<asset-type>/<collection>/<artifact>
```

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| `owner` | 业务或内容 owner | `product`, `xhs`, `auctra`, `scaena`, `story`, `generic` |
| `asset-type` | 稳定的视觉用途 | `landing-hero`, `cover`, `card-series`, `subject-candidate`, `storyboard`, `image-edit` |
| `collection` | 一个可共同评审的主题或交付单元 | `local-first-cli`, `summer-launch`, `brief-123`, `shot-042` |
| `artifact` | 集合索引、runbook 或候选 prompt | `README.md`, `runbook.yaml`, `prompts/01-clean-editorial.md` |

不要把 `openai`, `gateway`, `gpt-image-2`, `2026-07-17` 或个人姓名作为稳定顶层分类。provider、模型、尺寸、并发和成本属于 runbook；时间、作者和状态属于集合 README。

## 推荐目录

```text
prompts/
└── product/
    └── landing-hero/
        └── local-first-cli/
            ├── README.md
            ├── runbook.yaml
            ├── prompts/
            │   ├── 01-clean-editorial.md
            │   ├── 02-technical-diagram.md
            │   └── 03-cinematic-workspace.md
            └── references/
                └── README.md
```

常用 owner/asset-type：

- `product/landing-hero`, `product/feature-illustration`, `product/social-card`, `product/empty-state`, `product/docs-illustration`
- `xhs/cover`, `xhs/card-series`, `xhs/infographic`, `xhs/comic`
- `story/storyboard`, `story/location`, `story/prop`, `story/style`
- `scaena/subject-candidate`, `scaena/wardrobe`, `scaena/location`, `scaena/prop`, `scaena/style`, `scaena/correction`
- `auctra/brief-visual`, `auctra/character`, `auctra/location`, `auctra/cover`
- `generic/image-generate`, `generic/image-edit`, `generic/variation`

## 文件职责

### `README.md`

保存人类审阅信息，不提交给 provider：

- owner、asset type、collection goal
- source refs、权限、accepted/frozen/preflight 状态
- 目标平台、尺寸、交付路径、禁用项
- 候选清单和状态
- review/feedback/handoff 记录链接或 ID

### `prompts/*.md`

只保存会提交给图像模型的自然语言内容。可以使用 Markdown 标题组织目标、主体、构图、风格、文字安全区和禁用项，但不要使用 YAML frontmatter 或结构化运行 metadata。

命名使用两位序号和方向名：

```text
01-clean-editorial.md
02-bold-geometric.md
03-warm-lifestyle.md
```

### `runbook.yaml`

保存模型、尺寸、候选展开、reference images、限制和审批策略。prompt 路径相对于 runbook 解析，因此推荐使用 `prompts/<file>.md`。

## 候选拆分规则

新建文件，而不是继续扩大同一个 prompt，当变化涉及：

- 构图方向明显不同。
- 媒介或风格方向明显不同。
- 主体、地点或叙事时刻不同。
- planning board 与 clean video reference 不同。
- 有标记版与无标记版不同。

保留同一文件并修订，当变化只是：

- 更明确的光线、材质或镜头词。
- 修复文字安全区、边缘、比例或禁用项。
- 根据已记录 feedback 收紧同一视觉方向。

## 迁移长命令

把：

```bash
eikona generate --model openai:gpt-image-2 --prompt "<long prompt>" --json
```

迁移为：

```bash
eikona generate --model openai:gpt-image-2 --input prompts/<owner>/<asset-type>/<collection>/prompts/01-<direction>.md --json
```

迁移时不要把 shell 转义符、命令参数、模型名或 `--set` provider options 写进 prompt 文件。
