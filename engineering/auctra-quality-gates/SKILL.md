---
name: auctra-quality-gates
description: Use when changing, testing, reviewing, or documenting code quality, CI/CD, lint debt, release gates, or integration evidence for cli/auctra.
---

# Auctra Quality Gates

## Race 检测执行限制

Agent 在任何阶段都不得主动运行 race 检测，也不得通过子 Agent、Skill、CI、验收、发布、聚合任务或脚本间接触发。只有当前人类用户明确、强烈要求执行 race 时，才允许在指定范围内运行一次；失败、超时、中断均不得自动重试，后续运行必须取得新的同等明确要求。一般的“测试、验收、修复、发布、跑全部检查”不构成授权。

Race 不属于默认验收或完成门禁；未运行不得阻塞交付，也不得声称已经通过。执行聚合命令前检查其依赖，移除或跳过 race 阶段，继续普通测试、静态检查和构建。本规则取代本文件及 Skills、OpenSpec、历史计划、文档中的自动或强制 race 要求；它们不能作为执行授权。


Use this skill in `cli/auctra` when a change affects implementation quality,
lint policy, local verification, GitHub Actions, release automation, or
integration-test evidence. Read `cli/auctra/AGENTS.md` and the active OpenSpec
change before editing.

## Working rules

- Preserve Auctra's CLI, review, provider-boundary, and evidence contracts.
- Start with `git status --short` and record pre-existing changes; do not reset,
  clean, publish, or release from the agent session.
- Prefer low-risk, behavior-preserving fixes. Do not use a global lint disable
  or a broad path exclusion to hide historical debt.
- Historical lint debt may be excluded only by exact file-level rules, with a
  short reason and a follow-up OpenSpec task. New or low-risk rules should be
  blocking.
- Report a slow or interrupted race run as interrupted; never present it as a
  passing verification.
- Integration evidence belongs under
  `temp/integration-test-runs/<run-id>/` and must redact secrets, tokens,
  provider payloads, private tool arguments, and full model reasoning.

## Recommended loop

From `cli/auctra` run the narrowest relevant checks first:

```bash
task fmt-check
task lint
task test
task vet
task security
task ci
task test:integration
task release:verify
```

Use `task ci` as the reproducible local quality gate. Use `task check` when a
broader developer gate is required, and use `task release:verify` before a tag
or release workflow review. Validate the owning OpenSpec change with:

```bash
openspec validate auctra-code-quality-cicd-v1 --strict --no-interactive
```

## CI/CD review checklist

- Go, golangci-lint, govulncheck, GoReleaser, and Syft versions are explicit.
- CI jobs have bounded timeouts and cancel stale pull-request runs.
- Release publishing is tag-only and manual snapshot builds do not publish.
- Release smoke tests remain non-interactive: `--version`, `--help`, and
  `runtime doctor --json`.
- The final report names passed, failed, skipped, and interrupted gates plus
  the evidence directory for integration tests.
