---
name: aigora-skill-router
description: Use when an Aigora task crosses domains or its skill and documentation entrypoint is unclear; select only relevant guidance.
---

# Aigora 任务导航

已经清楚要改哪些文件时，直接动手即可；需要了解某个模块的约束或接口约定时，再按任务加载对应技能和文档。普通文档修改、文字润色和小改动不需要先建 OpenSpec 提案，也不用加载全套编码流程。

先看 `docs/README.md` 选择领域；跨域或入口不清时再查下表。本技能同时同步到后端（`apigateway/aigora`）和控制台（`apigateway/aigora-web-console`）两个 target：标〔控制台〕的技能只在控制台 runtime 中生成，后端 runtime 没有 `aigora-opendesign-shell`；未标注的技能以后端 profile 为准，控制台需要时从 source 层按需读取或切回后端 target。下表文档路径默认相对于 Aigora 仓库根；在控制台会话中读取后端文档时，加 `../aigora/` 前缀。

## 按任务选技能与文档

| 任务类型 | 推荐加载的技能 | 对应文档入口 |
| --- | --- | --- |
| 新建或推进 OpenSpec 提案、校验、归档 | 对应的 `openspec-*` 技能 | `openspec/changes/` 下的对应目录 |
| 还在理思路、产品或架构探索，尚未决定实现 | `openspec-explore` | `docs/planning/README.md` |
| 后端服务、异步任务（Worker）、数据库读写 | `backend-system-workflow` | `docs/architecture/README.md` |
| PostgreSQL/GORM 架构优化：N+1、预算汇总/重放、CAS、SKIP LOCKED、有界回收、pool/在线索引 | `backend-system-workflow` 的 `references/database-interaction-performance.md`；稳定合同变更再加 `yeisme-evolutionary-change-policy` | `docs/architecture/database-interaction-architecture.md`、`docs/operations/database-performance-validation.md`、`openspec/changes/aigora-database-interaction-optimization-v1/`（设计，未实测） |
| 修改 CLI 命令与输出格式 | `ai-native-cli-output-contract` | `docs/protocols/README.md` |
| 修改对外 API、配置项或数据库表结构（兼容性评估） | `yeisme-evolutionary-change-policy` | 对应协议或迁移的 OpenSpec 目录 |
| 控制台页面与右侧 Inspector〔控制台〕：MCP/Agent、Connection/Channel、Route/Group/Profile/Binding、渠道/路由监控详情 | `aigora-opendesign-shell` + `aigora-operator-i18n` + `yeisme-frontend-quality-workflow`；一般页面框架可加 `yeisme-frontend-design-router` | `docs/operator/README.md`、`docs/operator/right-inspector-entity-matrix.md`、`../aigora-web-console/docs/README.md`、监控变更 `openspec/changes/archive/2026-10-19-aigora-channel-route-monitoring-v1/` |
| Seedance 视频模块架构 / 路由设计 | `aigora-seedance-core-architecture` / `aigora-seedance-next-router-design` | `docs/architecture/README.md` / `docs/routing/README.md` |
| 文本、Image、Video 统一分发控制面 | `backend-system-workflow`；视频生命周期或 Seedance 路由分别叠加 `aigora-seedance-core-architecture`、`aigora-seedance-next-router-design` | `docs/architecture/media-dispatch-convergence.md` |
| 本地密钥与凭据管理 | `credentialctl-usage` | `docs/upstreams/README.md` |
| 下游 Agent 发现能力、提交生成任务、生成变更预览 | `aigora-agent-core` / `aigora-generation-jobs` / `aigora-operator-guarded` | `docs/protocols/downstream-agent-interaction.md` |
| 整理或检查集成测试证据 | `project-integration-test-evidence` | `docs/operations/README.md` |
| 审查代码改动（diff review） | `review` | 当前改动的源码与测试 |
| 纯文档、Skill 或 OpenSpec 维护 | `aigora-skill-router` + 对应的 OpenSpec/profile 校验 | 不触发全仓实现流程，不自动运行 race |

按实际需要加载技能即可，不必把设计、开发、审查和全量测试强行串成固定流水线。跨多个模块时可以同时看对应的几篇文档。

## 注意事项

- 遵循项目 `AGENTS.md`：不主动运行 `-race`；密钥、权限、账本、生产变更和接口兼容性都按规范处理。
- 旧版内置 Web 已经退役；前端修改统一在独立客户端 `../aigora-web-console/` 下进行，不要从历史归档里恢复旧界面。
- 控制台专属技能只在控制台 profile 中启用；后端会话不要假设 `aigora-opendesign-shell` 可用，需要时先进入控制台 target。
- 根据改动范围选择验证命令：只改文档、文案或链接时，检查对应内容即可，不需要跑全套 Go 测试或真实厂商调用；改了代码逻辑再跑对应的单测或集成测试。

## 技能文件在哪维护

技能源在 Yeisme 工作区根目录（`apigateway/` 的上一级）的 `.skills/yeisme/`（自建）和 `.skills/imported/`（导入）。后端 profile 是 `.skills/profiles/targets/apigateway/aigora.txt`，控制台 profile 是 `.skills/profiles/targets/apigateway/aigora-web-console.txt`。可以用 `bash scripts/skills.sh resolve <name>` 查找某个技能的源码位置。

子项目里的 `.agents/skills/` 和 `.claude/skills/` 都是生成副本，不要直接手改。改完技能源码或 profile 后，在 Yeisme 工作区根目录运行：

```bash
# 在 Yeisme 工作区根目录运行
bash scripts/skills.sh profile validate apigateway/aigora
bash scripts/skills.sh sync-target apigateway/aigora
```

同步后确认 `.agents/skills/` 与 `.claude/skills/` 内容一致。全仓运行时校验用 `bash scripts/skills.sh validate-subprojects-runtime`；它还会检查其他 target，失败时先判断是否与本次改动有关。

同步控制台时，把 `profile validate` 和 `sync-target` 的目标换成 `apigateway/aigora-web-console`。运行时顶层的 `README.md` 是两端一致维护的元数据，不是技能包。


## 数据库设计的状态边界

Aigora 继续 PostgreSQL + GORM，先“少查、少搬、少锁、可重放”。预算汇总不是第二本账，需全部 writer 同事务与 DB fence，未结算 hold 不能只从 spend 重建。队列领取和过期回收都要有界，保留状态 CAS、每次独立 fence 和 Attempt/Job 锁总序。PG pool 当前仍驱动管理、DBStats 已有，候选 pool 配置与非事务在线索引是后续实现，不宣称当前支持。无实测不写提升倍数，SQLite/skip 不能证明 PG 锁与在线 DDL，默认不运行 race。

只改这两个已激活包时，在 workspace root 使用 `bash scripts/skills.sh sync-selected apigateway/aigora backend-system-workflow aigora-skill-router`；保留 runtime 独有改动备份，不全 target 覆盖。

## 资源命令与版本合同

先读取安装版的 help/结构化发现面，确认 canonical 路径存在。运行 `aigora models list --agent`，从 `fact.model.N.id` 取真实 ID，再调用 `aigora models describe <id> --agent`；`<id>` 是待替换的语法说明，不作为可直接执行的 Next。保持原项目、配置、过滤与权限范围。解析失败报告合同或版本问题，可查 `--json`，不要解析人读表或猜 ID。

详情类旧 show 只作隐藏兼容；正常操作使用 describe，独立 inspect/export/download 等动作保持原义。补全是同一目录的只读视图；需要安装时显式运行 completion install，并用 completion doctor 区分文件存在与 shell 可发现。源码候选通过不代表 PATH 安装版已更新。
