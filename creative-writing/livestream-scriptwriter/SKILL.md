---
name: livestream-scriptwriter
description: Use when preparing Chinese livestream scripts, product explanations, host talking points, rhythm plans, objection handling, urgency, transitions, interaction prompts, and closing loops.
---

# 中文直播脚本写手

写主播能现场讲出来的中文脚本，并准备低互动时的兜底话术。

## 输入

- 产品/主题、平台、主播声音、观众痛点、优惠、合规限制和直播时长。
- 证明素材、FAQ、禁用承诺、库存/活动真实情况和互动目标。

## 输出

- 直播节奏表：开场、信任建立、产品证明、异议处理、互动、紧迫感、循环收口。
- 主播话术、转场句、低互动兜底话术和评论区问题。
- 合规风险和需要用户确认的优惠/库存/承诺。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../short-video-scriptwriter/references/audio-video-live-script-playbook.md`：需要短视频、剧本、直播或播客时间线与制作限制时读取。

## 工作流

1. 明确产品/主题、平台、主播声音、观众痛点、优惠和限制。
2. 设计开场、信任建立、产品证明、异议处理、紧迫感、互动提示和循环收口。
3. 按分段标注时长，准备低互动时的兜底话术。
4. 把常见异议写成可回答脚本。
5. 检查紧迫感是否真实，避免虚假稀缺。

## 质量门槛

- 话术要能口播，不写长段书面语。
- 紧迫感必须来自真实活动或库存，不编造。
- 医疗、金融、功效、价格承诺必须谨慎并提示用户确认。

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
