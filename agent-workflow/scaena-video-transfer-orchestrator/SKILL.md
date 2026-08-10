---
name: scaena-video-transfer-orchestrator
description: Use when operating an existing-decomposition Scaena video-transfer project, especially validating a reference package, adapting it to a new market, sampling Eikona character/style assets, preparing pixel-locked character masks, reviewing continuity, creating a first-shot canary, or handing off a reference-video generation request; keep Anatomia, canonical state, provider calls, subject freeze, mask acceptance, cost approval, and production acceptance behind explicit gates.
---

# Scaena 视频转绘编排

把“已有拆解包 + 原视频运动参考 + 新市场视觉方向”路由成可暂停、可审阅、可恢复的 Scaena 测试流程。这个 skill 只管理对话阶段、工具选择、门禁和 handoff；Scaena 拥有生产状态，Eikona 拥有视觉 run/artifact，Auctra 拥有剧本和 canonical story，Pi 不直接写这些状态。

## 适用边界

- 适用于 `data/scaena-video-transfer-lab` 或同结构的已有拆解视频转绘项目。
- 默认从 `package_ready` 开始；已有角色、场景、分集和分镜时，不重新调用 Anatomia。
- 默认市场是 `korea`，视觉是 `korean_contemporary_cinematic_drama`，语言是 `ko-KR`；用户的新选择覆盖默认值，但必须记录成新的 adaptation/style decision。
- “预览生成成功”只表示候选任务完成，不表示 accepted、frozen、production-ready 或可发布。

## 阶段路由

按 [references/phase-gates.md](references/phase-gates.md) 判断当前阶段，只推进一个最小阶段：

```text
package_ready
  -> adaptation_pending
  -> style_sampling
  -> style_locked
  -> asset_batch_planned
  -> asset_batch_running
  -> assets_review
  -> shot_preview_running
  -> shot_review
  -> prompt_revision
  -> final_generation
```

用户的“继续”只表示继续检查和提出下一动作，不能自动等价于付费调用、接受候选、冻结主体、绑定镜头或导出。

当用户明确要求“原场景完全保留”“像素锁定”“第一个视频第一个分镜”时，切换到像素锁定 canary 分支：

```text
source_registered
  -> chunk_locked
  -> eikona_candidates_review
  -> subjects_frozen
  -> mask_pending_review
  -> mask_accepted
  -> manifest_validated
  -> canary_cost_approved
  -> provider_task_created_once
  -> pixel_lock_composite_review
```

详细经验和停点读取 [references/pixel-lock-production-lessons.md](references/pixel-lock-production-lessons.md)。

## 交互路由

### 1. 用户说“帮我拆解视频”

1. 说明本项目已经完成拆解。
2. 调用只读 MCP 工具 `scaena.transfer.package.validate`，默认读取项目相对路径 `inputs/reference-assets/归档.zip`。
3. 调用 `scaena.transfer.context.show`，读取市场适配上下文。
4. 若返回 `status=ok`，只询问最小决策：关系和动作顺序是否保留；B 是否只改外貌，还是同时改姓名、服装和背景；目标市场/语言是否为韩国。
5. 若返回 `blocked|failed`，先修复 package，不生成图片或视频。

### 2. 用户说“我希望生产韩国风格的”

将需求拆成两个独立决定：

- `market_profile`：姓名、学校/住宅、服装、生活物件、韩文标识、字幕和文化语境。
- `visual_profile`：摄影、灯光、色彩、镜头、材质和真实感。

先生成小样本：A identity、B identity、A+B relationship frame、Korean environment frame。样本必须绑定同一个 style revision、market profile 和 reference lineage。未确认前只允许 candidate/lookdev。

### 3. 用户说“这个风格可以，下一步”

先回传风格版本、候选清单、预计批次、预算/权限状态和阻塞项，等待明确的 style-lock decision。确认后再创建资产批次计划；不要直接启动整批生成。

### 4. 用户说“开始第一集视频”

先选一个 2–5 秒哨兵镜头，要求同时验证 A/B 关系、动作因果、原视频运动/机位和结束构图。若 subject/style/reference/preflight 尚未冻结，只能生成 non-production shot preview；生产视频必须停止并返回 readiness blocker。

若真实源视频尚未登记，本地 CLI 可以把用户显式提供的单个项目外普通文件直接接纳进 CAS：

```bash
scaena source-video register --from /workspaces/yeisme-agent/temp/love-strikes-project-upload/E001.mp4 --project /workspaces/yeisme-agent/data/scaena-video-transfer-lab --json
```

该文件参数是一次瞬时只读授权，不要求项目内复制、symlink 或 hardlink staging；原始路径不得进入 receipt/evidence。登记完成后，视频参考输入必须走 Scaena 的 source-video / input-bundle durable ref 合同。不能把本地路径、`file://`、聊天附件 URL 或 provider URL 直接当作 `reference_video` ref。

## 工具边界

当前已落地的转绘专用 MCP 工具为：

| Tool | 作用 | 写入 | 下一步 |
| --- | --- | --- | --- |
| `scaena.transfer.package.validate` | 校验角色、场景、分集和分镜入口，初始化 `package_ready` | 应用服务 | `scaena.transfer.adaptation.propose` |
| `scaena.transfer.context.show` | 读取持久化阶段、韩国市场上下文和下一动作 | 否 | 当前 `allowed_actions` |
| `scaena.transfer.adaptation.propose` | 记录韩国改编简报 ref 和人物关系保留规则 | 应用服务 | `scaena.transfer.style.preview` |
| `scaena.transfer.style.preview` | 返回四个 Eikona Generation Intent 并进入 `style_sampling` | 应用服务 | `scaena.transfer.job.watch` |
| `scaena.transfer.style.lock` | 用户明确确认四张小样后的 style lock | 应用服务 | `scaena.transfer.asset_batch.plan` |
| `scaena.transfer.asset_batch.plan` | 返回六名核心角色及主角多视图资产计划 | 应用服务 | `scaena.transfer.asset_batch.generate` |
| `scaena.transfer.asset_batch.generate` | 明确确认后启动资产批次状态并返回 Eikona intents | 应用服务 | `scaena.transfer.job.watch` |
| `scaena.transfer.job.watch` | 用 job/artifact refs 推进 style、asset 或 sentinel job | 应用服务 | 阶段相关下一动作 |
| `scaena.transfer.shot_preview.generate` | 资产审核确认后只启动一个 2–5 秒哨兵镜头 | 应用服务 | `scaena.transfer.job.watch` |
| `scaena.transfer.shot_review.record` | 记录 accepted/revise，禁止自动整集 | 应用服务 | final gate 或 prompt revision |
| `scaena.transfer.prompt_revision.propose` | 保存脱敏修改原因并返回一个哨兵镜头重抽 intent | 应用服务 | 再次生成哨兵镜头 |

Pi/插件只能调用 Scaena typed API、MCP owner 或 Eikona CLI；不得在插件中拼 provider 请求、读取 `.scaena` SQLite、覆盖 manifest/evidence，或把聊天 transcript 当作事实来源。

所有 Eikona 图片 intent 在韩国转绘项目中默认显式使用 `openai/gpt-5.4-image-2`。短别名只作为兼容输入，历史 `openai:gpt-image-2` 只允许兼容读取；新的 prompt、skill、runbook 和正向命令必须保存 slash-form canonical ref。若 Eikona 回执出现双 provider 前缀、空 `original_model_ref` 或模型漂移，停止 Scaena handoff 并返回模型规范化 blocker。Pi 不保存 key，凭据只存在 Eikona user-level channel。

## 结果合同

每次工具调用都投影为短结果：

```text
status=<ok|blocked|failed|requires_action|partial>
phase=<current phase>
refs=<opaque refs>
allowed_actions=<next allowed actions>
blockers=<blocking codes>
next_user_action=<one user-facing action>
evidence_refs=<redacted evidence refs>
job_ref=<long-running job ref, when present>
```

`--json`、`--agent`、MCP result 和人类摘要必须来自同一个 typed projection。不要输出 raw prompt、provider payload、签名 URL、密钥、私有工具参数或完整模型推理。

## 连续性要求

在生成或审阅角色资产时，至少检查：身份、脸/发型、轮廓、默认服装、伤口/状态、视线、站位、关键道具和市场细节。A/B 的关系位置和动作因果必须保留；人物外貌可变，但不能让角色在跨镜头中失去可识别身份。

首批核心主体建议为 6 个：女主、男主、现男友、闺蜜、背叛对象、男主女友。归档中可继续扩展到完整角色表，但配角不应阻塞首个 A/B 哨兵镜头。

## 安全停点

遇到以下任一情况，返回 `blocked` 或 `needs_input`，不自行猜测：

- package digest、角色/场景/分集/镜头入口缺失或过期；
- 用户没有确认关系保留和市场适配范围；
- 主体、风格、参考版本无法确认；
- 权限、成本、provider 能力或远端模型状态未知；
- production request 缺少 frozen subject/style/reference、generation preflight 或 exact shot binding；
- provider 返回成功但没有 artifact digest、owner receipt 或 review 状态；
- Eikona artifact 仍是 candidate、尚未完成 typed handoff/stage/apply，或 Scaena 没有 frozen `SubjectVersion`；
- 蒙版仍是 `pending_review`、退回版本没有 supersedes lineage，或审核蒙版外出现非零像素差异；
- Eikona model ref 不是 canonical `openai/gpt-5.4-image-2`，或回执出现重复 provider 前缀；
- 生产 bundle 的 `reference_video` 仍是本地路径、`file://` 或瞬时 URL，而不是已登记的 durable source-video ref；
- 需要替换或删除已有资产但没有明确确认。

## 验证入口

进入项目后优先使用真实命令：

```bash
cd /workspaces/yeisme-agent/data/scaena-video-transfer-lab
go -C /workspaces/yeisme-agent/agent/scaena test ./internal/domain/transferworkflow ./internal/mcp -run 'Transfer' -count=1
/workspaces/yeisme-agent/agent/scaena/dist/scaena --help
/workspaces/yeisme-agent/agent/scaena/dist/scaena mcp --help
```

如果源码命令失败，记录实际错误并停在 capability blocker；不要用旧二进制的成功帮助输出推断当前源码已经可运行。生产阶段另行加载 `$scaena-subject-asset-readiness` 和 `$scaena-production-operator`。

## 复用参考

- 项目流程：`data/scaena-video-transfer-lab/docs/01-韩国市场转绘交互设计.md`
- 项目阶段合同：`data/scaena-video-transfer-lab/docs/02-阶段门禁与验收.md`
- 项目工具合同：`data/scaena-video-transfer-lab/docs/03-Pi交互与工具合同.md`
- Love Strikes 实测复盘：`data/scaena-video-transfer-lab/docs/08-Love-Strikes-Scaena-Eikona生产复盘.md`
- 视频参考约束：`$ai-drama-video-reference-director`
- 主体生产门禁：`$scaena-subject-asset-readiness`
- Scaena 生产操作：`$scaena-production-operator`
