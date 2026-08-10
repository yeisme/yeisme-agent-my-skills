# 视频参考合同与语义

## 何时读取

当输入包含 Blender 预演、动作参考、相机参考、姿态参考或 Seedance `reference_video` 时读取本文件。它描述 Skill 的判断边界，不替代 Scaena 的 SDK、数据库或 OpenSpec 合同。

## 参考角色

| role | 应保留 | 可由生成模型重解释 | 典型检查 |
| --- | --- | --- | --- |
| `camera` | 相机路径、景别、俯仰/摇移、视线方向 | 焦段微调、运动平滑 | 相机运动相位和构图锚点 |
| `motion` | 动作顺序、速度变化、关键相位 | 细节表演、手指和布料 | 起势、接触、转折、收势 |
| `composition` | 主体相对位置、前中后景关系、留白 | 背景细节、材质和光线 | 主体占比、遮挡、屏幕方向 |
| `pose` | 姿态、重心、朝向、肢体关系 | 面部和服装细节 | 身份、骨架、接触关系 |
| `geometry` | 物体相对形状、空间关系和路径 | 非关键材质与纹理 | 道具、地面、障碍物和空间连续性 |

## 持久化最小字段

持久化只保存可重建的引用和事实：

- `asset_ref`、`asset_version`、内容 `digest`、权限/来源和 review 状态；
- `role`、序号、镜头/主体绑定、裁剪段、目标时长、画幅和 fps（若已确认）；
- `ShotIntent`/`ShotGenerationSpec` refs 与 digest、capability ref、policy/version 和幂等键；
- 生成 receipt、输出 artifact refs、连续性 findings 和下一步 owner action。

不要持久化原始本地路径作为唯一身份、一次性 URL、signed URL、API key、provider payload 或完整 prompt。

## 门禁顺序

```text
rendered media
  -> asset ingest + probe
  -> rights/review
  -> shot binding
  -> frozen input bundle
  -> capability/cost admission
  -> owner bridge / explicit canary
  -> CAS import, pending_review
  -> continuity review
  -> Scaena selection / production acceptance
  -> assembly / export
```

任一前置事实缺失都应停在 `needs_input`、`needs_contract` 或 `blocked`。`provider succeeded` 不能替代最后三步。

## 失败分类

- `.blend` 只有场景数据、没有渲染视频：`needs_input`；
- 视频已登记但没有探测事实或权限：`blocked`；
- 只有图片 `VisualReferenceBinding`、没有视频输入合同：`needs_contract`；
- capability 不证明支持该模型/模式：`blocked`，不静默降级或换模型；
- 生成结果没有 CAS/import receipt：`needs_contract`，不得标记为 production asset；
- 连续性发现动作、相机、主体或空间 blocker：`needs_human_review` 或 `repair`，不得自动接受。

## Owner handoff

- 镜头语义和镜头理由：`ai-drama-director`、`ai-drama-visual-language`；
- 主体/风格/权限和冻结：`scaena-subject-asset-readiness`；
- 执行、恢复、review、assembly：`scaena-production-operator`；
- 动作/镜头/主体/空间/时间检查：`ai-drama-continuity-supervisor`；
- 节奏、声音、字幕和 assembly proposal：`ai-drama-edit-and-sound`。

以上 Skills 只能产生 proposal、finding 或 owner action，不拥有 Scaena canonical state。
