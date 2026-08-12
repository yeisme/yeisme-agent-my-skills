# 外部创作 Skill 启发与导入决策

访问日期：2026-08-11。以下记录只用于来源审查和原创设计，不作为外部人物身份、作品表达或事实正确性的授权证明。

## 候选来源

| 来源 | 固定 ref | 仓库许可 | 可吸收的抽象设计 | 当前决策 |
| --- | --- | --- | --- | --- |
| [momozi1996/DirectorAgents](https://github.com/momozi1996/DirectorAgents) | `1a9e8047d9ed328968030341cfe146bd90712584` | GitHub metadata 与 `LICENSE` 标识 MIT | 顺序阶段 handoff、候选方案对照、首席整合、风格光谱 | 不直接导入；重写为 task role、critic panel、canonical owner 和 StyleLens |
| [momozi1996/awesome-ai-persona-skills](https://github.com/momozi1996/awesome-ai-persona-skills) | `ddb35e538b3b9e817e39f0ce0a9129b5c0a8f0c8` | GitHub metadata 与 `LICENSE` 标识 MIT | writings/conversations/expression/decisions/timeline 的研究分面、平台内容矩阵、实证/教学/结构化方法 | 不批量导入；只提炼通用任务能力和证据结构 |

## 采用的设计

1. 将“多位名人协作”改写为“不同任务角色按阶段 handoff”。角色名称表达职责，例如 Story Architect、Continuity Supervisor、Platform Editor、Fact Reviewer，不表达真实人物身份。
2. 将“辩论投票”限制为候选评审。多数票不是事实或质量证明；最终决策由 rubric、evidence、canonical owner 和用户 gate 决定。
3. 将“首席导演”改写为 canonical owner/integrator。Auctra 拥有文本、candidate、review、version 和 export；skill 只产生 proposal。
4. 将“表达 DNA/导演光谱”改写为可观察 StyleLens 维度，并加入 counter lens、负向相似性约束和 stale 规则。
5. 将“内容矩阵”改写为同一事实源面向不同平台的 artifact transformation，不复制特定博主口吻。

## 已审阅候选与 Yeisme 落点

| 候选文件 | 值得吸收的能力 | Yeisme 原创落点 | 导入结论 |
| --- | --- | --- | --- |
| `DirectorAgents/SKILL.md` | 顺序链、候选争论、首席整合、风格光谱 | `creative-role-task-map`、`ai-drama-critic-panel`、canonical owner、StyleLens dimensions | 高价值结构，只抽象，不导入 persona orchestrator |
| `DirectorAgents/skills/bongjoonho-perspective/SKILL.md` | 类型外壳、社会/阶层压力与空间关系 | `social_and_theme_pressure`、`scene_pressure`、`imagery_and_space` | 不导入；禁止“像某导演那样拍”触发 |
| `DirectorAgents/skills/akirakurosawa-perspective/SKILL.md` | 动作、天气、群体调度和动态构图的观察方向 | `scene_pressure`、`sentence_or_shot_rhythm`、`production_constraints` | 不导入；只保留可观察 craft lens |
| `Novelists/liucixin-skill/SKILL.md` | 科学概念→社会冲突、宏观尺度、极端情境测试、科学事实核验 | 科幻 genre contract、`fact_and_explanation_density`、`temporal_architecture`、`internet-access` evidence gate | 中等价值；不导入活跃作家 persona/文风模仿 |
| `zimeiti/baoyu-skill/SKILL.md` | 分级教学、先实测再推荐、平民化解释、反焦虑 | Researcher → Tutorial Writer handoff；证据先行、分层教学、能力边界 | 高价值方法；不用人物口吻和账号身份 |
| `zimeiti/qiuzhi2046-skill/SKILL.md` | 痛点前置、实操验证、多平台内容矩阵、产品经理结构 | Platform Strategist → Researcher → Long/Short Writer 顺序 handoff | 高价值工作流；易受时效和个人事实影响，不导入 persona |
| `zimeiti/lijigang-skill/SKILL.md` | 精准压缩、结构化变量/条件/输出、哲学追问 | Brief Architect、information architecture、prompt/workflow review | 中等价值；Lisp/标志格式可能高度可识别，只抽象结构 |

上述“高/中价值”评价指任务方法对 Yeisme 的适配度，不是对人物、作品或仓库整体质量的排名。

## 拒绝直接导入的原因

- 多个 skill 以“像某人那样写/拍”“模拟口吻”“复刻人格”为核心触发，与 Yeisme 的原创性和 owner 边界不一致。
- DirectorAgents 的导演匹配脚本把自然语言语义编码为 shell 关键词和固定人名表，违反 Yeisme skill routing governance。
- 部分研究附件只有“来源：访谈/作品/评论”等概括，缺少逐条 URL、发布日期或 claim-level citation；不能直接作为高置信事实。
- MIT 许可不自动覆盖被分析者作品、第三方语料、人物身份、商标、肖像或底层版权表达。
- 批量安装 31+ 导演和 100+ persona 会造成触发冲突、上下文膨胀、多个 writer 竞争和 profile 难以治理。

## 未来 canary 条件

只有同时满足以下条件，才可考虑把单个外部 skill 放入 `.skills/imported/`：

1. 使用明确仓库 URL、固定 commit 和单一 module 运行 `scripts/skills.sh import`。
2. 每个关键 claim 有可核验来源；不把原作长段、台词、独特表达或未经授权语料带入仓库。
3. 触发改成任务职责，不要求身份冒充或精确文风复刻。
4. 与现有 router/worker 没有重名、重叠 writer 或 owner 冲突。
5. 通过来源 diff、license review、prompt-injection review、skill validation 和至少五类 forward scenario。
