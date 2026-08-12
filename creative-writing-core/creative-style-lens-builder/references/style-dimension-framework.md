# StyleLens 维度框架

StyleLens 描述“作品要产生什么效果、通过哪些可观察选择实现、哪些相似性必须避免”。它不是人物人格、作者替身或可直接复制的提示词。

## 字段

| 字段 | 要求 |
| --- | --- |
| `target_effect` | 读者/观众应感到、理解或期待什么。 |
| `source_refs` | 来源 URL、作品/材料名、访问日期、固定 commit 或项目 revision。 |
| `evidence_confidence` | `high` / `medium` / `low`；事实、解释和用户决定分开标记。 |
| `dimensions` | 只选择与当前媒介和 artifact 有关的 5-9 项。 |
| `counter_lens` | 至少一个与主参考形成差异的结构、语气、文化或受众约束。 |
| `originality_constraints` | 禁止复现的专名、设定、句式、意象、对白、桥段和口头禅。 |
| `worker_handoff` | primary role/skill、兼容约束、owner、gate 和下一动作。 |

## 可选维度

| 维度 | 要回答的问题 | 可观察信号 |
| --- | --- | --- |
| `reader_promise` | 为什么点开、追读、看完或收藏？ | 每阶段回报、悬念、信息收益、情绪回报。 |
| `narrative_distance` | 视角离人物多近？谁知道什么？ | POV、自由间接引语、旁白密度、知识边界。 |
| `temporal_architecture` | 时间如何组织？ | 顺叙/倒叙/循环/并行、时间跳跃、回忆触发。 |
| `scene_pressure` | 场景靠什么推进？ | 欲望、阻力、选择、代价、权力变化、信息增量。 |
| `pacing_density` | 单位篇幅的信息和转折密度是多少？ | 段落/镜头长度、反转间隔、静默空间、章尾钩子。 |
| `sentence_or_shot_rhythm` | 语言或镜头如何呼吸？ | 长短句、停顿、重复、运动/静止、剪辑频率。 |
| `imagery_and_space` | 意象和空间承担什么功能？ | 色彩、材质、天气、地形、道具、构图和空间阻隔。 |
| `dialogue_and_subtext` | 人物说什么、隐藏什么？ | 话轮长度、沉默、反问、语用差异、潜台词。 |
| `emotional_temperature` | 情绪外放还是克制？ | 情绪强度曲线、动作替代形容词、喜剧/悲剧距离。 |
| `social_and_theme_pressure` | 制度、阶层、文化或伦理如何影响选择？ | 资源分配、身份代价、群体规范、主题命题与反命题。 |
| `fact_and_explanation_density` | 事实、科普和解释占多少？ | 来源密度、术语解释、例证、推断标记。 |
| `production_constraints` | 什么必须能写、拍、演、剪或发布？ | 时长、场景数、演员/道具、平台格式、字幕与预算。 |

## 每个维度的写法

每个选中维度包含：

```text
dimension: scene_pressure
target: 每场至少出现一次不可撤回选择
intensity: high
signals: 目标明确；阻力升级；选择产生后果
avoid: 只靠旁白解释冲突；无代价反转
verify: 场景卡和初稿逐场检查
```

## 原创性检查

1. 删除人名后，StyleLens 仍必须可执行；否则说明它依赖身份而非方法。
2. 不使用来源作品的专名、独特设定、标志性台词、长句、桥段组合或专属意象链。
3. 单一参考必须加入用户自身 voice、目标受众、不同文化语境或反向结构中的至少一种差异机制。
4. 风格只约束可观察选择，不替代事实研究、结构设计、人物动机或 canonical review。
5. 输出前分别检查结构相似、表达相似和世界设定相似；任一过高都要回退重写。
