## Why

现有创作 Grilling 已具备领域入口与 Frontier 协议，但决策主要停留在单次聊天，难以恢复长期共创或检查上游改变的影响。用户选择从想法到成稿的逐步深度共创，需要专业问法连接 owner 的持久会话与真实写作候选，同时保持 Skills 可移植。

## What Changes

- 扩展 `creative-writing-core` 中既有共享协议与小说、漫剧、其他 AI 做剧分支，覆盖作品承诺、人物、结构、单元、场景、成稿和修订。
- 增加 owner-session 可选绑定和动作发现：从 owner 提供的版本化 projection 获得 Frontier、版本、待验证项和可执行动作，缺能力时诚实回退。
- 保留 projectless chat-only、领域明确时零路由追问、同轮问题无依赖、可反驳建议和共同理解确认。
- 确认阶段成果后串行交接最窄 writer，接收试写或候选后回到受影响的决策；不让访谈 Skill 自行写正文或接受 Canon。
- 扩充静态矩阵与人工共创验收说明，明确当前项目内反馈、未来跨作品偏好和自动创作的分期。

## Capabilities

### New Capabilities

- `creative-grilling-owner-session`：专业 Frontier、可恢复 owner binding、写作交接、宿主问答适配与兼容降级。

### Modified Capabilities

无。本 source 尚无同名主规范；已有 Skill 名称、v0.1 route/brief/handoff 继续可用，新 owner-session binding 是可选版本化扩展。

## Impact

- 仅拥有 `creative-writing-core/` 下既有 Skills、references 和验证脚本；不修改 `auctra-novel/`、`ai-drama/` 等独立源子模块。
- 产品状态由 consumer owner 保存；本源不持有正文、Canon、数据库、任务租约或 provider 凭据。
- 宿主提供问答控件时使用结构化提问，否则使用编号文本；不依赖特定宿主 Plan 模式。
- 不创建新 Router，不批量激活 Skills，不在本次规格交付中修改 runtime 副本或安装配置。
