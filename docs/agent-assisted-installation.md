# 云端集成 Yeisme AI 做剧 Skills

AI 做剧 Skills 云端仓库：

```text
https://github.com/yeisme/ai-drama-skills
```

仓库包含做剧路由、故事架构、角色、Showrunner、导演、视觉、连续性、声音剪辑、评审和生产编排等 Skills。默认先安装 `ai-drama-router`，让它根据剧型和当前阶段选择最小组合，不需要一次安装全部矩阵。

## 直接复制给 Agent

```text
请把 Yeisme AI 做剧 Skills 集成到当前项目。

云端仓库：
https://github.com/yeisme/ai-drama-skills

先执行最小安装：
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes

集成要求：
1. 先只安装并读取 ai-drama-router，把它作为短剧、漫剧、电视剧、电影、单元剧、喜剧和音频剧的统一入口，不要一次安装全部 Skills。
2. 读取当前项目最近的 AGENTS.md、已有故事资料和制作约束，不覆盖现有 owner、技术栈、测试命令或更严格的权限规则。
3. 根据我的目标识别剧型、当前阶段、已有素材、目标产物和最小 ContextPack。
4. 由 ai-drama-router 选择一个 primary Skill，最多附加一个必要 constraint。需要追加 Skill 时，继续从同一个仓库按名称安装：
   npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill <skill-name> --yes
5. 如果我要求快速测试、demo 或概念验证，走最短可运行路径；如果我明确开始正式项目或 MVP，再进入完整但渐进的策划、架构、制作、评审和验证流程。
6. 如果我明确说不用完整工作流、直接做或正常执行，就停止加载额外项目流程，只保留当前做剧任务真正需要的 Skills。
7. grill-me、creative grilling、完整评审、QA 和发布流程只能按需触发，不要因为安装了做剧入口就自动运行。
8. 安装后确认 ai-drama-router/SKILL.md 可读，并报告：仓库 URL、实际安装路径、已启用 Skills、当前 DramaRoutePlan、没有启用的 Skills、下一步建议和仍需授权的外部动作。

不要 commit、push、发布、部署、调用付费模型或写入生产系统，除非我明确授权。
```

## 最短安装命令

Skills CLI 会自动检测当前支持的 Agent：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-router \
  --yes
```

需要明确安装给 Codex 和 Claude Code 时：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill ai-drama-router \
  --agent codex \
  --agent claude-code \
  --copy \
  --yes
```

先查看云端仓库提供的全部 Skills：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills --list
```

## 按任务追加 Skill

不要预装完整矩阵。先由 `ai-drama-router` 确认当前任务，再从同一 URL 安装它选择的 Skill：

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills \
  --skill <skill-name> \
  --yes
```

常见选择示例：

| 任务 | 可能选择的 Skill |
| --- | --- |
| 选择短剧、漫剧、电影或音频剧形态 | `ai-drama-format-strategist` |
| 设计故事冲突、节拍、钩子和结局 | `ai-drama-story-architecture` |
| 设计人物、秘密、关系和角色状态 | `ai-drama-character-engine` |
| 规划季、集、长期弧线和下一集交接 | `ai-drama-showrunner` |
| 场面调度、表演、机位和镜头意图 | `ai-drama-director` |
| 视觉 brief、关键帧、分镜和风格连续性 | `ai-drama-visual-language` |
| 检查人物、服装、道具、空间和时间连续性 | `ai-drama-continuity-supervisor` |
| 剪辑节奏、声音、音乐、字幕和组接 | `ai-drama-edit-and-sound` |
| 多评委比较候选结果并提出修复 | `ai-drama-critic-panel` |
| 成本、版权、供应商、重试预算和交付门 | `ai-drama-producer` |

最终选择以 Router 读取到的项目上下文为准。

## 需要跨项目 Profile 管理时

只有需要统一管理 Skill source、`.agents/.claude` 双 runtime 和项目 profile 时，才使用聚合仓库：

```text
https://github.com/yeisme/yeisme-agent-my-skills
```

```bash
git clone --recurse-submodules \
  https://github.com/yeisme/yeisme-agent-my-skills.git \
  "$HOME/.local/share/yeisme-agent-my-skills"

"$HOME/.local/share/yeisme-agent-my-skills/scripts/skills.sh" \
  --project "$PWD" \
  init

"$HOME/.local/share/yeisme-agent-my-skills/scripts/skills.sh" \
  --project "$PWD" \
  profile add ai-drama-router

"$HOME/.local/share/yeisme-agent-my-skills/scripts/skills.sh" \
  --project "$PWD" \
  sync

"$HOME/.local/share/yeisme-agent-my-skills/scripts/skills.sh" \
  --project "$PWD" \
  validate
```

普通项目优先使用前面的 `npx skills add`，不要为了安装一个 Router 引入完整 profile 管理。

## 云端更新提示词

```text
请从 https://github.com/yeisme/ai-drama-skills 更新当前项目已经启用的做剧 Skills。先列出当前安装项和本地修改，只更新现有 Skills，不自动增加完整矩阵。更新后重新读取 ai-drama-router，确认现有 DramaRoutePlan 仍然有效，并报告更新前后版本、实际安装路径、验证结果和兼容性风险。不要覆盖未提交的本地修改。
```

## 验收结果

Agent 完成后至少应报告：

- 云端仓库 URL；
- 实际安装目录；
- 已启用的 Router、primary 和 constraint；
- 当前剧型、阶段、输入和目标产物；
- 没有安装或没有触发的高成本工作流；
- 验证结果；
- 尚未执行的 push、发布、部署、付费调用和生产写入。
