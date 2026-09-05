# 城市 Spec 字段说明

每个城市一个 `assets/cities/<id>.json`，`schema_version: iconic-landmark-city/1.0`。新增城市 = 复制 `london.json` 修改，然后 `render_poster.py --reindex`。所有结构化字段由 agent/人编辑 spec（属于源内容），manifest 与系列索引由脚本生成。

## 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 城市 slug，小写，如 `london`、`paris`；用于 tags 与输出路径 |
| `series.id` / `series.no` | string / int | 系列标识与编号；编号全系列唯一，渲染时三位零填充 |
| `city.name` / `city.country` | string | 大写英文，进排版与 tags |
| `city.est` | string | 右上角 EST. 年份，通常取 hero 地标建成年 |
| `city.coordinates` | string[] | 右下角经纬度两行 |
| `landmarks[]` | object[] | `id`（进 tags）、`name`（进提示词）、`role`：`hero` 恰好一个，`supporting` / `foreground` 若干 |
| `tags.palette` | object | `family` / `paper` / `accents[]`，进 tags；家族默认 `morandi-warm` |
| `tags.use` | string[] | 用途 tags，如 `cover`、`poster`、`print` |
| `photo.*` | string / string[] | 上半摄影全部细节，字段即模板槽位；见 london.json 示例 |
| `vector.*` | string / string[] | 下半矢量解构细节：`hero_identity`、`hero_simplification`、`hero_palette`、`supporting`、`supporting_palette`、`sun`、`river`、`easter_egg`、`feel` |
| `typography.title` | string[] | 两行大写主标题，如 `["LONDON", "BIG BEN"]` |
| `typography.subtitle` / `typography.footer` | string | 副标题与底部脚注 |
| `negative_extra` | string[] | 城市专属负面词，追加到固定基线之后 |
| `variants` | object[] | 可选。封面/构图变体：`id`（slug，进 tags 与文件名）、`label`（审阅用中文说明）、`overrides`（按顶层字段深度合并到基础 spec） |

## 变体（variants）

- 变体与基础版共享视觉系统和系列编号，只通过 `overrides` 改差异字段；不要复制整份 spec。
- 合并规则：dict 递归合并；数组与标量整体替换；唯一例外是 `negative_extra` 数组按追加合并（变体只写新增负面词）。
- 每个变体独立 combo 哈希与 `variant:<id>` tag；基础版 tag 为 `variant:base`。
- 变体必须遵守视觉系统（分割比例、排版槽位、风格栈不变）；`overrides` 不该触碰 `series`、`id`。典型用途：封面刊头留白、时段/色调版本、彩蛋开关。
- 渲染输出文件名：`01-<city>-<hero>.md`（base），`NN-<city>-<hero>-<variant-id>.md`（变体按声明顺序编号）。

## 写作要点

- `photo.hero_features` 与 `vector.hero_identity` 是同一地标的两种表达：前者点明真实摄影要表现的特征，后者列出矢量解构必须保留的识别元素——两者必须对应，这是「上下严格对应」的来源。
- `photo` 各字段写具体、可验证的描述（视点、占比、色名、镜头参数），不要写抽象风格词；风格词已在固定风格栈里。
- 彩蛋（`easter_egg`）必须与该城市真实相关，且写明面积上限。
