# Auctra 中文小说工作流 Mermaid 图

当需要解释 Auctra 与中文小说 skills 如何协作、如何从写前上下文进入候选稿、review、台账、优化闭环，或需要给用户/维护者展示流程时读取本文件。本文件只描述工作流和边界，不代表所有命令已经在 Auctra 中实现；命令能力缺口应在输出中单独标注。

## 端到端写章闭环

```mermaid
flowchart TD
    Start([用户提出写章/续写/修订]) --> Route[creative-writing-router]
    Route --> Project{是否是 Auctra 中文小说项目?}
    Project -->|否| Direct[按普通小说 skills 输出 Markdown]
    Project -->|是| Gate[auctra gate check --before chapter_write --json]

    Gate --> Context[chinese-novel-context-pack-builder<br/>构建最小上下文包]
    Context --> Plan{上下文足够?}
    Plan -->|否| Missing[列出 missing_inputs<br/>建议补 material / handoff 命令]
    Missing --> Context
    Plan -->|是| Writer[chinese-novel-chapter-writer<br/>生成章节候选稿]

    Writer --> ReviewQueue[Auctra review queue<br/>候选稿进入待审]
    ReviewQueue --> Review[auctra-novel-review-orchestrator<br/>缺陷登记与 review action 建议]
    Review --> Decision{建议动作}

    Decision -->|accept / partial| Ledger[chinese-novel-state-ledger-updater<br/>提取台账 delta]
    Decision -->|reject / revise| Optimize[auctra-novel-optimization-loop<br/>修订队列与下一轮上下文补丁]
    Ledger --> Optimize
    Optimize --> Next[下一轮 context patch / revision queue]
    Next --> Context
```

## Review 状态机

```mermaid
stateDiagram-v2
    [*] --> CandidateCreated: content generate / chapter draft
    CandidateCreated --> PendingReview: write review item
    PendingReview --> NeedsContext: missing baseline
    NeedsContext --> PendingReview: context pack supplied

    PendingReview --> Accepted: review accept
    PendingReview --> PartiallyAccepted: review partial
    PendingReview --> Rejected: review reject
    PendingReview --> NeedsRevision: blocking or needs_revision

    NeedsRevision --> RevisionQueued: optimization loop
    RevisionQueued --> CandidateCreated: regenerate / revise

    Accepted --> LedgerSuggested: state ledger updater
    PartiallyAccepted --> LedgerSuggested: accepted diff only
    Rejected --> ArchivedCandidate: no long-term facts

    LedgerSuggested --> ConfirmedLedger: user or app service confirms
    ConfirmedLedger --> [*]
    ArchivedCandidate --> [*]
```

## 写前上下文包构建

```mermaid
flowchart LR
    Bible[项目圣经/读者契约] --> Pack[context pack]
    Outline[章节大纲/场景卡] --> Pack
    State[人物状态/知识边界] --> Pack
    Foreshadow[伏笔台账/线索热度] --> Pack
    Summary[最近章节摘要] --> Pack
    Style[最近风格样本] --> Pack
    Review[review queue / handoff] --> Pack

    Pack --> Check{最小信息足够?}
    Check -->|是| Handoff[交给章节写手/审稿/修订]
    Check -->|否| Missing[missing_inputs + 建议 Auctra 命令]
```

## 写后台账建议

```mermaid
flowchart TD
    Draft[章节候选稿或接受版本] --> Source{source_status}
    Source -->|candidate / unknown| Suggest[只产出待确认台账建议]
    Source -->|accepted / partial| Extract[提取可入账 delta]
    Source -->|rejected| Ignore[不写入长期事实]

    Extract --> Character[character_state_delta]
    Extract --> Continuity[continuity_delta]
    Extract --> Foreshadow[foreshadowing_delta]
    Extract --> Event[event_index_entry]
    Extract --> Summary[chapter_summary]
    Extract --> Style[style_sample]

    Suggest --> Confirm[等待用户或 Auctra review 确认]
    Character --> Confirm
    Continuity --> Confirm
    Foreshadow --> Confirm
    Event --> Confirm
    Summary --> Confirm
    Style --> Confirm
```

## 用户反馈与规则提案闭环

```mermaid
sequenceDiagram
    participant U as 用户
    participant O as Auctra optimization loop
    participant R as review defect register
    participant C as context pack
    participant S as skill reference rules

    U->>O: 反馈“不对/不符合/太 AI/钩子弱”
    O->>R: 归因到 defect category
    O->>O: 统计同类问题次数
    alt 少于 3 次
        O-->>U: 记录为 repeated_issue_tracking
        O->>C: 输出 next_context_patch
    else 达到 3 次
        O->>S: 生成 rule_proposal
        O-->>U: 请求确认是否更新规则
    end
```

## Auctra 结构化资产边界

```mermaid
flowchart TB
    Agent[外部 agent / skill] --> CLI[auctra CLI]
    CLI --> App[Auctra app service]
    App --> State[(.auctra structured state)]
    App --> Evidence[(run evidence / review / export)]

    Agent --> Prose[普通 Markdown 报告/素材]
    Prose --> CLI

    Agent -.->|禁止手写| State
    Agent -.->|禁止伪造| Evidence

    State --> Review[review queue]
    Review --> Version[accepted version]
    Version --> Export[export]
```

## 推荐使用方式

- 需要说明“为什么写章前先整理上下文”时，使用“写前上下文包构建”。
- 需要说明“候选稿为什么不能直接改长期台账”时，使用“写后台账建议”和“Review 状态机”。
- 需要设计或汇报 Auctra 小说优化能力时，使用“端到端写章闭环”和“用户反馈与规则提案闭环”。
- 需要强调 agent 不能手写 `.auctra/**` 时，使用“Auctra 结构化资产边界”。
