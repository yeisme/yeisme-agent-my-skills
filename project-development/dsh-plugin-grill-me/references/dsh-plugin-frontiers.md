# DSH 插件 Grill Frontiers

按阶段组织的决策 frontier 地图。每个阶段给出进入条件、核心问题与绊线；上游阶段未敲定时不进入下游阶段。“事实来源”列的是 Agent 应先查的仓内真源，不是问用户的问题。问题按 `grill-me` 的轮次与提问格式使用，每题附可反驳的推荐答案。

## 阶段总览（依赖顺序）

```
S0 场景与表面 → S1 owner 与边界 → S2 数据与投影 → S3 seam 与宿主
      → S4 形态与组合 → S5 界面契约 → S6 生命周期与降级 → S7 交付与验证
```

S5 只在 shape B（React Web 面）时进入；纯 preset/数据 bundle 从 S4 直接到 S6。

## S0 场景与表面

进入条件：用户给出想做的能力或问题，尚无确定表面。

核心问题：

- 目标用户与 job-to-be-done 是什么？没有这个面板时，用户现在的替代路径是什么？
- 领域数据按会话作用域还是 process/project 作用域？（决定表面的第一事实：换会话就该换视图 → tab；跨会话 → pane；只是动作入口 → header action + overlay。）
- 为什么不是更窄的一个表面？MVP 的最小可见闭环是什么？
- 这是产品面（用户可见价值）还是基础设施（服务其它插件）？

绊线：为了“看起来完整”同时铺 tab+pane+overlay 三个面；没有目标场景的面板。

事实来源：`docs/plugin-tab-development.md` §1、既有 `packages/` 的 surface 先例。

## S1 owner 与边界

进入条件：表面方向已定。

核心问题：

- 领域真相归谁？Ordo（run/task/session/lease/approval/verification/evidence/closeout）、DSH core、本仓插件，还是外部系统？
- 本插件对真相的角色：只读投影、命令入口，还是需要自有状态？若需要自有状态，为什么既有 owner 不够？
- 是否触碰第二 scheduler、task ledger、writer lease、approval ledger、capacity reservation 或 terminal result？（触碰即回到 S0 重新设计。）

绊线：本仓造第二账本；浏览器侧 domain store；任意 iframe bridge；复活独立 Workbench/BFF/TaskService/第二主壳。

事实来源：`AGENTS.md` Architecture Boundaries 与 Prohibited Actions、`openspec/changes/ordo-dsh-plugin-visualization-v1/`。

## S2 数据与投影

进入条件：owner 边界与本插件角色已确认。

核心问题：

- host→浏览器过界字段面：opaque ref、有界摘要、版本、freshness、evidence ref、server-authored action 是否够用？哪些字段是真正必要的？
- 投影是 logged tool calls 的纯 fold（确定性 id、可重放）还是需要存储域？有界窗口（如最近 200 条）是否诚实标注边界并指向权威读路径（`*_state`/`*_report`）？
- 若需存储域：per-session 记录、`$DSH_HOME/storages/`、sqlite 需 Node ≥ 22.5、schema 版本与迁移策略。
- 明确列出绝不过界的内容：cookie/token/raw URL/文件路径/任意 fetch/raw prompt/provider payload/private tool arguments/绝对路径。

绊线：“临时”放宽过界字段；浏览器侧缓存再计算形成第二份权威状态。

事实来源：`docs/plugin-tab-development.md` §3、`docs/plugin-host-protocol.md`。

## S3 seam 与宿主

进入条件：数据面已定。

核心问题：

- 全部能力是否落在已发布 surface（`@deepseek-ai/dsh-*`、`@deepseek-ai/cordis`）？列出具体依赖的 API 与版本。
- 若需要 DSH core 改动：走 `upstream-prs/<slug>/` 通道（changes.patch + new-files/ + apply.sh + README），还是插件侧先 capability probe 等官方？止损条件是什么？
- probe 策略：Remote/capability 缺失时入口 visible-but-disabled 加 `disabledReason()`，绝不静默隐藏、绝不假回退。
- unknown/partial/cancel_unknown/stale cursor 出现时：只禁用 mutation 并要求 owner reconcile，绝不自动 retry 或替换 writer。

绊线：fork core；把官方 seam 合入、官方 `dsh web` 或 host 几何实现当作完成条件；死按钮。

事实来源：`AGENTS.md` Upstream Seam Channel、`docs/plugin-host-protocol.md`。

## S4 形态与组合

进入条件：seam 路线已定。

核心问题：

- shape A（自包含 bundle，`lib/` 预构建）还是 shape B（host/client/bundle 三包 + React）？上游 pin/预设数据 → A；新交互 UI → B。
- `cordis.patch.yml` 是否只用仓内收敛的 `- insert: [id, name]` 语法？完整语法（id 覆盖行、多条 insert）仅限带 `YEISME-VENDORED.md` 的 vendored bundle。
- preset-root 注册：领域 host 行放领域 agent preset，不进全局 patch；web 行 host half 是否保持空 `apply`（防 scoped tool catalog 重复注册与 client 命令失效环）？
- vendoring：排除 `.git`/lockfile/上游构建产物/过程文档；commit 预构建 `lib/`；pin commit + license + 升级流程进 `YEISME-VENDORED.md`；升级 = fresh-clone 字节 diff + 人工复核 + 全门禁重跑。

绊线：全局 patch 塞领域行；手写带 schema/state/audit 语义的 JSON/YAML/JSONL/Markdown metadata（用 openspec CLI 或应用服务生成）。

事实来源：`docs/plugin-tab-development.md` §2/§9、`AGENTS.md`。

## S5 界面契约（仅 shape B）

进入条件：已选 shape B。

核心问题：

- `ui-surface` 与 `ui-visual-kit` token 的使用面怎么分？design.md 是否填了 visual-system §12 的 UI Contract？
- 容器密度、状态矩阵、插件 archetype 与既有面板是否一致？zh/en 双语词典、焦点返回、可读禁用原因是否齐？
- 响应式与可访问性的验收怎么定义？`check:surfaces`、`test:visual`、`check:plugins` 的通过标准？

绊线：跳过 visual-system 文档直接写 UI；自造另一套视觉 token。

事实来源：`docs/design/dsh-unified-panel-visual-system.md`（Agent 必须先读再问）。

## S6 生命周期与降级

进入条件：形态已定（shape A 从 S4 直达本阶段）。

核心问题：

- 会话生命周期：per-session tab 是否沿 `parentId` 祖先（带环防护）按 preset 成员判定注册/注销？pane 是否 keep-alive singleton？
- 每个 registration（pane、slot、locale、subscription）是否都流入 `apply` 返回的 disposer？HMR、profile 切换、插件禁用、会话切换四条路径是否对称拆除？
- 会话失去领域 preset 时绝不留死 tab；降级链：pane 不可用 → overlay 兜底；overlay 也不可用时给可读原因。

事实来源：`docs/plugin-tab-development.md` §3/§4。

## S7 交付与验证

进入条件：设计主干已收敛。

核心问题：

- 需要 OpenSpec change 吗？判据：改稳定合同/persistence schema/submodule 边界/生产行为/凭据/外部副作用 → 必须；可逆窄探针、本地 spike、UI/UX 小扩展 → 可先做后补。新 capability 只写 `ADDED`。
- 任务拆分是否原子、可并行、有 owner、验证命令、预期结果与失败复查步骤？design.md 有 Mermaid？
- 验证门清单：`pnpm run typecheck`、`test`、`build`、`check:bundles`、`check:plugins`，shape B 加 `check:surfaces`，加 `openspec validate <change-id> --strict --no-interactive` 与 `git diff --cached --check`。完成定义 = 仓内协议对接，不依赖官方 seam。
- 集成证据：`temp/integration-test-runs/<run-id>/`，脱敏 secret、raw prompt、provider payload、private tool arguments、绝对路径与完整思维链。

绊线：把官方 `dsh plugin add`/Web boot 写成插件完成条件的阻塞项（它们只是可选 host 集成证据）。

事实来源：`AGENTS.md` Validation、根仓 AGENTS.md 的 OpenSpec 分层规则。

## “不知道”的处理

需要真实使用、视觉感受或运行证据才能判断的问题（视觉密度、交互手感、上游运行时行为），停止纯讨论，建议按 `docs/cookbook/dsh-plugin-hot-development.md` 的热开发工作流做可丢弃 prototype；拿到证据后回来重算 frontier。
