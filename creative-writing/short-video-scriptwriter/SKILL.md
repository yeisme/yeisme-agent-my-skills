---
name: short-video-scriptwriter
description: Use when writing Chinese short-video scripts for Douyin, Bilibili-style videos, or social shorts with first-three-second hook, timeline, voiceover, visuals, captions, transitions, and CTA.
---

# 中文短视频脚本写手

写能拍出来的中文脚本，不把文章拆行伪装成脚本。

## 输入

- 平台、时长、观众、主题、证据/素材、拍摄限制和账号语气。
- 是否真人出镜、口播、混剪、产品展示、字幕密度和行动引导。

## 输出

- 3 个前三秒钩子候选。
- 按时间线输出画面、口播、字幕、转场和行动引导。
- 纯口播版本、拍摄限制提醒和剪辑注意事项。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../short-video-scriptwriter/references/audio-video-live-script-playbook.md`：需要短视频、剧本、直播或播客时间线与制作限制时读取。

## 工作流

1. 明确平台、时长、观众、主题、证据和拍摄限制。
2. 先给出 3 个前三秒钩子候选。
3. 按时间线起草：画面、口播、字幕、转场和行动引导。
4. 检查节奏、画面可拍性、口播顺畅度、时长适配和行动引导自然度。
5. 用户需要时提供纯口播版本。

## 质量门槛

- 每个镜头或段落都应有信息变化。
- 口播要能自然读出来，不写书面长句。
- 画面必须可拍或可剪，不写无法实现的镜头。

## Auctra 轻集成

- 普通脚本可直接输出 Markdown。
- 结构化项目中可建议 `auctra text new short_video_script --title "..." --platform douyin --json`。
- 需要审稿、导出分镜或归档时使用 Auctra review/export。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
