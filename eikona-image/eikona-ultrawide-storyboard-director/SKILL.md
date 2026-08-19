---
name: eikona-ultrawide-storyboard-director
description: Use when designing ultrawide continuous-space storyboards, action blocking boards, short-drama previs boards, or historical battle panorama boards for Eikona; produce scene beats, prompts, generation commands, video-cleanup guidance, review, and handoff steps.
---

# Eikona 超宽故事看板导演

把剧情、动作冲突、历史推演或短视频镜头调度设计成 3:1 或更宽的连续空间故事看板：同一背景空间内，用多个时间点定格展示角色走位、冲突升级、关键转折和落点。

## 输入

- 场景主题、空间类型、角色、剧情节点、动作节奏、时间顺序和目标用途。
- 可选：是否用于视频生成、是否需要箭头/圈线/编号/时间线、参考图、禁用元素、历史事实来源、Scaena project/shot refs 与 generation preflight。

缺剧情节点时先提取 4-6 个 beats；缺空间信息时先给出 2-3 个适合连续调度的空间候选。

## 参考资料

需要详细模板、适用场景和视频转化规则时读取：

- `references/ultrawide-storyboard-playbook.md`

## 工作流

1. 先判断是否属于 Scaena production。若是 episode/shot/cover/motion context，必须先调用 `$scaena-subject-asset-readiness`；没有 current passed preflight 时只能输出 planning/lookdev brief，不得输出 production generation command。
2. 明确用途：剧情规划、动作调度、连续性检查、历史战役推演、视频镜头预演。
3. 拆成 4-6 个时间点 beats，例如：追逐 -> 拦截 -> 近身冲突 -> 环境破坏 -> 借环境反击 -> 逃离/落点。
4. 设计一个连续背景空间：入口、移动路径、冲突中心、遮挡物、可互动道具、出口。
5. 决定标记策略：规划看板可用箭头、编号、圈线、时间线；视频参考图必须输出去标记 clean-cinematic 版本。
6. 加载 `eikona-file-prompt-workflow`，将 planning board 与 clean video-reference 分成两个 prompt 文件，保存到 `prompts/story/storyboard/<collection>/`；Scaena production 使用 `prompts/scaena/storyboard/<shot-ref>/` 并引用 preflight/frozen subject refs。
7. 输出 prompt 文件、负面约束、runbook、本地验证命令、真实生成命令、review/feedback/handoff 下一步。

## Prompt 结构

必须显式包含：

- ultrawide continuous-space storyboard 或 panoramic action blocking board。
- 一个统一背景空间，而不是分隔漫画格。
- 多个时间点的同一角色/队伍位置，使用 ghosted/time-slice composition 或 sequential frozen moments。
- 从左到右或按空间路径的动作顺序。
- 关键道具、障碍、入口、出口和冲突升级点。
- 仅当用于 planning board 时加入 arrows, circled hotspots, labels, timeline markers。
- 当用于视频时加入 clean cinematic frame, no arrows, no labels, no circles, no timeline marks。

## 命令示例

以下直接生成示例适用于独立 planning，或已通过 Scaena production preflight 的上下文。Scaena context 无 preflight 时不要运行真实生成命令。

输出模式：例行自动化用 `--agent`；非终态 run 用 `eikona watch <run_id> --events` 观察；脚本/CI 用 `--json --compact`（共存期内裸 `--json` 仍是 legacy full）；取证用 `--json --full`。

本地验证规划看板：

```bash
eikona generate --model fixture:image --aspect 3:1 --size 1536x512 --input prompts/story/storyboard/night-market-conflict/prompts/01-planning-board.md --dry-run --agent
```

真实生成规划看板：

```bash
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --aspect 3:1 --size 1536x512 --input prompts/story/storyboard/night-market-conflict/prompts/01-planning-board.md --agent
eikona review packet <run_id> --agent
eikona feedback accept <run_id> --artifact <artifact_id> --reason spatial_continuity --reason beat_clarity --agent
eikona assets handoff <artifact_id> --agent
```

视频参考图必须生成干净电影镜头：

```bash
eikona generate --use-channel openai --model openai/gpt-5.4-image-2 --aspect 16:9 --size 1536x864 --input prompts/story/storyboard/night-market-conflict/prompts/02-clean-video-reference.md --agent
```

## 输出

- Beats 表：编号、时间点、角色位置、动作、冲突升级、空间落点。
- 空间调度 brief：背景、入口/出口、路径、遮挡、道具、相机观察点。
- 分类目录、集合 README，以及 planning board 和 clean video-reference 两个独立 prompt 文件。
- 本地验证、真实生成、review、feedback、handoff 命令。

## 质量标准

- 画面必须是连续空间，不是普通分镜格或拼贴海报。
- 角色运动路径、冲突升级和落点必须一眼可读。
- 箭头、文字、圈线和时间线只作为导演调度参考；不把它们当成最终视频画面元素。
- 动作冲突类看板适合转视频；线索、调查、地图推演类更适合剧情规划和连续性检查。
- 历史战役或现实事件必须区分已知事实、推演假设和视觉简化，不伪造来源。
- Scaena production 必须使用 frozen subject/style/location/prop references；planning board 的同一角色多时点表现不能被当作角色一致性验收。

## 边界

- 不生成真实个人或受版权保护角色的未经授权复刻。
- 不把私密剧本、原始提示词、供应商载荷或完整思维链写入结构化资产。
- 不声称 Eikona 已完成视频生成；本 skill 只产出图像看板和视频参考图提示。
- 不绕过 Scaena subject freeze、shot binding 或 generation preflight；无 preflight 时只允许 non-production planning/lookdev。
