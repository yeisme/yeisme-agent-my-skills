---
name: podcast-scriptwriter
description: Use when writing Chinese podcast scripts, episode outlines, host notes, interview flows, monologues, transitions, retention points, and listener takeaways.
---

# 中文播客脚本写手

把想法变成听得下去、有节奏的中文节目。

## 输入

- 单集主题、听众、形式、时长、主持人声音、素材和嘉宾信息。
- 是否独白、访谈、圆桌、叙事节目、需要口播稿还是主持人提纲。

## 输出

- 单集承诺、开场钩子、分段地图、转场、结尾收获。
- 独白口播稿或访谈问题弧线。
- 听众重新进入提示点、追问和剪辑备注。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../short-video-scriptwriter/references/audio-video-live-script-playbook.md`：需要短视频、剧本、直播或播客时间线与制作限制时读取。

## 工作流

1. 明确单集承诺、听众、形式、时长、主持人声音和素材。
2. 设计开场钩子、分段地图、故事/证据节点、转场和结尾收获。
3. 用有节奏的口语写作，设置路标和听众重新进入提示点。
4. 访谈节目准备问题弧线和追问。
5. 检查是否有太长的无路标段落。

## 质量门槛

- 开场必须让听众知道为什么继续听。
- 口播稿自然，不像论文朗读。
- 访谈问题要能引出故事和细节，不只问泛泛观点。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
