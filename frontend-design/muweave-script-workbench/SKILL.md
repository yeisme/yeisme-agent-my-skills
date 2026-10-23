---
name: muweave-script-workbench
description: Use when designing or implementing MuWeave's five-view screenplay workbench and its management-level novel bible with project-local mock data, structured blocks, local ScriptDraftV1 recovery, revision conflicts, App Shell Inspector, and truthful Auctra boundaries.
---

# 幕织剧本工作台

## 目标

把 OpenDesign 的剧本管理、正文、集纲、故事图谱和风格设定转成 MuWeave 的 L3 feature package。页面消费结构化 screenplay projection，五个视图共享一个本地 `ScriptDraftV1`，不拥有 Auctra canonical screenplay。实时模式通过 Scaena production-center facade 读取和提交，浏览器不直连 Auctra 或 Anatomia。剧本管理内的工具书二级工作区维护角色、地点、道具、时间线和主题；开发 mock 只来自客户端 `src/mocks/script/`，不依赖根仓 `data/`。

## 先读的来源

- `client/muweave-frame-studio/docs/design/script-workbench-ui-spec.md`
- `client/muweave-frame-studio/docs/architecture/script-workbench-contract-boundary.md`
- `client/muweave-frame-studio/src/features/script/contract.ts`
- `temp/open-design/pane-track-polish-v11-20261007/drama-development-center-unified/docs/script-workbench/design.md`
- `temp/open-design/pane-track-polish-v11-20261007/drama-development-center-unified/docs/script-workbench/prd.md`

## 不变量

- 五视图只能修改 `src/features/script/`、页面测试和剧本页面文档；共享合同、Shell、路由 registry 交给 L0。
- block 类型必须区分场景标题、动作、人物、对白、括注和转场。
- 管理、正文、集纲、图谱和风格修改都进入同一 `ScriptDraftV1` patch 集合。
- 工具书资料卡修改也必须进入同一 `ScriptDraftV1`，不得创建第二份小说真源。
- localStorage key 为 `muweave.frame-studio.script-draft.v1:<projectId>`；只保存本地未提交 draft，不保存凭据、Prompt、provider payload 或私有路径。
- base revision 变化时保留草稿并进入 stale/conflict，阻断 owner 采用；不自动合并、不自动丢弃。
- App Shell Inspector 承载属性、集纲、图谱、风格和 AI；页面不得渲染第二个右侧 Shell。
- AI、canonical save、版本采用和 owner mutation 在 Auctra 未接入时必须显示 unavailable 或 disabled reason。
- 真实本地预览使用 `bun run dev:script-preview`；它通过同源 `/__dev/scaena` 代理进入 Scaena，默认 project/episode 为 `project-local`/`episode-01`。显式 `?mode=live` 仍可覆盖 facade、project 和 episode；缺少配置时保持 empty/unavailable。
- 开发代理只在服务端读取用户级 owner key，并将 loopback 请求映射到开发 service principal；浏览器、production build 和 OpenDesign prototype 不得持有凭据。
- 每个 mutation 使用稳定 `idempotencyKey` 与 `expectedRevision`；unknown 结果只 reconcile 原 operation。
- `writing.from_evidence` 固定 Anatomia snapshot，`writing.fork` 固定父 track/revision，`submit` 和 `accept` 保持分离。

## 交互

- 默认中央视图为正文，默认 Inspector 页签为集纲。
- 正文支持 block 文本、类型、增删和顺序调整。
- 集纲支持全剧、分集、场纲；图谱关系保留来源 scene/block/evidence；风格支持继承、覆盖和恢复继承。
- 支持 Escape、Tab、方向键、焦点恢复和 `prefers-reduced-motion`。
- 820px 以下优先浏览、审批和低风险输入，不提供完整桌面编辑密度。

## 必须验证

- projection、draft migration、reducer、local save/recovery、backup、save failure、stale/conflict。
- 五视图切换和 Inspector 五页签。
- mock route `?mode=mock` 与默认 empty/unavailable route 的差异。
- 工具书二级工作区、Bible projection 和项目内《雨夜重逢》mock 完整性。
- 1440×900、1280×800、1024×768、820px、390px。
- 证据写入 `temp/integration-test-runs/<run-id>/` 并脱敏。

## 工作区 v2（剧本 / 小说，仅 `?mode=mock`）

- 先读：`client/muweave-frame-studio/docs/design/script-workspace-v2-ui-spec.md`、`docs/architecture/script-workspace-v2-contract-boundary.md`、OpenSpec `script-workspace-v2`。
- 八视图（管理 / 正文 / 集纲 / 图谱 / 风格 / 资料 / 审阅 / 版本）在工作区 Pane 内；**侧栏的每个 Tab 都是独立 shell Pane**（左：目录 · 工作集 · 速查；右：卡片 · 属性 · 问题 · 关联 · 风格 · AI），Pane 内不再放第二条标签条。
- Pane 无本地状态（shell 会卸载被切走的 Tab）：筛选、搜索、草稿、滚动放 `store.slot`；跨 Pane 动作只用 `store.reveal(pane)`，不假设 Pane 在哪个容器；页面不 import `useShell` / dock，只用标签上的 `data-pane-tab` 钩子，找不到就退回专注浮窗。
- 真源是内存工作稿 `ScriptWorkspaceStore`（不使用浏览器存储）；AI 与 owner 动作只有 `fixture` 能力才执行并标“原型模拟”，否则 disabled + 原因。没有综合分数。
- 色彩与图标：沿用全局暮紫色系（不要橙色 / 珊瑚）；单元状态用 `StatusGlyph` 形状图标，开关“开”态用 `weight="fill"`，选中的视图 Tab 用 duotone，`Ic` 与外壳图标同一线宽；新增图标先查有没有别的概念已经在用同一个 Phosphor 图形。
- 设计原型同步：OpenDesign 原型 `script-workspace-v2`（统一项目 `script-workspace-v2/`，镜像 `manju-script-workspace`）已用同一套 Pane 模型（9 个 Pane、三种移动方式、`reveal`、状态栏、`Ctrl+Shift+F`）；改客户端交互时先改原型并跑它的 `flows-panes.mjs`，规则写在原型 `docs/ui-spec.md` 的“Pane 模型”。
- 验证：`bunx vitest run src/features/script`、`MUWEAVE_E2E_PORT=4198 bunx playwright test tests/script-workbench.spec.ts --project=desktop-1440`（不要对 4196 预览服务跑 e2e）。

真实命令：

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run test:e2e
bun run build
```

本地 live facade 预览：

```bash
bun run dev:script-preview
```

浏览器地址使用 `http://10.10.1.101:4196/#/script`。需要演示数据时显式使用 `?mode=mock`；不能把 mock 或 OpenDesign readback 当作 owner 完成证据。

OpenDesign 同步先用 MCP 读取；若文件工具返回空结果，使用：

```bash
curl -fsS http://127.0.0.1:7456/api/projects/drama-development-center-unified/files
curl -fsS http://127.0.0.1:7456/api/projects/drama-development-center-unified/raw/index.html
```

禁止 race 检测、真实 Auctra/Provider/AI 调用、提交、推送和部署。
