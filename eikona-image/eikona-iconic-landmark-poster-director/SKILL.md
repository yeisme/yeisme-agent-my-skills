---
name: eikona-iconic-landmark-poster-director
description: Use when creating ICONIC LANDMARK SERIES premium city landmark posters or covers through Eikona — vertical 2:3 art posters with a real-photography upper half and a minimalist vector deconstruction lower half of the same landmarks, archival typography, city-parameterized specs, series numbering, and namespaced tag management for cover/poster asset libraries.
---

# Eikona 城市地标海报导演（ICONIC LANDMARK SERIES）

把「上半真实摄影 + 下半矢量解构 + 建筑档案排版」的固定视觉系统参数化为城市系列海报。视觉系统不变，城市数据独立成 spec；渲染、tags、系列索引一律由脚本生成。适合高水平封面设计与系列海报资产库。落盘规范遵循 `eikona-file-prompt-workflow`，执行与 run evidence 交给 `yeisme-eikona-cli-runtime`。

## 输入

- `city`：城市 spec id（`assets/cities/<id>.json`，现有 `london`，含 base + `cover-title-space` + `blue-hour` 三个变体）。
- `aspect` / `size`：默认 2:3（`1024x1536`）。
- 新城市：复制 london.json 改内容，不需要改代码。
- 封面/构图变体：在 spec 的 `variants` 数组声明，渲染器深度合并后随基础版一起输出；合并规则与约束见 [references/city-spec.md](references/city-spec.md)。

## 工作流

1. 渲染海报提示词（确定性，纯 stdlib）：

   ```bash
   python3 .skills/yeisme/eikona-image/eikona-iconic-landmark-poster-director/scripts/render_poster.py \
     --city london --out prompts/<owner>/landmark-poster/london
   ```

2. 产物：
   - `prompts/01-<city>-<hero>.md`：完整海报提示词，无 frontmatter。
   - `runbook.yaml`：`eikona.batch.v1`，模型固定 `openai/gpt-5.4-image-2`。
   - `manifest.json`：namespaced tags + combo 哈希，脚本生成，不要手写。
3. 系列索引：新增/修改城市 spec 后运行 `render_poster.py --reindex`，重新生成 `assets/series-index.json`（编号、城市、地标、combo）。不要手工维护索引。
4. 按 runbook 走 Eikona CLI 执行；审阅淘汰后改城市 spec 重渲，combo 变化即提示词内容变化。

## 视觉系统（固定，不随城市变）

- 竖版 2:3；上半 45% 真实摄影，下半 55% 极简二维矢量解构；两半必须表现同一组地标、视觉轴线对应。
- 上半：真实旅行摄影、中长焦压缩、golden hour 质感、前景水体、弱化远景。
- 下半：象牙白艺术纸、大面积负空间、几何解构保留核心识别元素、极细线条、无粗黑描边、档案感而非卡通。
- 排版：建筑事务所档案 / 博物馆图录式；固定槽位（左上系列名、左下城市大字、右上 EST、右下坐标、底部小字）。
- 风格栈与负面词基线固定在渲染器内；城市 spec 只可追加城市专属负面词（`negative_extra`）。

详见 [references/visual-system.md](references/visual-system.md)；城市 spec 字段见 [references/city-spec.md](references/city-spec.md)。

## Tags 管理

每张海报输出 namespaced tags（`ns:value`），写入 manifest.json，用于封面/海报资产库的检索、筛选与去重：

- `series:*` / `series.no:NNN`：系列归属与编号（三位零填充）。
- `geo.city:*` / `geo.country:*`：城市与国家。
- `landmark:*`：地标，多值（hero/supporting/foreground 各一个）。
- `layout:photo-vector-split`、`aspect:2:3`：版式系统标识。
- `palette.family:*` / `palette.paper:*` / `palette.accent:*`：色彩家族与点缀色，跨城市保持一致性可审。
- `component:photography|vector-deconstruction|archival-typography`：构成组件。
- `use:cover|poster|print`：用途。
- `combo`：spec 内容哈希，批间去重与变更检测。

完整规则与扩展原则见 [references/tags.md](references/tags.md)。

## 不要做

- 不要把城市内容写进渲染器代码；城市差异只能进 `assets/cities/*.json`。
- 不要手写 manifest.json、tags 或 series-index.json——一律由 `render_poster.py` 生成。
- 不要在单城 spec 里破坏视觉系统（分割比例、排版槽位、风格栈）；要做新系统就开新技能/新系列 id。
- 系列编号 `series.no` 全系列唯一；新城市用 `--reindex` 检查冲突。
