## Skill 分工

`template-registry-agent-operator` 负责消费闭环；`template-registry-template-author` 负责内容 authoring；`yeisme-prompt-repository-router` 负责 owner 选择。Scaena/Eikona 领域 Skill 只引用 exact 英文模板并保留领域准入。

## 渐进加载

主 SKILL 只保存决策和真实命令，locale/layout 与验证细节放在 references。新 Skill 通过 `scripts/skills.sh profile add` 进入 root 和内容仓 profile，runtime 由同步脚本生成。

## 安全

Skill 明确禁止把 `docs/template-zh-CN.md` 手工拼成编译模板，禁止手写 JSON/YAML metadata，禁止在 authoring/preview 阶段调用 provider。
