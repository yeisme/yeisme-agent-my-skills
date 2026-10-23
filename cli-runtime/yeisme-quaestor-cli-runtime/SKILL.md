---
name: yeisme-quaestor-cli-runtime
description: Use when changing, testing, reviewing, documenting, designing, or operating the Quaestor research product runtime under cli/quaestor, including product workflows, evidence ledgers, quantitative validation, CLI behavior, app-service/API/client contracts, adapters, redaction, and Go validation.
---

# Yeisme Quaestor CLI Runtime

Use this skill for `cli/quaestor`, the Yeisme research product engine whose current operator surface is the CLI and whose future services or approved clients must consume the same evidence and application-service contracts.

## Boundary

- Quaestor owns its local CLI workflows, query/research orchestration, output rendering, and evidence boundaries.
- Product PRDs, research workflow design, API projections, and approved client contract gaps are in scope; independent frontend implementation requires its own approved client owner.
- Internet access, crawling, and provider calls must stay behind explicit adapters and redact credentials, raw prompts, provider payloads, private tool arguments, and full chain-of-thought.
- Do not move Quaestor behavior into Connectors; skill profiles may select it or invoke it through stable command/API surfaces.

## Workflow

1. Enter `cli/quaestor` before concrete implementation.
2. Read local `AGENTS.md` and use Quaestor OpenSpec changes for behavior changes.
3. Preserve CLI output contracts for human summaries, `--json`, `--agent`, stderr diagnostics, and redaction.
4. Reuse existing local test and fixture patterns before adding new test systems.

## If this fails

| Trigger | First fix | Still failing |
| --- | --- | --- |
| Implementation request | Enter `cli/quaestor`; read local `AGENTS.md` | Do not implement from root |
| Internet, crawl, or provider call | Keep it behind an explicit adapter | Redact credentials, raw prompts, payloads, and chain-of-thought |
| Independent frontend requested | Needs its own approved client owner | Do not put frontend implementation in this CLI |
| Move Quaestor behavior into Connectors | Stop | Invoke only through stable command or API surfaces |

## Validation

```bash
cd cli/quaestor
gofmt -w ./cmd ./internal ./tests
go test ./...
go build -trimpath ./cmd/quaestor
```


## 资源命令与版本合同

先读取安装版的 help/结构化发现面，确认 canonical 路径存在。运行 `quaestor thesis list --agent`，从 `fact.thesis.N.id` 取真实 ID，再调用 `quaestor thesis describe <id> --agent`；`<id>` 是待替换的语法说明，不作为可直接执行的 Next。保持原项目、配置、过滤与权限范围。解析失败报告合同或版本问题，可查 `--json`，不要解析人读表或猜 ID。

详情类旧 show 只作隐藏兼容；正常操作使用 describe，独立 inspect/export/download 等动作保持原义。补全是同一目录的只读视图；需要安装时显式运行 completion install，并用 completion doctor 区分文件存在与 shell 可发现。源码候选通过不代表 PATH 安装版已更新。
