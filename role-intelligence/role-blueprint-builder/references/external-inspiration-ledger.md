# 外部角色技能启发账本

访问日期：2026-08-11。所有结论只吸收抽象设计，不复制外部 SKILL 正文、角色台词、世界种子或人格文件。

## 来源与决策

| Source | Pinned ref | License evidence | 可吸收设计 | 主要缺陷/拒绝项 | 当前决策 |
| --- | --- | --- | --- | --- | --- |
| [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill) | `27642f5bfed2dc1bbf8ee59a2c1ee602a626bbd7` | GitHub metadata + `LICENSE`: MIT | 多来源研究、思维模型/启发式/表达分层、矛盾保留、诚实边界、独立 fidelity 测试 | 模板鼓励第一人称公众人物冒充；依赖重型多 Agent；研究资产和成本可能失控 | 不 import；吸收证据、推断和评测结构 |
| [Emperor Agent](https://github.com/TheSyart/emperor-agent) | `91fb94cef3be0640591b2a9d7edfcc6cc54a330f` | GitHub metadata + `LICENSE`: MIT | Skill 渐进加载、AgentDefinition、tool allowlist、sandbox、Goal acceptance/evidence、权限取交集 | 它是 agent runtime，不是角色人格框架；皇帝命名不能成为 authority | 不 import skill；吸收运行治理原则 |
| [Linggen](https://github.com/Jimlinsen/linggen) | `32b02679f4b224b321753c1a286ca802d293f551` | GitHub metadata + `LICENSE`: MIT | 从深层约束到表层声线、世界/关系/禁区、可变与不可变分离、演化检查 | 含大量受保护世界 seed；“不是 AI/从海里来”等存在叙事可能误导；对话内自演化缺少 owner ledger | 不 import；只吸收 layered boundary 和 invariant/delta 思路 |
| [Waifu Skill](https://github.com/miunasu/waifu-skill) | `4944ec2c3e42f1522bd94aaa18d2a88428de85c5` | GitHub metadata + `LICENSE`: MIT | lore/persona 分轨、原作证据、冲突纠正、版本回滚、跨世界术语适配 | “不是 AI”硬规则、受保护角色声线、手写结构化状态、删除/覆盖流程过于简单 | 不 import；吸收 canon/behavior 分离和 correction ledger |
| [Possession Skill](https://github.com/Summer907/possession-skill) | `b58b2900fac063f1212e36aee16fcaf30473989f` | GitHub metadata + `LICENSE`: MIT | profile/personality/interaction/memory/relations 五面、证据等级、冲突文件、OOC 场景测试 | 质量分可被同一模型自评；Wiki 权利与版本不足；没有确定性游戏状态和权限模型 | 不 import；吸收 evidence/conflict/scenario-test 模式 |
| [Qiqing Liuyu](https://github.com/Lniosy/qiqing-liuyu) | `6db6e96cf802411f01cbaa499173bd8fcb48d633` | GitHub metadata 未识别许可证 | 明确“情感是表演而非意识”、情绪强度、观点边界、去模板化表达 | 许可证不清；从心率直接推断情绪风险高；示例鼓励虚构个人经历；不应覆盖所有人格策略 | quarantine；不 import，只保留透明 affect modulation 原则 |
| [Digital Life](https://github.com/wildbyteai/digital-life) | `09d8a19112c7946a0d40351af13bed719379d497` | GitHub metadata + `LICENSE`: MIT | consent、privacy gate、最小数据、evidence trace、proposal/review、不得冒充本人 | 部分心理/人生判断仍需更严格证据；不能直接当角色运行时 | 不 import；吸收 privacy/evidence/proposal-first 原则 |

## 统一抽象

外部设计被重写为四个 Yeisme 合同：

1. `RoleBlueprint`：来源、行为、状态、权限和评测的 proposal。
2. `RoleRoute`：场景到 skill/owner/readiness 的路由。
3. `OwnerAdapter`：Auctra、游戏、Pinax、digital-human、Ordo 等各自实现。
4. `EvidenceGate`：consent、rights、canon、memory、permission、replay 和 safety 的晋级门禁。

仓库许可只覆盖仓库内容，不自动授权真实人物身份、肖像、私人数据、作品角色、台词、商标、世界设定或可识别表达。
