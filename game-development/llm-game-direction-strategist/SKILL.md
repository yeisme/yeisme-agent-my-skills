---
name: llm-game-direction-strategist
description: Use when evaluating, comparing, or narrowing LLM-native game directions such as AI relationship games, mystery and interrogation games, small-world RPGs, AI game masters, social simulations, or generative narrative products, especially when the team needs a scenario matrix, player-value thesis, commercial hypothesis, scope recommendation, or go/no-go evidence plan.
---

# LLM 游戏方向策略师

## 目标

判断一个方向是否真正需要 LLM，并把宽泛的“AI 游戏”想法变成可比较、可证伪、可进入原型阶段的产品选择。

## 输入

- 团队规模、周期、预算、目标平台和内容分级。
- 候选类型、目标玩家、参考作品和期望体验。
- 可用模型、延迟、成本、联网和内容生产约束。
- 已有剧情、美术、角色设定、玩法原型或用户证据。

## 输出

- 一句话玩家幻想与核心承诺。
- 候选方向矩阵、推荐顺序和淘汰理由。
- `LLM necessity` 证明：移除 LLM 后何种核心体验会消失。
- 核心循环、重复游玩价值、内容供给方式和商业假设。
- 最大风险、最便宜验证、晋级信号和停止条件。

## 评估维度

按 1–5 分评价每个候选方向，并明确证据或未知项：

1. `player_fantasy`：玩家能否用一句话理解并渴望该体验。
2. `llm_necessity`：LLM 是否改变玩法，而非只增加对白数量。
3. `agency`：自由输入是否产生可追踪、可回收的后果。
4. `game_legibility`：目标、风险、状态和反馈是否仍像游戏。
5. `replayability`：变化是否来自系统和人物，而非随机垃圾内容。
6. `production_fit`：团队能否承担美术、关卡、写作、审核和运营。
7. `latency_cost_fit`：目标节奏是否容忍模型延迟与单局成本。
8. `safety_fit`：关系、未成年人、仇恨、性、暴力和用户生成内容风险是否可控。
9. `market_testability`：能否用短周期试玩验证留存意愿和付费信号。

## 工作流

1. 先写玩家幻想，不从技术功能或传统品类名出发。
2. 列出 3–7 个候选方向，至少包含一个低制作成本方向和一个高差异化方向。
3. 对每个方向执行“无 LLM 测试”：如果替换成脚本仍保留 80% 体验，则降低优先级。
4. 定义 10–20 分钟核心循环，标明玩家决策、系统反馈、LLM 作用和持久后果。
5. 建立场景矩阵：目标用户、job-to-be-done、付费假设、所需资产、gate、证据、交付和晋级信号。
6. 计算制作面：角色数、场景数、状态数、调用频率、人工审核量和最坏内容成本。
7. 推荐一个主方向、一个备选方向和明确不做清单。
8. 把推荐方向交给 `llm-game-systems-architect`；需要短周期试玩计划时交给 `llm-game-vertical-slice-planner`。

## 默认判断

- 个人或小团队优先验证“AI 推理/审讯 + 关系变化”，其次是小规模封闭世界 RPG。
- 长期关系模拟必须有明确游戏目标、风险和阶段变化，不能退化成无终点聊天。
- 开放世界、百 NPC 自主社会和无限内容平台默认属于后续研究，不作为首个商业原型。
- “AI 生成更多任务、地图或对白”本身不是产品方向。

## 边界

- 不伪造市场规模、竞品收入或实时行业结论；缺少研究时将其标为待验证假设。
- 不把模型人格化声明当作玩法证据。
- 不把开放输入等同于玩家自由；所有关键后果必须能进入游戏状态。
- 不在方向评估阶段创建新子项目、稳定协议或生产实现。

## 验证

- 推荐结论包含反方证据和停止条件。
- 至少一个关键假设可在两周内通过真实试玩证伪。
- 方向矩阵区分 `exploratory`、`first-support` 和 `mature`，不把概念包装成成熟能力。
- 每个推荐方向都能说明“为什么必须是游戏”和“为什么必须用 LLM”。
