---
name: project-development-router
description: Use when starting, scaffolding, architecting, or implementing a new project or MVP, or when delivery spans product intent, shared specifications, frontend/backend work, integration, QA, or release; choose quick-demo, full-project, or workflow-off before loading the smallest compatible workflow.
---

# 项目开发工作流路由器

把新项目、MVP 和跨栈交付请求先分成 `quick-demo`、`full-project` 或 `workflow-off`，再选择最小可用技能链。路由器只负责模式、owner 和下一道门；不要把所有技能一次性加载，也不要让实现 agent 自行补全产品决策。

## 何时使用

在以下任一情况触发：

- 用户要求新建、初始化、设计架构或开始实现一个项目、产品、CLI、Agent、服务、平台或 MVP。
- 用户给出 PRD、截图、Figma/Open Design handoff，要求做高保真页面。
- 功能同时涉及前端、后端、API、数据库、测试或视觉验收。
- 用户要求前后端并行、Mock、OpenAPI、垂直切片或持续截图对比。
- 当前任务需要判断应进入哪个子项目、使用哪条技能链或哪个验收门。

单纯的产品方向讨论、单一子项目的小范围代码修改或一次性 QA，应直接路由到更窄的技能，不要强行启动整条链路。

## 模式门

在读取完整规格、评审或交付流程前先判断模式：

| 模式 | 明确信号 | 默认行为 |
| --- | --- | --- |
| `quick-demo` | 快速 demo、prototype、spike、throwaway、先验证想法 | 最少文件、mock 或内存状态、一个可运行检查；不强制 PRD、OpenSpec 或完整评审，并明确不代表 production-ready |
| `full-project` | 新项目、正式 MVP、长期维护、production-ready、准备持续迭代 | 读取 [正式项目工作流](references/full-project-workflow.md)，按阶段门禁推进；门禁是按需选择，不是把所有技能全部运行 |
| `workflow-off` | 不用完整流程、跳过规划、正常做、直接实现、不要 grill | 停止本路由器，不加载重型项目流程，按最近的 `AGENTS.md` 和快速本地迭代规则继续 |

如果请求确实无法判断是可丢弃验证还是长期项目，只问一个短问题。用户说“项目”或“MVP”时默认 `full-project`；用户明确说“快速测试/demo”时直接进入 `quick-demo`。用户可以在任意阶段说“跳过完整流程”退出。

模式只约束当前任务。是否在其他项目自动识别这套流程，由该项目 profile 是否启用 `project-development-router` 决定，不创建额外的 workflow mode 配置文件。

## Ponytail 约束

进入设计或实现后，若 `ponytail` 已可用，默认使用 `full`：先理解 owner、现有代码和真实执行路径，再依次检查是否无需构建、能否复用、标准库、平台原生能力和已有依赖。用户说 `/ponytail off`、`stop ponytail` 或 `normal mode` 时立即关闭。

Ponytail 只减少不必要的方案和代码，不得删除信任边界校验、数据丢失保护、安全、无障碍、用户明确要求或与风险匹配的验证。`ponytail` 不可用时继续执行同样的最小完整实现原则，但不要声称已加载该 Skill。

## 快速本地分流

单一 owner 的本地非生产新增、修复或重构，若能沿用现有模式并以 mock、sandbox 或可丢弃测试数据完成验证，应直接进入
`yeisme-coding-execution-driver` 加一个本域 skill。新增模块、内部 API、迁移源文件、fixture 或 mock 本身不是规格审批门。

只有任务需要共享 UI/API/数据合同、前后端或多 writer 并行、稳定公开合同/持久化边界，或真实外部影响时，才先进入规格、合同或 OpenSpec 路径。完整判断见 `docs/workflows/rapid-local-iteration.md`；不要为了普通实现细节向用户重复索要确认。

## 路由步骤

1. 先选择 `quick-demo`、`full-project` 或 `workflow-off`；不要在模式未定时加载整套评审链。
2. 读取最近的 `AGENTS.md`、代码 owner、现有 PRD/设计/API/数据文档和项目测试入口。
3. 判断任务阶段：方向、规格、设计、契约、实现、集成、视觉质量或发布。
4. 只选择一个主工作流，最多附加一个领域约束；独立审查保持只读。
5. 判断是否需要冻结共享规格。仅当任务需要并行 lane、共享 UI/API/数据合同或稳定边界时，先使用 `$spec-driven-feature-workflow`；单 owner 的可逆本地切片可直接进入执行技能，并记录最小行为、owned paths 和 focused verification。
6. 有前后端并行需求时使用 `$api-contract-parallel-workflow`；契约冻结后才拆前后端工作。
7. 需要一个完整可验收功能时使用 `$vertical-slice-delivery`，把 UI、API、持久化、测试和证据放在同一切片。
8. 进入具体代码后切换到拥有代码的子项目，并叠加该项目的 runtime skill；根目录只负责路由和治理。
9. 在实现前确定 workspace mode：需要持续预览、浏览器渲染或截图迭代的客户端/Web lane 默认留在当前工作区；会运行热加载服务、worker、daemon、迁移或持久化依赖的后端 lane 默认使用独立分支/worktree。用户或子项目的明确要求可以覆盖该默认，但必须记录原因和隔离资源。

## 路由矩阵

| 用户意图 | 主技能 | 必要约束或后续门 |
| --- | --- | --- |
| 快速 demo、prototype、spike | 当前 owner 的最小实现流程 | `ponytail`；一个可运行检查；不加载完整 PRD/OpenSpec/评审链 |
| 新项目、正式 MVP、长期产品 | `project-development-router` 的 `full-project` 模式 | 按 [正式项目工作流](references/full-project-workflow.md) 逐门选择 |
| 用户明确跳过完整流程 | 最近 `AGENTS.md` 的普通执行规则 | 不加载 `grill-me`、完整 PRD 或自动评审链 |
| 价值、范围、场景、PRD | `agent-platform-prd` 或 `plan-ceo-review` | `plan-eng-review` |
| 高保真截图、Figma、Open Design 到 Web UI | `yeisme-frontend-design-router` → `ui-spec-frontend-workflow` | `yeisme-frontend-quality-workflow`、`design-review` |
| 单 owner、本地非生产的新增/修复/重构 | `yeisme-coding-execution-driver` | 本域 runtime skill；按快速迭代策略直接实现和聚焦验证 |
| 统一 PRD、UI、API、数据和验收规格 | `spec-driven-feature-workflow` | owner 的 OpenSpec 或设计评审 |
| OpenAPI、Mock、typed client、前后端并行 | `api-contract-parallel-workflow` | `backend-system-workflow`、`yeisme-evolutionary-change-policy` |
| 一个完整业务行为端到端交付 | `vertical-slice-delivery` | `project-integration-test-evidence` |
| 代码实现、修复、测试执行 | `yeisme-coding-execution-driver` | 具体领域 runtime skill |
| 集成、组件、系统或 E2E 验证 | `project-integration-test-evidence` | `qa`、owner 测试命令 |
| 发布前审查 | `review`、`health`、`qa` | `cso`、`document-release`、`ship` 按需触发 |

高保真设计的标准链路是：

```text
参考图 / Figma / PRD
        ↓
UI Spec + design tokens + states
        ↓
API / data contract
        ↓
Frontend mock lane + Backend real lane
        ↓
Vertical slice integration
        ↓
Playwright screenshots + visual review
```

默认的前后端并行形态是：

```text
contract ready
      ↓
current workspace: client preview/render lane
      +
isolated branch/worktree: backend hot-reload/debug lane
      ↓
small vertical-slice integration
      ↓
staged checkpoint commits → visual + functional acceptance
```

### Workspace 与提交路由

| 场景 | 默认位置 | 运行要求 | 阶段性产物 |
| --- | --- | --- | --- |
| 客户端/Web 需要实时预览 | 当前 checkout/current branch | 保留 dev server、浏览器端口和截图路径；单 writer | 可预览 UI、状态截图、focused tests |
| 后端服务/worker/daemon 需要热加载或自动调试 | `feature/<topic>` 独立 worktree | 独立端口、数据库/缓存、运行目录、日志和进程组 | 后端 focused tests、health/trace、调试摘要 |
| API/schema/typed client/mock | contract owner 的 workspace | 单一规范源，生成物不可手改 | contract checkpoint、生成命令、兼容检查 |
| 只读审查/验证 | 无 writer workspace | 不取得写租约 | diff、测试或截图证据 |

阶段性提交按“contract → 可预览客户端 → 后端切片 → 集成验收”推进；每次只提交所属路径和一个清晰意图。推送、PR、合并和 worktree 清理由显式授权的发布流程处理。

## 共享交付物

根据 owner 的文档归属，把交付物放在项目自己的 `docs/` 或 `openspec/changes/<change-id>/` 下；不要因为本技能而在根目录复制子项目文档。常见交付物包括：

- `PRD`：场景、用户目标、范围、非目标和验收结果。
- `DESIGN_SPEC` 或 UI Spec：布局、tokens、组件树、交互、响应式、loading/empty/error/permission 状态。
- `openapi.yaml` 或既有 API contract：请求、响应、错误、权限、分页、幂等和兼容策略。
- `DATABASE_SPEC`：实体、关系、状态转移、索引、迁移和数据保留边界。
- 验收矩阵：每个状态的可观察结果、测试入口、截图或运行证据路径。
- 垂直切片任务：owner、路径、依赖、并行 lane、验证命令、失败重检方式。

## 强制边界

- 不因用户说“做个应用”就静默运行全部产品、设计、工程、QA 和发布技能；先选模式，再渐进加载。
- `grill-me` 只在用户明确要求质询、挑战、压力测试或逐问时运行；需求清楚时跳过。
- 不从截图猜业务规则；不从代码猜未确认的产品范围。
- 不让前后端各自维护一份可漂移的字段定义；优先使用规范文件生成类型、client、mock 和文档。
- 不把页面数量、接口数量或技术栈当作完成标准；完成标准是一个用户行为的可运行证据。
- 不在根目录实现子项目代码；先进入拥有代码的子项目并读取其 `AGENTS.md`。
- 不为了“并行”把需要实时预览的客户端工作强行移出当前工作区；也不让后端热加载、数据库、端口或日志污染客户端预览环境。
- 不在 workspace 尚未决定、contract 尚未冻结或 owned paths 尚未声明时启动并行写入。
- 不在未获授权时创建子 agent、提交、推送、发布或执行生产写操作。

## 验证

路由完成时至少确认：

1. 已识别代码 owner 和文档 owner。
2. 已选定下一条最小技能链，并说明未加载的技能。
3. 共享规格、契约、验收和证据路径已命名。
4. 所有命令来自 owner 的真实项目脚本；若命令未知，先检查 `package.json`、`Taskfile.yml`、`Makefile`、README 或 CI 配置，不要臆造。
5. workspace mode、端口/数据/日志隔离和阶段性提交边界已记录。
6. 若修改的是本技能源，运行：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
```
