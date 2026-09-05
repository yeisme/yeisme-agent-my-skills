## 为什么

现有 operator 与 prompt repository router 仍把中文描述成 source template，也缺少新建英文模板、维护中文审阅译文和 CLI-authored metadata 的专用 Skill。

## 变更内容

- 更新 operator、router、Scaena 与 Eikona Skill 的语言规则。
- 新增 `template-registry-template-author`。
- 增加 locale reference、错误恢复和新模板 CLI 流程。
- 通过 profile 脚本启用并同步到 root 与内容仓。

## 影响

Skill 不复制模板正文、不手写 metadata、不替用户确认，也不执行 provider。
