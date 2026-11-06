# Yeisme Agent Skills

Yeisme 开源 Skills 聚合仓库。它提供跨项目 Skill 的发现入口，并通过 Git submodule 挂载具备独立产品边界、发布节奏和维护责任的 Skills 仓库。

创作共创的在研规格见 [creative-grilling-owner-session-v1](openspec/changes/archive/2026-09-11-creative-grilling-owner-session-v1/proposal.md)：复用小说与做剧专用 Frontier，连接可恢复的 owner 会话。当前仅完成规格与任务设计，新增 binding 尚未实现。

## 获取

```bash
git clone --recurse-submodules https://github.com/yeisme/yeisme-agent-my-skills.git
cd yeisme-agent-my-skills
python3 scripts/validate_repository.py
```

已克隆但尚未初始化子模块时：

```bash
git submodule update --init --recursive
```

## 云端安装 AI 做剧 Skills

最方便的入口是直接从 AI 做剧仓库安装 `ai-drama-router`：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-router \
  --yes
```

查看云端全部做剧 Skills：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills --list
```

`ai-drama-router` 是短剧、漫剧、电视剧、电影、单元剧、喜剧和音频剧的统一入口。先安装 Router，再由它选择一个 primary 和最多一个必要 constraint，不要一次激活完整矩阵。

包含仓库 URL、安装命令、Router 规则、完整开发工作流开关和验收要求的提示词见 [云端集成 Yeisme AI 做剧 Skills](docs/agent-assisted-installation.md)。

通用编码、Go 后端、Go CLI、Rust/原生高性能、React/Web 前端、全栈 MVP 和快速 demo 的云端组合见 [开发 Skills 组合安装指南](docs/development-skill-combinations.md)。

## 管理任意外部项目

本仓库提供可移植的 `scripts/skills.sh`。它把本 checkout 作为 Skill source，但允许 `--project` 指向任意项目或服务器工作目录。

首次接入：

```bash
git clone --recurse-submodules https://github.com/yeisme/yeisme-agent-my-skills.git
cd yeisme-agent-my-skills
scripts/skills.sh --project /path/to/project init
```

`init` 会：

- 通过 CLI 生成项目 `.skills/source.local` 与 `.skills/profiles/root.txt`；
- 激活 `yeisme-skill-routing-governance` 管理 Skill；
- 生成项目 `.agents/skills` 与 `.claude/skills`；
- 验证 profile、managed manifest 和双 runtime。

`yeisme-builder-profile` 是可选的长期上下文 Profile，不属于安装 AI 做剧 Router 的必要依赖。需要项目路由时再按下文加入 `project-development-router`。

搜索并添加复杂 Skill：

```bash
scripts/skills.sh --project /path/to/project search "task terms"
scripts/skills.sh --project /path/to/project resolve <skill-name>
scripts/skills.sh --project /path/to/project --dry-run profile add <skill-name>
scripts/skills.sh --project /path/to/project profile add <skill-name>
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

Agent 应先阅读候选 `SKILL.md`，默认选择一个 primary workflow、至多一个兼容 domain constraint，并把独立 audit 与实现职责分开。搜索结果不是自动安装批准。

### 可选的常用开发工作流

默认 `init` 不加载完整项目流程。希望某个项目自动识别新项目、正式 MVP、快速 demo 和跳过工作流时，再显式加入轻量路由器；`grill-me` 可同时加入，但它只允许用户显式调用：

```bash
scripts/skills.sh --project /path/to/project --dry-run profile add project-development-router
scripts/skills.sh --project /path/to/project profile add project-development-router
scripts/skills.sh --project /path/to/project profile add grill-me
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

不希望项目使用这套流程时移除路由器即可：

```bash
scripts/skills.sh --project /path/to/project profile remove project-development-router
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

Ponytail 等第三方多宿主插件仍由其上游安装和更新，不 vendor 到本 source。

服务器上的 source checkout 路径是本地状态。checkout 移动后重新绑定：

```bash
cd yeisme-agent-my-skills
scripts/skills.sh --project /path/to/project configure-source
scripts/skills.sh --project /path/to/project doctor
```

更新公共 Skills 后重新同步：

```bash
cd yeisme-agent-my-skills
git pull --ff-only
git submodule update --init --recursive
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

机器读取可使用：

```bash
scripts/skills.sh --project /path/to/project status --agent
scripts/skills.sh --project /path/to/project list-source --json
```

默认输出用于人类；`--agent` 输出稳定 `key=value`；`--json` 输出单个版本化 envelope。不要提交 `.skills/source.local`，它会在 Git 项目中自动加入本地 `.git/info/exclude`。

## 独立项目

| 路径 | 独立仓库 | 定位 |
| --- | --- | --- |
| [`ai-drama/`](ai-drama/README.md) | [ai-drama-skills](https://github.com/yeisme/ai-drama-skills) | AI 做剧路由、编剧、导演、连续性、评审和生产交接 |
| [`auctra-novel/`](auctra-novel/README.md) | [auctra-novel-skills](https://github.com/yeisme/auctra-novel-skills) | Auctra 与中文长篇小说创作矩阵 |
| [`agent-workflow/`](agent-workflow/README.md) | [agent-workflow-skills](https://github.com/yeisme/agent-workflow-skills) | 通用 Agent runtime、仓库路由和 Skill 治理 |
| [`scaena/`](scaena/README.md) | [scaena-skills](https://github.com/yeisme/scaena-skills) | Scaena 生产、主体资产门禁和视频转绘 |

独立项目保留原 Skill 名称，宿主 profile 按名称解析，因此拆仓不要求调用方重命名 Skill。

## 做剧自动化工作流（DEK v1 + Bootstrap）

做剧执行链横跨 `ai-drama/` 与 `scaena/` 两个独立项目。本仓库的 [`docs/drama-execution-kernel/`](docs/drama-execution-kernel/README.md) 是**抽象设计、执行单元、合同与流程纪律的唯一真源**；两个独立仓只放指针，不重复正文。目标：把一份剧本或小说交给 Agent 后，从环境安装到生成前准备全程可自动推进、可审计、可恢复。

**总览入口**：[`docs/drama-execution-kernel/HANDOFF.md`](docs/drama-execution-kernel/HANDOFF.md)（版本、真源表、Skills/合同状态、已知缺口、后续路线）；[`implementation-roadmap.md`](docs/drama-execution-kernel/implementation-roadmap.md)（C1/C2/C3 后续实现规格与交接）。

### 设计来源：流程核心纪律提取

从外部「糯米工作流程」里只提取**流程编排纪律**，不引入其角色、脚本、Windows 路径、桌面 CLI、模型白名单或单主控会话快照；全部改用现有做剧工具的真实合同表达。

| 提取的流程纪律 | 现有承载 |
| --- | --- |
| 单一正式入口；询问/规划/审计不扩为生产任务 | `ai-drama-router`（唯一语义入口） |
| 一次理解、按阶段交接；不增加第二套状态文件 | `DramaRoutePlan v1` 的 `stage_plans[]` / `gates[]` / `canonical_owner` |
| 清单不等于已读；hash 变化刷新 | `ai-drama-context-pack-builder` + `FrozenRef` digest |
| 每集六阶段流水线 | `automation_profile` 六阶段 stage_plan（见下） |
| 判断与执行分离 | `OwnerAction` / `IdempotentGrant` / owner CLI 受控入口 |
| 完成分级、禁止互相冒充 | `Outcome` 代数（DEK） |
| 准备任务停在正片提交前 | `stop_before_final_submit: true` + 费用显式授权 |
| 已授权连续推进、进度询问不暂停、未知先核对 | `continuous_advance` + `unknown_policy: reconcile_readonly` |
| 默认不看图，优先文字档案 | `visual_review_default: text_first` |
| 单主控、子代理默认关闭 | `subagents: disabled_unless_explicit` |

### 抽象与执行单元

- **六个抽象 + 一条调度律**：`FrozenRef` / `CapabilityInvocation` / `Outcome` / `IdempotentGrant` / `LineageReuse` / `HumanGate` + `WaveBatch` → [abstract-design.md](docs/drama-execution-kernel/abstract-design.md)。
- **一个作用，三类能力**：`GenerationCapability<kind>`（`image|video|audio`）+ `GenerationBinding`；CLI / MCP / HTTP / SDK / 第三方只是绑定，流程不感知入口 → [capability-abstraction.md](docs/drama-execution-kernel/capability-abstraction.md)。
- **9 个领域 EU + 2 个横切层**：`CanonIntake` → `DrawBatch` → `GenerationInvoke<kind>` → `CandidateRecord` → `HumanSelectFreeze` → `ShotBind` → `VideoSubmit` → `Reconcile` → `BoundedReplace` / `FailedRepair`；横切 `RemoteAction` 与 `ProjectionAlign` → [execution-units.md](docs/drama-execution-kernel/execution-units.md)。
- **三份待实现合同**：`yeisme.owner_action.v1`（含 `capability_id/kind/binding_ref/retry_used/approval_ref`）、`scaena.draw_batch.v1`、`yeisme.replacement_bound.v1` → [contracts/](docs/drama-execution-kernel/contracts/)。

### 落地 Skills（按模块归位，不建第二套 owner）

| Skill | 模块 | 职责 |
| --- | --- | --- |
| `ai-drama-bootstrap` | `ai-drama/` | Router 之前的环境准备：安装 skills / CLI、配置连接、交接 Router |
| `ai-drama-action-receipt` | `ai-drama/` | 冻结引用、幂等授权、结果词汇与 UNKNOWN 恢复 |
| `ai-drama-remote-operations` | `ai-drama/` | owner HTTP 服务 + remote profile + 控制中心投影对齐 |
| `scaena-asset-draw-batch` | `scaena/` | 确认清单批量抽卡、wave 依赖、统一回查、快覆盖 |
| `scaena-bounded-replacement` | `scaena/` | `identity_equal` 门、有界替换、失败受控修复 |

`ai-drama-router` 仍是唯一语义入口；DEK 不新建 router、不建跨 owner 网关、不改变各独立项目的 owner 边界。

### 自动化核心流程

`ai-drama.route-plan.v1` 增加可选 `automation_profile`（只控制执行推进方式，不改路由选择），六阶段顺序：

| # | stage_kind | Primary | 停止条件 |
| --- | --- | --- | --- |
| 1 | `source_admission` | `ai-drama-router` + `ai-drama-context-pack-builder` | 原文未读完 / hash 漂移 / 原创性 blocker |
| 2 | `asset_gap` | `scaena-subject-asset-readiness` / `scaena-asset-draw-batch` + `GenerationCapability<image>` | wave 上游未 frozen / 无审批窗口 / binding 非 executable / 重试耗尽 |
| 3 | `director_compose` | `ai-drama-director` | 对白 / mention / 时长未冻结 |
| 4 | `semantic_acceptance` | `ai-drama-continuity-supervisor` / `ai-drama-assessment` | 语义异议 / rights / cost blocker |
| 5 | `controlled_write` | `GenerationCapability<video\|audio>` + `ai-drama-action-receipt` + `scaena-production-operator` | UNKNOWN / 写前状态不符 / 无幂等键 / 越审批窗口 / 重试耗尽 |
| 6 | `scope_completion` | `ai-drama-production-orchestrator` | 任一集未收口；**停在正片提交前** |

完成分级：`ACCEPTED / COMPLETED / BOUND / REVIEWED / STAGE_COMPLETE / EPISODE_PREPARED / FULL_SCOPE_PREPARED`；`FULL_SCOPE_PREPARED` 不等于成片或审美验收。完整门禁矩阵见 [automation-core.md](docs/drama-execution-kernel/automation-core.md)。

### 一键开始：三版提示词 + 审批窗口

`ai-drama-bootstrap` 提供三种形态，**共用同一套安全不变式与命令真源**：

| 版本 | 位置 | 适合 |
| --- | --- | --- |
| 完整版 | `ai-drama-skills/ai-drama-bootstrap/references/bootstrap-prompt.md` | 新机器、逐条审计 |
| 简短版 | 同目录 `bootstrap-prompt-short.md` | 工具已装好，快速接剧本开做 |
| 渐进式 | 同目录 `bootstrap-prompt-progressive.md` | 分层放行：L0 探测 → L0.5 审批窗口 → L1 skills → L2 工具 → L3 连接 → L4 交接，每层可独立发送可停 |
| 对照指南 | 同目录 `prompt-variants.md` | 选版本 |

**不再询问 `cli|mcp|both`**：流程只认 `GenerationCapability<kind>`（`image|video|audio`），resolver 自动选 `executable` binding，理由写入 `receipt.binding_ref`。`surface-choice.md` 已降级为 binding 参考，不再是流程门禁。

**全自动化 + 全覆盖审批**（二者用一次窗口授权统一）：

```text
ApprovalWindow = capability_kinds[] + intent_digest + binding_allowlist
                 + count + cost_ceiling + retry_budget=2 + stop_before_final_submit
DISCOVERED → APPROVED → INVOKING → (RETRY×≤2) → ACCEPTED → COMPLETED
                                    └→ TERMINAL_REJECTED / UNKNOWN / NEEDS_DECISION
```

- 窗口内全自动：自动发现 binding、自动选可执行入口、**可重试错误自动重试最多 2 次**（同 `action_id` / `idempotency_key` / `intent_digest`）、连续推进六阶段、进度询问不暂停；
- 免审批只读：`probe` / `discover` / `tools/list` / `resources/read` / `status` / `reconcile`；必须审批：三类付费生成、绑定 / 替换 / 回滚、导出 / 发布、凭据 / 连接变更、正片提交、新增 kind 或超预算；
- UNKNOWN 只 `reconcile` 且不消耗重试预算；已受理 / 业务拒绝 / 创意变化禁止重试；耗尽或越界交 `needs_decision`；
- 一张窗口可覆盖三类，但付费生成仍按动作留独立凭证；换 binding 不增加权限。

三类合同、能力发现矩阵与完整规则见 [capability-abstraction.md](docs/drama-execution-kernel/capability-abstraction.md)；命令全表见 `ai-drama-skills/ai-drama-bootstrap/references/install-and-connect.md`。

### 验证

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-runtime
scripts/skills.sh resolve ai-drama-bootstrap
```

### 明确不做

不新建第二个做剧 router 或跨 owner 网关；不把 `cli/mcp` 或具体产品名做成流程分支或必答问题；不自动付费、不自动发布、不自动派生子代理、不跑 race；不把凭据值写进日志 / stdout / 仓库 / evidence；不把 `ACCEPTED` 写成完成；不把客户端路径当远端可读文件；不把 planned / readonly 能力升级为可写；不在 UNKNOWN 或创意输入变化时重试。

## 聚合模块

| 模块 | 说明 |
| --- | --- |
| [`architecture/`](architecture/README.md) | Aigora/Seedance 架构与下一代路由设计 |
| [`audio-workflow/`](audio-workflow/README.md) | Sonora 音频 Agent 路由 |
| [`cli-runtime/`](cli-runtime/README.md) | 待按产品 Owner 继续拆分的 CLI runtime 适配层 |
| [`content-writing/`](content-writing/README.md) | 教程、游记、评测、周报和公众号内容 |
| [`creative-writing-core/`](creative-writing-core/README.md) | 创作路由、风格 Lens、安装和渐进编排 |
| [`eikona-image/`](eikona-image/README.md) | Eikona 图片生成、资产、主体与社媒视觉 |
| [`engineering/`](engineering/README.md) | 工程、CLI、后端、语言和演进约束 |
| [`frontend-design/`](frontend-design/README.md) | Web/TUI 设计、动效、前端质量与视觉验收 |
| [`game-development/`](game-development/README.md) | LLM 原生游戏方向、系统架构和垂直切片 |
| [`knowledge/`](knowledge/README.md) | 企业多模态知识路由 |
| [`mcp/`](mcp/README.md) | MCP 构建、Gateway 运维与注册治理 |
| [`pinax-agent/`](pinax-agent/README.md) | Pinax 笔记、检索、记忆、项目和发布工作流 |
| [`project-development/`](project-development/README.md) | 项目路由、规格驱动和垂直切片交付 |
| [`qa-release/`](qa-release/README.md) | 性能与集成测试证据 |
| [`role-intelligence/`](role-intelligence/README.md) | 角色蓝图和跨项目角色路由 |
| [`scriptwriting/`](scriptwriting/README.md) | 短视频、直播、播客和场景剧本写作 |
| [`social-content/`](social-content/README.md) | 小红书与社媒内容生产矩阵 |
| [`video-analysis/`](video-analysis/README.md) | Anatomia 视频分析、分镜审阅和资产交接 |
| [`web-research/`](web-research/README.md) | 互联网研究和来源验证 |

后续拆分顺序、Owner 边界和兼容策略见 [`docs/repository-split-roadmap.md`](docs/repository-split-roadmap.md)。

## Skill 目录契约

```text
<module-or-project>/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/   # 可选
  scripts/      # 可选
  assets/       # 可选
```

- 每个 Skill 目录只保留一个 Agent 入口 `SKILL.md`，不添加重复 README 或快速参考文件。
- 项目或模块说明放在其根目录 `README.md`。
- `name` 必须与 Skill 目录名一致，`description` 应明确触发条件和边界。
- 结构化状态、资产、凭据、provider payload 和项目正典不进入 Skills 仓库。
- 独立仓库不得依赖维护者机器绝对路径；宿主专用命令必须明确标为适配层。

## 验证

```bash
python3 scripts/validate_repository.py
python3 scripts/test_network_install.py
scripts/skills.sh --help
python3 agent-workflow/scripts/test_skill_manager.py
python3 ai-drama/scripts/validate_skills.py
python3 ai-drama/ai-drama-router/scripts/validate_drama_matrix.py
python3 auctra-novel/scripts/validate_skills.py
python3 agent-workflow/scripts/validate_skills.py
python3 scaena/scripts/validate_skills.py
```

## License

聚合仓库采用 [MIT License](LICENSE)。每个独立子仓库也包含自己的许可证；产品源码仓库的可见性和许可证以对应仓库为准。

## CI/CD

- [模块化、分级 CI/CD](docs/ci-cd.md)：quick、full、integration、release 的触发场景、真实命令和权限边界。
