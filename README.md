# Project Skills

`my-skills/` 是本仓库自建、可发布、可同步的 skill 源码目录。这里的 skill 面向 agent 执行，不是普通项目文档，也不是 MCP、CLI、agent runtime 或 gateway 的实现代码。

## 目录合同

- `my-skills/`：项目自建 skill 的发布源。
- `skills/`：skills.sh、gstack、clawhub 等来源的三方 skill 本地目录。
- `.agents/skills/`：本仓库 agent 本地运行副本，由 `scripts/skills.sh sync-all`、`sync-custom` 或 `sync-third-party` 生成。
- `.claude/skills/`：Claude Code 本地运行副本，由同一套 `scripts/skills.sh` 命令从 `.agents/skills` 镜像生成。
- `.codex/skills/`：不用于本仓库自建 skill。
- `docs/skills/`：skill 编写规范、索引和分层说明。
- `mcp/`：MCP server、tool、transport、schema、adapter 和调试入口。

不要把 MCP 实现放进 `my-skills/`。skill 可以说明如何创建或审查 MCP，但实际 MCP 代码必须放到 `mcp/`。
不要把从 skills.sh、gstack、clawhub 或其它来源安装的外部 skill 放进 `my-skills/`；三方 skill 放 `skills/`，运行副本放 `.agents/skills/` 和 `.claude/skills/`。

## 自建 Skill 形状

Yeisme 自建 skill 必须使用以下结构：

```text
my-skills/<skill-name>/
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

项目自建 skill 只允许一个源码和一个本地运行副本：

```text
my-skills/<skill-name>/       自研发布源
.agents/skills/<skill-name>/  本地运行副本
.claude/skills/<skill-name>/  Claude Code 运行副本
```

不要创建或维护：

```text
.codex/skills/<skill-name>/
```

排查重复：

```bash
find .codex/skills -maxdepth 2 -name SKILL.md 2>/dev/null | sort
find my-skills -maxdepth 1 -mindepth 1 -type l -print
```

如果 Codex/Agent 中出现重复自研 skill，只保留 `my-skills/<skill-name>/` 发布源、`.agents/skills/<skill-name>/` 运行副本和 `.claude/skills/<skill-name>/` 运行副本。不要把外部安装包、symlink 或运行副本放进 `my-skills/`。

## 当前自建 Skills

- `yeisme-skill-publisher`：创建、校验、同步和发布 `my-skills/` 下的自建 skill。
- `yeisme-mcp-builder`：创建、组织、审查和记录 `mcp/` 下的自建 MCP 能力。
- `yeisme-mcp-gateway-maintainer`：维护 `mcp/gateway` 的 TypeScript 网关、CLI 渲染、健康检查、路由、审计和测试。
- `yeisme-mcp-registry-onboarding`：新增或审查 `mcp/registry.json` 中的 MCP 后端、凭证、客户端渲染、网关暴露和权限策略。
- `yeisme-apigateway-auth-sync`：维护 `apigateway` 中 Codex、Gemini CLI、OpenCode 认证同步 sidecar 和 new-api 渠道行为。
- `yeisme-opsroom-cli-runtime`：开发 `cli/opsroom` 的 workflow、daemon、Team Room、trace、TUI、eval 和 Generic CLI Runtime。
- `yeisme-repo-routing`：判断新文件、workflow、skill、MCP、CLI、agent、gateway 和文档应该落在哪一层。
- `yeisme-git-worktree-flow`：使用 Git flow、`git worktree`、`Taskfile` 和 `nerdctl compose.yml` 进行开发。
- `yeisme-coding-execution-driver`：把代码实现任务转成实时 checklist、持续执行循环、验证检查点和明确停止条件，避免 agent 编程中途无谓停下。
- `golang-github-release-guardrails`：为 Go 项目强制 GitHub Actions、golangci-lint 和 GoReleaser 发布护栏。
- `tui-design-standards`：审查或实现 TUI 时强制鼠标响应，并保持圆滑、克制、Apple-like 的终端界面质感。

## 验证与同步

每次新增或修改自建 skill 后运行：

```bash
scripts/skills.sh validate-custom
scripts/skills.sh sync-custom
scripts/skills.sh list-custom
```

从远程仓库安装自建 skill：

```bash
scripts/skills.sh install-custom <repo-url> [ref]
```

更详细的编写规范见 [docs/skills/skills-authoring.md](/home/yeshugen/workplace/yeisme-agent/docs/skills/skills-authoring.md)。
