# Continuity and Evidence Reference

连续性检查必须能回到可复核的事实和 artifact evidence，而不是“看起来差不多”。

## Minimum evidence

每个 finding 至少关联：

- source refs：CanonSnapshot、SubjectVersion、StyleVersion、Scene/Shot refs；
- artifact ref：artifact id、digest、owner、生成/导入 receipt；
- check：检查维度、适用镜头、结论和 `pass/warn/block/unknown/stale`；
- freshness：读取时的 revision/version/digest 和 stale reason；
- next action：repair proposal、重新生成、人工确认或停止。

## Blocking dimensions

主体身份、服装/伤口、关键道具、空间位置、时间顺序、动作方向、光线、声音、字幕时间和 reference version 任一无法确认或发生冲突，都不能被当作 pass。

## Redaction

证据可以保留结论、短摘要、指标、artifact digest 和引用路径，但不得写 raw prompt、provider payload、凭据、私有工具参数或完整 chain-of-thought。

连续性结论只提供 finding/evidence/proposal。`production_accepted` 与 delivery 仍由 Scaena 的状态闸门决定。
