# ai-drama-task-role-consolidation Specification

## ADDED Requirements

### Requirement: 任务角色意图必须优先路由到官方模板

Router 对形态策略、故事架构、人物引擎、分集规划、场景写作和多候选评审六类意图 SHALL 把 primary 解析为官方模板 exact ref（`promptrepo://official/writing/ai-drama-*@<version>`），经消费方 CLI（`template-registry prompt` 或 owner 领域命令）编译；MUST NOT 再把已收编的任务角色解析为需安装的矩阵 Skill。

#### Scenario: 形态策略请求

- **WHEN** 用户请求选择剧型、时长、集数与类型契约
- **THEN** DramaRoutePlan 的 primary SHALL 为 `template:writing/ai-drama-format-strategy`
- **AND** resolution_status SHALL 为 `template_ref_available`，不触发 Skill 安装决策。

### Requirement: 保留 Skill 必须继续承载宿主交互职责

Router 门禁（originality、artifact lifecycle、评估合同冻结）、上下文包构建、生产编排、制片预算与 owner 交接 SHALL 继续由保留 Skill 承载；它们的输出 MUST NOT 被模板输出替代为 canonical。

#### Scenario: 评估请求先冻结合同

- **WHEN** 用户要求评估或打分但没有冻结 AssessmentContract
- **THEN** Router SHALL 先路由 `ai-drama-assessment` Skill 冻结合同
- **AND** 候选比较再经 `writing/ai-drama-critic-review` 模板执行。
