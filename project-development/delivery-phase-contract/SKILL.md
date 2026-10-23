---
name: delivery-phase-contract
description: Use when a delivery request spans more than one surface (UI, API, persistence, or a real cross-side link), when a frontend or backend task must be accepted independently, or when an agent is about to start the other side, the database, or a full-site sweep inside one task; enforce exactly one PHASE (CONTRACT, FRONTEND, BACKEND, INTEGRATION), phase-local write scope, contract-derived mocks, phase-local acceptance, and explicit-only integration entry.
---

# 阶段隔离交付合同

跨端请求先拆成单一阶段任务，再开工。目标不是少做事，而是让每一端都能独立开发、独立验收，并且不把“另一端还没好”当成失败，也不把“本端通过”说成功能可发布。

规则真源是 `docs/workflows/phase-scoped-delivery.md`（阶段隔离交付规则）。本技能负责在具体任务里执行它。

## 使用场景

- 请求同时涉及页面/交互、API/业务规则、持久化或真实跨端链路。
- 用户要求“前端先做完”“后端独立验收”“先做 Mock，不启动后端”。
- 任务开始漂移：要顺手启动另一端、检查数据库、截图全站，或为通过测试而在组件里编造响应。
- 需要明确“什么时候算结束、什么时候必须停下来记录阻塞”。

以下情况不要使用本技能：单 owner、本地非生产、可逆、只有一个写入者的普通改动（按 `docs/workflows/rapid-local-iteration.md` 的本地快速迭代默认策略直接实现并聚焦验证）；只读审查、只采集证据、只回答问题的任务。

## 输入

- 用户请求与期望的可观察结果。
- 最近的 `AGENTS.md`、相关合同文件（OpenAPI/schema/IDL）、现有 mock、fixture、typed client。
- 本端真实的启动与检查命令：类型检查、聚焦测试、mock 运行方式、浏览器或运行时入口。
- 另一端的交付状态（可能尚未开始）。

## 输出

每个阶段任务结束时给出固定四项，不粘贴完整代码或成功日志：

1. 修改范围（实际写入的路径）。
2. 实际执行的检查与结果。
3. 未验证事项或阻塞（含缺失合同项、最小变更提案）。
4. 阶段状态与下一阶段所需信息。

阶段状态只能是 `PHASE_PASS`、`PHASE_FAIL`、`BLOCKED` 或 `INTEGRATION_PENDING`。

## 工作流

1. **选阶段。** 为当前任务选定唯一 PHASE：`CONTRACT`、`FRONTEND`、`BACKEND` 或 `INTEGRATION`。跨端需求拆成独立任务，而不是在一个任务里做完两端。缺少明确 `INTEGRATION` 指令时不进入联调。
2. **写任务卡。** 记录 PHASE、owned paths、shared read paths、forbidden paths、依赖、运行模式、验收命令、本次不做的事、结束条件。合同路径在 `FRONTEND`/`BACKEND` 阶段是只读的。
3. **确认依赖。** `FRONTEND` 依赖冻结的合同和派生 mock；`BACKEND` 依赖合同与数据/权限规则；`INTEGRATION` 依赖两端交付摘要与契约版本。依赖缺失就写清缺失项。
4. **本端实现。** 只写 owned paths，保持真实请求调用层，在网络层 mock；mock 响应由合同派生，不新增合同未定义的字段、状态码或错误结构。
5. **本端验收。** 只跑影响本阶段的检查。前端覆盖适用的 loading、empty、success、error、permission 状态；后端覆盖 API、业务、权限与契约一致性。另一端未启动不属于本阶段失败。
6. **判定状态。** 验收全过记 `PHASE_PASS`；证据指向本阶段路径的失败记 `PHASE_FAIL`；缺合同/凭据/依赖/外部决定记 `BLOCKED`；本阶段通过而真实跨端链路未验证时同时标记 `INTEGRATION_PENDING`。
7. **停止。** 达到本阶段验收即结束，不自动追加另一端验收、全站巡检或发布前检查。需要真实跨端验证时单独开 `INTEGRATION` 任务，只验证任务列出的链路。

## 边界

- 不因为“顺手”启动另一端的服务、数据库、迁移或浏览器验收。
- 不私自修改共享合同后再同步另一端实现；只记录问题与最小变更提案，并把受阻部分标记 `BLOCKED`。
- 不在组件或业务代码里硬塞假业务逻辑来绕过后端缺失。
- 不把 mock 的宽松行为当作真实 API 契约；不用自造的身份、角色或权限字段替代服务端判断。
- 不把未执行的检查写成通过，不把 `PHASE_PASS` 表述成“可以发布”。
- 需要真实外部写入、凭据、部署、发布或不可逆数据操作时，回到 owner 的审批门，而不是在本技能里自行决定。
- 稳定合同发生生成性变更时遵守 `yeisme-evolutionary-change-policy`。
- 阶段隔离不降低验证强度：本端聚焦验证、集成证据仍按 `project-integration-test-evidence` 落盘。

## 验证

- 本端命令来自项目真实脚本（`package.json`、`Taskfile.yml`、`Makefile`、README、CI），找不到就说明，不臆造。
- 通用最小检查：`git diff --check`。
- 前端阶段：类型检查、受影响交互的聚焦测试、目标页面在 mock 模式下的状态检查。
- 后端阶段：API/业务/权限测试、契约一致性检查、隔离测试数据库。
- 集成阶段：任务列出的真实链路端到端验证，证据写入 owning subproject 的 `temp/integration-test-runs/<run-id>/` 并脱敏。
- 修改本技能源后运行：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
```

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| 任务同时要求做两端 | 拆成两个阶段任务，先冻结合同 | 不合并成一个“全栈一次做完”的任务 |
| 合同缺字段或冲突 | 记录最小变更提案，标记 `BLOCKED` | 不猜接口、不顺手改合同 |
| 前端因后端未启动失败 | 改为 mock 运行模式，重新执行本端检查 | 不把环境缺失记为本端 `PHASE_FAIL` |
| 想顺手修全仓告警 | 归类 `introduced` / `pre_existing` | 只修 `introduced` 的 owned paths |
| 想直接进入联调 | 确认存在明确的 `INTEGRATION` 任务与两端交付摘要 | 不自动联调 |
