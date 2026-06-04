---
name: codegraph-cli-code-intelligence
description: Use when inspecting, planning, debugging, refactoring, reviewing, or impact-checking code with the CodeGraph CLI before editing implementation files.
---

# CodeGraph CLI Code Intelligence

## 使用场景

当任务需要理解代码结构、调用关系或改动影响时使用本 skill，尤其是：

- 在大型子项目中定位函数、类型、模块和调用链。
- 实现或重构前，需要先判断哪些文件会被影响。
- bugfix 或 review 需要确认调用方、依赖方、dead code 或风险入口。
- 合并前需要跑结构化 impact check，而不只依赖全文搜索。
- agent 准备改代码，但当前上下文不足以可靠判断边界。

这个 skill 默认使用本地 CLI `codegraph`。优先 CLI + skills；不要因为一次代码结构查询就新增 MCP server 或 Gateway 路由。

## 工具基线

默认工具是 Optave CodeGraph 的 CLI：

```bash
npm install -g @optave/codegraph
codegraph --help
```

如果项目不能全局安装，用临时执行方式：

```bash
npx @optave/codegraph --help
```

如果本机存在其它同名工具，先确认 `codegraph --help` 输出包含 build、search、context、impact、diff-impact 或 check 这类代码图能力；不匹配时不要把命令结果当成 CodeGraph 证据。

## 工作流

1. 进入拥有代码的子项目目录，先读本地 `AGENTS.md` 和任务相关文档。
2. 检查 CLI 是否可用：

```bash
codegraph --help
```

3. 对当前项目建立或刷新索引。以 CLI help 中显示的命令为准，常见形态是：

```bash
codegraph build
```

4. 用全文搜索和 CodeGraph 查询组合定位边界：

```bash
rg -n "<symbol-or-error>" .
codegraph search "<symbol-or-error>"
codegraph context "<file-or-symbol>"
```

5. 在改代码前做影响分析：

```bash
codegraph impact "<symbol-or-file>"
```

6. 如果已有 git diff，在 review、重构或合并前检查 diff 影响：

```bash
codegraph diff-impact
codegraph check
```

7. 把 CodeGraph 输出转成具体工程结论：
   - 入口和调用方是什么。
   - 哪些文件必须改，哪些文件不应碰。
   - 哪些 tests 或 contract 需要更新。
   - 是否存在循环依赖、未使用代码或跨模块边界风险。

8. 再按子项目执行 skill 继续：实现任务用 `yeisme-coding-execution-driver`，行为变更用 `test-driven-development`，失败排查用 `systematic-debugging`，完成前用 `verification-before-completion`。

## 输出要求

使用本 skill 后，给用户或计划中的结论要包含：

- CodeGraph 使用的项目目录。
- 实际运行过的查询类别，例如 build、search、context、impact、diff-impact 或 check。
- 结构性发现：关键 symbol、调用链、影响文件和风险点。
- 由这些发现推导出的改动范围和验证命令。

不要把大段 CLI 原始输出贴进最终答复；只保留工程结论和必要的命令。

## 边界

- CodeGraph 是辅助判断，不替代 `rg`、语言服务器、编译器、测试和 reviewer。
- CLI help 和项目版本优先于本 skill 中的示例命令；如果命令名不同，按本机 CLI 实际输出调整。
- 不在根目录对所有子项目做全仓索引；进入具体 owner 子项目后再索引。
- 不把 CodeGraph 结果当作安全审计结论；安全任务仍用 `cso` 或对应安全流程。
- 不把索引缓存、报告缓存或生成数据库提交进 git。

## 验证

最小验证：

```bash
codegraph --help
codegraph build
codegraph check
```

结合子项目本地门禁继续运行对应测试，例如：

```bash
go test ./...
```

如果 CodeGraph 不支持当前语言或项目结构，明确说明降级为 `rg`、编译器、测试和人工调用链检查。
