# Production Constraints Reference

生产约束先于生成调用和软评分。未知不是允许，过期不是通过。

## Constraint dimensions

至少检查以下维度，并为每项保留 `allowed`、`blocked`、`unknown` 或 `stale` 状态：

- `cost`：单次、单镜头、单集和累计预算，包含重试上限；
- `rights_privacy`：人物肖像、参考图、版权、隐私和发布权限；
- `provider_capability`：模型、额度、尺寸、时长、并发和工具能力；
- `quality_continuity`：主体、风格、动作、空间、字幕和音画约束；
- `human_review`：需要谁确认、确认什么、确认有效期；
- `delivery`：目标格式、时长、分辨率、字幕和交付位置。

## Admission order

1. 读取当前 CanonSnapshot、ProductionConstraintProfile 和 capability receipt。
2. 先执行 zero-call admission；任何 cost、rights、permission 或 capability 的 `unknown` 都返回 `needs_input` 或 `cost_reconfirm`。
3. 冻结 retry budget、kill switch、超时和 late-result 处理方式。
4. 只有 admission 通过后，才允许 Eikona/其他 provider 产生外部调用。
5. 生成后仍需通过 continuity、human review、production acceptance 和 delivery gate；高分不能跳过这些闸门。

约束不是第二套数据库。实际权限、额度和生产状态由 Owner service 发布，Skill 只读取并解释其 refs。
