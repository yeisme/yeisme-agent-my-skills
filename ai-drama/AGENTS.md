# AI Drama Skills 工作区说明

本目录是 Yeisme 第一方 AI 漫剧 Skills 模块，负责可复用的创作判断、评估流程、路由和 Owner handoff 说明，不负责保存剧本正文、ProductionGraph、资产 bytes、provider 凭据或运行时数据库。

## 目录边界

- 每个 Skill 目录必须包含 `SKILL.md` 与 `agents/openai.yaml`。
- `references/` 只放该 Skill 需要按需读取的规则、量表和示例。
- `.skills/yeisme/` 是发布源；`.agents/skills/` 和 `.claude/skills/` 是生成运行副本，不在本目录维护。
- canonical screenplay 归 Auctra，调度/receipt 归 Ordo，视觉 artifact 归 Eikona，ProductionGraph/production acceptance 归 Scaena。

## 设计约束

- Skill 输出 proposal、评估和 handoff，不直接修改其他 Owner 的 canonical state。
- 多评委必须盲评、绑定 CandidateSet/rubric/profile 版本，并记录模型相关性簇。
- 高分不能覆盖 rights、identity、continuity、permission、cost 或 preflight blocker。
- 不记录 raw prompt、provider payload、私有工具参数、凭据或完整 chain-of-thought。
- 参考具体导演时使用高层创作原则，不复制具体作品的台词、场景或镜头序列。

## 验证

从宿主仓库根目录运行：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
```

只有经 profile promotion 决定后才运行 `scripts/skills.sh sync-root` 或 `scripts/skills.sh sync-subprojects`。
