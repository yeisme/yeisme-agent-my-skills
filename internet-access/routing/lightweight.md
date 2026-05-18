# Lightweight 路线

## 目的

用一个聚焦的本地 CLI 查询快速回答简单网页问题。优先直接运行命令，不使用本地辅助脚本。

## 什么时候使用

- 用户询问定义、URL、发布日期、负责人、版本号、简短解释或单个事实。
- 一到三个来源足够。
- 用户更重视速度而不是深度。
- 不需要交互或登录。

## 本地 CLI 工作流

1. 判断目标来源是否已知。
2. 来源未知时，把查询优化成核心关键词并使用 `firecrawl search`：

```bash
firecrawl search "GitHub" --limit 5
firecrawl search "REST API definition" --limit 3
```

3. 来源已知时，优先使用来源专用 CLI：

```bash
gh repo view firecrawl/firecrawl --json name,description,stargazerCount,url
npm view firecrawl-mcp version description repository --json
python -m pip index versions requests
```

`gh` 只在目标是 GitHub 时使用；不要为了普通网页搜索先调用 `gh`。

4. 如果答案位于已知 URL，直接抓取：

```bash
firecrawl scrape "https://github.com/firecrawl/firecrawl"
```

5. 如果本地 CLI 缺失，降级到内置搜索/浏览器工具或 `curl`。

6. 如果用户只要“当前版本/状态/URL”，不要升级浏览器。

除非第一批结果不清楚，或主题本身高度不稳定，否则不要为简单事实查询运行多角度调研。

## 输出格式

```markdown
**答案**：[1-2 句话直接回答]

**来源**：[URL 或命令结果对应来源]
```

只有当要点确实提升清晰度时，才添加最多三个 bullet。

## 质量标准

- 引用来源 URL。
- 用户询问事实时，避免泛泛总结。
- 对可能变化的信息使用当前搜索。
- 如果结果冲突或来源质量弱，升级到 `standard.md`。
