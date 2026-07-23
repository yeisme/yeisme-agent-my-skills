# Scaena 主体资产就绪门

## Production gate matrix

| 对象 | 必须满足 | 允许的 non-production 例外 |
| --- | --- | --- |
| Project style | 唯一 active frozen version、rights、forbidden drift | `look_development` |
| Primary character | accepted source、完整 identity sheet、default wardrobe、human freeze | `subject_candidate` |
| Secondary character | accepted source、轻量 identity sheet、首次出现前 freeze | 远景一次性角色可按规则降为 background |
| Background character | frozen archetype/style、rights、`ephemeral=true` | 仅无名字、无特写、无持续台词、无跨镜复用 |
| Recurring location | establishing/reverse/layout/detail anchors、frozen version | 一次性非 establishing 背景 |
| Story-critical prop | geometry、scale、material、marking、rights、frozen version | shot 显式标记 incidental/no-prop |
| Wardrobe | subject、continuity segment、color/material/silhouette frozen variant | background archetype wardrobe |

## Stable blockers

| Code | Repair direction |
| --- | --- |
| `SUBJECT_SOURCE_UNACCEPTED` | 回到 Auctra accepted source/visual brief |
| `SUBJECT_BRIEF_MISSING` | 建立主体 visual brief |
| `SUBJECT_VERSION_NOT_FROZEN` | 生成候选并执行 Scaena human freeze |
| `STYLE_PACK_NOT_FROZEN` | 审阅并冻结 project style |
| `WARDROBE_VARIANT_NOT_FROZEN` | 补齐 continuity wardrobe variant |
| `SHOT_SUBJECT_BINDING_MISSING` | 绑定 exact frozen versions |
| `GENERATION_PREFLIGHT_REQUIRED` | 创建 production preflight |
| `GENERATION_PREFLIGHT_STALE` | 按 current versions 重建 preflight |
| `REFERENCE_CAPABILITY_MISSING` | 更换支持 reference bundle 的 model/plan |
| `CONSISTENCY_REVIEW_REQUIRED` | 执行 human consistency decision |
| `BACKGROUND_EXCEPTION_INVALID` | 提升为 secondary subject 并建立资产包 |
| `LEGACY_SUBJECT_STATE_UNVERIFIED` | 重新 review/freeze，不 grandfather |

## Character pack minimum

Primary：front、three-quarter、profile、full-body、neutral/core expressions、face/hair/body/silhouette anchors、default wardrobe、allowed variation、forbidden drift、source/rights/review/version/digest。

Secondary：front/three-quarter、full-body、neutral + core expression、identity anchors、default wardrobe、forbidden drift、source/rights/review/version/digest。

## Acceptance authority

```text
Auctra accepted source != Eikona accepted candidate
Eikona accepted candidate != Scaena frozen subject version
Scaena frozen subject version != accepted shot asset
machine assessment pass != human acceptance
```
