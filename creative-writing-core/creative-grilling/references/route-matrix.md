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

