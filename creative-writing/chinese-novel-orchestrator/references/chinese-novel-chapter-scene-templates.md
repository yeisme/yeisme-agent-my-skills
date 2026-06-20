# 中文小说章节与场景模板

## 使用时机

当需要把大纲写成章节、把章节拆成场景卡、或把一章交给多个 worker 修订时读取本文件。它提供通用模板和场景家族入口；具体悬疑、情感、升级、世界观、过渡、高潮回收场景，按 `## 场景家族入口` 读取对应 library。不要把所有模板一次性塞进正文，只读取当前章节需要的家族。

## 章节模板

```markdown
# 第 X 章《标题》

## 章节目标
- 入场状态：
- 本章必须改变的状态：人物 / 信息 / 关系 / 危险 / 资源 / 世界规则
- 失败代价：
- 读者承诺：这一章读完能获得什么

## 入场压力
- 类型：危险 / 异常 / 倒计时 / 关系破裂 / 选择 / 新线索 / 资源耗尽
- 首段画面：
- 主角当前误判：
- 读者比主角多知道或少知道的信息：

## 场景列表
| scene_id | 场景功能 | 地点时间 | 出场人物 | 欲望 | 阻力 | 转折 | 后果 | 钩子交接 |
|---|---|---|---|---|---|---|---|---|
| S1 | 开场压力 |  |  |  |  |  |  |  |
| S2 | 信息/关系升级 |  |  |  |  |  |  |  |
| S3 | 章尾反转/选择 |  |  |  |  |  |  |  |

## 章尾钩子
- 钩子类型：危险 / 揭示 / 选择 / 背叛 / 倒计时 / 情绪反转
- 下一章必须偿还：
- 不能透支的承诺：
```

## 场景卡模板

```markdown
## scene_id: Sx
- 场景家族：suspense / relationship / escalation / worldbuilding / transition / climax-payoff / investigation-procedure / power-politics / heist-strategy / survival-disaster / horror-supernatural / comedy-satire
- 场景功能：开场压力 / 线索 / 关系变化 / 规则展示 / 升级 / 余波 / 高潮
- location_time：
- active_characters：
- point_of_view：
- 入场状态：
- desire：角色想要什么
- obstacle：谁或什么阻止
- tactic：角色采取的策略
- turn：场景中点或末尾的不可逆变化
- consequence：代价、获得、误判或新风险
- dialogue_function：试探 / 威胁 / 掩饰 / 诱导 / 告白 / 解释中的冲突
- subtext：角色真正不愿说出的东西
- sensory_detail：1-3 个可见、可听、可触、可闻细节
- continuity_notes：新增事实、知识边界、道具状态、时间线
- exit_hook：交给下一场或下一章的钩子
```

## 章首模板

| 类型 | 适用 | 填空 |
|---|---|---|
| 压力开场 | 需要立刻抓住读者 | `当[异常/危险]发生时，主角正在[行动]，他/她最怕的[后果]已经开始。` |
| 误判开场 | 悬疑、情感、权谋 | `主角以为[判断]，但第一个细节[证据]说明事情不对。` |
| 关系开场 | 情感、群像、合作破裂 | `[角色A]说/做了[表层动作]，真正要测试的是[角色B的底线]。` |
| 倒计时开场 | 追逐、考试、任务、救援 | `距离[期限]只剩[时间]，主角缺少[关键资源]。` |

## 章中转折模板

```markdown
- 旧目标：
- 新发现：
- 谁因此受益：
- 谁因此失去筹码：
- 主角必须改变的策略：
- 读者此刻产生的新问题：
```

## 章尾模板

| 钩子类型 | 模板 | 风险 |
|---|---|---|
| 危险逼近 | `主角刚解决[问题]，却发现[更大危险]已经进入现场。` | 不能凭空降临，要有前文 seed |
| 真相揭示 | `[证据]证明先前的[判断]是错的，真正指向[新嫌疑/新规则]。` | 揭示后下一章要推进，不可反复吊胃口 |
| 关系反转 | `[角色]选择[行动]，表面是帮助，实际改变了[信任/背叛/亏欠]。` | 角色动机要可回看 |
| 艰难选择 | `主角只能保住[对象A]或[对象B]，代价是[后果]。` | 选择必须真有代价 |

## 章节连续性 delta 模板

```markdown
## continuity_delta
- timeline：本章新增或改变的时间点
- location_state：地点变化、破坏、封锁、公开/隐藏状态
- character_state：伤病、情绪、立场、关系、资源、误判
- knowledge_boundary：谁知道了什么，谁仍不知道什么
- item_state：证物、武器、信物、文件、钱、药、能力消耗
- world_rule_delta：新增规则或例外，是否暂定
- foreshadowing：seed / upgrade / payoff / debt
- forbidden_moves_check：是否触犯禁写规则
```

## 场景 handoff 模板

```markdown
- 交给技能：chinese-novel-chapter-writer / dialogue-editor / continuity-editor / hook-pacing-editor / style-polisher
- 需要读取的 reference：
- 本场不可改动：
- 本场必须强化：冲突 / 对白 / 线索 / 关系 / 节奏 / 文风
- 验收：场景结束后状态必须从[入场状态]变为[离场状态]
```

## 场景家族入口

- 悬疑、调查、线索、误导、审讯、反转：读取 `chinese-novel-scene-library-suspense.md`。
- 情感、关系拉扯、试探、误会、告白、背叛、和解：读取 `chinese-novel-scene-library-relationship.md`。
- 升级、战斗、竞赛、谈判、资源争夺、失败代价：读取 `chinese-novel-scene-library-escalation.md`。
- 世界观、规则展示、组织势力、道具能力、信息解释：读取 `chinese-novel-scene-library-worldbuilding.md`。
- 过渡章、日常缓冲、旅途、训练、调查间隙、余波：读取 `chinese-novel-scene-library-transition.md`。
- 小高潮、卷中反转、卷末高潮、伏笔回收、情绪结算：读取 `chinese-novel-scene-library-climax-payoff.md`。
- 调查程序、取证、证词矛盾、时间线复核、监控盲区：读取 `chinese-novel-scene-library-investigation-procedure.md`。
- 权谋、宫斗、朝堂、宗门、公司派系、公开仪式：读取 `chinese-novel-scene-library-power-politics.md`。
- 夺宝、潜入、救援、破阵、团队分工、撤离追逐：读取 `chinese-novel-scene-library-heist-strategy.md`。
- 生存、灾变、无限流副本、资源耗尽、逃生倒计时：读取 `chinese-novel-scene-library-survival-disaster.md`。
- 灵异、恐怖、民俗禁忌、规则怪谈、异常信号：读取 `chinese-novel-scene-library-horror-supernatural.md`。
- 喜剧、讽刺、黑色幽默、身份错位、误会升级：读取 `chinese-novel-scene-library-comedy-satire.md`。

## 搜索与创意入口

- 需要“参考知名小说”“搜索预设关键词”“同类作品结构拆解”时，先读取 `chinese-novel-search-keyword-presets.md`，只抽象结构机制，不摘录或仿写。
- 需要批量生成场景思路、前 10 章钩子、类型组合变体时，读取 `chinese-novel-premise-scene-idea-bank.md`。
