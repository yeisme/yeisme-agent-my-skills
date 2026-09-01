# 云端安装开发 Skills 组合

这份指南覆盖通用编码、Go 后端、Go CLI、Rust/原生高性能、前端 UI、全栈项目和快速 demo。所有第一方组合都从同一个云端聚合仓库安装：

```text
https://github.com/yeisme/yeisme-agent-my-skills
```

Ponytail 使用它自己的上游仓库：

```text
https://github.com/DietrichGebert/ponytail
```

先查看聚合仓库当前可安装的 Skills：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills --list
```

## 组合原则

- 现有项目普通改动直接进入实现，不强制完整项目工作流。
- 新项目或正式 MVP 才启用 `project-development-router`，先选择 `quick-demo`、`full-project` 或 `workflow-off`。
- 每个阶段只让一个 primary workflow 主导；语言、性能、前端质量等作为约束或后续阶段运行。
- 性能优化先测量，再改代码；Rust 只用于有证据的原生/系统热路径，不用于整仓重写。
- Ponytail 是可选的最小实现约束，不替代安全、数据保护、无障碍和必要测试。
- review、QA、security、release 和完整集成证据按风险或交付阶段加载，不塞进每个日常编码组合。

## 组合速查

| 场景 | 默认组合 | 按需追加 |
| --- | --- | --- |
| 现有仓库写代码、修 bug、重构 | `yeisme-coding-execution-driver` | `ponytail` |
| 新项目或正式 MVP | `project-development-router` + `yeisme-coding-execution-driver` | `vertical-slice-delivery`、`project-integration-test-evidence` |
| Go 后端、API、worker、MCP、daemon | `backend-system-workflow` + `go-rust-implementation-defaults` | `performance-profiler`、`project-integration-test-evidence` |
| Go CLI | `golang-cobra-viper-cli-architecture` + `go-rust-implementation-defaults` | `backend-system-workflow`、`project-integration-test-evidence` |
| Rust 或原生高性能内核 | `performance-profiler` → `go-rust-implementation-defaults` → `yeisme-coding-execution-driver` | `ponytail` |
| React/Web 前端 | `yeisme-frontend-design-router` + `ui-spec-frontend-workflow` | `yeisme-frontend-quality-workflow`、`yeisme-ui-motion-quality` |
| 前后端完整垂直切片 | `project-development-router` + `vertical-slice-delivery` | `api-contract-parallel-workflow`、`project-integration-test-evidence` |
| 快速 demo | `project-development-router` 的 `quick-demo` 模式 | `ponytail` |
| 不使用完整工作流 | 不安装或停用 `project-development-router` | 只保留当前任务需要的一个 Skill |

## 通用写代码

安装执行入口：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill yeisme-coding-execution-driver \
  --yes
```

可选安装 Ponytail：

```bash
npx --yes skills add https://github.com/DietrichGebert/ponytail \
  --skill ponytail \
  --yes
```

直接复制给 Agent：

```text
请为当前项目配置通用编码工作流。

第一方 Skills 仓库：
https://github.com/yeisme/yeisme-agent-my-skills

Ponytail 仓库：
https://github.com/DietrichGebert/ponytail

执行：
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills --skill yeisme-coding-execution-driver --yes
npx --yes skills add https://github.com/DietrichGebert/ponytail --skill ponytail --yes

读取最近的 AGENTS.md 和现有代码路径，复用项目已有语言、框架、依赖、测试工具和实现模式。普通功能、修复和重构直接完成本地实现、 focused tests 和必要文档，不自动启动完整 PRD、架构评审、QA 或发布链。Ponytail 使用 full 强度，优先现有代码、标准库、平台能力和已安装依赖；不能简化掉安全、错误处理、无障碍和必要测试。

不要 commit、push、发布或部署，除非我明确授权。完成后报告修改文件、验证命令、测试结果、保留的风险和刻意没有引入的复杂度。
```

## Go 后端、API、Worker、MCP 或 Daemon

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill backend-system-workflow \
  --skill go-rust-implementation-defaults \
  --skill yeisme-coding-execution-driver \
  --yes
```

直接复制给 Agent：

```text
请从 https://github.com/yeisme/yeisme-agent-my-skills 为当前项目安装并使用以下 Skills：
- backend-system-workflow
- go-rust-implementation-defaults
- yeisme-coding-execution-driver

安装命令：
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills --skill backend-system-workflow --skill go-rust-implementation-defaults --skill yeisme-coding-execution-driver --yes

以 backend-system-workflow 作为当前实现的 primary，以 go-rust-implementation-defaults 作为语言和运行时约束。优先项目现有语言；服务、MCP、gateway、worker、daemon 或单文件发布边界明确时再选择 Go。Go 默认 pure Go，正常 build/test/release 路径保持 CGO_ENABLED=0。数据库业务访问使用 GORM；不要在 handler 或普通业务逻辑中硬编码 SQL。并发、幂等、超时、取消、错误传播、健康检查、日志和资源预算必须有明确行为。

先运行现有测试，再实现最小垂直改动。普通 Go 单元和服务测试使用 go test、httptest 和 table-driven tests；CLI 用户流程优先复用 testscript。只有 integration、component、system 或 e2e 入口才写集成证据。完成后报告架构边界、真实命令、测试结果、CGO 状态和未解决风险。
```

## Go CLI

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill golang-cobra-viper-cli-architecture \
  --skill go-rust-implementation-defaults \
  --skill yeisme-coding-execution-driver \
  --yes
```

直接复制给 Agent：

```text
请从 https://github.com/yeisme/yeisme-agent-my-skills 安装 golang-cobra-viper-cli-architecture、go-rust-implementation-defaults 和 yeisme-coding-execution-driver，为当前项目实现或维护 Go CLI。

保持 command、config、application service、output renderer 和基础设施 adapter 边界清晰。优先 pure Go 和 CGO_ENABLED=0；配置遵循现有项目约定，不为了少量参数额外引入 Viper。人类默认输出、--agent、--json、stdout/stderr 和退出码保持稳定。复用现有测试系统；关键 CLI 用户路径使用 testscript 或项目已有 process test。不要自动发布 binary 或创建 GitHub Release。
```

## Rust 或原生高性能

先安装测量、决策和实现三个阶段需要的 Skills：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill performance-profiler \
  --skill go-rust-implementation-defaults \
  --skill yeisme-coding-execution-driver \
  --yes
```

直接复制给 Agent：

```text
请从 https://github.com/yeisme/yeisme-agent-my-skills 安装 performance-profiler、go-rust-implementation-defaults 和 yeisme-coding-execution-driver，为当前项目评估并实现高性能能力。

按阶段执行，不要同时启动三个 primary：
1. 先用 performance-profiler 建立 startup、latency、throughput、CPU、memory 或 allocation 基线，定位真实 hot path。
2. 再用 go-rust-implementation-defaults 判断保留现有语言、使用预构建 native package、拆成 Go 服务，还是实现小型 Rust/native kernel。
3. 只有测量证据证明必要时，才由 yeisme-coding-execution-driver 实施最小改动并做 before/after benchmark。

不要因为“追求性能”整仓改写 Rust。长运行服务、HTTP/MCP、worker、daemon、单二进制和并发控制优先评估 Go；parser、codec、WASM、内存敏感热路径、文件系统原语或确实需要维护的 native package 才评估 Rust。Rust 必须隔离在窄边界，通过稳定 API/FFI/package 被主项目消费，并提供 fallback、跨平台构建和回滚说明。

完成后报告测量基线、瓶颈证据、语言决策、改动范围、benchmark 对比和仍未达到的目标。
```

## React/Web 前端

基础组合：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill yeisme-frontend-design-router \
  --skill ui-spec-frontend-workflow \
  --yes
```

需要完成实现后的质量门时再追加：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill yeisme-frontend-quality-workflow \
  --skill yeisme-ui-motion-quality \
  --yes
```

直接复制给 Agent：

```text
请从 https://github.com/yeisme/yeisme-agent-my-skills 为当前项目安装 yeisme-frontend-design-router 和 ui-spec-frontend-workflow。需要实现后质量验证时，再安装 yeisme-frontend-quality-workflow；只有任务确实包含动效时才安装 yeisme-ui-motion-quality。

先读取现有设计系统、组件库、路由、状态管理、样式方案和截图，不要默认重建技术栈。由 frontend router 选择最小设计路径，再由 ui-spec-frontend-workflow 固化页面目标、状态、组件树、响应式行为、数据边界和验收截图，然后实现代码。优先现有组件、原生 CSS 和已安装依赖。必须覆盖 loading、empty、error、disabled、focus、keyboard、responsive 和 reduced-motion；不要为了“更高级”添加无意义动画或新 UI 框架。

实现完成后按项目现有命令运行 typecheck、unit/component tests 和必要的 Playwright/视觉检查。完成后报告页面路径、组件变化、交互状态、响应式与无障碍结果、截图证据和剩余问题。
```

## 前后端完整项目或正式 MVP

先安装项目路由和垂直切片入口：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill project-development-router \
  --skill vertical-slice-delivery \
  --yes
```

只有前后端需要并行合同或真实集成测试时再追加：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill api-contract-parallel-workflow \
  --skill project-integration-test-evidence \
  --yes
```

直接复制给 Agent：

```text
请从 https://github.com/yeisme/yeisme-agent-my-skills 为当前项目安装 project-development-router 和 vertical-slice-delivery。

先选择模式：快速 demo 使用 quick-demo；明确的正式项目或 MVP 使用 full-project；我说直接做、不用完整流程时使用 workflow-off。full-project 先确认 owner、目标用户、核心路径、稳定合同和最小垂直切片，再逐步选择前端、后端、API、测试和发布 Skills，不一次加载全部流程。

只有前后端确实需要并行时才安装 api-contract-parallel-workflow；只有存在 integration、component、system 或 e2e 测试入口时才安装 project-integration-test-evidence。先交付一条可运行的端到端用户路径，再扩展场景。不要自动 commit、push、部署或调用付费服务。
```

## 快速 Demo 与关闭完整工作流

快速 demo 只需要项目 Router：

```bash
npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills \
  --skill project-development-router \
  --yes
```

提示词：

```text
使用 project-development-router 的 quick-demo 模式。只实现能验证核心假设的最小可运行版本，复用现有技术栈和依赖，保留一个真实运行检查；不创建完整 PRD、OpenSpec、长期抽象、完整评审链或发布流程。明确标出 demo 的限制和升级到正式项目的触发条件。
```

关闭完整工作流：

```text
本次使用 workflow-off。不要加载 project-development-router 的完整项目流程，按最近的 AGENTS.md 和当前任务直接实现，只启用完成任务必需的 Skill。
```

## 安装后检查

查看实际安装结果：

```bash
find .agents/skills -mindepth 1 -maxdepth 2 -name SKILL.md -print | sort
```

Agent 应完整阅读实际启用的 `SKILL.md`，并报告：

- 使用的云端仓库 URL；
- 已安装 Skills 和安装目录；
- 当前阶段的 primary workflow；
- 兼容约束和稍后才运行的 audit/quality Skill；
- 未安装的高成本流程及原因；
- 项目真实验证命令和结果；
- 尚未执行的 commit、push、发布、部署、付费调用和生产写入。
