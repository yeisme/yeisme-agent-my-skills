# Writer 串行往返与项目反馈

访谈 Skill 不写正文。阶段理解确认 + 用户明确授权试写后，才把实际写作交给既有领域 router 选择的最窄 writer；候选返回后恢复访谈。全程不隐式创建子 Agent（除非用户明确 delegation 授权）。

## 交接规则

- 串行：一次只有一个 writer primary；访谈在 writer 执行期间暂停提问，不并行展开新 frontier。
- 便携 handoff 复用 `creative.owner-handoff.v0.1`：owner 为领域 router 选出的最窄 writer Skill；`mutation_required=true` 时 `confirmation_required=true` 保持不变；不写宿主私有命令或脚本路径。
- handoff 携带：已确认阶段范围（decided + rationale）、source refs/digest、proof 目标（success signal）、返回期望（candidate 数量与篇幅上限）。不携带 raw prompt、受保护全文或 credential。

## 候选返回（proof-return）

- 候选一律进入待审（candidate）状态；不自动 accept、不自动定稿、不自动进入生产。
- 依据候选重新打开受影响节点：证据支持/推翻哪些假设，只重开被影响分支，其余决定保留。
- 同一授权不重复索取：阶段范围与授权未变时，追加同范围试写不再重新确认；范围变化（新章节、新媒介、更长篇幅、付费生成）需重新授权。

## 用户对候选的合法选项

- 采纳某一候选并说明理由（进入 decided，附 reopen 条件）。
- 全部拒绝（reject-all）：回到 frontier，明确失败原因，选择重问、换策略或降低承诺。
- 维持基线（baseline-best）：现有写法/现状已够好，不需要本轮改动；这是合法结论，不是失败。

## 反馈作用域

- owner 已确认的项目反馈可作为本项目引用依据；引用时标注来源与版本。
- 当前项目反馈不跨项目：新作品/新项目启动时不把旧作品反馈加载为全局偏好；作者可显式推翻旧偏好，一条反馈不得普遍化。
- 未实现的后续能力，当前一律不调用、不模拟：
  - F1 跨作品个人偏好（personal style/preference profile）；
  - F2 多作者风格参考聚合；
  - F3 自动候选创作 + 人类总审（auto-draft with human final review）。
  以上只在路线记录中可见；没有对应 capability 就返回 `needs_contract`，不假装存在。

## 反馈冲突处理

- 新反馈与旧决定冲突时，展示两者（来源、时间、理由），由作者裁决；Agent 建议标注为 proposal。
- 冲突裁决写入决定的 rationale 与 reopen 条件，供后续恢复引用。
