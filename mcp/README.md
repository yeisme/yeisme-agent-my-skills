# MCP Skills

MCP 构建、Gateway 维护/运营、服务发布、消费、Peering 和 registry onboarding 的治理模块。Skill 只描述流程；MCP server、transport、schema、adapter 和运行代码必须位于对应实现仓库。

Gateway V1 角色 Skill：

- `yeisme-mcp-gateway-maintainer`：修改、测试、发布 Gateway 源码。
- `yeisme-mcp-gateway-operator`：通过 Action Catalog、revision、approval 和 operation 运营已部署 Gateway。
- `yeisme-mcp-gateway-provider`：通过 Export Profile 发布显式授权的 MCP 能力。
- `yeisme-mcp-gateway-consumer`：消费本地或 Peer-origin Gateway 能力。
- `yeisme-mcp-gateway-peer-operator`：建立和维护单向、单跳可信 Peer。

Gateway Pack 只保存 Skill name/version 引用，不携带、安装、更新或热替换 Skill 内容。

MCP 操作路由与后端快路径：

- `yeisme-mcp-router`：把 MCP 操作意图（eikona/gitea/gateway 后端）路由到最窄操作 skill，统一首调校验与 digest 纪律。
- `gitea-mcp-quickstart`：gitea-mcp 紧凑面的两调用快路径（search→exec 复制 exec_example）与 guard/allowlist/错误恢复。
- per-backend 导航卡（consumer 增补）：`yeisme-mcp-gateway-consumer/references/backends.md`，导航非真源。
