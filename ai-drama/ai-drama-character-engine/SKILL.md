---
name: ai-drama-character-engine
description: Use when designing, simulating, stress-testing, or revising AI drama characters, motivations, secrets, relationships, voices, decisions, and state transitions.
---

# AI Drama Character Engine

## 目标

让人物根据欲望、恐惧、价值观、记忆和关系做出有代价的选择，而不是让作者随意推动人物。

## 输入

- `CharacterState` 或角色 proposal；
- `CanonSnapshot`、关系图、世界规则和当前 beat；
- 已发生事件、角色知道的信息和禁止违反的事实。

## 工作流

1. 建立欲望、恐惧、秘密、价值观、底线、资源和行为习惯。
2. 区分角色知道的事实、错误信念和观众知道的事实。
3. 对当前冲突模拟至少 2–3 个行动选择，标注收益、代价、关系变化和下一状态。
4. 检查行动是否符合性格，是否过早泄露秘密，是否制造新的戏剧压力。
5. 输出 `CharacterDecisionProposal` 或 `CharacterStateDelta`，等待 Auctra/Dramaturge owner 接受。

## 质量门槛

- 角色的选择必须可追溯到欲望/恐惧/价值观，而不是只服从剧情需要；
- 每次重大选择至少改变一个关系、资源、风险或自我认知；
- 角色声线、潜台词和行动不能互相矛盾；
- 不使用心理诊断标签替代行为证据；
- 跨集状态变化必须有 event/beat refs。

## 边界与验证

不保存私有记忆、不替代 canonical screenplay、不把角色模拟当作真实心理诊断。结构变更交给 Auctra/Dramaturge：

```bash
cd /workspaces/yeisme-agent/cli/auctra
auctra --help
go test ./...
```
