# Project Skills

`.skills/yeisme/` 是本仓库自建、可发布、可同步的 skill 源码目录。这里的 skill 面向 agent 执行，不是普通项目文档，也不是 MCP、CLI、agent runtime 或 gateway 的实现代码。

## 目录合同

- `.skills/yeisme/`：项目自建 skill 的发布源。
- `.skills/imported/`：skills.sh、gstack、clawhub 等来源的三方 skill 本地目录。
- `.skills/profiles/root.txt`：根目录会话的 skill profile。
- `.skills/profiles/targets/<subproject>.txt`：子项目会话的 skill profile。
- `.agents/skills/`：本仓库 agent 本地运行副本，由 `scripts/skills.sh sync-root` 按根 profile 生成。
- `.claude/skills/`：Claude Code 本地运行副本，由同一套 `scripts/skills.sh` 命令从根 `.agents/skills` 镜像生成。
- `.codex/skills/`：不用于本仓库自建 skill。
- `docs/skills/`：skill 编写规范、索引和分层说明。
- `mcp/`：MCP server、tool、transport、schema、adapter 和调试入口。

不要把 MCP 实现放进 `.skills/yeisme/`。skill 可以说明如何创建或审查 MCP，但实际 MCP 代码必须放到 `mcp/`。
不要把从 skills.sh、gstack、clawhub 或其它来源安装的外部 skill 放进 `.skills/yeisme/`；三方或导入型 skill 放 `.skills/imported/`，分配关系放 profile，运行副本放 `.agents/skills/` 和 `.claude/skills/`。

## 自建 Skill 形状

Yeisme 自建 skill 必须使用以下结构：

```text
.skills/yeisme/<module>/<skill-name>/
  SKILL.md
  agents/openai.yaml
```

可选目录只在直接有用时创建：

- `scripts/`：稳定、重复、需要确定性的辅助脚本。
- `references/`：详细材料，只在需要时加载。
- `assets/`：会被复制或用于生成输出的模板、图片、字体或样例文件。

不要在单个 skill 目录里创建额外 `README.md`、`CHANGELOG.md`、`QUICK_REFERENCE.md`。`SKILL.md` 就是 agent-facing 合同。

## `SKILL.md` 要求

Frontmatter 必须包含：

```yaml
---
name: skill-name
description: Use when ...
---
```

要求：

- `name` 必须和目录名一致。
- `description` 必须说明触发条件、任务对象和范围。
- `description` 推荐以 `Use when ...` 开头。
- `description` 不能是泛泛介绍，例如 “Helpful skill for developers”。
- 正文必须说明使用场景、输入、输出、工作流、边界和验证方式。
- 正文保持精简；详细背景放 `references/`。
- 命令示例必须写用户可直接运行的真实命令；不要把本地执行包装器、shell alias 或 agent-only 前缀写进 skill 正文、文档或最终答复。

## `agents/openai.yaml` 要求

必须包含：

```yaml
display_name: Human Friendly Name
short_description: One-sentence visible summary.
default_prompt: A concrete starting prompt for this skill.
```

要求：

- `display_name` 是人类可读名称。
- `short_description` 和 `SKILL.md description` 范围一致。
- `default_prompt` 是可直接执行的起始任务。
- 修改 `SKILL.md` 触发范围后必须同步检查 `agents/openai.yaml`。

## 重复 Skill 防线

项目自建 skill 只允许一个源码和按 profile 生成的运行副本：

```text
.skills/yeisme/<module>/<skill-name>/       自研发布源
.agents/skills/<skill-name>/  根 profile 运行副本
.claude/skills/<skill-name>/  Claude Code 根 profile 运行副本
<subproject>/.agents/skills/<skill-name>/  子项目 profile 运行副本
```

不要创建或维护：

```text
.codex/skills/<skill-name>/
```

排查重复：

```bash
find .codex/skills -maxdepth 2 -name SKILL.md 2>/dev/null | sort
find .skills/yeisme -maxdepth 2 -mindepth 2 -type l -print
```

如果 Codex/Agent 中出现重复自研 skill，只保留 `.skills/yeisme/<module>/<skill-name>/` 发布源，并通过 profile 决定是否生成根或子项目运行副本。不要把外部安装包、symlink 或运行副本放进 `.skills/yeisme/`。

## 当前自建 Skills

- `yeisme-skill-publisher`：创建、校验、同步和发布 `.skills/yeisme/` 下的自建 skill。
- `ai-native-cli-output-contract`：统一多应用 CLI 的默认摘要、`--agent`、`--json`、`--events`、`--explain`、envelope、脱敏和契约测试要求。
- `yeisme-mcp-builder`：创建、组织、审查和记录 `mcp/` 下的自建 MCP 能力。
- `yeisme-mcp-gateway-operator`：通过 `mcp-gateway` CLI、Web UI、TUI、API 和 `/mcp` endpoint 操作已部署的 MCP Gateway。
- `yeisme-mcp-gateway-maintainer`：维护 `mcp/gateway` 的 TypeScript 网关、CLI 渲染、健康检查、路由、审计和测试。
- `yeisme-mcp-registry-onboarding`：新增或审查 `mcp/registry.json` 中的 MCP 后端、凭证、客户端渲染、网关暴露和权限策略。
- `yeisme-apigateway-auth-sync`：维护 `apigateway` 中 Codex、Gemini CLI 认证同步 sidecar 和 new-api 渠道行为。
- `yeisme-cohors-cli-runtime`：开发 `cli/cohors` 的 workflow、daemon、Team Room、trace、CLI/TUI 输出风格、eval 和 Generic CLI Runtime。
- `yeisme-eikona-cli-runtime`：开发 `cli/eikona` 的生图、参考图编辑、provider adapter、run evidence、项目库、Web UI 和 release 行为。
- `yeisme-taskbridge-cli-runtime`：开发 `cli/taskbridge` 的任务控制面、provider 同步、action file、Agent JSON 合同和 Go CLI 行为。
- `performance-profiler`：为项目软件建立性能基线、定位瓶颈，并用重复测量产出优化前后证据。
- `ui-spec-frontend-workflow`：把 PRD、线框图、截图或高保真 UI 图转成 React UI Spec、组件树、前端实现、动画约束和截图回归闭环。
- `yeisme-frontend-quality-workflow`：维护 Storybook、Tailwind stories、Chromatic、addon-designs、Lighthouse、Axe、Playwright 和 browser-use 前端质量门禁。
- `backend-system-workflow`：设计、实现或审查后端 API、worker、状态机、持久化、并发、权限、可观测性、迁移、测试和性能门禁。
- `codegraph-cli-code-intelligence`：通过 CodeGraph CLI 索引代码、查询上下文、做调用关系和改动影响分析，先缩小实现边界再修改代码。
- `yeisme-repo-routing`：判断新文件、workflow、skill、MCP、CLI、agent、gateway 和文档应该落在哪一层。
- `yeisme-claude-skills-layout`：为 Yeisme 项目设计、迁移或审查由 `skillctl` 管理的 `.claude/skills` 与 `.agents/skills` 双 active runtime。
- `yeisme-git-worktree-flow`：使用 Git flow、`git worktree`、`Taskfile` 和 `nerdctl compose.yml` 进行开发。
- `yeisme-coding-execution-driver`：把代码实现任务转成实时 checklist、持续执行循环、验证检查点和明确停止条件，避免 agent 编程中途无谓停下。
- `golang-cobra-viper-cli-architecture`：为 Yeisme Go CLI 默认使用 Cobra/Viper、命令/配置/输出边界和公共模块提取提供架构约束。
- `golang-github-release-guardrails`：为 Go 项目强制 GitHub Actions、golangci-lint 和 GoReleaser 发布护栏。
- `internet-access`：指导 agent 优先使用本地 CLI 从互联网获取、核验、提取信息，并在需要交互时升级到 agent-browser、Playwright 或 browser-use。
- `tui-design-standards`：审查或实现 TUI 时强制鼠标响应，并保持圆滑、克制、Apple-like 的终端界面质感。

## 验证与同步

每次新增或修改自建 skill 后运行：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
scripts/skills.sh sync-root
scripts/skills.sh sync-subprojects
scripts/skills.sh list-custom
```

从远程仓库安装自建 skill：

```bash
scripts/skills.sh install-custom <repo-url> [ref]
```

更详细的编写规范见 [docs/skills/skills-authoring.md](../../docs/skills/skills-authoring.md)。
