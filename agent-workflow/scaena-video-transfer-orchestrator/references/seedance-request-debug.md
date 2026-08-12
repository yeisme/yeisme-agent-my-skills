# Seedance 请求调试速查

这个参考规定回答“最终提示词是什么”的最低信息层级。它只描述调试方法，不保存或展示 raw prompt、provider body、签名 URL、object key 或凭据。

## 命令

```bash
scaena video task prompt \
  --project /workspaces/yeisme-agent/data/scaena-video-transfer-lab \
  --model doubao-seedance-2-0-260128 \
  --task <task-id> \
  --agent
```

这是本地账本查询：零 provider 调用、零 credential lookup、零费用。`--agent` 只给低 token 的 provenance facts，不展开 `data`。需要本地文件比对时，追加 `--verify-prompt-file ./prompts/E001-G01.txt`；结果为 `matched|mismatched|unavailable|not_requested`，不会输出文件内容或路径。

当且仅当问题涉及媒体顺序、错误角色 asset 或 provider 参数时，升级到：

```bash
scaena video task debug \
  --project /workspaces/yeisme-agent/data/scaena-video-transfer-lab \
  --model doubao-seedance-2-0-260128 \
  --task <task-id> \
  --json
```

## 回答模板

1. **原始来源**：说明 `inline_flag` 或 `prompt_file`、SHA-256 摘要前缀、字节数与 file verification；prompt file 的正文由操作者本地查看。完整摘要仅在显式 JSON data 内可用。
2. **变换规则**：说明 Scaena 是否原样传递；Tokenspace mixed reference 是 identity transform。
3. **媒体绑定**：按 `content[]` ordinal 列出 `text`、`reference_video`、`reference_image` 的 asset/ref 及 internal semantic role。
4. **参数**：model、时长、ratio、resolution、audio、API surface 和 filing inclusion。
5. **推断边界**：解释这是输入事实；Seedance 输出偏差要分为媒体绑定错误、source range/action anchor 不足、或模型采样。像素锁定是否成功只由蒙版合成和帧差验证。

## 分流

| 调试结果 | 判断 | 修复 |
| --- | --- | --- |
| `content[]` 含有不该出现的角色 asset | bundle/resolver bug | 修复 candidate group 的 allowed character 和 bundle，创建新 draw。 |
| `content[]` 正确，产物却新增角色/错误动作 | 模型采样或参考解释 | 缩短 source range；保留源动作 anchor；在预算内定向 reroll。 |
| prompt digest 与本地文件不一致 | 操作输入漂移 | 用正确版本文件重新创建已批准的 draw。 |
| `capture_status=not_captured` | 历史任务没有安全快照 | 不伪造正文；利用 bundle lineage 分析，后续改用 `--prompt-file`。 |
| 蒙版外差异不为零 | composite failure | 停止交付，修复 mask/对齐；不要用新的 prompt 覆盖验收失败。 |
