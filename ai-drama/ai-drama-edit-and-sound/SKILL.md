---
name: ai-drama-edit-and-sound
description: Use when planning AI drama shot order, information release, attention rhythm, pauses, music, ambience, Foley, dialogue, subtitles, timing, or episode assembly review.
---

# AI Drama Edit And Sound

## 目标

把镜头、声音和字幕组织成观众可理解的时间体验。剪辑不是拼接文件，而是控制信息、注意力和情绪回收。

## 工作流

1. 读取 Episode/Scene/Shot refs、DirectorDecisionGraph、dialogue、duration 和 subtitle constraints。
2. 标注每个镜头的进入信息、退出问题、情绪强度、节奏和可删性。
3. 设计 cut order、transition、pause、ambience、Foley、music cue、dialogue 和 subtitle timing。
4. 检查画面动作、声音方向、字幕和总时长的同步。
5. 输出 `AssemblyProposal`、`SoundPlan` 或 finding，交给 Scaena assembly/review owner。

## 质量门槛

- 删除一个镜头或声音后必须能说明损失；
- 声音不能只做装饰，至少承担空间、信息、情绪或转场功能；
- 字幕不能遮挡关键主体，时间线必须可复算；
- 音画冲突、未授权素材、时长超限和空白段落必须阻塞或进入 Review。

## 边界与验证

不直接导出最终平台包、不上传、不发布；assembly 和 delivery 由 Scaena 管理。

```bash
cd /workspaces/yeisme-agent/agent/scaena
task test:architecture
task test:integration
```
