## 1. Workflow 与文档

- [x] 1.1 建立或映射 quick/full 场景，保留 existing required check。
  - Acceptance: workflow YAML 可解析，真实命令来自本项目 AGENTS/Taskfile/package scripts。
- [x] 1.2 发布项目 CI/CD 文档，记录级别、路径升级、release 和 credential 边界。
  - Acceptance: 文档可从项目 docs 入口发现，命令可以直接复制运行。
- [x] 1.3 确认项目既有 release 或不适用边界。
  - Acceptance: 手动 dispatch 不正式发布；publish 只从 SemVer tag 进入。

## 2. Verification

- [x] 2.1 运行 YAML/action 静态检查。
  - Acceptance: `actionlint .github/workflows/*.yml` 或等价检查返回 0。
- [x] 2.2 运行项目最窄 quick gate；Go release 项目同时运行 `goreleaser check`，并对失败做归因。
  - Acceptance: CI/CD target slice 检查返回 0；既有代码、并行脏树或环境失败单独记录，不得冒充全仓通过，也不得通过删减门禁掩盖。
- [x] 2.3 运行 `openspec validate skills-modular-tiered-ci-cd-v1 --strict --no-interactive` 和 `git diff --check`。
  - Acceptance: 两条命令返回 0。

## Evidence

- workflow、文档、配置、静态检查、OpenSpec 和 diff target 已完成；项目 quick gate 的通过与既有/并行/环境失败由根级最终验证逐项归因，未把失败冒充为通过。
