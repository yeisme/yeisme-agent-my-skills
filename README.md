# Yeisme Agent Skills

Yeisme 开源 Skills 聚合仓库。它提供跨项目 Skill 的发现入口，并通过 Git submodule 挂载具备独立产品边界、发布节奏和维护责任的 Skills 仓库。

## 获取

```bash
git clone --recurse-submodules https://github.com/yeisme/yeisme-agent-my-skills.git
cd yeisme-agent-my-skills
python3 scripts/validate_repository.py
```

已克隆但尚未初始化子模块时：

```bash
git submodule update --init --recursive
```

## 管理任意外部项目

本仓库提供可移植的 `scripts/skills.sh`。它把本 checkout 作为 Skill source，但允许 `--project` 指向任意项目或服务器工作目录。

首次接入：

```bash
git clone --recurse-submodules https://github.com/yeisme/yeisme-agent-my-skills.git
cd yeisme-agent-my-skills
scripts/skills.sh --project /path/to/project init
```

`init` 会：

- 通过 CLI 生成项目 `.skills/source.local` 与 `.skills/profiles/root.txt`；
- 激活 `yeisme-skill-routing-governance` 管理 Skill；
- 生成项目 `.agents/skills` 与 `.claude/skills`；
- 验证 profile、managed manifest 和双 runtime。

搜索并添加复杂 Skill：

```bash
scripts/skills.sh --project /path/to/project search "task terms"
scripts/skills.sh --project /path/to/project resolve <skill-name>
scripts/skills.sh --project /path/to/project --dry-run profile add <skill-name>
scripts/skills.sh --project /path/to/project profile add <skill-name>
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

Agent 应先阅读候选 `SKILL.md`，默认选择一个 primary workflow、至多一个兼容 domain constraint，并把独立 audit 与实现职责分开。搜索结果不是自动安装批准。

服务器上的 source checkout 路径是本地状态。checkout 移动后重新绑定：

```bash
cd yeisme-agent-my-skills
scripts/skills.sh --project /path/to/project configure-source
scripts/skills.sh --project /path/to/project doctor
```

更新公共 Skills 后重新同步：

```bash
cd yeisme-agent-my-skills
git pull --ff-only
git submodule update --init --recursive
scripts/skills.sh --project /path/to/project sync
scripts/skills.sh --project /path/to/project validate
```

机器读取可使用：

```bash
scripts/skills.sh --project /path/to/project status --agent
scripts/skills.sh --project /path/to/project list-source --json
```

默认输出用于人类；`--agent` 输出稳定 `key=value`；`--json` 输出单个版本化 envelope。不要提交 `.skills/source.local`，它会在 Git 项目中自动加入本地 `.git/info/exclude`。

## 独立项目

| 路径 | 独立仓库 | 定位 |
| --- | --- | --- |
| [`ai-drama/`](ai-drama/README.md) | [ai-drama-skills](https://github.com/yeisme/ai-drama-skills) | AI 做剧路由、编剧、导演、连续性、评审和生产交接 |
| [`auctra-novel/`](auctra-novel/README.md) | [auctra-novel-skills](https://github.com/yeisme/auctra-novel-skills) | Auctra 与中文长篇小说创作矩阵 |
| [`agent-workflow/`](agent-workflow/README.md) | [agent-workflow-skills](https://github.com/yeisme/agent-workflow-skills) | 通用 Agent runtime、仓库路由和 Skill 治理 |
| [`ordo/`](ordo/README.md) | [ordo-skills](https://github.com/yeisme/ordo-skills) | Ordo DAG、worktree 和 runtime canary |
| [`scaena/`](scaena/README.md) | [scaena-skills](https://github.com/yeisme/scaena-skills) | Scaena 生产、主体资产门禁和视频转绘 |

独立项目保留原 Skill 名称，宿主 profile 按名称解析，因此拆仓不要求调用方重命名 Skill。

## 聚合模块

| 模块 | 说明 |
| --- | --- |
| [`architecture/`](architecture/README.md) | Aigora/Seedance 架构与下一代路由设计 |
| [`audio-workflow/`](audio-workflow/README.md) | Sonora 音频 Agent 路由 |
| [`cli-runtime/`](cli-runtime/README.md) | 待按产品 Owner 继续拆分的 CLI runtime 适配层 |
| [`content-writing/`](content-writing/README.md) | 教程、游记、评测、周报和公众号内容 |
| [`creative-writing-core/`](creative-writing-core/README.md) | 创作路由、风格 Lens、安装和渐进编排 |
| [`eikona-image/`](eikona-image/README.md) | Eikona 图片生成、资产、主体与社媒视觉 |
| [`engineering/`](engineering/README.md) | 工程、CLI、后端、语言和演进约束 |
| [`frontend-design/`](frontend-design/README.md) | Web/TUI 设计、动效、前端质量与视觉验收 |
| [`game-development/`](game-development/README.md) | LLM 原生游戏方向、系统架构和垂直切片 |
| [`knowledge/`](knowledge/README.md) | 企业多模态知识路由 |
| [`mcp/`](mcp/README.md) | MCP 构建、Gateway 运维与注册治理 |
| [`pinax-agent/`](pinax-agent/README.md) | Pinax 笔记、检索、记忆、项目和发布工作流 |
| [`project-development/`](project-development/README.md) | 项目路由、规格驱动和垂直切片交付 |
| [`qa-release/`](qa-release/README.md) | 性能与集成测试证据 |
| [`role-intelligence/`](role-intelligence/README.md) | 角色蓝图和跨项目角色路由 |
| [`scriptwriting/`](scriptwriting/README.md) | 短视频、直播、播客和场景剧本写作 |
| [`social-content/`](social-content/README.md) | 小红书与社媒内容生产矩阵 |
| [`video-analysis/`](video-analysis/README.md) | Anatomia 视频分析、分镜审阅和资产交接 |
| [`web-research/`](web-research/README.md) | 互联网研究和来源验证 |

后续拆分顺序、Owner 边界和兼容策略见 [`docs/repository-split-roadmap.md`](docs/repository-split-roadmap.md)。

## Skill 目录契约

```text
<module-or-project>/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/   # 可选
  scripts/      # 可选
  assets/       # 可选
```

- 每个 Skill 目录只保留一个 Agent 入口 `SKILL.md`，不添加重复 README 或快速参考文件。
- 项目或模块说明放在其根目录 `README.md`。
- `name` 必须与 Skill 目录名一致，`description` 应明确触发条件和边界。
- 结构化状态、资产、凭据、provider payload 和项目正典不进入 Skills 仓库。
- 独立仓库不得依赖维护者机器绝对路径；宿主专用命令必须明确标为适配层。

## 验证

```bash
python3 scripts/validate_repository.py
scripts/skills.sh --help
python3 agent-workflow/scripts/test_skill_manager.py
python3 ai-drama/scripts/validate_skills.py
python3 ai-drama/ai-drama-router/scripts/validate_drama_matrix.py
python3 auctra-novel/scripts/validate_skills.py
python3 agent-workflow/scripts/validate_skills.py
python3 ordo/scripts/validate_skills.py
python3 scaena/scripts/validate_skills.py
```

## License

聚合仓库采用 [MIT License](LICENSE)。每个独立子仓库也包含自己的许可证；产品源码仓库的可见性和许可证以对应仓库为准。
