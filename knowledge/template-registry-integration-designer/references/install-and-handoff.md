# 安装与交接

## 安装 Skills

普通项目先安装 Registry Operator：

```bash
template-registry prompt skill install --runtime both --json
```

使用 Yeisme Skills manager 的项目安装集成设计 Skill：

```bash
cd yeisme-agent-my-skills
scripts/skills.sh --project /path/to/project profile add template-registry-integration-designer
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

集中 profile 管理项目不得让 Registry 直接覆盖 `.agents/skills` 或 `.claude/skills`。

## 提示词和工作流交接

| 接收方 | 交接内容 | 保留在接收方的状态 |
| --- | --- | --- |
| 通用 Agent | verified prompt package、步骤说明、可携带资料 | 聊天/执行状态与 Provider 权限 |
| Eikona | exact image template ref、输入、reference asset refs | Visual Job、费用、模型、图片 evidence、acceptance |
| Scaena | storyboard/shot/edit exact refs、step outputs | ProductionGraph、连续性、review、export |
| Auctra | writing template ref、source bindings | canonical text、revision、author review |
| Sonora | audio template ref、script/audio requirements | voice rights、TTS/provider、audio artifact |
| Pinax | exact ref 或经允许安装的 prompt draft | vault、索引、Git 和笔记 lifecycle |

优先交接 exact `promptrepo://` ref、snapshot/template/contract digest、recipe/package digest、缺失依赖和确认状态。不要复制另一个 owner 的私有数据库或隐藏 Prompt。

Skill 安装、Prompt 编译、领域执行和资产接受是四个不同状态。任何编译包都不能自行授权付费生成、访问凭据、发布或把候选资产标为 canonical。
