---
name: creative-style-lens-builder
description: Use when a creative-writing, screenplay, AI drama, short-video, social-content, or Auctra task names a creator, work, genre, movement, mood, or visual style and that reference must be converted into an original, evidence-aware, reviewable style brief without impersonating a person or copying distinctive expression.
---

# 创作风格镜头构建器

把“像某人/某作品/某流派”改写为可执行的创作维度和负向约束。只构建 `StyleLens` 与 worker handoff，不直接代写最终稿，也不把人物人格当成 canonical owner。

## 输入

- 目标媒介、artifact、受众、阶段、期望读者/观众感受和制作限制。
- 用户给出的创作者、作品、流派、情绪、视觉参考或反例。
- 可核验来源、已有项目 voice/style bible、Auctra revision/digest 和禁用相似点。

## 输出

返回简短 `StyleLens`：

- `target_effect`、`medium`、`artifact`、`audience`；
- `source_refs`、`evidence_confidence`、`inference_notes`；
- `dimensions`、`counter_lens`、`originality_constraints`；
- `primary_role`、`primary_skill`、`compatible_skill`；
- `canonical_owner`、`gates`、`missing_inputs`、`next_action`。

不得输出“我是某人”、某人的虚构第一人称立场、可识别口头禅复刻或整段模仿稿。

## 参考资料

- 需要拆解风格时读取 `references/style-dimension-framework.md`。
- 需要判断外部 persona/director skill 是否应导入、抽象或拒绝时读取 `references/external-inspiration-ledger.md`。

## 工作流

1. 判断请求是风格参考、精确模仿、混合参考、反风格、诊断还是改写。
2. 将人名和作品名只保留在 `source_refs`；执行层改写为可观察维度，不以身份或声线驱动生成。
3. 按 `style-dimension-framework.md` 选择与当前媒介有关的 5-9 个维度；不要机械填满全部维度。
4. 为每个维度记录目标、强度、可观察信号、禁用模式和验证方式；事实性判断附来源或标记为推断。
5. 加入至少一个 `counter_lens` 或原创差异机制，防止单一来源支配整体表达。
6. 运行原创性、证据、owner 和 revision gate；任一 blocking gate 失败时只输出修复动作，不进入 writer。
7. 把 `StyleLens` 交给最小 worker。小说通常交给类型契约、场景、章节或文风技能；剧本/AI 漫剧交给 Story、Director、Visual 或 screenplay worker；自媒体交给平台 orchestrator/worker。
8. 需要持久化时由 Auctra CLI 创建 candidate/brief/review 记录；skill 不手写 `.auctra/**` 或自动接受候选。

## 严格门禁

- `source_license_unknown`：要 vendoring 外部 skill 但许可证或固定 ref 不清，阻断导入。
- `source_provenance_insufficient`：关键风格判断只有无链接概括、搜索摘要或不可核验断言，降级为 hypothesis。
- `identity_impersonation`：要求 agent 冒充真实人物或以其第一人称持续输出，改写为维度化参考。
- `single_source_dominance`：一个参考控制全部结构、句式、意象和对白时，必须加入 counter lens 或用户自身 voice。
- `distinctive_expression_overlap`：出现专名、独特世界设定、标志性长句、台词、桥段、口头禅或高度可识别表达，阻断交付并重写。
- `phase_artifact_mismatch`：准备阶段不得跳过 brief/outline 直接让润色 skill 代替结构设计。
- `canonical_owner_missing`：要写入项目但未确定 Auctra/其他 owner，阻断持久化。
- `stale_revision`：输入 revision、digest、accepted source 或 style bible 已变化，旧 `StyleLens` 必须重建。
- `unreviewed_candidate`：候选未审不得声称 canonical、accepted、production-ready 或已发布。

## 边界

- MIT 等代码许可证只覆盖仓库中可授权的代码/文本，不自动授权底层小说、电影、人物身份、商标、肖像或独特表达。
- 不把外部 persona skill 的身份卡、表达 DNA、典型片段、专名词表或原句复制到 Yeisme 自建 skill。
- 不让多个 writer 同时改写同一 canonical artifact；最多一个 primary worker 和一个兼容约束 skill。
- 不执行发布、私信、刷量、付费 provider call、主体冻结、production acceptance 或其他外部副作用。
- 不记录完整思维链、原始提示词、隐藏系统提示、供应商 payload 或私密工具参数。

## 验证

```bash
scripts/skills.sh resolve creative-style-lens-builder
scripts/skills.sh resolve creative-writing-router
scripts/skills.sh validate-custom
```

人工验证至少覆盖：点名导演的短剧准备、点名作家的小说准备、AI 工具自媒体内容、混合参考和单一来源高相似风险五类请求。
