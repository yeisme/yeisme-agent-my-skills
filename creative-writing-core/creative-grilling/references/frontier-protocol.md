# Frontier 访谈协议

## 节点状态

每个决策节点使用以下概念状态之一：

- `unsettled`：尚未提问或前置条件不足。
- `decided`：用户已明确选择并理解主要取舍。
- `provisional`：暂定选择，可让下游问题继续，但必须保留重新打开条件。
- `needs_fact`：需要 Agent 核实现有状态、平台规则、工具能力或外部证据。
- `needs_research`：需要多来源研究、用户/市场证据或专业事实。
- `needs_prototype`：需要试写、分镜、样片、声音测试、视觉样张或交互原型。
- `blocked`：缺少权利、预算、owner、权限或其他无法在当前会话解决的条件。
- `reopened`：下游回答暴露矛盾，必须回到上游重新选择。

`provisional` 不是伪装的确定。只有可逆且不会造成高成本下游承诺的节点才允许暂定。

## Frontier 判定

一个节点只有在以下条件同时满足时才能进入当前轮：

1. 所有依赖节点已经 `decided` 或可安全 `provisional`。
2. 所需事实已核实，或问题本身明确要求用户选择可接受的不确定性。
3. 它不依赖当前轮中另一个问题的答案。
4. 它属于当前 `decision_scope` 和 `target_artifact`。

每轮后重新计算，不预写后续完整问卷。若回答改变了媒介、受众、篇幅、商业模式、原创性或生产边界，重新打开所有受影响分支。

## 三类问题的责任

### Fact

Agent 负责读取现有项目状态、canon、owner 合同、平台规范、工具能力和可靠来源。事实仍不确定时标记证据缺口，不向用户索要可以自行查到的实现细节。

### Decision

用户负责目标、风险容忍、读者承诺、审美方向、范围、预算优先级、权利选择和最终接受标准。Agent 必须给出建议，但不能替用户完成这些选择。

### Hypothesis

涉及“是否好看、是否好笑、声音是否鲜活、节奏是否抓人、镜头是否可读、读者是否愿意追更”等可体验判断时，停止语言循环，提出最小证据动作：

- 两个策略差异明确的短试写；
- 一场核心戏或一章 proof slice；
- 6–12 格分镜或一个镜头样片；
- 两种对白/声线 live test；
- 小样读者测试或生产 capability probe。

实验结果返回后，只重新打开被证据影响的节点。

## 轮次质量

- 一轮应能被用户按编号回答；若问题过多，说明 scope 未切好，应先缩小访谈包。
- 推荐答案必须包含最重要的反面代价，避免用户只对“听起来正确”的措辞点头。
- 高影响选择优先于低层实现细节；先问作品承诺，再问表达手段。
- 不把同义改写的两个选项伪装成真实选择。
- 不为追求问题数量展开与目标 artifact 无关的分支。

## 恢复、刷新与重开（owner-session 可选）

本节只在存在 `creative.owner-session-binding.v0.1` 时生效；projectless 会话不引入任何持久状态文件，恢复能力完全来自 owner 的版本化 projection。

### 恢复

1. 将 binding 的 `session_revision`/`session_digest` 与 owner 当前版本比对；不一致时先刷新（`needs_refresh`），刷新后重算 frontier，再继续提问。
2. 恢复时展示三件事：已决定摘要（含理由与取舍）、未决项、被重开节点及原因；仍有效的决定不要求重答。
3. 问题引用使用稳定 ref（如 `novel.character.core_motivation`），不使用“上一轮 Q3”这类会随版本漂移的序号。

### 示例

- 稳定 ref：恢复时表述为“`novel.commitment.format=连载` 已定，理由是周更留存测试”，而不是“你上次第 2 题选了 B”。binding 刷新后轮次序号变化，ref 不变。
- 同轮依赖：`structure.act3_payoff` 依赖 `character.core_motivation`，而后者被 owner 标记 `reopened` 时，本轮只问动机，不同时问结局；两问同时出现即违规。
- 旧 source：决定引用 `source_refs=[auctra://proj/nan-1/story@rev12]`；恢复时 owner 已到 rev15 且相关场景被 reopen，该决定回到 `reopened`，需在新 source 上重问，不沿用旧结论。
- 角色身份：恢复摘要始终区分“你的决定（用户，decision 来源）”与“我的建议（Agent，proposal/hypothesis）”；Agent 建议不得被写成既成事实。
- 未知转试写：恢复后用户对“两种结局哪种更抓人”回答“不知道”，转 `needs_prototype` 并给出有界 proof handoff（如两个 800 字结尾候选），不替用户选择。

### 重开与在途交接

- owner 将上游决定标记 `reopened` 时，只重开依赖它的下游分支；未受影响的选择保留并展示。
- 存在进行中的 writer handoff 时，上游重开先暂停该交接，待重问收敛后用新 digest 重新生成 handoff；不拿旧 digest 提交。
- 每次重开说明影响范围（哪些决定保留、哪些作废、为什么），不要求用户复述历史。

## 收束与确认

frontier 为空不等于自动完成。先总结已决定、暂定、未决和验证项，再询问用户是否确认共同理解。用户确认后只完成访谈 handoff；除非用户随后另行要求，不自动进入计划或实施。

