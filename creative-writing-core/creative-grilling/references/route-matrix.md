# 创作 Grilling 路由与安全矩阵

每个 CASE 是静态覆盖声明；验证器检查入口、domain、project mode、depth 和关键不变量是否存在。真实访谈质量仍需人工 transcript canary。

### CASE CG-01 aggregate-novel
- entry: `creative-grill-me`
- domain: `novel`
- invariant: 聚合入口在小说意图明确时零路由追问。

### CASE CG-02 aggregate-manga-drama
- entry: `creative-grill-me`
- domain: `manga_drama`
- invariant: 聚合入口在漫剧意图明确时零路由追问。

### CASE CG-03 direct-novel
- entry: `novel-grill-me`
- domain: `novel`
- invariant: 不询问内容媒介，直接计算小说 frontier。

### CASE CG-04 direct-manga-drama
- entry: `manga-drama-grill-me`
- domain: `manga_drama`
- invariant: 不询问内容媒介，直接计算漫剧 frontier。

### CASE CG-05 projectless-readonly
- project_mode: `projectless`
- invariant: `owner_mutations=0`，结果保持 chat-only。

### CASE CG-06 auctra-facts
- project_mode: `auctra`
- invariant: 使用 Auctra 只读 projection 获取可发现事实。

### CASE CG-07 scaena-facts
- project_mode: `scaena`
- invariant: 读取 board、readiness、exceptions 或 production session projection。

### CASE CG-08 cross-owner-order
- project_mode: `cross_owner`
- invariant: 先完成 Auctra story/canon handoff，再进入 Scaena production handoff。

### CASE CG-09 unknown-answer
- status: `needs_evidence`
- invariant: “不知道”转换为 research/prototype ticket，不替用户回答。

### CASE CG-10 passive-agreement
- status: `needs_decision`
- invariant: 只复核最高影响、最难逆转的取舍。

### CASE CG-11 depth-override
- depth: `quick|standard|deep`
- invariant: 用户显式覆盖优先于自适应选择。

### CASE CG-12 hard-gates
- status: `blocked`
- invariant: rights、budget、stale、pending review 和 paid action 均 fail closed。

### CASE CG-13 missing-skill
- status: `missing`
- invariant: 缺少底层 Skill 时明确报告，不静默模拟。

### CASE CG-14 shared-understanding
- status: `ready_for_handoff`
- invariant: 用户确认共同理解前 `owner_mutations=0`。


### CASE CG-15 owner-session-bind
- binding: `creative.owner-session-binding.v0.1`
- invariant: 可选 companion；旧 route/brief/handoff 字段与例子不变，旧 consumer 不接受新必填字段；binding 含版本、来源、权限与 typed actions。

### CASE CG-16 owner-session-legacy
- status: `needs_contract`
- invariant: owner 只支持旧 brief/scratch 合同时，返回 needs_contract 或显式 legacy handoff，保留讨论结果，不声称持久恢复。

### CASE CG-17 shell-action-rejected
- invariant: 不可信 shell 模板不执行，只走宿主已登记 typed capability adapter。

### CASE CG-18 session-stale
- status: `needs_refresh`
- invariant: binding revision/digest 落后 owner 当前版本时先刷新；旧轮次序号不提交到新版本。

### CASE CG-19 upstream-reopen
- invariant: owner 标记上游 reopened 时只重开受影响分支，保留未受影响选择，暂停在途 writer handoff。

### CASE CG-20 stage-entry
- invariant: 按阶段进入条件加载最窄阶段问法（想法/人物/结构/章节/场景/成稿/修订；漫剧各 phase），上游未定不预问下游。

### CASE CG-21 same-turn-independence
- invariant: 同轮问题互不依赖；存在依赖时只提问依赖链最上游一问。

### CASE CG-22 unknown-to-proof
- status: `needs_evidence`
- invariant: “不知道/哪个更好看”转有界 proof（试写/proof slice/样片/读者小样），证据返回后只重开受影响节点。

### CASE CG-23 writer-roundtrip
- invariant: 阶段确认+授权后串行交接最窄 writer；候选返回进入待审，不自动 accept；访谈不代写正文、不隐式创建子 Agent。

### CASE CG-24 reject-all-baseline
- invariant: 候选可全部拒绝（说明失败原因回到 frontier），也可维持基线为合法结论。

### CASE CG-25 feedback-scope
- invariant: 当前项目反馈不跨项目；作者可推翻旧偏好；反馈引用标注来源与版本，匿名/低证据反馈不单独触发重开；F1 跨作品偏好/F2 多作者参考/F3 自动候选创作均未实现，不调用不模拟。

### CASE CG-26 host-control-fallback
- invariant: 有结构化提问控件用控件，无控件用编号文本；不因缺特定 Plan 模式拒绝工作；projectless 保持 chat-only。
