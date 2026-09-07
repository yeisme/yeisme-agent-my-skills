# 持久化与编译

## 可复用流程：recipe

Recipe 保存 exact template refs、步骤、依赖、bindings 和 presets。使用 CLI 生成，不手写 JSON：

```bash
template-registry prompt recipe init --path workflows/campaign.json --id campaign-production --json

printf '%s' '{"path":"workflows/campaign.json","step":{"id":"image_prompt","ref":"promptrepo://official/image/xhs-product-cover-v2@2.0.0?locale=en","locale":"en","output_requirement":"One reviewed image-generation prompt"}}' |
  template-registry prompt recipe step --stdin --json

printf '%s' '{"path":"workflows/campaign.json","step":{"id":"video_prompt","ref":"promptrepo://official/video/ai-drama-shot-video-generation@1.0.0?locale=en","locale":"en","depends_on":["image_prompt"],"bindings":{"reference_image":{"kind":"step_output","ref":"image_prompt"}},"output_requirement":"One shot-video prompt bound to the accepted image artifact"}}' |
  template-registry prompt recipe step --stdin --json

template-registry prompt recipe validate --path workflows/campaign.json --json
```

`step_output` 表示等待前序实际产物。前序 Prompt 编译完成并不等于图片或视频已经生成；实际产物需由领域工具生成、审核，再导入会话绑定。

## 一次任务：session

```bash
template-registry prompt session create --recipe-file workflows/campaign.json --goal '制作一套已审阅的商品图片与短视频提示包' --json
template-registry prompt session next --session <session-id> --json
```

资料使用 `prompt source import`，候选字段使用 `session update`，用户真实确认使用 `session confirm`。每次修改携带最新 `expected_revision`。Session 保存资料快照、来源、字段状态、确认、编译和导出历史；Agent 不改 SQLite 或 metadata。

编译只消费固定输入：

```bash
template-registry prompt compile --session <session-id> --expected-revision <revision> --json
template-registry prompt export --compile <compile-id> --output ./prompt-package --format directory --mode portable --json
template-registry prompt bundle verify --path ./prompt-package --json
```

修改模板、资料、字段或前序产物会使受影响步骤过期。保留旧编译，生成新版本；不要默认使用 stale 产物。
