# Yeisme Skills CI/CD

本项目采用根级 `docs|quick|full|integration|release` 语义，但 workflow、命令和证据由本仓库自己维护。Profile：`skills/content`。

## 分级

### quick

普通源代码 PR 的快速门禁：

- `python3 scripts/validate_repository.py`

### full

默认分支以及 workflow、dependency/lock、Taskfile/package scripts、schema/contract、migration 变化进入 full：

- `python3 scripts/validate_repository.py`
- `python3 scripts/test_network_install.py`

### integration

integration/component/system/e2e、compose、staging 或 adapter conformance 变化进入 integration；真实凭据、付费 provider 和生产环境不属于普通 CI：

- 不适用；原因见本页说明。

### release

No binary CD; publication follows the skills repository owner workflow.

手动触发只允许验证、integration 或 snapshot。正式发布必须来自项目约定的 SemVer tag，并在 publish job 重新执行 mandatory gates。

## 模块和兼容

- 小于 100 行且职责单一的 workflow 可以保持单文件。
- 超过 180 行的项目自有 workflow 必须按 source/test/analysis/build/integration/snapshot/publish 拆分，或记录有界例外。
- 现有 required check 名称保持兼容；拆分时由稳定聚合 job 汇总结果。
- CI 默认 `permissions: contents: read`，PR checkout 使用 `persist-credentials: false`；写权限只出现在明确的 publish/sync job。

## 本地检查

运行与当前变更相匹配的最小命令，再在 final gate 运行 full 或 integration。不得把未运行、被中断或因环境缺失跳过的命令写成通过。
