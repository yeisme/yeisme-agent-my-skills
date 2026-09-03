## Why

本项目需要把 CI/CD 映射到统一的分级与场景语义，避免普通 PR 等待无关重任务，也避免默认分支或发布漏跑必要门禁。

## What Changes

- 为 `Yeisme Skills` 建立项目自有的 quick/full workflow 与文档。
- 保留现有 required check 和 release 入口；新增配置全部采用最小权限。
- 超过 180 行的 workflow 按 snapshot/publish 或独立职责拆分。

## Capabilities

### New Capabilities

- `modular-tiered-ci-cd`: 本项目的模块化、分级、按场景执行 CI/CD。

### Modified Capabilities

无。

## Impact

- `.github/workflows/**`
- `docs/ci-cd.md`
- 现有项目质量门与 release contract
