---
name: screenplay-scene-writer
description: Use when writing or revising Chinese screenplay, stage, radio-drama, or scene scripts with scene objective, conflict, action line, dialogue, subtext, blocking, and producible transition.
---

# 中文场景剧本写手

写能被表演、拍摄或录制的中文场景。

## 输入

- 场景目标、地点/时间、人物、冲突、转折点、制作限制和媒介。
- 人物关系、隐藏信息、对白风格、必须保留的事件和时长。

## 输出

- 标准化场景稿：场景标头、动作线、对白、停顿、转场。
- 人物目标、潜台词、权力变化和制作限制说明。
- 可选改写版或排练提示。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../short-video-scriptwriter/references/audio-video-live-script-playbook.md`：需要短视频、剧本、直播或播客时间线与制作限制时读取。

## 工作流

1. 明确场景目标、地点/时间、人物、冲突、转折点和制作限制。
2. 定义每个角色想要什么、隐瞒什么。
3. 动作线写可见行为，不写小说式内心说明。
4. 对白要有潜台词和权力变化。
5. 以清晰结果或可制作转场收束。

## 质量门槛

- 场景有目标和冲突。
- 动作可制作、可表演。
- 对白不解释画面已经能呈现的内容。

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
