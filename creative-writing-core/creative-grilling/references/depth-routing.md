# 自适应访谈深度

## Depth 值

| Depth | 适用范围 | 覆盖要求 |
| --- | --- | --- |
| `quick` | 单一、可逆、projectless artifact | 通常一至两轮，只问会改变方向或返工成本的决策；其余转为未决项 |
| `standard` | 默认；一个完整 phase 或已有项目中的一个 artifact | 覆盖当前 phase 的目标、范围、canon、验证和 handoff |
| `deep` | 跨阶段、长篇、跨媒介、rights 风险、跨 owner、付费生产或用户明确要求 | 逐 phase 运行独立 frontier，每个 phase 单独确认，不一次展开完整生产链 |

轮次是指导值，不设置问题数量硬上限。问题过多时先缩小 `target_artifact`，而不是截断关键分支。

## 选择顺序

1. 用户显式指定 `quick|standard|deep` 时直接采用。
2. 出现跨 owner、canonical mutation、rights/改编、付费生产、长篇/多集扩张时选择 `deep`。
3. 已有项目或需要覆盖一个完整 phase 时选择 `standard`。
4. 其他单一、可逆、projectless 请求选择 `quick`。

用户说“收束、先到这里、接受当前不确定性”时立即停止扩展 frontier，并把剩余节点写入 brief。

