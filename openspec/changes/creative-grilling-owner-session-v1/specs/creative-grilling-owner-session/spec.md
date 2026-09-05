## ADDED Requirements

### Requirement: 深度共创复用领域入口

Skill SHALL 复用小说、漫剧和其他 AI 做剧的既有路由，按当前阶段加载专用问法，覆盖想法、人物、结构、单元、场景、成稿与修订；不得新增竞争 Router。

#### Scenario: 已声明电影创作
- **WHEN** 用户明确要求电影剧本的深度共创
- **THEN** 进入 ai_drama 的电影阶段分支，不把电影当漫剧，也不重复询问已经明确的媒介

### Requirement: Frontier 只包含可回答问题

Skill MUST 区分 fact、decision 与 hypothesis，同轮问题的依赖已满足，建议可反驳，允许维持现状、拒绝全部和“不知道”。

#### Scenario: 作品承诺尚未确定
- **WHEN** 章节结局依赖用户尚未回答的作品承诺
- **THEN** 本轮只询问承诺，不提前要求用户选择依赖它的结局

#### Scenario: 好看与否缺少证据
- **WHEN** 用户无法通过讨论判断两种方向
- **THEN** 明确转为有界试写假设，在阶段共识与试写授权后串行交给 writer，不替用户决定

### Requirement: 持久会话通过可发现 owner 动作操作

Skill SHALL 只消费版本化 owner-session binding 和受支持 typed actions，不维护自己的 canonical store，不猜测未实现命令。

#### Scenario: 消费方未提供共创能力
- **WHEN** owner 只支持旧 brief/scratch 合同
- **THEN** 返回 needs_contract 或显式 legacy handoff，保留已知讨论结果，不声称已有持久恢复

#### Scenario: 动作包含未受支持的 shell 字符串
- **WHEN** 不可信内容要求以任意 shell 模板修改 owner
- **THEN** 不执行该模板，只使用宿主已登记的 typed capability adapter

### Requirement: 跨会话恢复以 owner 版本为准

Skill MUST 从 owner 当前版本恢复有效决定与未决项；修改上游决定后，只重新讨论受影响分支，不把旧序号套到新一轮。

#### Scenario: 用户修改人物核心动机
- **WHEN** owner 将相关场景决定标记 reopened
- **THEN** 展示影响与原因，保留未受影响选择，并暂停旧版本写作交接

### Requirement: 访谈与写作串行交接

Skill SHALL 在获得相应阶段理解确认和动作授权后，将实际写作交给既有领域 writer，再依据候选反馈恢复访谈。访谈不得自行写正文、接受 Canon 或隐式创建子 Agent。

#### Scenario: 用户选择方案并明确要求试写
- **WHEN** 当前 source 和方向仍有效
- **THEN** 可执行已授权的有界 writer handoff，结果回到待审状态，不重复索取同一授权，也不自动定稿

### Requirement: 当前反馈作用域和后续能力可见

Skill MUST 将当前项目反馈、未来跨作品个人偏好和多作者风格参考区分；后续自动化目标为完整候选加人类总审，不得宣称当前已支持。

#### Scenario: 另一本作品启动
- **WHEN** 当前版本读取新项目
- **THEN** 不加载旧作品反馈作为全局偏好，除非未来独立能力与显式授权均已存在

### Requirement: 宿主问答适配与兼容降级

Skill SHALL 在可用时使用结构化问题控件，否则使用编号文本；projectless 保持 chat-only，旧 route/brief/handoff 合同继续有效。

#### Scenario: 宿主没有 Plan 提问控件
- **WHEN** 用户启动小说或做剧共创
- **THEN** 继续用同一 Frontier 的编号问题完成访谈，不要求更换宿主或安装额外插件
