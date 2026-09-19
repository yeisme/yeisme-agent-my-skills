---
name: creative-grilling
description: Use when an explicitly requested creative interview needs the shared dependency-aware Frontier protocol, adaptive depth, fact/decision/hypothesis separation, or CreativeDecisionBrief contract across novel, manga-drama, adaptation, and other content-creation domains.
---

# 创作 Grilling 共享协议

提供创作访谈的共同机制，不负责选择用户入口、拥有领域 canon、生成正文或操作 Auctra/Scaena。公开入口是 `creative-grill-me`、`novel-grill-me` 和 `manga-drama-grill-me`；本 Skill 可以被这些入口加载，也保留 `$creative-grilling` 高级直接调用兼容性。

## 必读参考

- 每轮访谈前读取 [references/frontier-protocol.md](references/frontier-protocol.md)。
- 需要选择 `quick|standard|deep` 时读取 [references/depth-routing.md](references/depth-routing.md)。
- 生成 route、brief 或 owner handoff 时读取 [references/contracts.md](references/contracts.md)。
- 需要检查覆盖场景时读取 [references/route-matrix.md](references/route-matrix.md)。
- 进入、恢复或重开 owner-session 会话时按 [references/frontier-protocol.md](references/frontier-protocol.md) 的恢复小节执行；binding 合同见 [references/contracts.md](references/contracts.md)。
- 阶段确认并授权试写时读取 [references/writer-handoff.md](references/writer-handoff.md)，串行交接最窄 writer 并在候选返回后恢复访谈。
- 宿主问答控件适配、typed action 发现或 legacy owner 降级时读取 [references/host-adaptation.md](references/host-adaptation.md)。
- 其他 AI 做剧（非漫剧）分支读取 [references/ai-drama-decision-map.md](references/ai-drama-decision-map.md)。
- 审阅交互质量时读取 [references/canaries.md](references/canaries.md) 的合成 transcript canary。

## 共享工作流

1. 接收入口已经确定的 `domain`、`project_mode`、`phase`、`target_artifact` 和可选 depth override。领域尚未确定时返回入口路由，不在本协议中猜测。
2. 根据风险和范围选择 depth。用户显式覆盖优先；用户可随时要求缩小范围、跳过分支或收束。
3. 建立当前 artifact 的概念决策 DAG，并将节点分为：
   - `fact`：Agent 从项目、owner projection、工具或可靠来源核实。
   - `decision`：目标、风险、范围、审美承诺与接受标准，由用户决定。
   - `hypothesis`：只能由调研、试写、分镜、样片、声音测试或生产 probe 验证。
4. 只提出当前 frontier。所有前置节点必须已 `decided`、可安全 `provisional` 或具有足够事实；同一轮问题互不依赖。
5. 每个问题给出一个可反驳建议和最重要取舍。用户回答后更新状态、检查矛盾、重新打开受影响节点并重算 frontier。
6. 用户回答“不知道”时转成 `needs_research`、`needs_prototype` 或 `blocked`，不得替用户选择。
7. 用户连续机械接受建议时，只复核最高影响、最难逆转的一项；不人为制造低价值争论。
8. frontier 为空后输出聊天内 `creative.decision-brief.v0.1`。用户确认共同理解前，不调用 owner mutation、writer、生成 provider 或生产操作。
9. 用户确认后只输出 `creative.owner-handoff.v0.1`，由后续 owner Skill 决定真实命令和确认门。
10. 用户明确授权试写时，按 [references/writer-handoff.md](references/writer-handoff.md) 串行交接最窄 writer；候选返回进入待审，只重开受影响节点，访谈不代写正文。
11. 存在 `creative.owner-session-binding.v0.1` 时按恢复/刷新/重开规则执行；binding 缺席时行为与旧版完全一致。

## 问题格式

```text
❓ Q1 — [决策] <标题>：<问题、可选项和必要上下文>

➡️ 建议：<明确、可反驳的立场>。
⚖️ 取舍：<最重要的收益与代价>。
```

事实尚未核实时不要伪装成决策题。建议不得覆盖用户价值判断，也不得把搜索结果当作创作方向的最终答案。

## 不变量

- 事实检索在当前授权范围内完成；没有明确 delegation 授权时不创建子 agent。
- projectless 访谈保持 chat-only。
- 访谈确认不等于持久化、review accept、付费生成、主体冻结、生产接受、导出或发布授权。
- 下游只能串行选择一个 primary owner Skill；共享协议不与 writer/router 竞争 artifact ownership。
- 输出不包含 raw prompt、受保护作品全文、provider payload、credential、私有路径或完整思维链。
- 缺少入口、领域 Skill 或 owner adapter 时返回 `missing`/`needs_contract`，不得静默模仿完整流程。

## 验证

```bash
python3 scripts/validate_creative_grilling_matrix.py
```

