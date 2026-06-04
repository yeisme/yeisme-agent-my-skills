---
name: golang-github-release-guardrails
description: Use when creating, reviewing, or modifying a Go/Golang project that involves GitHub, Git repository management, CI, release, tags, pull requests, or distribution; enforce GitHub Actions, golangci-lint, and GoReleaser as required project guardrails.
---

# Golang GitHub Release Guardrails

## 使用场景

当任务同时满足以下条件时必须使用本 skill：

- 项目是 Go/Golang 项目，或本次改动影响 `go.mod`、Go CLI、Go 服务、Go SDK、Go 工具链。
- 任务涉及 GitHub 或 Git 管理，包括仓库初始化、PR、branch、tag、release、CI、lint、发布制品、版本管理、自动化工作流或仓库治理。

如果任务同时涉及 Go CLI 架构、Cobra/Viper、配置层、命令边界或公共模块提取，也同时使用 `golang-cobra-viper-cli-architecture`。本 skill 只负责 CI、lint 和 release 护栏。

## 强制规则

任何涉及 GitHub/Git 管理的 Go 项目，都必须具备以下三类文件或等价配置：

1. GitHub Actions workflow：至少包含 CI workflow。
2. golangci-lint 配置：项目根目录或 Go 模块根目录必须有 `.golangci.yml` 或 `.golangci.yaml`。
3. GoReleaser 配置：项目根目录或 Go 模块根目录必须有 `.goreleaser.yaml` 或 `.goreleaser.yml`。

如果缺任意一项，不要只提醒用户；默认直接补齐，除非用户明确要求只做分析或禁止改文件。

## 放置规则

- 单仓库 Go 项目：文件放在仓库根目录。
- monorepo 中的独立 Go 模块：文件放在该 Go 模块根目录；如果 GitHub Actions 只能由仓库根目录触发，则 workflow 放在仓库根 `.github/workflows/`，并使用 `working-directory` 指向模块。
- 子模块或独立远端仓库：优先把 workflow 和配置放在子模块仓库根目录，避免父仓库替子仓库发布。

## 最低文件集

```text
<go-module-root>/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .golangci.yml
└── .goreleaser.yaml
```

## CI 最低要求

CI workflow 至少包含：

- `actions/checkout`，PR 场景必须设置 `persist-credentials: false`。
- `actions/setup-go`，优先用 `go-version-file: go.mod`。
- `go mod download` 和 `go mod verify`。
- `go mod tidy && git diff --exit-code go.mod go.sum`。
- `go test ./...`。
- 如有 daemon、并发、socket、worker、队列或状态机，必须增加 `go test -race ./...`。
- `golangci-lint`，版本固定，不使用 `latest`。
- `go build` 或等价 smoke build；CLI 项目必须运行二进制 `--help`。
- `goreleaser check`。

完整 GoReleaser snapshot 构建可能很慢。默认 PR CI 可以只跑 `goreleaser check`；完整 `goreleaser release --snapshot --clean --skip=publish` 至少要在手动 CI、release workflow 或发布前本地验证中存在。

## Release 最低要求

Release workflow 必须满足：

- 只允许 semver tag 触发真实发布，例如 `vX.Y.Z`、`vX.Y.Z-alpha.N`。
- `workflow_dispatch` 只能构建 snapshot，不能直接发布正式 GitHub Release。
- 发布前复跑测试、lint 和 `goreleaser check`，不要只依赖人工记忆。
- `permissions` 最小化：CI 用 `contents: read`，release 才用 `contents: write`。
- 使用 `GITHUB_TOKEN`，不要要求 PAT，除非有明确跨仓库发布需求。
- 建议使用 protected environment，例如 `release`。

## golangci-lint 策略

- 初版门禁要能通过当前代码，优先启用低噪声规则，例如 `govet`、`ineffassign`、`misspell`。
- 如果项目已有较高质量基础，可以启用 `errcheck`、`staticcheck`、`unused`、`revive`。
- 若严格规则会引出大量历史问题，不要让首版 CI 变成不可落地的重构项目；先记录专项清理，再逐步打开规则。
- 禁止无原因的宽泛 `nolint`。局部关闭必须写成 `//nolint:<linter> // 中文原因`。

## GoReleaser 策略

- CLI 项目必须通过 GoReleaser 发布跨平台二进制。
- 默认覆盖 `linux`、`darwin`、`windows`，以及 `amd64`、`arm64`。
- Windows archive 用 zip，其他平台可用 tar.gz。
- 必须生成 checksums。
- 如果面向真实用户分发，优先增加 SBOM；需要更高供应链保证时再接入 cosign keyless signing。
- release hook 不要执行会修改源码的命令，例如 `go mod tidy`；应使用 `go mod download` 和 `go mod verify`。

## 工作流程

1. 定位 Go 模块根目录：读取 `go.mod`，确认 module path、CLI 入口和仓库边界。
2. 检查是否已有 `.github/workflows/`、`.golangci.yml`、`.goreleaser.yaml`。
3. 缺失则补齐；已有则按本 skill 的安全和发布规则审查并修正。
4. 更新 README 或相邻文档，说明本地验证、CI、tag 发布和 snapshot 命令。
5. 本地验证至少运行：

```bash
go mod tidy && git diff --exit-code go.mod go.sum
go test ./...
golangci-lint run
goreleaser check
```

如果项目包含并发运行时或 daemon，还必须运行：

```bash
go test -race ./...
```

如果时间允许或用户要求发布前验证，运行：

```bash
goreleaser release --snapshot --clean --skip=publish
```

## 例外

- 临时实验目录、一次性 spike、教学片段可以不补发布链路，但必须在回答中明确“不适合作为正式 GitHub Go 项目发布”。
- 如果项目不使用 GitHub，而是 GitLab/Gitea 等平台，仍必须保留 golangci-lint 和 GoReleaser；CI workflow 改用对应平台的 pipeline 文件。
- 如果用户明确要求只写文档或只做 review，不主动改文件，但必须把缺失项列为阻塞问题。
