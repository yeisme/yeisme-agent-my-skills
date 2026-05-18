# 本地研究基础设施

## 目的

说明在 Yeisme、Hermes、OpenWebUI、MCP Gateway 等本地部署环境中，如何把通用互联网信息获取路线落到已经配置好的本地服务和 CLI。这个文件只处理本地研究基础设施选择，不替代 `source_priority.md`、`deep_research.md` 或 `browser_tools.md`。

## 适用场景

使用本路线：

- 用户明确提到 Hermes、OpenWebUI、Open WebUI、Research Harness、MCP Gateway、SearXNG、Firecrawl 后端或本机服务。
- 当前任务是在本仓库内设计、调试、审查或使用 OpenWebUI Hermes 的联网研究能力。
- agent 需要决定是在宿主 shell 里用 CLI 搜索，还是在 OpenWebUI/Hermes 内使用已配置的工具。
- 搜索质量问题和本地服务配置有关，例如结果太少、query 生成太宽、Firecrawl loader 没生效。

不要把本路线当成全局默认规则。普通互联网信息获取仍按来源优先级选择 `firecrawl`、`gh`、包管理器、`curl`/`jq` 或浏览器工具。

## 本仓库策略

在 Yeisme/Hermes/OpenWebUI 语境里：

- 不使用、不排障 BigModel/Zai `web-search-prime` 作为默认联网搜索后端；该能力在 MCP Gateway 侧按策略保持 disabled。
- 宿主 agent 做搜索、抓取和大样本研究时，优先使用本地 `firecrawl` CLI，并连接 `backend-server/firecrawl` 已配置后端。
- OpenWebUI 内置 Web Search 走 SearXNG，Web Loader 走 Firecrawl。
- OpenWebUI Research Harness 负责研究任务规划、query buckets、证据 trace、source diversity gate 和答案质量检查；它不是通用网页搜索 CLI 的替代品。
- `gh` 仍只用于 GitHub 结构化来源，不因为任务在 Hermes/OpenWebUI 中就升级成通用搜索工具。

## 宿主 shell 路线

agent 在宿主 shell 内执行研究任务时，优先直接用本地 CLI：

```bash
firecrawl view-config
firecrawl search "Open WebUI web_search_queries_generated query prompt" --limit 5 --json
firecrawl search "Open WebUI web_search_queries_generated query prompt" --api-url http://localhost:32741 --limit 5 --json
firecrawl scrape "https://docs.openwebui.com/" --api-url http://localhost:32741
```

使用规则：

- 先用 `firecrawl view-config` 判断当前 CLI 是否已经指向本地 Firecrawl 后端。
- 如果当前配置没有指向本地后端，再显式传 `--api-url`。
- 本仓库默认 Firecrawl API 端口记录在 `docs/service-ports.md`，常见宿主入口是 `32741`；SearXNG 搜索入口常见端口是 `32742`。
- 对复杂研究，把结果写入 `.firecrawl/`，再用 `jq`、`rg`、`head` 等增量读取，避免把全部输出塞进上下文。

示例：

```bash
mkdir -p .firecrawl
firecrawl search "Hermes Agent Open WebUI Research Harness" --limit 10 --json -o .firecrawl/hermes-research.json
jq -r '.data.web[]? | [.title, .url] | @tsv' .firecrawl/hermes-research.json
```

## OpenWebUI/Hermes 路线

当任务发生在 OpenWebUI/Hermes 内部时，优先利用已经注入的 OpenWebUI 配置：

| 能力 | 默认本地组件 | 作用 |
| --- | --- | --- |
| Web Search | SearXNG | 返回候选搜索结果。 |
| Web Loader | Firecrawl | 加载网页正文。 |
| Research Harness | OpenWebUI Tool | 规划 research profile、生成 query buckets、记录 trace、做质量检查。 |
| Agent CLI Tool | OpenWebUI Tool | 在容器内调用白名单 agent CLI。 |

OpenWebUI 容器内通常通过 `host.docker.internal` 访问宿主服务：

```text
http://host.docker.internal:32742/search
http://host.docker.internal:32741
```

在宿主机直接访问时，应以 `docs/service-ports.md` 和当前 `.env` 为准，不把 token、API key 或真实密钥写进回答。

## Research Harness 选择

OpenWebUI Hermes 的 Research Harness 当前适合这些任务：

- `daily_news_digest`：今日热点、综合新闻、多来源摘要。
- `technical_research`：技术调研、错误排查、版本行为，保留精确术语并优先一手来源。
- `fact_check`：事实核查、传言辨析、单一来源不足判断。

如果 agent 在 OpenWebUI/Hermes 上下文中能调用 Research Harness，应优先让它做规划和 trace，再让底层搜索服务收集 evidence。关键输出应包含：

- profile。
- query buckets。
- raw/deduped/selected counts。
- dropped reasons。
- coverage limits。
- trace path。
- quality grade。

如果用户要求 100/200/300 个样本，Research Harness 可能只适合作为第一轮规划器；大样本去重、分类和完整台账仍按 `deep_research.md` 与 `evidence_ledger.md` 执行。若本地工具或 OpenWebUI 阀值限制了预算，必须报告被 clamp 的参数和需要追加的批次。

## 查询生成约束

本仓库 OpenWebUI 查询生成 prompt 的原则也适用于 agent 直接搜索：

- 第一条 query 保留用户的精确目标、产品名、命令、flag、文件名、错误文本、URL、版本和日期。
- 不要把精确技术问题改写成宽泛类别。
- 用户没有要求最新/当前/新闻时，不要机械加年份。
- 中文问题里的英文产品名、API 名、repo 名和错误文本保持英文。
- follow-up 问题要从附近上下文恢复精确主题，但 query 保持短。

技术调研示例：

```bash
firecrawl search "Open WebUI web_search_queries_generated query prompt" --limit 8
firecrawl search "Open WebUI web_search_queries_generated query prompt official docs" --limit 8
firecrawl search "\"Open WebUI web_search_queries_generated query prompt\"" --limit 8
```

## 排障路线

当 Hermes/OpenWebUI 搜索质量差时，按顺序排查：

1. 宿主 Firecrawl CLI 是否可用：

```bash
firecrawl view-config
firecrawl search "openwebui" --limit 3 --json
```

2. 本地服务端口是否与文档一致：

```bash
ss -lntp | rg ':(32741|32742|7457|8000|8642)\b'
```

3. OpenWebUI 子项目健康检查是否通过：

```bash
cd /home/yeshugen/workplace/yeisme-agent/backend-server/openwebui-hermes
task health
task webui-config-status
```

4. Research Harness 是否报告 `search_scarcity`、`domain_scarcity` 或预算 clamp。
5. 如果是技术问题，确认 query 是否保留了原始命令、错误文本和版本，而不是被泛化。

## 参考位置

本路线来自这些本仓库材料：

- `docs/skills/skill-trigger-guide.md`
- `docs/service-ports.md`
- `my-skills/yeisme-mcp-gateway-operator/SKILL.md`
- `my-skills/yeisme-mcp-gateway-maintainer/SKILL.md`
- `my-skills/yeisme-mcp-registry-onboarding/SKILL.md`
- `backend-server/openwebui-hermes/AGENTS.md`
- `backend-server/openwebui-hermes/README.md`
- `backend-server/openwebui-hermes/scripts/openwebui_hermes/prompts/search_query_generation.md`
- `backend-server/openwebui-hermes/scripts/openwebui_hermes/research_harness.py`
- `backend-server/openwebui-hermes/openspec/specs/research-harness/spec.md`
