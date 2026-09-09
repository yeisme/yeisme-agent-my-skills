# Eikona 主体资产包参考

## Candidate pack

下表用于已经选择“可复用主体包”的任务，不是所有做剧请求的起步清单。快速 demo 的最小包是每人一张同服装全身单视图、一个多人开场构图及当前动作所需道具。透明输出、六视图、表情和拆层仅在本轮交付需要时成为硬要求；模板有这些槽位不代表全部必做。

人工定妆三视图可呈现同一人物的正/侧/背面；它是审阅用途。进入图像或视频生成前优先选清晰单视图，按实际身份人数绑定。多人开场图须验证人数、身份对应、接触关系、道具持有者、门桌拓扑和行动通路。短动作测试通过后再扩展完整时长，仍遵守Scaena当前准入要求。

| Kind | Minimum candidate roles |
| --- | --- |
| Primary character | front、three-quarter、profile、full-body、neutral、core expressions、default wardrobe |
| Secondary character | front/three-quarter、full-body、neutral、one core expression、default wardrobe |
| Recurring location | establishing、reverse、layout、detail、time/light variant |
| Story-critical prop | orthographic/three-quarter、scale reference、material/detail、marking |
| Wardrobe | front/full-body、material/color detail、silhouette、continuity segment |
| Project style | palette、render language、lighting/camera anchors、forbidden drift examples |

## Reference roles

```text
identity_anchor
wardrobe_anchor
style_anchor
location_layout_anchor
prop_geometry_anchor
source_asset
correction_preserve
```

记录 role 和顺序；不要只保存一个无语义的 reference list。

## Review dimensions

```text
identity
face_hair
silhouette
wardrobe
location_layout
prop_geometry
style_adherence
view_completeness
obvious_artifacts
rights
```

每个维度输出 `pass|warn|fail|missing_input` 与 evidence ref。不得根据平均分自动接受。

## Correction types

- identity drift：保留 composition/location/camera，修复 face/hair/silhouette。
- wardrobe drift：保留 identity/pose/location，修复 frozen wardrobe variant。
- location drift：保留 subject/action/camera intent，修复 layout anchors。
- prop drift：保留 subject/shot，修复 geometry/scale/material/marking。
- style drift：保留 subject identity/shot staging，修复 project style anchors。

Correction 输出永远是 derived candidate，不能覆盖 source artifact。
