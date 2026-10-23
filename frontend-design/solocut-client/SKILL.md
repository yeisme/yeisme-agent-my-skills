---
name: solocut-client
description: Use when planning, specifying, reviewing, or implementing the SoloCut director client in client/solocut. Enforces the OpenDesign progress gate, owner boundaries, public contracts, and honest task, candidate, adoption, render, and delivery states before any code change.
---

# SoloCut Client

SoloCut 是已批准的跨 owner 导演客户端，代码入口是 `client/solocut`。本 skill 负责任务路由和边界，不实现 UI，也不替代 owner 的领域规则。

## 先读

1. `client/solocut/AGENTS.md`
2. `client/solocut/docs/design/opendesign-progress.md`
3. `client/solocut/docs/design/visual-direction.md`
4. `client/solocut/openspec/changes/solocut-formal-client-foundation-v1/design.md`
5. 根 `docs/architecture/solocut-product-boundary.md`

## 边界

| 能力 | 归属 |
| --- | --- |
| 页面草稿、导航、布局偏好 | SoloCut |
| 制作计划、候选、采用、渲染 | Scaena |
| 接受文本和语义事件 | Auctra |
| 音频、词级时间和字幕来源 | Sonora |
| 图片绑定和当前资格 | Eikona |
| 文件引用和传输回执 | DriveBridge |
| 原片观察和参考包 | Anatomia |
| 模型能力、路由和原任务 | Aigora |

不得读取 owner 私有存储，不得保存 Provider 凭据，不得复制第二份时间线、候选账本或权利账本。

## 实现门禁

没有用户明确的实现授权时，只修改规格、文档和 skill。

同时满足以下条件后才允许单独的实现 change 修改产品代码：

- 用户已接受 `solocut-agent-editor/base.html` 作为设计与交互基线；当前条件已满足。
- 新增页面补齐对应 UI Spec、组件状态和响应式验收。
- 每个真实 owner 接线有 typed contract、错误、权限、幂等、恢复和独立 `INTEGRATION` 任务。
- 演示数据、合成媒体和未接线能力在界面上保持明确标记。

## 状态

任务受理、任务成功、待审阅、已采用、渲染通过、交付接受、文件回存和结果未知必须分开。未知结果只用原 identity 查询，取消后的迟到结果不得回写。

## OpenDesign 基线

以 `solocut-agent-editor/base.html` 为基线读取以下事实：

- `apple-token-contract`：颜色、字体、间距、圆角、阴影、焦点和动效。
- `project-library`：项目库布局和空状态。
- `agent-integration-entry`：Agent × 精剪入口。
- `continue-creation`：简报、导演协作、精剪成片路径。

只迁移设计合同和交互语义，不复制 HTML、Next.js chunks、静态资源、IndexedDB 或 demo service。

## 后续阶段路由

开始新任务前先读取：

- `client/solocut/docs/architecture/next-phase-roadmap.md`
- `client/solocut/docs/verification/phase-acceptance-matrix.md`
- `client/solocut/openspec/changes/solocut-next-phase-specification-v1/`

按单一阶段开工：

- `FRONTEND`：只修改 `src/`、前端测试和 mock；Go API 合同只读。
- `BACKEND`：只修改 `server/` 和后端证据；不做页面验收。
- `NATIVE`：只修改 `desktop/` 和 native bridge；浏览器 fallback 必须保留。
- `INTEGRATION`：只验证列出的最小真实链路，证据写入 `temp/integration-test-runs/<run-id>/`。

没有 PostgreSQL DSN、正式 auth、Tauri 系统依赖或 owner public contract 时，标记 `BLOCKED`/`INTEGRATION_PENDING`，不绕过合同。

## 验证

规格变更使用：

```bash
cd client/solocut
openspec validate solocut-formal-client-foundation-v1 --strict
```

skill 变更使用：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh profile validate client/solocut
scripts/skills.sh sync-target client/solocut
```

不要把规格校验写成测试、构建或真实联调通过。
