---
name: creative-writing-installer
description: Use when installing or enabling the correct creative-writing skill set for cli/auctra through skillctl when a Chinese creative task requires skills not present in the current runtime.
---

# 中文创作技能安装器

通过 `skillctl` 启用创作技能；不要手工编辑生成出来的运行时副本。

## 输入

- 路由器推荐的缺失技能、目标子项目、agent home、用户授权状态。
- 当前 profile、set ID、dry-run 结果和预期写作任务。

## 输出

- dry-run 安装/启用计划。
- 用户批准后执行的真实 `skillctl` 命令。
- 安装后重新 route 或 validate 的结果。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../wechat-article-writer/references/platform-nonfiction-playbook.md`：需要公众号、书评、产品评测、教程、周报或旅行攻略结构模板时读取。

## 工作流

1. 根据路由器或 route 结果识别缺失技能。
2. 优先选择最小 set，例如 `creative-writing-xhs` 或 `creative-writing-chinese-novel`。
3. 先运行 dry-run，展示将启用哪些技能。
4. 只有在用户明确同意或流程已批准时执行 `--yes`。
5. 安装后重新运行路由或校验。

## 质量门槛

- 不为一个写作任务安装无关技能组。
- 不手写 `.agents/skills/**` 或 `.claude/skills/**`。
- 命令必须是真实用户可运行命令。

## Auctra 轻集成

- 常用命令：`skillctl sets apply creative-writing-core --target cli/auctra --agent-home claude --dry-run`。
- 启用中文小说套件：`skillctl sets apply creative-writing-chinese-novel --target cli/auctra --agent-home claude --yes`。
- 启用单个技能：`skillctl manage skills enable chinese-novel-orchestrator --target cli/auctra --agent-home claude --yes`。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 执行前确认 dry-run 输出与用户目标一致。
- 执行后运行 `skillctl sets show creative-writing-chinese-novel --json` 或对应 set show。
- 安装器只报告安装结果，不声称稿件已完成。
