---
name: golang-cobra-viper-cli-architecture
description: Use when designing, implementing, refactoring, or reviewing a Yeisme Go/Golang CLI, especially when choosing Cobra/Viper defaults, command/config/output boundaries, and reusable internal modules.
---

# Golang Cobra Viper CLI Architecture

## 使用场景

当任务涉及 Yeisme 的 Go CLI 设计、实现、重构或审查时使用本 skill，尤其是：

- 新建 Go CLI 子项目或为现有 Go 项目补 CLI。
- 调整 Cobra 命令树、flag、completion、help text 或命令依赖注入。
- 设计 Viper 配置层、环境变量覆盖、profile、本地配置或配置校验。
- 提取 `internal/config`、`internal/output`、`internal/cli`、runner、redaction、diagnostics 等公共模块。
- 需要判断项目内复用、跨子项目复用、还是保持局部实现。

如果任务涉及 CLI 输出合同，同时使用 `ai-native-cli-output-contract`。如果任务涉及 GitHub CI、tag、release 或二进制分发，同时使用 `golang-github-release-guardrails`。

## 默认技术基线

没有明确相反需求时，Yeisme Go CLI 默认采用：

- Go module，入口为 `cmd/<app>/main.go`。
- Cobra / pflag 负责 command tree、flags、completion、help 和 `RunE`。
- Viper 负责 defaults、config files、environment overrides 和 typed config unmarshal。
- `internal/*` 承载业务、输出、配置、runner、存储和 provider adapter；命令层只接线和渲染。
- Default CLI human output is English; local project docs and OpenSpec artifacts default to Chinese; machine protocol fields remain stable English.

允许例外，但必须写清原因：

- 极小一次性工具且无配置文件、无环境变量覆盖、无 profile：可以只用 Cobra，不引入 Viper。
- 已有成熟框架或产品形态要求不同：遵守子项目 `AGENTS.md`，不要强行迁移。
- 服务端、MCP server 或 library-only Go module：只复用本 skill 中适用的配置、输出和边界规则。

## 参考形状

GitPulse 是当前参考实现：`cmd/gitpulse` 负责 Cobra 命令和用户输出接线，`internal/config` 负责 Viper 配置，`internal/output` 负责多格式渲染，领域能力放在 `internal/<domain>`。

新项目优先使用更容易提取公共模块的分层：

```text
cmd/<app>/main.go
internal/cli/
  root.go
  deps.go
  <domain>_cmd.go
internal/config/
  config.go
  defaults.go
  loader.go
  validator.go
internal/output/
  projection.go
  render.go
  json.go
  agent.go
  redaction.go
internal/runtime/
  runner.go
  clock.go
  filesystem.go
internal/<domain>/
  service.go
  model.go
  adapter.go
testdata/
```

如果现有项目已经像 GitPulse 一样把命令放在 `cmd/<app>`，不要为了目录纯度做大迁移；新增公共能力时可以先落到 `internal/cli`、`internal/config` 或 `internal/output`，再逐步移动薄命令。

## Cobra 规则

- `main.go` 只创建 root command、注入版本信息并执行；不要放业务逻辑。
- 每个命令使用 `RunE`，返回 error，由根执行层统一决定 stdout/stderr 和退出码。
- Cobra command 只解析参数、构造请求、调用 service、选择 renderer。
- 长逻辑不要写进 `PreRunE` 或 `RunE`；抽到 service 或 use case。
- 使用 `context.Context` 贯穿命令执行、外部命令、网络请求和长任务。
- Flag help must be English; command names, flag names, and schema keys stay stable English.
- Public options must be long-flag-first: `--help` teaches `--long-name` as the default surface, docs/examples show the long flag first, and short aliases are optional.
- Do not mint lowercase short aliases for new Yeisme-specific flags. If a short alias is truly needed, use an uppercase letter such as `-A`; keep lowercase aliases only for established conventions already used by that CLI, such as `-h` or an existing `-v`.
- Tests for new flags must cover `--help`, the long flag, any uppercase short alias, and the absence or rejection of accidental lowercase aliases.
- completion 函数只做轻量读取，不触发危险操作或远程写入。
- 测试中通过 command factory 创建新实例，避免全局 command 和全局 flag 污染。

## Viper 规则

- 配置优先级默认是：explicit flag > env > local config > project config > global config > defaults。
- env prefix 使用大写应用名，例如 `GITPULSE_`、`EIKONA_`；嵌套 key 用 `_` 替代 `.`。
- 用 `mapstructure` tag 定义 typed config；读取后必须执行显式 `Validate()`。
- defaults 必须同时服务于 Viper 和纯 struct 测试，避免默认值散落在命令层。
- config path 使用 XDG 优先，兼容旧路径时要有迁移或 fallback 说明。
- 写配置时只写用户请求的目标文件；不要在普通只读命令中隐式创建或改写配置。
- 用户级本地 config 或用户级 secret store 可以保存用户显式提交的本地 CLI 凭据；project/repo config、示例配置、日志、trace、测试 fixture、运行证据和错误详情不得包含真实 secrets、tokens、cookies 或 auth headers。
- env 继续用于 CI、部署和临时 shell 覆盖，但不要创建、推荐或兼容新的 shell credential script 作为本地持久化层。
- 文件监听、热加载和 profile 合并只有在产品真的需要时才加入。

## 输出和错误

- 所有输出模式从同一个 projection 渲染，遵守 `ai-native-cli-output-contract`。
- Default stdout is an English summary or table; `--json` stdout is JSON only; `--agent` is low-token key=value; diagnostics and logs go to stderr.
- renderer 不调用业务 service；业务层不拼接本地化 CLI 文案。
- 错误分为用户输入错误、环境错误、外部依赖错误、内部错误；面向人的错误给出可执行下一步，机器输出保留稳定 error code。
- 脱敏在 projection 或 renderer 边界统一处理，不依赖调用点自觉。

## 公共模块提取

优先级：

1. 先在当前子项目内提取窄接口的 `internal/*` 模块。
2. 至少两个 Yeisme Go CLI 出现稳定重复后，再考虑独立公共 Go module。
3. 跨子项目公共 module 必须是独立子项目或独立远端仓库；不要用相对路径穿透 submodule 边界。
4. 公共 module 只放稳定横切能力：输出 envelope、renderer、redaction、config loader、runner、test helpers、diagnostics。
5. 不要把产品领域模型、provider token 行为、具体工作流策略抽成公共模块。

提取前检查：

- API 是否比复制少维护成本。
- 是否有跨项目契约测试或 golden tests。
- 是否不会迫使简单 CLI 引入 daemon、TUI、数据库或 provider 依赖。
- 是否保留项目级 override，而不是把产品差异塞进一堆布尔参数。

## 工作流程

1. 进入拥有代码的子项目，读取 `AGENTS.md`、`go.mod`、现有 command/config/output 包。
2. 判断现有形态：GitPulse-style `cmd/<app>` 命令层、`internal/cli` 命令层，或其它结构。
3. 为新能力确定边界：
   - command wiring 放 Cobra 层
   - config loading/validation 放 `internal/config`
   - projection/rendering 放 `internal/output`
   - business/use case 放 `internal/<domain>`
   - external CLI/API 放 adapter/provider 包
4. 先写或更新最靠近行为的测试，再改实现。
5. 如果发现重复代码，按“项目内提取优先、跨项目提取谨慎”的规则处理。
6. 更新 CLI help、README 或子项目 docs，命令示例必须是用户可直接运行的真实命令。

## 验证

按子项目 `AGENTS.md` 运行本地门禁。Go CLI 通用检查至少包含：

```bash
gofmt -w <changed-go-files>
go test ./...
go build ./...
```

命令或输出变更还要验证：

```bash
go test ./cmd/... ./internal/cli/... ./internal/config/... ./internal/output/...
```

配置层变更要覆盖：

- defaults only
- global config
- project config
- local config
- env override
- explicit flag override
- invalid config

CLI 输出变更要覆盖：

- default human output
- `--json`
- `--agent`
- `--events`，如果该命令支持流式事件
- stdout/stderr 分离
- secret redaction

命令级 e2e、process e2e、stdout/stderr golden、fixture 文件树和完整用户流程默认使用 `github.com/rogpeppe/go-internal/testscript`。不要为这些场景手写大量 shell wrapper 或自定义 golden runner，除非子项目已有更强的本地 harness。

推荐形态：

```go
package e2e

import (
	"testing"

	"github.com/rogpeppe/go-internal/testscript"
)

func TestScripts(t *testing.T) {
	testscript.Run(t, testscript.Params{
		Dir: "testdata/script",
	})
}
```

推荐目录：

```text
tests/e2e/
  cli_script_test.go
testdata/script/
  status.txt
  config-errors.txt
  workflow-happy-path.txt
```

常用命令：

```bash
go test ./tests/e2e -run TestScripts -count=1
```

## 边界

- 本 skill 不替代子项目 runtime skill；业务规则以子项目 `AGENTS.md` 和对应 domain skill 为准。
- 本 skill 不要求所有 Go 项目都改造成 GitPulse；它提取的是默认架构和复用原则。
- 本 skill 不处理发布链路；GitHub Actions、golangci-lint 和 GoReleaser 由 `golang-github-release-guardrails` 约束。
