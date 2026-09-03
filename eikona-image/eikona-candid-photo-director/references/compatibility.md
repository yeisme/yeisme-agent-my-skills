# 兼容约束表

采样器在 `scripts/sample_matrix.py` 中硬校验以下规则；违规组合直接重采，不进入批次。规则的唯一机器来源是 `scripts/matrix.json` 的 `requires_scene` / `palette_rules` / `lens_state_rules`。

## 维度 → 场景类别约束

| 维度 | 取值 | 允许场景 |
| --- | --- | --- |
| camera | 从巨大荷叶下方仰拍 | lotus |
| camera | 从车厢前排远距离拍 | vehicle |
| camera | 从窗外向室内拍 | window |
| camera | 贴近水面的极低机位 | water |
| composition | 荷叶形成天然圆形框景 | lotus |
| composition | 窗框式框景 | window |
| composition | 大面积水面 | water |
| foreground | 完全失焦的荷花、巨大荷叶 | lotus |
| foreground | 公交座椅、汽车玻璃 | vehicle |
| foreground | 白色窗帘、窗框 | window |
| foreground | 竹叶 | 竹林水边 |
| foreground | 芦苇 | 芦苇湖边 |
| foreground | 水面反光 | water |
| light | 窗边高反差自然光 | window |
| light | 水面反射补光 | water |
| moment | 坐在船尾发呆 | 旧木舟 |
| moment | 沿木栈道缓慢行走 | 湖边木栈道 |
| moment | 用巨大荷叶挡太阳 | lotus |
| moment | 低头洗水果 | 河边洗水果、乡间浅溪 |
| moment | 弯腰触碰水面、赤脚踩水、蹲在水边 | water |
| moment | 靠着窗边午睡 | window |
| moment | 坐在石阶边晃腿 | 湖边石阶 |

## 色彩规则

`深蓝夜色+冷白灯光` 只允许：

- 场景：便利店冰柜、城市天台、极简民宿
- 光线：窗边高反差自然光、背景高亮人物稍暗、局部过曝高光

## 焦段 ↔ 摄影状态

| state | 允许 lens |
| --- | --- |
| 远距离压缩 | 85mm压缩人像、105mm远距离偷窥感长焦 |
| 近距离广角畸变 | 24mm超广角近距离、28mm广角 |

## 扩展规则的原则

- 只为「画面会明显荒谬」的组合加硬约束；暧昧但可成立的组合交给审阅淘汰，不要过度约束导致采样空间塌缩。
- 新场景加入矩阵时，先归类到 scene_categories，再检查上表是否需要新行。
