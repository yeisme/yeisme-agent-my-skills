# ICONIC LANDMARK SERIES 视觉系统

固定系统，所有城市共享。模板正文的 canonical 归属是模板仓库 `data/yeisme-prompt-templates/solutions/image/iconic-landmark-poster`（promptrepo 解决方案包，contract 声明 33 个输入）。编译与投递只使用 `main.en.md`（en 给 agent/模型）；`main.zh-CN.md` 是人工审阅译文，不进入编译。`scripts/render_poster.py` 只负责加载模板、绑定城市 spec、变体合并与 tags，不内嵌模板正文。本文档供审阅。改视觉系统必须改模板仓库的 `main.en.md`（并用 template-registry `contract refresh` 更新 digest）并同步本文档。

## 版式

- 竖版 2:3（默认 `1024x1536`）。
- 上半 45%：真实城市摄影。下半 55%：极简二维矢量建筑解构。
- 上下两半必须表现同一组地标；hero 地标在两半中保持相似视觉轴线（默认视觉中心偏右）。

## 上半｜真实摄影

- hero 地标完整不裁切，严格保持真实建筑比例，核心识别特征逐一点名（城市 spec `photo.hero_features`）。
- 中长焦建筑摄影（50–85mm），垂直线笔直，无鱼眼、无夸张广角畸变。
- 前景水体占摄影区域 20–25%，低饱和、细波纹、轻微倒影；允许极小比例参照物（游船等），不抢主体。
- 时间默认 golden hour 转 blue hour；天空多段柔和渐变；侧后光为 hero 边缘产生细腻轮廓光。
- 远景现代建筑必须弱化。

## 下半｜矢量解构

- 背景：温暖象牙白 / 奶油白高级艺术纸张，大面积干净负空间。
- hero 解构：保留核心识别元素（spec `vector.hero_identity`），简化为矩形 + 细长竖线 + 三角形 + 尖拱 + 极细几何线条；不使用粗黑描边。
- supporting 地标横向展开，高度必须明显低于 hero。
- 巨大半透明几何圆形「太阳」置于 hero 后方偏左并被遮挡，使用柔和雾粉 / Dusty Rose / Pale Peach，不用真实太阳纹理。
- 水体抽象：一条极细基准线 + 5–7 条不同长度极细水平线（雾蓝/灰蓝/浅海军蓝）。
- 允许 ≤ 画面 1% 的极简城市彩蛋（如红色双层巴士剪影）。
- 整体是建筑设计档案感，不是旅游卡通插画。

## Typography｜建筑档案排版（槽位固定）

| 位置 | 内容 | 来源 |
| --- | --- | --- |
| 左上 | ICONIC LANDMARK SERIES — No.NNN | series.no |
| 左下 | 城市名大字两行 + 极细短横线 + 小字副标题 | typography.title / subtitle |
| 右上 | EST. + 年份 | city.est |
| 右下 | 经纬度两行 | city.coordinates |
| 最下方 | 极小字号脚注 | typography.footer |

字体：高级现代主义无衬线，细字重，加宽字距；主标题深海军蓝 / Charcoal Navy。遵循建筑事务所档案、博物馆展览图录式排版。

## 风格栈与负面词

风格栈（固定）：Swiss International Style + British modernism + Bauhaus + Mid-century travel poster + architectural editorial illustration + museum exhibition graphic design + Japanese minimalism + Scandinavian graphic design。

负面词基线（固定，英文）：cyberpunk、futuristic city、3D render、clay style、oil painting、watercolor、thick black outlines、oversaturation、heavy HDR、architectural perspective errors、dense tourists、heavy traffic、cluttered background、garbled text。城市 spec 通过 `negative_extra` 追加城市专属项（如 `London Eye stealing the subject`）。

## 系列一致性检查

新增城市时对照：分割比例未变、hero 轴线一致、排版槽位齐全、palette.family 沿用 `morandi-warm`（或显式开新家族并记录原因）、负面词基线未被删减。
