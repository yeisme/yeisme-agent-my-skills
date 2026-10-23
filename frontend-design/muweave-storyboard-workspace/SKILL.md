---
name: muweave-storyboard-workspace
description: Use when designing or implementing MuWeave's contract-first storyboard workspace with OpenDesign visual handoff, Scaena safe projections, explicit media preview, candidate comparison, revision checks, and responsive review states.
---

# 幕织专业分镜

## 目标

把 OpenDesign 的镜头目录、中央舞台、候选托盘和右检查器转译为 MuWeave 的 Storyboard feature package。Scaena 拥有 ProductionGraph、分镜、候选、revision、审阅和回执；MuWeave 只消费宿主注入的 safe projection，并提供本地选择、比较、镜头表、动画预览和显式预览。分镜是收敛工作台，无限画布是发散工作台，两者通过 hash 意图双向交接。

## 先读的来源

- `client/muweave-frame-studio/docs/design/storyboard-workspace-ui-spec.md`
- `client/muweave-frame-studio/docs/architecture/storyboard-workspace-host-contract.md`
- `client/muweave-frame-studio/src/contracts/workspaces.ts`
- `client/muweave-frame-studio/src/features/storyboard/`
- `client/muweave-frame-studio/openspec/changes/storyboard-workbench-v2/`
- `client/muweave-frame-studio/src/shared/generation/machine.ts`（批量生成复用画布生成流程）
- OpenDesign project `drama-development-center-unified`
- `agent/scaena/openapi/openapi-v1.json`
- `agent/scaena/docs/protocols/storyboard-review-package.md`

## 不变量

- Storyboard 页面只修改 `src/features/storyboard/`、页面测试和页面文档；共享 contracts 与 adapter 由 L0 维护。
- 不能把剧本正文、Prompt、凭据、Provider payload、媒体 bytes 或 owner 私有路径写入浏览器持久化。
- 页面只渲染中央舞台/镜头表；镜头序列（`shots`）、镜头属性（`shot-props`）、任务（`tasks`）放在 Shell 的 page-scoped panes，Tab id 与标签保持稳定，页面与 Tab 通过 feature 内 store 共享状态；Tab 被拖到任意容器或分屏都要可用。
- 镜头选择和候选选择不得自动打开或播放媒体；只有显式“预览候选”、对比或“预览全片”可以读取 resolver，并遵守 `previewCapability`。
- patch、accept、reject、request_review 必须携带 expected revision/digest 和 idempotency key；409 保留本地 draft 并给出对比。
- 每个动作只在 `allowedActions` 有对应描述时可用；“送审”只走 owner 发布的 `request_review` 描述，不能映射到 `range-reviews`（那是审阅人裁决）。
- live patch 的 `set` 只用 Scaena snake_case 字段：`dramatic_purpose`、`action_summary`、`shot_size`、`camera_angle`、`camera_movement`、`duration_ms`、`voice_over`、`sfx`、`continuity_notes`；枚举外的值保留为“自定义”。
- unknown action 只允许回查原 operation，不生成替代 key 或重复提交。
- stale、offline、permission、contract mismatch 和 unavailable 必须有可读原因和 disabled reason。
- fixture 只能通过显式开发入口使用，不能被描述为 live Scaena 或生产完成。

## 正式 Scaena 与 PostgreSQL

- Scaena 是 storyboard canonical owner；MuWeave 只消费 `scaena.storyboard_workspace_projection.v1` safe projection，不创建 storyboard 数据库。
- 正式 Scaena service mode 使用现有 GORM + PostgreSQL；`storyboard_workspace_projection_records` 是可重建派生读模型，canonical breakdown/candidate/review rows 仍是唯一事实来源。
- workspace 读取使用 episode/breakdown/candidate refs、revision、digest 和 keyset cursor；不保存 prompt、源文本、provider payload、凭据或媒体 bytes。
- `ScriptHttpTransport` 只能接收宿主注入的 `StoryboardMediaResolver`。resolver 校验 `content:` ref、grant TTL、digestVerified 和 `image/png`、`image/jpeg`、`image/svg+xml` MIME；SVG 必须先由 Scaena/CAS sanitizer 去除脚本、事件处理器、外部引用与网络资源。
- patch/accept/reject 继续携带 `Idempotency-Key`、`If-Match`、expected version/digest；409 和 unknown 保留原输入并 reconcile 原 operation，不换新 key。
- 首期性能目标：workspace 首屏 p95 ≤300ms、候选详情 ≤200ms、action admission ≤500ms，不含 Provider 时间。优先使用 PostgreSQL JSONB、keyset cursor、现有 GORM pool/timeout 和 `pg_stat_statements`；不新增 Redis/Elastic/PgBouncer/独立 projection service。
- `ScriptHttpTransport` 兼容 Scaena `SuccessEnvelope`、嵌套 `projection/storyboard` 和旧 `creative_storyboard_projection`；contract mismatch 只输出安全 response-shape/request-id 诊断。
- `/__dev/scaena` 只用于同源开发联调；正式运行必须使用宿主注入的认证 adapter 和媒体 resolver。

迁移 runbook 位于 `agent/scaena/docs/operations/storyboard-postgres-migration.md`；任何 SQLite→PostgreSQL apply 都必须 dry-run、显式 confirm、GORM 写入、verify 后再切换，原 SQLite 保留为只读回滚源。

## OpenDesign 工作流

先使用 OpenDesign MCP 读取 project metadata、file metadata 和 entry file；文件读为空时使用 MCP 返回的 preview URL 做只读 HTTP 回读。远端写回必须先读取 baseline digest，再逐文件写入和逐文件 SHA-256 readback；digest 冲突时拒绝覆盖。

## 页面验收

- 1440×900、1280×800、1024×768、820px 和 390px。
- 浅色/深色主题、键盘选择、Escape 焦点恢复和 `prefers-reduced-motion`。
- ready、partial、stale、offline、permission、contract mismatch、unknown action。
- 候选 A/B、显式预览、镜头表、动画预览、保存冲突、原操作回查、画布 focus 意图和返回 Director intent。

真实命令：

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run build && node scripts/assert-production-boundaries.mjs
MUWEAVE_E2E_PORT=4255 node scripts/run-e2e.mjs tests/storyboard-workspace.spec.ts tests/app-shell.spec.ts
```

禁止 race 检测、真实 Provider 调用、部署、发布和未授权 OpenDesign 覆盖写入。
