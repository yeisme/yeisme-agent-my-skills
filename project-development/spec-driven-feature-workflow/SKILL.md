---
name: spec-driven-feature-workflow
description: Use when turning a product idea, PRD, screenshot, Figma/Open Design handoff, or cross-stack feature request into a shared specification covering product behavior, UI states, API/data contracts, acceptance criteria, and executable delivery tasks.
---

# 规格驱动功能工作流

先把需求变成前端、后端、测试和评审都能引用的共同合同，再开始实现。输出默认使用中文项目文档；命令名、路径、字段名和协议名保持现有英文形式。

## 输入与输出

接受以下任意输入：产品意图、PRD、用户流程、参考截图、Figma/Open Design handoff、已有页面、API 草案、数据库模型或一个跨栈功能请求。

为一个功能切片生成或更新：

1. 产品规格：目标用户、Job-to-be-done、场景、范围、非目标、成功信号和权限边界。
2. UI Spec：页面结构、设计 tokens、组件树、交互控件、响应式规则以及 loading、empty、success、error、permission denied 状态。
3. API contract：endpoint、request、response、错误、认证、权限、分页、幂等、并发和兼容策略。已有 OpenAPI 时，以它为规范源。
4. 数据规格：实体、关系、状态转移、约束、索引、迁移和数据保留边界。
5. 验收矩阵：每个状态的可观察结果、验证入口、测试层级、截图或运行证据。
6. 垂直切片任务：owner、owned paths、依赖、并行 lane、验证命令和失败重检方式。

## 工作流

### 1. 定位 owner 与边界

读取最近的 `AGENTS.md`、项目 README、现有文档、package manifest、Taskfile/Makefile、CI 和测试目录。确认代码、文档、API contract、数据库和客户端分别由谁拥有。子项目文档放在该子项目的 `docs/` 或 `openspec/changes/<change-id>/`，不要复制到根目录。

### 2. 锁定产品行为

把模糊描述改写成一条可观察的用户行为：

```text
角色 → 前置条件 → 操作 → 可观察结果 → 失败/权限分支 → 证据
```

列出探索性、首批支持和成熟场景；不要把尚未验证的场景写成生产承诺。明确非目标，防止实现 agent 通过“顺手补充”扩大范围。

### 3. 先写状态，再写组件

为每个页面、命令或 API 行为列出：

| 状态 | 必须表达的内容 | 验收信号 |
| --- | --- | --- |
| loading | 用户知道系统正在做什么 | skeleton、spinner 或进度信息稳定可见 |
| empty | 用户知道为什么为空以及下一步 | 空态说明和唯一主要 CTA |
| success | 核心数据和主操作 | 真实字段、排序/分页/筛选规则明确 |
| error | 错误原因和恢复动作 | retry、修复指引或人工介入路径 |
| permission denied | 不泄漏敏感数据 | 明确权限状态和安全的下一步 |

有高保真视觉输入时，先使用 `ui-spec-frontend-workflow` 提取布局、tokens、组件树和响应式规则；不要从截图臆测业务规则，也不要在 UI Spec 之前写 JSX/CSS。

### 4. 冻结 API 与数据合同

优先确定规范源：已有 `openapi.yaml`、schema、IDL 或项目合同。只有在规范源不存在时才创建草案，并标出未决项。API 至少覆盖 UI 的所有状态、错误和权限分支。数据设计必须遵守项目 ORM、迁移、并发和状态机规则；不要把硬编码 SQL 或字段拼接放入普通业务代码。

### 5. 编写验收矩阵

每条验收标准都要能被人或自动化观察：

```text
Given <前置条件>
When <用户或系统动作>
Then <结果>
And <错误、权限、边界或证据要求>
Verify: <真实项目命令、截图路径或检查入口>
```

将“像设计稿”“接口正确”“联调完成”改写成尺寸/状态/字段/状态码/截图/测试证据等可检查结果。

### 6. 输出可执行任务

任务必须先完成共享合同，再拆出前端 lane、后端 lane、集成 lane 和视觉 lane。标明哪些任务可并行、哪些任务等待 contract、哪些路径禁止修改。跨模块功能使用 `$vertical-slice-delivery` 继续推进。

## Ready 检查

只有满足以下条件才把规格标记为 ready：

- 用户行为、范围、非目标和权限边界明确。
- 设计、交互、响应式和所有关键状态有书面表达。
- API request/response/error/auth/pagination/idempotency 已冻结，未决项已列出。
- 数据模型和状态转移能承载验收场景。
- 每条验收标准都有真实验证入口或明确的阻塞原因。
- 变更未违反 `yeisme-evolutionary-change-policy`；若会改变稳定合同，已有 OpenSpec 迁移、弃用和回滚方案。

## 边界与验证

本技能负责规格编排，不负责代替 owner 实现代码、生成生产数据库、修改外部服务或凭空决定产品方向。实现阶段切换到 `yeisme-coding-execution-driver` 与具体领域 skill；前后端并行使用 `api-contract-parallel-workflow`；集成测试使用 `project-integration-test-evidence`。

规格完成后至少运行：

```bash
git diff --check
```

再按 owner 的真实命令运行 OpenSpec、API contract lint、类型生成或测试。找不到命令时先检查 `package.json`、`Taskfile.yml`、`Makefile`、README 和 CI，不要臆造验证结果。
