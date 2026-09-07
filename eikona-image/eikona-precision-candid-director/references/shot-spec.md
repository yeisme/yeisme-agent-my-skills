# Shot Spec 字段说明

每个镜头一个 `assets/shots/<id>.json`，`schema_version: precision-candid-shot/1.0`。新增镜头 = 复制现有 spec 修改。spec 由 agent/人编辑（源内容）；manifest 与 runbook 由脚本生成。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 镜头 slug，进 tags 与文件名 |
| `label` | string | 中文审阅说明，不进提示词 |
| `aspect` / `orientation` | string | 如 `9:16` / `Vertical` |
| `genre` | string | 可选。体裁短语，默认 `candid lifestyle photo`；非抓拍镜头用对应体裁，如 `ultra-realistic high-definition close-up portrait photograph` |
| `subject.id` / `pronoun` | string | 主体 slug 与英文代词（She/He/They） |
| `subject.description` | string | 主体外观一句话，须写明 adult |
| `subject.pose` / `expression` | string | 姿势与表情；description 以主体名词收尾时 pose 用分词形式（bending/lying/turning…）；description 以其他名词/形容词收尾时 pose 改用 `as she …` 从句，避免分词悬空 |
| `subject.wardrobe` | string | 服装完整描述 |
| `sections` | object[] | 可选。`{heading, body}` 分区段落（如 Eye makeup / Hair / Hands / Nails），渲染为服装句后的独立段落 |
| `camera.position` | string | 量化机位描述，如 `slightly above eye level and extremely close to her face`；与 `height` 二选一 |
| `camera.height` | string | 带单位的量化机位，如 `about 55 cm from the mattress`；与 `position` 二选一 |
| `camera.lens` | string | 焦段，如 `35mm`、`20mm wide angle`（slug 化后进 tag `lens:*`） |
| `camera.perspective` | string | 可选。透视说明，如 `strong perspective distortion` |
| `camera.framing` | string | 占幅比 + 裁切位置，如 `subject occupies about 68% of the frame, cropped from upper thighs upward` |
| `foreground` | object | 可选。`elements` / `coverage`，前景物与遮挡百分比 |
| `light.key` / `light.fill` | string | 主光/辅光，含方向与角度；fill 可省略（单光源） |
| `light.temperature` | string | 色温 slug，如 `mixed-warm-cool`、`direct-flash`（进 tag） |
| `palette` | object[] | 可选。`{color, pct}` 有序列表，pct 合计 100；首项为 `palette.primary` tag |
| `palette_text` | string | 可选。无百分比时的自由色表（如 `black, ivory white, pearl white`）；与 `palette` 二选一 |
| `background` | string | 可选。环境描述一句，渲染时首字母大写独立成句 |
| `fingerprints` | string[] | 可选。场景指纹：让画面可信的 3 个左右生活细节，每条进 tag |
| `atmosphere` | string | 氛围短句 |
| `quality` | string[] | 质感尾词（skin texture、grain、景深等） |
| `negative` | string[] | 负向词，渲染为 `no X, no Y` |
| `tail` | string[] | 可选。负向词之后的收尾词，如 `photorealistic` |
| `tags.use` / `tags.mood` | string[] | 用途与情绪 tags |
| `tags.theme` | string[] | 可选。主题/资产类 tags，如 `ethnic-minority`、`mountains`、`night`（怪谈、地域、时段类资产归类用） |

## 量化语言约定

- 数字是本风格的交付物：cm、%、degrees 直接进提示词，禁止改成 "slightly" / "some" 这类模糊词。
- 色块百分比必须合计 100，按占比降序排列；无量化色板的镜头可省略 `palette`（如直闪夜景）。
- 前景遮挡必须带百分比（`coverage`），与抓拍矩阵技能的「前景侵入」硬规则同源；无前景的镜头可省略 `foreground`。
- 场景指纹选「该场景真实会有、但摆拍会漏掉」的细节；3 个左右，不要超过 5 个。

## Tags 规则

命名空间：`style` / `shot` / `aspect` / `subject` / `lens` / `light.temperature` / `palette.primary` / `fingerprint` / `use` / `mood` + manifest 顶层 `combo`。值一律英文 slug。完整色板（含 pct）只作为数据存 manifest，不摊进 tag 列表。
