# 中文小说搜索关键词预设

## 使用时机

当用户要求“参考知名小说”“找同类作品结构”“补搜索关键词”“拆解某类桥段”时读取本文件。它只提供检索词、结构参考维度和反抄袭边界，不提供小说原文、具体作者文风仿写、搬运路径或同款剧情复刻。

## 使用原则

- 先确认用途：原创立项、类型契约、场景卡、章节写作、作品拆解、改编评估或社媒衍生。
- 搜索时优先找“结构、类型、桥段功能、叙事机制”，不要找“全文、txt 下载、同款、仿写”。
- 知名小说只能作为结构参考的比较对象，例如公平线索、权力博弈、试炼升级、规则生存、群像调度；不得复制人物、核心设定、情节链或标志性表达。
- 输出时必须把参考拆成抽象机制：读者承诺、压力源、信息差、选择代价、章尾回报。

## 预设格式

```markdown
### preset_id
- 适用：
- 中文关键词：
- English keywords：
- 结构参考维度：
- 排除词：全文 / txt下载 / 搬运 / 仿写某作者 / 照抄 / 同款剧情
- 交给技能：
- 反抄袭边界：
```

## 类型搜索包

### suspense-fair-play
- 适用：悬疑推理、密室、证据链、红鲱鱼、公平误导。
- 中文关键词：公平线索 推理小说 误导 红鲱鱼 真相回收 密室诡计 证据链 不可靠叙述 双时间线。
- English keywords：fair play mystery clue chain red herring locked room reveal unreliable narrator dual timeline.
- 结构参考维度：读者能否回看验证线索、嫌疑如何轮换、主角误判如何被事实纠正、反转后是否产生新行动。
- 交给技能：`chinese-novel-genre-contract-strategist`、`chinese-novel-scene-card-writer`、`chinese-novel-analysis-decomposer`。
- 反抄袭边界：只学习线索投放和误导机制，不复制诡计核心、凶手身份、标志性案件或侦探人设。

### power-politics-faction
- 适用：权谋、宫斗、朝堂、宗门、公司派系、家族继承。
- 中文关键词：权谋小说 派系 同盟 背叛 朝堂对质 宫斗 忠诚测试 家族继承 公开仪式 私下交易。
- English keywords：political intrigue faction alliance betrayal public accusation court politics loyalty test succession.
- 结构参考维度：每个派系想要什么、筹码如何交换、公开话语和真实目标如何相反、胜利是否制造下一层敌人。
- 交给技能：`chinese-novel-genre-contract-strategist`、`chinese-novel-outline-architect`、`chinese-novel-scene-card-writer`。
- 反抄袭边界：不复刻具体王朝、组织名、血缘秘密或经典夺嫡路线，只抽象权力流动和代价结构。

### wuxia-xianxia-jianghu
- 适用：武侠、仙侠、江湖恩仇、门派试炼、道义选择。
- 中文关键词：武侠 江湖 恩仇 门派 试炼 道义选择 侠义 因果 宗门大比 师徒反目。
- English keywords：wuxia jianghu sect trial chivalry moral choice cultivation tournament mentor betrayal.
- 结构参考维度：武力规则、江湖声誉、恩义债务、师承关系、突破代价和价值选择。
- 交给技能：`chinese-novel-genre-contract-strategist`、`chinese-novel-volume-arc-planner`、`chinese-novel-chapter-writer`。
- 反抄袭边界：不照搬经典门派、武功名、奇遇路线或主角成长轨迹，只复用“规则-选择-代价-名望”结构。

### survival-rule-instance
- 适用：无限流、生存、副本、规则怪谈、密闭空间逃生。
- 中文关键词：无限流 副本 规则怪谈 禁忌 生存 逃生 倒计时 团队背叛 资源耗尽。
- English keywords：survival game rule mystery taboo instance escape countdown scarce resources team betrayal.
- 结构参考维度：规则如何被发现、违规代价如何展示、团队信任如何被消耗、通关是否留下更大系统问题。
- 交给技能：`chinese-novel-outline-architect`、`chinese-novel-scene-card-writer`、`chinese-novel-hook-pacing-editor`。
- 反抄袭边界：不复制副本设定、怪物规则或通关答案，只学习规则揭示和压力升级。

### horror-supernatural-taboo
- 适用：灵异、恐怖、民俗禁忌、规则怪谈、心理惊悚。
- 中文关键词：灵异小说 恐怖 氛围 禁忌 民俗 异常信号 假安全 真相代价 规则怪谈。
- English keywords：supernatural horror uncanny signal taboo folklore false safety reveal cost psychological dread.
- 结构参考维度：异常从何处进入日常、规则如何限制角色、读者恐惧来自未知还是代价、真相揭示后是否更危险。
- 交给技能：`chinese-novel-genre-contract-strategist`、`chinese-novel-chapter-writer`、`chinese-novel-reader-retention-editor`。
- 反抄袭边界：不搬运具体民俗故事、恐怖意象组合或怪物设定，只抽象禁忌和信息控制。

### comedy-satire-status
- 适用：喜剧、讽刺、黑色幽默、身份错位、社会观察。
- 中文关键词：讽刺小说 身份错位 误会升级 地位反转 黑色幽默 回调 社会观察 荒诞。
- English keywords：comic novel satire status reversal misunderstanding ladder black comedy social observation callback.
- 结构参考维度：角色自认身份和外界评价的落差、误会如何升级为真实后果、笑点如何回收主题。
- 交给技能：`chinese-novel-brief-architect`、`chinese-novel-scene-card-writer`、`chinese-novel-style-polisher`。
- 反抄袭边界：不模仿具体作家的句式和冷幽默节奏，只复用“错位-升级-反转-主题揭示”。

## 排除词库

默认把这些词作为风险提示：全文、txt下载、未删减、搬运、盗版、仿写某作者、同款剧情、照抄、洗稿、替换人名、原文改写、续写某未授权作品。

## 输出要求

使用本文件后，交付物要写明：使用了哪些搜索预设、得到的结构启发、没有使用的受保护元素、下一步交给哪个技能。需要引用具体知名作品名时，只能作为用户已提供或公开讨论对象的标签，不把它写成可复刻剧情。
