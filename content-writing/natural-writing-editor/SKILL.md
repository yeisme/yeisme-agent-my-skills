---
name: natural-writing-editor
description: Use when diagnosing, rewriting, polishing, translating, or giving a final editorial pass to Chinese, English, or mixed prose so it reads naturally in its real context while preserving facts, responsibility, uncertainty, terminology, and the author's observable voice. Use for 去 AI 味、降低模板感、保真润色、作者声音校准、AI 写作痕迹审阅或长文终审；do not use it to promise AI-detector evasion or to replace a domain writer's factual work.
---

# 自然文本编辑器

把“去 AI 味”当作编辑问题，而不是词语清洗问题。先保真，再判断语境，最后只修改真正损害阅读的模式。

## 任务定位

先确定五个控制项：

1. `task`：`diagnose`、`rewrite`、`final-pass` 或 `voice-calibration`；
2. `scene`：聊天/邮件、公开文章、平台内容、技术文档、学术/政策、营销或文学叙事；
3. `intensity`：`light`、`standard` 或 `aggressive`；
4. `scope`：`local`、`bounded` 或 `structural`；
5. `voice_evidence`：原稿自身、用户样稿、项目 style bible，或无可靠证据。

缺省使用 `rewrite + standard + bounded`。技术、法律、学术、事故报告和审批文本默认 `light + local`。需要具体预设时读取 [references/edit-profiles.md](references/edit-profiles.md)。

新稿创作仍由对应内容 writer 拥有；本 skill 作为终稿编辑约束。用户直接提供现稿并要求改写、润色或审阅时，本 skill 可以作为 primary。

## 编辑流程

### 1. 建立写作情境

识别说话者、读者、目的、渠道、读者下一步和不能越过的边界。没有样稿时，不虚构“作者个性”；保留原文中已经存在且适合场景的稳定习惯。

### 2. 建立保真清单

逐项保护：

- 人名、机构、产品、日期、数字、版本、金额、比例、链接、路径、命令和代码；
- 引文、来源、案例、专名、法律定义和领域术语；
- 谁做了什么、谁负责、谁批准或反对；
- 事实、估计、观点、指控、假设之间的区别；
- 否定、条件、例外、置信度、必要/禁止/建议/可选等语气强度。

引用、代码、模板示例、角色台词和用户明确要求保留的表达，不参与普通“去味”改写。

### 3. 诊断高影响模式

需要系统审阅时读取 [references/pattern-taxonomy.md](references/pattern-taxonomy.md)。先通读全文，再用模式库验证直觉；只报告满足语境、密度和实际损害三个条件的问题。

- 单个词命中不是证据；
- 规则、教程和术语表中的重复可能是必要一致性；
- 被动语态、破折号、排比、连接词和副词都不得被绝对禁止；
- 宁可保留一个可接受句子，也不要为了“像人”强行制造口语、反问、自嘲、错别字或随机长短句。

### 4. 按净收益编辑

每处依次使用以下决策门：

1. 删除后不损失信息、逻辑或必要语气：删除；
2. 信息应保留但表达过满：收紧到证据支持的范围；
3. 表达确有问题：回到“谁做了什么、依据是什么、后果是什么”后重写；
4. 找不到明显更好的版本：保留原文。

优先处理高收益问题：助手元话语残留、虚构归因、事实冲突、空泛拔高、重复段落职责、机械句壳和与场景不符的宣传口吻。不要把一种模板替换成另一种模板，也不要在多处重复同一种“人味补丁”。

### 5. 校准作者声音

有可靠样稿时，提取可观察特征：句长分布、段落密度、直接程度、术语容忍度、幽默与克制、标点和列表习惯、事实与观点的区分方式。匹配分布和选择，不复制标志性短语，不推断作者身份或私人属性。

点名作者、作品或创作者风格时，先使用 `creative-style-lens-builder` 生成原创 StyleLens，再把它作为约束交给本 skill。

### 6. 复检并交付

终稿前读取 [references/quality-gates.md](references/quality-gates.md)。至少完成两遍：第一遍只读结果，检查自然度和场景适配；第二遍对照原文，检查事实、责任、限定和受保护内容。

默认直接交付改写稿。下列情况附一份简短变更说明：用户要求解释、使用 `aggressive` 或 `structural`、存在事实/结构取舍，或有内容需要用户决定。

诊断模式返回：最高影响问题、原文证据、误判排除、建议幅度，以及一个短示例；不擅自重写全文。

## 与社区技能的关系

- 默认只运行本 skill 的一次完整编辑流程。
- `humanizer-zh` 仅在用户明确要求 Humanizer、24 类模式盘点或独立专项审阅时按需加载；不要再叠加一次全文改写。
- `de-AI-writing` 保留为第三方对照 canary，不与本 skill 默认并行处理同一稿件。
- `good-writing` 只用于用户明确要求的作者风格研究；不得复制其范文表达，也不作为通用默认风格。
- 维护、升级或纳入新的社区方案时读取 [references/community-evidence.md](references/community-evidence.md)，先通过来源、许可证、冲突和回归检查，再决定是否吸收规则。

## 边界

- 不发明事实、来源、引文、经历、情绪、细节或第一人称体验。
- 不把专业术语替换成模糊近义词，不为句式变化破坏一致性。
- 不声称文本“无法检测”、保证通过 AI 检测器或以检测器分数作为验收门。
- 不把完整提示词、隐藏系统提示、供应商载荷、私密工具参数或完整思维链写入稿件或证据。
