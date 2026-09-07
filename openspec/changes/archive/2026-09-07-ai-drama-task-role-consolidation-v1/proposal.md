## 为什么

做剧矩阵中的任务角色 Skill（形态策略、故事架构、人物引擎、分集规划、场景写作、评审团）不依赖宿主工具，本质是"方法 + 输入合同 + 输出合同"的确定性提示内容。它们已收编为官方模板 `promptrepo://official/writing/ai-drama-*@1.0.0`（见 data/yeisme-prompt-templates change `official-drama-task-role-templates-v1`）。保留对应 Skill 会让消费方重复安装、重复解析，并让同一方法论出现两处漂移源。

## 变更内容

- 路由表：六个任务角色意图的 primary 改指官方模板 exact ref（`template:writing/ai-drama-*`），constraint 与门禁不变。
- 解析策略：新增 `template_ref_available`——模板承载意图无需 Skill 安装决策；`needs_install_decision` 只保留给真正需要外部代码/工具的 Skill。
- 退役五个任务角色 Skill 目录：`ai-drama-format-strategist`、`ai-drama-story-architecture`、`ai-drama-character-engine`、`ai-drama-showrunner`、`ai-drama-critic-panel`；`screenplay-scene-writer` 路由面由 `writing/ai-drama-scene-writing` 模板承接。
- README/AGENTS/docs 分组与引用同步；`validate_drama_matrix.py` 改为校验模板 ref 覆盖。
- 保留 Skill：router、assessment（评估合同门禁）、context-pack-builder、producer、production-orchestrator、director、visual-language、edit-and-sound、continuity-supervisor、video-reference-director、project-starter、panel-handoff。

## 影响

- 独立 Agent 最短路径从"Router + 按需安装矩阵 Skill"降为"Router + 官方模板目录"。
- 不改变 DramaRoutePlan 字段、originality 门禁、artifact lifecycle 与视频模型 guidance。
- 公共发行面（ai-drama-skills）Skill 数量 16→11。
