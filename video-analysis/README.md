# Video Analysis Skills

Anatomia 用户产品 Skills。安装源是公开的 Yeisme Skills 仓库，不是私有 `yeisme/anatomia` 代码仓。`anatomia` binary 来自公开可见的 GitHub Release，不从本 Skills 仓安装。后续独立发布仓名为 `anatomia-skills`；在拆仓完成前，用户一律从本模块安装 Skills。

一句话：

```bash
npx skills add yeisme/yeisme-agent-my-skills \
  --skill \
    anatomia-video-analysis-router \
    anatomia-video-evidence-navigator \
    anatomia-storyboard-reviewer \
    anatomia-asset-handoff-builder \
    anatomia-scaena-learning-loop \
  --agent codex --copy --full-depth -g -y
anatomia login --endpoint https://anatomia.example.com --key-file /absolute/private/anatomia-access.key
anatomia analyze file --file /absolute/path/demo.mp4 --to ./anatomia-output/demo --json
```

不要 `--all`。本仓库还包含其他产品模块。Skills 不安装 `anatomia` binary，也不携带 service key 或 provider key。

| Skill | 一句话 |
| --- | --- |
| `anatomia-video-analysis-router` | 登录并分析一个已授权本地视频；不列 Provider/模型 catalog |
| `anatomia-video-evidence-navigator` | 对已登记 ref 问一个有界问题 |
| `anatomia-storyboard-reviewer` | 校验并冻结分镜 revision |
| `anatomia-asset-handoff-builder` | 准备 package 并交给下游 owner |
| `anatomia-scaena-learning-loop` | 只路由已复核证据；learning CLI 尚未发布 |

维护者 planned runtime（如 `anatomia-vlm-codex-interaction`）留在 Anatomia 代码仓，不从这里安装。
