---
name: screenplay-scene-writer
description: Use when writing, revising, or converting Chinese screenplay, short-drama, stage, radio-drama, or scene scripts from story material or accepted Auctra dramatic recipes into producible scenes with scene objective, conflict, visible action, dialogue, subtext, blocking, transition, and source-safe screenplay semantics.
---

# 中文场景剧本写手

写能被表演、拍摄或录制的中文场景。核心区别：小说是给读者阅读的，剧本是给剧组拍摄或演出的；剧本只写最终观众能看到、听到，且制作团队能执行的内容。

## 输入

- 场景目标、地点/时间、人物、冲突、转折点、制作限制和媒介。
- 人物关系、隐藏信息、对白风格、必须保留的事件和时长。
- 可选：已接受的 Auctra Development Brief、scene card、dramatic recipe、production constraints 和 evidence refs。

## 输出

- 标准化场景稿：场景标头、动作线、对白、停顿、转场。
- 人物目标、潜台词、权力变化和制作限制说明。
- 小说材料转译说明：哪些心理、背景、文学描写被改成动作、表情、道具、环境声、对白或转场。
- 可选改写版或排练提示。

## 格式与编剧符号

- 修订已有剧本时保留作者的 `△/▲`、VO/OS、转场和场号，不批量“规范化”掉来源标记。
- canonical Fountain/剧本正文优先使用标准场景标头、人物提示、对白、括号提示和转场；不要无条件把 emoji 插入正文。
- 需要工作稿图例或 Studio 语义说明时，可使用 `§ 集`、`🎬 场`、`⌖ 地`、`◷ 时`、`👥 人`、`□ 道`、`△/▲ 动作`、`@ 角色`、`💬 对白`、`VO`、`OS`、`→ 转场`、`↶ 闪回`、`♪ 声音`、`CC 字幕`、`✦ 特效`、`▧ 参考图`。
- 图标只是展示；每个符号必须有文本标签。未知格式保持“未识别/待审”，不能猜成动作或对白。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `references/screenplay-vs-novel.md`：需要把小说、散文式叙述、心理描写或作者讲述改成可拍剧本时读取。
- `../short-video-scriptwriter/references/audio-video-live-script-playbook.md`：需要短视频、剧本、直播或播客时间线与制作限制时读取。

## 工作流

1. 明确场景目标、地点/时间、人物、冲突、转折点和制作限制。
2. 如果用户要求“参考热门剧/样本写类似剧本”，先使用 `$auctra-screenplay-pattern-research` 获取已审核的多来源 recipe；不要直接模仿单一样本台词、专名或独特桥段。
3. 定义每个角色想要什么、隐瞒什么。
4. 如果输入是小说或梗概，先标出不能直接拍摄的内容：内心独白、作者解释、抽象感受、细腻文学比喻、背景概述和时间跳跃。
5. 将不可拍内容转成可拍元素：动作、表情、道具、场面调度、环境声、对白、沉默、字幕、闪回、蒙太奇或可执行转场。
6. 动作线写可见行为，不写小说式内心说明；环境只写拍得到、听得到、能影响表演或镜头的信息。
7. 对白要能被演员说出口，有潜台词和权力变化；不能用对白替作者解释一切。
8. 以清晰结果或可制作转场收束。

## 质量门槛

- 场景有目标和冲突。
- 动作可制作、可表演。
- 所有情绪必须通过动作、表情、对白、沉默、道具或声画细节表现，不直接写“他很害怕”“她终于释怀”等不可见判断。
- 不写摄影机拍不到的内容，例如“想起”“放下”“无法原谅”“初恋般的味道”，除非已转成闪回、照片、对白、动作或声音线索。
- 时间跨度、回忆和背景信息必须有可制作方案，例如字幕、闪回、蒙太奇、新闻/文件/照片、角色行为或渐进式对白。
- 对白不解释画面已经能呈现的内容。
- Recipe 影响的是结构、节奏、角色功能和生产约束；输出不得复现样本专名、长台词或独特情节表达。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。
- 不读取或使用 holdout 正文作为写作上下文；只有 Auctra 明确允许的 accepted recipe/project refs 可进入场景写作。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
