# 兼容约束表

采样器在 `scripts/sample_matrix.py` 中硬校验以下规则；违规组合直接重采，不进入批次。规则的唯一机器来源是 `scripts/matrix.json` 的 `requires_scene` / `palette_rules` / `lens_state_rules`。取值一律英文。

## 维度 → 场景类别约束

| 维度 | 取值 | 允许场景 |
| --- | --- | --- |
| camera | low-angle shot from beneath giant lotus leaves | lotus |
| camera | long-distance shot from the front of the carriage | vehicle |
| camera | shooting indoors from outside the window | window |
| camera | extremely low angle near the water surface | water |
| composition | lotus leaves forming a natural circular frame | lotus |
| composition | window-frame framing | window |
| composition | large expanse of water | water |
| foreground | fully defocused lotus flowers、giant lotus leaves | lotus |
| foreground | bus seats、car window glass | vehicle |
| foreground | white curtains、window frame | window |
| foreground | bamboo leaves | waterside bamboo grove |
| foreground | reeds | reed-lined lakeshore |
| foreground | water-surface glare | water |
| light | high-contrast natural window light | window |
| light | fill light reflected off water | water |
| moment | sitting at the stern, daydreaming | old wooden boat |
| moment | walking slowly along the boardwalk | lakeside wooden boardwalk |
| moment | shading herself with a giant lotus leaf | lotus |
| moment | looking down while washing fruit | washing fruit by the river、shallow countryside stream |
| moment | bending over to touch the water、stepping into water barefoot、crouching by the water | water |
| moment | napping against the window | window |
| moment | sitting on stone steps, swinging her legs | lakeside stone steps |

## 色彩规则

`deep blue night + cool white lamplight` 只允许：

- 场景：convenience-store freezer aisle、city rooftop、minimalist guesthouse
- 光线：high-contrast natural window light、bright background, subject slightly darker、partially overexposed highlights

## 焦段 ↔ 摄影状态

| state | 允许 lens |
| --- | --- |
| long-distance compression | 85mm compressed portrait、105mm distant voyeuristic telephoto |
| close-range wide-angle distortion | 24mm ultra-wide close range、28mm wide angle |

## 扩展规则的原则

- 只为「画面会明显荒谬」的组合加硬约束；暧昧但可成立的组合交给审阅淘汰，不要过度约束导致采样空间塌缩。
- 新场景加入矩阵时，先归类到 scene_categories，再检查上表是否需要新行。
