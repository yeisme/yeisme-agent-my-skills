---
name: ai-drama-critic-panel
description: Use when comparing AI drama story, shot, keyframe, audio, or episode candidates with parallel blind judges, rubric scoring, disagreement analysis, adjudication, repair proposals, and human review gates.
---

# AI Drama Critic Panel

## 目标

把“哪个好”变成同一 CandidateSet 内可比较、可解释、可复盘的推荐。评委负责 advisory assessment，Scaena 负责最终 production decision。

## 评委角色

- Story：主题、钩子、因果、信息释放；
- Character：人物主动性、选择、代价、关系和情绪；
- Director/Visual：调度、镜头理由、主体身份、构图和可读性；
- Continuity：人物、服装、道具、空间、时间、动作和声音；
- Producer/Risk：时长、成本、rights、capability、交付风险。

## 工作流

1. 冻结 CandidateSet、CanonSnapshot、DirectorProfile、RubricProfile、JudgePanelProfile、seed 和成本策略。
2. 并行执行盲评；评委不可读取其他评委分数。
3. 同一 model family 标记为 correlation cluster；生成者自评不得成为决定性证据。
4. 用 0–4 anchored score 逐维评分，记录证据、coverage、indeterminate 和 blocker。
5. hard gates 先于软分；每维用中位数/截尾平均聚合，记录 IQR/分歧。
6. 近分候选做 pairwise comparison；Sol 输出排名和 `RepairProposal`。
7. 超出阈值、证据不足或 blocker 未决时输出 `needs_human_review`。

## 初始阈值

P0 可从以下校准起点开始：hard gates 全通过、总分至少 80/100、关键维度至少 3/4、evidence coverage 至少 0.8、分歧不超过 1.0。未经 gold set 和人工标签校准，不得晋级 production policy。

## 禁止

- 不把简单多数票当作独立证据；
- 不跨 CandidateSet、rubric 或 profile 版本比较总分；
- 不把推荐直接写成 selected、production_accepted 或 export；
- 不无限 reroll；
- 不写 raw prompt、provider payload 或完整 chain-of-thought。

## 验证

```bash
cd /workspaces/yeisme-agent/agent/ordo
bun run test
cd /workspaces/yeisme-agent/cli/eikona
go test ./internal/assessment ./internal/runtime ./internal/workflow
```
