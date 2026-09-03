# Tags 管理规则

每张海报的 tags 由 `render_poster.py` 生成进 `manifest.json`，格式为 `ns:value` 的 namespaced 扁平列表。tags 是封面/海报资产库的检索、筛选、去重与系列治理接口；不要手写，不要事后补。

## 命名空间

| 命名空间 | 示例 | 基数 | 用途 |
| --- | --- | --- | --- |
| `series` | `series:iconic-landmark` | 1 | 系列归属；新视觉系统 = 新系列 id |
| `series.no` | `series.no:001` | 1 | 系列编号，三位零填充，全系列唯一 |
| `geo.city` / `geo.country` | `geo.city:london` | 各 1 | 按城市/国家聚合 |
| `landmark` | `landmark:big-ben` | 多 | 每个 landmark 一条；hero 在 manifest 中可由城市 spec 的 role 推断 |
| `layout` | `layout:photo-vector-split` | 1 | 版式系统标识，同系列固定 |
| `aspect` | `aspect:2:3` | 1 | 画幅 |
| `palette.family` | `palette.family:morandi-warm` | 1 | 色彩家族，跨城一致性审查 |
| `palette.paper` | `palette.paper:warm-ivory` | 1 | 纸张底色 |
| `palette.accent` | `palette.accent:dusty-rose` | 多 | 点缀色，每色一条 |
| `component` | `component:photography` 等 | 固定 3 | 构成组件：摄影 / 矢量解构 / 档案排版 |
| `use` | `use:cover` | 多 | 用途：cover / poster / print |
| `combo` | manifest 顶层字段 | 1 | spec 内容 sha1 前 8 位，去重与变更检测 |

## 治理规则

- **值用 slug**：小写、连字符，如 `palace-of-westminster`、`charcoal-navy`；不直接放中文或空格。
- **新增命名空间需升级技能**：先更新本文件与渲染器 `compute_tags`，再重渲受影响城市；不要在单个 manifest 里发明临时 tag。
- **combo 即版本指纹**：spec 任何字节变化都会改变 combo；同一 `series.no` 出现两个 combo 说明 spec 被改过，审阅时以最新渲染为准。
- **系列索引**：`assets/series-index.json` 由 `--reindex` 从全部城市 spec 重新生成，用于检查编号冲突与地标覆盖；索引不含 tags 全量（避免双源），查 tags 看各批次 manifest。
- **筛选示例**：封面候选 = `use:cover`；某地标全部海报 = `landmark:big-ben`；色彩漂移审查 = 同 `series` 下对比 `palette.family` / `palette.accent`。
