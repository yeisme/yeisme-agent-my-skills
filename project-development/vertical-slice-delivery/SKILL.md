---
name: vertical-slice-delivery
description: Use when delivering a user-visible feature end to end across UI, API, persistence, tests, integration, and visual acceptance, or when a task needs explicit dependencies, state transitions, parallel lanes, and evidence before it can be called done.
---

# 垂直切片交付工作流

把一条用户可观察的行为从规格推进到可运行、可测试、可截图和可复核的完成状态。不要按“先做所有页面、再做所有 API”的水平层切割任务。

## 切片定义

一个合格切片必须包含：

- 一个明确的用户或自动化入口；
- 该行为所需的 UI/CLI、API/event、领域规则和持久化；
- loading/empty/success/error/permission/conflict 等适用状态；
- unit、integration、component、system 或 e2e 中与风险匹配的验证；
- 对集成和视觉结果的可追踪证据。

“完成页面”或“完成接口”不等于完成切片。

## 状态机

默认使用以下交付状态；若 owner 已有状态机，以 owner 合同为准，并补齐同等门禁：

```text
requirement_ready
      ↓
design_ready
      ↓
contract_ready
      ↓
implementation_ready
   ↙           ↘
frontend_done  backend_done
   ↘           ↙
integration_passed
      ↓
visual_passed
      ↓
accepted
```

任一验证失败进入 `rework`，修复后回到对应门；`blocked` 必须记录阻塞证据和需要的外部决定。状态转移应说明 actor、幂等性、审计/事件、副作用、重试和失败处理。

### 本地快速路径

对单 owner、可逆、非生产的本地切片，只要写明最小用户行为、owned paths 和 focused verification，就可以从 `requirement_ready` 直接进入实现与验证；不必因为新增模块、内部 API、迁移源代码或 mock 先补一套完整规格。该路径不得用于并行 writer、共享或稳定合同、非可丢弃数据迁移、生产启用或真实外部写入；这些情况仍回到完整的 contract/design 门。

## 交付步骤

### 1. 选择最小行为

用一句话定义：

```text
<角色> 在 <前置条件> 下执行 <动作>，看到 <结果>，并能在 <失败分支> 中恢复。
```

拆掉不能影响首条可交付路径的页面、字段、动画和附加场景。把探索性场景标注为 exploratory，不要伪装成成熟能力。

### 2. 按需冻结共享合同与门禁

需要共享 UI/API/数据合同、稳定公开表面或前后端并行时，先确认 `$spec-driven-feature-workflow` 的产品、UI、API、数据和验收规格为 ready；有前后端并行时再使用 `$api-contract-parallel-workflow`。单 owner 的本地快速路径不把完整规格当作前置门，但必须使用现有合同或写下最小行为和验证信号。contract 未冻结前，不启动依赖它的并行实现 lane。

### 3. 创建有 lease 的 lane

每条任务记录：

| 字段 | 要求 |
| --- | --- |
| owner | 具体 agent 或当前 root |
| owned paths | 可写路径的明确清单 |
| shared read paths | 只读输入 |
| forbidden paths | 不能改的共享或生成文件 |
| dependencies | 需要完成的前置状态 |
| verification | 真实可运行命令和预期结果 |
| evidence | 测试、截图、diff 或运行证据位置 |
| failure recheck | 失败后回到哪个门、先检查什么 |

前端和后端只有在 contract_ready 后才能并行。若用户没有明确授权使用 subagent，不创建子 agent；单 owner 的本地快速路径可以按 lane 顺序直接执行。

默认 workspace mode 也属于 lane contract：

- 需要浏览器预览、渲染、截图或交互调试的 frontend/client lane 留在当前 checkout/current branch，保持一个可观察的 preview runtime。
- 需要 hot reload、worker/daemon、数据库迁移、独立端口或长期日志的 backend lane 使用独立 `feature/<topic>` branch/worktree，并隔离端口、数据目录、缓存、临时文件和进程组。
- contract、typed client、mock、fixture 和生成文档指定一个 owner；不要让两个 worktree 同时生成或修改同一文件。
- 每条 lane 必须记录 `workspace_mode`、owned/forbidden paths、真实启动命令、端口/数据目录、focused verification 和集成依赖。

### 4. 完成最窄的实现闭环

优先顺序：

1. contract 生成材料和 fixture；
2. 后端最小真实行为与持久化；
3. 前端 service/mock 与核心状态；
4. focused unit/contract tests；
5. 真实集成路径；
6. fixed viewport screenshot、交互和可访问性检查；
7. 只修复本切片产生的差异，再推进到下一切片。

阶段性 checkpoint 按 `contract_ready`、`frontend_preview_ready`、`backend_slice_ready`、`integration_passed` 推进。每个 checkpoint 只包含可独立审查的一组 owned paths；子 agent 不提交，root 在获得仓库授权后创建窄提交。预览、集成或自动调试产生的临时产物必须留在项目规定的 `temp/` 或忽略目录中。

使用 owner 的现有测试 runner 和脚本。集成、组件、系统和 E2E 运行必须按 `project-integration-test-evidence` 保存 `summary.json`、`command.txt`、`stdout.log`、`stderr.log`、`env.json` 和 `artifacts/`，并脱敏秘密与内部提示词。

### 5. 关闭门禁

只有在以下证据齐全时把状态标记为 `accepted`：

- contract lint/generate 或等价兼容检查通过；
- 前后端 focused tests 通过；
- 真实集成路径覆盖成功、空态、错误、权限或冲突中适用的分支；
- 视觉截图与 UI Spec/批准基线一致，差异已修复或明确记录；
- `git diff --check` 通过，且没有把无关脏工作树误判为本切片失败。

## 失败重检

先把失败归类为 `introduced`、`pre_existing`、`concurrent`、`environment` 或 `ambiguous`。只修复 owned paths 中确认由本切片引入的问题；不要为了清理全仓旧告警修改无关业务逻辑。重复失败时回到最近一个成功状态，重新检查 contract、fixture、启动参数和证据目录。

## 边界

本技能不替代产品决策、领域 runtime、发布、部署、生产写入或外部消息发送。它只管理一个功能切片的依赖、状态和证据；代码实现切换到 `yeisme-coding-execution-driver`，UI 视觉门切换到 `ui-spec-frontend-workflow` 与 `yeisme-frontend-quality-workflow`，发布前再使用 `review`/`qa`/`ship`。快速路径的审批边界遵循 `docs/workflows/rapid-local-iteration.md`。
