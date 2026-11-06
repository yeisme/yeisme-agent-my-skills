# 生成能力抽象（Capability / Binding Split）

> DEK v1 的作用层抽象。**一个作用**：`GenerationCapability<kind>`，`kind = image | video | audio`。CLI / MCP / HTTP / SDK / 本地 / 第三方产品都只是 `GenerationBinding`，流程不感知入口。本文是抽象与流程的唯一真源。

## 一、四个对象

| 对象 | 内容 |
| --- | --- |
| `GenerationIntent` | `FrozenRef{ref,digest}` + typed controls + `IdempotentGrant` + `approval_ref`；不接受自由文本反向推断尺寸 / 模型 / 预算 / 权限 |
| `GenerationCapability<kind>` | 唯一作用 `invoke(intent) -> GenerationReceipt`，`role = generator`；不因入口分裂 |
| `GenerationBinding` | `discover() -> executable\|planned\|readonly\|unavailable\|needs_contract`；`adapt(intent)` / `normalize(response)` / `reconcile(action_id)`；`surface` 只是描述标签，不是流程分支 |
| `GenerationReceipt` | `action_id, kind, run_ref, artifact_refs[], outcome, readback_ref, event_cursor, binding_ref, retry_used, approval_ref` |

```text
GenerationIntent (FrozenRef + typed controls + IdempotentGrant + approval_ref)
        │
        ▼
GenerationCapability.invoke()          ← 流程只看到这一层
        │ capability resolver：discover() → 选 executable binding（理由写入 receipt）
        ▼
GenerationBinding.adapt() / normalize()
        │ cli | mcp | http | sdk | local | third_party
        ▼
GenerationReceipt (统一 Outcome / event_cursor / redaction)
```

**等价准则**（四条同时满足才算同一个作用，与协议 / 产品 / 语言 / 传输无关）：同一 Intent、同一 Receipt 形状、同一 IdempotentGrant / cost / redaction、可被同一 `reconcile` 只读恢复。不满足任一条 → `needs_contract`，不靠换 binding 混进流程。

**关键不变量**：Binding 只声明自己实际能做的；换 Binding **不得**给 Capability 增加新权限。成本、授权、幂等、回读、脱敏全在 Capability 层。

## 二、三类合同

| | `image` | `video` | `audio` |
| --- | --- | --- | --- |
| operations | `generate / edit / variation / upscale` | `generate / edit / extend / motion-preview` | `render / voice / SFX / music / mix / audition / replace` |
| typed controls | model、`size WxH`、quality、count、references、reference_mode、canvas、budget | model、channel、duration、ratio、resolution、reference roles/ordinals/counts、output/audio policy、capability maturity | cue timing、voice permission、rights、sync confidence、editability、review、`final_mix_owner_ref` |
| 真实入口（binding 无关） | `eikona generate --model openai/gpt-image-2.5-sunburst --quality high --size WxH --agent`；`eikona.execute{action:generate,args:{...}}`；`POST /api/v1/generate` | `scaena video generate`；`scaena video model list --json`；`workflow.submit_scaena_request`（Eikona MCP，走同一 application service，不 shell out） | `sonora` CLI：`audio` / `episode-audio` / `audition` / `generate` / `handoff` / `candidates` / `cue` / `audio-readiness`；`sonora-agent-router` |
| 公共约束源 | `eikona.visual_intent.v1`；`actions.describe` / `models.list` 参数 guide（size 为 16 倍数、总像素 655360–8294400、quality 枚举；`high` ≠ 2K，`max` ≠ 4K） | `video_request_constraints.cjs`；`durationPolicy=fixed\|map` 绑定 `directorDurationSec`；新提交不带 `durationAnchor`；exact model/channel lock 优先 | 逐镜版本化 `ShotAudioIntent` → audio-owner handoff；`video_native` / `replace_after_generation` |
| receipt 锚 | `run_id` + `eikona://artifact/<handle>` / `eikona://asset/<id>` + `eikona.asset_handoff.v2`（`permission: handoff_candidate`） | `submission_ref` + Aigora execution receipt + `pending_review` | audio owner 注册项 + `audition` 审听证据 + `final_mix` ref |
| 特有门禁 | 远程参考输入必须服务端可达 `eikona://` URI（`invalid_reference` 拒绝客户端绝对路径）；不重复描述已有资产服装颜色；`--quality high` + 像素 `--size WxH`，禁 `--size 2k`；`codex:imagegen` 1K 约束来自 typed evidence | 必须有 `ShotAudioIntent`；reference 数量 / 比例 / 时长锁死；`unknown_accept` 只 `reconcile`；面板展示不一致单独报告，不重试生成 | `video_native` 缺 rights/sync/voice/review 必须降级为 audio owner 补配或整镜 `replace_after_generation`；Sonora 默认**不是**逐句对白第一生产者（配乐 / SFX / 混音 / 原生音轨登记审听 / 失败句补配）；原生音轨独立审听 |

三类共用：`artifact_ref` path-free、digest 为唯一复用键、`ACCEPTED ≠ COMPLETED ≠ BOUND ≠ REVIEWED`、凭据只在 owner 侧、planned / readonly / unavailable 不升级为可写、不返回 provider key / raw payload / 全链路推理。

### 能力发现矩阵

| Binding | `surface` | 发现入口 | `ref_mode` | 状态 |
| --- | --- | --- | --- | --- |
| Eikona CLI | `cli` | `eikona setup --agent`、`--version`、CLI help | `same_host_local` 合法 | executable |
| Eikona MCP | `mcp` | `tools/list` / `inputSchema` / `resources/read`、`eikona mcp capabilities --json`、`actions.describe` / `models.list` | `server_reachable_uri` + `asset.upload.begin→PUT→complete` | executable，仅 `eikona.search` + `eikona.execute` allowlisted |
| Eikona HTTP `/api/v1` | `http` | `/api/v1/readiness` 十维、`/api/v1/mcp/actions` | `server_reachable_uri` | executable，含 OpenAI-compatible Images API 同步兼容 |
| Eikona SDK | `sdk` | typed Go SDK over `/api/v1` | `server_reachable_uri` | executable |
| 本地 `codex:imagegen` | `local` | adapter 注入 guarded stdin prompt | `same_host_local` | executable |
| Scaena video / Aigora | `owner_service` | `scaena video model list --json` / `scaena doctor --agent` | typed request ref | executable |
| Sonora | `owner_service` | `sonora` CLI / `sonora-agent-router` / `scaena://input/capabilities` | audio-owner handoff | executable |
| 第三方生图 / 视频 / 音频产品 | `third_party` | 自身 conformance 声明 | 需声明 | 默认 `needs_contract`，验过四条等价准则才纳管 |

`DeniedActionError` 对「未知」与「无权限」返回相同 → 停止重估 lane，不枚举探测 action 名。

## 三、全自动化流程（策略 A）

```text
DISCOVERED → APPROVED → INVOKING → (RETRY×≤2) → ACCEPTED → COMPLETED
                                    └→ TERMINAL_REJECTED / UNKNOWN / NEEDS_DECISION
```

1. `probe/discover`：只读探测三类 binding 的 `executable` 与 `declared_operations`，出候选表；
2. 用户给**一次审批**，生成 `ApprovalWindow`；
3. resolver 在窗口内自动选 binding、调 `invoke()`，**不询问 cli/mcp**；选择理由写进 `receipt.binding_ref`；
4. 可重试错误按 `retry_budget` 自动重试；
5. UNKNOWN 走 `reconcile` 只读，**不消耗重试预算**；
6. receipt → `event_cursor` → 控制中心同一 `action_id/revision`；越界或耗尽交回 `needs_decision`。

## 四、有界重试（`retry_budget = 2`）

| | 规则 |
| --- | --- |
| 可重试 | 瞬时网络 / 5xx / 429 / 超时且 `mutationAttempted=false`；`binding=unavailable` 换另一个 executable binding；能力发现漂移 |
| 禁止重试 | UNKNOWN 写、付费已受理 / `ACCEPTED`、业务 / 权限 / 语义拒绝（TERMINAL_REJECTED）、创意输入变化、模型 / 正文 / 时长 / 渠道变化 |
| 每次不变 | 同一 `action_id` + 同一 `idempotency_key` + 同一 `intent_digest` + 同一审批窗口；换 binding 记录理由；不新建 state、不改预算 |
| 耗尽 | `needs_decision` 交回人，保留全部尝试证据；不自动扩大预算、不换工具重发 |
| 重试 ≠ 重投 | `reconcile` 只读查原 `action_id`，不产生第二次 provider submit |

`retry_budget` 默认 2，可由 `ApprovalWindow` 覆盖；`retry_used` 写入 receipt。只读 `reconcile` 与 `discover` 不消耗预算。

## 五、审批窗口（全覆盖）

**一次审批 = 一个受边界的自动化窗口**：窗口内全自动（含自动重试、自动选 binding），越界必须重新审批。这同时满足「全自动化」与「凡 agent 发起的非只读动作都要审批」。

```text
ApprovalWindow
  capability_kinds[]        # image | video | audio 白名单
  intent_digest / scope_digest
  binding_allowlist         # 允许自动切换的 executable binding
  count / cost_ceiling
  retry_budget = 2
  stop_before_final_submit = true
  originality_decision_ref
  granted_by / granted_at / raw_authorization_ref
```

| 免审批（只读） | 必须审批 |
| --- | --- |
| `probe` / `discover` / `tools/list` / `resources/read` / `status` / `reconcile` | 三类付费生成、素材绑定 / 替换 / 回滚、`select` / `freeze`、导出 / 发布、凭据 / 连接变更、正片提交、新增 kind 或超预算 |

规则：

- 审批绑定 `(capability_kinds, intent_digest, binding_allowlist, count, cost_ceiling, retry_budget)`；任一漂移或新增动作重新审批；
- 一张窗口可覆盖三类 `capability_kinds[]`，但**付费生成仍按动作留独立凭证**；
- `both` / 多 binding 不重复审批；「继续」/ 进度询问不重置也不扩大授权；
- 付费生成与正片提交始终是独立新授权，不被窗口内的自动推进覆盖。

## 六、与既有抽象的关系

| 既有抽象 | 变化 |
| --- | --- |
| A1 `FrozenRef` | 不变；成为 `GenerationIntent.intent_ref` / `constraints_ref` |
| A2 `OwnerAction` | **细化为 `CapabilityInvocation`**：一个动作 = 一次 Capability 调用；owner 仍持有真源，Binding 不建第二真源 |
| A3 `Outcome` | 不变；`GenerationReceipt.outcome` 用同一词汇 |
| A4 `IdempotentGrant` | 不变且**上移**到 invocation；换 binding 不绕过 `--confirm` |
| A5 `LineageReuse` | 不变；`artifact_ref.digest` 是唯一复用键，与哪个 binding 产出无关 |
| A6 `HumanGate` | 不变；`review decide --confirm` / `select --actor human` 仍在 Capability 层 |
| B1 `WaveBatch` | 不变；调度器只调 `Capability.invoke()`，不感知 binding |
| C1 `yeisme.owner_action.v1` | 增加 `capability_id / kind / binding_ref / retry_used / approval_ref` |
| C2 / C3 | 不变 |

`ai-drama-router` 仍是唯一语义入口；`automation_profile` 增加 `retry_budget` 与 `approval_window_ref`。

## 七、明确不做

- 不新建第二个做剧 router、不建跨 owner 网关（root `owner-hosted-remote-profile` 已判 reject-now）；
- 不问 `SURFACE=cli|mcp|both` 作为流程门禁；入口差异只在 binding 层；
- 不把 `planned / readonly / unavailable` 升级为可写，不虚构上传动作；
- 不因换 binding 放宽成本 / 授权 / 引用 / 幂等 / 脱敏；
- 不把客户端绝对路径当远端可读文件，不把 `eikona accepted` 写成 `production_ready`；
- 不自动付费、不自动发布、不自动派生子代理、不跑 race；UNKNOWN 不重投。
