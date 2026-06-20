---
name: xhs-viral-structure-writer
description: Use when turning a topic, draft, or source material into Xiaohongshu-friendly structure with hook, readable body, save-worthy points, interaction cue, anti-AI polish, and platform risk awareness.
---

# 小红书爆款结构写手

把主题、草稿或素材整理成更适合小红书阅读与互动的中文笔记结构。

## 输入

- 主题、原始草稿、目标读者、账号定位、素材证据和希望触发的动作。
- 参考结构、平台赛道、禁用表达、是否需要图卡脚本。

## 输出

- 重构后的笔记结构和正文。
- 标题方向、封面短句、正文、话题标签和评论区引导。
- 去 AI 味检查和需要补充真实细节的问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../xhs-note-writer/references/xhs-content-playbook.md`：需要标题公式、正文结构、图卡页序和素材拆帖模板时读取。
- `../xhs-note-writer/references/xhs-title-card-and-risk-checklist.md`：需要封面标题、3/6/9 图卡和热点/个人品牌风险检查时读取。

## 工作流

1. 判断内容模式：种草、避坑、教程、清单、成长、观点、复盘或故事。
2. 设计结构：开头钩子、个人场景、核心信息、可收藏步骤、结尾互动。
3. 重写正文，保留用户本人事实，缺失细节以问题列出。
4. 安排标题、封面短句、正文节奏和标签。
5. 删除空泛总结、模板连接词、过度整齐句式和虚假热情。

## 质量门槛

- 每篇笔记必须有点开理由和收藏理由。
- 结构服务真实内容，不套模板牺牲可信度。
- 不声称保证涨粉、保证转化或绕过平台机制。

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
