## Context

`scaena-storyboard-breakdown` 已存在于 `.skills/yeisme/scaena`，也已进入 `agent/scaena` profile。它当前正确地把Scaena视为state owner、Dramaturge视为model owner，并覆盖source/run/review/revise/patch/accept/export；缺口主要是：

- instruction profile仍用Skill ref表达，未绑定official PromptRepo solution；
- 没有typed direction/profile选择流程；
- local run只入队，Skill没有foreground/watch/diff/findings的清晰模式选择；
- preflight对owner readiness、PromptRepo和format decision不够系统；
- 用户一句“继续”容易被误读为run/accept/export授权。

本change只更新现有Skill及references；不新增同义Skill、不修改CLI/HTTP/MCP实现、不自动改变profile activation。

## Goals / Non-Goals

**Goals:**

- 让Skill输出一个最小、符合`ai-drama.route-plan.v1`语义的director plan。
- 把host workflow、primary directing Skill和continuity constraint分开。
- 从明确项目/用户事实选择scenario profile，缺关键format时fail closed。
- 先做provider-free capability/Prompt/source/direction preflight，再请求一次cost-bound run授权。
- local优先foreground；remote/MCP保持async polling。
- 借助watch/diff/findings把review、revise/patch和accept gate做成明确循环。
- 保持Skill只输出refs/digests/counts/findings/actions，不持久化业务状态。

**Non-Goals:**

- 不把Prompt正文复制进Skill。
- 不让Skill变成Dramaturge provider client、Scaena state machine或候选writer。
- 不自动安装、启用、更新Skill或profile。
- 不自动accept/reject/export/出图/视频/发布。

## Decisions

### 1. Operation Skill不是director stage的第二个primary

`scaena-storyboard-breakdown` 是host workflow adapter：负责收集输入、调用Scaena、呈现结果和保留gate。它生成的`DramaRoutePlan`中：

```text
phase=director_plan
primary_skill=ai-drama-director
compatible_skill=ai-drama-continuity-supervisor
canonical_owner=production_owner
owner_binding=scaena
```

本Skill自身不进入`primary_skill`字段，也不与`ai-drama-director`竞争artifact ownership。它通过owner action/next action调用Scaena。

### 2. Intake只问会改变结构的最少问题

Required facts：

- project/source/episode；
- format/profile或足以确定profile的accepted project fact；
- target duration、aspect、shot range（可来自profile defaults）；
- exact Prompt template address（可用compat default）；
- owner connection、exact model、cost cap；
- execution host：local CLI或remote/MCP。
- exact episode boundary与owner capability input/output estimate。
- source classification、execution policy与provider retention/training/region facts。

如果“竖屏短剧/漫剧/广告/对话密集”、时长或画幅不明且会改变分镜，Skill返回`needs_format_decision`，先使用`ai-drama-format-strategist`或询问用户。不得只看剧本文风自行猜profile。

如果输入含多个episode或whole-episode estimate超出current capability，Skill只提供拆集、选择新exact model或调整明确direction的决策，不允许截断、隐式chunk、跨集合并或silent fallback。Multi-episode batch是后续Scaena orchestration surface，不由Skill用循环shell命令伪造canonical batch state。

如果project已有accepted profile/direction snapshot，优先复用exact ref/digest，不重复提问。

### 3. Profile routing

| Evidence | profile_id | Status |
| --- | --- | --- |
| accepted vertical short-drama project + 9:16/60–90s | `vertical-short-drama-v1` | first-support target |
| explicit dialogue-preservation job | `dialogue-dense-v1` | exploratory |
| explicit manga/dynamic-comic storyboard | `manga-panel-v1` | exploratory |
| explicit 15–30s product/CTA microdrama | `ad-microdrama-v1` | exploratory |
| ambiguous/conflicting | none | `needs_format_decision` |

Exploratory profile可运行provider-free fixture/component；live run前Skill必须展示maturity并要求用户确认实验性质。

### 4. PromptRepo compatibility mapping

Default exact address：

```text
promptrepo://official/video/ai-drama-storyboard-breakdown@1.0.0?locale=zh-CN
```

Legacy：

```text
skill:scaena-storyboard-breakdown + version=1
```

只作为compat ingress。Skill输出/命令优先使用`--prompt-template`，不读取或复制Prompt body。若用户明确给出另一个exact address，Skill先inspect/validate并展示ref/digest/maturity；不替换为latest。

### 5. Provider-free preflight使用真实命令

Skill开始时先检查真实command tree：

```bash
scaena storyboard breakdown run --help
scaena storyboard breakdown watch --help
scaena storyboard breakdown diff --help
scaena production status --project <project-path> --json
scaena prompt-asset repository doctor --json
scaena prompt-asset catalog inspect '<promptrepo-address>' --json
scaena prompt-asset catalog validate '<promptrepo-address>' --json
```

Preflight输出：source/profile/direction/prompt/owner/config/readiness/model/cost cap facts、provider call count=0、durable writes（help/status/inspect/validate均0；source import除外）和下一动作。

Skill不得根据设计文档猜尚不存在的command/flag。如果foreground/watch/diff尚未实现，返回`capability_missing`并使用当前async run/show路径；不能伪装已可用。

### 6. Local foreground与remote async是两条interaction projection

#### Local verified runtime

```bash
scaena storyboard breakdown run ... --foreground --timeout 10m --events
```

Skill等待到`review_required|failed|cancelled|WAIT_TIMEOUT`。Timeout后保留原ref并调用watch；不new idempotency key、不cancel。

#### Remote/API/MCP

Skill调用async run，获取breakdown ref，然后：

```text
run -> status/resource -> review -> revise/patch -> status -> accept/reject/export
```

MCP不要求long blocking tool。宿主可管理poll interval/notification，但不能让Skill重新submit。

### 7. Stable idempotency and approval packet

在run/revise前，Skill向用户呈现：

```text
source_ref/digest
direction_profile/ref/digest + duration/aspect/shot range
prompt template address/digest/locale/maturity
owner readiness/capability receipt
source classification + execution policy ref/digest
provider data policy ref/digest + retention/training/regions/expiry
connection_ref (not secret)
exact provider/model
fallbacks
max_attempts
max_cost_usd
write/cost effect
```

只有当前用户明确确认后执行一次mutation。Skill生成稳定idempotency key时，key必须绑定同一intent；`IDEMPOTENCY_CONFLICT`后先比较intent，不换key掩盖冲突。

“继续”“看看”“下一步”只允许read-only status/watch/review，除非上下文中当前动作和影响已经明确呈现并得到确认；不得跨越cost或canonical/export gate。

### 8. Review loop

Review顺序：

```text
safe summary
  -> direction summary
  -> findings
  -> shots
  -> explicit dialogue/prompt detail only when needed
  -> director + continuity assessment
  -> revise or typed patch
  -> reload current head / diff
  -> human accept or reject
  -> optional export
```

Skill在accept前必须呈现：

- story spine；
-逐镜beat和dramatic purpose；
- dialogue spine/保留情况；
- visual baseline/camera language；
- duration contract与实际shot total；
- coverage、blocking/warning findings；
- current candidate/version/digest。

这满足AI drama director gate，也不等于用户accept。

### 9. Revise vs patch决策

Agent revise：structure、shot add/remove/reorder、source/dialogue mapping、Prompt mapping、entity/continuity大改、profile/direction变更。需要model/cost/expected-version/idempotency/current approval。

Typed patch：仅Scaena允许的九个字段。Local write，不调用owner；仍创建immutable successor。Patch后必须reload/diff，不继续使用旧head。

任何`EXPECTED_VERSION_MISMATCH`/`CANDIDATE_NOT_HEAD`只read current head并呈现drift，不自动重试mutation。

### 10. Acceptance and downstream gate

Accept要求：current head、exact version/digest、no block/unknown/stale、human actor、明确materialization approval、stable idempotency。同样，reject和export各自需要当前明确批准。

Accept后Skill只返回ProductionGraph/receipt和可选export/one-click shot-planning handoff。批量出图或视频是新的paid downstream stage，必须再次展示已接受的分镜方向并获得授权；本Skill不调用Eikona。

### 11. Output

Skill最终/中间receipt保持低token：

```text
status
route_status
profile_id / profile_maturity
source_ref / source_digest
source_classification / execution_policy_ref / execution_policy_digest
direction_ref / direction_digest
prompt_snapshot_ref / prompt_digest
owner_readiness / capability_receipt_ref
data_policy_ref / retention_mode / training_usage / processing_regions / policy_expiry
breakdown_ref / version / state
candidate_ref / version / digest
scene_count / shot_count / duration_ms / coverage_ratio
finding_count / blocking
allowed_actions
next_command_or_tool
evidence_refs
```

不输出raw source、literal dialogue、Prompt body、provider options/payload、credential、private path或full reasoning。用户显式要求detail时可展示领域内容，但routine receipt仍不复制。

### 12. Failure routing

| Code/state | Skill action |
| --- | --- |
| `needs_format_decision` | 获取format/duration/aspect，不run |
| `PROMPT_BINDING_MISSING|STALE|CONFLICT` | inspect/sync/select exact address，不provider call |
| `OWNER_CAPABILITY_UNVERIFIED|OWNER_UNAVAILABLE` | doctor/config/handoff，不fake candidate |
| `DATA_POLICY_UNVERIFIED|DATA_POLICY_MISMATCH` | inspect/update connection policy或显式重新分类，不发送source |
| `OWNER_INPUT_LIMIT_EXCEEDED|OWNER_OUTPUT_LIMIT_EXCEEDED|EPISODE_BOUNDARY_REQUIRED` | 拆集/新direction/exact model decision，不truncate/chunk/fallback |
| `COST_CAP_REQUIRED|EXCEEDED` | 请求新的明确成本决定，不提高cap |
| `WAIT_TIMEOUT` | watch original ref，不resubmit |
| `SEMANTIC_PLAN_INVALID|REPAIR_EXHAUSTED` | 显示typed findings，停止或新human-approved revise |
| `EXPECTED_VERSION_MISMATCH|CANDIDATE_NOT_HEAD` | reload/diff current head |
| `BLOCKING_FINDINGS` | revise/patch/reject/review export，不accept |
| `IDEMPOTENCY_CONFLICT` | 比较intent，用户确认真新intent后才new key |

## Skill Source Changes

预计修改：

```text
scaena/scaena-storyboard-breakdown/SKILL.md
scaena/scaena-storyboard-breakdown/references/review-and-acceptance.md
scaena/scaena-storyboard-breakdown/references/routing-and-preflight.md   # new
scaena/scaena-storyboard-breakdown/agents/openai.yaml                    # only if concise prompt needs update
```

不添加README。Complex routing/preflight规则进入reference，主SKILL保持可扫描。

## Validation

从`.skills/yeisme/scaena`：

```bash
python3 scripts/validate_skills.py
```

从root同步/验证：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-target agent/scaena
scripts/skills.sh validate-subprojects-runtime
```

Sync只在source/profile/runtime paths quiescent且root有单一writer时执行。由于Skill已在profile中，本change默认不需要profile add。

## Risks / Trade-offs

- **[Skill变长]** → 主文件保留happy path和gates，routing/preflight细节进入一个reference。
- **[Operation Skill与director Skill混淆]** → route plan明确primary/constraint，Scaena Skill只作为host workflow。
- **[命令尚未实现]** → runtime help check是硬门；缺失则使用真实旧async路径并标记capability_missing。
- **[用户不想回答过多参数]** → 只问改变结构/成本的缺失事实；project accepted profile可复用。
- **[“继续”被误判授权]** → read-only continuation与cost/canonical/export approvals分开。
- **[Prompt detail污染上下文]** → safe summary/findings first，explicit read才展开，receipt refs-only。

## Migration Plan

1. 更新routing/preflight reference和主Skill。
2. 更新review reference加入direction summary、foreground/watch/diff和PromptRepo gates。
3. 调整OpenAI metadata默认提示（若需要），保留frontmatter name/description兼容。
4. 运行本repo validator。
5. Scaena CLI child实现稳定后，运行真实help/fixture command walkthrough。
6. root单一writer执行narrow target sync/runtime validation。

## Rollback

- 恢复上一Skill body/reference，保留同名目录/frontmatter。
- 重新sync target生成runtime copies。
- Scaena旧async run/show/revise/patch/accept/export仍可用；PromptRepo address mapping由Scaena compatibility path处理。

## Open Questions

无。Skill不选择实际provider/model；它只验证并呈现用户/owner给出的exact choice。
