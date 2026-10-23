---
name: muweave-3d-director-workspace
description: Use when designing or implementing MuWeave's contract-first 3D Director workspace with safe launch context, preview-only stage states, revision checks, handoff actions, and responsive review behavior.
---

# 幕织 3D 导演台

## 目标

把 OpenDesign 的导演流程承接为 MuWeave 的 Director feature package。Scaena ReplicaStage 是 stage、revision、freeze、control pass 和 artifact refs 的唯一 owner；MuWeave 通过宿主注入的 adapter 提供只读 WebGL 预演消费层，不写回场景或引擎状态。

## 先读的来源

- `client/muweave-frame-studio/docs/design/creative-workspaces-ui-spec.md`
- `client/muweave-frame-studio/docs/architecture/creative-workspaces-contract-boundary.md`
- `client/muweave-frame-studio/src/contracts/workspaces.ts`
- `temp/open-design/pane-track-polish-v11-20261007/drama-development-center-unified/docs/director-flow-implementation.md`
- `temp/open-design/pane-track-polish-v11-20261007/drama-development-center-unified/docs/production-integration.md`
- `agent/scaena/docs/protocols/replica-stage.md`
- `agent/scaena/docs/protocols/replica-stage-consumer-handoff.md`

## 不变量

- 只写 `src/features/director/`、页面测试和页面文档；共享合同、路由、Shell 和 registry 交给 L0。
- 页面只消费 `DirectorLaunchContextV1`、`DirectorProjectionV1` 和 typed action descriptors。
- 上下文必须包含 project、scene、可选 shot、source revision、return route 和 safe object refs。
- 不接受原始 Prompt、私有路径、provider payload、凭据或可直接执行的引擎命令。
- 舞台状态必须明确显示 `unavailable`、`preview_only` 或 `ready`。只有有效的 frozen/current stage、control pass、GLB/glTF artifact 和 digest 校验通过时才能显示“3D 预演可用”。
- WebGL viewer 必须懒加载、释放 GPU 资源、处理 WebGL 不可用、artifact 解析失败和 digest mismatch；mock 仅在开发环境显式 `?mode=mock`。
- committed ReplicaStage fixture 只能通过显式 `?mode=fixture` adapter 使用，页面必须显示 fixture 来源，不得把 fixture 当成 live production。
- 宿主负责 HTTP、认证、access grant、artifact fetch 和 digest verification；客户端不得出现 `/api/v1`、grant URL 或凭据。
- viewer 只读消费 `DirectorPreviewManifestV1` 与 `DirectorArtifactRefV1`，不接受任意 URL、私有路径或引擎命令。
- 重新排演、准备交接和返回分镜必须携带 expected revision、idempotency ref 和 disabled reason。
- 来源 revision 过期、权限不足、合同不匹配或离线时阻断动作，不自动创建新请求。

## 页面结构与交互

- 上下文栏展示项目、场景、镜头、revision 和返回分镜。
- 中央区域展示标注清晰的 preview-only/unavailable 舞台。
- 镜头序列栏展示相邻镜头和时长摘要；Inspector 展示镜头意图、景别、运镜和能力状态。
- Escape 关闭覆盖层并恢复焦点；移动端只支持浏览、审批和低风险输入。
- `prefers-reduced-motion` 下保留状态和焦点反馈，不用动效伪造排演完成。

## 必须验证

- launch context 的 project/scene/shot/revision/return route 校验。
- stage unavailable、preview only、permission required、contract mismatch、stale、offline。
- 返回分镜和交接 route intent 不复制领域数据。
- 1440×900、1280×800、1024×768、820px 和移动布局。
- Scaena feature gate 关闭时必须显示 `OWNER_UNAVAILABLE`，不得静默回退 mock。
- 证据写入 `temp/integration-test-runs/<run-id>/`，不得包含 secrets、Prompt、Provider payload 或完整推理。

真实命令：

```bash
cd /home/yeshugen/workplace/yeisme-agent/client/muweave-frame-studio
bun run typecheck
bun run test:unit
bun run test:e2e
bun run build
```

Scaena 适配器验证：

```bash
cd /home/yeshugen/workplace/yeisme-agent/agent/scaena
go test ./internal/application/production -run TestReplicaConsumerHandoffFixture -count=1
```

禁止 race 检测、真实 Provider 调用、生产部署和跨 feature import。MuWeave 的 WebGL viewer 只读，不代表 Scaena 真实引擎已经接通。
