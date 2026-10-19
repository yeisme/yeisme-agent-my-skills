---
name: solocut-editing-workflow
description: Use when designing, specifying, implementing, or reviewing SoloCut's editing workbench: media bins, script/storyboard, candidate review, dialogue and subtitle timing, timeline edits, operation recovery, and delivery handoff.
---

# SoloCut Editing Workflow

SoloCut 是剪辑软件和跨 owner 的编辑工作台。它组合公开合同，不拥有 Scaena、Auctra、Sonora、Eikona 或 DriveBridge 的 canonical state。

## 先读

1. `client/solocut/AGENTS.md`
2. `client/solocut/docs/design/opendesign-progress.md`
3. `client/solocut/docs/design/formal-frontend-shell.md`
4. `client/solocut/docs/product/information-architecture.md`
5. `client/solocut/docs/protocols/api-contract.md`
6. `client/solocut/openspec/changes/solocut-editing-workbench-specification-v1/`

## 产品边界

| 能力 | owner |
| --- | --- |
| 工程上下文、页面草稿、时间线 UI、候选比较 | SoloCut client |
| 制作计划、候选任务、采用、EditRevision、RenderPlan | Scaena |
| 接受剧本、对白版本、语义事件 | Auctra |
| 实际音频、词级时间、字幕来源 | Sonora |
| 图片绑定、视觉候选与资格 | Eikona |
| 文件引用、传输、交付回执 | DriveBridge |

SoloCut 不实现 3D 视口、相机、场景编辑、WebGL、Provider adapter 或第二份制作时间线。

## 主路径

```text
项目库 → 简报 → 脚本与分镜 → 候选 → 声音与节奏 → 时间线精剪 → 审阅 → 交付
```

每个阶段都必须分别表达：loading、empty、error、permission、pending、unknown、conflict、cancelled 和 recovery。

## 编辑不变量

- 候选完成不会自动改变正式时间线。
- 人工采用才会生成新的 EditRevision。
- 改对白先计算音频、词级对齐、字幕和关联镜头的影响范围。
- 改字幕样式只重做字幕合成；替换图片只影响绑定镜头。
- 手动修改或锁定范围使冲突提案过期，不覆盖手动内容。
- unknown 只查询原 operation identity，不换 key 重提。
- 任务完成、内容采用、渲染通过、交付确认和文件回存必须分开。

## OpenDesign 使用

OpenDesign 是设计参考和交互基线。使用 MCP 读取当前项目时，先完成工具发现和会话检查；会话过期时记录 `OPENDESIGN_MCP_SESSION_EXPIRED`，不要猜测远端内容，也不要把本地 HTML 当作远端回读。只迁移 tokens、布局、状态和交互语义，不复制原型源码、chunks、IndexedDB 或 mock service。

## 阶段路由

- `FRONTEND`：React 页面、tokens、状态面板、键盘和 Playwright。
- `BACKEND`：Go API、GORM、ETag、幂等和 operation recovery。
- `INTEGRATION`：公开 owner projection 的最小读取链路。
- `DOCS`：产品、接口、验收和 skill 更新。

阶段没有真实依赖时标记 `BLOCKED` 或 `INTEGRATION_PENDING`，不使用 DemoAdapter 冒充真实结果。

## 验证命令

```bash
cd client/solocut
bun run typecheck
bun run test
bun run build
SOLOCUT_E2E_PORT=4300 bun run test:browser
openspec validate solocut-editing-workbench-specification-v1 --strict
```

后端：

```bash
cd client/solocut/server
go test ./...
go vet ./...
CGO_ENABLED=0 go build ./cmd/solocut
```

不运行 race，不执行付费模型、部署或未授权 owner 写入。
