# AI Drama Skills

本模块把导演、编剧、人物、连续性、评估和制片判断拆成可路由的第一方 Skills。

Skill 是执行指导，不是第二套故事数据库。实现或修改跨项目合同时，应回到宿主仓库的根级 OpenSpec 与对应 Owner 的 OpenSpec。

当前根级设计：

`openspec/changes/ai-drama-skills-governance-v1/`

共享约束引用：

- `ai-drama-router/references/canon-boundary.md`
- `ai-drama-producer/references/production-constraints.md`
- `ai-drama-continuity-supervisor/references/continuity-evidence.md`

宿主仓库验证命令：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
```
