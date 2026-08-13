# 上下文来源与证据政策

## 来源优先级

| 等级 | 来源 | 可作为硬事实 | 使用规则 |
| --- | --- | --- | --- |
| 1 | current canonical owner facts | 是 | 必须绑定 current revision/version/digest |
| 2 | accepted project facts | 是 | 只在适用 scope 和 freshness 内使用 |
| 3 | adjudicated owner/human evidence | 可 | 用于 review、修复和历史结果，不覆盖更新的 canon |
| 4 | permission-safe retrieved evidence | 可 | 必须有 citation、permission snapshot、generation 和 pack digest |
| 5 | planned/candidate material | 否 | 只能标为 planned/candidate，不可提升为 confirmed |
| 6 | model memory/chat transcript | 否 | 只能作为待核实线索，不进入事实包 |

## 必须记录

- owner、source ref、project/Episode scope；
- revision/version、content digest、evidence maturity；
- permission/policy snapshot、freshness、citation；
- retrieval profile/generation 和 pack digest（若使用 RAG）；
- ignored reason、confidence 和过期条件。

## Fail-closed 状态

- `permission_denied`：不返回 excerpt，不用空结果冒充成功。
- `revoked`：移除 active item，使依赖 proposal stale。
- `stale`：要求重取 current source 或明确降级。
- `contract_mismatch`：不猜字段、不忽略未知 required contract。
- `owner_outage`：允许 `degraded_no_rag`，但不得把缓存或记忆冒充 current。
- `citation_missing`：影响决策的事实不得进入 ready pack。

## 信息最小化

- 正文、图像、视频和音频 bytes 留在 canonical owner；上下文包保存 opaque ref、摘要和必要片段。
- 不保存 raw prompt、provider payload、private tool args、凭据、signed URL 或完整思维链。
- 不把 caller 自报的 scope、owner 或 allowed ids 当作可信授权。
