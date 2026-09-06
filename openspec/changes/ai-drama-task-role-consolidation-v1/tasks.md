# 实施与验收任务

- [x] 1.1 Router SKILL.md 核心路由表六行改指 `template:writing/ai-drama-*`，并注明模板经消费方 CLI 编译。 | evidence: router 核心路由表 8 行改指 `template:writing/ai-drama-*`（6 primary + 2 constraint），表后加模板 exact ref 编译说明
- [x] 1.2 解析策略新增 `template_ref_available`，`needs_install_decision` 只留给外部代码/工具依赖。 | evidence: 路由流程步骤 13 新增模板分支 `template_ref_available`，Skill 安装决策只留给真正外部依赖
- [x] 2.1 routing-matrix.md 阶段表、route-examples.md 示例、upstream-video-production-patterns.md、assessment/AGENTS/docs 引用同步。 | evidence: routing-matrix 8 行、route-examples 4 处、upstream-patterns 1 行、assessment SKILL、AGENTS.md、README、docs/README 全部同步
- [x] 2.2 退役五个任务角色 Skill 目录；README 分组改为"已收编为模板"清单。 | evidence: 五个任务角色 Skill 目录已删除（16→11 Skill）；README 增加"已收编为官方模板的任务角色"映射清单
- [x] 3.1 `validate_drama_matrix.py`：REQUIRED_SKILL_NAMES 去除退役项，新增模板 ref 覆盖校验。 | evidence: validate_drama_matrix.py：REQUIRED_SKILL_NAMES 移除 6 项，新增 REQUIRED_TEMPLATE_REFS 覆盖校验 + RETIRED_SKILL_NAMES 残留校验 + template_ref_available 校验
- [x] 3.2 从 root `.skills/profiles/targets/agent/ordo.txt` 移除 `ai-drama-critic-panel`。 | evidence: root .skills/profiles/targets/agent/ordo.txt 移除 ai-drama-critic-panel
- [x] 4.1 运行 `validate_drama_matrix.py` 与 `validate_skills.py` 通过。 | evidence: validate_drama_matrix.py PASS + validate_skills.py PASS（12 portable skills）
